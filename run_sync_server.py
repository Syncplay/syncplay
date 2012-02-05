#coding:utf8

from twisted.internet import reactor

from syncplay.server import SyncFactory 

reactor.listenTCP(8999, SyncFactory())
reactor.run()
