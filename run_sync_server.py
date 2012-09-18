#coding:utf8

from twisted.internet import reactor

from syncplay.server import SyncFactory
from syncplay import utils
 
argsGetter = utils.ServerConfigurationGetter()
args = argsGetter.getConfiguration()
reactor.listenTCP(args.port, SyncFactory(args.password, args.isolate_rooms))
reactor.run()
