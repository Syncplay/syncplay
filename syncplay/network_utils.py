#coding:utf8

from .utils import ArgumentParser
from functools import wraps
from twisted.internet.protocol import ProcessProtocol
from twisted.protocols.basic import LineReceiver

def argumentCount(minimum, maximum=None):
    def decorator(f):
        @wraps(f)
        def wrapper(self, args):
            if ((len(args) != minimum) if maximum is None else not (minimum <= len(args) <= maximum)):
                self.dropWithError('Invalid arguments')
                return
            return f(self, args)
        return wrapper
    return decorator

class CommandProtocol(LineReceiver):
    states = None

    def __init__(self):
        self._state = self.initial_state

    def lineReceived(self, line):
        line = line.strip()
        if not line:
            return
        
        args = ArgumentParser.splitArguments(line)
        if not args:
            self.dropWithError('Malformed line')
            return
        command = args.pop(0)
        #if command not in ['ping', 'pong']:
        #    print '>>>', line
        if command == 'error':
            self.handle_error(args)
            return

        available_commands = self.states.get(self._state)
        handler = available_commands.get(command)
        if handler:
            handler = getattr(self, handler, None)
        if not handler:
            self.dropWithError('Unknown command: `%s`' % command)
            return # TODO log it too
        handler(args)

    def handle_error(self, args):
        print 'Error received from other side:', args

    def change_state(self, new_state):
        if new_state not in self.states:
            raise RuntimeError('Unknown state: %s' % new_state)
        self._state = new_state

    def send_message(self, *args):
        line = ArgumentParser.joinArguments(args)
        #if args[0] not in ['ping', 'pong']:
        #    print '<<<', line
        self.sendLine(line)

    def drop(self):
        self.transport.loseConnection()

    def dropWithError(self, error):
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


