# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import re

from flask import current_app as app


__all__ = ['load']


def load_module(module_name):
    return __import__(module_name, globals(), locals(), [b'object'], -1)

def load_file(module):
    kvs = {}
    for k in dir(module):
        if re.match('^[A-Z_]+$', k):
            kvs[k] = getattr(module, k)
    return kvs

def is_pyfile(filename):
    leaf = os.path.split(filename)[1]
    return re.match(r'^[a-z][a-z_]*\.pyc?$', leaf)

def is_initfile(filename):
    leaf = os.path.split(filename)[1]
    return re.match(r'^__init__.pyc?$', leaf)

def is_dir(filename):
    leaf = os.path.split(filename)[1]
    return re.match(r'^[a-z_]+$', leaf)

def load_config(module_name):
    module = load_module(module_name)
    file_path = module.__file__
    if is_pyfile(file_path):
        return load_file(module)
    kvs = {}
    kvs.update(**load_file(module))
    print file_path
    if not is_initfile(file_path):
        return kvs
    dir_path = os.path.split(file_path)[0]
    files = os.listdir(dir_path)
    for f in files:
        sub_path = os.path.join(dir_path, f)
        if is_pyfile(sub_path):
            prefix = f.split('.')[0].upper() + '_'
            submod = module_name + '.' + f.split('.')[0]
        elif is_dir(sub_path):
            prefix = f.upper() + '_'
            submod = module_name + '.' + f
        else:
            continue
        for k, v in load_config(submod).items():
            kvs[prefix + k] = v
    return kvs

def load(module_name):
    kvs = load_config(module_name)
    # app.config.update(**kvs)
    return kvs
