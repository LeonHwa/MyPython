#!/usr/bin/env python
# -*- coding:utf-8 -*-

def log(func):
    def wrapper(*args,**kwargs):
        print 'call %s' %(func.__name__)
        return func(*args,**kwargs)
    return wrapper

@log
def now():
    print '2015-3-25'

if __name__ == '__main__':
    now()