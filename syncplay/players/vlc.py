import subprocess
import re
import threading
from syncplay.players.basePlayer import BasePlayer
from syncplay import constants
import os
import random
import socket
import asynchat, asyncore
from syncplay.messages import getMessage
import time

class VlcPlayer(BasePlayer):
    speedSupported = True
    RE_ANSWER = re.compile(r"(?:^(?P<command>[a-zA-Z_]+)(?:\: )?(?P<argument>.*))")
    VLC_MIN_PORT = 10000
    VLC_MAX_PORT = 55000
    SLAVE_ARGS = ['--extraintf=luaintf','--lua-intf=syncplay']
    VLC_MIN_VERSION = "2.0.6"
    
    random.seed()
    vlcport = random.randrange(VLC_MIN_PORT, VLC_MAX_PORT) if (VLC_MIN_PORT < VLC_MAX_PORT) else VLC_MIN_PORT
    SLAVE_ARGS.append('--lua-config=syncplay={{port=\"{}\"}}'.format(str(vlcport)))
    
    def __init__(self, client, playerPath, filePath, args):
        self._client = client
        self._paused = None
        self._duration = None
        self._filename = None
        self._filepath = None
        
        self._durationAsk = threading.Event()
        self._filenameAsk = threading.Event()
        self._pathAsk = threading.Event()
        self._positionAsk = threading.Event()
        self._pausedAsk = threading.Event()
        self._vlcready = threading.Event()
        try:
            self._listener = self.__Listener(self, playerPath, filePath, args, self._vlcready)
        except ValueError:
            self._client.ui.showMessage(getMessage("en", "vlc-failed-connection"))
            self._client.stop(True)
            return 
        self._listener.setDaemon(True)
        self._listener.start()
        if(not self._vlcready.wait(constants.VLC_OPEN_MAX_WAIT_TIME)):
            self._vlcready.set()
            self._client.ui.showMessage(getMessage("en", "vlc-failed-connection"))
            self._client.stop(True)
        self._client.initPlayer(self)
        
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
        self._client.updateFile(self._filename, self._duration, self._filepath)
        self.setPaused(self._client.getGlobalPaused()) 
        self.setPosition(self._client.getGlobalPosition())

    def askForStatus(self):
        self._positionAsk.clear()
        self._pausedAsk.clear()
        self._listener.sendLine(".")
        self._positionAsk.wait()
        self._pausedAsk.wait()
        self._client.updatePlayerStatus(self._paused, self._position)
                
    def displayMessage(self, message, duration = constants.OSD_DURATION * 1000):
        duration /= 1000
        self._listener.sendLine('display-osd: {}, {}, {}'.format('top-right', duration, message))
 
    def setSpeed(self, value):        
        self._listener.sendLine("set-rate: {:.2f}".format(value))

    def setPosition(self, value):
        self._position = value
        self._listener.sendLine("set-position: {}".format(value))
    
    def setPaused(self, value):
        self._paused = value
        self._listener.sendLine('set-playstate: {}'.format("paused" if value else "playing"))
    
    def _getFileInfo(self):
        self._listener.sendLine("get-duration")
        self._listener.sendLine("get-filepath")
        self._listener.sendLine("get-filename")

    def lineReceived(self, line):      
        match, name, value = self.RE_ANSWER.match(line), "", ""
        if match:
            name, value = match.group('command'), match.group('argument')
  
        if(line == "filepath-change-notification"):
            t = threading.Thread(target=self._onFileUpdate)
            t.setDaemon(True)
            t.start()
        elif (name == "filepath" and value != "no-input"):
            if("file://" in value):
                value = value.replace("file://", "")
                if(not os.path.isfile(value)):
                    value = value.lstrip("/")
            self._filepath = value
            self._pathAsk.set()
        elif(name == "duration" and (value != "no-input")):
            self._duration = float(value.replace(",", "."))
            self._durationAsk.set()
        elif(name == "playstate"):
            self._paused = bool(value != 'playing') if(value != "no-input") else self._client.getGlobalPaused()
            self._pausedAsk.set()
        elif(name == "position"):
            self._position = float(value.replace(",", ".")) if (value != "no-input") else self._client.getGlobalPosition()
            self._positionAsk.set()
        elif(name == "filename"):
            self._filename = value
            self._filenameAsk.set()
        elif (line[:16] == "VLC media player"):
            vlc_version = line[17:22]
            if (int(vlc_version.replace(".","")) < int(self.VLC_MIN_VERSION.replace(".",""))):
                self._client.ui.showMessage(getMessage("en", "vlc-version-mismatch").format(str(vlc_version), str(self.VLC_MIN_VERSION)))
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
        if("vlc" in path and VlcPlayer.getExpandedPath(path)):
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

    def drop(self):
        self._listener.sendLine('close-vlc')
        self._durationAsk.set()
        self._filenameAsk.set()
        self._pathAsk.set()
        self._positionAsk.set()
        self._vlcready.set()
        self._pausedAsk.set()
        self._client.stop(False)

    class __Listener(threading.Thread, asynchat.async_chat):
        def __init__(self, playerController, playerPath, filePath, args, vlcReady):
            self.__playerController = playerController
            call = [playerPath]
            if(filePath):
                call.append(filePath)
            call.extend(playerController.SLAVE_ARGS)
            if(args): 
                call.extend(args)
            
            self._vlcready = vlcReady
            self.__process = subprocess.Popen(call, stderr=subprocess.PIPE)
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
            time.sleep(constants.VLC_SOCKET_OPEN_WAIT_TIME)
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
#            print "received: {}".format("".join(self._ibuffer))
            self.__playerController.lineReceived("".join(self._ibuffer))
            self._ibuffer = []

        def sendLine(self, line):
            if(self.connected):
#                print "send: {}".format(line)
                self.push(line + "\n")
