#!/usr/bin/env python
#coding:utf8
from distutils.core import setup
from py2exe.build_exe import py2exe

import syncplay
import sys

sys.argv.extend(['py2exe', '-p win32com ', '-i twisted.web.resource'])
common_info = dict(
    name='Syncplay',
    version=syncplay.version,
    author='Uriziel',
    author_email='urizieli@gmail.com',
    description='Syncplay',
)

info = dict(
    common_info,
    console=[{"script":"syncplayClient.py", "icon_resources":[(1, "resources\\icon.ico")], 'dest_base': "Syncplay"}, 'syncplayServer.py'],
    options={'py2exe': {
                         'dist_dir': "syncplay v%s" % syncplay.version,
                         'includes': 'cairo, pango, pangocairo, atk, gobject, twisted',
                         'excludes': 'venv, _ssl, doctest, pdb, unittest, difflib, win32clipboard, win32event, win32file, win32pdh, win32security, win32trace, win32ui, winxpgui, win32pipe, win32process',
                         'dll_excludes': 'msvcr71.dll',
                         'optimize': 2,
                         'compressed': 1
                         }
             },
    data_files = [("resources", ["resources/buzzer.wav", "resources/icon.ico",]), ("", ["resources/syncplayClientForceConfiguration.bat",])],
    zipfile = "lib/libsync",
                
)

setup(**info)

