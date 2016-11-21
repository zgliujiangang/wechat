### Wechat SDK:微信公众号开发第三方库

##### 安装
	1、git clone https://github.com/zgliujiangang/wechat.git
	2、cd wechat
	3、python setup.py install
##### 使用
	获取公众号的access_token和jsapi_ticket:
```python
# -*- coding: utf-8 -*-
from wechat_sdk import WechatApp

appid = "wxa8e2f9be2c6f347c"
appsecret = "0ed8890e310546b8ef45e1db174b2145"
cache_dir = "/home/user/cache_dir" # cache_dir是一个系统目录用于存放缓存数据
wechat_app = WechatApp(appid, appsecret, cache_dir=cache_dir)
print wechat_app.access_token
print wechat_app.jsapi_ticket
```
	目前sdk实现了公众号以下六大模块的功能，基本能满足一般需求:
	1 [自定义菜单]|(/wechat_sdk/contrib/menu.py)
	2 [消息管理]|(/wechat_sdk/contrib/msg.py)
	3 [微信网页开发]|(/wechat_sdk/contrib/web.py)
	4 [素材管理]|(/wechat_sdk/contrib/media.py)
	5 [用户管理]|(/wechat_sdk/contrib/user.py)
	6 [账号管理]|(/wechat_sdk/contrib/account.py)

	微信各模块使用教程请参考[examples](/examples/)
##### 卸载
	pip uninstall wechat_sdk