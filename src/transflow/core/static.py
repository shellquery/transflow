# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import url_for

__all__ = ['static_for']


def static_for(filename):
    return url_for('static', filename=filename)
