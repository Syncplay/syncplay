#!/usr/bin/env python3
# coding:utf8
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
    ep_client.main()