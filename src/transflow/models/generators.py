# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from types import ModuleType

from transflow.core.engines import db
from transflow.core.db import pad_left
from transflow.contribs import feistel, base62
from transflow.core.utils import make_module


class GeneratorModule(ModuleType):

    keys = {'user': '20jMQLgM68J2UBhhjWb1bA4oHdES19SWAODTeYtT25r'}

    def __getattr__(self, key):
        if key in self.keys:
            return self.generator(key)
        return super(GeneratorModule, self).__getattr__(key)

    def nextval(self, key):
        orig_id = db.session.execute(db.Sequence('%s_id_seq' % key))
        fei = feistel.Feistel(self.keys[key])
        return pad_left(base62.base62_encode(fei.encrypt(orig_id)))

    def generator(self, key):
        return lambda: self.nextval(key)

make_module(GeneratorModule, __name__)
