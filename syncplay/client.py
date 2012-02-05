#coding:utf8

import time

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory

from .network_utils import (
    arg_count,
    CommandProtocol,
)
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

    def handle_error(self, args):
        self.manager.stop()
        CommandProtocol.handle_error(self, args)

    @arg_count(0)
    def handle_init_hello(self, args):
        self.change_state('connected')

    @arg_count(1, 2)
    def handle_init_present(self, args):
        if len(args) == 2:
            who, what = args
        else:
            who, what = args[0], None
        if what:
            print '%s is present and is playing %s' % (who, what)
        else:
            print '%s is present' % who

    @arg_count(3, 4)
    def handle_connected_state(self, args):
        args = parse_state(args)
        if not args:
            self.drop_with_error('Malformed state attributes')
            return

        counter, paused, position, name = args

        self.manager.update_global_state(counter, paused, position, name)

    @arg_count(2)
    def handle_connected_seek(self, args):
        position, who = args
        try:
            position = int(position)
        except ValueError:
            self.drop_with_error('Invalid arguments')

        position /= 1000.0

        self.manager.seek(position, who)

    @arg_count(1)
    def handle_connected_ping(self, args):
        self.send_message('pong', args[0])

    @arg_count(2)
    def handle_connected_playing(self, args):
        who, what = args
        print '%s is playing %s' % (who, what)

    @arg_count(1)
    def handle_connected_joined(self, args):
        print '%s joined' % args[0]

    @arg_count(1)
    def handle_connected_left(self, args):
        print '%s left' % args[0]


    def send_state(self, counter, paused, position):
        self.send_message('state', counter, ('paused' if paused else 'playing'), int(position*1000))

    def send_seek(self, counter, position):
        self.send_message('seek', counter, int(position*1000))

    def send_playing(self, filename):
        self.send_message('playing', filename)


    states = dict(
        init = dict(
            present = 'handle_init_present',
            hello = 'handle_init_hello',
        ),
        connected = dict(
            state = 'handle_connected_state',
            seek = 'handle_connected_seek',
            ping = 'handle_connected_ping',
            playing = 'handle_connected_playing',
            joined = 'handle_connected_joined',
            left = 'handle_connected_left',
        ),
    )
    initial_state = 'init'

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
            reactor.callLater(0.1, connector.connect)
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
        self.global_who_paused = None
        self.global_noted_pause_change = None
        self.last_global_update = None
        self.counter = 0

        self.player = None
        self.ask_delayed = None
        self.player_paused = True
        self.player_paused_at = 0.0
        self.player_position = 0.0
        self.last_player_update = None
        self.player_speed_fix = False
        self.player_filename = None

        self.seek_sent_wait = False
        self.status_ask_sent = 0
        self.status_ask_received = 0

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
            return 0.0
        position = self.player_position
        if not self.player_paused:
            position += time.time() - self.last_player_update
        return position

    def get_global_position(self):
        if not self.last_global_update:
            return 0.0
        position = self.global_position
        if not self.global_paused:
            position += time.time() - self.last_global_update
        return position


    def init_player(self, player):
        self.player = player
        if self.last_global_update:
            self.player.set_position(self.get_global_position())
            self.player.set_paused(self.global_paused)
        self.schedule_ask_player()

    def init_protocol(self, protocol):
        self.protocol = protocol
        self.schedule_send_status()
        self.send_filename()
        if self.make_player:
            self.make_player(self)
            self.make_player = None


    def schedule_ask_player(self, when=0.2):
        if self.ask_delayed and self.ask_delayed.active():
            self.ask_delayed.reset(when)
        else:
            self.ask_delayed = reactor.callLater(when, self.ask_player)

    def ask_player(self):
        if not self.running:
            return
        if self.player:
            self.status_ask_sent += 1
            self.player.ask_for_status()
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

    def send_seek(self):
        if not (self.running and self.protocol):
            return
        self.counter += 1
        self.protocol.send_seek(self.counter, self.player_position)

    def send_filename(self):
        if self.protocol and self.player_filename:
            self.protocol.send_playing(self.player_filename)


    def update_player_status(self, paused, position):
        self.status_ask_received += 1
        if self.status_ask_received < self.status_ask_sent:
            return

        old_paused = self.player_paused
        self.player_paused = paused
        self.player_position = position
        self.last_player_update = time.time()

        if old_paused and not paused:
            self.player_paused_at = None
        if old_paused != paused and self.global_paused != paused:
            self.send_status()

        if not (self.global_paused or self.seek_sent_wait):
            diff = position - self.get_global_position()
            if (0.4 if self.player_speed_fix else 0.6) <= diff <= 4:
                #print 'server is %0.2fs ahead of client, slowing down' % diff
                if not self.player_speed_fix:
                    self.player.set_speed(0.75)
                    self.player_speed_fix = True
            else:
                if self.player_speed_fix:
                    #print 'resetting speed'
                    self.player.set_speed(1)
                    self.player_speed_fix = False
                if abs(diff) > 8:
                    self.send_seek()

        if not paused and self.player_paused_at is not None and position >= self.player_paused_at:
            #print 'Pausing %0.2fs after pause point' % (position - self.player_paused_at)
            self.player.set_paused(True)
            self.ask_player()

    def update_filename(self, filename):
        self.player_filename = filename
        self.send_filename()

    def update_global_state(self, counter, paused, position, name):
        curtime = time.time()
        self.global_paused = paused
        self.global_position = position
        self.global_who_changed = name
        updated_before = bool(self.last_global_update)
        self.last_global_update = curtime

        if not self.player:
            return

        changed = False
        if not updated_before:
            self.player.set_position(position)
            self.player.set_paused(paused)
            changed = True
        elif not (self.counter and counter < self.counter):
            diff = self.get_player_position() - position
            if self.last_player_update is not None:
                diff += curtime - self.last_player_update
            if abs(diff) > 4:
                self.player.set_position(position)
                changed = True
            if self.player_paused and not paused:
                self.player_paused_at = None
                self.player.set_paused(False)
                changed = True
                if self.global_noted_pause_change != paused:
                    print '%s unpaused' % name
            elif paused and not self.player_paused:
                self.player_paused_at = position
                if self.global_noted_pause_change != paused:
                    print '%s paused' % name
                if diff < 0:
                    self.player.set_paused(True)
                    changed = True
                #else:
                #    print 'Not pausing now'

        self.global_noted_pause_change = paused
        self.seek_sent_wait = False
        if changed:
            self.ask_player()

    def seek(self, position, who):
        self.global_position = position
        if self.player:
            self.player.set_position(position)
            self.ask_player()

        position = int(position*1000)
        seconds, mseconds = divmod(position, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        print '%s seeked to %02d:%02d:%02d.%03d' % (
            who, hours, minutes, seconds, mseconds
        )


