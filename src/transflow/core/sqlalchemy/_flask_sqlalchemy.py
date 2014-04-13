# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import random
import contextlib
import threading

from functools import partial

from flask import g, request
from flask.helpers import locked_cached_property
from sqlalchemy import orm, sql, types, exc
from sqlalchemy.util import OrderedDict, to_list
from sqlalchemy.orm import attributes, loading
from sqlalchemy.ext.compiler import compiles
from flask.ext.sqlalchemy import (SQLAlchemy, _SignallingSession,
                                  _EngineConnector, get_state, BaseQuery)
from flask.ext import sqlalchemy as flask_sqlalchemy


from . import types as custom_types
from . import mutable as custom_mutable
from . import hybrid as custom_hybrid

__all__ = ['SQLAlchemy']


class SQLAlchemyMixin(object):

    def __init__(self, *args, **kwargs):
        super(SQLAlchemyMixin, self).__init__(*args, **kwargs)
        self.current_user_id = current_user_id
        self.set_current_user_id = set_current_user_id
        for module in custom_types, custom_mutable:
            for key in module.__all__:
                if not hasattr(self, key):
                    setattr(self, key, getattr(module, key))

    def create_scoped_session(self, options=None):
        """Hepler factory method that creates a scoped session.

        See: https://github.com/mitsuhiko/flask-sqlalchemy/issues/64

        """
        if options is None:
            options = {}
        scopefunc = options.pop('scopefunc', None)
        db = self

        class PartialSignallingSession(_SignallingSession):

            def __init__(self, autocommit=False, autoflush=False):
                (super(PartialSignallingSession, self)
                 .__init__(db, autocommit, autoflush, **options))

        return orm.scoped_session(
            PartialSignallingSession, scopefunc=scopefunc)


class BaseQueryMixin(object):

    def get_or_create(self, **kwargs):
        """Like django's method get_or_create

        Args:
            defaults: Any keyword arguments passed to `filter_by()`
                      except defaults. defaults is a dict, is only use
                      to create an object.

        Returns:
            tuple: (object, is_created)

        """
        mapper = self._only_full_mapper_zero('get_or_create')
        defaults = kwargs.pop('defaults', {})
        instance = self.filter_by(**kwargs).first()
        if instance:
            return instance, False
        else:
            params = {k: v
                      for k, v in kwargs.iteritems()
                      if not isinstance(v, sql.ClauseElement)}
            if defaults:
                params.update(defaults)
            instance = mapper.class_(**params)
            self.session.add(instance)
            return instance, True

    def batch_get(self, *idents):
        mapper = self._only_full_mapper_zero('batch_get')
        lazyload_idents = {}
        or_list = []
        return_list = [None] * len(idents)
        for idx, ident in enumerate(idents):
            if hasattr(ident, '__composite_values__'):
                ident = ident.__coposite_values__()
            ident = to_list(ident)
            if len(ident) != len(mapper.primary_key):
                raise exc.InvalidRequestError(
                    "Incorrect number of values in identifier to formulate "
                    "primary key for query.batch_get(); "
                    "primary key columns are %s" %
                    ','.join("'%s'" % c for c in mapper.primary_key))

            key = mapper.identity_key_from_primary_key(ident)
            if not self._populate_existing and \
                    not mapper.always_refresh and \
                    self._lockmode is None:

                instance = loading.get_from_identity(
                    self.session, key, attributes.PASSIVE_OFF)
                if instance is not None:
                    # reject calls for id in indentity map but class
                    # mismatch.
                    if not issubclass(instance.__class__, mapper.class_):
                        instance = None
                    return_list[idx] = instance
                    continue

            lazyload_idents.setdefault(key[1], []).append(idx)
            and_list = [col == ide for col, ide in
                        zip(mapper.primary_key, ident)]
            or_list.append(sql.and_(*and_list))

        if or_list:
            # 加载未缓存对象到 return_list 中
            for instance in self.filter(sql.or_(*or_list)):
                ident = mapper.primary_key_from_instance(instance)
                for idx in lazyload_idents[tuple(ident)]:
                    return_list[idx] = instance

        return return_list

SQLAlchemy = type(SQLAlchemy.__name__,
                  (SQLAlchemyMixin, SQLAlchemy), {})
BaseQuery = type(BaseQuery.__name__,
                 (BaseQueryMixin, BaseQuery), {})

# dirty monkey patch
flask_sqlalchemy.BaseQuery = BaseQuery
flask_sqlalchemy.Model.query_class = BaseQuery


class current_user_id(sql.ColumnElement):
    type = types.String()

imsafe = threading.local()


@compiles(current_user_id)
def default_current_user_id(element, compiler, **kw):
    user_id = getattr(imsafe, '_db_current_user_id', request.user_id
                   if request else None)
    return compiler.process(sql.bindparam('current_user_id', user_id))


@contextlib.contextmanager
def set_current_user_id(user_id):
    imsafe._db_current_user_id = user_id
    yield
    delattr(imsafe, '_db_current_user_id')
