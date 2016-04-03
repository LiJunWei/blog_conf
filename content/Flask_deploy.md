Title: Flask部署
Date: 2016-01-31 14:27
Category: Python
Tags: Python, Flask
Slug: Flask部署
Author: 李俊伟

## 前言
开发完公司的数据库自动化平台，接下来就是要部署测试，之前没真正部署过，这次正好学习了，写下来部署的过程。项目用到Flask，部署采用的是gunicorn+supervisor+Nginx的方式，用gunicorn做容器，supervisor管理进程，Nginx做反向代理，以下是详细过程。

## 配置Python虚拟环境
先安装Python2.7  

	wget http://python.org/ftp/python/2.7/Python-2.7.tar.bz2 
	tar -jxvf Python-2.7.tar.bz2   
	cd Python-2.7
	./configure  后面可以加上你希望安装的路径 比如 --prefix=/usr/local ，默认是/usr/local   
	make & make install   
	make clean & make distclean   
安装pip，virtualenv   
因为系统默认是python2.6的，所以通过yum安装的pip会默认装到2.6的目录下，而且yum还依赖2.6，所以如果直接修改系统默认的python版本会导致无法使用yum，因此我通过distribute的方式安装easy_install继而安装pip。   

	wget https://pypi.python.org/packages/source/d/distribute/distribute-0.6.49.tar.gz      
	python distribute_setup.py #注意这里的python一定是你python2.7的路径下的python      
	mkdir myproject   
	cd myproject   
	virtualenv venv
安装需要的包   

	pip install -r requirements.txt #requirements.txt中记录了项目用到的所有包
安装gunicorn  
 
    pip install gunicorn  
安装supervisor

	pip install supervisor
    pip freeze > requirements.txt
	每次pip安装了新的库之后都要freeze一次，这是个好习惯  
## 配置supervisor
supervisor是基于Python的进程管理工具，可以用守护进程的方式执行程序。
  
	echo_supervisord_conf > supervisor.conf   # 生成 supervisor 默认配置文件   
这个文件放在哪里都可以，只要你执行supervisor的时候指定它就可以，但还是建议放到/etc下，这样好管理，在生成的默认配置文件底部有一个
include选项，用来包含要管理的程序的supervisor配置文件。

	[include]      
    files = /home/junweil/my_etc/supervisor/conf.d/*.conf    
下面是gunicorn的配置，命名为*.conf,放在supervisor/conf.d里面，我们应用的gunicorn，celery等程序的启动配置就应该放在          supervisor/conf.d中。  
  
	[program:wsgi]
  	command=/home/myproject/venv/bin/python/gunicorn -w 4 -b 0.0.0.0:5500 wsgi:app
  	directory=/home/myproject
  	startsecs=0
  	stopwaitsecs=0
  	autostart=false
  	autorestart=false
  	stdout_logfile=/home/my_log/gunicorn/gunicorn.log
  	stderr_logfile=/home/my_log/gunicorn/gunicorn.err   
下面是celery的配置，同gunicorn一样，我们的项目用到celery做异步任务的调度，如果不需要用到的可以忽略 
		  
	[program:celery]
	command=/home/myproject/venv/bin/python/celery worker -A app.celery --loglevel=info --beat
	environment=PYTHONPATH=/home/myproject
	directory=/home/myproject
	user=junweil
	stdout_logfile=/home/my_log/celery/celeryd.log
	stderr_logfile=/home/my_log/celery/celeryd.err
	autostart=true
	autorestart=true
	startsecs=10
## 安装nginx   
	CentOS yum install nginx
	Ubuntu apt-get install nginx
配置nginx，nginx主要用到了它的反向代理，详细配置就不列出来了。

		server {
			listen   80;
  	     	root /home/myproject/app;
  	     	server_name *****;
  	     	location / {
				proxy_pass	http://127.0.0.1:5500;
			}
		}
## 启动supervisor和nginx
运行命令`supervisord -c supervisor.conf`启动supervisor，这样刚才配置的gunicorn和celery就会以守护进程的方式运行起来。   
supervisor相关命令  
	
	supervisord -c supervisor.conf                          通过配置文件启动supervisor
	supervisorctl -c supervisor.conf status                 察看supervisor的状态
	supervisorctl -c supervisor.conf reload                 重新载入 配置文件
	supervisorctl -c supervisor.conf start [all]|[appname]	启动指定/所有 supervisor管理的程序进程
	supervisorctl -c supervisor.conf stop [all]|[appname]   关闭指定/所有 supervisor管理的程序进程
启动nginx

	nginx -c /etc/nginx/nginx.conf
nginx相关命令

	nginx -t 验证配置文件是否正确
	nginx -s reload 重新载入配置文件，并重启
在服务器上是nginx1.8版本的，我在自己虚拟机上实验的时候用的nginx1.9版本只要把配置文件放到sites-available文件夹中，并在sites-enabled中建立软连接指向sites-available文件夹中对应的配置文件即可。然后直接service nginx restart或/etc/init.d/nginx start
## flask启动文件 wsgi.py

	# coding: utf-8
	
	from app import create_app, db
	from flask import render_template
	
	app = create_app()
	
	
	@app.errorhandler(404)
	def not_found(error):
	    return render_template('error/404.html'), 404
	
	
	@app.errorhandler(500)
	def not_found(error):
	    return render_template('error/500.html'), 500
	
	
	@app.teardown_request
	def shutdown_session(exception=None):
	    db.session.remove()
	
	
	@app.teardown_appcontext
	def shutdown_session(exception=None):
	    db.session.remove()
	
	
	if __name__ == '__main__':
	    app.run()

