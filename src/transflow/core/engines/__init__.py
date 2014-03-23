# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from types import ModuleType

from flask.helpers import locked_cached_property

from transflow.core.utils import make_module


class EngineModule(ModuleType):

    @locked_cached_property
    def db(self):
        from flask import current_app
        from transflow.core._sqlalchemy import SQLAlchemy
        return SQLAlchemy(current_app)

    @locked_cached_property
    def redis(self):
        from flask import current_app
        from flask.ext.redis import Redis
        return Redis(current_app)

    @locked_cached_property
    def mail(self):
        from flask.ext.mail import Mail
        return Mail()

    @locked_cached_property
    def rq(self):
        from flask.ext.rq import RQ
        from flask import current_app
        return RQ(current_app)

make_module(EngineModule, __name__)
