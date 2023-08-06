'''
Copyright [2023] [许灿标]
license: Apache License, Version 2.0
email: lcctoor@outlook.com
'''

import re
from collections import deque
from random import uniform
from datetime import datetime as datetime2
from datetime import timedelta
from time import struct_time
from typing import Union


A = ['year', 'month', 'day', 'hour', 'minute', 'second']
B = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
C = ['年', '月', '日', '时', '分', '秒']

creat_time_keys = {}
add_keys = _ = {}

for a, b, c in zip(A, B, C):
    creat_time_keys[a] = creat_time_keys[b] = creat_time_keys[c] = a
    add_keys[a] = add_keys[b] = add_keys[c] = b

creat_time_default = {'year': 1, 'month': 1, 'day': 1, 'hour': 0, 'minute': 0, 'second': 0}


def parse_time(t: Union[str, dict, list, int, float]):
    typ = type(t)
    if typ in (int, float):
        return datetime2.fromtimestamp(t)  # 从时间戳生成
    elif not t:
        return datetime2.now()  # 生成当前时区的当前时间
    if typ is str: return datetime2(*map(int, re.findall('\d+', t)))  # 从字符串生成
    if typ in (list, tuple, deque): return datetime2(*t)  # 从容器生成
    if typ is cooltime: return t.t  # 从自身类型生成
    if typ is datetime2: return t  # 从datetime生成
    # 从标准库的time.localtime生成
    if typ is struct_time: return datetime2(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    # 从字典生成
    if typ is dict:
        s = creat_time_default | {creat_time_keys.get(k,k):v for k,v in t.items()}
        return datetime2(**s)
    raise TypeError(t)

def parse_add(dt: Union[int, float, dict]):
    if type(dt) in (int, float):
        return timedelta(seconds=dt)
    return timedelta(**{add_keys.get(k,k): v for k,v in dt.items()})

class cooltime():
    def __init__(self, t=None):
        self.t = t = parse_time(t)
        self.year = t.year
        self.month = t.month
        self.day = t.day
        self.hour = t.hour
        self.minute = t.minute
        self.second = t.second

    def __eq__(self, t): return self.t == parse_time(t)
    def __ne__(self, t): return self.t != parse_time(t)
    def __lt__(self, t): return self.t < parse_time(t)
    def __le__(self, t): return self.t <= parse_time(t)
    def __ge__(self, t): return self.t >= parse_time(t)
    def __gt__(self, t): return self.t >= parse_time(t)

    def __float__(self): return self.t.timestamp()
    def __int__(self): return int(self.t.timestamp())
    def __bool__(self): return True
    def __str__(self): return str(self.t)
    def str_floor(self): return str(self.t)[:19]
    def date(self): return str(self.t)[:10]
    def __repr__(self): return f"cooltime({str(self.t)[:19]})"
    def strftime(self, fmt="%Y-%m-%d %H:%M:%S"): return self.t.strftime(fmt)

    def __add__(self, dt): return cooltime(self.t + parse_add(dt))
    def __sub__(self, dt): return cooltime(self.t - parse_add(dt))
    def __iadd__(self, dt):
        self.t += parse_add(dt)
        return self
    def __isub__(self, dt):
        self.t -= parse_add(dt)
        return self

    @staticmethod
    def random(start=None, end=None):
        if not (start or isinstance(start, (int, float))):
            start = 63043200  # 北京时间1972-01-01
        if not (end or isinstance(end, (int, float))):
            end = 2114352000  # 北京时间2037-01-01
        return cooltime(uniform(float(cooltime(start)), float(cooltime(end))))