# -*- coding: utf-8 -*-


import sys; sys.path.append("..")
from examples.base_test import wechat_app
from wechat_sdk.contrib.user import UserManager


def user_test():
    user_manager = UserManager(wechat_app)
    user_list = user_manager.get_userlist()
    print user_list
    openid = user_list["data"]["openid"][0]
    user_info = user_manager.get_userinfo(openid)
    print user_info
    user_list = [{"openid": openid, "lang": "zh-CN"} for openid in user_list["data"]["openid"]]
    users_info = user_manager.batch_get_userinfo(user_list)
    print users_info


if __name__ == '__main__':
    user_test()