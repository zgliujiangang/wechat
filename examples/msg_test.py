# -*- coding: utf-8 -*-


import sys; sys.path.append("..")
import time
from examples.base_test import wechat_app
from wechat_sdk.contrib.msg import MsgHandler, ReplyTemplate, MsgManager


# 明文模式
msg_handler = MsgHandler(wechat_app, default="Hello World")
msg_manager = MsgManager(wechat_app)
# 密文模式
# msg_handler = MsgHandler(wechat_app, default="Hello World", crypto=True)


# router方法接受一个二元元祖，第一个参数对应xml中的msg_type,第二个参数对应event,如果没有event,则传空字符串
# 文本消息
@msg_handler.route(("text", ""))
def text(xml_tree):
    return ReplyTemplate.TEXT % (xml_tree.find("FromUserName").text, xml_tree.find("ToUserName").text, \
    	int(time.time()), xml_tree.find("Content").text)


# 点击事件消息
@msg_handler.route(("event", "click"))
def click(xml_tree):
    return ReplyTemplate.TEXT % (xml_tree.find("FromUserName").text, xml_tree.find("ToUserName").text, \
    	int(time.time()), xml_tree.find("EventKey").text)


# 订阅事件消息
@msg_handler.route(("event", "subscribe"))
def subscribe(xml_tree):
    content = "你好，正在测试 wechat sdk 关注事件推送接口！"
    return ReplyTemplate.TEXT % (xml_tree.find("FromUserName").text, xml_tree.find("ToUserName").text, \
    	int(time.time()), content)


if __name__ == '__main__':
    TEXT = """
            <xml>
                <ToUserName><![CDATA[111111]]></ToUserName>
                <FromUserName><![CDATA[222222]]></FromUserName>
                <CreateTime>111111111111</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[hello world!]]></Content>
            </xml>
            """
    print msg_handler(ReplyTemplate.VIDEO)
    print msg_handler(TEXT)
    print msg_manager.get_industry()


# Flask示例
# from flask import Flask

# app = Flask(__name__)

# @app.route("/msg/callback/")
# def msg_callback():
#     if request.method = 'get':
#         return msg_handler(request.args, auth=True)
#     else:
#         # 明文
#         return msg_handler(request.data)
#         # 密文
#         # return msg_handler(request.data, request.args)

# if __name__ == "__main__":
#     app.run(debug=True)