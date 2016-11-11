# -*- coding: utf-8 -*-


from ..urls import ApiUrl


class UserManager(object):

	def __init__(self, wechat):
		self.wechat = wechat
	
	def create_group(self, data):
		return self.wechat.post(ApiUrl.create_group, data=data)
	
	def get_groups(self):
		return self.wechat.get(ApiUrl.get_groups)

	def get_id(self, data):
		return self.wechat.post(ApiUrl.get_id, data=data)

	def update_group(self, data):
		return self.wechat.post(ApiUrl.update_group, data=data)

	def to_group(self, data):
		return self.wechat.post(ApiUrl.to_group, data=data)

	def batch_to_group(self, data):
		return self.wechat.post(ApiUrl.batch_to_group, data=data)

	def delete_group(self, data):
		return self.wechat.post(ApiUrl.delete_group, data=data)

	def set_remark(self, data):
		return self.wechat.post(ApiUrl.update_remark, data=data)

	def get_userinfo(self, openid):
		url = ApiUrl.get_userinfo % openid
		return self.wechat.get(url)

	def batch_get_userinfo(self, data):
		return self.wechat.post(ApiUrl.batch_get_userinfo, data=data)

	def get_userlist(self, next_openid=""):
		url = ApiUrl.get_userlist % next_openid
		return self.wechat.get(url)
