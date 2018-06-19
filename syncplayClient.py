#!/usr/bin/env python2

import sys

# libpath

try:
    if (sys.version_info.major != 3) or (sys.version_info.minor < 4):
        raise Exception("You must run Syncplay with Python 3.4 or newer!")
except AttributeError:
    import warnings
    warnings.warn("You must run Syncplay with Python 3.4 or newer!")

from syncplay.clientManager import SyncplayClientManager
from syncplay.utils import blackholeStdoutForFrozenWindow

if __name__ == '__main__':
    blackholeStdoutForFrozenWindow()
    SyncplayClientManager().run()
    
