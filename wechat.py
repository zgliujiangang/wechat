# coding: utf-8
import hashlib
from .conf import WechatConf, default_conf
from .msg import default_reply
from .menu import default_menu
from .utils import xml_to_dict
from .urls import ApiUrl


class Wechat(object):

    def __init__(self, conf=default_conf, reply_app=default_reply, \
        menu=default_menu, debug=False):
        assert isinstance(conf, WechatConf), "conf object must be a WechatConf instance!"
        self.conf = conf
        self.reply_app = reply_app
        self._menu = menu

    def get_access_token(self):
        access_token = self.get_cache_access_token()
        if not access_token:
            access_token = self.init_access_token()
        return access_token

    def init_access_token(self):
        url = ApiUrl.token % (self.conf.appid, self.conf.appsecret)
        resp = requests.get(url)
        result = json.loads(resp.text)
        access_token = result.get("access_token")
        expires_in = result.get("expires_in")
        if access_token and expires_in:
            self.cache_access_token(access_token, expires_in)
            return access_token
        raise ValueError(str(result))

    def cache_access_token(self, access_token, expires_in):
        # 缓存access_token 需要自定义
        pass

    def get_cache_access_token(self):
        # 获取缓存的access_token 需要自定义
        access_token = "1111111111"
        return access_token

    access_token = property(get_access_token)
    del get_access_token

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
        result = self._menu.create(self.access_token)
        return result

