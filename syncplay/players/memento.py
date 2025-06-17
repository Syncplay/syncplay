import os

from syncplay import constants

from syncplay.players.mpv import MpvPlayer
from syncplay.utils import findResourcePath, playerPathExists


class MementoPlayer(MpvPlayer):
    @staticmethod
    def run(client, playerPath, filePath, args):
        return MementoPlayer(
            client, MementoPlayer.getExpandedPath(playerPath), filePath, args
        )

    @staticmethod
    def getDefaultPlayerPathsList():
        l = []
        for path in constants.MEMENTO_PATHS:
            p = MementoPlayer.getExpandedPath(path)
            if p:
                l.append(p)
        return l

    @staticmethod
    def isValidPlayerPath(path):
        if "memento" in path and MementoPlayer.getExpandedPath(path):
            return True
        return False

    @staticmethod
    def getExpandedPath(playerPath):
        if not playerPathExists(playerPath):
            if playerPathExists(playerPath + "memento.exe"):
                playerPath += "memento.exe"
                return playerPath
            elif playerPathExists(playerPath + "\\memento.exe"):
                playerPath += "\\memento.exe"
                return playerPath
        if os.access(playerPath, os.X_OK):
            return playerPath
        for path in os.environ["PATH"].split(":"):
            path = os.path.join(os.path.realpath(path), playerPath)
            if os.access(path, os.X_OK):
                return path

    @staticmethod
    def getIconPath(path):
        return constants.MEMENTO_ICONPATH

    @staticmethod
    def getStartupArgs(userArgs):
        args = constants.MPV_ARGS
        args["scripts"] = findResourcePath("syncplayintf.lua")
        if userArgs:
            for argToAdd in userArgs:
                if argToAdd.startswith("--"):
                    argToAdd = argToAdd[2:]
                elif argToAdd.startswith("-"):
                    argToAdd = argToAdd[1:]
                if argToAdd.strip() == "":
                    continue
                if "=" in argToAdd:
                    (argName, argValue) = argToAdd.split("=", 1)
                    if argValue[0] == '"' and argValue[-1] == '"':
                        argValue = argValue[1:-1]
                else:
                    argName = argToAdd
                    argValue = ""
                args[argName] = argValue
        return args
