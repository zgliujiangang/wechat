
# coding: utf-8
import select

class Poll:

    instance = None

    def __init__(self):
        self.fd_pool = dict()
        pass

    def register(self, fd, event):
        self.impl.register(fd.fd, event)
        self.fd_pool[(fd.fd, event)] = fd

    def unregister(self, fd, event):
        self.impl.unregister(fd.fd)
        self.fd_pool.pop((fd.fd, event))
        del fd

    def modify(self, fd, event):
        self.impl.unregister(fd.fd)
        self.fd_pool.pop((fd.fd, event))
        self.register(fd, event)

    def poll(self):
        events = self.impl.poll(True)
        events = [(fd_pool.get(fd), events) for fd, event in events]
        return events

    @classmethod
    def current(cls):
        pass


class PollRunner(object):

    @classmethod
    def run(cls):
        while True:
            events = Poll.current().poll()
            for fd, event in events:
                fd.handler()


class AbstractFd(object):

    @property
    def fd(self):
        raise NotImplementedError

    def handler(self, event):
        raise NotImplementedError

    def register(self, event):
        Poll.current().register(self, event)

    def modify(self, event):
        Poll.current().modify(self, event)

    def unregister(self):
        Poll.current().unregister(self)


class SocketFd(AbstractFd):

    def __init__(self, socket):
        self.socket = socket
    
    @property
    def fd(self):
        return self.socket.fileno()

    @property
    def event(self):
        return "read"

    def handler(self, event):
        if event == "read":
            self.read_handler()
        elif event == "write":
            self.write_handler()
        elif event == "error":
            self.error_handler()
    
    def read_handler(self):
        connection, address = self.socket.accept()
        connection.setblocking(False)
        connectionfd = ConnectionFd(connection)
        Poll.current().register(connectionfd)

    def close(self):
        super(SocketFd, self).close(self)
        self.socket.close()


class ConnectionFd(AbstractFd):

    def __init__(self, connection):
        self.connection = connection
        self.stream = str()
    
    @property
    def fd(self):
        return self.connection.fileno()

    @property
    def event(self):
        return "read"

    def handler(self):
        try:
            recv = self.connection.recv(1024)
        except socket.error:
            self.close()
            pass
        if recv:
            self.stream += recv
        else:
            pass

    def close(self):
        super(ConnectionFd, self).close(self)
        self.connection.close()


class FileFd(AbstractFd):
    pass
