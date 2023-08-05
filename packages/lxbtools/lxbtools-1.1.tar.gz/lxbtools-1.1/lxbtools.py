# -*- coding:utf-8 -*-
# author: liuxiaobo
# time: 2021/6/19 16:46
import hashlib
from datetime import datetime


def md5(str):
    return hashlib.md5(str.encode('utf-8')).hexdigest()


def time_now():
    return datetime.now().strftime('%Y%m%d%H%M%S')
