# coding: utf-8
import requests
import json
import urllib2
import memcache
import time
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from .conf import WechatConf, default_conf
from .urls import ApiUrl
from .error import ErrorHandler
from .utils import random_str


class Wechat(object):

    def __init__(self, conf=default_conf, err_handler=ErrorHandler, debug=False):
        assert isinstance(conf, WechatConf), "conf object must be a WechatConf instance!"
        self.conf = conf
        self.err_handler = err_handler
        self.debug = debug

    def cache_data(self, key, value, expires_in):
        """
        缓存access_token
        redis eg: 
        redis_for_token.set(access_token_key, access_token, expires_in)
        """
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        mc.set(key, access_token, int(expires_in)-30)

    def get_cache_data(self, key):
        """
        获取缓存的access_token
        redis eg:
        access_token = redis_for_token.get(access_token_key)
        if not access_token:
            return None
        return access_token
        """
        mc = memcache.Client(['127.0.0.1:11211'], debug=0)
        return mc.get(key)

    def get_access_token(self):
        access_token_key = "%s:access_token" % self.conf.appid
        access_token = self.get_cache_data(access_token_key)
        if not access_token:
            print "here init access_token"
            access_token = self.init_access_token()
        return access_token

    def init_access_token(self):
        # 每日有调用次数上限，需要缓存结果
        resp = requests.get(ApiUrl.token.format(appid=self.conf.appid, appsecret=self.conf.appsecret))
        result = json.loads(resp.text)
        access_token = result.get("access_token")
        expires_in = result.get("expires_in")
        if access_token and expires_in:
            access_token_key = "%s:access_token" % self.conf.appid
            self.cache_data(access_token_key, access_token, expires_in)
            return access_token
        self.err_handler.dispatch_error(result.get("errcode"))

    access_token = property(get_access_token)
    del get_access_token

    def get_jsapi_ticket(self):
        jsapi_ticket_key = "%s:jsapi_ticket" % self.conf.appid
        jsapi_ticket = self.get_cache_data(jsapi_ticket_key)
        if not jsapi_ticket:
            print "here init jsapi_ticket"
            jsapi_ticket = self.init_jsapi_ticket()
        return jsapi_ticket

    def init_jsapi_ticket(self):
        # 每日有调用次数上限，需要缓存结果
        with self:
            result = self.get(ApiUrl.jsapi_ticket)
        jsapi_ticket_key = "%s:jsapi_ticket" % self.conf.appid
        self.cache_data(jsapi_ticket_key, result["ticket"], result["expires_in"])
        return result["ticket"]

    jsapi_ticket = property(get_jsapi_ticket)
    del get_jsapi_ticket

    def dispatch_error(self, errcode):
        if not self.debug:
            print errcode
        else:
            self.err_handler.dispatch_error(errcode)

    def url_format(self, url):
        return url.format(appid=self.conf.appid, appsecret=self.conf.appsecret, 
                            token=self.conf.token, access_token=self.access_token)

    def get(self, url, params=None):
        url = self.url_format(url)
        resp = requests.get(url, params)
        result = json.loads(resp.text)
        errcode = result.get("errcode")
        if errcode and str(errcode) != "0":
            self.dispatch_error(errcode)
        return result

    def post(self, url, data=None):
        # 参数data直接传字典进来，不要json编码，我后面会编码的
        url = self.url_format(url)
        # 传含有中文字符的json串时需要进行ensure_ascii处理
        data = json.dumps(data, ensure_ascii=False)
        resp = requests.post(url, data=data)
        result = json.loads(resp.text)
        errcode = result.get("errcode")
        if errcode and str(errcode) != "0":
            self.dispatch_error(errcode)
        return result

    def upload(self, url, **file_form):
        #result = wechat.upload("https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}", media=open(file_path, 'rb'), title='test')
        register_openers()
        url = self.url_format(url)
        datagen, headers = multipart_encode(file_form)
        request = urllib2.Request(url, datagen, headers)
        result = json.loads(urllib2.urlopen(request).read())
        errcode = result.get("errcode")
        if errcode and str(errcode) != "0":
            self.dispatch_error(errcode)
        return result

    def download(self, url, data=None):
        url = self.url_format(url)
        resp = urllib2.urlopen(url, data=data).read()
        try:
            result = json.loads(resp)
            print result
            errcode = result.get("errcode")
            if errcode and str(errcode) != "0":
                self.dispatch_error(errcode)
            # 有的素材会返回media_id所以能被json解析不代表未返回素材
            return {"type": "json", "result": result}
        except Exception as e:
            print "maybe download file successfully"
            # resp可以用StringIO.StringIO(resp)处理
            return {"type": "buffer", "result": resp}

    def jsconf(self, url):
        noncestr = random_str()
        timestamp = int(time.time())
        params = dict(noncestr=noncestr, url=url, timestamp=timestamp, jsapi_ticket=self.jsapi_ticket)
        items = params.items()
        items.sort(key=lambda x: x[0])
        params_string = '&'.join(['%s=%s' % item for item in items])
        signature = hashlib.sha1(params_string).hexdigest()
        return dict(appId=self.conf.appid, timestamp=timestamp, nonceStr=noncestr, signature=signature)

    def __enter__(self):
        self.real_debug = self.debug
        self.debug = True

    def __exit__(self, exc_type, exc_value, traceback):
        self.debug = self.real_debug
        del self.real_debug

