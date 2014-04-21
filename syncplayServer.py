#!/usr/bin/env python
#coding:utf8

import site

# libpath

from twisted.internet import reactor

from syncplay.server import SyncFactory, ConfigurationGetter

if __name__ == '__main__':
    argsGetter = ConfigurationGetter()
    args = argsGetter.getConfiguration()

    reactor.listenTCP(int(args.port), SyncFactory(args.password, args.motd_file, args.isolate_rooms))
    reactor.run()
