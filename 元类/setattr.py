#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Model(dict):

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    # def __setattr__(self, key, value):
    #     self[key] = value

class Field(object):
    def __init__(self,name):
        self.name = name




u = Model(AA = 'CC',BB = 'DD')
print(u.AA)
