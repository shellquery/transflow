# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import re

from wtforms.validators import Regexp, Length

from liyan.core import pinyin

__all__ = ['Tkey', 'Unikey', 'PinyinLength']


class Tkey(Regexp):

    def __init__(self, size=12, message=None):
        super(Tkey, self).__init__(
            r'^[0-9a-zA-Z]{%d}$' % size, message=message)

    def __call__(self, form, field):
        if self.message is None:
            self.message = '非法的tkey'

        super(Tkey, self).__call__(form, field)


class Unikey(Regexp):

    def __init__(self, message=None):
        super(Unikey, self).__init__(
            r'^[0-9a-zA-Z\-]{2,200}$', message=message)

    def __call__(self, form, field):
        if self.message is None:
            self.message = '非法的unikey'

        super(Unikey, self).__call__(form, field)


class PinyinLength(Length):

    @staticmethod
    def namelen(word):
        return pinyin.word_len(word)

    def __call__(self, form, field):
        l = field.data and self.namelen(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            if self.message is None:
                if self.min > 0 and self.max > 0:
                    self.message = (
                        '非法的名称，必须%s~%s个之间的英文单词数字或汉字'
                        % (self.min, self.max))
                elif self.min > 0:
                    self.message = (
                        '非法的名称，必须至少%s英文单词数字或汉字'
                        % self.min)
                elif self.max > 0:
                    self.message = (
                        '非法的名称，必须最多%s英文单词数字或汉字'
                        % self.max)

            raise ValueError(self.message % dict(min=self.min, max=self.max))


class Nickname(Regexp):
    """
    校验是否是合法的昵称.

    """

    def __init__(self, message=None):
        super(Nickname, self).__init__(
            ur'[\w\u3400-\u4db5\u4e00-\u9fcb.-]{1,20}', message=message)

    def __call__(self, form, field):
        if self.message is None:
            self.message = '昵称仅限中英文、数字、“.”、“-”及“_”'

        super(Nickname, self).__call__(form, field)


class CJKLength(Length):

    @staticmethod
    def cjk_len(text):
        if isinstance(text, str):
            text = unicode(text, 'U8')
        l = len(text)
        l -= len(re.findall('[\x00-\xff]', text)) / 2.0
        return l

    def __call__(self, form, field):
        l = field.data and self.cjk_len(field.data) or 0
        if l < self.min or self.max != -1 and l > self.max:
            if self.message is None:
                if self.max == -1:
                    self.message = '字段长度不得少于%(min)d个（半角字符算半个）'
                elif self.min == -1:
                    self.message = '字段长度不得多于%(max)d个（半角字符算半个）'
                else:
                    self.message = '字段长度必须在%(min)d到%(max)d之间（半角字符算半个）'

            raise ValueError(self.message % dict(min=self.min, max=self.max))
