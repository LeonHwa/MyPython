#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

thread.LockType  #锁对象的一种, 用于线程的同步
thread.error  #线程的异常

thread.start_new_thread(function, args[, kwargs])  #创建一个新的线程
function : 线程执行函数
args : 线程执行函数的参数, 类似为tuple,
kwargs : 是一个字典
返回值: 返回线程的标识符

thread.exit()  #线程退出函数
thread.allocate_lock()  #生成一个未锁状态的锁对象


锁对象的方法
lock.acquire([waitflag]) #获取锁
无参数时, 无条件获取锁, 无法获取时, 会被阻塞, 知道可以锁被释放
有参数时, waitflag = 0 时,表示只有在不需要等待的情况下才获取锁, 非零情况与上面相同
返回值 :　获得锁成功返回True, 获得锁失败返回False

lock.release() #释放锁

lock.locked() #获取当前锁的状态
返回值 : 如果锁已经被某个线程获取,返回True, 否则为False
"""

"""
#thread


import  thread
import  time

def print_time(thread_name,delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print "%s : %s" % (thread_name,time.ctime(time.time()))


try:
    thread.start_new_thread(print_time,("thread-1",2,) )
    # thread.start_new_thread(print_time,("thread-2",3,) )
except:
    print "errr:unable to start a new thread"


while True :#不写的话 创建完线程程序就结束了，看不到完整的结果
    pass
"""



#
# python的threading模块是对thread做了一些包装的，可以更加方便的被使用。经常和Queue结合使用,Queue模块中提供了同步的、
# 线程安全的队列类，包括FIFO（先入先出)队列Queue，LIFO（后入先出）队列LifoQueue，和优先级队列PriorityQueue。
# 这些队列都实现了锁原语，能够在多线程中直接使用。可以使用队列来实现线程间的同步
#
# #函数
# threading.active_count()  #返回当前线程对象Thread的个数
# threading.enumerate()  #返回当前运行的线程对象Thread(包括后台的)的list
# threading.Condition()  #返回条件变量对象的工厂函数, 主要用户线程的并发
# threading.current_thread()  #返回当前的线程对象Thread, 文档后面解释没看懂
# threading.Lock()  #返回一个新的锁对象, 是在thread模块的基础上实现的 与acquire()和release()结合使用
#
# #类
# threading.Thread  #一个表示线程控制的类, 这个类常被继承
# thraeding.Timer  #定时器,线程在一定时间后执行
# threading.ThreadError  #引发中各种线程相关异常

# threading.Thread(group = None, target = None, name = None, args = () kwars = {})
# group : 应该为None
# target : 可以传入一个函数用于run()方法调用,
# name : 线程名 默认使用"Thread-N"
# args : 元组, 表示传入target函数的参数
# kwargs : 字典, 传入target函数中关键字参数
#
# 属性:
# name  #线程表示, 没有任何语义
# doemon  #布尔值, 如果是守护线程为True, 不是为False, 主线程不是守护线程, 默认threading.Thread.damon = False
#
# 类方法:
# run()  #用以表示线程活动的方法。
# start()  #启动线程活动。
# join([time])  #等待至线程中止。这阻塞调用线程直至线程的join() 方法被调用中止-正常退出或者抛出未处理的异常-或者是可选的超时发生。
# isAlive(): 返回线程是否活动的。
# getName(): 返回线程名。
# setName(): 设置线程名。

import  threading
import  time

def test_thread(count):
    while count > 0:
     print  "count = %d   %s" %(count,time.ctime(time.time()))
     count -= 1
     time.sleep(1)

try:
    my_thread = threading.Thread(target=test_thread ,name= "fander",args=(100,))
    my_thread.start()
    my_thread.join()
except:
    print "can not syart a new thread"

while True:
    pass