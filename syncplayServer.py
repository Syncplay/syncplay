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

from OpenSSL import crypto
from twisted.internet import reactor, ssl
from twisted.internet.endpoints import SSL4ServerEndpoint

from syncplay.server import SyncFactory, ConfigurationGetter

with open('server.pem') as f:
    certData = f.read()

certificate = ssl.PrivateCertificate.loadPEM(certData).options()

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
        args.stats_db_file
    )
    endpoint4 = SSL4ServerEndpoint(reactor, int(args.port), certificate, interface='0.0.0.0')
    endpoint4.listen(factory)
    endpoint6 = SSL4ServerEndpoint(reactor, int(args.port), certificate, interface='::')
    endpoint6.listen(factory)
    reactor.run()
