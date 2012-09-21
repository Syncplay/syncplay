import os
import sys
class Syncplay(object):
    def __init__(self):
        if(os.name <> 'nt'):
            from syncplay.SyncplayMplayer import SyncplayMplayer
            SyncplayMplayer()
        else:
            from syncplay.SyncplayMPC import SyncplayMPC
            SyncplayMPC()

if(__name__ == '__main__'):
    if not '-g' in sys.argv:
        if(not '--force-gui-prompt' in sys.argv):
            sys.argv.extend(("-g",))
    Syncplay()