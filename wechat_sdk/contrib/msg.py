# -*- coding: utf-8 -*-
# 消息管理


import logging
import hashlib
from functools import wraps
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from ..utils.common import random_str
from ..urls import ApiUrl


def clear_text_decorator(func):
    # 明文模式装饰器
    @wraps(func)
    def decorator(msg_handler, xml, args):
        xml_tree = ET.fromstring(xml)
        try:
            msg_type = xml_tree.find("MsgType").text
        except AttributeError:
            msg_type = ""
        try:
            event = xml_tree.find("Event").text
        except AttributeError:
            event = ""
        response = func((msg_type, event), xml_tree)
        return response
    return decorator


def cipher_text_decorator(func):
    # 密文模式装饰器
    @wraps(func)
    def decorator(msg_handler, xml, args):
        de_ret, xml = msg_handler.msgcrypt.DecryptMsg(xml, args.get("msg_signature"), 
            args.get("timestamp"), args.get("nonce"))
        xml_tree = ET.fromstring(xml)
        try:
            msg_type = xml_tree.find("MsgType").text
        except AttributeError:
            msg_type = ""
        try:
            event = xml_tree.find("Event").text
        except AttributeError:
            event = ""
        response = func((msg_type, event), xml_tree)
        nonce = random_str(min_length=10, max_length=10)
        en_ret, response = msg_handler.msgcrypt.EncryptMsg(response, nonce)
        return response
    return decorator


class MsgHandler(object):
    #回复微信消息的类

    def __init__(self, wc, default="success", crypto=False):
        # crypto 是否加密[False:明文(未加密) True:密文(已加密)]
        # 通过设置crypto可以动态改变加解密模式
        self.wc = wc
        self.default = default
        self.crypto = crypto
        self.register_funcs = dict()

    @property
    def crypto(self):
        return self._crypto

    @crypto.setter
    def crypto(self, value):
        self._crypto = value
        if value:
            # 密文通讯
            from ..wx_crypto.WXBizMsgCrypt import WXBizMsgCrypt
            self.msgcrypt = WXBizMsgCrypt(self.wc.token, self.wc.aeskey, self.wc.appid)
            self.response = cipher_text_decorator(self.response)
        else:
            # 明文通讯
            self.msgcrypt = None
            self.response = clear_text_decorator(self.response)

    def route(self, msg_type):
        # msg_type是一个二元元祖,如("event", "click")
        def wrap(func):
            self.register(msg_type, func)
            return func
        return wrap

    def register(self, msg_type, func):
        msg_type = self.convert(msg_type)
        self.register_funcs[msg_type] = func

    def response(self, msg_type, params):
        # 回复微信消息
        try:
            msg_type = self.convert(msg_type)
            return self.register_funcs[msg_type](params) or self.default
        except KeyError as e:
            logging.error(str(e))
            return self.default
        except Exception as e:
            logging.error(str(e))
            raise e

    def convert(self, msg_type):
        msg_type = tuple([item.lower() for item in msg_type])
        return msg_type

    def auth(self, data, token):
        # 服务器接入验证
        try:
            params = [data.get("timestamp"), data.get("nonce"), token]
            params.sort()
            params_string = "".join(params)
            signature = hashlib.sha1(params_string).hexdigest()
            if signature == data.get("signature"):
                return data.get("echostr")
            else:
                logging.info("微信服务器接入验证时签名不匹配") 
                return "FAIL"
        except Exception as e:
            logging.error(str(e))
            return "FAIL"

    def __call__(self, xml=None, args=None, auth=False):
        #param xml:post消息体中的xml字符串
        #param args:url上携带的参数字典
        if not auth:
            return self.response(self, xml, args)
        else:
            # 服务器接入验证
            return self.auth(args, self.wc.token)


