#coding:utf8

from .utils import ArgumentParser
from functools import wraps
import syncplay

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
    def __init__(self):
        self.handler = None
        self.sender = None 

    def lineReceived(self, line):
        line = line.strip()
        if not line:
            return
        
        args = ArgumentParser.splitArguments(line)
        if not args:
            self.dropWithError('Malformed line')
            return
        command = args.pop(0)
        handler = getattr(self.handler, command, None)
        if not handler:
            self.dropWithError('Unknown command: `%s`' % command)
            return
        handler(args)

    def sendMessage(self, *args):
        line = ArgumentParser.joinArguments(args)
        self.sendLine(line)

    def drop(self):
        self.transport.loseConnection()

    def dropWithError(self, error):
        self.sendMessage('error', syncplay.version, error)
        self.drop()



