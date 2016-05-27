# coding: utf-8
import sys
sys.path.append("..")
from examples.init_wechat import wechat
from wechat_sdk.contrib.oauth2 import Oauth2
# 测试oauth接口
def test():
	oauth2 = Oauth2(wechat)
	print oauth2.code_ex_token("11111111111111")
	print oauth2.token_ex_info("11111", "22222")
	print oauth2.auth_url("www.baidu.com?*&&=111")
	print oauth2.check_token("111111", "1111111")
	print oauth2.refresh_token("111111")


if __name__ == '__main__':
	test()