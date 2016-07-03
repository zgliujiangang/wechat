# coding: utf-8
import logging
import hashlib
from .utils import xml_to_dict

class PayCallback(object):

	return_template = '<xml><return_code>%s</return_code><return_msg>%s</return_msg></xml>'
	code_success = "SUCCESS"
	code_fail = "FAIL"

	def __init__(self, conf):
		self.conf = conf

	def dispose(self, xml):
		# 第一步判断通信标识
		# xml是微信返回的xml字符串
		params = xml_to_dict(xml)
		if params.get("return_code") == "SUCCESS":
			# 交给下一步处理程序
			return self.success_return_code(params)
		else:
			# 交给错误处理程序
			return self.error_return_code(params)

	def success_return_code(self, params):
		# 第二步验签
		signature = params.pop('sign')
		_signature = self.sign(params)
		if signature == _signature:
			# 验签成功
			return self.success_signature(params)
		else:
			# 验签失败
			return self.error_signature(params)

	def success_signature(self, params):
		# 第三步判断支付结果
		if params.get("result_code") == "SUCCESS":
			return self.success_result_code(params)
		else:
			return self.error_result_code(params)

	# ---------------以下通过继承改写--------------
	def error_return_code(self, params):
		# return_code为fail时的处理方法
		# logging.info(params.get("return_msg"))
		return self.return_template % (self.code_fail, "通信错误")

	def error_signature(self, params):
		# 签名signature错误时调用的方法
		# logging.info(params)
		return self.return_template % (self.code_fail, "验签失败")

	def error_result_code(self, params):
		# 交易失败时的处理方法
		# logging.info(params)
		return self.return_template % (self.code_success, "OK")

	def success_result_code(self, params):
		# 交易成功时的处理方法
		return self.return_template % (self.code_success, "OK")
	# ---------------以上通过继承改写--------------

	def sign(self, params):
		# 签名
		items = params.items()
		items.sort(key=lambda x: x[0])
		params_string = '&'.join(['%s=%s' % item for item in items])
		string_sign_temp = '%s&key=%s' % (params_string, self.conf.pay_sign_key)
		md5 = hashlib.md5()
		md5.update(string_sign_temp)
		signature = md5.hexdigest().upper()
		return signature