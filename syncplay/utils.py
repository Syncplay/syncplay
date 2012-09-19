#coding:utf8

import os
import re
import itertools

class ArgumentParser():
    RE_ARG = re.compile(r"('(?:[^\\']+|\\\\|\\')*'|[^\s']+)(?:\s+|\Z)")
    RE_NEED_QUOTING = re.compile(r"[\s'\\]")
    RE_QUOTABLE = re.compile(r"['\\]")
    RE_UNQUOTABLE = re.compile(r"\\(['\\])")
    
    class InvalidArgumentException(Exception):
        pass
    
    @staticmethod
    def quoteArgument(arg):
        if isinstance(arg, unicode):
            arg = arg.encode('utf8')
        elif not isinstance(arg, str):
            arg = str(arg)
    
        if not arg or ArgumentParser.RE_NEED_QUOTING.search(arg):
            return "'%s'" % ArgumentParser.RE_QUOTABLE.sub(r'\\\g<0>', arg)
        return arg
    
    @staticmethod
    def unqoteArgument(arg):
        if arg.startswith("'") and len(arg) > 1:
            arg = ArgumentParser.RE_UNQUOTABLE.sub(r'\1', arg[1:-1])
        return arg.decode('utf8', 'replace')
    
    @staticmethod
    def __splitArguments(args):
        pos = 0
        while pos < len(args):
            match = ArgumentParser.RE_ARG.match(args, pos)
            if not match:
                raise ArgumentParser.InvalidArgumentException()
            pos = match.end()
            yield ArgumentParser.unqoteArgument(match.group(1))
            
    @staticmethod
    def splitArguments(args):
        try:
            return list(ArgumentParser.__splitArguments(args))
        except ArgumentParser.InvalidArgumentException:
            return None
        
    @staticmethod
    def joinArguments(args):
        args = list(itertools.ifilterfalse(lambda x: None == x, args))
        return ' '.join(ArgumentParser.quoteArgument(arg) for arg in args)
    
def find_exec_path(name):
    if os.access(name, os.X_OK):
        return name
    for path in os.environ['PATH'].split(':'):
        path = os.path.join(os.path.realpath(path), name)
        if os.access(path, os.X_OK):
            return path

def format_time(value):
    value = int(value*100)
    seconds, mseconds = divmod(value, 100)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return '%02d:%02d:%02d.%02d' % (hours, minutes, seconds, mseconds)
