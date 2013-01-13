import subprocess
import re
import threading
from syncplay.players.basePlayer import BasePlayer
from syncplay import constants
from syncplay.messages import getMessage
import os

class MplayerPlayer(BasePlayer):
    speedSupported = True
    RE_ANSWER = re.compile(constants.MPLAYER_ANSWER_REGEX)
    SLAVE_ARGS = constants.MPLAYER_SLAVE_ARGS
    def __init__(self, client, playerPath, filePath, args):
        self._client = client
        self._paused = None
        self._duration = None
        self._filename = None
        self._filepath = None
        try:
            self._listener = self.__Listener(self, playerPath, filePath, args)
        except ValueError:
            self._client.ui.showMessage(getMessage("en", "mplayer-file-required-notification"))
            self._client.ui.showMessage(getMessage("en", "mplayer-file-required-notification/example"))
            self._client.stop(True)
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
        self.setPaused(self._client.getGlobalPaused()) 
        self.setPosition(self._client.getGlobalPosition())
        self._client.initPlayer(self)
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
    
    def displayMessage(self, message, duration = (constants.OSD_DURATION*1000)):
        self._listener.sendLine('osd_show_text "{!s}" {} {}'.format(message, duration, constants.MPLAYER_OSD_LEVEL))
 
    def setSpeed(self, value):        
        self._setProperty('speed', "{:.2f}".format(value))

    def setPosition(self, value):
        self._position = value
        self._setProperty('time_pos', "{}".format(value))
    
    def setPaused(self, value):
        self._paused = value
        self._setProperty('pause', 'yes' if value else 'no') 
    
    def _getFilename(self):
        self._getProperty('filename')
        
    def _getLength(self):
        self._getProperty('length')
        
    def _getFilepath(self):
        self._getProperty('path')

    def _getPaused(self):
        self._getProperty('pause')

    def _getPosition(self):
        self._getProperty('time_pos')
    
    def lineReceived(self, line):
        match = self.RE_ANSWER.match(line)
        if not match:
            return
        name, value = match.group(1).lower(), match.group(2)
        
        if(name == "time_pos"):
            self._position = float(value)
            self._positionAsk.set()
        elif(name == "pause"):
            self._paused = bool(value == 'yes')
            self._pausedAsk.set()
        elif(name == "length"):
            self._duration = float(value)
            self._durationAsk.set()
        elif(name == "path"):
            self._filepath = value
            self._pathAsk.set()
        elif(name == "filename"):
            self._filename = value
            self._filenameAsk.set()
        
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
    def isValidPlayerPath(path):
        if("mplayer2" in path and MplayerPlayer.getExpandedPath(path)):
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
        self._listener.sendLine('quit')
        self._durationAsk.set()
        self._filenameAsk.set()
        self._pathAsk.set()
        self._positionAsk.set()
        self._pausedAsk.set()
        self._client.stop(False)
        for line in self._listener.readStderrLine():
            self._client.ui.showMessage(line, True, True)
    
    class __Listener(threading.Thread):
        def __init__(self, playerController, playerPath, filePath, args):
            self.__playerController = playerController
            if(not filePath):
                raise ValueError
            call = [playerPath, filePath]
            call.extend(playerController.SLAVE_ARGS)
            if(args):
                call.extend(args)
            self.__process = subprocess.Popen(call, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            threading.Thread.__init__(self, name="MPlayer Listener")

        def run(self):
            while(self.__process.poll() is None):
                line = self.__process.stdout.readline()
                line = line.rstrip("\r\n")
                self.__playerController.lineReceived(line)
            self.__playerController.drop()
            
        def sendLine(self, line):
            try:
                self.__process.stdin.write(line + "\n")
            except IOError:
                pass

        def readStderrLine(self):
            for line in self.__process.stderr.readlines():
                yield line
            
            
