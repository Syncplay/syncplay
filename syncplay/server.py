#coding:utf8

from collections import deque
import re
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
RE_NAME = re.compile('^(.*?)(\d*)$')

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
        name = args[0].strip()
        if not args:
            self.drop_with_error('Invalid nickname')
            return
        self.factory.add_watcher(self, args[0])
        self.change_state('connected')

    @arg_count(4)
    def handle_connected_state(self, args):
        args = parse_state(args)
        if not args:
            self.drop_with_error('Malformed state attributes')
            return

        counter, ctime, paused, position, _ = args

        self.factory.update_state(self, counter, ctime, paused, position)

    @arg_count(3)
    def handle_connected_seek(self, args):
        counter, ctime, position = args
        try:
            counter = int(counter)
            ctime = int(ctime)
            position = int(position)
        except ValueError:
            self.drop_with_error('Invalid arguments')

        ctime /= 1000.0
        position /= 1000.0

        self.factory.seek(self, counter, ctime, position)

    @arg_count(2)
    def handle_connected_pong(self, args):
        value, ctime = args
        try:
            ctime = int(ctime)
        except ValueError:
            self.drop_with_error('Invalid arguments')

        ctime /= 100000.0

        self.factory.pong_received(self, value, ctime)

    @arg_count(1)
    def handle_connected_playing(self, args):
        self.factory.playing_received(self, args[0])

    def __hash__(self):
        return hash('|'.join((
            self.transport.getPeer().host,
            str(id(self)),
        )))


    def send_state(self, counter, ctime, paused, position, who_last_changed):
        ctime = int(ctime*1000)
        paused = 'paused' if paused else 'playing'
        position = int(position*1000)
        if who_last_changed is None:
            self.send_message('state', counter, ctime, paused, position)
        else:
            self.send_message('state', counter, ctime, paused, position, who_last_changed)

    def send_seek(self, ctime, position, who_seeked):
        self.send_message('seek', int(ctime*1000), int(position*1000), who_seeked)

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

    def send_hello(self, name):
        self.send_message('hello', name)


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
        self.active = True

        self.paused = True
        self.position = 0
        self.filename = None
        self.max_position = 0
        self.last_update = None
        self.last_update_sent = None

        self.ping = None
        self.time_offset = 0
        self.time_offset_data = []
        self.pings_sent = dict()
        self.last_ping_received = time.time()

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
        allnames = (watcher.name.lower() for watcher in self.watchers.itervalues())
        while name.lower() in allnames:
            m = RE_NAME.match(name)
            name, number = m.group(1), m.group(2)
            if number:
                number = str(int(number)+1)
            else:
                number = '1'
            name += number

        watcher = WatcherInfo(watcher_proto, name)
        if self.watchers:
            watcher.max_position = min(w.max_position for w in self.watchers.itervalues())
        self.watchers[watcher_proto] = watcher
        for receiver in self.watchers.itervalues():
            if receiver == watcher:
                continue
            receiver.watcher_proto.send_joined(name)
            watcher_proto.send_present(receiver.name, receiver.filename)
        watcher_proto.send_hello(name)
        self.send_state_to(watcher)
        self.send_ping_to(watcher)

    def remove_watcher(self, watcher_proto):
        watcher = self.watchers.pop(watcher_proto, None)
        if not watcher:
            return
        watcher.active = False
        for receiver in self.watchers.itervalues():
            if receiver != watcher:
                receiver.watcher_proto.send_left(watcher.name)
        if self.pause_change_by == watcher:
            self.pause_change_time = None
            self.pause_change_by = None
        if not self.watchers:
            self.paused = True 

    def update_state(self, watcher_proto, counter, ctime, paused, position):
        watcher = self.watchers.get(watcher_proto)
        if not watcher:
            return

        curtime = time.time()
        ctime += watcher.time_offset
        if not paused:
            position += curtime - ctime

        watcher.paused = paused
        watcher.position = position
        watcher.max_position = max(position, watcher.max_position)
        watcher.last_update = curtime
        watcher.counter = counter
        
        pause_changed = paused != self.paused

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

    def seek(self, watcher_proto, counter, ctime, position):
        watcher = self.watchers.get(watcher_proto)
        if not watcher:
            return

        #print watcher.name, 'seeked to', position
        curtime = time.time()
        ctime += watcher.time_offset
        position += curtime - ctime
        watcher.counter = counter

        for receiver in self.watchers.itervalues():
            position2 = position
            receiver.max_position = position2
            if receiver == watcher:
                self.send_state_to(receiver, position, curtime)
            else:
                receiver.watcher_proto.send_seek(curtime-receiver.time_offset, position2, watcher.name)

    def send_state_to(self, watcher, position=None, curtime=None):
        if position is None:
            position = self.find_position()
        if curtime is None:
            curtime = time.time()

        ctime = curtime - watcher.time_offset

        if self.pause_change_by:
            watcher.watcher_proto.send_state(watcher.counter, ctime, self.paused, position, self.pause_change_by.name)
        else:
            watcher.watcher_proto.send_state(watcher.counter, ctime, self.paused, position, None)

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

    def pong_received(self, watcher_proto, value, ctime):
        watcher = self.watchers.get(watcher_proto)
        if not watcher:
            return

        ping_time = watcher.pings_sent.pop(value, None)
        if ping_time is not None:
            curtime = time.time()
            watcher.last_ping_received = curtime
            watcher.ping = ping = (curtime - ping_time)/2

            if watcher.time_offset_data is not None:
                time_offset = curtime - (ctime + ping)
                watcher.time_offset_data.append((ping, time_offset))

                if len(watcher.time_offset_data) > 1:
                    pmin = min(p for p,_ in watcher.time_offset_data)
                    pmax = max(p for p,_ in watcher.time_offset_data) - pmin
                    psum, pweights = 0, 0
                    for ping, offset in watcher.time_offset_data:
                        ping = 1-((ping-pmin)/pmax)
                        pweights += ping
                        psum += ping*offset
                    watcher.time_offset = psum/pweights
                else:
                    watcher.time_offset = time_offset

                if len(watcher.time_offset_data) > 20:
                    watcher.time_offset_data = None

            #print watcher.name, 'last ping', watcher.ping, 'time offset %.6f' % watcher.time_offset

    def send_ping_to(self, watcher):
        if not watcher.active:
            return

        chars = None
        while not chars or chars in watcher.pings_sent:
            chars = random_chars()

        curtime = time.time()
        if curtime - watcher.last_ping_received > 60:
            watcher.watcher_proto.drop()
            return

        watcher.watcher_proto.send_ping(chars)
        watcher.pings_sent[chars] = time.time()

        if len(watcher.pings_sent) > 30:
            watcher.pings_sent.pop(min((time, key) for key, time in watcher.pings_sent.iteritems())[1])

        self.schedule_send_ping(watcher)

    def schedule_send_ping(self, watcher, when=1):
        reactor.callLater(when, self.send_ping_to, watcher)

    def playing_received(self, watcher_proto, filename):
        watcher = self.watchers.get(watcher_proto)
        if not watcher:
            return

        watcher.filename = filename

        for receiver in self.watchers.itervalues():
            if receiver != watcher:
                receiver.watcher_proto.send_playing(watcher.name, filename)

