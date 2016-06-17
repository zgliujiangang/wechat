# coding: utf-8
# 接收消息和被动回复消息
import hashlib
from ..utils import xml_to_dict, random_str
from ..WXBizMsgCrypt import WXBizMsgCrypt


class Reply(object):
    #回复微信消息的类

    def __init__(self, wechat, default="success", mode=False):
        # mode 加密模式->False:明文；True:密文
        self.wechat = wechat
        self.default = default
        self.mode = mode
        self.register_funcs = dict()
        if mode:
            self.msgcrypt = WXBizMsgCrypt(wechat.conf.token, wechat.conf.aeskey, wechat.conf.appid)

    def route(self, msg_type):
        # msg_type是一个二元元祖,如("event", "click")
        def wrap(func):
            self.register(msg_type, func)
        return wrap

    def register(self, msg_type, func):
        msg_type = self.convert(msg_type)
        self.register_funcs[msg_type] = func

    def response(self, msg_type, *args, **kwargs):
        # 回复微信消息
        try:
            msg_type = self.convert(msg_type)
            return self.register_funcs[msg_type](*args, **kwargs) or self.default
        except Exception as e:
            print e
            return self.default

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
                print "服务器接入验证时签名不匹配"
                return "FAIL"
        except Exception as e:
            print e
            return "FAIL"

    def clear(self, xml):
        # 明文模式
        params = xml_to_dict(xml)
        response = self.response((params.get("MsgType"), params.get("Event", "")), params)
        return response

    def cipher(self, xml, args):
        # 密文模式
        de_ret, xml = self.msgcrypt.DecryptMsg(xml, args.get("msg_signature"), 
            args.get("timestamp"), args.get("nonce"))
        response = self.clear(xml)
        if response != self.default:
            # 回复的消息不是默认消息时才进行加密
            nonce = random_str(min_length=10, max_length=10)
            en_ret, response = self.msgcrypt.EncryptMsg(response, nonce)
        else:
            pass
        return response

    def __call__(self, data=None, args=None, auth=False):
        #param data:post消息体中的字符串
        #param args:url上携带的参数字典
        if not auth:
            if self.mode:
                response = self.cipher(data, args)
            else:
                response = self.clear(data)
            return response
        else:
            # 服务器接入验证 仅支持data以字典形式传入
            return self.auth(args, self.wechat.conf.token)


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