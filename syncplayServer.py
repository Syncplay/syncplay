#!/usr/bin/env python
#coding:utf8

import site

# libpath

from twisted.internet import reactor

from syncplay.server import SyncFactory, SyncIsolatedFactory, ConfigurationGetter

argsGetter = ConfigurationGetter()
args = argsGetter.getConfiguration()

if(not args.isolate_rooms):
    reactor.listenTCP(int(args.port), SyncFactory(args.password, args.motd_file))
else:
    reactor.listenTCP(int(args.port), SyncIsolatedFactory(args.password, args.motd_file))
reactor.run()
