# -*- coding: utf-8 -*-
# 微信网页开发


from urllib import quote
from ..urls import ApiUrl


class Scope:
    base = "snsapi_base"
    userinfo = "snsapi_userinfo"


class Oauth2(object):

    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect"

    def __init__(self, wechat):
        self.wechat = wechat

    def code_ex_token(self, code):
        url = ApiUrl.oauth2_token % code
        return self.wechat.get(url)
        
    def token_ex_info(self, access_token, openid):
        url = ApiUrl.oauth2_userinfo % (access_token, openid)
        return self.wechat.get(url)

    def refresh_token(self, retoken):
        url = ApiUrl.oauth2_refresh % retoken
        # debug here
        with self.wechat:
            return self.wechat.get(url)

    def check_token(self, access_token, openid):
        url = ApiUrl.oauth2_check % (access_token, openid)
        return self.wechat.get(url)

    def auth_url(self, url, scope=Scope.base, state="STATE", url_encode=True):
        if url_encode:
            url = quote(url)
        url = self.url % (self.wechat.conf.appid, url, scope, state)
        return url





