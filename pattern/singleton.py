# coding: utf-8


def singleton(cls):
	instance_dict = {}
	def wrap(*args, **kwargs):
		if cls not in instance_dict:
			instance = cls(*args, **kwargs)
			instance_dict[cls] = instance
		return instance_dict[cls]
	return wrap