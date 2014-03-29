# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from functools import wraps

from flask import request, redirect, url_for


def login_required(fn):
    @wraps(fn)
    def _fn(*args, **kwargs):
        if request.user:
            return fn(*args, **kwargs)
        else:
            return redirect(url_for('account.login'))
    return _fn

class classproperty(object):

    def __init__(self, getter):
        self.getter= getter

    def __get__(self, instance, owner):
        return self.getter(owner)
