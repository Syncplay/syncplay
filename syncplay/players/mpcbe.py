from syncplay import constants
import os.path
from syncplay.messages import getMessage
from syncplay.players.mpc import MPCHCAPIPlayer

class MpcBePlayer(MPCHCAPIPlayer):
    @staticmethod
    def run(client, playerPath, filePath, args):
        args.extend(['/open', '/new'])
        mpc = MpcBePlayer(client)
        mpc._mpcApi.callbacks.onConnected = lambda: mpc.initPlayer(filePath if filePath else None)
        mpc._mpcApi.startMpc(MpcBePlayer.getExpandedPath(playerPath), args)
        client.initPlayer(mpc)
        return mpc

    @staticmethod
    def getDefaultPlayerPathsList():
        return constants.MPC_BE_PATHS

    @staticmethod
    def getIconPath(path):
        return constants.MPC_BE_ICONPATH

    @staticmethod
    def isValidPlayerPath(path):
        if MpcBePlayer.getExpandedPath(path):
            return True
        return False

    @staticmethod
    def getExpandedPath(path):
        if os.path.isfile(path):
            if path.lower().endswith('mpc-be.exe'.lower()) or path.lower().endswith('mpc-be64.exe'.lower() or path.lower().endswith('mpc-beportable.exe'.lower())):
                return path
        if os.path.isfile(path + "mpc-be.exe"):
            path += "mpc-be.exe"
            return path
        if os.path.isfile(path + "\\mpc-be.exe"):
            path += "\\mpc-be.exe"
            return path
        if os.path.isfile(path + "mpc-beportable.exe"):
            path += "mpc-beportable.exe"
            return path
        if os.path.isfile(path + "\\mpc-beportable.exe"):
            path += "\\mpc-beportable.exe"
            return path
        if os.path.isfile(path + "mpc-be64.exe"):
            path += "mpc-be64.exe"
            return path
        if os.path.isfile(path + "\\mpc-be64.exe"):
            path += "\\mpc-be64.exe"
            return path

    @staticmethod
    def getMinVersionErrorMessage():
        return getMessage("mpc-be-version-insufficient-error").format(constants.MPC_BE_MIN_VER)
