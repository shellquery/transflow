# -*- coding: utf-8 -*-

from werkzeug.routing import BaseConverter


class TkeyConverter(BaseConverter):
    regex = '[0-9a-zA-Z]{12}'


class UnikeyConverter(BaseConverter):
    regex = '[0-9a-zA-Z\-]{2,200}'


addition_converters = {
    'tkey': TkeyConverter,
    'unikey': UnikeyConverter
}
