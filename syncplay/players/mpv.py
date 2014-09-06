import re
import subprocess
from syncplay.players.mplayer import MplayerPlayer
from syncplay import constants
import os, sys

class MpvPlayer(MplayerPlayer):
    POSITION_QUERY = 'time-pos'
    OSD_QUERY = 'show_text'
    RE_VERSION = re.compile('.*mpv (\d)\.(\d)\.\d.*')

    def _setProperty(self, property_, value):
        self._listener.sendLine("no-osd set {} {}".format(property_, value))

    def setPaused(self, value):
        if self._paused <> value:
            self._paused = not self._paused
            self._listener.sendLine('cycle pause')

    @staticmethod
    def run(client, playerPath, filePath, args):
        return MpvPlayer(client, MpvPlayer.getExpandedPath(playerPath), filePath, args)

    @staticmethod
    def getStartupArgs(path):
        ver = MpvPlayer.RE_VERSION.search(subprocess.check_output([path, '--version']))
        new_mpv = ver is None or int(ver.group(1)) > 0 or int(ver.group(2)) >= 5
        args = constants.MPV_SLAVE_ARGS
        if sys.platform.startswith('win') or not new_mpv:
             args.extend(constants.MPV_SLAVE_ARGS_WINDOWS)
        else:
             args.extend(constants.MPV_SLAVE_ARGS_NONWINDOWS)
        return args

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
        if "mpv" in path and MpvPlayer.getExpandedPath(path):
            return True
        return False

    @staticmethod
    def getExpandedPath(playerPath):
        if not os.path.isfile(playerPath):
            if os.path.isfile(playerPath + u"mpv.exe"):
                playerPath += u"mpv.exe"
                return playerPath
            elif os.path.isfile(playerPath + u"\\mpv.exe"):
                playerPath += u"\\mpv.exe"
                return playerPath
        if os.access(playerPath, os.X_OK):
            return playerPath
        for path in os.environ['PATH'].split(':'):
            path = os.path.join(os.path.realpath(path), playerPath)
            if os.access(path, os.X_OK):
                return path

    @staticmethod
    def getIconPath(path):
        return constants.MPV_ICONPATH
