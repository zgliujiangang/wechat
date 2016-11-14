# -*- coding: utf-8 -*-


try:
    import cPickle as pickle
except ImportError:
    import pickle
import os
import time


class CacheData:
    "用于序列化存入文件的cache类，适用单点服务缓存，多点服务实例请使用redis、memcache等专业缓存工具"

    def __init__(self, key, value, expire_in):
        self._key = key
        self._value = value
        self._expire_in = expire_in - 30
        self.create_time = time.time()

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        if time.time() >= self.create_time + self._expire_in:
            return None
        else:
            return self._value


def set(cache_dir, key, value, expire_in):
    data = CacheData(key, value, expire_in)
    cache_file = os.path.join(cache_dir, data.key)
    with open(cache_file, "w") as f:
        pickle.dump(data, f)


def get(cache_dir, key):
    cache_file = os.path.join(cache_dir, key)
    if not os.path.exists(cache_file):
        return None
    else:
        with open(cache_file) as f:
            data = pickle.load(f)
        return data.value