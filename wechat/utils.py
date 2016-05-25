# coding: utf-8
import hashlib
import re
import urllib

def sign(params, key):
    """
    微信签名方法
    params:待签名参数字典
    key:API秘钥
    """
    items = params.items()
    items.sort(key=lambda x: x[0])
    params_string = '&'.join(['%s=%s' % item for item in items])
    string_sign_temp = '%s&key=%s' % (params_string, key)
    md5 = hashlib.md5()
    md5.update(string_sign_temp)
    signature = md5.hexdigest().upper()
    return signature



def dict_to_xml(params):
    """
    dict转换成xml方法
    不支持嵌套xml，所有参数均在同一级
    """
    params_xml = ''.join(['<{0}>{1}</{0}>'.format(key, value) for key, value in params.items()])
    xml = '<xml>%s</xml>' % params_xml
    return xml


def xml_to_dict(xml):
    """
    xml转换成dict的方法
    不支持嵌套dict，所有参数均在同一级
    """
    re_string = '<(?P<tag>.*?)><!\[CDATA\[(?P<value>.*?)\]\]></(?P=tag)>'
    pattern = re.compile(re_string)
    result = pattern.findall(xml)
    # 有的不带CDATA
    re_string_ext = '<(?P<tag>.*?)>(?P<value>[^<|>|\[|\]]*?)</(?P=tag)>'
    pattern_ext = re.compile(re_string_ext)
    result_ext = pattern_ext.findall(xml)
    result.extend(result_ext)
    # 有的不带CDATA
    return {k: v for k, v in result}


def random_str(min_length=20, max_length=32):
    """
    随机字符串的生成方法
    不长于32位
    如果要获得一个确定长度的字符串可使min_length=max_length
    """
    length = random.randint(min_length, max_length)
    letters = string.ascii_letters
    digits = string.digits
    order_string = ''.join([letters, digits])
    sample = random.sample(order_string, length)
    return ''.join(sample)


def make_order_number():
    """
    根据当前时间和随机6位字符串生成的18位订单号
    订单号最长不超过32位
    """
    now = datetime.datetime.now().strftime('%y%m%d%H%M%S')
    serial = ''.join(random.sample(''.join([string.ascii_letters, string.digits]), 6))
    return '%s%s' % (now, serial)

def with_metaclass(meta, *bases):
    
    class metaclass(type):
        def __new__(cls, clsname, this_bases, d):
            return meta(clsname, bases, d)

    return type.__new__(metaclass, "templory_class", (), {})


def wechat_dumps(data):
    pass