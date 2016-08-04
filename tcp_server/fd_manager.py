# /usr/bin/env python
# coding: utf-8

from select_poll import IOLoop as FdEvent
from current_poll import Poll
from fd import SocketFd
from fd import ConnectionFd
from stream_handler import stream_handler


class AbstractFdHandler(object):

	def __call__(self):
		raise NotImplementedError


class SocketFdHandler(AbstractFdHandler):

	def __call__(self, fd_manager, s_fd, s_event):
		if s_event == FdEvent.READ:
			c_fd = s_fd.read()
			fd_manager.register(c_fd, FdEvent.READ)
		elif s_event == FdEvent.WRITE:
			pass
		elif s_event == FdEvent.ERROR:
			fd_manager.unregiter(s_fd)
			s_fd.error()


class ConnectionFdHandler(AbstractFdHandler):

	def __init__(self, stream_handler=stream_handler):
		self.stream_handler = stream_handler

	def __call__(self, fd_manager, c_fd, c_event):
		if c_event == FdEvent.READ:
			c_fd.read()
			fd_manager.register(c_fd, FdEvent.WRITE)
		elif c_event == FdEvent.WRITE:
			resp_stream = self.stream_handler(c_fd.stream)
			c_fd.write(resp_stream)
			fd_manager.unregister(c_fd)
			c_fd.close()
			del c_fd
		elif c_event == FdEvent.ERROR:
			fd_manager.unregiter(c_fd)
			c_fd.error()
			del c_fd


class FdManager(object):
	# 这个类要实现对fd到来事件的调度
	# 内部维持一个 描述符池 fd_poll 从 fileno 映射到fd object
	# dispatch register unregister modify

	def __init__(self, s_handler=None, c_handler=None):
		if s_handler is None:
			s_handler = SocketFdHandler()
		if c_handler is None:
			c_handler = ConnectionFdHandler()
		self.s_handler = s_handler
		self.c_handler = c_handler
		self.fd_poll = {}

	def dispatch(self, _fd, _event):
		# 对poll返回的fd和event进行调度处理
		fd, event = self.fd_poll.get(_fd), _event
		if isinstance(fd, SocketFd):
			self.s_handler(self, fd, event)
		elif isinstance(fd, ConnectionFd):
			self.c_handler(self, fd, event)
		else:
			pass

	def register(self, fd, event):
		Poll.current().register(fd.fd, event)
		self.fd_poll[fd.fd] = fd

	def unregister(self, fd):
		Poll.current().unregister(fd.fd)
		self.fd_poll.pop(fd.fd)

	def modify(self, fd, event):
		self.unregister(fd)
		self.register(fd, event)


