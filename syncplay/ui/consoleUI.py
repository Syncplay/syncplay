from __future__ import print_function
import threading
import re
import time 
import syncplay
import os

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
        while True:
            data = raw_input()
            data = data.rstrip('\n\r')
            if(not self.promptMode.isSet()):
                self.PromptResult = data
                self.promptMode.set()
            elif(self._syncplayClient):
                self._executeCommand(data)
        
    def promptFor(self, prompt = ">", message = ""):
        if message <> "":
            print(message)
        self.promptMode.clear()
        print(prompt, end='')
        self.promptMode.wait()
        return self.PromptResult

    def showMessage(self, message, noTimestamp = False):
        if(os.name == "nt"):
            message = message.encode('ascii','replace') 
        if(noTimestamp):
            print(message)
        else:
            print(time.strftime("[%X] ", time.localtime()) + message)

    def showDebugMessage(self, message):
        print(message)
        
    def showErrorMessage(self, message):
        print("ERROR:\t" + message)
                
    def _executeCommand(self, data):
        RE_ROOM = re.compile("^room( (\w+))?")
        matched_room = RE_ROOM.match(data)
        if matched_room:
            room = matched_room.group(2)
            if room == None:
                if  self._syncplayClient.userlist.currentUser.file:
                    room = self._syncplayClient.userlist.currentUser.file["name"]
                else:
                    room = self._syncplayClient.defaultRoom
            self._syncplayClient.setRoom(room)
            self._syncplayClient.sendRoom()
        elif data == "r":
            tmp_pos = self._syncplayClient.getPlayerPosition()
            self._syncplayClient.setPosition(self._syncplayClient.playerPositionBeforeLastSeek)
            self._syncplayClient.playerPositionBeforeLastSeek = tmp_pos
        elif data == "p":
            self._syncplayClient.setPaused(not self._syncplayClient.getPlayerPaused())
        elif data == 'help':
            self.showMessage( "Available commands:", True)
            self.showMessage( "\thelp - this help", True )
            self.showMessage( "\tr - revert last seek", True )
            self.showMessage( "\tp - toggle pause", True )
            self.showMessage( "\troom [name] - change room", True )
            self.showMessage("Syncplay version: {}".format(syncplay.version), True)
            self.showMessage("More info available at: {}".format(syncplay.projectURL), True)
        else:
            self.showMessage( "Unrecognized command, type 'help' for list of available commands" )    
