#coding:utf8

import sys

from twisted.internet import reactor

from syncplay import client
from syncplay.players import mpc

if __name__ == '__main__':
    args = sys.argv[1:]
    host = args.pop(0)
    name = args.pop(0)
    if ':' in host:
        host, port = host.split(':', 1)
        port = int(port)
    else:
        port = 8999

    manager = client.Manager(host, port, name)
    manager.start()
    player = mpc.MPCHCPlayer(manager)
    reactor.run()

