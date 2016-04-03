Title: Ansible问题总结
Date: 2016-04-03 18:43
Category: 自动化
Tags: 自动化
Slug: Ansible问题总结
Author: 李俊伟

##问题描述
	paramiko: The authenticity of host '[*.*.*.*]:8822' can't be established.
	The ssh-rsa key fingerprint is f22cae7f4b39a92d4a38f97b9102a57e.
	Are you sure you want to continue connecting (yes/no)?

用ansible去管理一台新机器时遇到了上面的问题，需要输入yes交互才能继续执行命令，因为这样的问题导致批量执行的任务有些没有执行。
解决办法也很简单

修改ansible.cfg文件中的

	#host_key_checking = False   关闭第一次使用ansible连接客户端是输入命令提示
默认是有注释的，去掉注释就行。

