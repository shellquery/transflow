# -*- coding: utf-8 -*-

from __future__ import unicode_literals

__all__ = ['pad_left']

def pad_left(s, c='0', bits=12):
    if len(s) >= bits:
        return s
    return '0' * (bits - len(s)) + s
