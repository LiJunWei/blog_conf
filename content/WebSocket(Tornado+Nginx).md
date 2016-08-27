Title: WebSocket使用初探(Tornado+Nginx)
Date: 2016-08-27 16:52
Category: WebSocket
Tags: WebSocket
Slug: WebSocket使用初探(Tornado+Nginx)
Author: 李俊伟
Summary: Tornado开发WebSocket应用，Nginx反向代理支持WebSocket协议从而实现网站长连接

## 使用场景
在web开发中有时候需要实时获取数据，可以采用的方法也很多，比如ajax轮询，长连接等。之前项目中有一个需求是实时的日志展示，实时性要求高
还有根据历史监控数据进行趋势图的绘制，数据量巨大，等待时间长。那么如果使用http请求来处理则面临着超时的问题，如果用ajax频繁的轮询将对服务器
造成很大的压力。websocket提供了客户端和服务器进行双向实时的全双工通信的方法。并且绝大多数现代浏览器都支持websocket，因此需要使用
nginx对websocket服务进行反代和负载均衡，nginx从1.3版本后开始支持websocket。项目用到的tornado框架也原生支持websocket，看来可以尝试
用websocket来尝试解决问题。

## Tornado的支持
tornado对websocket支持的很好，通过继承tornado.websocket.WebSocketHandler类就可以实现对websocket连接的处理。websocket是在标准
http上实现的，websocket中的握手和http中的握手兼容，它使用http中的Upgrade协议头将连接从http升级到WebSocket,从源码上可以看出
WebSocketHandler继承了tornado.web.RequestHandler，因此websocket也可以通过get_argument方法获取ws://URL?**=传来的参数。
WebSocketHandler提供了一系列方法用以处理连接和消息收发，源码中的docstring描述得很清楚，源码是最好的文档没有之一。

    class WebSocketHandler(tornado.web.RequestHandler):
    """Subclass this class to create a basic WebSocket handler.

    Override `on_message` to handle incoming messages, and use
    `write_message` to send messages to the client. You can also
    override `open` and `on_close` to handle opened and closed
    connections.

    See http://dev.w3.org/html5/websockets/ for details on the
    JavaScript interface.  The protocol is specified at
    http://tools.ietf.org/html/rfc6455.

    Here is an example WebSocket handler that echos back all received messages
    back to the client:

    .. testcode::

      class EchoWebSocket(tornado.websocket.WebSocketHandler):
          def open(self):
              print("WebSocket opened")

          def on_message(self, message):
              self.write_message(u"You said: " + message)

          def on_close(self):
              print("WebSocket closed")

    .. testoutput::
       :hide:

    ...

## Nginx配置反向代理和负载均衡

    upstream tornadoes {
        server 127.0.0.1:7000;
        server 127.0.0.1:7001;
    }

    server {
        listen 8000;
        server_name ***.com;

        location / {
            proxy_pass http://tornadoes;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
        }
    }

nginx默认采用循环的方式分配请求，循环的将请求分配到upstream中定义的服务地址。location中的定义对支持websocket必不可少。



