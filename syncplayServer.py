#!/usr/bin/env python3
#coding:utf8

import socket
import sys

# libpath

try:
    if (sys.version_info.major != 3) or (sys.version_info.minor < 4):
        raise Exception("You must run Syncplay with Python 3.4 or newer!")
except AttributeError:
    import warnings
    warnings.warn("You must run Syncplay with Python 3.4 or newer!")

from twisted.internet import reactor, tcp

from syncplay.server import SyncFactory, ConfigurationGetter

class DualStackPort(tcp.Port):

    def __init__(self, port, factory, backlog=50, interface='', reactor=None):
        tcp.Port.__init__(self, port, factory, backlog, interface, reactor)

    def createInternetSocket(self):
        s = tcp.Port.createInternetSocket(self)
        try:
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        except:
            pass
        return s

if __name__ == '__main__':
    argsGetter = ConfigurationGetter()
    args = argsGetter.getConfiguration()
    dsp = DualStackPort(int(args.port),
        SyncFactory(
            args.port,
            args.password,
            args.motd_file,
            args.isolate_rooms,
            args.salt,
            args.disable_ready,
            args.disable_chat,
            args.max_chat_message_length,
            args.max_username_length,
            args.stats_db_file),
        interface='::')
    dsp.startListening()
    reactor.run()
