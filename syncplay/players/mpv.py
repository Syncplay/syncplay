import re
import subprocess
from syncplay.players.mplayer import MplayerPlayer
from syncplay.messages import getMessage
from syncplay import constants
from syncplay.utils import isURL
import os, sys, time

class MpvPlayer(MplayerPlayer):
    RE_VERSION = re.compile('.*mpv (\d+)\.(\d+)\.\d+.*')
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
    def getStartupArgs(path, userArgs):
        args = constants.MPV_ARGS
        if userArgs:
            args.extend(userArgs)
        args.extend(constants.MPV_SLAVE_ARGS)
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
        self._listener.sendLine(u"no-osd set {} {}".format(property_, value))

    def setPaused(self, value):
        if self._paused <> value:
            self._paused = not self._paused
            self._listener.sendLine('cycle pause')

    def mpvErrorCheck(self, line):
        if "Error parsing option" in line or "Error parsing commandline option" in line:
            self.quitReason = getMessage("mpv-version-error")

        elif "Could not open pipe at '/dev/stdin'" in line:
            self.reactor.callFromThread(self._client.ui.showErrorMessage, getMessage("mpv-version-error"), True)
            self.drop()

        if constants and any(errormsg in line for errormsg in constants.MPV_ERROR_MESSAGES_TO_REPEAT):
            self._client.ui.showErrorMessage(line)

    def _handleUnknownLine(self, line):
        self.mpvErrorCheck(line)
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
    lastMPVPositionUpdate = None

    def setPaused(self, value):
        if self._paused == value:
            self._client.ui.showDebugMessage("Not sending setPaused to mpv as state is already {}".format(value))
            return
        pauseValue = "yes" if value else "no"
        self._setProperty("pause", pauseValue)
        self._paused = value
        if value == False:
            self.lastMPVPositionUpdate = time.time()

    def _getProperty(self, property_):
        floatProperties = ['time-pos']
        if property_ in floatProperties:
            propertyID = u"={}".format(property_)
        elif property_ == 'length':
            propertyID = u'=length:${=duration:0}'
        else:
            propertyID = property_
        self._listener.sendLine(u"print_text ""ANS_{}=${{{}}}""".format(property_, propertyID))

    def getCalculatedPosition(self):
        if self.fileLoaded == False:
            self._client.ui.showDebugMessage("File not loaded so using GlobalPosition for getCalculatedPosition({})".format(self._client.getGlobalPosition()))
            return self._client.getGlobalPosition()

        if self.lastMPVPositionUpdate is None:
            self._client.ui.showDebugMessage("MPV not updated position so using GlobalPosition for getCalculatedPosition ({})".format(self._client.getGlobalPosition()))
            return self._client.getGlobalPosition()

        if self._recentlyReset():
            self._client.ui.showDebugMessage("Recently reset so using self.position for getCalculatedPosition ({})".format(self._position))
            return self._position

        diff = time.time() - self.lastMPVPositionUpdate

        if diff > constants.MPV_UNRESPONSIVE_THRESHOLD:
            self.reactor.callFromThread(self._client.ui.showErrorMessage, getMessage("mpv-unresponsive-error").format(int(diff)), True)
            self.drop()
        if diff > constants.PLAYER_ASK_DELAY and not self._paused:
            self._client.ui.showDebugMessage("mpv did not response in time, so assuming position is {} ({}+{})".format(self._position + diff, self._position, diff))
            return self._position + diff
        else:
            return self._position

    def _storePosition(self, value):
        self.lastMPVPositionUpdate = time.time()
        if self._recentlyReset():
            self._client.ui.showDebugMessage("Recently reset, so storing position as 0")
            self._position = 0
        elif self._fileIsLoaded() or (value < constants.MPV_NEWFILE_IGNORE_TIME and self._fileIsLoaded(ignoreDelay=True)):
            self._position = max(value,0)
        else:
            self._client.ui.showDebugMessage("No file loaded so storing position as GlobalPosition ({})".format(self._client.getGlobalPosition()))
            self._position = self._client.getGlobalPosition()

    def _storePauseState(self, value):
        if self._fileIsLoaded():
            self._paused = value
        else:
            self._paused = self._client.getGlobalPaused()

    def askForStatus(self):
        self._positionAsk.clear()
        self._pausedAsk.clear()
        if not self._listener.isReadyForSend:
            self._client.ui.showDebugMessage("mpv not ready for update")
            return

        self._getPausedAndPosition()
        self._positionAsk.wait(constants.MPV_LOCK_WAIT_TIME)
        self._pausedAsk.wait(constants.MPV_LOCK_WAIT_TIME)
        self._client.updatePlayerStatus(self._paused if self.fileLoaded else self._client.getGlobalPaused(), self.getCalculatedPosition())

    def _getPausedAndPosition(self):
        self._listener.sendLine(u"print_text ANS_pause=${pause}\r\nprint_text ANS_time-pos=${=time-pos}")

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
        self._listener.sendLine(u'loadfile {}'.format(self._quoteArg(filePath)), notReadyAfterThis=True)

    def setPosition(self, value):
        if value < constants.DO_NOT_RESET_POSITION_THRESHOLD and self._recentlyReset():
            self._client.ui.showDebugMessage("Did not seek as recently reset and {} below 'do not reset position' threshold".format(value))
            return
        super(self.__class__, self).setPosition(value)
        self.lastMPVPositionUpdate = time.time()

    def openFile(self, filePath, resetPosition=False):
        self._client.ui.showDebugMessage("openFile, resetPosition=={}".format(resetPosition))
        if resetPosition:
            self.lastResetTime = time.time()
            if isURL(filePath):
                self.lastResetTime += constants.STREAM_ADDITIONAL_IGNORE_TIME
        self._loadFile(filePath)
        if self._paused != self._client.getGlobalPaused():
            self._client.ui.showDebugMessage("Want to set paused to {}".format(self._client.getGlobalPaused()))
        else:
            self._client.ui.showDebugMessage("Don't want to set paused to {}".format(self._client.getGlobalPaused()))
        if resetPosition == False:
            self.setPosition(self._client.getGlobalPosition())
        else:
            self._storePosition(0)

    def _handleUnknownLine(self, line):
        self.mpvErrorCheck(line)

        if line == "<SyncplayUpdateFile>" or "Playing:" in line:
            self._listener.setReadyToSend(False)
            self._clearFileLoaded()

        elif line == "</SyncplayUpdateFile>":
            self._onFileUpdate()
            self._listener.setReadyToSend(True)

        elif "Failed" in line or "failed" in line or "No video or audio streams selected" in line or "error" in line:
            self._listener.setReadyToSend(True)

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

    def _fileIsLoaded(self, ignoreDelay=False):
        if ignoreDelay:
            self._client.ui.showDebugMessage("Ignoring _fileIsLoaded MPV_NEWFILE delay")
            return True if self.fileLoaded else False

        if self.fileLoaded == True and self.lastLoadedTime != None and time.time() > (self.lastLoadedTime + constants.MPV_NEWFILE_IGNORE_TIME):
            return True
        else:
            return False