#!/usr/bin/python3.7+
# -*- coding:utf-8 -*-
"""
@auth: cml
@date: 2020-9-
@desc: ...
"""
from random import choice
from .crypto import get_random_string


def get_random_secret_key():
    """
    Return a 50 character random string usable as a SECRET_KEY setting value.
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)


def generate_random_string(length, type_=None):
    """
    功能： 根据不同长度生成随机字符串
    :param length: 字符串长度
    :param type_: 字符串字符类型: 数字， 字母， 所有
    :return: 具有一定长度的随机字符串 salt
    """
    if type_ == "num":
        seed = "1234567890"
    elif type_ == "abc":
        seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    elif type_ == "word":
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    else:
        seed = (
            "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@$%^&*()_+=-"
        )
    string_list = list()
    for i in range(0, length):
        string_list.append(choice(seed))
    salt = "".join(string_list)
    return salt



from .time_utils import *
