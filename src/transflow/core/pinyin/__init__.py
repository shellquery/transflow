# -*- coding:utf-8 -*-

from __future__ import unicode_literals


import types
import string
import os.path

from transflow.core.utils import make_module


class PinYin(types.ModuleType):

    alnum = string.digits + string.letters

    def __init__(self, *args, **kwargs):
        super(PinYin, self).__init__(*args, **kwargs)
        self.word_dict = {}
        dict_file = kwargs.get('dict_file', '/word.data')
        self.dict_file = (
            os.path.dirname(os.path.abspath(__file__)) + dict_file)
        self.load_word()

    def load_word(self):
        if not os.path.exists(self.dict_file):
            raise IOError("NotFoundFile")

        with file(self.dict_file) as f_obj:
            for f_line in f_obj.readlines():
                line = f_line.strip().split(' ')
                if line[1][-1] in string.digits:
                    v = line[1][:-1]
                else:
                    v = line[1]
                self.word_dict[line[0]] = v.lower()

    def word_len(self, word):
        '''
        统计字数 一个英文单词a-zA-Z0-9一个字 一个汉子一个字
        '''
        if not isinstance(word, unicode):
            word = word.decode('utf8')
        parts = self.trim_word(word).split(' ')
        l = 0
        for part in parts:
            l += self._part_len(part)
        return l

    def _part_len(self, part):
        return len(self._scatter(part))

    def _scatter(self, letters):
        eng = []
        ws = []
        for c in letters:
            if c in self.alnum:
                eng.append(c)
            else:
                if eng:
                    ws.append(''.join(eng))
                    eng = []
                ws.append(c)
        if eng:
            ws.append(''.join(eng))
        return ws

    def trim_word(self, word):
        '''
        特殊字符转换成空格
        多个空格转成一个空格
        去掉首位空格
        '''
        import re
        chars = []
        for c in word:
            key = '%X' % ord(c)
            if key in self.word_dict:
                chars.append(c)
            elif c in self.alnum:
                chars.append(c)
            else:
                chars.append(' ')
        new_word = ''.join(chars)
        return re.sub('\s+', ' ', new_word).strip()

    def tran(self, word):
        if not isinstance(word, unicode):
            word = word.decode('utf8')
        word = self.trim_word(word)
        parts = word.split(' ')
        pieces = []
        for part in parts:
            pieces.extend(self._tran_part(part))
        return '-'.join(pieces)

    def _tran_part(self, part):
        ws = self._scatter(part)
        ps = []
        for w in ws:
            if w[0] in self.alnum:
                ps.append(w)
            else:
                key = '%X' % ord(w)
                py = self.word_dict[key]
                if py:
                    ps.append(self.word_dict[key])
        return ps


make_module(PinYin, __name__)
