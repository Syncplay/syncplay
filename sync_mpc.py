#coding:utf8
import thread

from twisted.internet import reactor
from syncplay import client
from syncplay.players import mpc

from syncplay import utils

if __name__ == '__main__':
    args = utils.get_configuration()
    manager = client.Manager(args.host, args.port, args.name, lambda m: mpc.run_mpc(m))
    thread.start_new_thread(utils.stdin_thread, (manager,))
    manager.start()
