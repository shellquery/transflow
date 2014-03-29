# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from transflow.core.engines import db

from . import generators


__all__ = ['CompanyModel', 'ProjectModel',
           'MemberModel', 'StaffModel']


class CompanyModel(db.Model):
    __tablename__ = 'company'

    id = db.Column(
        'id',
        db.String(12), nullable=False,
        primary_key=True, default=generators.company)
    name = db.Column(
        'name',
        db.Unicode(256), nullable=False, index=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())

class ProjectModel(db.Model):
    __tablename__ = 'project'

    id = db.Column(
        'id',
        db.String(12), nullable=False,
        primary_key=True, default=generators.project)
    name = db.Column(
        'name',
        db.Unicode(256), nullable=False, index=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())

class MemberModel(db.Model):
    user_id = db.Column(
        'user_id',
        db.String(12), nullable=False,
        primary_key=True)
    project_id = db.Column(
        'project_id',
        db.String(12), nullable=False,
        primary_key=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())

class StaffModel(db.Model):
    user_id = db.Column(
        'user_id',
        db.String(12), nullable=False,
        primary_key=True)
    company_id = db.Column(
        'user_id',
        db.String(12), nullable=False,
        primary_key=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())
