# coding: utf-8
# 自定义菜单
import json
from ..utils import with_metaclass

type_set = frozenset(['click', 'view', 'scancode_push', 'scancode_waitmsg', 'pic_sysphoto', \
    'pic_photo_or_album', 'pic_weixin', 'location_select', 'media_id', 'view_limited'])

class MenuMeta(type):

    def __new__(cls, clsname, bases, d):
        menu_type = d.get("type")
        if not menu_type:
            raise KeyError("has no attribute: type")
        if menu_type.lower() not in type_set:
            raise AttributeError("has no such type")
        return type.__new__(cls, clsname, bases, d)


class MenuBase(object):

    def menu(self):
        menu_dict = {"type": self.type.lower(), "name": self.name}
        menu_dict.update(self.params)
        return menu_dict


Menu = with_metaclass(MenuMeta, MenuBase)

class ClickMenu(Menu):

    type = 'click'
    
    def __init__(self, name=None, key=None):
        self.name = name
        self.key = key
        self.params = {'key': key}


class ViewMenu(Menu):

    type = 'view'
    
    def __init__(self, name=None, url=None):
        self.name = name
        self.url = url
        self.params = {'url': url}

class MediaMenu(Menu):

    type = 'media_id'
    
    def __init__(self, name=None, media_id=None):
        self.name = name
        self.media_id = media_id
        self.params = {'media_id': media_id}


class scancode_pushMenu(Menu):

    type = 'scancode_push'
    
    def __init__(self, name=None, key=None):
        self.name = name
        self.key = key
        self.params = {'key': key}


class scancode_waitmsgMenu(Menu):

    type = 'scancode_waitmsg'
    
    def __init__(self, name=None, key=None):
        self.name = name
        self.key = key
        self.params = {'key': key}


class pic_sysphotoMenu(Menu):

    type = 'pic_sysphoto'
    
    def __init__(self, name=None, key=None):
        self.name = name
        self.key = key
        self.params = {'key': key}


class pic_photo_or_albumMenu(Menu):

    type = 'pic_photo_or_album'
    
    def __init__(self, name=None, key=None):
        self.name = name
        self.key = key
        self.params = {'key': key}


class pic_weixinMenu(Menu):

    type = 'pic_weixin'
    
    def __init__(self, name=None, key=None):
        self.name = name
        self.key = key
        self.params = {'key': key}


class location_selectMenu(Menu):

    type = 'location_select'
    
    def __init__(self, name=None, key=None):
        self.name = name
        self.key = key
        self.params = {'key': key}


class view_limitedMenu(Menu):

    type = 'view_limited'
    
    def __init__(self, name=None, media_id=None):
        self.name = name
        self.media_id = media_id
        self.params = {'media_id': media_id}


# menu container
class MenuGroup(MenuBase):

    def __init__(self, *args, **kwargs):
        if len(args) > 5:
            raise Exception("二级菜单最多不能超过5个，现有%s个二级菜单" % len(args))
        self.name = kwargs.pop("name")
        self.menu_list = args
    
    def menu(self):
        return {"name": self.name, "sub_button": [menu.menu() for menu in self.menu_list]}

class MenuGroups(object):

    menu = None
    def __init__(self, *group_list):
        if len(group_list) > 3:
            raise Exception("一级菜单不能超过三个，现有%s个一级菜单" % len(group_list))
        self.menu = {"button": [group.menu() for group in group_list]}
        self.group_list = group_list


"""
click1 = ClickMenu(name="点击1", key="1111")
click2 = ClickMenu(name="点击2", key='2222')
view1 = ViewMenu(name='链接1', url='http://www.hrjia.com')
view2 = ViewMenu(name='链接2', url='http://www.baidu.com')
media1 = MediaMenu(name='图片1', media_id='111111111111111')

group1 = MenuGroup(click1, view1, name='菜单1')
group2 = MenuGroup(view2, click2, name='菜单2')

test_menu = MenuGroups(group1, group2)
"""

    