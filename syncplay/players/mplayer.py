import subprocess
import re
import threading
import time
from syncplay.players.basePlayer import BasePlayer
from syncplay import constants, utils
from syncplay.messages import getMessage
import os, sys

class MplayerPlayer(BasePlayer):
    speedSupported = True
    customOpenDialog = False
    secondaryOSDSupported = False
    chatOSDSupported = False
    osdMessageSeparator = "; "

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
        self.delayedFilePath = None
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

    def displayMessage(self, message, duration=(constants.OSD_DURATION * 1000), secondaryOSD=False):
        message = self._sanitizeText(message.replace("\\n","<NEWLINE>")).replace("<NEWLINE>","\\n")
        self._listener.sendLine(u'{} "{!s}" {} {}'.format(self.OSD_QUERY, message, duration, constants.MPLAYER_OSD_LEVEL).encode('utf-8'))

    def displayChatMessage(self, username, message):
        username = self._sanitizeText(username)
        message = self._sanitizeText(message)
        messageString = u"<{}> {}".format(username, message)
        self._listener.sendLine(u'script-message-to syncplayintf chat "{}"'.format(messageString))

    def setSpeed(self, value):
        self._setProperty('speed', "{:.2f}".format(value))

    def _loadFile(self, filePath):
        self._listener.sendLine(u'loadfile {}'.format(self._quoteArg(filePath)))

    def openFile(self, filePath, resetPosition=False):
        self._filepath = filePath
        self._loadFile(filePath)
        self._onFileUpdate()
        if self._paused != self._client.getGlobalPaused():
            self.setPaused(self._client.getGlobalPaused())
        self.setPosition(self._client.getGlobalPosition())

    def setPosition(self, value):
        self._position = max(value,0)
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

    def _sanitizeText(self, text):
        text = text.replace("\r", "")
        text = text.replace("\n", "")
        text = text.replace("\\", u"\\\\\\uFEFF")
        text = text.replace("{", "\\\\{")
        text = text.replace("}", "\\\\}")
        return text

    def _quoteArg(self, arg):
        arg = arg.replace('\\', '\\\\')
        arg = arg.replace("'", "\\'")
        arg = arg.replace('"', '\\"')
        arg = arg.replace("\r", "")
        arg = arg.replace("\n", "")
        return u'"{}"'.format(arg)

    def _fileIsLoaded(self):
        return True

    def _handleUnknownLine(self, line):
        pass

    def _storePosition(self, value):
        self._position = max(value,0)

    def _storePauseState(self, value):
        self._paused = value

    def lineReceived(self, line):
        if line:
            self._client.ui.showDebugMessage("player << {}".format(line))
        if "Failed to get value of property" in line or "=(unavailable)" in line or line == "ANS_filename=" or line == "ANS_length=" or line == "ANS_path=":
            if "filename" in line:
                self._getFilename()
            elif "length" in line:
                self._getLength()
            elif "path" in line:
                self._getFilepath()
            return
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
    def getStartupArgs(path, userArgs):
        args = []
        if userArgs:
            args.extend(userArgs)
        args.extend(constants.MPLAYER_SLAVE_ARGS)
        return args

    @staticmethod
    def isValidPlayerPath(path):
        if "mplayer" in path and MplayerPlayer.getExpandedPath(path)  and not "mplayerc.exe" in path: # "mplayerc.exe" is Media Player Classic (not Home Cinema):
            return True
        return False

    @staticmethod
    def getPlayerPathErrors(playerPath, filePath):
        if not filePath:
            return getMessage("no-file-path-config-error")

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
            self.sendQueue = []
            self.readyToSend = True
            self.lastSendTime = None
            self.lastNotReadyTime = None
            self.__playerController = playerController
            if self.__playerController.getPlayerPathErrors(playerPath,filePath):
                raise ValueError()
            if filePath and '://' not in filePath:
                if not os.path.isfile(filePath) and 'PWD' in os.environ:
                    filePath = os.environ['PWD'] + os.path.sep + filePath
                filePath = os.path.realpath(filePath)

            call = [playerPath]
            if filePath:
                if sys.platform.startswith('win') and not utils.isASCII(filePath):
                    self.__playerController.delayedFilePath = filePath
                    filePath = None
                else:
                    call.extend([filePath])
            call.extend(playerController.getStartupArgs(playerPath, args))
            # At least mpv may output escape sequences which result in syncplay
            # trying to parse something like
            # "\x1b[?1l\x1b>ANS_filename=blah.mkv". Work around this by
            # unsetting TERM.
            env = os.environ.copy()
            if 'TERM' in env:
                del env['TERM']
            if filePath:
                self.__process = subprocess.Popen(call, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self.__getCwd(filePath, env), env=env)
            else:
                self.__process = subprocess.Popen(call, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
            threading.Thread.__init__(self, name="MPlayer Listener")


        def __getCwd(self, filePath, env):
            if not filePath:
                return None
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

        def sendChat(self, message):
            self.__playerController.reactor.callFromThread(self.__playerController._client.sendChat, message)

        def isReadyForSend(self):
            self.checkForReadinessOverride()
            return self.readyToSend

        def setReadyToSend(self, newReadyState):
            oldState = self.readyToSend
            self.readyToSend = newReadyState
            self.lastNotReadyTime = time.time() if newReadyState == False else None
            if self.readyToSend == True:
                self.__playerController._client.ui.showDebugMessage("<mpv> Ready to send: True")
            else:
                self.__playerController._client.ui.showDebugMessage("<mpv> Ready to send: False")
            if self.readyToSend == True and oldState == False:
                self.processSendQueue()

        def checkForReadinessOverride(self):
            if self.lastNotReadyTime and time.time() - self.lastNotReadyTime > constants.MPV_MAX_NEWFILE_COOLDOWN_TIME:
                self.setReadyToSend(True)

        def sendLine(self, line, notReadyAfterThis=None):
            self.checkForReadinessOverride()
            if self.readyToSend == False and "print_text ANS_pause" in line:
                self.__playerController._client.ui.showDebugMessage("<mpv> Not ready to get status update, so skipping")
                return
            try:
                if self.sendQueue:
                    if constants.MPV_SUPERSEDE_IF_DUPLICATE_COMMANDS:
                        for command in constants.MPV_SUPERSEDE_IF_DUPLICATE_COMMANDS:
                            if line.startswith(command):
                                for itemID, deletionCandidate in enumerate(self.sendQueue):
                                    if deletionCandidate.startswith(command):
                                        self.__playerController._client.ui.showDebugMessage(u"<mpv> Remove duplicate (supersede): {}".format(self.sendQueue[itemID]))
                                        self.sendQueue.remove(self.sendQueue[itemID])
                                        break
                            break
                    if constants.MPV_REMOVE_BOTH_IF_DUPLICATE_COMMANDS:
                        for command in constants.MPV_REMOVE_BOTH_IF_DUPLICATE_COMMANDS:
                            if line == command:
                                for itemID, deletionCandidate in enumerate(self.sendQueue):
                                    if deletionCandidate == command:
                                        self.__playerController._client.ui.showDebugMessage(u"<mpv> Remove duplicate (delete both): {}".format(self.sendQueue[itemID]))
                                        self.__playerController._client.ui.showDebugMessage(self.sendQueue[itemID])
                                        return
            except:
                self.__playerController._client.ui.showDebugMessage("<mpv> Problem removing duplicates, etc")
            self.sendQueue.append(line)
            self.processSendQueue()
            if notReadyAfterThis:
                self.setReadyToSend(False)

        def processSendQueue(self):
            while self.sendQueue and self.readyToSend:
                if self.lastSendTime and time.time() - self.lastSendTime < constants.MPV_SENDMESSAGE_COOLDOWN_TIME:
                    self.__playerController._client.ui.showDebugMessage("<mpv> Throttling message send, so sleeping for {}".format(constants.MPV_SENDMESSAGE_COOLDOWN_TIME))
                    time.sleep(constants.MPV_SENDMESSAGE_COOLDOWN_TIME)
                try:
                    lineToSend = self.sendQueue.pop()
                    if lineToSend:
                        self.lastSendTime = time.time()
                        self.actuallySendLine(lineToSend)
                except IndexError:
                    pass

        def actuallySendLine(self, line):
            try:
                if not isinstance(line, unicode):
                    line = line.decode('utf8')
                line = (line + u"\n").encode('utf8')
                self.__playerController._client.ui.showDebugMessage("player >> {}".format(line))
                self.__process.stdin.write(line)
            except IOError:
                pass
