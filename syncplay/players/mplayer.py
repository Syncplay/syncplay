#coding:utf8

from ..utils import find_exec_path
from collections import deque
from twisted.internet import reactor
from twisted.internet.protocol import ProcessProtocol
import re

RE_ANSWER = re.compile('^ANS_([a-zA-Z_]+)=(.+)$')

class LineProcessProtocol(ProcessProtocol):
    _leftover_out = ''
    _leftover_err = ''
    
    def parse_lines(self, leftovers, data):
        data = leftovers+data
        lines = data.split('\n')
        leftovers = lines.pop(-1)
        return leftovers, lines

    def errLineReceived(self, line):
        pass

    def outLineReceived(self, line):
        pass

    def outReceived(self, data):
        self._leftover_out, lines = self.parse_lines(self._leftover_out, data)
        for line in lines:
            self.outLineReceived(line)

    def errReceived(self, data):
        self._leftover_err, lines = self.parse_lines(self._leftover_err, data)
        for line in lines:
            self.errLineReceived(line)

    def writeLines(self, *lines):
        for line in lines:
            self.transport.write(line+'\n')


class MplayerProtocol(LineProcessProtocol):
    speed_supported = True

    def __init__(self, manager):
        self.__syncplayClient = manager
        self.ignore_end = False
        self.error_lines = deque(maxlen=50)
        self.tmp_paused = None
        self.set_pause = False
        
        self.duration = None
        self.filename = None
        self.filepath = None
        self.fileupdatesteps = 0

    def connectionMade(self):
        reactor.callLater(0.1, self.prepare_player)

    def processEnded(self, reason):
        self.__syncplayClient.player = None
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
        self.__syncplayClient.stop(False)

    def errLineReceived(self, line):
        if line:
            self.error_lines.append(line)

    def outLineReceived(self, line):
        if not (line and line.startswith('ANS_')):
            return
        m = RE_ANSWER.match(line)
        if not m:
            return

        name, value = m.group(1).lower(), m.group(2)
        handler = getattr(self, 'mplayer_answer_' + name, None)
        if handler:
            handler(value)

    
    def prepare_player(self):
        self.set_paused(True)
        
        self.set_position(0)
        self.send_get_filename()
        self.send_get_length()
        self.send_get_filepath()
        
    def ask_for_status(self):
        self.send_get_paused()
        self.send_get_position()


    def send_set_property(self, name, value):
        self.writeLines('%s %s %s' % ('set_property', name, value))

    def send_get_property(self, name):
        self.writeLines('%s %s' % ('get_property', name))

    def display_message(self, message):
        self.writeLines('%s %s %s %s' % ('osd_show_text', '"%s"'% str(message), 3000, 1))

    def send_get_filename(self):
        self.send_get_property('filename')

    def send_get_length(self):
        self.send_get_property('length')

    def send_get_filepath(self):
        self.send_get_property('path')

    def setUpFileInPlayer(self):
        self.fileupdatesteps = 0
        self.__syncplayClient.initPlayer(self)
        self.__syncplayClient.updateFile(self.filename, self.duration, self.filepath)
        if self.__syncplayClient.last_global_update:
            self.set_position(self.__syncplayClient.getGlobalPosition())
            self.set_paused(True)

    def mplayer_answer_filename(self, value):
        self.filename = value
        self.fileupdatesteps += 1
        if(self.fileupdatesteps == 3):
            self.setUpFileInPlayer()
            
    def mplayer_answer_path(self, value):
        self.filepath = value
        self.fileupdatesteps += 1
        if(self.fileupdatesteps == 3):
            self.setUpFileInPlayer()

    def mplayer_answer_length(self, value):
        self.duration = int(float(value))
        self.fileupdatesteps += 1
        if(self.fileupdatesteps == 3):
            self.setUpFileInPlayer()
   
    def set_paused(self, value):
        # docs say i can't set "pause" property, but it works...
        # no, Fluxid, it doesn't on Windows, fuck you. TODO:
        self.send_set_property('pause', 'yes' if value else 'no') 

    def send_get_paused(self):
        self.send_get_property('pause')

    def mplayer_answer_pause(self, value):
        value = value == 'yes'
        self.tmp_paused = value
    
    def set_position(self, value):
        self.send_set_property('time_pos', '%0.2f'%value)

    def send_get_position(self):
        self.send_get_property('time_pos')

    def mplayer_answer_time_pos(self, value):
        value = float(value)
        self.__syncplayClient.updatePlayerStatus(self.tmp_paused, value)


    def set_speed(self, value):
        self.send_set_property('speed', '%0.2f'%value)

    #def send_get_speed(self):
    #    self.send_get_property('speed')

    #def mplayer_answer_speed(self, value):
    #    value = float(value)
    #    self.__syncplayClient.update_player_speed(value)

    
    def drop(self):
        self.ignore_end = True
        self.writeLines('quit')
 

def run_mplayer(manager, mplayer_path, args):
    exec_path = find_exec_path(mplayer_path)
    print 'Running', exec_path
    if not exec_path:
        raise Exception('Mplayer executable not found')

    args = list(args)
    args.insert(0, mplayer_path)
    process_protocol = MplayerProtocol(manager)
    reactor.spawnProcess(process_protocol, exec_path, args=args, env=None)

