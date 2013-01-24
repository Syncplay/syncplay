from syncplay.players.mplayer import MplayerPlayer
from syncplay import constants

class MpvPlayer(MplayerPlayer):
    SLAVE_ARGS = constants.MPV_SLAVE_ARGS
    
    @staticmethod
    def run(client, playerPath, filePath, args):
        return MpvPlayer(client, MpvPlayer.getExpandedPath(playerPath), filePath, args)
    
    @staticmethod
    def getDefaultPlayerPathsList():
        l = []
        for path in constants.MPV_PATHS:
            p = MpvPlayer.getExpandedPath(path)
            if p:
                l.append(p) 
        return l
    
    @staticmethod
    def isValidPlayerPath(path):
        if("mpv" in path and MpvPlayer.getExpandedPath(path)):
            return True
        return False
