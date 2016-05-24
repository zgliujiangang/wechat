# coding: utf-8
import hashlib
from .conf import WechatConf, default_conf
from .msg import default_reply
from .utils import xml_to_dict


class Wechat(object):

    def __init__(self, conf=default_conf, reply_app=default_reply):
        assert isinstance(conf, WechatConf), "conf object must be a WechatConf instance!"
        self.conf = conf
        self.reply_app = reply_app

    def reply(self, method, data):
        if method.lower() == "get":
            # 服务器接入验证 仅支持data以字典形式传入
            return self.reply_app.auth(data, self.conf.token)
        else:
            # 消息对话 data仅支持xml字符串或者字典
            params = data
            if isinstance(data, str):
                params = xml_to_dict(data)
            response = self.reply_app.response((params.get("MsgType"), params.get("Event", "")), params)
            return response

    def menu(self, method, *args, **kwargs):
        pass

