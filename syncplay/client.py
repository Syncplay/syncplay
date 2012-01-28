#coding:utf8

import time

from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory

from .network_utils import CommandProtocol
from .utils import parse_state


class SyncClientProtocol(CommandProtocol):
    def __init__(self, manager):
        CommandProtocol.__init__(self)

        self.manager = manager

    def connectionMade(self):
        self.manager.protocol = self
        self.send_message('iam', self.manager.name)

    def connectionLost(self, reason):
        self.manager.protocol = None

    def handle_connected_state(self, arg):
        arg = parse_state(arg)
        if not arg:
            self.drop_with_error('Malformed state attributes')
            return

        paused, position, name = arg

        self.manager.update_global_state(paused, position, name)

    def send_state(self, paused, position):
        self.send_message('state', ('paused' if paused else 'playing'), int(position*100))


    states = dict(
        connected = dict(
            state = 'handle_connected_state',
            seek = 'handle_connected_seek',
            #ping = 'handle_connected_ping',
        ),
    )
    initial_state = 'connected'

class SyncClientFactory(ReconnectingClientFactory):
    def __init__(self, manager):
        self.manager = manager

    def buildProtocol(self, addr):
        return SyncClientProtocol(self.manager)


class Manager(object):
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name

        self.player = None
        self.protocol = None

        self.ask_delayed = None
        self.send_delayed = None

        self.global_paused = True
        self.global_position = 0.0

        self.player_paused = True
        self.player_position = 0.0

    def start(self):
        factory = SyncClientFactory(self)
        reactor.connectTCP(self.host, self.port, factory)
        self.running = True
        self.schedule_ask_player()
        self.schedule_send_status()

    def stop(self):
        if self.protocol:
            self.protocol.drop()
        if self.player:
            self.player.drop()
        self.running = False

    def schedule_ask_player(self, when=0.2):
        if self.ask_delayed and self.ask_delayed.active():
            self.ask_delayed.reset(when)
        else:
            self.ask_delayed = reactor.callLater(when, self.ask_player)

    def ask_player(self):
        if not self.running:
            return
        if self.player:
            self.player.send_get_position()
            self.player.send_get_paused()
        self.schedule_ask_player()

    def schedule_send_status(self, when=1):
        if self.send_delayed and self.send_delayed.active():
            self.send_delayed.reset(when)
        else:
            self.send_delayed = reactor.callLater(when, self.send_status)

    def send_status(self):
        if not self.running:
            return
        if self.protocol:
            self.protocol.send_state(self.player_paused, self.player_position)
        self.schedule_send_status()

    
    def update_player_position(self, value):
        self.player_position = value

    def update_player_paused(self, value):
        old = self.player_paused
        self.player_paused = value
        if old != value and self.global_paused != value:
            self.send_status()

    def update_global_state(self, paused, position, name):
        self.global_paused = paused
        self.global_position = position
        if self.player:
            changed = False
            if abs(self.player_position - position) > 4:
                self.player.send_set_position(position)
                changed = True
            if self.player_paused != paused:
                self.player.send_set_paused(paused)
                changed = True
            if changed:
                self.schedule_ask_player()

