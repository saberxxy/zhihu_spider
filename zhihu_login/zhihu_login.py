# -*- coding=utf-8 -*-
# 登录，保存cookie，并使用cookie登录

import time
import requests
import re
import pickle
import os
import queue
import urllib
import threading
from PIL import Image
from bs4 import BeautifulSoup

import zhihu_spider.zhihu_login.Util as Util
import zhihu_spider.zhihu_login.ThreadUtil as ThreadUtil
import zhihu_spider.common.GetRedisConn as RedisConn


# 获取cookie
def get_cookie():
    r = RedisConn.getConfig()
    # 从Redis中取到的值是bytes类型，要转为字符串
    username = r.get('zhihu_username').decode()
    password = r.get('zhihu_password').decode()

    # 获取cookie
    usercookies = {}
    s = requests.session()

    # 此处判断redis中是否有cookie信息
    if r.get('zhihu_usercookies'):
        usercookies = r.get('zhihu_usercookies').decode()
        # 需要的cookie为dict，此处为str，所以需要转为dict
        return eval(usercookies)

    catpcha_image = archieve_captcha(s)
    catpcha = input(r'请输入验证码>>>')
    data = {"phone_num": username, "password": password, "captcha": catpcha}
    status = s.post(Util.PHONE_LOGIN, headers=Util.Default_Headers, data=data)
    print(status.json()['msg'])
    if status.status_code == 200:
        usercookies = requests.utils.dict_from_cookiejar(s.cookies)
        r.set('zhihu_usercookies', usercookies)
        print('已保存入Redis')
    else:
        pass

    return usercookies


# 获取验证码
def archieve_captcha(s):
    c = s.get(Util.CAPTCHA_URL, headers = Util.Default_Headers)
    print(Util.CAPTCHA_URL)
    if c.status_code == 200:
        with open('../capture.gif', 'wb') as f:
            f.write(c.content)
        image = Image.open('../capture.gif')
        image.show()
    else:
        return '获取验证码失败'


# 获取session
def get_session():
    cookies = get_cookie()
    s = requests.session()
    s.cookies = requests.utils.cookiejar_from_dict(cookies)
    return s


if __name__ == '__main__':
    cookie = get_cookie()
    print(cookie)










