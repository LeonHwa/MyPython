#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# from urllib import parse
# kw = []
# for k, v in parse.parse_qs('http://www.baidu.com/index.php?username=guol&psw=123&id=6666888&key=fanderKey', True).items():
#     print('k = %s   v = %s' %(k,v))
# import inspect
# def a():
#     pass
# aa = inspect.signature(a)
# print("inspect.signature（fn)是:%s" % aa)
# print("inspect.signature（fn)的类型：%s" % (type(aa)))
# print("\n")
#
# bb = aa.parameters
# print("signature.paramerters属性是:%s" % bb)
# print("ignature.paramerters属性的类型是%s" % type(bb))
# print("\n")
#
# for cc, dd in bb.items():
#     print("mappingproxy.items()返回的两个值分别是：%s和%s" % (cc, dd))
#     print("mappingproxy.items()返回的两个值的类型分别是：%s和%s" % (type(cc), type(dd)))
#     print("\n")
#     ee = dd.kind
#     print("Parameter.kind属性是:%s" % ee)
#     print("Parameter.kind属性的类型是:%s" % type(ee))
#     print("\n")
#     gg = dd.default
#     print("Parameter.default的值是: %s" % gg)
#     print("Parameter.default的属性是: %s" % type(gg))
#     print("\n")
#
#
# ff = inspect.Parameter.KEYWORD_ONLY
# print("inspect.Parameter.KEYWORD_ONLY的值是:%s" % ff)
# print("inspect.Parameter.KEYWORD_ONLY的类型是:%s" % type(ff))
import  os
print(os.getcwd())