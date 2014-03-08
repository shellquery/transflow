# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from transflow.core.engines import db
from . import generators


__all__ = ['UserModel']


class UserModel(db.Model):
    __tablename__ = 'account'

    id = db.Column('id', db.String(12), nullable=False,
                   primary_key=True, default=generators.user)
    email = db.Column('email', db.String(256), nullable=False,
                      unique=True, index=True)
    realname = db.Column('realname', db.Unicode(128), nullable=False,
                         index=True)
    unikey = db.Column('unikey', db.String(256), nullable=False,
                       index=True)
    date_created = db.Column('date_created', db.DateTime(timezone=True),
                             server_default=db.func.current_timestamp())
