# coding: utf-8


class WechatConf(object):

    def __init__(self, appid=None, appsecret=None, token=None):
        self.appid = appid
        self.appsecret = appsecret
        self.token = token

    def __getattr__(self, attr_name):
        attr =  object.__getattr__(self, attr_name, None)
        if attr is None:
            raise AttributeError("wechatconf please set this attribute before use it:%s" % attr_name)
        return attr


default_conf = test_conf = WechatConf(appid='88888888', appsecret='88888888', token="88888888")
