# coding: utf-8
import sys
import json
import urllib
import datetime
sys.path.append(".")

from wechat.wechat import Wechat
from wechat.conf import WechatConf
from wechat.urls import ApiUrl
from wechat.msg import Reply, ReplyTemplate
from wechat.menu import default_menu

conf = WechatConf(appid="wxa8e2f9be2c6f347c", appsecret="0ed8890e310546b8ef45e1db174b2145", token="hrjiaweixin123")
wechat = Wechat(conf=conf)
#access_token = wechat.access_token
reply = Reply(wechat=wechat)


#如果是非事件消息，第二个值传空字符串
@reply.route(("text", ""))
def text(params):
	return ReplyTemplate.TEXT % (params.get("FromUserName"), params.get("ToUserName"), \
		datetime.datetime.now().strftime("%Y%m%d%H%S"), params.get("Content"))

#如果是事件消息，传两个参数
@reply.route(("event", "click"))
def click(params):
	return ReplyTemplate.TEXT % (params.get("FromUserName"), params.get("ToUserName"), \
		datetime.datetime.now().strftime("%Y%m%d%H%S"), params.get("EventKey"))

@reply.route(("event", "subscribe"))
def subscribe(params):
	content = "你好，正在测试wechat sdk 关注事件推送接口！"
	return ReplyTemplate.TEXT % (params.get("FromUserName"), params.get("ToUserName"), \
		datetime.datetime.now().strftime("%Y%m%d%H%S"), content)




#print wechat.access_token
#print default_menu.menu
#print wechat.post(ApiUrl.create_menu, data=json.dumps(default_menu.menu))
# 编码有问题待解决
test = {"x": '你是不是傻'}
# Flask示例
if request.method = 'get':
	reply(request.args, auth=True)
else:
	reply(request.data)



