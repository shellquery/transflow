# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from flask import Flask

app = Flask(__name__)


with app.app_context():
    from transflow.models import UserModel
    print UserModel.query.all()
