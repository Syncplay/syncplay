# -*- mode: python -*-

import os
workdir = os.getcwd()

import syncplay

block_cipher = None


a = Analysis(['syncplayClient.py'],
             pathex=[workdir],
             binaries=[],
             datas=[('resources/*', 'resources')],
             hiddenimports=['PySide2', 'PySide2.QtCore', 'PySide2.QtWidgets'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Syncplay',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='resources/icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name="syncplay_v{}".format(syncplay.version))
