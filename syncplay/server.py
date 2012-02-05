#coding:utf8

import time
import random

from twisted.internet import reactor
from twisted.internet.protocol import Factory

from .network_utils import (
    arg_count,
    CommandProtocol,
)
from .utils import parse_state

random.seed()

CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def random_chars():
    return ''.join(random.choice(CHARS) for _ in xrange(10))

class SyncServerProtocol(CommandProtocol):
    def __init__(self, factory):
        CommandProtocol.__init__(self)

        self.factory = factory

    def connectionLost(self, reason):
        self.factory.remove_watcher(self)

    def handle_init_iam(self, args):
        if not len(args) == 1:
            self.drop_with_error('Invalid arguments')
            return
        self.factory.add_watcher(self, args[0])
        self.change_state('connected')

    @arg_count(3)
    def handle_connected_state(self, args):
        args = parse_state(args)
        if not args:
            self.drop_with_error('Malformed state attributes')
            return

        counter, paused, position, _ = args

        self.factory.update_state(self, counter, paused, position)

    @arg_count(2)
    def handle_connected_seek(self, args):
        try:
            counter = int(args[0])
            position = int(args[1])
        except ValueError:
            self.drop_with_error('Invalid arguments')

        position /= 1000.0

        self.factory.seek(self, counter, position)

    @arg_count(1)
    def handle_connected_pong(self, args):
        self.factory.pong_received(self, args[0])

    @arg_count(1)
    def handle_connected_playing(self, args):
        self.factory.playing_received(self, args[0])

    def __hash__(self):
        return hash('|'.join((
            self.transport.getPeer().host,
            str(id(self)),
        )))


    def send_state(self, counter, paused, position, who_last_changed):
        paused = 'paused' if paused else 'playing'
        position = int(position*1000)
        if who_last_changed is None:
            self.send_message('state', counter, paused, position)
        else:
            self.send_message('state', counter, paused, position, who_last_changed)

    def send_seek(self, position, who_seeked):
        self.send_message('seek', int(position*1000), who_seeked)

    def send_ping(self, value):
        self.send_message('ping', value)

    def send_playing(self, who, what):
        self.send_message('playing', who, what)

    def send_present(self, who, what):
        if what:
            self.send_message('present', who, what)
        else:
            self.send_message('present', who)

    def send_joined(self, who):
        self.send_message('joined', who)

    def send_left(self, who):
        self.send_message('left', who)

    def send_hello(self):
        self.send_message('hello')


    states = dict(
        init = dict(
            iam = 'handle_init_iam',
        ),
        connected = dict(
            state = 'handle_connected_state',
            seek = 'handle_connected_seek',
            pong = 'handle_connected_pong',
            playing = 'handle_connected_playing',
        ),
    )
    initial_state = 'init'


class WatcherInfo(object):
    def __init__(self, watcher_proto, name):
        self.watcher_proto = watcher_proto
        self.name = name

        self.position = 0
        self.filename = None
        self.max_position = 0
        self.last_update = None
        self.last_update_sent = None

        self.ping = None
        self.last_ping_time = None
        self.last_ping_value = None

        self.counter = 0


