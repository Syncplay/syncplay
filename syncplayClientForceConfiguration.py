#!/usr/bin/env python

from syncplay.clientManager import SyncplayClientManager
import sys
if(__name__ == '__main__'):
    if not '-g' in sys.argv:
        if(not '--force-gui-prompt' in sys.argv):
            sys.argv.extend(("-g",))
    SyncplayClientManager()
