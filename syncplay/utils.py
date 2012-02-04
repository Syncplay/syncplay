#coding:utf8

import os
import re

RE_ARG = re.compile(r"('(?:[^\\']+|\\\\|\\')*'|[^\s']+)(?:\s+|\Z)")
RE_NEED_QUOTING = re.compile(r"[\s'\\]")
RE_QUOTABLE = re.compile(r"['\\]")
RE_UNQUOTABLE = re.compile(r"\\(['\\])")

class InvalidArgumentException(Exception):
    pass

def quote_arg(arg):
    if isinstance(arg, unicode):
        arg = arg.encode('utf8')
    elif not isinstance(arg, str):
        arg = str(arg)

    if not arg or RE_NEED_QUOTING.search(arg):
        return "'%s'" % RE_QUOTABLE.sub(r'\\\g<0>', arg)
    return arg

def unqote_arg(arg):
    if arg.startswith("'") and len(arg) > 1:
        arg = RE_UNQUOTABLE.sub(r'\1', arg[1:-1])
    return arg.decode('utf8', 'replace')

def _split_args(args):
    pos = 0
    while pos < len(args):
        match = RE_ARG.match(args, pos)
        if not match:
            raise InvalidArgumentException()
        pos = match.end()
        yield unqote_arg(match.group(1))

def split_args(args):
    try:
        return list(_split_args(args))
    except InvalidArgumentException:
        return None

def join_args(args):
    return ' '.join(quote_arg(arg) for arg in args)


def parse_state(args):
    if len(args) == 3:
        counter, state, position = args
        who_changed_state = None
    elif len(args) == 4:
        counter, state, position, who_changed_state = args
    else:
        return

    try:
        counter = int(counter)
    except ValueError:
        return

    if not state in ('paused', 'playing'):
        return

    paused = state == 'paused'

    try:
        position = int(position)
    except ValueError:
        return

    position /= 1000.0

    return counter, paused, position, who_changed_state

def find_exec_path(name):
    if os.access(name, os.X_OK):
        return name
    for path in os.environ['PATH'].split(':'):
        path = os.path.join(os.path.realpath(path), name)
        if os.access(path, os.X_OK):
            return path

