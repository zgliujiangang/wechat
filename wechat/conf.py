# coding: utf-8


class WechatConf(object):

    def __init__(self, appid=None, appsecret=None, token=None):
    	assert appid is not None, "appid is none!"
    	assert appsecret is not None, "appsecret is none!"
        self.appid = appid
        self.appsecret = appsecret
        self.token = token


default_conf = test_conf = WechatConf(appid='wechatsdk', appsecret='wechatsdk', token="wechatsdk")
