#!/usr/bin/env python3
#coding:utf8

import socket
import sys

# libpath

try:
    if (sys.version_info.major != 3) or (sys.version_info.minor < 4):
        raise Exception("You must run Syncplay with Python 3.4 or newer!")
except AttributeError:
    import warnings
    warnings.warn("You must run Syncplay with Python 3.4 or newer!")

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint, TCP6ServerEndpoint

from syncplay.server import SyncFactory, ConfigurationGetter

class ServerStatus: pass

def isListening6(f):
    ServerStatus.listening6 = True

def isListening4(f):
    ServerStatus.listening4 = True

def failed6(f):
    ServerStatus.listening6 = False
    print(f.value)
    print("IPv6 listening failed.")

def failed4(f):
    ServerStatus.listening4 = False
    if ServerStatus.listening6 and "Address already in use" in str(f.value):
        pass
    else:
        print(f.value)
        print("IPv4 listening failed.")


if __name__ == '__main__':
    argsGetter = ConfigurationGetter()
    args = argsGetter.getConfiguration()
    factory = SyncFactory(
        args.port,
        args.password,
        args.motd_file,
        args.isolate_rooms,
        args.salt,
        args.disable_ready,
        args.disable_chat,
        args.max_chat_message_length,
        args.max_username_length,
        args.stats_db_file,
        args.tls
    )
    endpoint6 = TCP6ServerEndpoint(reactor, int(args.port))
    endpoint6.listen(factory).addCallbacks(isListening6, failed6)
    endpoint4 = TCP4ServerEndpoint(reactor, int(args.port))
    endpoint4.listen(factory).addCallbacks(isListening4, failed4)
    if ServerStatus.listening6 or ServerStatus.listening4:
        reactor.run()
    else:
        print("Unable to listen using either IPv4 and IPv6 protocols. Quitting the server now.")
        sys.exit()
