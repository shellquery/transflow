# -*- coding:utf-8 -*-
from __future__ import unicode_literals

__all__ = ['MetaDict']


class MetaDict(dict):

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value
