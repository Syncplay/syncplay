#-----------------------------------------------------------------------------
#  Copyright (C) 2019 Alberto Sottile
#
#  Distributed under the terms of the 3-clause BSD License.
#-----------------------------------------------------------------------------

__version__ = '0.1.0'

import sys
import platform
from distutils.version import LooseVersion as V

if sys.platform != "darwin" or V(platform.mac_ver()[0]) < V("10.14"):
    from ._dummy import *
else:
    from ._detect import *

del sys, platform, V