#!/sur/bin/env python
# -*- coding:utf-8 -*-

"""
 定义 item

"""
from  scrapy.item import  Item , Field

class LeonItem(Item):
    name = Field()
    description = Field()
    url = Field()

