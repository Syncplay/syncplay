#coding:utf8

import time
import random

from twisted.internet import reactor
from twisted.internet.protocol import Factory

from .network_utils import CommandProtocol
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

    def handle_init_iam(self, arg):
        self.factory.add_watcher(self, arg.strip())
        self.change_state('connected')

    def handle_connected_state(self, arg):
        arg = parse_state(arg)
        if not arg:
            self.drop_with_error('Malformed state attributes')
            return

        paused, position, _ = arg

        self.factory.update_state(self, paused, position)

    def handle_connected_seek(self, arg):
        try:
            position = int(arg)
        except ValueError:
            self.drop_with_error('Invalid position numeral')

        position /= 100.0

        self.factory.seek(self, position)

    def handle_connected_pong(self, arg):
        self.factory.pong_received(self, arg)

    def __hash__(self):
        return hash('|'.join((
            self.transport.getPeer().host,
            str(id(self)),
        )))


    def send_state(self, paused, position, who_last_changed):
        self.send_message('state', ('paused' if paused else 'playing'), int(position*100), who_last_changed)

    def send_seek(self, position, who_seeked):
        self.send_message('seek', int(position*100), who_seeked)

    def send_ping(self, value):
        self.send_message('ping', value)


    states = dict(
        init = dict(
            iam = 'handle_init_iam',
        ),
        connected = dict(
            state = 'handle_connected_state',
            seek = 'handle_connected_seek',
            pong = 'handle_connected_pong',
        ),
    )
    initial_state = 'init'


class WatcherInfo(object):
    def __init__(self, watcher_proto, name):
        self.watcher_proto = watcher_proto
        self.name = name

        self.position = 0
        self.max_position = 0
        self.last_update = None
        self.last_update_sent = None

        self.ping = None
        self.last_ping_time = None
        self.last_ping_value = None

    def update_position(self, position):
        if self.ping is not None:
            position += self.ping
        self.position = position
        self.max_position = max(position, self.max_position)
        self.last_update = time.time()


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
        self.watchers[watcher_proto] = watcher
        self.send_state_to(watcher)
        self.schedule_send_ping(watcher_proto)
        # send info someone joined

    def remove_watcher(self, watcher_proto):
        watcher = self.watchers.pop(watcher_proto, None)
        if self.pause_change_by == watcher:
            self.pause_change_by = None
        # send info someone quit

    def update_state(self, watcher_proto, paused, position):
        watcher = self.watchers.get(watcher_proto)
        if not watcher:
            return

        watcher.update_position(position)
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

    def seek(self, watcher_proto, position):
        #TODO
        #for receiver in self.watchers.itervalues():
        pass

    def send_state_to(self, watcher, position=None, curtime=None):
        if position is None:
            position = self.find_position()
        if curtime is None:
            curtime = time.time()

        if watcher.ping is not None:
            position += watcher.ping

        if self.pause_change_by:
            watcher.watcher_proto.send_state(self.paused, position, self.pause_change_by.name)
        else:
            watcher.watcher_proto.send_state(self.paused, position, None)

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
            print watcher.name, watcher.ping

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

