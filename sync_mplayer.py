#coding:utf8

import sys

from twisted.internet import reactor

from syncplay import client
from syncplay.players import mplayer

if __name__ == '__main__':
    args = sys.argv[1:]
    host = args.pop(0)
    name = args.pop(0)
    if ':' in host:
        host, port = host.split(':', 1)
        port = int(port)
    else:
        port = 8999
    
    args.extend(('-slave', '-msglevel', 'all=1:global=4'))

    manager = client.Manager(host, port, name, lambda m: mplayer.run_mplayer(m, 'mplayer', args))
    manager.start()

