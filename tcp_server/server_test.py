# coding: utf-8

import socket
from select_poll import IOLoop
from current_poll import Poll
from fd_manager import FdManager
from fd import SocketFd

if __name__ == '__main__':

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(("127.0.0.1", 8000))
	s.setblocking(False)
	s.listen(20)

	s_fd = SocketFd(s)
	fd_manager = FdManager()
	fd_manager.register(s_fd, IOLoop.READ)
	while True:
	    events = Poll.current().poll(0.1)
	    print events
	    import gevent
	    #from gevent import monkey;monkey.patch_all()
	    gevent.joinall([gevent.spawn(fd_manager.dispatch, fd, event) for fd, event in events])
	    #for fd, event in events:
		#	fd_manager.dispatch(fd, event)