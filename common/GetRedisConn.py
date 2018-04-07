# -*- coding=utf-8 -*-
# 获取Redis连接

import configparser
import redis

def getConfig():
    cf = configparser.ConfigParser()
    cf.read("..\\config\\config.conf")
    redis_host = str(cf.get("redis", "ip"))
    redis_port = int(cf.get("redis", "port"))
    redis_databasename = int(cf.get("redis", "databasename"))
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_databasename)
    print('已获取Redis连接')
    return r

if __name__ == '__main__':
    getConfig()
