#!/usr/bin/env python
#coding:utf8

from setuptools import setup
import py2exe
from setup_common import common_info

info = dict(
    common_info,
    console = ['syncplay_mplayer.py', 'syncplay_mpc.py', 'run_sync_server.py'],
)

setup(**info)

