#coding:utf8

import time

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class SyncProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory

        self.state = 'init'
        self.active = False

    def connectionMade(self):
        self.active = True

    def connectionLost(self, reason):
        self.active = False
        self.factory.remove_watcher(self)

    def lineReceived(self, line):
        line = line.strip()
        if not line:
            return
        line = line.split(None, 1)
        if len(line) != 2:
            self._drop_with_error('Malformed line')
            return
        command, arg = line

        available_commands = self.states.get(self.state)
        if not available_commands:
            return # TODO log it

        handler = available_commands.get(command)
        if handler:
            handler = getattr(self, handler, None)
        if not handler:
            self._drop_with_error('Unknown command: `%s`' % command)
            return # TODO log it too

        handler(arg)

    # Own

    def _get_ident(self):
        return '|'.join((
            self.transport.getPeer().host,
            str(id(self)),
        ))

    def _send(self, *args):
        self.sendLine(' '.join((arg if isinstance(arg, basestring) else str(arg)) for arg in args))

    def _drop(self):
        self.active = False
        self.transport.loseConnection()

    def _drop_with_error(self, error):
        self._send('error', error)
        self._drop()

    def _handle_init_welcome(self, arg):
        self.factory.add_watcher(self, arg.strip())
        self.state = 'connected'

    def _handle_connected_state(self, arg):
        arg = arg.split(None, 1)
        if len(arg) != 2:
            self._drop_with_error('Malformed state attributes')
            return
        state, position = arg

        if not state in ('paused', 'playing'):
            self._drop_with_error('Unknown state')
            return

        paused = state == 'paused'

        try:
            position = int(position)
        except ValueError:
            self._drop_with_error('Invalid position numeral')

        position /= 100.0

        self.factory.update_state(self, paused, position)

    def _handle_connected_seek(self, arg):
        try:
            position = int(arg)
        except ValueError:
            self._drop_with_error('Invalid position numeral')

        position /= 100.0

        self.factory.seek(self, position)

    def send_state(self, paused, position, who_last_changed):
        self._send('state', ('paused' if paused else 'playing'), int(position*100), who_last_changed)

    def send_seek(self, position, who_seeked):
        self._send('seek', int(position*100), who_seeked)

    states = dict(
        init = dict(
            welcome = '_handle_init_welcome',
        ),
        connected = dict(
            state = '_handle_connected_state',
            seek = '_handle_connected_seek',
            #ping = '_handle_connected_ping',
        ),
    )

    def __hash__(self):
        return hash(self._get_ident())


class WatcherInfo(object):
    def __init__(self, watcher_proto, name):
        self.watcher_proto = watcher_proto
        self.name = name

        self.position = 0
        self.max_position = 0
        self.last_update = None
        self.last_update_sent = None

    def update_position(self, position):
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
        return SyncProtocol(self)

    # Own

    def add_watcher(self, watcher_proto, name):
        watcher = WatcherInfo(watcher_proto, name)
        self.watchers[watcher_proto] = watcher
        self._send_state_to(watcher)
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

        position = self._find_position()
        for receiver in self.watchers.itervalues():
            if (
                receiver == watcher or
                pause_changed or
                (curtime-receiver.last_update_sent) > self.update_time_limit
            ):
                self._send_state_to(receiver, position, curtime)

    def seek(self, watcher_proto, position):
        pass
        #for receiver in self.watchers.itervalues():

    def _send_state_to(self, watcher, position=None, curtime=None):
        if position is None:
            position = self._find_position()
        if curtime is None:
            curtime = time.time()
        watcher.watcher_proto.send_state(self.paused, position, (self.pause_change_by and self.pause_change_by.name) or '')
        watcher.last_update_sent = curtime

    def _find_position(self):
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

