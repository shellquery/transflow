# -*- coding: utf-8 -*-

from __future__ import unicode_literals


from sqlalchemy.ext.hybrid import Comparator

from tranflow.core.engines import db


__all__ = ['pad_left', 'CaseInsensitiveComparator']


def pad_left(s, c='0', bits=12):
    if len(s) >= bits:
        return s
    return '0' * (bits - len(s)) + s


class CaseInsensitiveComparator(Comparator):

    def __eq__(self, other):
        return db.func.lower(self.__clause_element__()) == db.func.lower(other)
