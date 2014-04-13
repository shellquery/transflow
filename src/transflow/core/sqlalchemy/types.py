# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

import socket
import struct
import anyjson as json
import sqlalchemy as sa
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import TypeDecorator, LargeBinary, CHAR, \
    Integer, String, BigInteger, Boolean
from sqlalchemy.dialects.postgresql import UUID, INET, CIDR
from iptools import IpRange
import uuid

__all__ = ['JSONType', 'LowerString', 'GUID']


class LowerString(TypeDecorator):

    impl = String

    def process_bind_param(self, value, dialect):
        return value.lower()


class JSONType(TypeDecorator):

    impl = LargeBinary

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class GUID(TypeDecorator):

    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value)
            else:
                # hexstring
                return "%.32x" % value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)
