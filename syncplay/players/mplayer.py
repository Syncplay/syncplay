import subprocess
import re
import threading
from syncplay.players.basePlayer import BasePlayer

class MplayerPlayer(BasePlayer):
    speedSupported = True
    RE_ANSWER = re.compile('^ANS_([a-zA-Z_]+)=(.+)$')
    def __init__(self, client, playerPath, filePath):
        self._client = client
        self._paused = None
        self._duration = None
        self._filename = None
        self._filepath = None
        
        self._listener = self.__Listener(self, playerPath, filePath)
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
    
    def displayMessage(self, message):
        self._listener.sendLine('osd_show_text "{!s}" {} {}'.format(message, 3000, 1))
 
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
        mplayer = MplayerPlayer(client, playerPath, filePath)
        return mplayer

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
        def __init__(self, playerController, playerPath, filePath):
            self.__playerController = playerController
            self.__process = subprocess.Popen([playerPath, filePath, '-slave', '-msglevel', 'all=1:global=4'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
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
            
            
