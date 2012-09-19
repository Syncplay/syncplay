import os

class Syncplay(object):
    def __init__(self):
        if(os.name <> 'nt'):
            from syncplay.SyncplayMplayer import SyncplayMplayer
            SyncplayMplayer()
        else:
            from syncplay.SyncplayMPC import SyncplayMPC
            SyncplayMPC()

if(__name__ == '__main__'):
    Syncplay()