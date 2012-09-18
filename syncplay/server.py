#coding:utf8

import re
import time
import random
from functools import wraps
import hashlib
from twisted.internet import reactor
from twisted.internet.protocol import Factory

from .network_utils import argumentCount, CommandProtocol

random.seed()

CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def random_chars():
    return ''.join(random.choice(CHARS) for _ in xrange(10))

def state(state):
    def decorator(f):
        @wraps(f)
        def wrapper(self, args):
            if (not self.compareState(state)):
                self.dropWithError('Invalid watcher state')
                return
            return f(self, args)
        return wrapper
    return decorator

class SyncServerProtocol(CommandProtocol):
    def __init__(self, factory):
        CommandProtocol.__init__(self)
        self.handler = self._MessagesHandler(self, factory)
        self.sender = self._MessagesSender(self)
        self.factory = factory
        self.state = 'init'
    
    def dropWithError(self, error):
        CommandProtocol.dropWithError(self, error)
        print "Client drop: %s -- %s" % (self.transport.getPeer().host, error)
        
    def __hash__(self):
        return hash('|'.join((
            self.transport.getPeer().host,
            str(id(self)),
        )))
        
    def connectionLost(self, reason):
        self.factory.remove_watcher(self)
        
    def change_state(self, state):
        self.state = state
    
    class _MessagesHandler(object):
        def __init__(self, protocol, factory):
            self.__protocol = protocol
            self.factory = factory
            
        def dropWithError(self, error):
            self.__protocol.dropWithError(error)
        
        def compareState(self, state):
            if state != self.__protocol.state:
                return False
            else:
                return True
        
        @state('init')
        @argumentCount(2, 3)    
        def iam(self, args):
                name = re.sub('[^\w]','',args.pop(0))
                if not name:
                    self.dropWithError('Invalid nickname')
                    return
                room = re.sub('[^\w]','',args.pop(0))
                if not room:
                    self.dropWithError('Invalid room')
                    return
                if(self.factory.password):
                    if(len(args)):
                        password = args.pop(0)
                        if(self.factory.password <> password):
                            self.dropWithError('Wrong server password specified')
                    else:
                        self.dropWithError('No password specified')
                        return
                self.factory.add_watcher(self.__protocol, name, room)
                self.__protocol.change_state('connected')
    
        
        @state('connected')        
        @argumentCount(3)
        def seek(self, args):
            counter, ctime, position = args
            try:
                counter = int(counter)
                ctime = int(ctime)
                position = int(position)
            except ValueError:
                self.dropWithError('Invalid arguments')
    
            ctime /= 1000.0
            position /= 1000.0
    
            self.factory.seek(self.__protocol, counter, ctime, position)
    
        @state('connected')
        @argumentCount(2)
        def pong(self, args):
            value, ctime = args
            try:
                ctime = int(ctime)
            except ValueError:
                self.dropWithError('Invalid arguments')
    
            ctime /= 100000.0
    
            self.factory.pong_received(self.__protocol, value, ctime)
    
        @state('connected')
        @argumentCount(1)
        def playing(self, args):
            self.factory.playing_received(self.__protocol, args[0])

        
        @state('connected')
        @argumentCount(1)
        def room(self, args):
            watcher = self.factory.watchers.get(self.__protocol)
            old_room = watcher.room
            watcher.room = str(re.sub('[^\w]','',args[0]))
            self.factory.broadcast(watcher, lambda receiver: receiver.watcher_proto.send_room(watcher.name,watcher.room))
            if not watcher.room in self.factory.paused: 
                self.factory.paused[watcher.room] = True
            self.factory.remove_room_if_empty(old_room)
            
        @state('connected') 
        @argumentCount(0)
        def list(self, args):
            watcher = self.factory.watchers.get(self.__protocol)
            for w in self.factory.watchers.itervalues():
                    if w == watcher:
                        continue
                    self.__protocol.sender.send_present(w.name, w.room, w.filename)
        
        @state('connected')    
        @argumentCount(4)
        def state(self, args):
            args = self.__parseState(args)
            if not args:
                self.dropWithError('Malformed state attributes')
                return
            counter, ctime, paused, position, _ = args
            self.factory.update_state(self.__protocol, counter, ctime, paused, position)

        def __parseState(self, args):
            if len(args) == 4:
                counter, ctime, state, position = args
                who_changed_state = None
            elif len(args) == 5:
                counter, ctime, state, position, who_changed_state = args
            else:
                return
            if not state in ('paused', 'playing'):
                return 
            paused = state == 'paused'
            try:
                counter = int(counter)
                ctime = int(ctime)
                position = int(position)
            except ValueError:
                return
            ctime /= 1000.0
            position /= 1000.0
            return counter, ctime, paused, position, who_changed_state
        
    class _MessagesSender(object):
        def __init__(self, protocol):
            self.__protocol = protocol

        def send_state(self, counter, ctime, paused, position, who_last_changed):
            ctime = int(ctime*1000)
            paused = 'paused' if paused else 'playing'
            position = int(position*1000)
            if who_last_changed is None:
                self.__protocol.sendMessage('state', counter, ctime, paused, position)
            else:
                self.__protocol.sendMessage('state', counter, ctime, paused, position, who_last_changed)
    
        def send_seek(self, ctime, position, who_seeked):
            self.__protocol.sendMessage('seek', int(ctime*1000), int(position*1000), who_seeked)
    
        def send_ping(self, value):
            self.__protocol.sendMessage('ping', value)
    
        def send_playing(self, who, where, what):
            self.__protocol.sendMessage('playing', who, where, what)
    
        def send_room(self, who, where):
            self.__protocol.sendMessage('room', who, where)
    
        def send_present(self, who, where, what):
            if what:
                self.__protocol.sendMessage('present', who, where, what)
            else:
                self.__protocol.sendMessage('present', who, where)
    
        def send_joined(self, who):
            self.__protocol.sendMessage('joined', who)
    
        def send_left(self, who):
            self.__protocol.sendMessage('left', who)
    
        def send_hello(self, name):
            self.__protocol.sendMessage('hello', name)
        


