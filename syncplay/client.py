#coding:utf8

import time
import re

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory

from .network_utils import (
    arg_count,
    CommandProtocol,
)
from .utils import (
    format_time,
    parse_state,
)


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

    @arg_count(1)
    def handle_init_hello(self, args):
        print 'Connected as', args[0]
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

    @arg_count(4, 5)
    def handle_connected_state(self, args):
        args = parse_state(args)
        if not args:
            self.drop_with_error('Malformed state attributes')
            return

        counter, ctime, paused, position, name = args

        self.manager.update_global_state(counter, ctime, paused, position, name)

    @arg_count(3)
    def handle_connected_seek(self, args):
        ctime, position, who = args
        try:
            ctime = int(ctime)
            position = int(position)
        except ValueError:
            self.drop_with_error('Invalid arguments')

        ctime /= 1000.0
        position /= 1000.0

        self.manager.seek(ctime, position, who)

    @arg_count(1)
    def handle_connected_ping(self, args):
        self.send_message('pong', args[0], int(time.time()*100000))

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


    def send_state(self, counter, ctime, paused, position):
        self.send_message('state', counter, int(ctime*1000), ('paused' if paused else 'playing'), int(position*1000))

    def send_seek(self, counter, ctime, position):
        self.send_message('seek', counter, int(ctime*1000), int(position*1000))

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
        self.counter_recv = 0

        self.player = None
        self.ask_delayed = None
        self.player_paused = True
        self.player_paused_at = 0.0
        self.player_position = 0.0
        self.last_player_update = None
        self.player_speed_fix = False
        self.player_filename = None
        self.player_position_before_last_seek = 0
        
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

    def send_status(self, force = False):
        if not (self.running and self.protocol):
            return
        self.schedule_send_status()
        if self.counter > self.counter_recv and not force:
            return
        self.counter += 1
        curtime = time.time()
        position = self.player_position
        if not self.player_paused:
            position += curtime - self.last_player_update
        if self.protocol:
            self.protocol.send_state(self.counter, curtime, self.player_paused, self.player_position)

    def send_seek(self):
        if not (self.running and self.protocol):
            return
        self.counter += 10
        self.protocol.send_seek(self.counter, time.time(), self.player_position)
        print 'You seeked to', format_time(self.player_position)
        
    def send_filename(self):
        if self.protocol and self.player_filename:
            self.protocol.send_playing(self.player_filename)

    def exectue_seek_cmd(self, seek_type, minutes, seconds):
        self.player_position_before_last_seek = self.player_position

        if seek_type == 's':
            if seconds <> None:
                seconds = int(seconds)
            else:
                seconds = 0
            if minutes <> None:
                seconds += int(minutes) * 60
            self.player.set_position(seconds)
        else: #seek_type s+
            if seconds <> None:
                seconds = int(seconds)
            else:
                seconds = 20
            if minutes <> None:
                seconds += int(minutes) * 60
            else:
                seconds += 60
            self.player.set_position(self.player_position+seconds)
            
    def execute_command(self, data):
        RE_SEEK = re.compile("^(s[+s]?) ?(-?\d+)?([^0-9](\d+))?$")
        matched_seek = RE_SEEK.match(data)
        if matched_seek :
            self.exectue_seek_cmd(matched_seek.group(1), matched_seek.group(2), matched_seek.group(4))
        elif data == "r":
            self.counter += 1
            tmp_pos = self.player_position
            self.protocol.send_seek(self.counter, time.time(), self.player_position_before_last_seek)
            self.player_position_before_last_seek = tmp_pos
        elif data == "p":
            self.player.set_paused(not self.player_paused)

    def update_player_status(self, paused, position):
        self.status_ask_received += 1
        if self.status_ask_received < self.status_ask_sent:
            return

        old_paused = self.player_paused
        self.player_paused = paused
        self.player_position = position
        self.last_player_update = time.time()
        diff = position - self.get_global_position()
        if old_paused and not paused:
            self.player_paused_at = None
        if old_paused != paused and self.global_paused != paused:
            self.send_status(True)
            if paused:
                print "You have paused"
                if(diff > 0):
                    self.player.set_position(self.get_global_position())
                    self.ask_player()
            else:
                print "You have resumed"
            
        if not (self.global_paused or self.seek_sent_wait):
            if (0.4 if self.player_speed_fix else 0.6) <= diff <= 4:
                #print 'client is %0.2fs ahead of server, slowing down' % diff
                if not self.player_speed_fix:
                    self.player.set_speed(0.75)
                    self.player_speed_fix = True
            else:
                if self.player_speed_fix:
                    #print 'resetting speed'
                    self.player.set_speed(1)
                    self.player_speed_fix = False
        if abs(diff) > 8:# and not self.seek_sent_wait:
            self.send_seek()
            self.seek_sent_wait = True

        if not paused and self.player_paused_at is not None and position >= self.player_paused_at:
            #print 'Pausing %0.2fs after pause point' % (position - self.player_paused_at)
            self.player.set_paused(True)
            self.ask_player()

    def update_filename(self, filename):
        filename = unicode(filename, errors='replace')
        self.player_filename = filename.encode('ascii','replace')

        self.send_filename()

    def update_global_state(self, counter, ctime, paused, position, name):
        self.counter_recv = max(self.counter_recv, counter)
        counter_valid = self.counter and counter >= self.counter

        curtime = time.time()
        updated_before = bool(self.last_global_update)

        if updated_before and not counter_valid:
            return

        if not paused:
            position += curtime - ctime
        self.global_paused = paused
        self.global_position = position
        self.global_who_changed = name
        self.last_global_update = curtime

        if not self.player:
            return

        changed = False
        self.seek_sent_wait = False

        if not updated_before:
            self.player.set_position(position)
            self.player.set_paused(paused)
            changed = True

        if counter_valid:
            diff = self.get_player_position() - position
            if abs(diff) > 4:
                self.player.set_position(position)
                #self.player.set_paused(True)
                print "Rewind due to time difference"
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
            self.global_noted_pause_change = paused

        if changed:
            self.ask_player()

    def seek(self, ctime, position, who):
        curtime = time.time()
        position += curtime - ctime
        self.global_position = position
        self.last_global_update = curtime
        if self.player:
            self.player_position_before_last_seek = self.player_position
            self.player.set_position(position)
            self.ask_player()
        print who, 'seeked to', format_time(position)


