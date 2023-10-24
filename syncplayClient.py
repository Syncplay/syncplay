#!/usr/bin/env python3

import sys

# libpath

try:
    if (sys.version_info.major != 3) or (sys.version_info.minor < 4):
        raise Exception("You must run Syncplay with Python 3.4 or newer!")
except AttributeError:
    import warnings
    warnings.warn("You must run Syncplay with Python 3.4 or newer!")

from syncplay import ep_client

if __name__ == '__main__':
    def isWindows():
        return sys.platform.startswith(constants.OS_WINDOWS)

    def doWindowsRedistCheck():
        import ctypes
        try:
            ctypes.CDLL('vcruntime140.dll')
        except OSError:
            ctypes.windll.user32.MessageBoxW(0, '''Syncplay relies on the Microsoft Visual C++ Redistributable which is not installed.
                 It can be downloaded at https://aka.ms/vs/17/release/vc_redist.x86.exe
                 For more details see httsp://syncplay.pl/''', "Syncplay", 1)
        sys.exit()

    if isWindows():
        doWindowsRedistCheck()
        
    ep_client.main()
