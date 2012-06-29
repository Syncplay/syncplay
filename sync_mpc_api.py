#coding:utf8
import thread
import sys

from twisted.internet import reactor
from syncplay import client
from syncplay.players import mpc_using_api

from syncplay import utils


def prepare_args(args):
    if (args.mpc_path == None):
        sys.exit("You must supply mpc-path on first run")
    args.args.extend(['/open', '/new'])

if __name__ == '__main__':
    try:
        args = utils.get_configuration()  
        prepare_args(args)
        manager = client.Manager(args.host, args.port, args.name, lambda m: mpc_using_api.run_mpc(m, args.mpc_path, args.file, args.args))
        manager.start()
    finally:
        manager.stop()
