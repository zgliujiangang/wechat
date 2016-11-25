# -*- coding: utf-8 -*-
# 消息管理


import time
import logging
import hashlib
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from ..utils.common import random_str
from ..urls import ApiUrl


class MsgHandler(object):
    #回复微信消息的类

    def __init__(self, wp, default="success", crypto=False):
        # crypto 是否加密[False:明文(未加密) True:密文(已加密)]
        # 当crypto为True时WechatApp实例应包含aeskey
        self.wp = wp
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
            self.msgcrypt = WXBizMsgCrypt(self.wp.token, self.wp.aeskey, self.wp.appid)
            self.response = self.cipher_response
        else:
            # 明文通讯
            self.msgcrypt = None
            self.response = self.clear_response

    def route(self, msg_type):
        # msg_type是一个二元元祖,如("event", "click")
        def wrap(func):
            self.register(msg_type, func)
            return func
        return wrap

    def register(self, msg_type, func):
        msg_type = self.convert(msg_type)
        self.register_funcs[msg_type] = func

    def clear_response(self, xml, args=None):
        # 回复微信消息,明文通讯
        xml_tree = ET.fromstring(xml)
        try:
            msg_type = xml_tree.find("MsgType").text
        except AttributeError:
            msg_type = ""
        try:
            event = xml_tree.find("Event").text
        except AttributeError:
            event = ""
        try:
            _msg_type = self.convert((msg_type, event))
            return self.register_funcs[_msg_type](xml_tree) or self.default_response(xml_tree)
        except KeyError as e:
            logging.error(str(e))
            return self.default_response(xml_tree)
        except Exception as e:
            logging.error(str(e))
            raise e

    def cipher_response(self, xml, args):
        # 回复微信消息,密文通讯
        de_ret, xml = self.msgcrypt.DecryptMsg(xml, args.get("msg_signature"), 
            args.get("timestamp"), args.get("nonce"))
        response = self.clear_response(xml, args)
        nonce = random_str(min_length=10, max_length=10)
        en_ret, response = self.msgcrypt.EncryptMsg(response, nonce)
        return response

    def default_response(self, xml_tree):
        return ReplyTemplate.TEXT % (xml_tree.find("FromUserName").text, 
            xml_tree.find("ToUserName").text, int(time.time()), self.default)

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
            return self.response(xml, args)
        else:
            # 服务器接入验证
            return self.auth(args, self.wp.token)


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
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[voice]]></MsgType>
                <Voice>
                <MediaId><![CDATA[%s]]></MediaId>
                </Voice>
            </xml>
            """

    VIDEO = """
            <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[video]]></MsgType>
                <Video>
                <MediaId><![CDATA[%s]]></MediaId>
                <Title><![CDATA[%s]]></Title>
                <Description><![CDATA[%s]]></Description>
                </Video> 
            </xml>
            """
    MUSIC = """
            <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[music]]></MsgType>
                <Music>
                <Title><![CDATA[%s]]></Title>
                <Description><![CDATA[%s]]></Description>
                <MusicUrl><![CDATA[%s]]></MusicUrl>
                <HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
                <ThumbMediaId><![CDATA[%s]]></ThumbMediaId>
                </Music>
            </xml>
            """


class MsgManager(object):
    # message manage 消息管理

    def __init__(self, wp):
        self.wp = wp

    def add_account(self, kf_account, nickname, password):
        """注意，2016年7月1日起客服功能已改版，相关接口已失效
        """
        data = {"kf_account": kf_account, "nickname": nickname, "password": password}
        return self.wp.post(ApiUrl.add_staff, data)

    def update_account(self, kf_account, nickname, password):
        data = {"kf_account": kf_account, "nickname": nickname, "password": password}
        return self.wp.post(ApiUrl.update_staff, data)

    def delete_account(self, kf_account, nickname, password):
        data = {"kf_account": kf_account, "nickname": nickname, "password": password}
        return self.wp.post(ApiUrl.delete_staff, data)

    def set_headimg(self, kf_account, headimg):
        url = ApiUrl.set_headimg % kf_account
        return self.wp.upload(url, media=headimg)

    def get_account_list(self):
        return self.wp.get(ApiUrl.get_kflist)

    def send_to_user(self, msg_type, touser, **kwargs):
        """发送消息给微信用户
        @param msgtype: 消息类型
        @param touser: 用户的open_id
        @param kwargs: 具体的消息参数
        """
        self.validate_msgtype(msgtype)
        kf_account = kwargs.pop("kf_account", None)
        data = {"touser": touser, "msgtype": msgtype, msgtype: kwargs}
        if kf_account:
            data["customservice"] = {"kf_account": kf_account}
        return self.wp.post(ApiUrl.send_msg, data)

    def send_to_mass(self, msgtype, tousers, **kwargs):
        """批量发送消息给微信用户
        @param msgtype: 消息类型
        @param tousers: 用户的open_id组成的list["openid1", "openid2", ...]
        @param kwargs: 具体的消息参数
        """
        self.validate_msgtype(msgtype)
        data = {"touser": tousers, "msgtype": msgtype, msgtype: kwargs}
        return self.wp.post(ApiUrl.mass_send, data)

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
        return self.wp.post(ApiUrl.group_send, data)

    def send_to_preview(self, msgtype, touser, **kwargs):
        """消息预览接口, 每日限制100次
        @param msgtype: 消息类型
        @param touser: 用户的open_id
        @param kwargs: 具体的消息参数
        """
        self.validate_msgtype(msgtype)
        data = {"touser": touser, "msgtype": msgtype, msgtype: kwargs}
        return self.wp.post(ApiUrl.preview_send, data)

    def get_msg_status(self, msg_id):
        """获取群发消息的状态
        @param msg_id: 群发接口返回的msg_id
        """
        return self.wp.post(ApiUrl.msg_status, {"msg_id": msg_id})

    def set_industry(self, industry_id1, industry_id2):
        """设置所属行业
        @param industry_id1: 公众号模板消息所属行业编号
        @param industry_id2: 公众号模板消息所属行业编号
        """
        return self.wp.post(ApiUrl.set_industry, {"industry_id1": industry_id1, 
            "industry_id2": industry_id2})

    def get_industry(self):
        # 获取账号设置的行业信息
        return self.wp.get(ApiUrl.get_industry)

    def add_template(self, template_id_short):
        """添加模板ID
        @param template_id_short: 模板库中模板的编号
        """
        return self.wp.post(ApiUrl.add_template, {"template_id_short": template_id_short})

    def get_all_template(self):
        # 获取账号下所有模板ID
        return self.wp.get(ApiUrl.get_template)

    def delete_template(self, template_id):
        """删除账号下的模板
        @param template_id: 模板ID
        """
        return self.wp.post(ApiUrl.delete_template, {"template_id": template_id})

    def send_template_msg(self, touser, template_id, url, template_data):
        """发送模板消息
        @param touser: 微信用户open_id
        @param template_id: 模板ID
        @param url: 超链接
        @param template_data: 渲染模板的数据
        """
        data = {"touser": touser, "template_id": template_id, "url": url, "data": template_data}
        return self.wp.post(ApiUrl.send_template_msg, data)

    def get_autoreply_info(self):
        # 获取当前公众号的自动回复规则
        return self.wp.get(ApiUrl.get_autoreply_info)

    def validate_msgtype(self, msgtype):
        if msgtype not in ("text", "image", "voice", "video", "musci", "news", "mpnews", "wxcard"):
            raise ValueError("invalid msg type: %s" % msgtype)

