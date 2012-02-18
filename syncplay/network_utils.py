#coding:utf8

from functools import wraps
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from twisted.internet.defer import succeed
from twisted.internet.protocol import (
    ProcessProtocol,
    Protocol,
)
from twisted.protocols.basic import LineReceiver
from twisted.web.iweb import IBodyProducer

from zope.interface import implements

from .utils import (
    join_args,
    split_args,
)


def arg_count(minimum, maximum=None):
    def decorator(f):
        @wraps(f)
        def wrapper(self, args):
            if ((len(args) != minimum) if maximum is None else not (minimum <= len(args) <= maximum)):
                self.drop_with_error('Invalid arguments')
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
        #print '>>>', line
        args = split_args(line)
        if not args:
            self.drop_with_error('Malformed line')
            return
        command = args.pop(0)

        if command == 'error':
            self.handle_error(args)
            return

        available_commands = self.states.get(self._state)
        handler = available_commands.get(command)
        if handler:
            handler = getattr(self, handler, None)
        if not handler:
            self.drop_with_error('Unknown command: `%s`' % command)
            return # TODO log it too

        handler(args)

    def handle_error(self, args):
        print 'Error received from other side:', args

    def change_state(self, new_state):
        if new_state not in self.states:
            raise RuntimeError('Unknown state: %s' % new_state)
        self._state = new_state

    def send_message(self, *args):
        line = join_args(args)
        #print '<<<', line
        self.sendLine(line)

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


class BodyProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass

class BodyGetter(Protocol):
    def __init__(self, length, callback):
        self.length = length
        self.callback = callback
        self.body = StringIO()

    def dataReceived(self, data):
        if self.length > 0:
            data = data[:self.length]
            self.body.write(data)
            self.length -= len(length)

    def connectionLost(self, reason):
        self.callback(self.body.getvalue())

def null_response_handler(status, headers, body):
    pass

def handle_response(callback):
    def defer_callback(response):
        status = response.code
        headers = response.headers.getAllRawHeaders()
        def body_callback(body):
            callback(status, headers, body)
        response.deliverBody(BodyGetter(response.length, body_callback))
    return defer_callback

