# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import rsa

from transflow.core.helpers import cache_for


@cache_for(600)
def shake(size=256):
    return rsa.newkeys(size)


def decrypt(crypto, privkey):
    return rsa.decrypt(crypto, privkey)
