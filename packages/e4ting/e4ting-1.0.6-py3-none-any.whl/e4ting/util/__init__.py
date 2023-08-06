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

from .util import *

def __getattr__(func):
    from common import util
    return getattr(util, func)

