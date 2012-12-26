#!/usr/bin/env python
#coding:utf8

from setuptools import setup
import py2exe #@UnusedImport
from setuptools import find_packages
import syncplay
import sys

sys.argv.extend(['py2exe', '-p win32com ', '-i twisted.web.resource'])
common_info = dict(
    name='Syncplay',
    version=syncplay.version,
    author='Uriziel',
    author_email='urizieli@gmail.com',
    description='Syncplay',
    packages=find_packages(exclude=['venv']),
    install_requires=['Twisted>=11.1'],
)

info = dict(
    common_info,
    console=[{"script":"syncplayClient.py", "icon_resources":[(1, "resources\\icon.ico")]}, 'syncplayServer.py'],
    options={'py2exe': {
                         'includes': 'cairo, pango, pangocairo, atk, gobject',
                         'excludes': '_ssl, doctest, pdb, unittest, difflib, win32clipboard, win32event, win32file, win32pdh, win32security, win32trace, win32ui, winxpgui, win32pipe, win32process',
                         'dll_excludes': 'msvcr71.dll',
                         'optimize': 2,
                         'compressed': 1
                         }
                          
          },

)

setup(**info)

