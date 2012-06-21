#coding:utf8
import thread
import sys

from twisted.internet import reactor
from syncplay import client
from syncplay.players import mpc


import common_functions

if __name__ == '__main__':
    host, port, name, args = common_functions.get_configuration()
    manager = client.Manager(host, port, name, lambda m: mpc.run_mpc(m))
    thread.start_new_thread(common_functions.stdin_thread, (manager,))
    manager.start()
