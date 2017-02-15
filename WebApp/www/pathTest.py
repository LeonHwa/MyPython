#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import  re
# w = 'foolsdFoolsnbiFoo3'
# ans = re.findall('(?i)(foo.)',w)
# print(ans)

# m = re.match(r'c','canjcjv')
# print(m.group(0))

# s = 'i am the one'



s = '#gkjk68g#65464555559kmj5k5#hdjhk289vhklv5'

arr = re.findall(r'#([0-9a-zA-Z]*)',s)
print(arr)
sql = ''
len = len(arr)
i = 0

print(' or '.join(arr))
# for id in arr:
#     oor = ""
#     if i < len - 1 :
#         oor = "or "
#     sql += "id = " + id +" "+ oor
#     i += 1
#
# print(sql)


