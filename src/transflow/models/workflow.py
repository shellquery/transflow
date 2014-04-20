# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from transflow.core.engines import db

from . import generators
from .properties import extend_properties


__all__ = ['TaskModel', 'CrossModel', 'DocumentModel',
           'CrossDocumentModel', 'TaskOutCrossModel',
           'CrossInTaskModel']


@extend_properties
class TaskModel(db.Model):
    __tablename__ = 'task'

    id = db.Column(
        'id',
        db.String(40), nullable=False,
        primary_key=True, default=generators.task)
    user_id = db.Column(
        'user_id',
        db.String(40), nullable=False)
    project_id = db.Column(
        'project_id',
        db.String(40), nullable=False)
    name = db.Column(
        'name',
        db.Unicode(256), nullable=False)
    description = db.Column(
        'description',
        db.Unicode(256), nullable=True,
        server_default='')
    is_ready = db.Column(
        'is_ready',
        db.Boolean(), nullable=False,
        default=False,
        server_default='false')
    is_finished = db.Column(
        'is_finished',
        db.Boolean(), nullable=False,
        default=False,
        server_default='false')
    progress = db.Column(
        'progress',
        db.Integer(), nullable=False,
        server_default='0')
    date_start = db.Column(
        'date_start',
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.current_timestamp())
    date_end = db.Column(
        'date_end',
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.current_timestamp())
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        nullable=False,
        server_default=db.func.current_timestamp())

    @classmethod
    def __declare_last__(cls):
        cls.down_crosses = db.relationship(
            'CrossModel',
            secondary=TaskOutCrossModel.__table__,
            backref=db.backref(
                'up_tasks',
                innerjoin=True,
                order_by=TaskOutCrossModel.date_created,
                lazy='subquery'),
            primaryjoin=TaskModel.id == TaskOutCrossModel.task_id,
            secondaryjoin=TaskOutCrossModel.cross_id == CrossModel.id,
            order_by=TaskOutCrossModel.date_created,
            foreign_keys=[TaskOutCrossModel.task_id,
                          TaskOutCrossModel.cross_id],
            passive_deletes='all', lazy='subquery')


class CrossModel(db.Model):
    __tablename__ = 'cross'

    id = db.Column(
        'id',
        db.String(40), nullable=False,
        primary_key=True, default=generators.cross)
    project_id = db.Column(
        'project_id',
        db.String(40), nullable=False,
        index=True)
    is_start = db.Column(
        'is_start',
        db.Boolean(), nullable=False,
        server_default='false')
    is_end = db.Column(
        'is_end',
        db.Boolean(), nullable=False,
        server_default='false')
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())

    @classmethod
    def __declare_last__(cls):
        cls.documents = db.relationship(
            'DocumentModel',
            secondary=CrossDocumentModel.__table__,
            backref=db.backref(
                'crosses',
                innerjoin=True,
                order_by=CrossDocumentModel.date_created.desc(),
                lazy='dynamic'),
            primaryjoin=CrossModel.id == CrossDocumentModel.cross_id,
            secondaryjoin=CrossDocumentModel.document_id == DocumentModel.id,
            order_by=CrossDocumentModel.date_created.desc(),
            foreign_keys=[CrossDocumentModel.cross_id,
                          CrossDocumentModel.document_id],
            passive_deletes='all', lazy='dynamic')

        cls.down_tasks = db.relationship(
            'TaskModel',
            secondary=CrossInTaskModel.__table__,
            backref=db.backref(
                'up_cross',
                innerjoin=True,
                uselist=False),
            primaryjoin=CrossModel.id == CrossInTaskModel.cross_id,
            secondaryjoin=CrossInTaskModel.task_id == TaskModel.id,
            order_by=CrossInTaskModel.date_created,
            foreign_keys=[CrossInTaskModel.cross_id,
                          CrossInTaskModel.task_id],
            passive_deletes='all', lazy='subquery')


class CrossDocumentModel(db.Model):
    __tablename__ = 'cross_document'

    cross_id = db.Column(
        'cross_id',
        db.String(40), nullable=False,
        primary_key=True)
    document_id = db.Column(
        'document_id',
        db.String(40), nullable=False,
        primary_key=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())


class DocumentModel(db.Model):
    __tablename__ = 'document'

    id = db.Column(
        'id',
        db.String(40), nullable=False,
        primary_key=True, default=generators.document)
    project_id = db.Column(
        'project_id',
        db.String(40), nullable=False,
        index=True)
    name = db.Column(
        'name',
        db.Unicode(256), nullable=False)
    url = db.Column(
        'url',
        db.Unicode(1024), nullable=False)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())


class TaskOutCrossModel(db.Model):
    __tablename__ = 'task_out_cross'

    task_id = db.Column(
        'task_id',
        db.String(40), nullable=False,
        primary_key=True)
    cross_id = db.Column(
        'cross_id',
        db.String(40), nullable=False,
        primary_key=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())


class CrossInTaskModel(db.Model):
    __tablename__ = 'cross_in_task'

    cross_id = db.Column(
        'cross_id',
        db.String(40), nullable=False,
        primary_key=True)
    task_id = db.Column(
        'task_id',
        db.String(40), nullable=False,
        primary_key=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())