class SyncFactory(Factory):
    def __init__(self, min_pause_lock = 3, update_time_limit = 1):
        self.watchers = dict()

        self.paused = True
        self.pause_change_time = None
        self.pause_change_by = None

        self.min_pause_lock = min_pause_lock
        self.update_time_limit = update_time_limit

    def buildProtocol(self, addr):
        return SyncServerProtocol(self)


    def add_watcher(self, watcher_proto, name):
        watcher = WatcherInfo(watcher_proto, name)
        if self.watchers:
            watcher.max_position = min(w.max_position for w in self.watchers.itervalues())
        self.watchers[watcher_proto] = watcher
        for receiver in self.watchers.itervalues():
            if receiver == watcher:
                continue
            receiver.watcher_proto.send_joined(name)
            watcher_proto.send_present(receiver.name, receiver.filename)
        watcher_proto.send_hello()
        self.send_state_to(watcher)
        self.schedule_send_ping(watcher_proto)

    def remove_watcher(self, watcher_proto):
        watcher = self.watchers.pop(watcher_proto, None)
        for receiver in self.watchers.itervalues():
            if receiver != watcher:
                receiver.watcher_proto.send_left(watcher.name)
        if self.pause_change_by == watcher:
            self.pause_change_time = None
            self.pause_change_by = None
        if not self.watchers:
            self.paused = True 
        # send info someone quit

    def update_state(self, watcher_proto, counter, paused, position):
        watcher = self.watchers.get(watcher_proto)
        if not watcher:
            return

        if not paused and watcher.ping is not None:
            position += watcher.ping
        watcher.position = position
        watcher.max_position = max(position, watcher.max_position)
        watcher.last_update = time.time()
        watcher.counter = counter

        pause_changed = paused != self.paused

        curtime = time.time()
        if pause_changed and (
            not self.pause_change_by or
            self.pause_change_by == watcher or
            (curtime-self.pause_change_time) > self.min_pause_lock
        ):
            self.paused = not self.paused
            self.pause_change_time = curtime
            self.pause_change_by = watcher
        else:
            pause_changed = False

        position = self.find_position()
        for receiver in self.watchers.itervalues():
            if (
                receiver == watcher or
                pause_changed or
                (curtime-receiver.last_update_sent) > self.update_time_limit
            ):
                self.send_state_to(receiver, position, curtime)

    def seek(self, watcher_proto, counter, position):
        watcher = self.watchers.get(watcher_proto)
        if not watcher:
            return

        #print watcher.name, 'seeked to', position
        if not self.paused and watcher.ping is not None:
            position += watcher.ping
        watcher.counter = counter

        for receiver in self.watchers.itervalues():
            if not self.paused and receiver.ping is not None:
                position2 = position + receiver.ping
            receiver.max_position = position2
            if receiver == watcher:
                # send_state_to modifies by ping already...
                self.send_state_to(receiver, position)
            else:
                receiver.watcher_proto.send_seek(position2, watcher.name)

    def send_state_to(self, watcher, position=None, curtime=None):
        if position is None:
            position = self.find_position()
        if curtime is None:
            curtime = time.time()

        if not self.paused and watcher.ping is not None:
            position += watcher.ping

        if self.pause_change_by:
            watcher.watcher_proto.send_state(watcher.counter, self.paused, position, self.pause_change_by.name)
        else:
            watcher.watcher_proto.send_state(watcher.counter, self.paused, position, None)

        watcher.last_update_sent = curtime

    def find_position(self):
        curtime = time.time()
        try:
            return min(
                max(watcher.max_position, watcher.position + (0 if self.paused else curtime-watcher.last_update))
                for watcher in self.watchers.itervalues()
                if watcher.last_update
            )
        except ValueError:
            #min() arg is an empty sequence
            return 0.0

    def pong_received(self, watcher_proto, value):
        watcher = self.watchers.get(watcher_proto)
        if not watcher:
            return

        if watcher.last_ping_value == value:
            ping = (time.time() - watcher.last_ping_time)/2
            if watcher.ping is None:
                watcher.ping = ping
            else:
                watcher.ping = watcher.ping*0.6 + ping*0.4

        self.schedule_send_ping(watcher_proto)

    def send_ping_to(self, watcher_proto):
        watcher = self.watchers.get(watcher_proto)
        if not watcher:
            return
        chars = random_chars()
        watcher.last_ping_time = time.time()
        watcher.last_ping_value = chars
        watcher.watcher_proto.send_ping(chars)

    def schedule_send_ping(self, watcher_proto, when=1):
        reactor.callLater(when, self.send_ping_to, watcher_proto)

    def playing_received(self, watcher_proto, filename):
        watcher = self.watchers.get(watcher_proto)
        if not watcher:
            return

        watcher.filename = filename

        for receiver in self.watchers.itervalues():
            if receiver != watcher:
                receiver.watcher_proto.send_playing(watcher.name, filename)

