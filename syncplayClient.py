#!/usr/bin/env python

from syncplay.clientManager import SyncplayClientManager
from syncplay.utils import blackholeStdoutForFrozenWindow
if(__name__ == '__main__'):
    blackholeStdoutForFrozenWindow()
    SyncplayClientManager().run()
    