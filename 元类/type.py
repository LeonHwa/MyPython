#!/usr/bin/env python
# -*- coding:utf-8 -*-

class ObjectCreactor(object):
    pass
ObjectCreactor.name = 'fander'
print(ObjectCreactor)
print(ObjectCreactor.name)
o = ObjectCreactor()
print(o)

#使用type创建class  type(类名, 父类的元组（针对继承的情况，可以为空），包含属性的字典（名称和值）)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
MyClass = type('MyClass',(),{})
print(MyClass)
m = MyClass()
print(m)

# class Foo(object):
#     bar = True
Foo = type('Foo',(),{'bar':True})#给foo添加bar属性 默认为True
f = Foo()
print(f.bar )
print(Foo.bar )

FooChild = type('FooChild',(Foo,),{})
print(FooChild)
print(FooChild.bar)

dic = {'Lili':'23','Fon':'20','Car':'30'}
attrs = ((name, value) for name, value in dic.items())
print(attrs)


# 元类会自动将你通常传给‘type’的参数作为自己的参数传入
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    '''返回一个类对象，将属性都转为大写形式'''
    #  选择所有不以'__'开头的属性
    attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
    # 将它们转为大写形式
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)
    # 通过'type'来做类对象的创建
    return type(future_class_name, future_class_parents, uppercase_attr)


__metaclass__ = upper_attr  #  这会作用到这个模块中的所有类

class Bird(object):
    bar = 'bip'

print(hasattr(Bird,'bar'))
print(hasattr(Bird,'BAR'))
bb = Bird()
print(bb.BAR)