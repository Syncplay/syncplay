#coding:utf8

from setuptools import find_packages

common_info = dict(
    name = 'SyncPlay',
    version = '0.7',
    author = 'Tomasz Kowalczyk, Uriziel',
    author_email = 'code@fluxid.pl, urizieli@gmail.com',
    description = 'Solution to synchronize playback of multiple MPlayer and MPC-HC instances over the network.',
    packages = find_packages(exclude=['venv']),
    install_requires = ['Twisted>=11.1'],
)
