# -*- coding: utf-8 -*-


try:
    import cPickle as pickle
except ImportError:
    import pickle
import os
import time


class BaseCache(object):
    # 缓存的基类

    def set(self, key, value, expire_in=None):
        return NotImplemented

    def get(self, key):
        return NotImplemented

    def delete(self, key):
        return NotImplemented


class PickleCacheData:
    # 序列化缓存数据类

    def __init__(self, key, value, expire_in=None):
        self._key = key
        self._value = value
        self._expire_in = expire_in
        self.create_time = time.time()

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        if self._expire_in is None:
            return self._value
        elif time.time() >= self.create_time + self._expire_in - 30:
            return None
        else:
            return self._value


class PickleCache(BaseCache):
    # 序列化缓存, 适用单点服务缓存，多点服务实例请使用redis、memcache等专业缓存工具

    def __init__(self, cache_dir):
        assert cache_dir is not None, "cache_dir不能为None"
        assert os.path.isdir(cache_dir), "cache_dir:%s必须是一个有效的目录" % cache_dir
        self.cache_dir = cache_dir

    def set(self, key, value, expire_in=None):
        data = PickleCacheData(key, value, expire_in)
        cache_file = os.path.join(self.cache_dir, data.key)
        with open(cache_file, "w") as f:
            pickle.dump(data, f)

    def get(self, key):
        cache_file = os.path.join(self.cache_dir, key)
        if not os.path.exists(cache_file):
            return None
        else:
            with open(cache_file) as f:
                data = pickle.load(f)
            return data.value

    def delete(self, key):
        cache_file = os.path.join(self.cache_dir, key)
        if os.path.exists(cache_file):
            os.remove(cache_file)