#!/usr/bin/env python
# -*-coding:utf-8 -*-

import  sqlite3
conn = sqlite3.connect('fander.db')
cursor = conn.cursor()
cursor.execute('create table IF NOT EXISTS user (id varchar(20) primary key ,name varchar(20))')
cursor.execute('SELECT * FROM  user WHERE id = ?',('1',))
value = cursor.fetchall()
print  value
cursor.execute('INSERT  INTO  user (id,name) VALUES(\'1\',\'Leon\')')
#获取行数
print cursor.rowcount

#提交
conn.commit()
conn.close()
