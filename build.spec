# -*- mode: python ; coding: utf-8 -*-

from syncplay import version

a = Analysis(
    ['syncplayClient.py'],
    pathex=[],
    binaries=[],
    datas=[['syncplay/resources', 'resources']],
    hiddenimports=[
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "PySide6.QtCore",
        "PySide2.QtGui",
        "PySide2.QtWidgets",
        "PySide2.QtCore",
        "PyQt5.QtGui",
        "PyQt5.QtWidgets",
        "PyQt5.QtCore"
    ],
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
    target_arch=None,
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
    target_arch=None,
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
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDocumentTypes': [
            {
                'CFBundleName': 'Syncplay',
                'CFBundleShortVersionString': version,
                'CFBundleIdentifier': 'pl.syncplay.Syncplay',
                'LSMinimumSystemVersion': '10.12.0',
                'NSHumanReadableCopyright': 'Copyright © 2025 Syncplay All Rights Reserved'
            }
        ]
    }
)