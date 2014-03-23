# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from flask import Flask

from transflow.core.session import RedisSessionInterface

from .wrappers import TransflowRequest

app = Flask(__name__)

with app.app_context():
    from transflow.core import config_loader
    config_loader.load('transflow.config')
    from transflow.core.engines import redis
    from . import views  # noqa
    from .blueprints import blueprint_www
    app.register_blueprint(blueprint_www, subdomain='www')
    app.request_class = TransflowRequest
    app.session_interface = RedisSessionInterface(redis)
