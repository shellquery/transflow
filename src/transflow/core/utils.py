# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

__all__ = ['make_module']

def make_module(clazz, module_name):
    module = sys.modules[module_name]
    new_module = sys.modules[module.__name__] = clazz(module.__name__, module.__doc__)
    new_module.__dict__.update({
        '__file__': module.__file__,
        '__builtins__': module.__builtins__
    })
    return new_module
