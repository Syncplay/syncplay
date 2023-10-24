version = '1.7.1'
revision = ' release candidate 1'
milestone = 'Yoitsu'
release_number = '108'
projectURL = 'https://syncplay.pl/'

def isWindows():
    return sys.platform.startswith("win")

def doWindowsRedistCheck():
    import ctypes
    try:
        ctypes.CDLL('vcruntime140.dll')
    except OSError:
        ctypes.windll.user32.MessageBoxW(0, '''Syncplay relies on the Microsoft Visual C++ Redistributable which is not installed.
             It can be downloaded at https://aka.ms/vs/17/release/vc_redist.x86.exe
             For more details see http://syncplay.pl/''', "Syncplay", 1)
    sys.exit()

if isWindows():
    doWindowsRedistCheck()
