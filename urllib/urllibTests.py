#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
一个简单的Python爬虫, 用于抓取豆瓣电影Top前100的电影的名称

"""

import urllib2
import  re
class spider(object):

    def __init__(self):
        self.page = 1
        self.cur_url = "http://movie.douban.com/top250?start={page}&filter=&type="
        self.data = []
        self._top_num = 1
        print "爬虫准备开始"


    def start(self):
        print """
              ###############################
                  一个简单的豆瓣电影前100爬虫
                  Author: Leon_Hwa
                  Version: 0.0.1
                  Date: 2016-12-07
              ###############################
          """
        while self.page <= 4:
            my_page = self.get_page(self.page)
            self.find_title(my_page)
            self.page += 1


    # 解析每个网页的源码
    def get_page(self,cur_page):
        url = self.cur_url
        try:
            my_page = urllib2.urlopen(url.format(page = (cur_page - 1) * 25)).read().decode("utf-8")
        except urllib2.URLError,e:
            if hasattr(e, "code"):
                print "The server couldn't fulfill the request."
                print "Error code: %s" % e.code
            elif hasattr(e, "reason"):
                print "We failed to reach a server. Please check your url and read the Reason"
                print "Reason: %s" % e.reason
        return  my_page

   # 分析源码找到title
    def find_title(self,my_page):
       temp_data = []
       # re.S 单选模式——点任意匹配模式
       """
           I 	IGNORECASE 	忽略大小写
           M 	MULTILINE 	多行模式
           S 	DOTALL 	单选模式——点任意匹配模式
           L 	LOCALE 	使预定字符类 \w \W \b \B \s \S 取决于当前区域设定
           U 	UNICODE 	使预定字符类 \w \W \b \B \s \S \d \D 取决于unicode定义的字符属性
           X 	VERBOSE 	详细模式。该模式下正则表达式可以是多行，忽略空白字符，并可以加入注释
       """
       # 加上re.S后, .将会匹配换行符
       movie_items = re.findall(r'<span>.*?class="title">(.*?)</span>',my_page,re.S)

       for index ,item in enumerate(movie_items):
           if item.find("&nbsp") == -1:
               temp_data.append("top" + str(self._top_num) +" " + item)
               self._top_num += 1
       self.data.extend(temp_data)



mySpider = spider()
mySpider.start()
for item in mySpider.data:
    print  item