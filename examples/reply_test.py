# coding: utf-8
import sys
sys.path.append("..")

from .init_wechat import wechat
from wechat_sdk.contrib.msg import Reply, ReplyTemplate
#自动回复消息测试
#TODO 消息加解密AES_KEY的实现
reply = Reply(wechat, default="yes i am just a test")
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
	content = "你好，正在测试 wechat sdk 关注事件推送接口！"
	return ReplyTemplate.TEXT % (params.get("FromUserName"), params.get("ToUserName"), \
		datetime.datetime.now().strftime("%Y%m%d%H%S"), content)

# Flask示例
# from flask import request
# @app.route("/wechat/callback/")
# def wechat_callback():
# 	if request.method = 'get':
# 		return reply(request.args, auth=True)
# 	else:
# 		return reply(request.data)

if __name__ == '__main__':
	TEXT = """
            <xml>
                <ToUserName><![CDATA[111111]]></ToUserName>
                <FromUserName><![CDATA[222222]]></FromUserName>
                <CreateTime>111111111111</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[我一直很好，你也要一直好下去！]]></Content>
            </xml>
            """
	print reply(ReplyTemplate.VIDEO)
	print reply(TEXT)