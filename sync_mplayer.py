#coding:utf8
import thread
import sys

from twisted.internet import reactor
from syncplay import client
from syncplay.players import mplayer


import common_functions

if __name__ == '__main__':
    host, port, name, args = common_functions.get_configuration()
    args.extend(('-slave', '-msglevel', 'all=1:global=4'))
    manager = client.Manager(host, port, name, lambda m: mplayer.run_mplayer(m, 'mplayer', args))
    thread.start_new_thread(common_functions.stdin_thread, (manager,))
    manager.start()

