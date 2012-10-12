from __future__ import print_function
import threading
import re
import time 
import syncplay

class ConsoleUI(threading.Thread):
    def __init__(self):
        self.promptMode = threading.Event()
        self.PromptResult = ""
        self.promptMode.set()
        self._syncplayClient = None
        threading.Thread.__init__(self, name="ConsoleUI")
        
    def addClient(self, client):
        self._syncplayClient = client
        
    def run(self):
        try:
            while True:
                data = raw_input()
                data = data.rstrip('\n\r')
                if(not self.promptMode.isSet()):
                    self.PromptResult = data
                    self.promptMode.set()
                elif(self._syncplayClient):
                    self._executeCommand(data)
        except:
            self._syncplayClient.protocolFactory.stopRetrying()
            pass
        
    def promptFor(self, prompt = ">", message = ""):
        if message <> "":
            print(message)
        self.promptMode.clear()
        print(prompt, end='')
        self.promptMode.wait()
        return self.PromptResult

    def showMessage(self, message, noTimestamp):
        if(noTimestamp):
            print(message)
        else:
            print(time.strftime("[%X] ", time.localtime()) + message)

    def showDebugMessage(self, message):
        print(message)
        
    def showErrorMessage(self, message):
        print("ERROR:\t" + message)
        
    def __exectueSeekCmd(self, seek_type, minutes, seconds):
        self._syncplayClient.playerPositionBeforeLastSeek = self._syncplayClient.player_position
        if seek_type == 's':
            seconds = int(seconds) if seconds <> None else 0
            seconds += int(minutes) * 60 if minutes <> None else 0 
            self._syncplayClient.setPosition(seconds)
        else: #seek_type s+
            seconds = int(seconds) if seconds <> None and minutes <> None else 20
            seconds += int(minutes) * 60 if minutes <> None else 60
            self._syncplayClient.setPosition(self.player_position+seconds)
            
    def _executeCommand(self, data):
        RE_SEEK = re.compile("^([\+\-s]+) ?(-?\d+)?([^0-9](\d+))?$")
        RE_ROOM = re.compile("^room( (\w+))?")
        matched_seek = RE_SEEK.match(data)
        matched_room = RE_ROOM.match(data)
        if matched_seek :
            self.__exectueSeekCmd(matched_seek.group(1), matched_seek.group(2), matched_seek.group(4))
        elif matched_room:
            room = matched_room.group(2)
            if room == None:
                if  self._syncplayClient.users.currentUser._filename <> None:
                    room = self._syncplayClient.users.currentUser._filename
                else:
                    room = self._syncplayClient.defaultRoom
            self._syncplayClient.protocol.sendRoomSetting(room)
        elif data == "r":
            tmp_pos = self._syncplayClient.getPlayerPosition()
            self._syncplayClient.setPosition(self._syncplayClient.playerPositionBeforeLastSeek)
            self._syncplayClient.playerPositionBeforeLastSeek = tmp_pos
        elif data == "p":
            self._syncplayClient.setPaused(not self._syncplayClient.getPlayerPaused())
        elif data == "k": #TODO: remove?
            self._syncplayClient.stop()
        elif data == 'help':
            self.showMessage( "Available commands:" )
            self.showMessage( "\thelp - this help" )
            self.showMessage( "\ts [time] - seek" )
            self.showMessage( "\ts+ [time] - seek to: current position += time" )
            self.showMessage( "\tr - revert last seek" )
            self.showMessage( "\tp - toggle pause" )
            self.showMessage( "\troom [name] - change room" )
            self.showMessage("Syncplay version: %s" % syncplay.version)
            self.showMessage("More info available at: %s" % syncplay.projectURL)
        else:
            self.showMessage( "Unrecognized command, type 'help' for list of available commands" )    
