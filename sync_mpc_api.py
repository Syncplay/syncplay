#coding:utf8
import thread
import sys

from twisted.internet import reactor
from syncplay import client
from syncplay.players import mpc_using_api

from syncplay import utils

if __name__ == '__main__':
    args = utils.get_configuration()  
    if(args.mpc_path == None):
        sys.exit("You must supply mpc-path on first run")
    args.args.extend(['/open', '/new'])
    manager = client.Manager(args.host, args.port, args.name, lambda m: mpc_using_api.run_mpc(m, args.mpc_path, args.file, args.args))
    thread.start_new_thread(utils.stdin_thread, (manager,))
    manager.start()
