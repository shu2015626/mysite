# -*- coding: utf-8 -*-
'''
请写模块说明
'''
__author__ = "sunsn"
__date__ = '2018/9/1 15:40'

import hashlib


def hash_code(s, salt='mysite'): # 加点盐
    h = hashlib.sha3_256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()
