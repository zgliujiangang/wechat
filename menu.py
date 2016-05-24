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

    def menu(self):
        menu_dict = {"type": self.type, "name": self.name}
        menu_dict.update(self.params)
        return menu_dict


Menu = with_metaclass(MenuMeta, MenuBase)

class ClickMenu(Menu):

    type = 'click'
    
    def __init__(self, name=None, key=None):
        self.name = name
        self.params = {'key': key}


class ViewMenu(Menu):

    type = 'view'
    
    def __init__(self, name=None, url=None):
        self.name = name
        self.params = {'url': url}

class MediaMenu(Menu):

    type = 'media_id'
    
    def __init__(self, name=None, media_id=None):
        self.name = name
        self.params = {'media_id': media_id}


class scancode_pushMenu(Menu):

    type = 'scancode_push'
    
    def __init__(self, name=None, key=None):
        self.name = name
        self.params = {'key': key}


class scancode_waitmsgMenu(Menu):

    type = 'scancode_waitmsg'
    
    def __init__(self, name=None, key=None):
        self.name = name
        self.params = {'key': key}


class pic_sysphotoMenu(Menu):

    type = 'pic_sysphoto'
    
    def __init__(self, name=None, key=None):
        self.name = name
        self.params = {'key': key}


class pic_photo_or_albumMenu(Menu):

    type = 'pic_photo_or_album'
    
    def __init__(self, name=None, key=None):
        self.name = name
        self.params = {'key': key}


class pic_weixinMenu(Menu):

    type = 'pic_weixin'
    
    def __init__(self, name=None, key=None):
        self.name = name
        self.params = {'key': key}


class location_selectMenu(Menu):

    type = 'location_select'
    
    def __init__(self, name=None, key=None):
        self.name = name
        self.params = {'key': key}


class view_limitedMenu(Menu):

    type = 'view_limited'
    
    def __init__(self, name=None, media_id=None):
        self.name = name
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



"""
from wechat.menu import ClickMenu, ViewMenu, MenuGroup, MenuGroups

click1 = ClickMenu(name="你好", key="1111")
click2 = ClickMenu(name="wwo", key='2222')
view1 = ViewMenu(name='1111', url='http://www.hrjia.com')
view2 = ViewMenu(name='2222', url='http://www.baidu.com')
media = MediaMenu(name='xxs', media_id='111111111111111')

group1 = MenuGroup(click1, name='菜单1')
group2 = MenuGroup(view2, click1, name='菜单2')

menu1 = MenuGroups(group1, group2).menu
menu2 = MenuGroups(click1, group2).menu

print menu
"""