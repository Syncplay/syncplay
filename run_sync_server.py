#coding:utf8

from twisted.internet import reactor

from syncplay.server import SyncFactory
from syncplay import utils
 
argsGetter = utils.ServerConfigurationGetter()
args = argsGetter.getConfiguration()
reactor.listenTCP(8999, SyncFactory(args.password, args.banlist, args.isolate_rooms))
reactor.run()
