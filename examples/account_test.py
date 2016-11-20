# -*- coding: utf-8 -*-


import sys; sys.path.append("..")
from examples.base_test import wechat_app
from wechat_sdk.contrib.account import AccountManager


def account_test():
	account_manager = AccountManager(wechat_app)
	result = account_manager.get_shorturl("http://www.baidu.con")
	print result


if __name__ == '__main__':
	account_test()