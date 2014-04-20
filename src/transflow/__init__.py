# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from .wrappers import TransflowFlask

app = TransflowFlask(__name__)
app.static_folder = 'static'

with app.app_context():
    from transflow.core import config_loader
    config_loader.load('transflow.config')
    from . import views  # noqa
    from .blueprints import blueprint_www
    app.register_blueprint(blueprint_www, subdomain='www')
