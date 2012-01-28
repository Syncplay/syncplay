#coding:utf8

import re

from twisted.internet import reactor

from ..network_utils import network_utils

RE_ANSWER = re.compile('^ANS_([a-zA-Z_])=(.+)$')


class MplayerProtocol(ProcessProtocol):
    def outLineReceived(self, line):
        if not line.starts_with('ANS_'):
            return
        m = RE_ANSWER.match(line)
        if not m:
            return

        name, value = m.group(1).lower, m.group(2)
        handler = getattr(self, 'answer_' + name, None)
        if handler:
            handler(value)


    def send_set_paused(self, value):
        # docs say i can't set "pause" property, but it works...
        self.set_property('paused', 'yes' if value else 'no')

    def send_get_paused(self):
        self.get_property('paused')

    def answer_pause(self, value):
        value = value == 'yes'


    def send_set_position(self, value):
        self.set_property('time_pos', '%0.2f'%value)

    def send_get_position(self):
        self.get_property('time_pos')

    def answer_time_pos(self, value):
        value = float(value)


    def send_set_speed(self, value):
        self.set_property('speed', '%0.2f'%value)

    def send_get_speed(self):
        self.get_property('speed')

    def answer_speed(self, value):
        value = float(value)


def run_mplayer(manager, mplayer_path, args):
    pass
