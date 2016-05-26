# coding: utf-8
import sys
import json
import urllib
import datetime
sys.path.append(".")

from wechat.wechat import Wechat
from wechat.conf import WechatConf
from wechat.urls import ApiUrl
from wechat.contrib.msg import Reply, ReplyTemplate
from wechat.contrib.oauth2 import Oauth2

conf = WechatConf(appid="wxa8e2f9be2c6f347c", appsecret="0ed8890e310546b8ef45e1db174b2145", token="hrjiaweixin123")
wechat = Wechat(conf=conf)
#access_token = wechat.access_token
#**********调用微信接口**********
#wechat.get(ApiUrl.url, params=params)
#wechat.post(ApiUrl.url, data=data, _json=_json)
#wechat.upload(ApiUrl.url, **file_form)
#如果你想调用接口出错时抛出异常，可以像下面如此调用，在with语句内debug是True的
#with wechat:
#	result = wehchat.get(url, params)
#**********调用微信接口**********


#自动回复消息测试
#TODO 消息加解密AES_KEY的实现
# reply = Reply(wechat=wechat)
# #如果是非事件消息，第二个值传空字符串
# @reply.route(("text", ""))
# def text(params):
# 	return ReplyTemplate.TEXT % (params.get("FromUserName"), params.get("ToUserName"), \
# 		datetime.datetime.now().strftime("%Y%m%d%H%S"), params.get("Content"))

# #如果是事件消息，传两个参数
# @reply.route(("event", "click"))
# def click(params):
# 	return ReplyTemplate.TEXT % (params.get("FromUserName"), params.get("ToUserName"), \
# 		datetime.datetime.now().strftime("%Y%m%d%H%S"), params.get("EventKey"))

# @reply.route(("event", "subscribe"))
# def subscribe(params):
# 	content = "你好，正在测试 wechat sdk 关注事件推送接口！"
# 	return ReplyTemplate.TEXT % (params.get("FromUserName"), params.get("ToUserName"), \
# 		datetime.datetime.now().strftime("%Y%m%d%H%S"), content)
# Flask示例
#from flask import request
#@app.route("/wechat/callback/")
#def wechat_callback():
#	if request.method = 'get':
#		return reply(request.args, auth=True)
#	else:
#		return reply(request.data)



# 测试自定义菜单
# from wechat.menu import test_menu
# print wechat.access_token
# print test_menu.menu
# print wechat.post(ApiUrl.create_menu, data=test_menu.menu)
# 测试自定义菜单


# 测试oauth接口
# oauth2 = Oauth2(wechat)
#print oauth2.code_ex_token("11111111111111")
#print oauth2.token_ex_info("11111", "22222")
#print oauth2.auth_url("www.baidu.com?*&&=111")
#print oauth2.check_token("111111", "1111111")
#print oauth2.refresh_token("111111")
# 测试oauth接口




