# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from transflow.core.engines import db

from . import generators


__all__ = ['TaskModel', 'CrossModel',
           'TaskOutCrossModel', 'CrossInTaskModel']


class TaskModel(db.Model):
    __tablename__ = 'task'

    id = db.Column(
        'id',
        db.String(12), nullable=False,
        primary_key=True, default=generators.task)
    is_start = db.Column(
        'is_start',
        db.Boolean(), nullable=False,
        server_default='false')
    is_end = db.Column(
        'is_start',
        db.Boolean(), nullable=False,
        server_default='false')
    is_ready = db.Column(
        'is_ready',
        db.Boolean(), nullable=False,
        server_default='false')
    is_finished = db.Column(
        'is_finished',
        db.Boolean(), nullable=False,
        server_default='false')
    progress = db.Column(
        'progress',
        db.Integer(), nullable=False,
        server_default='0')
    user_id = db.Column(
        'user_id',
        db.String(12), nullable=False)
    project_id = db.Column(
        'project_id',
        db.String(12), nullable=False,
        primary_key=True)
    name = db.Column(
        'name',
        db.Unicode(256), nullable=False)
    description = db.Column(
        'description',
        db.Unicode(256), nullable=True)
    date_start = db.Column(
        'date_start',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())
    date_end = db.Column(
        'date_end',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())


class CrossModel(db.Model):
    __tablename__ = 'cross'

    id = db.Column(
        'id',
        db.String(12), nullable=False,
        primary_key=True, default=generators.cross)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())


class CrossStorageModel(db.Model):
    __tablename__ = 'cross_storage'

    cross_id = db.Column(
        'cross_id',
        db.String(12), nullable=False,
        primary_key=True)
    document_id = db.Column(
        'document_id',
        db.String(12), nullable=False,
        primary_key=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())


class DocumentModel(db.Model):
    __tablename__ = 'document'

    id = db.Column(
        'id',
        db.String(12), nullable=False,
        primary_key=True, default=generators.document)
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
        db.String(12), nullable=False,
        primary_key=True)
    cross_id = db.Column(
        'cross_id',
        db.String(12), nullable=False,
        primary_key=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())


class CrossInTaskModel(db.Model):
    __tablename__ = 'cross_in_task'

    cross_id = db.Column(
        'cross_id',
        db.String(12), nullable=False,
        primary_key=True)
    task_id = db.Column(
        'task_id',
        db.String(12), nullable=False,
        primary_key=True)
    date_created = db.Column(
        'date_created',
        db.DateTime(timezone=True),
        server_default=db.func.current_timestamp())
