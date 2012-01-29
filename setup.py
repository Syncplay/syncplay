#coding:utf8

from setuptools import setup
from setup_common import common_info

info = dict(
    common_info,
    scripts = ['sync_mplayer.py', 'sync_mpc.py', 'run_sync_server.py'],
)

setup(**info)

