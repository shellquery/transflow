# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import types

from flask import g

from transflow.models import UserModel

from .datastructures import MetaDict

__all__ = ['user_meta_notexists', 'preload_user_meta', 'user_meta']


def _user_meta_table():
    if not hasattr(g, '_user_meta_table'):
        g._user_meta_table = {}
    return g._user_meta_table


user_meta_notexists = MetaDict(
    id='0' * 12,
    is_exists=False,
    realname='已注销',
    email='',
    gender='unknown',
    unikey='',
    introduction='已注销')


def preload_user_meta(users, user_id_key='user_id'):
    if isinstance(users, (list, set, tuple)):
        users = list(users)
    elif isinstance(users, types.GeneratorType):
        users = [u for u in users]
    else:
        users = [users]
    user_ids = set()
    for user in users:
        if isinstance(user, basestring):
            user_ids.add(user)
        elif hasattr(user, user_id_key):
            user_id = getattr(user, user_id_key, None)
            if user_id:
                user_ids.add(user_id)
        elif isinstance(user, dict):
            user_id = user.get(user_id_key)
            if user_id:
                user_ids.add(user_id)
    table = _user_meta_table()
    user_ids = user_ids - set(table.keys())
    users = UserModel.query.batch_get(*user_ids)
    for user_id, user in zip(user_ids, users):
        if not user:
            table[user_id] = user_meta_notexists
        else:
            table[user_id] = MetaDict(user.as_dict())


def user_meta(user_id):
    table = _user_meta_table()
    if user_id not in table:
        preload_user_meta(user_id)
    return table[user_id]
