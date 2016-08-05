#coding: utf-8
import gevent
from gevent import monkey;monkey.patch_all()
import requests
import time
import urllib2

URL = "http://www.baidu.com/"

def request_task():
    t1 = time.time()
    [requests.get(URL) for i in range(100)]
    t2 = time.time()
    print "request task take:%s" % (t2-t1)
    return t2 - t1

def gevent_request_task():
    t1 = time.time()
    gevent.joinall([gevent.spawn(requests.get, URL) for i in range(100)])
    t2 = time.time()
    print "gevent request task take:%s" % (t2-t1)
    return t2 - t1

def urllib_task():
    t1 = time.time()
    [urllib2.urlopen(URL) for i in range(100)]
    t2 = time.time()
    print "urllib task take:%s" % (t2-t1)
    return t2 - t1

def gevent_urllib_task():
    t1 = time.time()
    gevent.joinall([gevent.spawn(urllib2.urlopen, URL) for i in range(100)])
    t2 = time.time()
    print "gevent urllib task take:%s" % (t2-t1)
    return t2 - t1


if __name__ == '__main__':
    request_task()
    gevent_request_task()
    urllib_task()
    gevent_urllib_task()