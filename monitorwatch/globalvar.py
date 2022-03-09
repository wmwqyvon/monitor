#!/usr/bin/env python3
# -*- coding:utf-8-*-

def init_global():
    global GLOBAL_DICT
    GLOBAL_DICT = {}


def set_global(name, value):
    try:
        GLOBAL_DICT[name] = value
        return True
    except KeyError:
        return False


def get_global(name):
    try:
        return GLOBAL_DICT[name]
    except KeyError:
        return "Not Found"
