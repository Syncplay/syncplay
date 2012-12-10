#coding:utf8

from twisted.internet import reactor

from syncplay.server import SyncFactory
from syncplay.ui.ConfigurationGetter import ServerConfigurationGetter
 
argsGetter = ServerConfigurationGetter()
args = argsGetter.getConfiguration()
reactor.listenTCP(int(args.port), SyncFactory(args.password, args.isolate_rooms))
reactor.run()
