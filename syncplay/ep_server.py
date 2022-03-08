import sys

from twisted.internet import reactor, endpoints
from twisted.internet.endpoints import TCP4ServerEndpoint, TCP6ServerEndpoint
from twisted.internet.error import CannotListenError

from twisted.web import server, resource

from syncplay.server import SyncFactory, ConfigurationGetter
from syncplay.webapi import WebAPI

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
    if f.type is CannotListenError and ServerStatus.listening6:
        pass
    else:
        print(f.value)
        print("IPv4 listening failed.")


def main():
    argsGetter = ConfigurationGetter()
    args = argsGetter.getConfiguration()
    factory = SyncFactory(
        args.port,
        args.password,
        args.motd_file,
        args.rooms_db_file,
        args.permanent_rooms_file,
        args.isolate_rooms,
        args.salt,
        args.disable_ready,
        args.disable_chat,
        args.max_chat_message_length,
        args.max_username_length,
        args.stats_db_file,
        args.tls
    )
    if args.webhook_port:
        site = server.Site(WebAPI(factory))
        webapi6 = TCP6ServerEndpoint(reactor, int(args.webhook_port))
        webapi6.listen(site)
        #webapi4 = TCP4ServerEndpoint(reactor, int(args.webhook_port))
        #webapi4.listen(site)
    endpoint6 = TCP6ServerEndpoint(reactor, int(args.port))
    endpoint6.listen(factory).addCallbacks(isListening6, failed6)
    endpoint4 = TCP4ServerEndpoint(reactor, int(args.port))
    endpoint4.listen(factory).addCallbacks(isListening4, failed4)
    if ServerStatus.listening6 or ServerStatus.listening4:
        reactor.run()
    else:
        print("Unable to listen using either IPv4 and IPv6 protocols. Quitting the server now.")
        sys.exit()

if __name__ == "__main__":
    main()

