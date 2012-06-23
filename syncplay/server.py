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
        name = re.sub('[^\w]','',args[0])
        if not name:
            self.drop_with_error('Invalid nickname')
            return
        self.factory.add_watcher(self, name)
        self.change_state('connected')

    @arg_count(1)
    def handle_connected_room(self, args):
        watcher = self.factory.watchers.get(self)
        old_room = watcher.room
        watcher.room = str(re.sub('[^\w]','',args[0]))
        self.factory.broadcast(watcher, lambda receiver: receiver.watcher_proto.send_room(watcher.name,watcher.room))
        if not watcher.room in self.factory.paused: 
            self.factory.paused[watcher.room] = True
        self.factory.remove_room_if_empty(old_room)
        watcher = self.factory.watchers.get(self)

    @arg_count(4)
    def handle_connected_state(self, args):
        args = parse_state(args)
        if not args:
            self.drop_with_error('Malformed state attributes')
            return
        counter, ctime, paused, position, _ = args
        self.factory.update_state(self, counter, ctime, paused, position)
    
    @arg_count(0)
    def handle_connected_list(self, args):
        watcher = self.factory.watchers.get(self)
        for w in self.factory.watchers.itervalues():
                if w == watcher:
                    continue
                self.send_present(w.name, w.room, w.filename)
            
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

    def send_playing(self, who, where, what):
        self.send_message('playing', who, where, what)

    def send_room(self, who, where):
        self.send_message('room', who, where)

    def send_present(self, who, where, what):
        if what:
            self.send_message('present', who, where, what)
        else:
            self.send_message('present', who, where)

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
            room = 'handle_connected_room',
            list = 'handle_connected_list',
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

        self.room = 'default'
        self.ping = None
        self.time_offset = 0
        self.time_offset_data = []
        self.pings_sent = dict()
        self.last_ping_received = time.time()

        self.counter = 0

class SyncFactory(Factory):
    def __init__(self, min_pause_lock = 3, update_time_limit = 1):
        self.watchers = dict()
        self.paused = {}
        self.paused['default'] = True
        self.pause_change_time = None
        self.pause_change_by = None

        self.min_pause_lock = min_pause_lock
        self.update_time_limit = update_time_limit

    def buildProtocol(self, addr):
        return SyncServerProtocol(self)

    def add_watcher(self, watcher_proto, name):
        allnames = []
        for watcher in self.watchers.itervalues():
            allnames.append(watcher.name.lower()) 
        while name.lower() in allnames:
            name += '_'    
            
        watcher = WatcherInfo(watcher_proto, name)
        if self.watchers:
            watcher.max_position = min(w.max_position for w in self.watchers.itervalues())
        self.watchers[watcher_proto] = watcher
        watcher_proto.send_hello(name)
        self.send_state_to(watcher)
        self.send_ping_to(watcher)

    def remove_watcher(self, watcher_proto):
        watcher = self.watchers.pop(watcher_proto, None)
        if not watcher:
            return
        self.remove_room_if_empty(watcher.room)
        watcher.active = False
        self.broadcast(watcher, lambda receiver: receiver.watcher_proto.send_left(watcher.name))
        
        if self.pause_change_by == watcher:
            self.pause_change_time = None
            self.pause_change_by = None
            
    def remove_room_if_empty(self, room):
        room_user_count = sum(1 if watcher.room == room else 0 for watcher in self.watchers.itervalues())
        if not room_user_count:
            if room == 'default':
                self.paused['default'] = True
            else:
                self.paused.pop(room) 

    
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
        
        pause_changed = paused != self.paused[watcher.room]

        if pause_changed and (
            not self.pause_change_by or
            self.pause_change_by == watcher or
            (curtime-self.pause_change_time) > self.min_pause_lock
        ):
            self.paused[watcher.room] = not self.paused[watcher.room]
            self.pause_change_time = curtime
            self.pause_change_by = watcher
        else:
            pause_changed = False

        position = self.find_position(watcher.room)
        
        self.send_state_to(watcher, position, curtime)
        self.broadcast_room(watcher, lambda receiver: self.send_state_to(receiver, position, curtime) if pause_changed or (curtime-receiver.last_update_sent) > self.update_time_limit else False)

    def seek(self, watcher_proto, counter, ctime, position):
        watcher = self.watchers.get(watcher_proto)
        if not watcher:
            return

        #print watcher.name, 'seeked to', position
        curtime = time.time()
        ctime += watcher.time_offset
        position += curtime - ctime
        watcher.counter = counter
        
        watcher.max_position = position
        self.send_state_to(watcher, position, curtime)
        
        self.broadcast_room(watcher, lambda receiver: self.__do_seek(receiver, position, watcher, curtime))
    
    def __do_seek(self, receiver, position, watcher, curtime):
        receiver.max_position = position
        receiver.watcher_proto.send_seek(curtime-receiver.time_offset, position, watcher.name)
        
    def send_state_to(self, watcher, position=None, curtime=None):
        if position is None:
            position = self.find_position(watcher.room)
        if curtime is None:
            curtime = time.time()

        ctime = curtime - watcher.time_offset

        if self.pause_change_by:
            watcher.watcher_proto.send_state(watcher.counter, ctime, self.paused[watcher.room], position, self.pause_change_by.name)
        else:
            watcher.watcher_proto.send_state(watcher.counter, ctime, self.paused[watcher.room], position, None)

        watcher.last_update_sent = curtime

    def find_position(self, room):
        curtime = time.time()
        try:
            return min(
                max(watcher.max_position, watcher.position + (0 if self.paused[watcher.room] else curtime-watcher.last_update))
                for watcher in self.watchers.itervalues()
                if watcher.last_update and watcher.room == room
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
        if (time.time()-watcher.last_update_sent) > 8:
            self.remove_watcher(watcher.watcher_proto)
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
        self.broadcast(watcher, lambda receiver: receiver.watcher_proto.send_playing(watcher.name, watcher.room, filename))
                
    def broadcast_room(self, sender, what):
        for receiver in self.watchers.itervalues():
            if receiver.room == sender.room and receiver != sender:
                what(receiver)
                
    def broadcast(self, sender, what):
        for receiver in self.watchers.itervalues():
            #if receiver != sender:
            what(receiver)
