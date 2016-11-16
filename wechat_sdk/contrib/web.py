# -*- coding: utf-8 -*-
# 微信网页开发


import time
import hashlib
from urllib import quote
from ..urls import ApiUrl
from ..utils.common import random_str


class Scope:
    # base静默授权，用户无感知，userinfo弹出授权页面，用户感知
    base = "snsapi_base"
    userinfo = "snsapi_userinfo"


class WebManager(object):
    # 网页授权中的access_token与访问微信api接口所需的access_token不是同一个概念

    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect"

    def __init__(self, wp):
        self.wp = wp

    def get_access_token(self, code):
        """通过code换取access_token
        @param code: 授权回调后，第三方url上携带的code
        """
        return self.wp.get(ApiUrl.oauth2_token % code)

    def refresh_access_token(self, refresh_token):
        """用refresh_token刷新access_token
        @param refresh_token: code换取access_token接口返回的refresh_token
        """
        url = ApiUrl.oauth2_refresh % refresh_token
        return self.wp.get(url)

    def auth_access_token(self, access_token, openid):
        """验证access_token是否有效
        @param access_token: code换取的access_token
        @param openid: 需要拉取信息用户的open_id
        """
        url = ApiUrl.oauth2_auth_token % (access_token, openid)
        return self.wp.get(url)

    def get_userinfo(self, access_token, openid):
        """拉取用户信息, 有两种情况可成功拉取 1、scope为userinfo一定能拉取，2、scope为base,但用户不久前已授权过userinfo
        @param access_token: code换取的access_token
        @param openid: 需要拉取信息用户的open_id
        """
        url = ApiUrl.oauth2_userinfo % (access_token, openid)
        return self.wp.get(url)

    def make_auth_url(self, redirect_uri, scope=Scope.base, state="STATE", url_encode=True):
        """生成用于授权的url
        @param redirect_uri: 授权回调的uri
        @param scope: 授权级别，base或者userinfo
        @param url_encode: 是否对url进行encode
        """
        if url_encode:
            redirect_uri = quote(redirect_uri)
        url = self.url % (self.wp.appid, redirect_uri, scope, state)
        return url

    def make_js_config(self, url):
        """生成用于网页开发的js config
        @param url: 调取js sdk页面的url
        """
        noncestr = random_str()
        timestamp = int(time.time())
        params = dict(noncestr=noncestr, url=url, timestamp=timestamp, jsapi_ticket=self.wp.jsapi_ticket)
        items = params.items()
        items.sort(key=lambda x: x[0])
        params_string = '&'.join(['%s=%s' % item for item in items])
        signature = hashlib.sha1(params_string).hexdigest()
        return dict(appId=self.wp.appid, timestamp=timestamp, nonceStr=noncestr, signature=signature)

