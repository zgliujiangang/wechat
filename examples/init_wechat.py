# -*- coding: utf-8 -*-


import sys; sys.path.append("..")
from wechat_sdk import Wechat
import os


# 如果使用sdk本身的缓存，请传入cache_dir参数
cache_dir = os.path.join(os.path.dirname(__file__), "cache_dir")
wechat = Wechat(appid="wxa8e2f9be2c6f347c", appsecret="0ed8890e310546b8ef45e1db174b2145", 
    token="hrjiaweixin123", aeskey="aeskey", cache_dir=cache_dir)

# 如果自定义cache_data和get_cache_data方法则无须传入cache_dir
# import memcache
# def cache_data(key, value, expires_in):
#     mc = memcache.Client(['127.0.0.1:11211'], debug=0)
#     mc.set(key, value, int(expires_in)-10)

# def get_cache_data(key):
#     mc = memcache.Client(['127.0.0.1:11211'], debug=0)
#     return mc.get(key)
# wechat = Wechat(appid="wxa8e2f9be2c6f347c", appsecret="0ed8890e310546b8ef45e1db174b2145", 
#     token="hrjiaweixin123", aeskey="aeskey", cache_data=cache_data, get_cache_data=get_cache_data)


#直接访问属性access_token获取
access_token = wechat.access_token
print "access_token", access_token
#直接访问属性jsapi_ticket获取
jsapi_ticket = wechat.jsapi_ticket
print "jsapi_ticket", jsapi_ticket

        