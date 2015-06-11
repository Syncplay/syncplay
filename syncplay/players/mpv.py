import re
import subprocess
from syncplay.players.mplayer import MplayerPlayer
from syncplay.messages import getMessage
from syncplay import constants
import os, sys, time

class MpvPlayer(MplayerPlayer):
    RE_VERSION = re.compile('.*mpv (\d)\.(\d)\.\d.*')
    osdMessageSeparator = "\\n"

    @staticmethod
    def run(client, playerPath, filePath, args):
        try:
            ver = MpvPlayer.RE_VERSION.search(subprocess.check_output([playerPath, '--version']))
        except:
            ver = None
        constants.MPV_NEW_VERSION = ver is None or int(ver.group(1)) > 0 or int(ver.group(2)) >= 6
        if constants.MPV_NEW_VERSION:
            return NewMpvPlayer(client, MpvPlayer.getExpandedPath(playerPath), filePath, args)
        else:
            return OldMpvPlayer(client, MpvPlayer.getExpandedPath(playerPath), filePath, args)

    @staticmethod
    def getStartupArgs(path):
        args = constants.MPV_SLAVE_ARGS

        try:
            pseudogui = subprocess.check_output([path, '--profile=help'])
        except:
            pseudogui = ''
        if 'pseudo-gui' in pseudogui:
            args.extend(constants.MPV_SLAVE_GUI_NEW)
        else:
            args.extend(constants.MPV_SLAVE_GUI)

        if constants.MPV_NEW_VERSION:
            args.extend(constants.MPV_SLAVE_ARGS_NEW)
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

    @staticmethod
    def getPlayerPathErrors(playerPath, filePath):
        return None

class OldMpvPlayer(MpvPlayer):
    POSITION_QUERY = 'time-pos'
    OSD_QUERY = 'show_text'

    def _setProperty(self, property_, value):
        self._listener.sendLine("no-osd set {} {}".format(property_, value))

    def setPaused(self, value):
        if self._paused <> value:
            self._paused = not self._paused
            self._listener.sendLine('cycle pause')

    def mpvVersionErrorCheck(self, line):
        if "Error parsing option" in line or "Error parsing commandline option" in line:
            self.quitReason = getMessage("mpv-version-error")

        elif "Could not open pipe at '/dev/stdin'" in line:
            self.reactor.callFromThread(self._client.ui.showErrorMessage, getMessage("mpv-version-error"), True)
            self.drop()

    def _handleUnknownLine(self, line):
        self.mpvVersionErrorCheck(line)
        if "Playing: " in line:
            newpath = line[9:]
            oldpath = self._filepath
            if newpath != oldpath and oldpath is not None:
                self.reactor.callFromThread(self._onFileUpdate)
                if self._paused != self._client.getGlobalPaused():
                    self.setPaused(self._client.getGlobalPaused())
                self.setPosition(self._client.getGlobalPosition())

class NewMpvPlayer(OldMpvPlayer):
    lastResetTime = None

    def _getProperty(self, property_):
        floatProperties = ['length','time-pos']
        if property_ in floatProperties:
            propertyID = u"={}".format(property_)
        else:
            propertyID = property_
        self._listener.sendLine(u"print_text ""ANS_{}=${{{}}}""".format(property_, propertyID))

    def _storePosition(self, value):
        if self._recentlyReset():
            self._position = 0
        elif self._fileIsLoaded():
            self._position = value
        else:
            self._position = self._client.getGlobalPosition()

    def _storePauseState(self, value):
        if self._fileIsLoaded():
            self._paused = value
        else:
            self._paused = self._client.getGlobalPaused()

    def askForStatus(self):
        self._positionAsk.clear()
        self._pausedAsk.clear()
        self._getPaused()
        self._getPosition()
        self._positionAsk.wait(constants.MPV_LOCK_WAIT_TIME)
        self._pausedAsk.wait(constants.MPV_LOCK_WAIT_TIME)
        self._client.updatePlayerStatus(self._paused, self._position)

    def _preparePlayer(self):
        if self.delayedFilePath:
            self.openFile(self.delayedFilePath)
        self.setPaused(True)
        self.reactor.callLater(0, self._client.initPlayer, self)

    def _clearFileLoaded(self):
        self.fileLoaded = False
        self.lastLoadedTime = None

    def _loadFile(self, filePath):
        self._clearFileLoaded()
        self._listener.sendLine(u'loadfile {}'.format(self._quoteArg(filePath)))

    def openFile(self, filePath, resetPosition=False):
        if resetPosition:
            self.lastResetTime = time.time()
        self._loadFile(filePath)
        if self._paused != self._client.getGlobalPaused():
            self.setPaused(self._client.getGlobalPaused())
        self.setPosition(self._client.getGlobalPosition())

    def _handleUnknownLine(self, line):
        self.mpvVersionErrorCheck(line)

        if line == "<SyncplayUpdateFile>" or "Playing:" in line:
            self._clearFileLoaded()

        elif line == "</SyncplayUpdateFile>":
            self._onFileUpdate()

    def _recentlyReset(self):
        if not self.lastResetTime:
            return False
        elif time.time() < self.lastResetTime + constants.MPV_NEWFILE_IGNORE_TIME:
            return True
        else:
            return False

    def _onFileUpdate(self):
        self.fileLoaded = True
        self.lastLoadedTime = time.time()
        self.reactor.callFromThread(self._client.updateFile, self._filename, self._duration, self._filepath)
        if not (self._recentlyReset()):
            self.reactor.callFromThread(self.setPosition, self._client.getGlobalPosition())
        if self._paused != self._client.getGlobalPaused():
            self.reactor.callFromThread(self._client.getGlobalPaused)

    def _fileIsLoaded(self):
        if self.fileLoaded == True and self.lastLoadedTime != None and time.time() > (self.lastLoadedTime + constants.MPV_NEWFILE_IGNORE_TIME):
            return True
        else:
            return False