# coding: utf-8

from .utils import with_metaclass
"""
请注意，3到8的所有事件，仅支持微信iPhone5.4.1以上版本，\
和Android5.4以上版本的微信用户，旧版本微信用户点击后将没有回应，\
开发者也不能正常接收到事件推送。9和10，是专门给第三方平台旗下未微信认证\
（具体而言，是资质认证未通过）的订阅号准备的事件类型，它们是没有事件推送的，\
能力相对受限，其他类型的公众号不必使用。
"""

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

    def convert(self):
        menu = {"type": self.type, "name": self.name}
        menu.update(self.params)
        return menu


Menu = with_metaclass(MenuMeta, MenuBase)

class ClickMenu(Menu):

    type = 'click'
    
    def __init__(self, name, key):
        self.name = name
        self.params = {'key': key}


class ViewMenu(Menu):

    type = 'view'
    
    def __init__(self, name, url):
        self.name = name
        self.params = {'url': url}

class MediaMenu(Menu):

    type = 'media_id'
    
    def __init__(self, name, media_id):
        self.name = name
        self.params = {'media_id': media_id}


class scancode_pushMenu(Menu):

    type = 'scancode_push'
    
    def __init__(self, name, key):
        self.name = name
        self.params = {'key': key}


class scancode_waitmsgMenu(Menu):

    type = 'scancode_waitmsg'
    
    def __init__(self, name, url):
        self.name = name
        self.params = {'url': url}


class pic_sysphotoMenu(Menu):

    type = 'pic_sysphoto'
    
    def __init__(self, name, url):
        self.name = name
        self.params = {'url': url}


class pic_photo_or_albumMenu(Menu):

    type = 'pic_photo_or_album'
    
    def __init__(self, name, url):
        self.name = name
        self.params = {'url': url}


class pic_weixinMenu(Menu):

    type = 'pic_weixin'
    
    def __init__(self, name, url):
        self.name = name
        self.params = {'url': url}


class location_selectMenu(Menu):

    type = 'location_select'
    
    def __init__(self, name, url):
        self.name = name
        self.params = {'url': url}


class view_limitedMenu(Menu):

    type = 'view_limited'
    
    def __init__(self, name, url):
        self.name = name
        self.params = {'url': url}


# menu container
class MenuGroup(object):

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.menu_list = args
        self.no_sub = kwargs.get("no_sub", True)
    
    def menu(self):
        if len(self.menu_list) == 1 and self.no_sub:
            return self.menu_list[-1].convert()
        else:
            return {"name": self.name, "sub_button": [menu.convert() for menu in self.menu_list]}

class MenuGroups(object):

    menu = None
    def __init__(self, *group_list):
        self.menu = {"button": [group.menu() for group in group_list]}



"""
from flask_wechat.menu import ClickMenu, ViewMenu, MenuGroup, MenuGroups

click1 = ClickMenu("你好", "1111")
click2 = ClickMenu("wwo", '2222')
view1 = ViewMenu('1111', 'http://www.hrjia.com')
view2 = ViewMenu('2222', 'http://www.baidu.com')

group1 = MenuGroup('菜单1', click1, view1)
group2 = MenuGroup('菜单2', view2, click1)

menu = MenuGroups(group1, group2).menu

print menu
"""