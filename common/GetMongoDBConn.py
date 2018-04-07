# -*- coding=utf-8 -*-
# 获取MongoDB连接

import configparser
import pymongo

def getConfig():
    cf = configparser.ConfigParser()
    cf.read("..\\config\\config.conf")
    mongodb_host = str(cf.get("mongodb", "ip"))
    mongodb_port = int(cf.get("mongodb", "port"))
    conn = pymongo.MongoClient(mongodb_host, mongodb_port)
    print('已获取MongoDB连接')
    return conn

if __name__ == '__main__':
    print(getConfig())