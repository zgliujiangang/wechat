# coding: utf-8
from urllib import quote
from ..wechat import Wechat
from ..urls import ApiUrl


#网页授权必须配置授权回调域名
#网页授权的access_token与获取基础信息的access_token不是同一个东西

class Scope(object):
    base = "snsapi_base"
    userinfo = "snsapi_userinfo"


class Oauth2(object):

    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect"

    def __init__(self, wechat):
        assert isinstance(wechat, Wechat), "wechat must be a Wechat instance"
        self.wechat = wechat

    def code_ex_token(self, code):
        url = ApiUrl.oauth2_token % code
        # debug here
        with self.wechat:
            return self.wechat.get(url)
        
    def token_ex_info(self, access_token, openid):
        url = ApiUrl.oauth2_userinfo % (access_token, openid)
        return self.wechat.get(url)

    def refresh_token(self, retoken):
        url = ApiUrl.oauth2_refresh % retoken
        return self.wechat.get(url)

    def check_token(self, access_token, openid):
        url = ApiUrl.oauth2_check % (access_token, openid)
        return self.wechat.get(url)

    def auth_url(self, url, scope=Scope.base, state="STATE", url_encode=True):
        if url_encode:
            url = quote(url)
        url = self.url % (self.wechat.conf.appid, url, scope, state)
        return url





