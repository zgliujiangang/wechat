# -*- coding: utf-8 -*-


import sys; sys.path.append("..")
from wechat_sdk import WechatApp
import os


# 如果使用sdk本身的序列化缓存，请传入cache_dir参数
cache_dir = os.path.join(os.path.dirname(__file__), "cache_dir")
wechat_app = WechatApp(appid="wxa8e2f9be2c6f347c", appsecret="0ed8890e310546b8ef45e1db174b2145", 
    token="hrjiaweixin123", aeskey="aeskey", cache_dir=cache_dir)


# 如果自定义cache则无须传入cache_dir
# import memcache
# from wechat_sdk.utils.cache import BaseCache

# class MemoryCache(BaseCache):

#     def __init__(self, mc):
#         self.mc = mc

#     def set(self, key, value, expires_in):
#         mc.set(key, value, int(expires_in)-10)

#     def get(self, key):
#         return mc.get(key)

#     def delete(self, key):
#         mc.delete(key)

# mc = memcache.Client(['127.0.0.1:11211'], debug=0)
# my_cache = MemoryCache(mc)
# wechat = WechatApp(appid="wxa8e2f9be2c6f347c", appsecret="0ed8890e310546b8ef45e1db174b2145", 
#     token="hrjiaweixin123", aeskey="aeskey", cache=my_cache)


#直接访问属性access_token获取
access_token = wechat_app.access_token
print "access_token", access_token
#直接访问属性jsapi_ticket获取
jsapi_ticket = wechat_app.jsapi_ticket
print "jsapi_ticket", jsapi_ticket

        