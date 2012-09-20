#!/usr/bin/env python
#coding:utf8

from setuptools import setup
import py2exe #@UnusedImport
from setuptools import find_packages
import syncplay

common_info = dict(
    name = 'Syncplay',
    version = syncplay.version,
    author = 'Tomasz Kowalczyk, Uriziel',
    author_email = 'code@fluxid.pl, urizieli@gmail.com',
    description = 'Syncplay',
    packages = find_packages(exclude=['venv']),
    install_requires = ['Twisted>=11.1'],
)

info = dict(
    common_info,
    console = [{"script":"syncplayClient.py","icon_resources":[(1,"icon.ico")]}, 'syncplayServer.py'],
    options = {'py2exe': {
                      'packages':'encodings',
                      'includes': 'cairo, pango, pangocairo, atk, gobject',
                      }
          },

)

setup(**info)

