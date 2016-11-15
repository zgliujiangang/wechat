# -*- coding: utf-8 -*-

import json
import sys; sys.path.append("..")
from examples.base_test import wechat_app
from wechat_sdk.contrib.menu import mediaButton, clickButton, \
viewButton, SubButtonGroup, MainButtonGroup, MenuManager


def test():
    menu_manager = MenuManager(wechat_app)
    click1 = clickButton(name="点击1", key="1111")
    click2 = clickButton(name="点击2", key='2222')
    click3 = clickButton(name="点击3", key="333")
    view1 = viewButton(name='链接1', url='http://www.hrjia.com')
    view2 = viewButton(name='链接2', url='http://www.baidu.com')

    group1 = SubButtonGroup('菜单1', click1, view1)
    group2 = SubButtonGroup('菜单2', view2, click2)

    test_menu = MainButtonGroup(group1, click3, group2)

    # 传入一个MainButtonGroup的实例是允许的，否则的话自己构造菜单传入
    # print menu_manager.create(test_menu)
    menu = menu_manager.get()
    print menu
    current_menu = menu_manager.get_current()
    print current_menu


if __name__ == '__main__':
    test()
