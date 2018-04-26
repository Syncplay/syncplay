# -*- mode: python -*-

block_cipher = None


a = Analysis(['syncplayClient.py'],
             pathex=['C:\\Users\\Alberto\\Documents\\syncplay-py3-qtpy-pyside2'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Syncplay',
          debug=False,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=False,
          icon='resources/icon.ico')
