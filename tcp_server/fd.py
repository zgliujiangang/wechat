# /usr/bin/env python
# coding: utf-8

class AbstractFd(object):
    # 描述符的抽象基类

    @property
    def fd(self):
        # 返回描述符
        raise NotImplementedError

    def read(self):
        # 当描述符可读时调用
        raise NotImplementedError

    def write(self):
        # 当描述符可写时调用
        raise NotImplementedError

    def error(self):
        # 当描述符出错时调用
        raise NotImplementedError

    def close(self):
        # 关闭该描述符
        raise NotImplementedError


class SocketFd(AbstractFd):
    # socket描述符

    def __init__(self, socket):
        self.socket = socket
    
    @property
    def fd(self):
        return self.socket.fileno()
    
    def read(self):
        # 返回连接描述符
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
    # 连接描述符

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


class FileFd(AbstractFd):
    # 文件描述符 未实现
    pass