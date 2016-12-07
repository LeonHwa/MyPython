#!/usr/bin/env python
# -*- coding:utf-8 -*-
import  urllib
import  re

url = "http://www.thejoyrun.com"
page = urllib.urlopen(url)
html = page.read()
# print  html

# links = re.findall(r'<img class="head-img" src="(.*?)"',html,re.S)
# print  links
#下载头像
# for index,item in enumerate(links):
#     urllib.urlretrieve(item,'%s.jpg' % index)

spitList = re.split(r'[\s\"]',html)

for index, str in  enumerate(spitList):
    if(re.match(r'http:.*.(png|jpg)',str)):
        urllib.urlretrieve(str, '%s.jpg' % index)
