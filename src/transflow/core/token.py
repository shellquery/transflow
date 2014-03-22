# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import base64

from transflow.core.engines import redis


class Token(object):
    prefix = 'token'
    expire = 3600

    @classmethod
    def key(cls, token_id):
        return '%s:%s' % (cls.prefix, token_id)

    @classmethod
    def set(cls, token_id, value):
        redis.setex(cls.key(token_id), cls.expire, value)

    @classmethod
    def get(cls, token_id):
        return redis.get(cls.key(token_id))


class AccessToken(Token):
    prefix = 'access-token'
    expire = 3600

    @classmethod
    def generate(cls):
        return base64.b32encode(os.urandom(20))
