#coding:utf8

from twisted.internet.protocol import ProcessProtocol
from twisted.protocols.basic import LineReceiver

class CommandProtocol(LineReceiver):
    states = None

    def __init__(self):
        self._state = self.initial_state

    def lineReceived(self, line):
        line = line.strip()
        if not line:
            return
        line = line.split(None, 1)
        if len(line) != 2:
            self.drop_with_error('Malformed line')
            return
        command, arg = line

        available_commands = self.states.get(self._state)
        handler = available_commands.get(command)
        if handler:
            handler = getattr(self, handler, None)
        if not handler:
            self.drop_with_error('Unknown command: `%s`' % command)
            return # TODO log it too

        handler(arg)

    def change_state(self, new_state):
        if new_state not in self.states:
            raise RuntimeError('Unknown state: %s' % new_state)
        self._state = new_state

    def send_message(self, *args):
        self.sendLine(' '.join(
            (arg if isinstance(arg, basestring) else str(arg))
            for arg in args
            if arg is not None
        ))

    def drop(self):
        self.transport.loseConnection()

    def drop_with_error(self, error):
        self.send_message('error', error)
        self.drop()


def parse_lines(leftovers, data):
    data = leftovers+data
    lines = data.split('\n')
    leftovers = lines.pop(-1)
    return leftovers, lines

class LineProcessProtocol(ProcessProtocol):
    _leftover_out = ''
    _leftover_err = ''

    def errLineReceived(self, line):
        pass

    def outLineReceived(self, line):
        pass

    def outReceived(self, data):
        self._leftover_out, lines = parse_lines(self._leftover_out, data)
        for line in lines:
            self.outLineReceived(line)

    def errReceived(self, data):
        self._leftover_err, lines = parse_lines(self._leftover_err, data)
        for line in lines:
            self.errLineReceived(line)

    def writeLines(self, *lines):
        for line in lines:
            self.transport.write(line+'\n')

