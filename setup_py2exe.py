#!/usr/bin/env python
#coding:utf8

from setuptools import setup
import py2exe
from setup_common import common_info

info = dict(
    common_info,
    console = ['sync_mplayer.py', 'sync_mpc_api.py', 'sync_mpc.py', 'run_sync_server.py'],
)

setup(**info)

