#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
def a(a, b=0, *c,  **f):
    pass

aa = inspect.signature(a)
print("inspect.signature（fn)是:%s" % aa)
print("inspect.signature（fn)的类型：%s" % (type(aa)))
print("\n")

bb = aa.parameters
print("signature.paramerters属性是:%s" % bb)
print("ignature.paramerters属性的类型是%s" % type(bb))
print("\n")
