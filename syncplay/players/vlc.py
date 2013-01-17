import subprocess
import re
import threading
from syncplay.players.basePlayer import BasePlayer
from syncplay import constants
from syncplay.messages import getMessage
import os
import random
import socket
import asynchat, asyncore

class VlcPlayer(BasePlayer):
    speedSupported = True
    RE_ANSWER = re.compile(r"(?:^(?P<command>[a-zA-Z_]+)(?:\: )?(?P<argument>.*))")
    VLC_MIN_PORT = 10000
    VLC_MAX_PORT = 65000
    SLAVE_ARGS = ['--extraintf=luaintf','--lua-intf=syncplay','-vvv']
    
    random.seed()
    vlcport = random.randrange(VLC_MIN_PORT, VLC_MAX_PORT)
    SLAVE_ARGS.append('--lua-config=syncplay={{port=\"{}\"}}'.format(str(vlcport)))
    
    def __init__(self, client, playerPath, filePath, args):
        self._client = client
        self._paused = None
        self._duration = None
        self._filename = None
        self._filepath = None
        self._readyforchange = True
        self._updatenotification = False
        
        try:
            self._listener = self.__Listener(self, playerPath, filePath, args)
            
        except ValueError:
            self._client.ui.showMessage("Failed to load VLC")
            self._client.stop(True)
            return 

        self._listener.setDaemon(True)
        self._listener.start()
        
        self._durationAsk = threading.Event()
        self._filenameAsk = threading.Event()
        self._pathAsk = threading.Event()
        
        self._positionAsk = threading.Event()
        self._pausedAsk = threading.Event()
        
        self._vlcready = threading.Event()
        
        self._vlcready.wait()
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
        self._getFilepath()
        self._getLength()
        self._fileUpdateWaitEvents()
        self._client.updateFile(self._filename, self._duration, self._filepath)
        
    def _preparePlayer(self):
        self.setPaused(self._client.getGlobalPaused()) 
        self.setPosition(self._client.getGlobalPosition())
        self._client.initPlayer(self)
        self._readyforchange = True     

    def askForStatus(self):
        if (self._updatenotification):
            self._updatenotification = False
            self._onFileUpdate()
            
        self._positionAsk.clear()
        self._pausedAsk.clear()
        self._listener.sendLine(".")
        self._positionAsk.wait()
        self._pausedAsk.wait()
        self._client.updatePlayerStatus(self._paused, self._position)
                
    def displayMessage(self, message, duration = constants.OSD_DURATION):
        self._listener.sendLine('display-osd: {}, {}, {}'.format('top-right', duration, message))
 
    def setSpeed(self, value):        
        self._setProperty('speed', "{:.2f}".format(value))
        self._listener.sendLine("set-rate: {:.2f}".format(value))

    def setPosition(self, value):
        self._position = value
        self._listener.sendLine("set-position: {}".format(value))
    
    def setPaused(self, value):
        self._paused = value
        self._listener.sendLine('set-playstate: {}'.format("paused" if value else "playing"))
    
    def _getFilename(self):
        self._listener.sendLine("get-filename")
        
    def _getLength(self):
        self._listener.sendLine("get-duration")
        
    def _getFilepath(self):
        self._listener.sendLine("get-filepath")

    def _getPaused(self):
        self._listener.sendLine(".")

    def _getPosition(self):
        self._listener.sendLine(".")
    
    def lineReceived(self, line):      
        #print "received: {}".format(line)
        if (line[:16] == "VLC media player"):
            self._vlcready.set()
            return
        
        elif(line == "filepath-change-notification"):
            if (self._readyforchange):
                self._updatenotification = True
            return
        
        match = self.RE_ANSWER.match(line)
        if not match:
            return
        name, value = match.group('command'), match.group('argument')
  
        if (name == "filepath"):
            if (value != "no-input"):
                self._filepath = value
                self._pathAsk.set()

        
        elif(name == "duration"):
            if (value != "no-input"):
                self._duration = float(value)
                print line
                self._durationAsk.set() #
            
        elif(name == "playstate"):
            if(value == "no-input"):
                self._paused = self._client.getGlobalPaused()
            else:
                self._paused = bool(value != 'playing')
            self._pausedAsk.set()
            
        elif(name == "position"):
            if (value == "no-input"):
                self._position = self._client.getGlobalPosition()
            else:
                self._position = float(value)
            self._positionAsk.set()
            
        elif(name == "get-interface-version"):
            print name
            
        elif(name == "play-error"):
            print name
                        
        elif(name == "set-playstate-error"):
            print name
                        
        elif(name == "set-rate-error"):
            print name
                        
        elif(name == "display-osd-error"):
            print name

        elif(name == "filename"):
            self._filename = value
            self._filenameAsk.set()
                        
        
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
        def __init__(self, playerController, playerPath, filePath, args):
            self.__playerController = playerController
            call = [playerPath]
            if(filePath):
                call.append(filePath)
            call.extend(playerController.SLAVE_ARGS)
            if(args): 
                call.extend(args)

            self.__process = subprocess.Popen(call)
            threading.Thread.__init__(self, name="VLC Listener")
            asynchat.async_chat.__init__(self)
            self.set_terminator("\n")
            self._ibuffer = []
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect(('localhost', self.__playerController.vlcport))
            
        def run(self):
            asyncore.loop()
            
        def collect_incoming_data(self, data):
            self._ibuffer.append(data)
    
        def found_terminator(self):
            self.__playerController.lineReceived("".join(self._ibuffer))
            self._ibuffer = []

        def sendLine(self, line):
            self.__playerController._vlcready.wait()
            #print "send: {}".format(line)
            self.push(line + "\n")