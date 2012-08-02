#coding:utf8

from setuptools import find_packages

common_info = dict(
    name = 'Syncplay',
    version = '0.9',
    author = 'Tomasz Kowalczyk, Uriziel',
    author_email = 'code@fluxid.pl, urizieli@gmail.com',
    description = 'Syncplay',
    packages = find_packages(exclude=['venv']),
    install_requires = ['Twisted>=11.1'],
)