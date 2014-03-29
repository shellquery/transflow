# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from transflow.core.engines import db
from transflow.core.decorators import classproperty

from . import generators


__all__ = ['PropertyKey', 'MetaProperties', 'extend_properties']


class PropertyKey(db.Model):
    __tablename__ = 'property_key'

    key = db.Column(
        'key',
        db.String(256), nullable=False,
        primary_key=True)
    name = db.Column(
        'name',
        db.String(256), nullable=False)
    column_type = db.Column(
        'column_type',
        db.String(64), nullable=False,
        primary_key=True)
    parameters = db.Column(
        'parameters',
        db.MutableDict.as_mutable(db.JSONType),
        nullable=False, default=dict)
    description = db.Column(
        'description',
        db.String(1024), nullable=True)

class MetaProperties(db.Model):
    __tablename__ = 'meta_properties'

    table_name = db.Column(
        'table_name',
        db.String(256), nullable=False,
        primary_key=True)
    defines = db.Column(
        'defines',
        db.MutableList.as_mutable(db.JSONType),
        nullable=False, default=list)


def extend_properties(clazz):
    table_name = clazz.__tablename__
    clazz_name = clazz.__name__
    ep_clazz_name = '%sEntityProperties' % table_name.capitalize()
    class_entities = type(
        bytes(ep_clazz_name),
        (db.Model,),
        {'__tablename__': '%s_entity_properties' % table_name,
         'id': db.Column(
            'id',
            db.String(40), nullable=False,
            primary_key=True),
         'properties': db.Column(
            'properties',
            db.MutableList.as_mutable(db.JSONType),
            nullable=False, default=list)})
    column = db.relationship(
        class_entities,
        primaryjoin='%s.id==%s.id' % (clazz_name, ep_clazz_name),
        uselist=False,
        foreign_keys='[%s.id]' % ep_clazz_name, passive_deletes='all')
    clazz.properties = column
    setattr(MetaProperties, table_name, classproperty(
        lambda cls: cls.query.get(table_name)))
    clazz.meta_properties = classproperty(
        lambda cls: getattr(MetaProperties, table_name))
    return clazz
