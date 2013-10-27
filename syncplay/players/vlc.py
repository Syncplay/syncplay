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
from syncplay.messages import getMessage
import time

class VlcPlayer(BasePlayer):
    speedSupported = True
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
        
        self._durationAsk = threading.Event()
        self._filenameAsk = threading.Event()
        self._pathAsk = threading.Event()
        self._positionAsk = threading.Event()
        self._pausedAsk = threading.Event()
        self._vlcready = threading.Event()
        try:
            self._listener = self.__Listener(self, playerPath, filePath, args, self._vlcready)
        except ValueError:
            self._client.ui.showErrorMessage(getMessage("en", "vlc-failed-connection"), True)
            self.reactor.callFromThread(self._client.stop, (True),)
            return 
        self._listener.setDaemon(True)
        self._listener.start()
        if(not self._vlcready.wait(constants.VLC_OPEN_MAX_WAIT_TIME)):
            self._vlcready.set()
            self._client.ui.showErrorMessage(getMessage("en", "vlc-failed-connection"), True)
            self.reactor.callFromThread(self._client.stop, (True),)
        self.reactor.callFromThread(self._client.initPlayer, (self),)
        
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

    def askForStatus(self):
        self._filechanged = False
        self._positionAsk.clear()
        self._pausedAsk.clear()
        self._listener.sendLine(".")
        if self._filechanged  == False:
            self._positionAsk.wait()
            self._pausedAsk.wait()
            self._client.updatePlayerStatus(self._paused, self._position)
        else:
            self._client.updatePlayerStatus(self._client.getGlobalPaused(), self._client.getGlobalPosition())
                
    def displayMessage(self, message, duration = constants.OSD_DURATION * 1000):
        duration /= 1000
        self._listener.sendLine('display-osd: {}, {}, {}'.format('top-right', duration, message.encode('ascii','ignore'))) #TODO: Proper Unicode support
 
    def setSpeed(self, value):        
        self._listener.sendLine("set-rate: {:.2n}".format(value))

    def setPosition(self, value):
        self._position = value
        self._listener.sendLine("set-position: {:n}".format(value))
    
    def setPaused(self, value):
        self._paused = value
        self._listener.sendLine('set-playstate: {}'.format("paused" if value else "playing"))
        
    def _isASCII (self, s):
        return all(ord(c) < 256 for c in s)
    
    def openFile(self, filePath):
        if (self._isASCII(filePath) == True):
            self._listener.sendLine('load-file: {}'.format(filePath.encode('ascii','ignore'))) #TODO: Proper Unicode support
        else:
            self._client.ui.showErrorMessage(getMessage("en", "vlc-unicode-loadfile-error"), True)
        
    def _getFileInfo(self):
        self._listener.sendLine("get-duration")
        self._listener.sendLine("get-filepath")
        self._listener.sendLine("get-filename")

    def lineReceived(self, line):      
        match, name, value = self.RE_ANSWER.match(line), "", ""
        if match:
            name, value = match.group('command'), match.group('argument')
  
        if(line == "filepath-change-notification"):
            self._filechanged = True 
            t = threading.Thread(target=self._onFileUpdate)
            t.setDaemon(True)
            t.start()
        elif (name == "filepath" and value != "no-input"):
            self._filechanged = True
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
            self._paused = bool(value != 'playing') if(value != "no-input" and self._filechanged == False) else self._client.getGlobalPaused()
            self._pausedAsk.set()
        elif(name == "position"):
            self._position = float(value.replace(",", ".")) if (value != "no-input" and self._filechanged == False) else self._client.getGlobalPosition()
            self._positionAsk.set()
        elif(name == "filename"):
            self._filechanged = True
            self._filename = value.decode('utf-8')
            self._filenameAsk.set()
        elif(line.startswith("interface-version: ")):
            interface_version = line[19:24]
            if (int(interface_version.replace(".","")) < int(constants.VLC_INTERFACE_MIN_VERSION.replace(".",""))):
                self._client.ui.showErrorMessage(getMessage("en", "vlc-interface-version-mismatch").format(str(interface_version), str(constants.VLC_INTERFACE_MIN_VERSION)))
        elif (line[:16] == "VLC media player"):
            vlc_version = line[17:22]
            if (int(vlc_version.replace(".","")) < int(constants.VLC_MIN_VERSION.replace(".",""))):
                self._client.ui.showErrorMessage(getMessage("en", "vlc-version-mismatch").format(str(vlc_version), str(constants.VLC_MIN_VERSION)))
            self._vlcready.set()
            self._listener.sendLine("get-interface-version")


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
        if("vlc" in path.lower() and VlcPlayer.getExpandedPath(path)):
            return True
        return False
        
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
        self._listener.sendLine('close-vlc')
        self._durationAsk.set()
        self._filenameAsk.set()
        self._pathAsk.set()
        self._positionAsk.set()
        self._vlcready.set()
        self._pausedAsk.set()
        self.reactor.callFromThread(self._client.stop, (False),)

    class __Listener(threading.Thread, asynchat.async_chat):
        def __init__(self, playerController, playerPath, filePath, args, vlcReady):
            self.__playerController = playerController
            call = [playerPath]
            if(filePath):
                if (self.__playerController._isASCII(filePath) == True):
                    call.append(filePath) #TODO: Proper Unicode support
                else:
                    playerController._client.ui.showErrorMessage(getMessage("en", "vlc-unicode-loadfile-error"), True)
            def _usevlcintf(vlcIntfPath):
                vlcSyncplayInterfacePath = vlcIntfPath + "syncplay.lua"
                if os.path.isfile(vlcSyncplayInterfacePath):
                    with open(vlcSyncplayInterfacePath, 'rU') as interfacefile:
                        for line in interfacefile:
                            if "local connectorversion" in line:
                                interface_version = line[26:31]
                                if (int(interface_version.replace(".","")) >= int(constants.VLC_INTERFACE_MIN_VERSION.replace(".",""))):
                                    return True
                                else:
                                    playerController._client.ui.showErrorMessage(getMessage("en", "vlc-interface-oldversion-ignored"))
                                    return False
                playerController._client.ui.showErrorMessage(getMessage("en", "vlc-interface-not-installed"))
                return False
            if sys.platform.startswith('linux'):
                playerController.vlcIntfPath = "/usr/lib/vlc/lua/intf/"
            elif sys.platform.startswith('darwin'):
                playerController.vlcIntfPath = "/Applications/VLC.app/Contents/MacOS/share/lua/intf/"
            else:
                playerController.vlcIntfPath = os.path.dirname(playerPath).replace("\\","/") + "/lua/intf/" # TODO: Make Mac version use /Applications/VLC.app/Contents/MacOS/share/lua/intf/
            playerController.vlcModulePath = playerController.vlcIntfPath + "modules/?.luac"
            if _usevlcintf(playerController.vlcIntfPath) == True:
                playerController.SLAVE_ARGS.append('--lua-config=syncplay={{port=\"{}\"}}'.format(str(playerController.vlcport)))
            else:
                if sys.platform.startswith('linux'):
                    playerController.vlcDataPath = "/usr/lib/syncplay/resources"
                else:
                    playerController.vlcDataPath = utils.findWorkingDir()+"\\resources"
                playerController.SLAVE_ARGS.append('--data-path={}'.format(playerController.vlcDataPath))
                playerController.SLAVE_ARGS.append('--lua-config=syncplay={{modulepath=\"{}\",port=\"{}\"}}'.format(playerController.vlcModulePath,str(playerController.vlcport)))
            
            call.extend(playerController.SLAVE_ARGS)
            if(args): 
                call.extend(args)
            
            self._vlcready = vlcReady
            self.__process = subprocess.Popen(call, stderr=subprocess.PIPE)
            for line in iter(self.__process.stderr.readline,''):
                if "[syncplay]" in line:
                    if "Listening on host" in line:
                        break
                    elif "lua interface error" in line:
                        playerController._client.ui.showErrorMessage(getMessage("en", "vlc-error-echo").format(line), True)
                        break
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
#            print "received: {}".format("".join(self._ibuffer))
            self.__playerController.lineReceived("".join(self._ibuffer))
            self._ibuffer = []

        def sendLine(self, line):
            if(self.connected):
#                print "send: {}".format(line)
                self.push(line + "\n")
