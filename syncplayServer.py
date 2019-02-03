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
from twisted.internet.endpoints import TCP4ServerEndpoint, SSL4ServerEndpoint, TCP6ServerEndpoint

from syncplay.server import SyncFactory, ConfigurationGetter

with open('server.crt', 'r') as f:
    cert_data = f.read()
with open('server.key', 'r') as f:
    key_data = f.read()

cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_data)
options = ssl.CertificateOptions(
    privateKey=key,
    certificate=cert,
    acceptableProtocols=[b'h2'],
)

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
    #endpoint4 = TCP4ServerEndpoint(reactor, int(args.port))
    endpoint4 = SSL4ServerEndpoint(reactor, int(args.port), options)
    endpoint4.listen(factory)
    #endpoint6 = TCP6ServerEndpoint(reactor, int(args.port))
    #endpoint6.listen(factory)
    reactor.run()
