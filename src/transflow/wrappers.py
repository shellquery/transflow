# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Flask

from flask.helpers import locked_cached_property
from flask.wrappers import Request

from transflow.core.session import RedisSessionInterface
from transflow.core.static import static_for
from transflow.core.engines import redis, mail
from transflow.core.converters import addition_converters


class TransflowRequest(Request):

    @locked_cached_property
    def user_id(self):
        return self.user.get('id')

    @locked_cached_property
    def user(self):
        from transflow.core.users import user_meta
        from transflow.core.tokens import AccessToken
        user_id = self.cookies.get('transflow_user_id')
        access_token = self.cookies.get('transflow_access_token')
        if not user_id or not access_token:
            return {}
        if user_id != AccessToken.get(access_token):
            return {}
        user = user_meta(user_id)
        return user


class TransflowFlask(Flask):
    request_class = TransflowRequest
    session_interface = RedisSessionInterface(redis)

    def __init__(self, *args, **kwargs):
        super(TransflowFlask, self).__init__(*args, **kwargs)
        funcs = dict(static_for=static_for)
        self.jinja_env.globals.update(funcs)
        self.url_map.converters.update(addition_converters)

    def init(self):
        redis.init_app(self)
        mail.init_app(self)
