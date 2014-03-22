# -*-coding:utf-8 -*-

from __future__ import unicode_literals

import time
import pickle
from functools import wraps


def cache_for(duration):
    def deco(func):
        @wraps(func)
        def fn(*args, **kwargs):
            key = pickle.dumps((args, kwargs))
            value, expire = func.func_dict.get(key, (None, None))
            now = int(time.time())
            if value is not None and expire > now:
                return value
            value = func(*args, **kwargs)
            func.func_dict[key] = (value, int(time.time()) + duration)
            return value
        return fn
    return deco
