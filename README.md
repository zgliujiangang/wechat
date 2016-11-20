### Wechat SDK:微信公众号开发第三方库

##### 安装
	1、git clone https://github.com/zgliujiangang/wechat.git
	2、cd wechat
	3、python setup.py install
##### 使用
```python
from wechat_sdk import WechatApp
appid = "wxa8e2f9be2c6f347c"
appsecret = "0ed8890e310546b8ef45e1db174b2145"
cache_dir = "user/myfolder/cache_dir"
wechat_app = WechatApp(appid, appsecret, cache_dir)
print wechat_app.access_token
print wechat_app.jsapi_ticket
```
	微信各模块使用请参考examples
##### 卸载
	pip uninstall wechat_sdk