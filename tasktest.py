# coding: utf-8
import sys
sys.path.append('.')


from wechat.mycelery import async_task
from wechat.sms import sms_service


if __name__ == '__main__':
    mobile = '18268174851'
    msg = '你好！'
    async_task.delay(sms_service.send, [sms_service, mobile, msg])