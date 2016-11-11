# -*- coding: utf-8 -*-


from ..urls import ApiUrl


# TODO 目前只支持客服消息接口，未支持群发接口和模板消息接口
class CustService(object):

	def __init__(self, wechat):
		self.wechat = wechat

	def add_staff(self, data):
		return self.wechat.post(ApiUrl.add_staff, data=data)

	def update_staff(self, data):
		return self.wechat.post(ApiUrl.update_staff, data=data)

	def delete_staff(self, data):
		return self.wechat.post(ApiUrl.delete_staff, data=data)

	def set_headimg(self, account, media):
		url = ApiUrl.set_headimg % account
		return self.wechat.upload(url, media=media)

	def get_kflist(self):
		return self.wechat.get(ApiUrl.get_kflist)

	def send_msg(self, data):
		return self.wechat.post(ApiUrl.send_msg, data=data)