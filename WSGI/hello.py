#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
 environ：一个包含所有HTTP请求信息的dict对象；
 start_response：一个发送HTTP响应的函数。

start_response()函数接收两个参数，一个是HTTP响应码，一个是一组list表示的HTTP Header，每个Header用一个包含两个str的tuple表示。
"""
# def application(environ,start_response):
#     start_response('200 ok',[('Content-Type','text/html')])
#     return [b'<h1>Hello,Leon!</h1>']

#，从environ里读取PATH_INFO，这样可以显示更加动态的内容
def application(environ,start_response):
    start_response('200 ok',[('Content-Type','text/html')])
    path =  environ['PATH_INFO']
    method = environ['REQUEST_METHOD']
    print  method
    body = '<h1>Hello,%s</h1>' % (path[1:] or 'KK')
    return [body.encode('utf-8')]
