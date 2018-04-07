# -*- coding=utf-8 -*-
# 获取话题信息

"""
uuid，话题编号，话题名称，话题链接，父级话题编号，
子级话题编号【一个话题的子话题可能很多，所以存成列表】，
话题别名，关注人数，话题描述，入库时间，
话题层级（从根话题开始为0），问题数
"""

import requests
import threading
import queue
import urllib
import uuid
import re
import json
import time
from bs4 import BeautifulSoup

from zhihu_spider.zhihu_login import zhihu_login
import zhihu_spider.zhihu_login.Util as Util
import zhihu_spider.zhihu_login.ThreadUtil as ThreadUtil


# cookies = zhihu_login.get_cookie()
# s = requests.session()
# s.cookies = requests.utils.cookiejar_from_dict(cookies)
s = zhihu_login.get_session()
print(s)

hot_url = "https://www.zhihu.com/topic/19744646/hot"
organize_url = "https://www.zhihu.com/topic/19744646/organize"
parent_url = "https://www.zhihu.com/api/v3/topics/19744646/parent"
children_url = "https://www.zhihu.com/api/v3/topics/19744646/children"

# r_hot = s.get(url = hot_url, headers = Util.Default_Headers)
# soup_hot = BeautifulSoup(r_hot.content, 'lxml')
# print(soup_hot)
# print(cookies)


# 来源于hot_url的数据

r_hot = s.get(url = hot_url, headers = Util.Default_Headers)
soup_hot = BeautifulSoup(r_hot.content, 'lxml')
# print(soup)

# uuid
uuid = uuid.uuid1()
print('UUID：', uuid)

# 话题编号
a = soup_hot.findAll('a', attrs={'class':'Tabs-link is-active'})
topic_id = str(re.findall(r'.*href="/topic/(.*)/hot', str(a))[0])
print('话题编号：', topic_id)
# print(a)


# 话题名称
a = soup_hot.findAll('h1', attrs={'class':'TopicCard-titleText'})[0].contents[0]
topic_name = str(a)
print('话题名称：', topic_name)


# 话题链接
a = soup_hot.findAll('a', attrs={'class':'Tabs-link is-active'})
topic_link = "https://www.zhihu.com" + \
    str(re.findall(r'.*href="(.*)">', str(a))[0])
print('话题链接：', topic_link)

# 关注人数
# print(soup_hot)
a = soup_hot.findAll('strong', attrs={'class':'NumberBoard-itemValue'})
follow_number = str(a[0].contents[0]).replace(',', '')
print('关注人数：', follow_number)

# 问题数
a = soup_hot.findAll('strong', attrs={'class':'NumberBoard-itemValue'})
question_number = str(a[1].contents[0]).replace(',', '')
print('问题数：', question_number)


# 来源于organize_url的数据
# 话题别名
# r_organize = s.get(url = organize_url, headers = Util.Default_Headers)
# soup_organize = BeautifulSoup(r_organize.content, 'lxml')
# print(soup_organize)

# 话题描述
a = soup_hot.findAll('span', attrs={'class':'RichText'})[0]
topic_describe = str(re.findall(r'.*">(.*) http', str(a))[0])
print('话题描述：', topic_describe)

# 来源于parent_url的数据
# 父级话题和子级话题不是在页面加载的，需要要请求Ajax
# 父级话题编号【一个话题的父话题可能很多，所以存成列表】
parent_topic_id_list = []
r_parent = s.get(url = parent_url, headers = Util.Default_Headers)
jsondata = json.loads(re.match(".*?({.*}).*", r_parent.text, re.S).group(1))['data']
# print(jsondata)
for i in jsondata:
    parent_topic_id_list.append(i['id'])
parent_topic_id_str = ','.join(parent_topic_id_list)
print('父级话题编号：', parent_topic_id_str)

# 来源于children_url的数据
# 子级话题编号【一个话题的子话题可能很多，所以存成列表】
children_topic_id_list = []
r_children = s.get(url = children_url, headers = Util.Default_Headers)
jsondata = json.loads(re.match(".*?({.*}).*", r_children.text, re.S).group(1))['data']
for i in jsondata:
    children_topic_id_list.append(i['id'])
children_topic_id_str = ','.join(children_topic_id_list)
print('子级话题编号：', children_topic_id_str)


# 入库时间
store_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print('入库时间：', store_time)

"""
# 话题层级（从根话题开始为0）
"""