#!/usr/bin/env python
# -*- coding:utf-8 -*-
import  sys
import  asyncio

import  orm3

from  Models import  User,Blog,Comment


async def test(loop):
    await  orm3.create_pool(user ='www-data', password='www-data', db='db',loop = loop)

    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')

    await  u.save()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete( asyncio.wait([test(loop)]) )
    loop.close()
    if loop.is_closed():
        sys.exit()

