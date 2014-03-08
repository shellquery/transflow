# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from types import ModuleType

from flask.helpers import locked_cached_property

from .utils import make_module


class EngineModule(ModuleType):

    @locked_cached_property
    def db(self):
        from flask import current_app
        from transflow.core.sqlalchemy import SQLAlchemy
        return SQLAlchemy(current_app)

    @locked_cached_property
    def redis(self):
        from flask.ext.redis import Redis
        return Redis()

make_module(EngineModule, __name__)
