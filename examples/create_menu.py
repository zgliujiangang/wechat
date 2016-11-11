# coding: utf-8
import sys
sys.path.append("..")

from examples.init_wechat import wechat
from wechat_sdk.contrib.menu import MediaMenu, ClickMenu, \
ViewMenu, MenuGroup, MenuGroups, MenuManager


def test():
	menumanager = MenuManager(wechat)

	click1 = ClickMenu(name="点击1", key="1111")
	click2 = ClickMenu(name="点击2", key='2222')
	view1 = ViewMenu(name='链接1', url='http://www.hrjia.com')
	view2 = ViewMenu(name='链接2', url='http://www.baidu.com')
	# media_id为上传永久素材获取到的media_id
	# media1 = MediaMenu(name='测试图片', media_id='OVygHfzd3teiBAykiejczQLDG198q6mjeB_ZkNVfyVM')

	group1 = MenuGroup(click1, view1, name='菜单1')
	group2 = MenuGroup(view2, click2, name='菜单2')

	test_menu = MenuGroups(group1, group2)

	# 传入一个MenuGroups的实例是允许的，否则的话自己构造菜单传入
	print menumanager.create_menu(test_menu)
	#print menumanager.create_menu(test_menu.menu)
	#print menumanager.get_menu()
	#print menumanager.delete_menu()

if __name__ == '__main__':
	test()
