#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    一些公共的工具
    Add By :e4ting  2023-03-10 14:35:41
"""
import sys,os
import json,time
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack
from textwrap import dedent
# from log.general_log import handle_uncaught_exception

# 强迫 接管系统未知异常
from .log import general_log

# try:
#     from db import *
# except ImportError:
#     pass

# try:
#     from etc import *
# except ImportError:
#     pass


# def get_func(name):
#     return globals()[name]

# __getattr__ = get_func
