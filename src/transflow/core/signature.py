# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import rsa
import json

from transflow.core.helpers import cache_for


@cache_for(600)
def shake(size=512):
    return rsa.newkeys(size)

def freeze(keypair):
    return json.dumps((keypair[0].save_pkcs1(), keypair[1].save_pkcs1()))

def restore(freezed):
    kp = json.loads(freezed)
    return rsa.PublicKey.load_pkcs1(kp[0]), rsa.PrivateKey.load_pkcs1(kp[1])

def decrypt(crypto, private_key):
    return rsa.decrypt(crypto, private_key)
