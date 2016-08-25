#!/usr/bin/env python
#coding=utf-8
import threading
import time
 
class SafeDict(dict):

    def __init__(self, *args, **kwargs):
        self.lock = threading.Lock()

    def __getattr__(self, attrname):
        with self.lock:
            super(SafeDict, self).__getattr__(self, attrname)