class ReplyTemplate(object):

    TEXT = """
            <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
            </xml>
            """

    IMAGE = """
            <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[%s]]></MediaId>
                </Image>
            </xml>
            """
    VOICE = """
            <xml>
                <ToUserName><![CDATA[toUser]]></ToUserName>
                <FromUserName><![CDATA[fromUser]]></FromUserName>
                <CreateTime>12345678</CreateTime>
                <MsgType><![CDATA[voice]]></MsgType>
                <Voice>
                <MediaId><![CDATA[media_id]]></MediaId>
                </Voice>
            </xml>
            """

    VIDEO = """
            <xml>
                <ToUserName><![CDATA[toUser]]></ToUserName>
                <FromUserName><![CDATA[fromUser]]></FromUserName>
                <CreateTime>12345678</CreateTime>
                <MsgType><![CDATA[video]]></MsgType>
                <Video>
                <MediaId><![CDATA[media_id]]></MediaId>
                <Title><![CDATA[title]]></Title>
                <Description><![CDATA[description]]></Description>
                </Video> 
            </xml>
            """
    MUSIC = """
            <xml>
                <ToUserName><![CDATA[toUser]]></ToUserName>
                <FromUserName><![CDATA[fromUser]]></FromUserName>
                <CreateTime>12345678</CreateTime>
                <MsgType><![CDATA[music]]></MsgType>
                <Music>
                <Title><![CDATA[TITLE]]></Title>
                <Description><![CDATA[DESCRIPTION]]></Description>
                <MusicUrl><![CDATA[MUSIC_Url]]></MusicUrl>
                <HQMusicUrl><![CDATA[HQ_MUSIC_Url]]></HQMusicUrl>
                <ThumbMediaId><![CDATA[media_id]]></ThumbMediaId>
                </Music>
            </xml>
            """
    NEWS = """
            <xml>
                <ToUserName><![CDATA[toUser]]></ToUserName>
                <FromUserName><![CDATA[fromUser]]></FromUserName>
                <CreateTime>12345678</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>2</ArticleCount>
                <Articles>
                <item>
                <Title><![CDATA[title1]]></Title> 
                <Description><![CDATA[description1]]></Description>
                <PicUrl><![CDATA[picurl]]></PicUrl>
                <Url><![CDATA[url]]></Url>
                </item>
                <item>
                <Title><![CDATA[title]]></Title>
                <Description><![CDATA[description]]></Description>
                <PicUrl><![CDATA[picurl]]></PicUrl>
                <Url><![CDATA[url]]></Url>
                </item>
                </Articles>
            </xml> 
            """


class MsgManager(object):
    # message manage 消息管理

    def __init__(self, wc):
        self.wc = wc

    def add_account(self, kf_account, nickname, password):
        data = {"kf_account": kf_account, "nickname": nickname, "password": password}
        return self.wc.post(ApiUrl.add_staff, data)

    def update_account(self, kf_account, nickname, password):
        data = {"kf_account": kf_account, "nickname": nickname, "password": password}
        return self.wc.post(ApiUrl.update_staff, data)

    def delete_account(self, kf_account, nickname, password):
        data = {"kf_account": kf_account, "nickname": nickname, "password": password}
        return self.wc.post(ApiUrl.delete_staff, data)

    def set_headimg(self, kf_account, headimg):
        url = ApiUrl.set_headimg % kf_account
        return self.wc.upload(url, media=headimg)

    def get_account_list(self):
        return self.wc.get(ApiUrl.get_kflist)

    def send_to_user(self, msg_type, touser, **kwargs):
        """发送消息给微信用户
        @param msgtype: 消息类型
        @param touser: 用户的opend_id
        @param kwargs: 具体的消息参数
        """
        self.validate_msgtype(msgtype)
        kf_account = kwargs.pop("kf_account", None)
        data = {"touser": touser, "msgtype": msgtype, msgtype: kwargs}
        if kf_account:
            data["customservice"] = {"kf_account": kf_account}
        return self.wc.post(ApiUrl.send_msg, data)

    def send_to_mass(self, msgtype, tousers, **kwargs):
        """批量发送消息给微信用户
        @param msgtype: 消息类型
        @param tousers: 用户的opend_id组成的list["openid1", "openid2", ...]
        @param kwargs: 具体的消息参数
        """
        self.validate_msgtype(msgtype)
        data = {"touser": tousers, "msgtype": msgtype, msgtype: kwargs}
        return self.wc.post(ApiUrl.mass_send, data)

    def send_to_group(self, msgtype, group_id, is_to_all, **kwargs):
        """发送消息给微信用户组
        @param msgtype: 消息类型
        @param group_id: 用户组ID
        @param is_to_all: 是否加入历史消息(True or False)
        @param kwargs: 具体的消息参数
        """
        self.validate_msgtype(msgtype)
        data = {"filter": {"is_to_all": is_to_all, "group_id": group_id}, "msgtype": msgtype, 
        msgtype: kwargs}
        return self.wc.post(ApiUrl.group_send, data)

    def send_to_preview(self, msgtype, touser, **kwargs):
        """消息预览接口, 每日限制100次
        @param msgtype: 消息类型
        @param touser: 用户的opend_id
        @param kwargs: 具体的消息参数
        """
        self.validate_msgtype(msgtype)
        data = {"touser": touser, "msgtype": msgtype, msgtype: kwargs}
        return self.wc.post(ApiUrl.preview_send, data)

    def get_msg_status(self, msg_id):
        """获取群发消息的状态
        @param msg_id: 群发接口返回的msg_id
        """
        return self.wc.post(ApiUrl.msg_status, {"msg_id": msg_id})

    def validate_msgtype(self, msgtype):
        if msgtype not in ("text", "image", "voice", "video", "musci", "news", "mpnews", "wxcard"):
            raise ValueError("invalid msg type: %s" % msgtype)

