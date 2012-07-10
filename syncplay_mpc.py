#coding:utf8
from syncplay import client
from syncplay.players import mpc

from syncplay import utils


def prepareArguments():
    args = utils.MPCConfigurationGetter()
    args.prepareClientConfiguration()
    return args.getClientConfiguration()

if __name__ == '__main__':
    manager = None
    try:
        args = prepareArguments()
        manager = client.Manager(args.host, args.port, args.name, lambda m: mpc.run_mpc(m, args.mpc_path, args.file, args._args))
        manager.start()
    finally:
        if(manager): manager.stop()

