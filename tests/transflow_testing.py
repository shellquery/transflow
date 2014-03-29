# -*- coding: utf-8 -*
from __future__ import unicode_literals

import os
import unittest

from flask.ext.testing import TestCase as _TestCase

from transflow import app
from transflow.core.engines import db


class TestCase(_TestCase):

    db_path = '/tmp/transflow.db'
    SQL_ALCHEMY_DATABASE_URI = 'sqlite:///%s' % db_path
    TESTING = True
    WTF_CSRF_ENABLED = False

    def create_app(self):
        try:
            os.unlink(self.db_path)
        except OSError:
            pass
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.unlink(self.db_path)
