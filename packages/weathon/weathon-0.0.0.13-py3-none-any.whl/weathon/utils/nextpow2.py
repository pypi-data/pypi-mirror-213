# -*- coding: utf-8 -*-
# @Time    : 2023/3/18 14:45
# @Author  : LiZhen
# @FileName: nextpow2.py
# @github  : https://github.com/Lizhen0628
# @Description:


import ctypes as ct


class FloatBits(ct.Structure):
    _fields_ = [
        ('M', ct.c_uint, 23),
        ('E', ct.c_uint, 8),
        ('S', ct.c_uint, 1)
    ]


class Float(ct.Union):
    _anonymous_ = ('bits',)
    _fields_ = [
        ('value', ct.c_float),
        ('bits', FloatBits)
    ]


def next_pow2(x):
    if x < 0:
        x = -x
    if x == 0:
        return 0
    d = Float()
    d.value = x
    if d.M == 0:
        return d.E - 127
    return d.E - 127 + 1

def get_next_power_2(n):
    """
        Returns the closest number that is smaller than n that is a power of 2.
    """

    power = 1
    while (power < n):
        power *= 2
    if power > 1:
        return power / 2
    else:
        return 1