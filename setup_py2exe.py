#coding:utf8

from setuptools import setup
from setup_common import common

info = dict(
    common,
    scripts = ['sync_mplayer.py', 'sync_mpc.py', 'run_sync_server.py'],
)

setup(**info)
