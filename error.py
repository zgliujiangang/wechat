# coding: utf-8


class WechatError(Exception):
    pass


class ErrorHandler(object):
    err_dict = {}

    @classmethod
    def dispatch_error(cls, errcode, debug=False):
        error = cls.err_dict.get(str(errcode))
        if not debug:
            print errcode, error
        else:
            if not error:
                raise ValueError('can not find this errcode: %s' % errcode)
            else:
                raise WechatError(error)


