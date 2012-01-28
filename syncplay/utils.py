#coding:utf8

def split_args(args, number):
    # FIXME Make argument format smarter
    return args.split(None, number-1)

def parse_state(args):
    args = split_args(args, 3)
    l = len(args)
    if l == 2:
        state, position = args
        who_changed_state = None
    elif l == 3:
        state, position, who_changed_state = args
    else:
        return

    if not state in ('paused', 'playing'):
        return

    paused = state == 'paused'

    try:
        position = int(position)
    except ValueError:
        return

    position /= 100.0

    return paused, position, who_changed_state

