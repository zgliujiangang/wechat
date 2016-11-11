# coding: utf-8
import sys
sys.path.append("..")

from wechat_sdk import Wechat


# 将appid、appsecret、token传入WechatConf

# Wechat类是整个sdk的核心类，默认使用memcached缓存access_token和jsapi_ticket，也可以自定制:
# redis = Redis.connection(*args, **kwargs)
# class MyWechat(Wechat):
# 	#复写缓存数据的方法
# 	def cache_data(self, key, value, expires_in):
# 		redis.set(key, value, expires_in)
# 	#复写获取缓存数据的方法
# 	def get_cache_data(self, key):
# 		return redis.get(key)
# wechat = MyWechat(**kwargs)
# access_token = wechat.access_token
# jsapi_ticket = wechat.jsapi_ticket
# ......
wechat = Wechat(appid="wxa8e2f9be2c6f347c", appsecret="0ed8890e310546b8ef45e1db174b2145", token="hrjiaweixin123", aeskey="aeskey")
#直接访问属性access_token获取
access_token = wechat.access_token
#直接访问属性jsapi_ticket获取
jsapi_ticket = wechat.jsapi_ticket
print access_token
print jsapi_ticket