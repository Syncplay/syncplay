import os
from syncplay import constants
from syncplay.players.mpv import MpvPlayer
from syncplay.utils import playerPathExists

class MpvnetPlayer(MpvPlayer):


    @staticmethod
    def run(client, playerPath, filePath, args):
            constants.MPV_NEW_VERSION = True
            constants.MPV_OSC_VISIBILITY_CHANGE_VERSION = True
            return MpvnetPlayer(client, MpvnetPlayer.getExpandedPath(playerPath), filePath, args)

    @staticmethod
    def getDefaultPlayerPathsList():
        l = []
        for path in constants.MPVNET_PATHS:
            p = MpvnetPlayer.getExpandedPath(path)
            if p:
                l.append(p)
        return l


    @staticmethod
    def isValidPlayerPath(path):
        if "mpvnet" in path and MpvnetPlayer.getExpandedPath(path):
            return True
        return False


    @staticmethod
    def getExpandedPath(playerPath):
        if not playerPathExists(playerPath):
            if playerPathExists(playerPath + "mpvnet.exe"):
                playerPath += "mpvnet.exe"
                return playerPath
            elif playerPathExists(playerPath + "\\mpvnet.exe"):
                playerPath += "\\mpvnet.exe"
                return playerPath
        if os.access(playerPath, os.X_OK):
            return playerPath
        for path in os.environ['PATH'].split(':'):
            path = os.path.join(os.path.realpath(path), playerPath)
            if os.access(path, os.X_OK):
                return path


    @staticmethod
    def getIconPath(path):
        return constants.MPVNET_ICONPATH

    def sendMpvOptions(self):
        for key in self._listener.mpv_arguments:
            if key != "script" and key != "input-ipc-server":
                self._setProperty(key, self._listener.mpv_arguments[key])
        super().sendMpvOptions()

