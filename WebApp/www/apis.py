#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

'''
JSON API definition.
'''

import json, logging, inspect, functools,time


def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)
def month_day_timeFilter(timestamp):
    timeArray = time.localtime(timestamp)
    # %Y-%m-%d %H:%M:%S"
    month_day_time = time.strftime("%m-%d", timeArray)
    return  month_day_time
def standard_timeFilter(timestamp):
    timeArray = time.localtime(timestamp)
    # %Y-%m-%d %H:%M:%S"
    month_day_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return  month_day_time

def removeSub(tag):
    return tag.replace('#', '')

class PageManager(object):
    def __init__(self,blog_count,page_index = 1,page_base = 6):
        self.blog_count = blog_count
        self.current_page = page_index
        if blog_count%page_base != 0 and blog_count > page_base:
            self.page_count = int(blog_count/page_base) + 1
        elif blog_count <= page_base:
            self.page_count = 1
        elif blog_count%page_base == 0:
            self.page_count = int(blog_count/page_base)


        self.offset = (page_index - 1) * page_base

        self.limit = page_base
        if page_index > self.page_count:
            self.limit = 0

        self.has_pre =  int(page_index > 1)
        self.has_next = int(page_index < self.page_count)


class APIError(Exception):
    '''
    the base APIError which contains error(required), data(optional) and message(optional).
    '''
    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message

class APIValueError(APIError):
    '''
    Indicate the input value has error or invalid. The data specifies the error field of input form.
    '''
    def __init__(self, field, message=''):
        super(APIValueError, self).__init__('value:invalid', field, message)

class APIResourceNotFoundError(APIError):
    '''
    Indicate the resource was not found. The data specifies the resource name.
    '''
    def __init__(self, field, message=''):
        super(APIResourceNotFoundError, self).__init__('value:notfound', field, message)

class APIPermissionError(APIError):
    '''
    Indicate the api has no permission.
    '''
    def __init__(self, message=''):
        super(APIPermissionError, self).__init__('permission:forbidden', 'permission', message)
