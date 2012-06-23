#coding:utf8
import thread

from twisted.internet import reactor
from syncplay import client
from syncplay.players import mpc

from syncplay import utils

if __name__ == '__main__':
    host, port, name, args = utils.get_configuration()
    #host = 'localhost'
    #port = 9000
    #name = 'Bosman'
    manager = client.Manager(host, port, name, lambda m: mpc.run_mpc(m))
    thread.start_new_thread(utils.stdin_thread, (manager,))
    manager.start()
