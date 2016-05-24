# coding: utf-8
import hashlib
from .conf import WechatConf, default_conf
from .msg import default_reply
from .menu import default_menu
from .utils import xml_to_dict
from .urls import ApiUrl


class Wechat(object):

    def __init__(self, conf=default_conf, reply_app=default_reply, \
        menu=default_menu):
        assert isinstance(conf, WechatConf), "conf object must be a WechatConf instance!"
        self.conf = conf
        self.reply_app = reply_app
        self._menu = menu

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

    def create_menu(self):
        self.default_menu.create(self.access_token)
        pass

    def get_access_token(self):
        access_token, expires_in = self.init_access_token()
        pass

    def init_access_token(self):
        url = ApiUrl.token % (self.conf.appid, self.conf.appsecret)
        resp = requests.get(url)
        result = json.loads(resp.text)
        if result.get("access_token"):
            return result.get("access_token"), result.get("expires_in")
        raise ValueError(str(result))

    access_token = property(get_access_token)
    del get_access_token

