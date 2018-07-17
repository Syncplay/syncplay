# -*- mode: python -*-

import os
workdir = os.getcwd()

block_cipher = None


a = Analysis(['syncplayServer.py'],
             pathex=[workdir],
             binaries=[],
             datas=[('resources/*', 'resources')],
             hiddenimports=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Syncplay',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=True)
