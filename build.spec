# -*- mode: python ; coding: utf-8 -*-

import importlib.util
import sys

from syncplay import version

target_arch = "universal2" if sys.platform == "darwin" else None

hiddenimports = [
    "{}.{}".format(binding, module)
    for binding in ("PySide6", "PySide2", "PyQt5")
    if importlib.util.find_spec(binding)
    for module in ("QtGui", "QtWidgets", "QtCore")
]

a = Analysis(
    ['syncplayClient.py'],
    pathex=[],
    binaries=[],
    datas=[['syncplay/resources', 'resources']],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=1,
)

b = Analysis(
    ['syncplayServer.py'],
    pathex=[],
    binaries=[],
    datas=[['syncplay/resources', 'resources']],
    optimize=1,
)
MERGE((a, "client", "client"), (b, "server", "server"))
pyz = PYZ(a.pure)
pyzb = PYZ(b.pure)

# Main executable for the client
exe_client = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Syncplay',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=target_arch,
    codesign_identity=None,
    entitlements_file=None,
    icon=['syncplay/resources/icon.ico'],
)

# Additional executable for the server
exe_server = EXE(
    pyzb,
    b.scripts,
    [],
    exclude_binaries=True,
    name='syncplayServer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Use console=True for server scripts
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=target_arch,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe_client,
    exe_server,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='syncplay',
)

# Bundle the client executable and include the server executable as a resource
app = BUNDLE(
    exe_client,
    a.binaries,
    a.datas,
    [('syncplayServer', exe_server.name, 'EXECUTABLE')],
    name='Syncplay.app',
    icon='./syncplay/resources/icon.icns',
    bundle_identifier=None,
    version=version,
    target_arch=target_arch,
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDocumentTypes': [
            {
                'CFBundleName': 'Syncplay',
                'CFBundleShortVersionString': version,
                'CFBundleIdentifier': 'pl.syncplay.Syncplay',
                'LSMinimumSystemVersion': '10.12.0',
                'NSHumanReadableCopyright': 'Copyright © 2026 Syncplay All Rights Reserved'
            }
        ]
    }
)