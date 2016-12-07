#!usr/bin/env python
# -*- coding:utf-8 -*-

import  re


some_test = 'alpha,beta,,,,gama delta'
#有逗号和空格都分开
sd = re.split('[, ]+',some_test)
print  sd
sb = re.split('[,   ]+',some_test,maxsplit=1)#只能分为2组
print  sb

some_test = ' "Hm...Err -- are you sure? " he said,sounding insecure'
# 查找所有的单词
print  re.findall('[a-zA-Z]+',some_test)
