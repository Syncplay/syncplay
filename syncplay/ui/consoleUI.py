from __future__ import print_function
import threading
import time 
import syncplay
import re
from syncplay import utils
from syncplay import constants
from syncplay.messages import getMessage
import sys
from syncplay.utils import formatTime

class ConsoleUI(threading.Thread):
    def __init__(self):
        self.promptMode = threading.Event()
        self.PromptResult = ""
        self.promptMode.set()
        self._syncplayClient = None
        threading.Thread.__init__(self, name="ConsoleUI")
        
    def addClient(self, client):
        self._syncplayClient = client
        
    def drop(self):
        pass
    
    def run(self):
        try:
            while True:
                data = raw_input().decode(sys.stdin.encoding)
                data = data.rstrip('\n\r')
                if not self.promptMode.isSet():
                    self.PromptResult = data
                    self.promptMode.set()
                elif self._syncplayClient:
                    self._executeCommand(data)
        except EOFError:
            pass

    def updateRoomName(self, room=""):
        pass

    def setControllerStatus(self, username, isController):
        pass

    def promptFor(self, prompt=">", message=""):
        if message <> "":
            print(message)
        self.promptMode.clear()
        print(prompt, end='')
        self.promptMode.wait()
        return self.PromptResult

    def showUserList(self, currentUser, rooms):
        for room in rooms:
            message = u"In room '{}':".format(room)
            self.showMessage(message, True)
            for user in rooms[room]:
                userflags = u""
                if user.isController():
                    userflags = userflags + u"(Controller) "
                username = userflags + u"*<{}>*".format(user.username) if user == currentUser else userflags + u"<{}>".format(user.username)
                if user.file:
                    message = u"{} is playing:".format(username)
                    self.showMessage(message, True)
                    message = u"    File: '{}' ({})".format(user.file['name'], formatTime(user.file['duration']))
                    if currentUser.file:
                        if user.file['name'] == currentUser.file['name'] and user.file['size'] != currentUser.file['size']:
                            message += u" (their file size is different from yours!)"
                    self.showMessage(message, True)
                else:
                    message = u"{} is not playing a file".format(username)
                    self.showMessage(message, True)

    def userListChange(self):
        pass

    def showMessage(self, message, noTimestamp=False):
        message = message.encode(sys.stdout.encoding, 'replace')
        if noTimestamp:
            print(message)
        else:
            print(time.strftime(constants.UI_TIME_FORMAT, time.localtime()) + message)

    def showDebugMessage(self, message):
        print(message)

    def showErrorMessage(self, message, criticalerror = False):
        print("ERROR:\t" + message)            

    def _extractSign(self, m):
        if m:
            if m == "-":
                return -1
            else:
                return 1
        else:
            return None
        
    def _tryAdvancedCommands(self, data):
        o = re.match(constants.UI_OFFSET_REGEX, data)
        s = re.match(constants.UI_SEEK_REGEX, data)
        if o:
            sign = self._extractSign(o.group('sign'))
            t = utils.parseTime(o.group('time'))
            if t is None:
                return
            if o.group('sign') == "/":
                    t =  self._syncplayClient.getPlayerPosition() - t
            elif sign:
                    t = self._syncplayClient.getUserOffset() + sign * t
            self._syncplayClient.setUserOffset(t)
            return True
        elif s:
            sign = self._extractSign(s.group('sign'))
            t = utils.parseTime(s.group('time'))
            if t is None:
                return
            if sign:
                t = self._syncplayClient.getGlobalPosition() + sign * t 
            self._syncplayClient.setPosition(t)
            return True
        return False 
     
    def _executeCommand(self, data):
        command = re.match(constants.UI_COMMAND_REGEX, data)
        if not command:
            return
        if command.group('command') in constants.COMMANDS_UNDO:
            tmp_pos = self._syncplayClient.getPlayerPosition()
            self._syncplayClient.setPosition(self._syncplayClient.playerPositionBeforeLastSeek)
            self._syncplayClient.playerPositionBeforeLastSeek = tmp_pos
        elif command.group('command') in constants.COMMANDS_LIST:
            self._syncplayClient.getUserList()
        elif command.group('command') in constants.COMMANDS_PAUSE:
            self._syncplayClient.setPaused(not self._syncplayClient.getPlayerPaused())
        elif command.group('command') in constants.COMMANDS_ROOM:
            room = command.group('parameter')
            if room == None:
                if  self._syncplayClient.userlist.currentUser.file:
                    room = self._syncplayClient.userlist.currentUser.file["name"]
                else:
                    room = self._syncplayClient.defaultRoom

            self._syncplayClient.setRoom(room)
            self._syncplayClient.sendRoom()
        elif command.group('command') in constants.COMMANDS_CREATE:
            self._syncplayClient.createControlledRoom()
        elif command.group('command') in constants.COMMANDS_AUTH:
            controlpassword = command.group('parameter')
            self._syncplayClient.identifyAsController(controlpassword)
        else:
            if self._tryAdvancedCommands(data):
                return
            if command.group('command') not in constants.COMMANDS_HELP:
                self.showMessage(getMessage("unrecognized-command-notification"))
            self.showMessage(getMessage("commandlist-notification"), True)
            self.showMessage(getMessage("commandlist-notification/room"), True)
            self.showMessage(getMessage("commandlist-notification/list"), True)
            self.showMessage(getMessage("commandlist-notification/undo"), True)
            self.showMessage(getMessage("commandlist-notification/pause"), True)
            self.showMessage(getMessage("commandlist-notification/seek"), True)
            self.showMessage(getMessage("commandlist-notification/help"), True)
            self.showMessage(getMessage("commandlist-notification/create"), True)
            self.showMessage(getMessage("commandlist-notification/auth"), True)
            self.showMessage(getMessage("syncplay-version-notification").format(syncplay.version), True)
            self.showMessage(getMessage("more-info-notification").format(syncplay.projectURL), True)
    
