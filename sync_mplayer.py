#coding:utf8
import thread
import sys

from twisted.internet import reactor
from syncplay import client
from syncplay.players import mplayer

from syncplay import utils

if __name__ == '__main__':
    args = utils.get_configuration()
    args.args.extend(('-slave', '-msglevel', 'all=1:global=4'))
    manager = client.Manager(args.host, args.port, args.name, lambda m: mplayer.run_mplayer(m, 'mplayer', args.args))
    thread.start_new_thread(utils.stdin_thread, (manager,))
    manager.start()

