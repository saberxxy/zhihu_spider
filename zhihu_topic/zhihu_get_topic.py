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
import zhihu_spider.common.GetMysqlConn as mysql_conn

# 获取session
s = zhihu_login.get_session()
# 获取MySQL数据库连接
cursor = mysql_conn.getConfig()

def get_topic_info(level, number):
    # print("session：", s)

    hot_url = "https://www.zhihu.com/topic/" + str(number) + "/hot"
    organize_url = "https://www.zhihu.com/topic/" + str(number) + "/organize"
    parent_url = "https://www.zhihu.com/api/v3/topics/" + str(number) + "/parent"
    children_url = "https://www.zhihu.com/api/v3/topics/" + str(number) + "/children"

    # 来源于hot_url的数据
    r_hot = s.get(url = hot_url, headers = Util.Default_Headers)
    soup_hot = BeautifulSoup(r_hot.content, 'lxml')
    # print(hot_url)
    # print(soup_hot)

    # uuid
    topic_uuid = str(uuid.uuid1())
    # print('UUID：', topic_uuid)

    # 话题编号
    topic_id = str(number)
    # print('话题编号：', topic_id)

    # 话题名称
    try:
        a_2 = soup_hot.findAll('title', attrs={'data-react-helmet':'true'})[0].contents[0]
        topic_name = str(a_2).replace(' - 知乎', '').replace('话题名称： ', '')
    except Exception:
        topic_name = 0
    # print('话题名称：', topic_name)

    # 话题链接
    try:
        # a_3 = soup_hot.findAll('a', attrs={'class':'Tabs-link is-active'})
        topic_link = "https://www.zhihu.com/topic/" + topic_id + "/hot"
    except Exception:
        topic_link = 0
    # print('话题链接：', topic_link)

    # 关注人数
    try:
        a_4 = soup_hot.findAll('strong', attrs={'class':'NumberBoard-itemValue'})
        follow_number = int(str(a_4[0].contents[0]).replace(',', ''))
    except Exception:
        follow_number = 0
    # print('关注人数：', follow_number)

    # 问题数
    try:
        a_5 = soup_hot.findAll('strong', attrs={'class':'NumberBoard-itemValue'})
        question_number = int(str(a_5[1].contents[0]).replace(',', ''))
    except Exception:
        question_number = 0
    # print('问题数：', question_number)

    # 话题描述
    try:
        a_6 = soup_hot.findAll('span', attrs={'class':'RichText'})[0]
        topic_describe = str(a_6.contents[0])
    except Exception:
        topic_describe = 0
    # print(a_6)

    # print('话题描述：', topic_describe)

    # 来源于parent_url的数据
    # 父级话题和子级话题不是在页面加载的，需要要请求Ajax
    # 父级话题编号【一个话题的父话题可能很多，所以存成列表】
    parent_topic_id_list = []
    r_parent = s.get(url = parent_url, headers = Util.Default_Headers)
    jsondata = json.loads(re.match(".*?({.*}).*", r_parent.text, re.S).group(1))['data']
    # print(jsondata)
    for i in jsondata:
        parent_topic_id_list.append(i['id'])
    parent_topic_id = ','.join(parent_topic_id_list)
    # print('父级话题编号：', parent_topic_id)

    # 来源于children_url的数据
    # 子级话题编号【一个话题的子话题可能很多，所以存成列表】
    children_topic_id_list = []
    r_children = s.get(url = children_url, headers = Util.Default_Headers)
    jsondata = json.loads(re.match(".*?({.*}).*", r_children.text, re.S).group(1))['data']
    for i in jsondata:
        children_topic_id_list.append(i['id'])
    children_topic_id = ','.join(children_topic_id_list)
    # print('子级话题编号：', children_topic_id)

    # 入库时间
    store_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # print('入库时间：', store_time)

    # 话题层级（从根话题开始为0）
    topic_level = int(level)
    # print("话题层级：", topic_level)

    topic_info = {}
    topic_info['topic_uuid'] = topic_uuid
    topic_info['topic_id'] = topic_id
    topic_info['topic_name'] = topic_name
    topic_info['topic_link'] = topic_link
    topic_info['follow_number'] = follow_number
    topic_info['question_number'] = question_number
    topic_info['topic_describe'] = topic_describe
    topic_info['parent_topic_id'] = parent_topic_id
    topic_info['children_topic_id'] = children_topic_id
    topic_info['store_time'] = store_time
    topic_info['topic_level'] = topic_level
    print(topic_info)

    return topic_info


# 入库
def input_mysql(topic_info):
    # print(topic_info)
    topic_id_exists = cursor.execute("select topic_id from zhihu_topic where topic_id=%s",
                   (topic_info['topic_id']) )
    # print(topic_id_exists)
    if topic_id_exists >= 1:
        print('话题已经存在，不再入库')
        return '话题已经存在，不再入库'

    cursor.execute("insert into zhihu_topic(topic_uuid, topic_id, topic_name, topic_link,"
            "follow_number, question_number, topic_describe, parent_topic_id,"
            "children_topic_id, store_time, topic_level"
            ") values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (topic_info['topic_uuid'], topic_info['topic_id'], topic_info['topic_name'],
             topic_info['topic_link'], topic_info['follow_number'],
             topic_info['question_number'], topic_info['topic_describe'],
             topic_info['parent_topic_id'], topic_info['children_topic_id'],
             topic_info['store_time'], topic_info['topic_level']))
    cursor.execute("commit")
    print('提交完毕，入库成功')
    return '提交完毕，入库成功'


if __name__ == '__main__':
    # 获取数据库里最大的level，获取该level的下一级level的话题的子话题id
    # 由于已经入库的就不再入库，因此可以从任何位置开始
    cursor.execute("select distinct topic_level from zhihu_topic order by topic_level desc limit 1")
    x = cursor.fetchall()[0]
    print(x['topic_level']-1)

    for level in range(x['topic_level']-1, 100):
        print('抓取第', str(level+1), '层级的话题')
        cursor.execute("select children_topic_id, topic_level from zhihu_topic where topic_level=%s \
                       and children_topic_id <> ''",
                       (str(level)))
        a = cursor.fetchall()

        children_topic_id_list = []
        children_topic_id_str = ''
        for i in a:
            children_topic_id_str += i['children_topic_id']+','
        for j in eval(children_topic_id_str[:-1]):
            topic_info = get_topic_info(level+1, j)
            input_mysql(topic_info)





