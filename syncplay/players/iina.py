import os
from syncplay import constants
from syncplay.utils import findResourcePath
from syncplay.players.mpv import MpvPlayer
from syncplay.players.python_mpv_jsonipc.python_mpv_jsonipc import IINA

class IinaPlayer(MpvPlayer):


    @staticmethod
    def run(client, playerPath, filePath, args):
            constants.MPV_NEW_VERSION = True
            constants.MPV_OSC_VISIBILITY_CHANGE_VERSION = True
            return IinaPlayer(client, IinaPlayer.getExpandedPath(playerPath), filePath, args)

    @staticmethod
    def getStartupArgs(userArgs):
        args = {}
        if userArgs:
            for argToAdd in userArgs:
                if argToAdd.startswith('--'):
                    argToAdd = argToAdd[2:]
                elif argToAdd.startswith('-'):
                    argToAdd = argToAdd[1:]
                if argToAdd.strip() == "":
                    continue
                if "=" in argToAdd:
                    (argName, argValue) = argToAdd.split("=", 1)
                else:
                    argName = argToAdd
                    argValue = "yes"
                args[argName] = argValue
        return args

    @staticmethod
    def getDefaultPlayerPathsList():
        l = []
        for path in constants.IINA_PATHS:
            p = IinaPlayer.getExpandedPath(path)
            if p:
                l.append(p)
        return l

    @staticmethod
    def isValidPlayerPath(path):
        if "iina-cli" in path and IinaPlayer.getExpandedPath(path):
            return True
        return False

    @staticmethod
    def getExpandedPath(playerPath):
        if os.access(playerPath, os.X_OK):
            return playerPath
        for path in os.environ['PATH'].split(':'):
            path = os.path.join(os.path.realpath(path), playerPath)
            if os.access(path, os.X_OK):
                return path

    @staticmethod
    def getIconPath(path):
        return constants.IINA_ICONPATH

    def __init__(self, client, playerPath, filePath, args):
        from twisted.internet import reactor
        self.reactor = reactor
        self._client = client
        self._set_defaults()

        self._playerIPCHandler = IINA
        self._create_listener(playerPath, filePath, args)

    def _preparePlayer(self):
        for key, value in constants.IINA_PROPERTIES.items():
            self._setProperty(key, value)
        self._listener.sendLine(["load-script", findResourcePath("syncplayintf.lua")])
        super()._preparePlayer()
