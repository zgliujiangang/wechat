# coding: utf-8

from select_poll import _Select

class Poll:

	instance = None

	@classmethod
	def current(cls):
		if cls.instance is None:
			cls.instance = _Select()
		return cls.instance