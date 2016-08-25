# coding: utf-8

import gevent
from gevent import monkey;monkey.patch_all()
import urllib2
import time

def fetch():
    #print 'fetch start'
    response = urllib2.urlopen("http://127.0.0.1:8000/")
    #result = response.read()
    #print result
    #print 'fetch end'


def asyncfetch():
    gevent.joinall([gevent.spawn(fetch) for i in range(10000)])


if __name__ == '__main__':
    t1 = time.time()
    asyncfetch()
    t2 = time.time()
    print t2 - t1


