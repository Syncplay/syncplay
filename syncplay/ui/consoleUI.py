from __future__ import print_function
import threading
import time 
import syncplay
import os
import re
from syncplay import utils

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
        
    def promptFor(self, prompt=">", message=""):
        if message <> "":
            print(message)
        self.promptMode.clear()
        print(prompt, end='')
        self.promptMode.wait()
        return self.PromptResult

    def showMessage(self, message, noTimestamp=False):
        if(os.name == "nt"):
            message = message.encode('ascii', 'replace') 
        if(noTimestamp):
            print(message)
        else:
            print(time.strftime("[%X] ", time.localtime()) + message)

    def showDebugMessage(self, message):
        print(message)
        
    def showErrorMessage(self, message):
        print("ERROR:\t" + message)            

    def _extractSign(self, m):
        if(m):
            if(m == "-"):
                return -1
            else:
                return 1
        else:
            return None
        
    def _tryAdvancedCommands(self, data):
        o = re.match(r"^(?:o|offset)\ ?(?P<sign>[/+-])?(?P<time>\d+(?:[^\d\.](?:\d+)){0,2}(?:\.(?:\d+))?)$", data)
        s = re.match(r"^(?:s|seek)?\ ?(?P<sign>[+-])?(?P<time>\d+(?:[^\d\.](?:\d+)){0,2}(?:\.(?:\d+))?)$", data)
        if(o):
            sign = self._extractSign(o.group('sign'))
            t = utils.parseTime(o.group('time'))
            if(t is None):
                return
            if(sign):
                if (o.group('sign') == "/"):
                    t = t - self._syncplayClient.getPlayerPosition()
                else:
                    t = self._syncplayClient.getUserOffset() + sign * t
            self._syncplayClient.setUserOffset(t)
            return True
        elif s:
            sign = self._extractSign(s)
            t = utils.parseTime(s.group('time'))
            if(t is None):
                return
            if(sign):
                t = self._syncplayClient.getGlobalPosition() + sign * t 
            self._syncplayClient.setPosition(t)
            return True
        return False 
     
    def _executeCommand(self, data):
        command = re.match(r"^(?P<command>[^\ ]+)(?:\ (?P<parameter>.+))?", data)
        if(not command):
            return
        if(command.group('command') in ["u", "undo", "revert"]):
            tmp_pos = self._syncplayClient.getPlayerPosition()
            self._syncplayClient.setPosition(self._syncplayClient.playerPositionBeforeLastSeek)
            self._syncplayClient.playerPositionBeforeLastSeek = tmp_pos
        elif (command.group('command') in ["l", "list", "users"]):
            self._syncplayClient.getUserList()
        elif (command.group('command') in ["p", "play", "pause"]):
            self._syncplayClient.setPaused(not self._syncplayClient.getPlayerPaused())
        elif (command.group('command') in ["r", "room"]):
            room = command.group('parameter')
            if room == None:
                if  self._syncplayClient.userlist.currentUser.file:
                    room = self._syncplayClient.userlist.currentUser.file["name"]
                else:
                    room = self._syncplayClient.defaultRoom

            self._syncplayClient.setRoom(room)
            self._syncplayClient.sendRoom()
        else:
            if(self._tryAdvancedCommands(data)):
                return
            if (command.group('command') not in ['help', 'h', '?', '/?', '\?']):
                self.showMessage("Unrecognized command")
            self.showMessage("Available commands:", True)
            self.showMessage("\tr [name] - change room", True)
            self.showMessage("\tl - show user list", True)
            self.showMessage("\tu - undo last seek", True)
            self.showMessage("\tp - toggle pause", True)
            self.showMessage("\t[s][+-][time] - seek to the given value of time, if + or - is not specified it's absolute time in seconds or min:sec", True)
            self.showMessage("\th - this help", True)
            self.showMessage("Syncplay version: {}".format(syncplay.version), True)
            self.showMessage("More info available at: {}".format(syncplay.projectURL), True)
    
