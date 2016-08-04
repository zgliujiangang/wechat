
# coding: utf-8
import select
import socket

class IOLoop:
    READ = 0x001
    WRITE = 0x004
    ERROR = 0x008 | 0x010


class Poll(object):

    instance = None

    @classmethod
    def current(cls):
        if cls.instance is None:
            cls.instance = _Select()
        return cls.instance

class FdManager(object):

    def __init__(self, conn_handler=None):
        self.fd_pool = {}
        self.conn_handler = conn_handler

    def handler(self, _fd, _event):
        fd = self.fd_pool.get(_fd)
        event = _event
        if isinstance(fd, SocketFd):
            if event == IOLoop.READ:
                conn_fd = fd.read()
                self.register(conn_fd, IOLoop.READ)
            elif event == IOLoop.WRITE:
                fd.write()
            elif event == IOLoop.ERROR:
                self.unregister(fd)
                fd.error()
                del fd
        elif isinstance(fd, ConnectionFd):
            if event == IOLoop.READ:
                stream = fd.read()
                self.register(fd, IOLoop.WRITE)
            elif event == IOLoop.WRITE:
                if fd.stream and self.conn_handler:
                    stream = self.conn_handler(fd.stream)
                    fd.write(stream)
                else:
                    fd.write("<html><body><p>yes you can do it</p></body></html>")
                self.unregister(fd)
                fd.close()
                del fd
            elif event == IOLoop.ERROR:
                self.unregister(fd)
                fd.error()
                del fd
        else:
            raise ValueError(_fd)

    def register(self, fd, event):
        Poll.current().register(fd.fd, event)
        self.fd_pool[fd.fd] = fd

    def unregister(self, fd):
        Poll.current().unregister(fd.fd)
        self.fd_pool.pop(fd.fd)

    def modify(self, fd, event):
        self.unregister(fd)
        self.register(fd, event)

    def poll(self):
        return Poll.current().poll(0.01)


class PollRunner(object):

    @classmethod
    def run(cls):
        def application(stream):
            return stream
        fd_manager = FdManager(conn_handler=application)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 8000))
        s.setblocking(False)
        s.listen(10)
        s_fd = SocketFd(s)
        fd_manager.register(s_fd, IOLoop.READ)
        while True:
            events = fd_manager.poll()
            print events
            for fd, event in events:
                fd_manager.handler(fd, event)


class AbstractFd(object):

    @property
    def fd(self):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError

    def error(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class SocketFd(AbstractFd):

    def __init__(self, socket):
        self.socket = socket
    
    @property
    def fd(self):
        return self.socket.fileno()
    
    def read(self):
        connection, address = self.socket.accept()
        connection.setblocking(False)
        connection_fd = ConnectionFd(connection)
        return connection_fd

    def write(self):
        raise NotImplementedError

    def error(self):
        print 'happend an error:%s' % self.fd
        self.close()

    def close(self):
        self.socket.close()


class ConnectionFd(AbstractFd):

    def __init__(self, connection):
        self.connection = connection
        self.stream = None
    
    @property
    def fd(self):
        return self.connection.fileno()

    def read(self):
        try:
            recv = self.connection.recv(1024)
            self.stream = recv
            return recv
        except socket.error:
            return None
        finally:
            return None

    def write(self, stream):
        self.connection.send(stream)

    def error(self):
        print 'happend an error:%s' % self.fd
        self.close()

    def close(self):
        self.connection.close()


class _Select(object):
    """A simple, select()-based IOLoop implementation for non-Linux systems"""
    def __init__(self):
        self.read_fds = set()
        self.write_fds = set()
        self.error_fds = set()
        self.fd_sets = (self.read_fds, self.write_fds, self.error_fds)

    def close(self):
        pass

    def register(self, fd, events):
        if events & IOLoop.READ and fd not in self.read_fds:
            self.read_fds.add(fd)
        if events & IOLoop.WRITE and fd not in self.write_fds:
            self.write_fds.add(fd)
        if events & IOLoop.ERROR and fd not in self.error_fds:
            self.error_fds.add(fd)
            # Closed connections are reported as errors by epoll and kqueue,
            # but as zero-byte reads by select, so when errors are requested
            # we need to listen for both read and error.
            # self.read_fds.add(fd)

    def modify(self, fd, events):
        self.unregister(fd)
        self.register(fd, events)

    def unregister(self, fd):
        self.read_fds.discard(fd)
        self.write_fds.discard(fd)
        self.error_fds.discard(fd)

    def poll(self, timeout):
        readable, writeable, errors = select.select(
            self.read_fds, self.write_fds, self.error_fds, timeout)
        events = {}
        for fd in readable:
            events[fd] = events.get(fd, 0) | IOLoop.READ
        for fd in writeable:
            events[fd] = events.get(fd, 0) | IOLoop.WRITE
        for fd in errors:
            events[fd] = events.get(fd, 0) | IOLoop.ERROR
        return events.items()



if __name__ == '__main__':
    PollRunner.run()
