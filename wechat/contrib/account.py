# coding: utf-8
from urllib import quote
from ..urls import ApiUrl
class AccountManager(object):

	def __init__(self , wechat):
		self.wechat = wechat

	def create_qrcode(self, data):
		return self.wechat.post(ApiUrl.create_qrcode, data=data)

	def download_qrcode(self, ticket):
		url = ApiUrl.download_qrcode % quote(ticket)
		return self.wechat.download(url)

	def get_shorturl(self, data):
		return self.wechat.post(ApiUrl.get_shorturl, data=data)
