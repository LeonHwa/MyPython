#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Leon Hwa'

import  asyncio, logging

import  aiomysql

def log(sql,args=()):
    logging.info('SQL: %s' %sql)


async def create_pool(loop,**kwargs):
      logging.info('create database connection pool...')
      global __pool
      __pool = await  aiomysql.create_pool(
            host = '127.0.0.1',
            port = 3306,
            user = kwargs['user'],
            password = kwargs['password'],
            db = kwargs['db'],
            charset = kwargs.get('charset','utf8'),
            autocommit = kwargs.get('autocommit',True),
            maxsize = kwargs.get('maxsize',10),
            minsize = kwargs.get('minsize',1),
            loop = loop
     )

#select
async def select(sql,args,size = None):
    log(sql,args)
    global  __pool
    async  with  __pool.get() as conn:
        async  with  conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql.replace('?','%s'),args or ())
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()

        logging.info('rows returned: %s' % len(rs))
        return  rs


async def execute(sql,args,autucommit = True):
    log(sql)
    async  with __pool.get() as conn:
        if not autucommit:
            await conn.begin
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await  cur.execute(sql.replace('?','%s'),args)
                affeted = cur.rowcount
            if not autucommit:
                 await  conn.commit()
        except BaseException as e:
            if not autucommit:
                 await  conn.rollback()
            raise

        return  affeted

'''
定义Model
'''
# __new__()方法接收到的参数依次是：
#
#     当前准备创建的类的对象；
#
#     类的名字；
#
#     类继承的父类集合；
#
#     类的方法集合。

class Field(object):
    def __init__(self,name,column_type,primary_key,default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
    def __str__(self):# 相当于oc c重写description方法
        return  '<%s,  %s:%s>' %(self.__class__.__name__,self.column_type,self.name)

class StringField(Field):
    def __init__(self,name = None,column_type = 'varchar(100)',primary_key = False,default = None):
        super().__init__(name,column_type,primary_key,default)
class IntegerField(Field):
    def __init__(self,name = None,column_type = 'bigint',primary_key = False,default = 0):
        super().__init__(name,column_type,primary_key,default)

class BooleanField(Field):
    def __init__(self,name = None,column_type = 'boolean',primary_key = False,default = False):
        super().__init__(name,column_type,primary_key,default)

class FloatField(Field):
    def __init__(self,name = None,column_type = 'real',primary_key = False,default = 0.0):
        super().__init__(name,column_type,primary_key,default)
class TextField(Field):
    def __init__(self,name = None,column_type = 'text',primary_key = False,default = None):
        super().__init__(name,column_type,primary_key,default)


class ModelMetaclass(type):
    def __new__(cls, name, bases,attrs):
        if name == 'Model':
            return type.__new__(cls,name,bases,attrs)
        tableName = attrs.get('__table__',None) or name #如果有就用__table__对应的值 没有就用 类名name
        mappings = dict()
        fields = []
        primarykey = None
        for k,v in attrs.items():
            if isinstance(v,Field):
                logging.info('found mapping: %s ==> %s' % (k,v))
                mappings[k] = v
                if v.primary_key:
                    # 判断是不是主键
                    if primarykey:
                        raise  RuntimeError('Duplicate primary key for Field : %s' % k)
                    primarykey = k
                else:
                    fields.append(k)
        if not primarykey:
          raise RuntimeError(' primary key not found')

        #将原始类属性删除掉
        for k in mappings.keys():
             attrs.pop(k)
        escaped_field = list(map(lambda f : '`%s`' %f ,fields))
        #或者如下
        #escaped_field = list(map(lambda f: str, fields))
        attrs['__mappings__'] = mappings #提取出来的类属性（Field对象）
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primarykey
        attrs['__fields__'] = fields#类属(除了是主键以外的集合)
        attrs['__table__'] = tableName

        #sql语句 (把他们作为string类型的 类属性)
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primarykey, ', '.join(escaped_field), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (
        tableName, ', '.join(escaped_field), primarykey, create_args_string(len(escaped_field) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (
        tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primarykey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primarykey)
        return type.__new__(cls,name,bases,attrs)
def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)


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

    def getValue(self,key):
        return getattr(self,key,None)

    def getValueOrDefault(self,key):
        value = getattr(self,key,None)
        if value is None:#可能之前有 但是删掉了 保存在__mapping__ 里面
            field = self.__mappings__[key]
            if field.default is not None:
                value =field.default() if callable(field.default) else field.default
                logging.debug('using default value %s : %s' % (key,str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    async  def findAll(cls, where=None, args=None, **kw):
        ' find objects by where clause. '
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = await select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        ' find number by select and where. '
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    async def find(cls, pk):
        ' find object by primary key. '
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warning('failed to insert record: affected rows: %s' % rows)

    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
          logging.warning('failed to update by primary key: affected rows: %s' % rows)

    async def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows: %s' % rows)
