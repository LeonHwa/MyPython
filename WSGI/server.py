#!/usr/bin/env python
# -*- coding:utf-8 -*-

from  wsgiref.simple_server import  make_server
#导入自己编写的函数
from  hello import  application

#创建一个服务器  IP 为空（默认为本地） 端口8000 处理函数是application
httpd = make_server('',8000,application)
print 'server Http on 8000'
httpd.serve_forever()

