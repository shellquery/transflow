# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import current_app as app
from sqlalchemy.ext.hybrid import hybrid_property

from transflow.core.engines import db
from transflow.core.db import CaseInsensitiveComparator

from . import generators
from .properties import extend_properties


__all__ = ['UserModel', 'EmailTempModel']

@extend_properties
class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(
        'id',
        db.String(40), nullable=False,
        primary_key=True, default=generators.user)
    email = db.Column(
        'email',
        db.String(256), nullable=False, unique=True, index=True)
    realname = db.Column(
        'realname',
        db.Unicode(128), nullable=False, index=True)
    introduction = db.Column(
        'introduction',
        db.Unicode(1024), nullable=True)
    password_hash = db.Column(
        'password_hash', db.CHAR(40), nullable=False)
    gender = db.Column(
        'gender',
        db.Enum('male', 'femail', 'unknown',
                name='user_gender_enum'))
    avatar = db.Column(
        'avatar',
        db.String(1024), nullable=False,
        default=app.config['DEFAULT_USER_AVATAR'])
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())
    date_last_signed_in = db.Column(
        'date_last_signed_in',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())

    @hybrid_property
    def email_insensitive(self):
        return self.email.lower()

    @email_insensitive.comparator
    def email_insensitive_comparator(cls):
        return CaseInsensitiveComparator(cls.email)

    def as_dict(self):
        return dict(
            realname=self.realname,
            email=self.email,
            introduction=self.introduction,
            gender=self.gender,
            avatar=self.avatar,
            date_created=self.date_created)


class EmailTempModel(db.Model):
    id = db.Column('id', db.String(40), nullable=False,
                   primary_key=True, default=generators.email_temp)
    email = db.Column('email', db.String(256), nullable=False,
                      unique=True, index=True)
    random_code = db.Column('random_code', db.String(64), nullable=False)
    date_created = db.Column('date_created',
                             db.DateTime(timezone=True),
                             server_default=db.func.current_timestamp(),
                             nullable=False,
                             index=True)

    @hybrid_property
    def email_insensitive(self):
        return self.email.lower()

    @email_insensitive.comparator
    def email_insensitive_comparator(cls):
        return CaseInsensitiveComparator(cls.email)
