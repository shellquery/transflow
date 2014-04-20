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
    admin_user_id = db.Column(
        'admin_user_id',
        db.String(40), nullable=False,
        index=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())
    staffs_count = db.Column(
        'staffs_count',
        db.Integer(), nullable=False,
        default=0, server_default='0')
    projects_count = db.Column(
        'projects_count',
        db.Integer(), nullable=False,
        default=0, server_default='0')

    staffs = db.relationship(
        'StaffModel',
        backref=db.backref('company', lazy='joined', innerjoin=True),
        primaryjoin='StaffModel.company_id==CompanyModel.id',
        foreign_keys='[StaffModel.company_id]',
        passive_deletes='all',
        lazy='dynamic')

    projects = db.relationship(
        'ProjectModel',
        backref=db.backref('company', lazy='joined', innerjoin=True),
        primaryjoin='ProjectModel.company_id==CompanyModel.id',
        foreign_keys='[ProjectModel.company_id]',
        passive_deletes='all',
        lazy='dynamic')


@extend_properties
class ProjectModel(db.Model):
    __tablename__ = 'project'

    id = db.Column(
        'id',
        db.String(40), nullable=False,
        primary_key=True, default=generators.project)
    company_id = db.Column(
        'company_id',
        db.String(40), nullable=False,
        index=True)
    manage_user_id = db.Column(
        'manage_user_id',
        db.String(40), nullable=False,
        index=True)
    name = db.Column(
        'name',
        db.Unicode(256), nullable=False, index=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())
    members_count = db.Column(
        'members_count',
        db.Integer(), nullable=False,
        default=0, server_default='0')
    tasks_count = db.Column(
        'tasks_count',
        db.Integer(), nullable=False,
        default=0, server_default='0')
    crosses_count = db.Column(
        'crosses_count',
        db.Integer(), nullable=False,
        default=0, server_default='0')
    documents_count = db.Column(
        'documents_count',
        db.Integer(), nullable=False,
        default=0, server_default='0')

    members = db.relationship(
        'MemberModel',
        backref=db.backref('project', lazy='joined', innerjoin=True),
        primaryjoin='MemberModel.project_id==ProjectModel.id',
        foreign_keys='[MemberModel.project_id]',
        passive_deletes='all',
        lazy='dynamic')

    documents = db.relationship(
        'DocumentModel',
        backref=db.backref('project', lazy='joined', innerjoin=True),
        primaryjoin='DocumentModel.project_id==ProjectModel.id',
        foreign_keys='[DocumentModel.project_id]',
        passive_deletes='all',
        lazy='dynamic')

    crosses = db.relationship(
        'CrossModel',
        backref=db.backref('project', lazy='joined', innerjoin=True),
        primaryjoin='CrossModel.project_id==ProjectModel.id',
        foreign_keys='[CrossModel.project_id]',
        passive_deletes='all',
        lazy='dynamic')

    cross_start = db.relationship(
        'CrossModel',
        primaryjoin=('and_(CrossModel.project_id==ProjectModel.id, '
                     'CrossModel.is_start)'),
        foreign_keys='[CrossModel.project_id]',
        passive_deletes='all',
        uselist=False,
        lazy='joined')

    cross_end = db.relationship(
        'CrossModel',
        primaryjoin=('and_(CrossModel.project_id==ProjectModel.id, '
                     'CrossModel.is_end)'),
        foreign_keys='[CrossModel.project_id]',
        passive_deletes='all',
        uselist=False,
        lazy='joined')

    tasks = db.relationship(
        'TaskModel',
        backref=db.backref('project', lazy='joined', innerjoin=True),
        primaryjoin='TaskModel.project_id==ProjectModel.id',
        foreign_keys='[TaskModel.project_id]',
        passive_deletes='all',
        lazy='dynamic')


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
