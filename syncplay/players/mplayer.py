import subprocess
import re
import threading
import time
from syncplay.players.basePlayer import BasePlayer
from syncplay import constants
from syncplay.messages import getMessage
import os

class MplayerPlayer(BasePlayer):
    speedSupported = True
    RE_ANSWER = re.compile(constants.MPLAYER_ANSWER_REGEX)
    POSITION_QUERY = 'time_pos'
    OSD_QUERY = 'osd_show_text'

    def __init__(self, client, playerPath, filePath, args):
        from twisted.internet import reactor
        self.reactor = reactor
        self._client = client
        self._paused = None
        self._position = 0.0
        self._duration = None
        self._filename = None
        self._filepath = None
        self.quitReason = None
        self.lastLoadedTime = None
        self.fileLoaded = False
        try:
            self._listener = self.__Listener(self, playerPath, filePath, args)
        except ValueError:
            self._client.ui.showMessage(getMessage("mplayer-file-required-notification"))
            self._client.ui.showMessage(getMessage("mplayer-file-required-notification/example"))
            self.drop()
            return
        self._listener.setDaemon(True)
        self._listener.start()

        self._durationAsk = threading.Event()
        self._filenameAsk = threading.Event()
        self._pathAsk = threading.Event()

        self._positionAsk = threading.Event()
        self._pausedAsk = threading.Event()

        self._preparePlayer()

    def _fileUpdateClearEvents(self):
        self._durationAsk.clear()
        self._filenameAsk.clear()
        self._pathAsk.clear()

    def _fileUpdateWaitEvents(self):
        self._durationAsk.wait()
        self._filenameAsk.wait()
        self._pathAsk.wait()

    def _onFileUpdate(self):
        self._fileUpdateClearEvents()
        self._getFilename()
        self._getLength()
        self._getFilepath()
        self._fileUpdateWaitEvents()
        self._client.updateFile(self._filename, self._duration, self._filepath)

    def _preparePlayer(self):
        self.setPaused(True)
        self.reactor.callLater(0, self._client.initPlayer, self)
        self._onFileUpdate()

    def askForStatus(self):
        self._positionAsk.clear()
        self._pausedAsk.clear()
        self._getPaused()
        self._getPosition()
        self._positionAsk.wait()
        self._pausedAsk.wait()
        self._client.updatePlayerStatus(self._paused, self._position)

    def _setProperty(self, property_, value):
        self._listener.sendLine("set_property {} {}".format(property_, value))

    def _getProperty(self, property_):
        self._listener.sendLine("get_property {}".format(property_))

    def displayMessage(self, message, duration=(constants.OSD_DURATION * 1000)):
        self._listener.sendLine(u'{} "{!s}" {} {}'.format(self.OSD_QUERY, message, duration, constants.MPLAYER_OSD_LEVEL).encode('utf-8'))

    def setSpeed(self, value):
        self._setProperty('speed', "{:.2f}".format(value))

    def _loadFile(self, filePath):
        self._listener.sendLine(u'loadfile {}'.format(self._quoteArg(filePath)))

    def openFile(self, filePath):
        self._loadFile(filePath)
        self._onFileUpdate()
        if self._paused != self._client.getGlobalPaused():
            self.setPaused(self._client.getGlobalPaused())
        self.setPosition(self._client.getGlobalPosition())

    def setPosition(self, value):
        self._position = value
        self._setProperty(self.POSITION_QUERY, "{}".format(value))
        time.sleep(0.03)

    def setPaused(self, value):
        if self._paused <> value:
            self._paused = not self._paused
            self._listener.sendLine('pause')

    def _getFilename(self):
        self._getProperty('filename')

    def _getLength(self):
        self._getProperty('length')

    def _getFilepath(self):
        self._getProperty('path')

    def _getPaused(self):
        self._getProperty('pause')

    def _getPosition(self):
        self._getProperty(self.POSITION_QUERY)

    def _quoteArg(self, arg):
        arg = arg.replace('\\', '\\\\')
        arg = arg.replace("'", "\\'")
        arg = arg.replace('"', '\\"')
        return u'"{}"'.format(arg)

    def _fileIsLoaded(self):
        return True

    def _clearFileLoaded(self):
        pass

    def _handleUnknownLine(self, line):
        pass

    def _storePosition(self, value):
        self._position = value

    def _storePauseState(self, value):
        self._paused = value

    def lineReceived(self, line):
        match = self.RE_ANSWER.match(line)
        if not match:
            self._handleUnknownLine(line)
            return

        name, value =[m for m in match.groups() if m]
        name = name.lower()

        if name == self.POSITION_QUERY:
            self._storePosition(float(value))
            self._positionAsk.set()
        elif name == "pause":
            self._storePauseState(bool(value == 'yes'))
            self._pausedAsk.set()
        elif name == "length":
            self._duration = float(value)
            self._durationAsk.set()
        elif name == "path":
            self._filepath = value
            self._pathAsk.set()
        elif name == "filename":
            self._filename = value.decode('utf-8')
            self._filenameAsk.set()
        elif name == "exiting":
            if value != 'Quit':
                if self.quitReason is None:
                    self.quitReason = getMessage("media-player-error").format(value)
                self.reactor.callFromThread(self._client.ui.showErrorMessage, self.quitReason, True)
            self.drop()

    @staticmethod
    def run(client, playerPath, filePath, args):
        mplayer = MplayerPlayer(client, MplayerPlayer.getExpandedPath(playerPath), filePath, args)
        return mplayer

    @staticmethod
    def getDefaultPlayerPathsList():
        l = []
        for path in constants.MPLAYER_PATHS:
            p = MplayerPlayer.getExpandedPath(path)
            if p:
                l.append(p)
        return l

    @staticmethod
    def getIconPath(path):
        return constants.MPLAYER_ICONPATH

    @staticmethod
    def getStartupArgs(path):
        return constants.MPLAYER_SLAVE_ARGS

    @staticmethod
    def isValidPlayerPath(path):
        if "mplayer" in path and MplayerPlayer.getExpandedPath(path):
            return True
        return False

    @staticmethod
    def getExpandedPath(playerPath):
        if not os.path.isfile(playerPath):
            if os.path.isfile(playerPath + u"mplayer.exe"):
                playerPath += u"mplayer.exe"
                return playerPath
            elif os.path.isfile(playerPath + u"\\mplayer.exe"):
                playerPath += u"\\mplayer.exe"
                return playerPath
        if os.access(playerPath, os.X_OK):
            return playerPath
        for path in os.environ['PATH'].split(':'):
            path = os.path.join(os.path.realpath(path), playerPath)
            if os.access(path, os.X_OK):
                return path

    def notMplayer2(self):
        self.reactor.callFromThread(self._client.ui.showErrorMessage, getMessage("mplayer2-required"), True)
        self.drop()

    def _takeLocksDown(self):
        self._durationAsk.set()
        self._filenameAsk.set()
        self._pathAsk.set()
        self._positionAsk.set()
        self._pausedAsk.set()

    def drop(self):
        self._listener.sendLine('quit')
        self._takeLocksDown()
        self.reactor.callFromThread(self._client.stop, True)

    class __Listener(threading.Thread):
        def __init__(self, playerController, playerPath, filePath, args):
            self.__playerController = playerController
            if not filePath:
                raise ValueError()
            if '://' not in filePath:
                if not os.path.isfile(filePath) and 'PWD' in os.environ:
                    filePath = os.environ['PWD'] + os.path.sep + filePath
                filePath = os.path.realpath(filePath)

            call = [playerPath, filePath]
            call.extend(playerController.getStartupArgs(playerPath))
            if args:
                call.extend(args)
            # At least mpv may output escape sequences which result in syncplay
            # trying to parse something like
            # "\x1b[?1l\x1b>ANS_filename=blah.mkv". Work around this by
            # unsetting TERM.
            env = os.environ.copy()
            if 'TERM' in env:
                del env['TERM']
            self.__process = subprocess.Popen(call, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self.__getCwd(filePath, env), env=env)
            threading.Thread.__init__(self, name="MPlayer Listener")


        def __getCwd(self, filePath, env):
            if os.path.isfile(filePath):
                cwd = os.path.dirname(filePath)
            elif 'HOME' in env:
                cwd = env['HOME']
            elif 'APPDATA' in env:
                cwd = env['APPDATA']
            else:
                cwd = None
            return cwd

        def run(self):
            line = self.__process.stdout.readline()
            if "MPlayer 1" in line:
                self.__playerController.notMplayer2()
            else:
                line = line.rstrip("\r\n")
                self.__playerController.lineReceived(line)
            while self.__process.poll() is None:
                line = self.__process.stdout.readline()
                line = line.rstrip("\r\n")
                self.__playerController.lineReceived(line)
            self.__playerController.drop()

        def sendLine(self, line):
            try:
                line = (line.decode('utf8') + u"\n").encode('utf8')
                self.__process.stdin.write(line)
            except IOError:
                pass
