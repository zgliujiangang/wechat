# -*- coding: utf-8 -*-


import sys; sys.path.append("..")
from examples.base_test import wechat_app
from wechat_sdk.contrib.web import WebManager


def test():
    web_manager = WebManager(wechat_app)
    auth_url = web_manager.make_auth_url("http://www.baidu.com")
    print auth_url
    js_config = web_manager.make_js_config("http://127.0.0.1/")
    print js_config


if __name__ == '__main__':
    test()