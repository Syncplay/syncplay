#!/usr/bin/env python
#coding:utf8

from setuptools import setup
import py2exe
from setup_common import common_info

info = dict(
    common_info,
    console = ['syncplay_mplayer.py', {"script":"syncplay_mpc.py","icon_resources":[(1,"icon.ico")]}, 'run_sync_server.py'],
)

setup(**info)

