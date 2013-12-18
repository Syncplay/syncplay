#!/usr/bin/env python

import site

# libpath

from syncplay.clientManager import SyncplayClientManager
from syncplay.utils import blackholeStdoutForFrozenWindow

if(__name__ == '__main__'):
    blackholeStdoutForFrozenWindow()
    SyncplayClientManager().run()
    
