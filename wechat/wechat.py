# coding: utf-8
import requests
import json
import urllib2
import memcache
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from .conf import WechatConf, default_conf
from .urls import ApiUrl
from .error import ErrorHandler


class Wechat(object):

    def __init__(self, conf=default_conf, err_handler=ErrorHandler, debug=False):
        assert isinstance(conf, WechatConf), "conf object must be a WechatConf instance!"
        self._conf = conf
        self.err_handler = err_handler
        self.debug = debug

    def get_access_token(self):
        access_token = self.get_cache_access_token()
        if not access_token:
            print "i am init access_token"
            access_token = self.init_access_token()
        return access_token

    def init_access_token(self):
        # 每日有调用次数上限，需要缓存结果
        resp = requests.get(ApiUrl.token.format(appid=self._conf.appid, appsecret=self._conf.appsecret))
        result = json.loads(resp.text)
        access_token = result.get("access_token")
        expires_in = result.get("expires_in")
        if access_token and expires_in:
            self.cache_access_token(access_token, expires_in)
            return access_token
        self.err_handler.dispatch_error(result.get("errcode"))

    def cache_access_token(self, access_token, expires_in):
        """
        缓存access_token
        redis eg: 
        redis_for_token.set(access_token_key, access_token, expires_in)
        """
        access_token_key = self._conf.appid
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        mc.set(access_token_key, access_token, int(expires_in)-30)

    def get_cache_access_token(self):
        """
        获取缓存的access_token
        redis eg:
        access_token = redis_for_token.get(access_token_key)
        if not access_token:
            return None
        return access_token
        """
        access_token_key = self._conf.appid
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        return mc.get(access_token_key)

    access_token = property(get_access_token)
    del get_access_token

    def dispatch_error(self, errcode):
        if not self.debug:
            print errcode
        else:
            self.err_handler.dispatch_error(errcode)

    def url_format(self, url):
        return url.format(appid=self._conf.appid, appsecret=self._conf.appsecret, 
                            token=self._conf.token, access_token=self.access_token)

    def get(self, url, params=None):
        url = self.url_format(url)
        resp = requests.get(url, params)
        result = json.loads(resp.text)
        if "errcode" in result:
            self.dispatch_error(result.get("errcode"))
        return result

    def post(self, url, data=None, _json=None):
        url = self.url_format(url)
        resp = requests.post(url, data=data, json=_json)
        result = json.loads(resp.text)
        if "errcode" in result:
            self.dispatch_error(result.get("errcode"))
        return result

    def upload(self, url, **file_form):
        #result = wechat.upload("https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}", media=open(file_path, 'rb'), title='test')
        register_openers()
        url = self.url_format(url)
        datagen, headers = multipart_encode(file_form)
        request = urllib2.Request(url, datagen, headers)
        result = json.loads(urllib2.urlopen(request).read())
        if "errcode" in result:
            self.dispatch_error(result.get("errcode"))
        return result

    def jsconf(self, url):
        # return {"appId": appID, "timestamp": timestamp, "nonceStr": nonceStr, "signature": signature}
        pass

    def __enter__(self):
        self.real_debug = self.debug
        self.debug = True

    def __exit__(self):
        self.debug = self.real_debug
        del self.real_debug

    def __getattr__(self, attr_name):
        attr = object.__getattr__(self, attr_name, None)
        if attr is None:
            raise AttributeError("wechat please set this attribute before use it:%s" % attr_name)
        return attr

