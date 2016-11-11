# /usr/bin/env python
# -*- coding: utf-8 -*-


from functools import wraps


def singleton(cls):
    instance_dict = {}
    @wraps(cls)
    def instance(*args, **kwargs):
        if cls not in instance_dict:
            instance_dict[cls] = cls(*args, **kwargs)
        return instance_dict[cls]
    return instance