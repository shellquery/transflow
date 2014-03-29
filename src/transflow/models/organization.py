# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from transflow.core.engines import db

from . import generators
from .properties import extend_properties


__all__ = ['CompanyModel', 'ProjectModel',
           'MemberModel', 'StaffModel']


@extend_properties
class CompanyModel(db.Model):
    __tablename__ = 'company'

    id = db.Column(
        'id',
        db.String(40), nullable=False,
        primary_key=True, default=generators.company)
    name = db.Column(
        'name',
        db.Unicode(256), nullable=False, index=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())

@extend_properties
class ProjectModel(db.Model):
    __tablename__ = 'project'

    id = db.Column(
        'id',
        db.String(40), nullable=False,
        primary_key=True, default=generators.project)
    name = db.Column(
        'name',
        db.Unicode(256), nullable=False, index=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())

@extend_properties
class MemberModel(db.Model):
    __tablename__ = 'member'

    id = db.Column(
        'id',
        db.String(40), nullable=False,
        primary_key=True, default=generators.member)
    user_id = db.Column(
        'user_id',
        db.String(40), nullable=False,
        index=True)
    project_id = db.Column(
        'project_id',
        db.String(40), nullable=False,
        index=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())

@extend_properties
class StaffModel(db.Model):
    __tablename__ = 'staff'

    id = db.Column(
        'id',
        db.String(40), nullable=False,
        primary_key=True, default=generators.staff)
    user_id = db.Column(
        'user_id',
        db.String(40), nullable=False,
        index=True)
    company_id = db.Column(
        'company_id',
        db.String(40), nullable=False,
        index=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())
