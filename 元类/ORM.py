#!/usr/bin/env python
# -*- coding:utf-8 -*-



class Field(object):
    def __init__(self,name,colum_type):
        self.name = name
        self.colum_type =  colum_type
    def __str__(self):
        return '<%s %s>' %(self.__class__.__name__,self.name)

class StringField(Field):
    def __init__(self,name):
        super(StringField,self).__init__(name,colum_type='varchar(100)')
class IntegerField(Field):
    def __init__(self,name):
        super(IntegerField,self).__init__(name,colum_type='bigint')

class ModelMetaclass(type):
    def __new__(cls, name, bases,attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases,attrs)
        print('Found model: %s' % name)
        mappings = dict()
        for k,v in attrs.items():
            if isinstance(v,Field):
                print('Found mapping %s == > %s' % (k,v))
                mappings[k] = v
        for k in  mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        return type.__new__(cls, name, bases, attrs)


class Model(dict,metaclass= ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k ,v in self.__mappings__.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self,k,None))

        sql = 'insert into %s (%s) values(%s)' % (self.__table__,','.join(fields),','.join(params))
        print('sql : %s' % sql)
        print('args : %s' % str(args))

class User(Model):
    id  = IntegerField('id')
    name = StringField('name')
    email = StringField('email')
    password = StringField('password')

#未初始化的时候 即 id = 123456之前  ModelMetaclass 的__new__方法已经开始调用
#   把 k :id  value:IntegerField('id') 等四个键值对 从attrs 转移到  __mappings__ 中（Field的作用只是在ModelMetaclass中有用）
# 所以 User 从attrs中删除后 就再也没有 id name email password  四个类属性了
# 但是 User 爷爷类是dict  父类是Model Model实现了 __getattr__ 、__setattr__ 方法 User(id = 123456)时 User '又'创建了类属性id

u = User(id = 123456,name ='Leon',email = 'test@gmail.com',password = '88888888')
u.save()