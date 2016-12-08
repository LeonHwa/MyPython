#!/usr/bin/env python
# -*- coding:utf-8 -*-

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
                rs = await cur.fetcgall()

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

class ModelMetaclass(type):
    def __new__(cls, name, bases,attrs):
        if name == 'Model':
            return type.__new__(cls,name,bases,attrs)


class Model(dict,metaclass= ModelMetaclass):

