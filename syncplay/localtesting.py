#coding:utf8
'''
Monkey patches for testing with emulated network latency and time offset
'''

from collections import deque
import os
import time
import random

from twisted.internet import reactor

from . import network_utils


try:
    OFFSET = float(os.environ['OFFSET'])
except (ValueError, KeyError):
    pass
else:
    orig_time = time.time
    def new_time(*args, **kwargs):
        return orig_time(*args, **kwargs) + OFFSET
    time.time = new_time

try:
    LAG_MU = float(os.environ['LAG_MU'])
    LAG_SIGMA = float(os.environ['LAG_SIGMA'])
except (ValueError, KeyError):
    pass
else:
    random.seed()
    OriginalCommandProtocol = network_utils.CommandProtocol

    class LaggedCommandProtocol(OriginalCommandProtocol):
        def __init__(self, *args, **kwargs):
            self._queue_in = deque()
            self._queue_out = deque()
            OriginalCommandProtocol.__init__(self, *args, **kwargs)

        def lineReceived(self, line):
            self._queue_in.append(line)
            reactor.callLater(
                abs(random.gauss(LAG_MU, LAG_SIGMA)),
                lambda: OriginalCommandProtocol.lineReceived(self, self._queue_in.popleft())
            )

        def sendLine(self, line):
            self._queue_out.append(line)
            reactor.callLater(
                abs(random.gauss(LAG_MU, LAG_SIGMA)),
                lambda: OriginalCommandProtocol.sendLine(self, self._queue_out.popleft())
            )

    network_utils.CommandProtocol = LaggedCommandProtocol

