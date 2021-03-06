# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from types import ModuleType

from transflow.core.utils import make_module


class GeneratorModule(ModuleType):

    keys = {'user': '20jMQLgM68J2UBhhjWb1bA4oHdES19SWAODTeYtT25r',
            'email_temp': '20jMQLgM68J2UBhhjWb1bA4oHdES19SWAODTeYtT25r',
            'company': '20jMQLgM68J2UBhhjWb1bA4oHdES19SWAODTeYtT25r',
            'project': '20jMQLgM68J2UBhhjWb1bA4oHdES19SWAODTeYtT25r',
            'task': '20jMQLgM68J2UBhhjWb1bA4oHdES19SWAODTeYtT25r',
            'cross': '20jMQLgM68J2UBhhjWb1bA4oHdES19SWAODTeYtT25r',
            'document': '20jMQLgM68J2UBhhjWb1bA4oHdES19SWAODTeYtT25r',
            'member': '20jMQLgM68J2UBhhjWb1bA4oHdES19SWAODTeYtT25r',
            'staff': '20jMQLgM68J2UBhhjWb1bA4oHdES19SWAODTeYtT25r',
            }

    def __getattr__(self, key):
        if key in self.keys:
            return self.generator(key)
        return super(GeneratorModule, self).__getattr__(key)

    def nextorigid(self, key):
        from transflow.core.engines import db
        return db.session.execute(db.Sequence('%s_id_seq' % key))

    def nextval(self, key):
        from transflow.core.dbutils import pad_left
        from transflow.contribs import feistel, base62
        orig_id = self.nextorigid(key)
        fei = feistel.Feistel(self.keys[key])
        return pad_left(base62.base62_encode(fei.encrypt(orig_id)))

    def generator(self, key):
        return lambda: self.nextval(key)

make_module(GeneratorModule, __name__)
