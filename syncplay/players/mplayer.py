#coding:utf8

import re
import sys

from twisted.internet import reactor

from ..network_utils import LineProcessProtocol
from ..utils import find_exec_path

RE_ANSWER = re.compile('^ANS_([a-zA-Z_]+)=(.+)$')


class MplayerProtocol(LineProcessProtocol):
    def __init__(self, manager):
        self.manager = manager

    def connectionMade(self):
        self.manager.player = self
        self.send_set_paused(True)
        self.send_set_position(0)

    def processExited(self, reason):
        self.manager.player = None

    def processEnded(self, reason):
        reactor.stop()

    def errLineReceived(self, line):
        sys.stderr.write(line+'\n')

    def outLineReceived(self, line):
        if not line.startswith('ANS_'):
            sys.stdout.write(line+'\n')
            return
        m = RE_ANSWER.match(line)
        if not m:
            return

        name, value = m.group(1).lower(), m.group(2)
        handler = getattr(self, 'answer_' + name, None)
        if handler:
            handler(value)

    
    def set_property(self, name, value):
        self.writeLines('%s %s %s' % ('set_property', name, value))

    def get_property(self, name):
        self.writeLines('%s %s' % ('get_property', name))


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
        self.transport.loseConnection()
        reactor.callLater(1, self.graceful_kill)

    def gracefull_kill(self):
        if self.transport.pid:
            self.transport.signalProcess('TERM')
            reactor.callLater(2, self.try_kill)

    def kill(self):
        if self.transport.pid:
            self.transport.signalProcess('KILL')


def run_mplayer(manager, mplayer_path, args):
    exec_path = find_exec_path(mplayer_path)
    print 'Running', exec_path
    if not exec_path:
        raise Exception('Mplayer executable not found')

    args = list(args)
    args.insert(0, mplayer_path)
    
    process_protocol = MplayerProtocol(manager)
    reactor.spawnProcess(process_protocol, exec_path, args=args, env=None)

