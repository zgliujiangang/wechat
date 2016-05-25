# coding: utf-8
import sys
import json
sys.path.append(".")

from wechat.wechat import Wechat
from wechat.conf import WechatConf
from wechat.urls import ApiUrl
from wechat.menu import default_menu

conf = WechatConf(appid="wxa8e2f9be2c6f347c", appsecret="0ed8890e310546b8ef45e1db174b2145", token="hrjiaweixin123")

wechat = Wechat(conf=conf)

print wechat.access_token
print default_menu.menu
print wechat.post(ApiUrl.create_menu, data=json.dumps(default_menu.menu))
# 编码有问题待解决



