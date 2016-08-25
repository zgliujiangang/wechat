# coding: utf-8
# @CopyRight

import requests

class smsServiceProxy(object):

    def __init__(self, smsService):
        self.smsService = smsService
        pass

    def send(self, mobile, msg):
        try:
            return self.smsService.send(mobile, msg)
        except Exception:
            return False


class smsService(object):

    service_url = "http://sdk2.entinfo.cn/webservice.asmx/SendSMS"

    def __init__(self, sn, pwd):
        self.sn = sn
        self.pwd = pwd

    def send(self, mobile, msg):
        params = dict(sn=self.sn, pwd=self.pwd, mobile=mobile, content=msg)
        headers = {"Content-Type": "text/xml; charset=utf-8"}
        resp = requests.get(self.service_url, params=params, headers=headers)
        return resp.text


sms_service = smsServiceProxy(smsService("SDK-SYN-010-00044", "_9a_aff1"))
test_sms_service = smsServiceProxy(smsService("SDK-SYN-010-test", "_9a_test"))


class Service:

    def __init__(self):
        raise InitException("这里不能被实例化")

    @staticmethod
    def send_sm(mobile, msg):
        # mobile 号码
        # msg 短信内容
        # return：False 发送失败 True 发送成功
        #send short message
        params = {"sn": "SDK-SYN-010-00044",
                  "pwd": "_9a_aff1",
                  "mobile": mobile,
                  "content": msg}
        headers = {"Content-Type": "text/xml; charset=utf-8"}
        resp = requests.get("http://sdk2.entinfo.cn/webservice.asmx/SendSMS",\
            params=params, headers=headers)
        return resp.text

    @staticmethod
    def send_email(mailbox, email):
        pass


class InitException(Exception):

    def __init__(self, *args, **kwargs):
        super(InitException, self).__init__(*args, **kwargs)