# coding: utf-8
import hashlib
import requests
import json
from .conf import WechatConf, default_conf
from .msg import default_reply
from .menu import default_menu
from .utils import xml_to_dict
from .urls import ApiUrl
from .error import ErrorHandler


class Wechat(object):

    def __init__(self, conf=default_conf, reply_app=default_reply, \
        menu=default_menu, err_handler=ErrorHandler, debug=False):
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
        # 每日有调用次数上限，需要缓存结果
        result = self.get(ApiUrl.token)
        access_token = result.get("access_token")
        expires_in = result.get("expires_in")
        if access_token and expires_in:
            self.cache_access_token(access_token, expires_in)
            return access_token
        else:
            raise ValueError("can not get access_token: %s" % str(result))

    def cache_access_token(self, access_token, expires_in):
        # 缓存access_token 需要自定义
        # eg:redis.set(access_token_key, access_token, expires=expires_in)
        pass

    def get_cache_access_token(self):
        # 获取缓存的access_token 需要自定义
        # eg:access_token = redis.get(access_token_key)
        # eg:if not access_token:
        # eg:   return None
        # eg:return access_token
        access_token = "1111111111"
        #return access_token
        return True

    access_token = property(get_access_token)
    del get_access_token

    def reply(self, data, auth=False):
        if not auth:
            # 消息对话 data仅支持xml字符串或者字典
            params = data
            if isinstance(data, str):
                params = xml_to_dict(data)
            response = self.reply_app.response((params.get("MsgType"), params.get("Event", "")), params)
            return response
        else:
            # 服务器接入验证 仅支持data以字典形式传入
            return self.reply_app.auth(data, self.conf.token)
            
    def create_menu(self):
        result = self._menu.create(self.access_token)
        return result

    def dispatch_error(err_code):
        self.err_handler.dispatch_error(err_code, self.debug)

    def get(self, url, params=None):
        url = self.url_format(url)
        resp = requests.get(url, params)
        result = json.loads(resp.text)
        if "errcode" in result:
            self.dispatch_error(result.get("errcode"))
        return result

    def post(self, url, data=None, json=None):
        url = self.url_format(url)
        resp = requests.post(url, data=data, json=json)
        result = json.loads(resp.text)
        if "errcode" in result:
            self.dispatch_error(result.get("errcode"), self.debug)
        return result

    def url_format(self, url):
        return url.format(appid=self.conf.appid, appsecret=self.conf.appsecret, 
                            token=self.conf.token, access_token=self.access_token})

    def __getattr__(self, attr_name):
        attr = object.__getattr__(self, attr_name, None)
        if attr is None:
            raise AttributeError("11111")
        return attr

