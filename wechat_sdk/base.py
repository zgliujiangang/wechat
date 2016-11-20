# -*- coding: utf-8 -*-


import json
import requests
import urllib2
import logging
import functools
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from .urls import ApiUrl
from .error import ErrorHandler
from .utils.cache import BaseCache, PickleCache


def url_format_wrap(fn):
    @functools.wraps(fn)
    def wrap(wp, url, *args, **kwargs):
        url = wp.url_format(url)
        return fn(wp, url, *args, **kwargs)
    return wrap


class WechatApp(object):

    def __init__(self, appid, appsecret, **kwargs):
        """微信api访问类
        @param appid: 公众号的appid
        @param appsecret: 公众号的appsecret
        @param token: 用于消息加解密的token
        @param aeskey: 用于消息加解密的EncodingAESKey
        @param paysignkey: 用于支付签名的key
        @param err_handler: 错误处理的类
        @param cache_dir: 存放缓存数据的目录，如果未传cache参数，则必须传入此参数
        @param cache: 实现数据缓存的实例, 有set, get, delete三个方法，继承自BaseCache
        """
        self.appid = appid
        self.appsecret = appsecret
        self.token = kwargs.get("token", None)
        self.aeskey = kwargs.get("aeskey", None)
        self.paysignkey = kwargs.get("paysignkey", None)
        self.err_handler = kwargs.get("err_handler", ErrorHandler)
        cache = kwargs.get("cache")
        if cache:
            assert isinstance(cache, BaseCache), "cache必须是BaseCache的实例"
            self.cache = cache
        else:
            cache_dir = kwargs.get("cache_dir")
            self.cache = PickleCache(cache_dir)

    @property
    def access_token_key(self):
        return "%s:access_token" % self.appid

    @property
    def jsapi_ticket_key(self):
        return "%s:jsapi_ticket" % self.appid

    @property
    def access_token(self):
        access_token = self.cache.get(self.access_token_key)
        if not access_token:
            logging.info("init access_token...")
            access_token = self.init_access_token()
        return access_token

    def init_access_token(self):
        # 每日有调用次数上限，需要缓存结果
        resp = requests.get(ApiUrl.token.format(appid=self.appid, appsecret=self.appsecret))
        result = json.loads(resp.text)
        access_token = result.get("access_token")
        expires_in = result.get("expires_in")
        if access_token and expires_in:
            self.cache.set(self.access_token_key, access_token, expires_in)
            return access_token
        self.err_handler.dispatch_error(result.get("errcode"))

    def delete_access_token(self):
        self.cache.delete(self.access_token_key)

    @property
    def jsapi_ticket(self):
        jsapi_ticket = self.cache.get(self.jsapi_ticket_key)
        if not jsapi_ticket:
            logging.info("init jsapi_ticket...")
            jsapi_ticket = self.init_jsapi_ticket()
        return jsapi_ticket

    def init_jsapi_ticket(self):
        # 每日有调用次数上限，需要缓存结果
        result = self.get(ApiUrl.jsapi_ticket)
        self.cache.set(self.jsapi_ticket_key, result["ticket"], result["expires_in"])
        return result["ticket"]

    def delete_jsapi_ticket(self):
        self.cache.delete(self.jsapi_ticket_key)

    def url_format(self, url):
        return url.format(appid=self.appid, appsecret=self.appsecret, 
                            token=self.token, access_token=self.access_token)

    @url_format_wrap
    def get(self, url, params=None):
        resp = requests.get(url, params)
        result = json.loads(resp.text)
        errcode = result.get("errcode")
        if errcode and str(errcode) != "0":
            self.err_handler.dispatch_error(errcode)
        return result

    @url_format_wrap
    def post(self, url, data=None):
        # data为字典，后面会json转换的
        # 传含有中文字符的json串时需要进行ensure_ascii处理
        data = json.dumps(data, ensure_ascii=False)
        resp = requests.post(url, data=data)
        result = json.loads(resp.text)
        errcode = result.get("errcode")
        if errcode and str(errcode) != "0":
            self.err_handler.dispatch_error(errcode)
        return result

    @url_format_wrap
    def upload(self, url, **file_form):
        # 文件上传，如果有open操作，请在with上下文环境中执行
        register_openers()
        datagen, headers = multipart_encode(file_form)
        request = urllib2.Request(url, datagen, headers)
        result = json.loads(urllib2.urlopen(request).read())
        errcode = result.get("errcode")
        if errcode and str(errcode) != "0":
            self.err_handler.dispatch_error(errcode)
        return result

    @url_format_wrap
    def download(self, url, data=None):
        # 文件下载，返回buffer, 也有可能返回json串
        resp = urllib2.urlopen(url, data=json.dumps(data)).read()
        try:
            result = json.loads(resp)
            errcode = result.get("errcode")
            if errcode and str(errcode) != "0":
                self.err_handler.dispatch_error(errcode)
            # 有的素材会返回media_id所以能被json解析不代表未返回素材
            return {"type": "json", "json": result}
        except Exception as e:
            logging.error(str(e))
            logging.info("maybe download file successfully")
            # resp可以用StringIO.StringIO(resp)处理
            return {"type": "buffer", "buffer": resp}

