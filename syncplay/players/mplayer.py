#coding:utf8

import re
import sys
from collections import deque

from twisted.internet import reactor

from ..network_utils import LineProcessProtocol
from ..utils import find_exec_path

RE_ANSWER = re.compile('^ANS_([a-zA-Z_]+)=(.+)$')


class MplayerProtocol(LineProcessProtocol):
    def __init__(self, manager):
        self.manager = manager
        self.ignore_end = False
        self.error_lines = deque(maxlen=50)
        self.filename = None # To be moved to Manager

    def connectionMade(self):
        reactor.callLater(0.1, self.prepare_player)

    def processEnded(self, reason):
        self.manager.player = None
        if not self.ignore_end:
            if reason.value.signal is not None:
                print 'Mplayer interrupted by signal %d.' % reason.value.signal
            elif reason.value.exitCode is not None:
                print 'Mplayer quit with exit code %d.' % reason.value.exitCode
            else:
                print 'Mplayer quit unexpectedly.'
            if self.error_lines:
                print 'Up to 50 last lines from its error output below:'
                for line in self.error_lines:
                    print line
        reactor.stop()

    def errLineReceived(self, line):
        if line:
            self.error_lines.append(line)

    def outLineReceived(self, line):
        if not line.startswith('ANS_'):
            return
        m = RE_ANSWER.match(line)
        if not m:
            return

        name, value = m.group(1).lower(), m.group(2)
        handler = getattr(self, 'answer_' + name, None)
        if handler:
            handler(value)

    
    def prepare_player(self):
        self.send_set_paused(True)
        self.send_set_position(0)
        self.send_get_filename()
        self.manager.player = self


    def set_property(self, name, value):
        self.writeLines('%s %s %s' % ('set_property', name, value))

    def get_property(self, name):
        self.writeLines('%s %s' % ('get_property', name))


    def send_get_filename(self):
        self.get_property('filename')

    def answer_filename(self, value):
        self.filename = value


    def send_set_paused(self, value):
        # docs say i can't set "pause" property, but it works...
        self.set_property('pause', 'yes' if value else 'no')

    def send_get_paused(self):
        self.get_property('pause')

    def answer_pause(self, value):
        value = value == 'yes'
        self.manager.update_player_paused(value)


    def send_set_position(self, value):
        self.set_property('time_pos', '%0.2f'%value)

    def send_get_position(self):
        self.get_property('time_pos')

    def answer_time_pos(self, value):
        value = float(value)
        self.manager.update_player_position(value)


    def send_set_speed(self, value):
        self.set_property('speed', '%0.2f'%value)

    def send_get_speed(self):
        self.get_property('speed')

    def answer_speed(self, value):
        value = float(value)
        self.manager.update_player_speed(value)

    
    def drop(self):
        self.ignore_end = True
        self.transport.loseConnection()

def run_mplayer(manager, mplayer_path, args):
    exec_path = find_exec_path(mplayer_path)
    print 'Running', exec_path
    if not exec_path:
        raise Exception('Mplayer executable not found')

    args = list(args)
    args.insert(0, mplayer_path)
    
    process_protocol = MplayerProtocol(manager)
    reactor.spawnProcess(process_protocol, exec_path, args=args, env=None)

