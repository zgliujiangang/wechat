
# coding: utf-8
import select
import socket

class Poll(object):

    instance = None

    def __init__(self):
        self.fd_pool = dict()
        self.impl = _Select()

    def register(self, fd, event):
        self.impl.register(fd.fd, event)
        self.fd_pool[fd.fd] = fd

    def unregister(self, fd):
        self.impl.unregister(fd.fd)
        self.fd_pool.pop(fd.fd)

    def modify(self, fd, event):
        self.unregister(fd)
        self.register(fd, event)

    def poll(self):
        events = self.impl.poll(1)
        print events
        events = [(self.fd_pool.get(fd), event) for fd, event in events]
        return events

    @classmethod
    def current(cls):
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

class PollRunner(object):

    @classmethod
    def run(cls):
        poll = Poll.current()
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 8000))
        s.setblocking(False)
        s.listen(10)
        s_fd = SocketFd(s)
        poll.register(s_fd, IOLoop.READ)
        while True:
            events = poll.poll()
            for fd, event in events:
                fd.handler(event)


class AbstractFd(object):

    @property
    def fd(self):
        raise NotImplementedError

    def handler(self, event):
        if event == IOLoop.READ:
            self.read_handler()
        elif event == IOLoop.WRITE:
            self.write_handler()
        elif event == IOLoop.ERROR:
            self.error_handler()
        else:
            print 'happend an event:%s' % event
            self.close()

    def read_handler(self):
        raise NotImplementedError

    def write_handler(self):
        raise NotImplementedError

    def error_handler(self):
        raise NotImplementedError

    def close(self):
        Poll.current().unregister(self)


class SocketFd(AbstractFd):

    def __init__(self, socket):
        self.socket = socket
    
    @property
    def fd(self):
        return self.socket.fileno()
    
    def read_handler(self):
        connection, address = self.socket.accept()
        connection.setblocking(False)
        connection_fd = ConnectionFd(connection)
        Poll.current().register(connection_fd, IOLoop.READ)

    def write_handler(self):
        raise NotImplementedError

    def error_handler(self):
        self.close()

    def close(self):
        super(SocketFd, self).close()
        self.socket.close()

class IOLoop:
    READ = 0x001
    WRITE = 0x004
    ERROR = 0x008 | 0x010


class ConnectionFd(AbstractFd):

    def __init__(self, connection):
        self.connection = connection
        self.stream = str()
    
    @property
    def fd(self):
        return self.connection.fileno()

    def read_handler(self):
        try:
            recv = self.connection.recv(1024)
        except socket.error:
            self.close()
        else:
            if recv:
                print 'recv length:%s'% len(recv)
                self.stream += recv
                print self.stream
                self.set_write()
            else:
                print 'close connection'
                self.close()

    def set_write(self):
        if getattr(self, "has_set_write", False) == True:
            pass
        else:
            Poll.current().register(self, IOLoop.WRITE)
            self.has_set_write = True

    def write_handler(self):
        print 'aaaa'
        self.connection.send(self.stream)
        self.close()

    def close(self):
        super(ConnectionFd, self).close()
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
