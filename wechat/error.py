# coding: utf-8


class WechatError(Exception):
    pass


class ErrorHandler(object):
    
    err_dict = {"40016": "不合法的按钮个数"}

    @classmethod
    def dispatch_error(cls, errcode):
        error = cls.err_dict.get(str(errcode))
        if not error:
            raise ValueError('can not find this errcode: %s' % errcode)
        else:
            raise WechatError(error)


