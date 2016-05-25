# coding: utf-8
from urllib import quote
from .wechat import Wechat
from .urls import ApiUrl


class Oauth2(object):

    base = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"
    info = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
    def __init__(self, wechat):
        assert isinstance(wechat, Wechat), "wechat must be a Wechat instance"
        self.wechat = wechat

    def access_token_openid(self, code):
        url = ApiUrl.oauth2_token % code
        result = self.wechat.get(url)
        _access_token, openid = result.get("access_token"), result.get("openid")
        return _access_token, openid

    def userinfo(self, access_token, openid):
        url = ApiUrl.userinfo % (access_token, openid)
        result = self.wechat.get(url)
        return result

    def base_url(self, url):
        return self.base % (self.wechat.conf.appid, quote(url))

    def info_url(self, url):
        return self.info % (self.wechat.conf.appid, quote(url))