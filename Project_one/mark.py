# -*- coding:utf-8 -*-
import  re, sys
from  util import  *

print '<html><head><title>...</title><body>'

title = True

for block in blocks(sys.stdin):
    # *表示 >= 0 个
    # sub  中间的替换左边的
    block = re.sub(r'\*(.+?)\*',r'<em>\1<\em>',block)
    if title:
        print '<h1>'
        print block
        print '<\h1>'
        title = False
    else:
        print 'P'
        print block
        print '\p'

print '</body></html>'
