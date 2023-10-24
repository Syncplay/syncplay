import sys
import ctypes

from syncplay.clientManager import SyncplayClientManager
from syncplay.utils import blackholeStdoutForFrozenWindow, isWindows

def main():   
    def doWindowsRedistCheck():
        try:
            ctypes.CDLL('vcruntime140.dll')
        except OSError:
            ctypes.windll.user32.MessageBoxW(0, '''Syncplay relies on the Microsoft Visual C++ Redistributable which is not installed.
                 It can be downloaded at https://aka.ms/vs/17/release/vc_redist.x86.exe
                 For more details see http://syncplay.pl/''', "Syncplay", 1)
        sys.exit()
    if isWindows():
        doWindowsRedistCheck()
    blackholeStdoutForFrozenWindow()
    SyncplayClientManager().run()

if __name__ == "__main__":
    main()
