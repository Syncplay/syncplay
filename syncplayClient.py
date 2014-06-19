#!/usr/bin/env python

import site, sys

# libpath

try:
	if ((sys.version_info.major != 2) or (sys.version_info.minor < 7)):
		raise Exception("You must run Syncplay with Python 2.7!")
except AttributeError:
	import warnings
	warnings.warn("You must run Syncplay with Python 2.7!")

from syncplay.clientManager import SyncplayClientManager
from syncplay.utils import blackholeStdoutForFrozenWindow

if(__name__ == '__main__'):
    blackholeStdoutForFrozenWindow()
    SyncplayClientManager().run()
    
