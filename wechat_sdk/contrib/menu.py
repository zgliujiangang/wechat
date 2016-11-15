# -*- coding: utf-8 -*-
# 自定义菜单


import json
from ..utils.common import with_metaclass
from ..urls import ApiUrl


# 菜单按钮类型集合
BUTTON_SET = frozenset(['click', 'view', 'scancode_push', 'scancode_waitmsg', 'pic_sysphoto', \
    'pic_photo_or_album', 'pic_weixin', 'location_select', 'media_id', 'view_limited'])


class ButtonMeta(type):

    def __new__(cls, clsname, bases, d):
        button_type = d.get("Meta").button_type
        if button_type.lower() not in BUTTON_SET:
            raise AttributeError("has no such type: %s" % button_type)
        return type.__new__(cls, clsname, bases, d)


class ButtonBase(object):

    @property
    def data(self):
        _data = {}
        meta_cls = self.Meta
        for field in meta_cls.field_list:
            _data[field] = getattr(self, field)
        _data["type"] = meta_cls.button_type
        return _data


Button = with_metaclass(ButtonMeta, ButtonBase)


class clickButton(Button):
    # 点击

    def __init__(self, name, key):
        self.name = name
        self.key = key

    class Meta:
        button_type = "click"
        field_list = ("name", "key")


class viewButton(Button):
    # 链接
    
    def __init__(self, name, url):
        self.name = name
        self.url = url

    class Meta:
        button_type = "view"
        field_list = ("name", "url")


class mediaButton(Button):
    # 图片
    
    def __init__(self, name, media_id):
        self.name = name
        self.media_id = media_id

    class Meta:
        button_type = "media_id"
        field_list = ("name", "media_id")


class scancode_pushButton(Button):
    # 扫码推事件
    
    def __init__(self, name, key):
        self.name = name
        self.key = key

    class Meta:
        button_type = "scancode_push"
        field_list = ("name", "key")


class scancode_waitmsgMenu(Button):
    # 扫码带提示
    
    def __init__(self, name, key):
        self.name = name
        self.key = key

    class Meta:
        button_type = "scancode_waitmsg"
        field_list = ("name", "key")


class pic_sysphotoButton(Button):
    # 系统拍照发图
    
    def __init__(self, name, key):
        self.name = name
        self.key = key

    class Meta:
        button_type = "pic_sysphoto"
        field_list = ("name", "key")


class pic_photo_or_albumButton(Button):
    # 拍照或者相册发图
    
    def __init__(self, name, key):
        self.name = name
        self.key = key

    class Meta:
        button_type = "pic_photo_or_album"
        field_list = ("name", "key")


class pic_weixinButton(Button):
    # 微信相册发图
    
    def __init__(self, name, key):
        self.name = name
        self.key = key

    class Meta:
        button_type = "pic_weixin"
        field_list = ("name", "key")


class location_selectButton(Button):
    # 发送位置

    def __init__(self, name, key):
        self.name = name
        self.key = key

    class Meta:
        button_type = "location_select"
        field_list = ("name", "key")


class view_limitedButton(Button):
    # 图文消息
    
    def __init__(self, name, media_id):
        self.name = name
        self.media_id = media_id

    class Meta:
        button_type = "view_limited"
        field_list = ("name", "media_id")


class SubButtonGroup(ButtonBase):
    # 二级菜单组

    def __init__(self, name, *button_list):
        if len(button_list) > 5:
            raise Exception("二级菜单按钮最多不能超过5个，现有%s个二级菜单按钮" % len(button_list))
        self.name = name
        self.button_list = button_list
    
    @property
    def data(self): 
        return {"name": self.name, "sub_button": [button.data for button in self.button_list]}


class MainButtonGroup(ButtonBase):
    # 一级菜单组

    def __init__(self, *button_list):
        if len(button_list) > 3:
            raise Exception("一级菜单不能超过三个，现有%s个一级菜单" % len(button_list))
        self.button_list = button_list

    @property
    def data(self):
        return {"button": [button.data for button in self.button_list]}


class MenuManager(object):
    # menu manage 菜单管理

    def __init__(self, wp):
        self.wp = wp

    def create(self, data):
        # 自定义菜单创建
        if isinstance(data, MainButtonGroup):
            data = data.data
        return self.wp.post(ApiUrl.create_menu, data=data)

    def get(self):
        # 自定义菜单查询
        return self.wp.get(ApiUrl.get_menu)

    def get_current(self):
        # 公众号当前菜单配置
        return self.wp.get(ApiUrl.get_current_menu)

    def delete(self):
        # 自定义菜单删除
        return self.wp.get(ApiUrl.delete_menu)