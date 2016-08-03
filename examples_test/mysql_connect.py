# coding: utf-8

import logging
import traceback


logging.info("i am a test")


# mysql 日志	# 主要记录与mysql交互的信息
# redis 日志	# 主要记录与redis交互的信息
# celery 日志	# 主要记录任务执行的消息
# func 日志		# 主要接口出错的日志信息
# root 日志		# 普通日志信息 供各个模块调用



class MysqlContext(object):

	logger = logging.getLogger("mysql")

	def __init__(self, mysql):
		self.mysql = mysql
		
	def __enter__(self):
		return self.mysql

	def __exit__(self, exec_type, exec_value, traceback):
		if exec_type:
			traceback_info = traceback.format_exception(exec_type, exec_value, traceback)
			logger.error(traceback_info)
			self.mysql.rollback()
			# self.mysql.end("rollback")
		else:
			self.mysql.commit()
			# self.mysql.end()


from basic import mysql
mysql_context = MysqlContext(mysql)


from . import mysql_context

with mysql_context as mysql:
	mysql.getAll(sql, params)
	mysql.insert("hr_admin", id=1, name='111', sex=0)


def transcation(func):
	# 事务装饰器
	"""
	@transcation
	def mysql_execute():
		mysql.execute(query, params)
		return True
	"""
	@wraps(func)
	def wrap(*args, **kwargs):
		with mysql_context:
			return func(*args, **kwargs)
	return wrap