#!/usr/bin/env python2
#coding:utf8

import site, sys

# libpath

try:
    if (sys.version_info.major != 2) or (sys.version_info.minor < 7):
        raise Exception("You must run Syncplay with Python 2.7!")
except AttributeError:
    import warnings
    warnings.warn("You must run Syncplay with Python 2.7!")

from twisted.internet import reactor

from syncplay.server import SyncFactory, ConfigurationGetter

if __name__ == '__main__':
    argsGetter = ConfigurationGetter()
    args = argsGetter.getConfiguration()
    reactor.listenTCP(int(args.port), SyncFactory(args.password, args.motd_file, args.isolate_rooms, args.salt, args.disable_ready,args.disable_chat, args.max_chat_message_length))
    reactor.run()
