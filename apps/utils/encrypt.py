# -*- coding: utf-8 -*-
'''
请写模块说明
'''
__author__ = "sunsn"
__date__ = '2018/9/1 15:40'

import hashlib


def hash_code(string, salt='mysite', algorithm='sha256'):
    """记得加盐"""
    if not isinstance(string, bytes):
        string += salt
    else:
        string = string.decode() + salt

    string_bytes = string.encode('utf-8')

    if hasattr(hashlib, algorithm):
        h = getattr(hashlib, algorithm)()
    else:
        raise Exception("不认识的算法，请输入如下内容之一：%s" % "/".join(hashlib.__all__))

    h.update(string_bytes)
    hash_string = h.hexdigest()
    return hash_string