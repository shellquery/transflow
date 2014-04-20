# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from wtforms import fields
from wtforms.validators import Optional, Required

from .validators import Tkey, Unikey, PinyinLength

__all__ = ['tkey', 'unikey', 'pinyin']


def tkey(required=True):
    _validators = []
    if required:
        _validators.append(Required())
    else:
        _validators.append(Optional())
    _validators.append(Tkey())
    return fields.StringField(validators=_validators)


def unikey(required=True):
    _validators = []
    if required:
        _validators.append(Required())
    else:
        _validators.append(Optional())
    _validators.append(Unikey())
    return fields.StringField(validators=_validators)


def pinyin(required=True, min=-1, max=-1):
    _validators = []
    if required:
        _validators.append(Required())
    else:
        _validators.append(Optional())
    _validators.append(PinyinLength(min=min, max=max))
    return fields.StringField(validators=_validators)
