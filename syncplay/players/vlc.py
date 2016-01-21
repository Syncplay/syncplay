import subprocess
import re
import threading
from syncplay.players.basePlayer import BasePlayer
from syncplay import constants, utils
import os
import sys
import random
import socket
import asynchat, asyncore
import urllib
import time
from syncplay.messages import getMessage

class VlcPlayer(BasePlayer):
    speedSupported = True
    customOpenDialog = False
    secondaryOSDSupported = True
    osdMessageSeparator = "; "

    RE_ANSWER = re.compile(constants.VLC_ANSWER_REGEX)
    SLAVE_ARGS = constants.VLC_SLAVE_ARGS
    if not sys.platform.startswith('darwin'):
         SLAVE_ARGS.extend(constants.VLC_SLAVE_NONOSX_ARGS)
    random.seed()
    vlcport = random.randrange(constants.VLC_MIN_PORT, constants.VLC_MAX_PORT) if (constants.VLC_MIN_PORT < constants.VLC_MAX_PORT) else constants.VLC_MIN_PORT

    def __init__(self, client, playerPath, filePath, args):
        from twisted.internet import reactor
        self.reactor = reactor
        self._client = client
        self._paused = None
        self._duration = None
        self._filename = None
        self._filepath = None
        self._filechanged = False
        self._lastVLCPositionUpdate = None
        self.shownVLCLatencyError = False
        try: # Hack to fix locale issue without importing locale library
            self.radixChar = "{:n}".format(1.5)[1:2]
            if self.radixChar == "" or self.radixChar == "1" or self.radixChar == "5":
                raise ValueError
        except:
            self._client.ui.showErrorMessage("Failed to determine locale. As a fallback Syncplay is using the following radix character: \".\".")
            self.radixChar = "."

        self._durationAsk = threading.Event()
        self._filenameAsk = threading.Event()
        self._pathAsk = threading.Event()
        self._positionAsk = threading.Event()
        self._pausedAsk = threading.Event()
        self._vlcready = threading.Event()
        self._vlcclosed = threading.Event()
        try:
            self._listener = self.__Listener(self, playerPath, filePath, args, self._vlcready, self._vlcclosed)
        except ValueError:
            self._client.ui.showErrorMessage(getMessage("vlc-failed-connection"), True)
            self.reactor.callFromThread(self._client.stop, True,)
            return
        self._listener.setDaemon(True)
        self._listener.start()
        if not self._vlcready.wait(constants.VLC_OPEN_MAX_WAIT_TIME):
            self._vlcready.set()
            self._client.ui.showErrorMessage(getMessage("vlc-failed-connection"), True)
            self.reactor.callFromThread(self._client.stop, True,)
        self.reactor.callFromThread(self._client.initPlayer, self,)

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
        self._getFileInfo()
        self._fileUpdateWaitEvents()
        args = (self._filename, self._duration, self._filepath)
        self.reactor.callFromThread(self._client.updateFile, *args)
        self.setPaused(self._client.getGlobalPaused())
        self.setPosition(self._client.getGlobalPosition())

    def askForStatus(self, cookie=None):
        self._filechanged = False
        self._positionAsk.clear()
        self._pausedAsk.clear()
        self._listener.sendLine(".")
        if self._filename and not self._filechanged:
            self._positionAsk.wait(constants.PLAYER_ASK_DELAY)
            self._client.updatePlayerStatus(self._paused,
                                            self.getCalculatedPosition(),
                                            cookie=cookie)
        else:
            self._client.updatePlayerStatus(self._client.getGlobalPaused(),
                                            self._client.getGlobalPosition(),
                                            cookie=cookie)

    def getCalculatedPosition(self):
        if self._lastVLCPositionUpdate is None:
            return self._client.getGlobalPosition()
        diff = time.time() - self._lastVLCPositionUpdate
        if diff > constants.PLAYER_ASK_DELAY and not self._paused:
            self._client.ui.showDebugMessage("VLC did not response in time, so assuming position is {} ({}+{})".format(self._position + diff, self._position, diff))
            if diff > constants.VLC_LATENCY_ERROR_THRESHOLD:
                if not self.shownVLCLatencyError or constants.DEBUG_MODE:
                    self._client.ui.showErrorMessage(getMessage("media-player-latency-warning").format(int(diff)))
                    self.shownVLCLatencyError = True
            return self._position + diff
        else:
            return self._position

    def displayMessage(self, message, duration=constants.OSD_DURATION * 1000, secondaryOSD=False):
        duration /= 1000
        if secondaryOSD == False:
            self._listener.sendLine('display-osd: {}, {}, {}'.format('top-right', duration, message.encode('utf8')))
        else:
            self._listener.sendLine('display-secondary-osd: {}, {}, {}'.format('center', duration, message.encode('utf8')))

    def setSpeed(self, value):
        self._listener.sendLine("set-rate: {:.2n}".format(value))

    def setPosition(self, value):
        self._lastVLCPositionUpdate = time.time()
        self._listener.sendLine("set-position: {}".format(value).replace(".",self.radixChar))

    def setPaused(self, value):
        self._paused = value
        if not value:
            self._lastVLCPositionUpdate = time.time()
        self._listener.sendLine('set-playstate: {}'.format("paused" if value else "playing"))

    def getMRL(self, fileURL):
        fileURL = fileURL.replace(u'\\', u'/')
        fileURL = fileURL.encode('utf8')
        fileURL = urllib.quote_plus(fileURL)
        if sys.platform.startswith('win'):
            fileURL = "file:///" + fileURL
        else:
            fileURL = "file://" + fileURL
        fileURL = fileURL.replace("+", "%20")
        return fileURL

    def openFile(self, filePath, resetPosition=False):
        if utils.isASCII(filePath):
            self._listener.sendLine('load-file: {}'.format(filePath.encode('ascii', 'ignore')))
        else:
            fileURL = self.getMRL(filePath)
            self._listener.sendLine('load-file: {}'.format(fileURL))

    def _getFileInfo(self):
        self._listener.sendLine("get-duration")
        self._listener.sendLine("get-filepath")
        self._listener.sendLine("get-filename")

    def lineReceived(self, line):
        try:
            self._client.ui.showDebugMessage("player << {}".format(line))
        except:
            pass
        match, name, value = self.RE_ANSWER.match(line), "", ""
        if match:
            name, value = match.group('command'), match.group('argument')

        if line == "filepath-change-notification":
            self._filechanged = True
            t = threading.Thread(target=self._onFileUpdate)
            t.setDaemon(True)
            t.start()
        elif name == "filepath":
            self._filechanged = True
            if value == "no-input":
                self._filepath = None
            else:
                if "file://" in value:
                    value = value.replace("file://", "")
                    if not os.path.isfile(value):
                        value = value.lstrip("/")
                self._filepath = value
            self._pathAsk.set()
        elif name == "duration":
            if value == "no-input":
                self._duration = 0
            else:
                self._duration = float(value.replace(",", "."))
            self._durationAsk.set()
        elif name == "playstate":
            self._paused = bool(value != 'playing') if(value != "no-input" and self._filechanged == False) else self._client.getGlobalPaused()
            self._pausedAsk.set()
        elif name == "position":
            self._position = float(value.replace(",", ".")) if (value != "no-input" and self._filechanged == False) else self._client.getGlobalPosition()
            self._lastVLCPositionUpdate = time.time()
            self._positionAsk.set()
        elif name == "filename":
            self._filechanged = True
            self._filename = value.decode('utf-8')
            self._filenameAsk.set()
        elif line.startswith("vlc-version: "):
            vlc_version = line.split(': ')[1].replace(' ','-').split('-')[0]
            if not utils.meetsMinVersion(vlc_version, constants.VLC_MIN_VERSION):
                self._client.ui.showErrorMessage(getMessage("vlc-version-mismatch").format(str(vlc_version), str(constants.VLC_MIN_VERSION)))
            self._vlcready.set()

    @staticmethod
    def run(client, playerPath, filePath, args):
        vlc = VlcPlayer(client, VlcPlayer.getExpandedPath(playerPath), filePath, args)
        return vlc

    @staticmethod
    def getDefaultPlayerPathsList():
        l = []
        for path in constants.VLC_PATHS:
            p = VlcPlayer.getExpandedPath(path)
            if p:
                l.append(p)
        return l

    @staticmethod
    def isValidPlayerPath(path):
        if "vlc" in path.lower() and VlcPlayer.getExpandedPath(path):
            return True
        return False

    @staticmethod
    def getPlayerPathErrors(playerPath, filePath):
        return None

    @staticmethod
    def getIconPath(path):
        return constants.VLC_ICONPATH

    @staticmethod
    def getExpandedPath(playerPath):
        if not os.path.isfile(playerPath):
            if os.path.isfile(playerPath + u"vlc.exe"):
                playerPath += u"vlc.exe"
                return playerPath
            elif os.path.isfile(playerPath + u"\\vlc.exe"):
                playerPath += u"\\vlc.exe"
                return playerPath
        if os.access(playerPath, os.X_OK):
            return playerPath
        for path in os.environ['PATH'].split(':'):
            path = os.path.join(os.path.realpath(path), playerPath)
            if os.access(path, os.X_OK):
                return path

    def drop(self):
        self._vlcclosed.clear()
        self._listener.sendLine('close-vlc')
        self._vlcclosed.wait()
        self._durationAsk.set()
        self._filenameAsk.set()
        self._pathAsk.set()
        self._positionAsk.set()
        self._vlcready.set()
        self._pausedAsk.set()
        self.reactor.callFromThread(self._client.stop, False,)

    class __Listener(threading.Thread, asynchat.async_chat):
        def __init__(self, playerController, playerPath, filePath, args, vlcReady, vlcClosed):
            self.__playerController = playerController
            self.requestedVLCVersion = False
            call = [playerPath]
            if filePath:
                if utils.isASCII(filePath):
                    call.append(filePath)
                else:
                    call.append(self.__playerController.getMRL(filePath))
            def _usevlcintf(vlcIntfPath, vlcIntfUserPath):
                vlcSyncplayInterfacePath = vlcIntfPath + "syncplay.lua"
                if not os.path.isfile(vlcSyncplayInterfacePath):
                    vlcSyncplayInterfacePath = vlcIntfUserPath + "syncplay.lua"
                if os.path.isfile(vlcSyncplayInterfacePath):
                    with open(vlcSyncplayInterfacePath, 'rU') as interfacefile:
                        for line in interfacefile:
                            if "local connectorversion" in line:
                                interface_version = line[26:31]
                                if utils.meetsMinVersion(interface_version, constants.VLC_INTERFACE_MIN_VERSION):
                                    return True
                                else:
                                    playerController._client.ui.showErrorMessage(getMessage("vlc-interface-oldversion-warning"))
                                    return False
                playerController._client.ui.showErrorMessage(getMessage("vlc-interface-not-installed"))
                return False
            if sys.platform.startswith('linux'):
                playerController.vlcIntfPath = "/usr/lib/vlc/lua/intf/"
                playerController.vlcIntfUserPath = os.path.join(os.getenv('HOME', '.'), ".local/share/vlc/lua/intf/")
            elif sys.platform.startswith('darwin'):
                playerController.vlcIntfPath = "/Applications/VLC.app/Contents/MacOS/share/lua/intf/"
                playerController.vlcIntfUserPath = os.path.join(os.getenv('HOME', '.'), "Library/Application Support/org.videolan.vlc/lua/intf/")
            elif 'bsd' in sys.platform or sys.platform.startswith('dragonfly'):
                # *BSD ports/pkgs install to /usr/local by default.
                # This should also work for all the other BSDs, such as OpenBSD or DragonFly.
                playerController.vlcIntfPath = "/usr/local/lib/vlc/lua/intf/"
                playerController.vlcIntfUserPath = os.path.join(os.getenv('HOME', '.'), ".local/share/vlc/lua/intf/")
            else:
                playerController.vlcIntfPath = os.path.dirname(playerPath).replace("\\", "/") + "/lua/intf/"
                playerController.vlcIntfUserPath = os.path.join(os.getenv('APPDATA', '.'), "VLC\\lua\\intf\\")
            playerController.vlcModulePath = playerController.vlcIntfPath + "modules/?.luac"
            if _usevlcintf(playerController.vlcIntfPath, playerController.vlcIntfUserPath):
                playerController.SLAVE_ARGS.append('--lua-config=syncplay={{port=\"{}\"}}'.format(str(playerController.vlcport)))
            else:
                if sys.platform.startswith('linux'):
                    playerController.vlcDataPath = "/usr/lib/syncplay/resources"
                else:
                    playerController.vlcDataPath = utils.findWorkingDir() + "\\resources"
                playerController.SLAVE_ARGS.append('--data-path={}'.format(playerController.vlcDataPath))
                playerController.SLAVE_ARGS.append('--lua-config=syncplay={{modulepath=\"{}\",port=\"{}\"}}'.format(playerController.vlcModulePath, str(playerController.vlcport)))

            call.extend(playerController.SLAVE_ARGS)
            if args:
                call.extend(args)

            self._vlcready = vlcReady
            self._vlcclosed = vlcClosed
            self.__process = subprocess.Popen(call, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            for line in iter(self.__process.stderr.readline, ''):
                if "[syncplay]" in line:
                    if "Listening on host" in line:
                        break
                    if "Hosting Syncplay" in line:
                        break
                    elif "Couldn't find lua interface" in line:
                        playerController._client.ui.showErrorMessage(getMessage("vlc-failed-noscript").format(line), True)
                        break
                    elif "lua interface error" in line:
                        playerController._client.ui.showErrorMessage(getMessage("media-player-error").format(line), True)
                        break
            self.__process.stderr = None
            threading.Thread.__init__(self, name="VLC Listener")
            asynchat.async_chat.__init__(self)
            self.set_terminator("\n")
            self._ibuffer = []
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sendingData = threading.Lock()

        def initiate_send(self):
            with self._sendingData:
                asynchat.async_chat.initiate_send(self)

        def run(self):
            self._vlcready.clear()
            self.connect(('localhost', self.__playerController.vlcport))
            asyncore.loop()

        def handle_connect(self):
            asynchat.async_chat.handle_connect(self)
            self._vlcready.set()

        def collect_incoming_data(self, data):
            self._ibuffer.append(data)

        def handle_close(self):
            asynchat.async_chat.handle_close(self)
            self.__playerController.drop()

        def found_terminator(self):
            self.__playerController.lineReceived("".join(self._ibuffer))
            self._ibuffer = []

        def sendLine(self, line):
            if self.connected:
                if not self.requestedVLCVersion:
                    self.requestedVLCVersion = True
                    self.sendLine("get-vlc-version")
                try:
                    self.push(line + "\n")
                    self.__playerController._client.ui.showDebugMessage("player >> {}".format(line))
                except:
                    pass
            if line == "close-vlc":
                self._vlcclosed.set()
