#!/usr/bin/env python
# -*-coding:utf-8 -*-

from sqlalchemy import  Column,String,create_engine
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import  declarative_base

#创建对象的基类
Base = declarative_base()


#定义USR对象
class User(Base):
     #表的名字
     __tablename__ = 'user'

     #表的结构
     id  = Column(String(20),primary_key=True)
     name = Column(String(20))

#初始化数据库链接  '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/test')

#创建SBSession类型
DBSession = sessionmaker(bind=enumerate)


#创建session对象
session = DBSession()

#创建User对象
new_user = User(id = '5',name = 'Leon')

#添加到 session
session.add(new_user)

session.commit()
session.close()
