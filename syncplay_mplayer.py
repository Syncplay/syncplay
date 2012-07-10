#coding:utf8
from syncplay import client
from syncplay.players import mplayer

from syncplay import utils

def prepareArguments():
    args = utils.ConfigurationGetter()
    args.prepareClientConfiguration()
    return args.getClientConfiguration()

if __name__ == '__main__':
    args = prepareArguments()
    args.args.extend(('-slave', '-msglevel', 'all=1:global=4'))
    if(args.file): args.args.extend((args.file,))
    manager = client.Manager(args.host, args.port, args.name, lambda m: mplayer.run_mplayer(m, 'mplayer', args.args))
    manager.start()

