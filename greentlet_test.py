# /usr/bin/env python
# coding: utf-8
import socket
import gevent

def connect_hanlder(connection):
    pass


def socket_accept(s):
    while True:
        try:
            connection, address = s.accept()
            connection.setblocking(False)
            while True:
                try:
                    recv = connection.recv(1024)
                    connection.send(recv)
                    connection.close()
                    break
                except socket.error:
                    print 'connection blocking'
                    gevent.sleep(0)
                except Exception:
                    connection.close()
        except socket.error:
            print 'socket blocking'
            gevent.sleep(0)
        except Exception:
            s.close()
        finally:
            print 'loop finally'


if __name__ == '__main__':

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 8000))
    s.setblocking(False)
    s.listen(20)

    gevent.joinall([gevent.spawn(socket_accept, s)for i in range(20)])

