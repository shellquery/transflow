# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from flask import Flask

from transflow.core.session import RedisSessionInterface

from .wrappers import TransflowRequest

app = Flask(__name__)
app.request_class = TransflowRequest
app.session_interface = RedisSessionInterface()

with app.app_context():
    from transflow.core import config_loader
    config_loader.load('transflow.config')
    from . import views  # noqa