class WatcherInfo(object):
    def __init__(self, watcher_proto, name, room):
        self.watcher_proto = watcher_proto
        self.name = name
        self.active = True

        self.paused = True
        self.position = 0
        self.filename = None
        self.max_position = 0
        self.last_update = None
        self.last_update_sent = None

        self.room = room
        self.ping = None
        self.time_offset = 0
        self.time_offset_data = []
        self.pings_sent = dict()
        self.last_ping_received = time.time()

        self.counter = 0

class SyncFactory(Factory):
    def __init__(self, password = '', banlist = None , isolate_rooms = False, min_pause_lock = 2 , update_time_limit = 1):
        self.watchers = dict()
        self.paused = {}
        self.pause_change_time = None
        self.pause_change_by = None
        if(password):
            password = hashlib.md5(password).hexdigest()
        self.password = password
        self.banlsit = banlist
        self.isolate_rooms = isolate_rooms
        
        self.min_pause_lock = min_pause_lock
        self.update_time_limit = update_time_limit

    def buildProtocol(self, addr):
        return SyncServerProtocol(self)

    def add_watcher(self, watcher_proto, name, room):
        allnames = []
        for watcher in self.watchers.itervalues():
            allnames.append(watcher.name.lower()) 
        while name.lower() in allnames:
            name += '_'  
        if(not self.paused.has_key(room)):
            self.paused[room] = True  
        watcher = WatcherInfo(watcher_proto, name, room)
        if self.watchers:
            watcher.max_position = min(w.max_position for w in self.watchers.itervalues())
        self.watchers[watcher_proto] = watcher
        watcher_proto.sender.send_hello(name)
        self.send_state_to(watcher)
        self.send_ping_to(watcher)

    def remove_watcher(self, watcher_proto):
        watcher = self.watchers.pop(watcher_proto, None)
        if not watcher:
            return
        self.remove_room_if_empty(watcher.room)
        watcher.active = False
        self.broadcast(watcher, lambda receiver: receiver.watcher_proto.sender.send_left(watcher.name))
        
        if self.pause_change_by == watcher:
            self.pause_change_time = None
            self.pause_change_by = None
            
    def remove_room_if_empty(self, room):
        room_user_count = sum(1 if watcher.room == room else 0 for watcher in self.watchers.itervalues())
        if not room_user_count:
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
        receiver.watcher_proto.sender.send_seek(curtime-receiver.time_offset, position, watcher.name)
        
    def send_state_to(self, watcher, position=None, curtime=None):
        if position is None:
            position = self.find_position(watcher.room)
        if curtime is None:
            curtime = time.time()

        ctime = curtime - watcher.time_offset

        if self.pause_change_by:
            watcher.watcher_proto.sender.send_state(watcher.counter, ctime, self.paused[watcher.room], position, self.pause_change_by.name)
        else:
            watcher.watcher_proto.sender.send_state(watcher.counter, ctime, self.paused[watcher.room], position, None)

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
                        ping = 1-((ping-pmin)/pmax) if(pmax <> 0) else 1
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
        if curtime - watcher.last_ping_received > 8:
            watcher.watcher_proto.drop()
            return

        watcher.watcher_proto.sender.send_ping(chars)
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
        self.broadcast(watcher, lambda receiver: receiver.watcher_proto.sender.send_playing(watcher.name, watcher.room, filename))
                
    def broadcast_room(self, sender, what):
        for receiver in self.watchers.itervalues():
            if receiver.room == sender.room and receiver != sender:
                what(receiver)
                
    def broadcast(self, sender, what):
        if(self.isolate_rooms):
            self.broadcast_room(sender, what)
        for receiver in self.watchers.itervalues():
            what(receiver)
