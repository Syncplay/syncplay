#coding:utf8

import time

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory

from .network_utils import CommandProtocol
from .utils import parse_state


class SyncClientProtocol(CommandProtocol):
    def __init__(self, manager):
        CommandProtocol.__init__(self)

        self.manager = manager

    def connectionMade(self):
        self.send_message('iam', self.manager.name)
        self.manager.init_protocol(self)

    def connectionLost(self, reason):
        self.manager.protocol = None

    def handle_connected_state(self, arg):
        arg = parse_state(arg)
        if not arg:
            self.drop_with_error('Malformed state attributes')
            return

        counter, paused, position, name = arg

        self.manager.update_global_state(counter, paused, position, name)

    def handle_connected_ping(self, arg):
        self.send_message('pong', arg)

    def send_state(self, counter, paused, position):
        self.send_message('state', counter, ('paused' if paused else 'playing'), int(position*100))


    states = dict(
        connected = dict(
            state = 'handle_connected_state',
            seek = 'handle_connected_seek',
            ping = 'handle_connected_ping',
        ),
    )
    initial_state = 'connected'

class SyncClientFactory(ClientFactory):
    def __init__(self, manager):
        self.manager = manager
        self.retry = True

    def buildProtocol(self, addr):
        return SyncClientProtocol(self.manager)

    def startedConnecting(self, connector):
        destination = connector.getDestination()
        print 'Connecting to %s:%d' % (destination.host, destination.port)

    def clientConnectionLost(self, connector, reason):
        if self.retry:
            print 'Connection lost, reconnecting'
            connector.connect()
        else:
            print 'Disconnected'

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed'
        self.manager.stop()

    def stop_retrying(self):
        self.retry = False


class Manager(object):
    def __init__(self, host, port, name, make_player):
        self.host = host
        self.port = port
        self.name = name

        self.protocol_factory = None
        self.protocol = None
        self.send_delayed = None
        self.global_paused = True
        self.global_position = 0.0
        self.last_global_update = None
        self.counter = 0

        self.player = None
        self.ask_delayed = None
        self.player_paused = True
        self.player_paused_at = 0.0
        self.player_position = 0.0
        self.last_player_update = None
        self.player_speed_fix = False

        self.make_player = make_player
        self.running = False


    def start(self):
        if self.running:
            return
        self.protocol_factory = SyncClientFactory(self)
        reactor.connectTCP(self.host, self.port, self.protocol_factory)
        self.running = True
        reactor.run()

    def stop(self):
        if not self.running:
            return
        self.running = False
        if self.protocol_factory:
            self.protocol_factory.stop_retrying()
        if self.protocol:
            self.protocol.drop()
        if self.player:
            self.player.drop()
        reactor.callLater(0.1, reactor.stop)


    def get_player_position(self):
        if not self.last_player_update:
            return None
        position = self.player_position
        if not self.player_paused:
            position += time.time() - self.last_player_update
        return position

    def get_global_position(self):
        if not self.last_global_update:
            return None
        position = self.global_position
        if not self.global_paused:
            position += time.time() - self.last_global_update
        return position


    def init_player(self, player):
        self.player = player
        if self.last_global_update:
            self.player.send_set_position(self.get_global_position())
            self.player.send_set_paused(self.global_paused)
        self.schedule_ask_player()

    def init_protocol(self, protocol):
        self.protocol = protocol
        self.schedule_send_status()
        self.make_player()


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
        self.counter += 1
        if self.protocol:
            self.protocol.send_state(self.counter, self.player_paused, self.player_position)
        self.schedule_send_status()

    
    def update_player_position(self, value):
        self.player_position = value
        self.last_player_update = time.time()

        if not self.global_paused:
            diff = self.get_global_position() - value
            if 0.6 <= abs(diff) <= 4:
                #print 'server is %0.2fs ahead of client' % diff
                if diff > 0:
                    speed = 1.5
                else:
                    speed = 0.75
                #print 'fixing at speed %0.2f' % speed
                if not self.player_speed_fix:
                    self.player.send_set_speed(speed)
                    self.player_speed_fix = True
            elif self.player_speed_fix:
                self.player.send_set_speed(1)
                self.player_speed_fix = False

        if not self.player_paused and self.player_paused_at is not None and value >= self.player_paused_at:
            self.player.send_set_paused(True)
            self.schedule_ask_player()


    def update_player_paused(self, value):
        old = self.player_paused
        self.player_paused = value
        if not value:
            self.player_paused_at = None
        if old != value and self.global_paused != value:
            self.send_status()

    def update_global_state(self, counter, paused, position, name):
        curtime = time.time()
        self.global_paused = paused
        self.global_position = position
        updated_before = bool(self.last_global_update)
        self.last_global_update = curtime

        if not self.player:
            return

        if not updated_before:
            self.player.send_set_position(position)
            self.player.send_set_paused(paused)
        elif not (self.counter and counter < self.counter):
            diff = self.get_player_position() - position
            if self.last_player_update is not None:
                diff += curtime - self.last_player_update
            if abs(diff) > 4:
                self.player.send_set_position(position)
            if self.player_paused and not paused:
                self.player_paused_at = None
                self.player.send_set_paused(False)
            elif paused and not self.player_paused:
                self.player_paused_at = position
                if diff < 0:
                    self.player.send_set_paused(True)

