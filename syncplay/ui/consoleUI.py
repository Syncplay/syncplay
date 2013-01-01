from __future__ import print_function
import threading
import time 
import syncplay
import os
import re
from syncplay import utils
from syncplay import constants
from syncplay.messages import getMessage
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
            print(time.strftime(constants.UI_TIME_FORMAT, time.localtime()) + message)

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
        o = re.match(constants.UI_OFFSET_REGEX, data)
        s = re.match(constants.UI_SEEK_REGEX, data)
        if(o):
            sign = self._extractSign(o.group('sign'))
            t = utils.parseTime(o.group('time'))
            if(t is None):
                return
            if (o.group('sign') == "/"):
                    t =  self._syncplayClient.getPlayerPosition() - t
            elif(sign):
                    t = self._syncplayClient.getUserOffset() + sign * t
            self._syncplayClient.setUserOffset(t)
            return True
        elif s:
            sign = self._extractSign(s.group('sign'))
            t = utils.parseTime(s.group('time'))
            if(t is None):
                return
            if(sign):
                t = self._syncplayClient.getGlobalPosition() + sign * t 
            self._syncplayClient.setPosition(t)
            return True
        return False 
     
    def _executeCommand(self, data):
        command = re.match(constants.UI_COMMAND_REGEX, data)
        if(not command):
            return
        if(command.group('command') in constants.COMMANDS_UNDO):
            tmp_pos = self._syncplayClient.getPlayerPosition()
            self._syncplayClient.setPosition(self._syncplayClient.playerPositionBeforeLastSeek)
            self._syncplayClient.playerPositionBeforeLastSeek = tmp_pos
        elif (command.group('command') in constants.COMMANDS_LIST):
            self._syncplayClient.getUserList()
        elif (command.group('command') in constants.COMMANDS_PAUSE):
            self._syncplayClient.setPaused(not self._syncplayClient.getPlayerPaused())
        elif (command.group('command') in constants.COMMANDS_ROOM):
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
            if (command.group('command') not in constants.COMMANDS_HELP):
                self.showMessage(getMessage("en", "unrecognized-command-notification"))
            self.showMessage(getMessage("en", "commandlist-notification"), True)
            self.showMessage(getMessage("en", "commandlist-notification/room"), True)
            self.showMessage(getMessage("en", "commandlist-notification/list"), True)
            self.showMessage(getMessage("en", "commandlist-notification/undo"), True)
            self.showMessage(getMessage("en", "commandlist-notification/pause"), True)
            self.showMessage(getMessage("en", "commandlist-notification/seek"), True)
            self.showMessage(getMessage("en", "commandlist-notification/help"), True)
            self.showMessage("Syncplay version: {}".format(syncplay.version), True)
            self.showMessage("More info available at: {}".format(syncplay.projectURL), True)
    
