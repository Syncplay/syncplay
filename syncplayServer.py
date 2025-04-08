#!/usr/bin/env python3

import sys

# libpath

try:
    if (sys.version_info.major != 3) or (sys.version_info.minor < 6):
        raise Exception("You must run Syncplay with Python 3.6 or newer!")
except AttributeError:
    import warnings
    warnings.warn("You must run Syncplay with Python 3.6 or newer!")

from syncplay import ep_server

if __name__ == '__main__':
    ep_server.main()