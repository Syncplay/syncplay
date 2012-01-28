#coding:utf8

import time

from twisted.internet.protocol import Factory

from .network_utils import CommandProtocol
from .utils import parse_state


class SyncClientProtocol(CommandProtocol):
    def __init__(self, factory):
        CommandProtocol.__init__(self)

        self.factory = factory

    def connectionMade(self):
        self.send_message('iam', self.factory.name)

    def handle_connected_state(self, arg):
        arg = parse_state(arg)
        if not arg:
            self.drop_with_error('Malformed state attributes')
            return

        paused, position, name = arg

        self.factory.update_state(self, paused, position, name)


    states = dict(
        connected = dict(
            state = 'handle_connected_state',
            seek = 'handle_connected_seek',
            #ping = 'handle_connected_ping',
        ),
    )
    initial_state = 'connected'

