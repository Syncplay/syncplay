#!/usr/bin/env python
#coding:utf8

from twisted.internet import reactor

from syncplay.server import SyncFactory, SyncIsolatedFactory
from syncplay.ui.ConfigurationGetter import ServerConfigurationGetter
 
argsGetter = ServerConfigurationGetter()
args = argsGetter.getConfiguration()
if(not args.isolate_rooms):
    reactor.listenTCP(int(args.port), SyncFactory(args.password, args.motd_file))
else:
    reactor.listenTCP(int(args.port), SyncIsolatedFactory(args.password, args.motd_file))
reactor.run()
