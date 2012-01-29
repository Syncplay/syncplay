#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = 'SyncPlay',
    version = '0.1',
    author = 'Tomasz Kowalczyk, Uriziel',
    author_email = 'code@fluxid.pl',
    description = 'Solution to synchronize playback of multiple MPlayer and MPC-HC instances over the network.',
    packages = find_packages(exclude=['venv']),
    scripts = ['sync_mplayer.py', 'sync_mpc.py', 'run_sync_server.py'],
    install_requires = ['Twisted>=11.1'],
)
