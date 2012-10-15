#coding:utf8
import hashlib
import os.path
import time
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor, task
from syncplay.protocols import SyncClientProtocol

class SyncClientFactory(ClientFactory):
    def __init__(self, client, retry = 10):
        self._client = client
        self.retry = retry
        self._timesTried = 0
        self.reconnecting = False
        
    def buildProtocol(self, addr):
        return SyncClientProtocol(self._client)

    def startedConnecting(self, connector):
        destination = connector.getDestination()
        self._client.ui.showMessage('Connecting to {}:{}'.format(destination.host, destination.port))

    def clientConnectionLost(self, connector, reason):
        if self._timesTried < self.retry:
            self._timesTried += 1
            message = 'Connection lost, reconnecting'
            self._client.ui.showMessage(message)
            self.reconnecting = True
            reactor.callLater(0.1*(2**self._timesTried), connector.connect)
        else:
            message = 'Disconnected'
            self._client.ui.showMessage(message)

    def clientConnectionFailed(self, connector, reason):
        if not self.reconnecting:
            message = 'Connection failed'
            self._client.ui.showMessage(message)
            self._client.stop(True)
        else:
            self.clientConnectionLost(connector, reason)
        
    def resetRetrying(self):
        self._timesTried = 0

    def stopRetrying(self):
        self._timesTried = self.retry
    
class SyncplayClient(object):
    def __init__(self, playerClass, ui, args):
        self.protocolFactory = SyncClientFactory(self)
        self.ui = UiManager(self, ui)
        self.userlist = SyncplayUserlist(self.ui)
        if(args.room == None or args.room == ''):
            args.room = 'default'
        self.defaultRoom = args.room
        self.playerPositionBeforeLastSeek = 0.0
        self.setUsername(args.name)
        self.setRoom(args.room)
        if(args.password):
            args.password = hashlib.md5(args.password).hexdigest()
        self._serverPassword = args.password
        self._protocol = None
        self._player = None
        self._playerClass = playerClass
        self._startupArgs = args
        
        self._running = False
        self._askPlayerTimer = None
        
        self._lastPlayerUpdate = None
        self._playerPosition = 0.0
        self._playerPaused = True
        
        self._lastGlobalUpdate = None
        self._globalPosition = 0.0
        self._globalPaused = 0.0
        self._speedChanged = False
        
    def initProtocol(self, protocol):
        self._protocol = protocol
        
    def destroyProtocol(self):
        if(self._protocol):
            self._protocol.drop()
        self._protocol = None
        
    def initPlayer(self, player):
        self._player = player
        self.scheduleAskPlayer()
    
    def scheduleAskPlayer(self, when=0.1):
        self._askPlayerTimer = task.LoopingCall(self.askPlayer)
        self._askPlayerTimer.start(when)
        
    def askPlayer(self):
        if(not self._running):
            return
        if(self._player):
            self._player.askForStatus()

    def _determinePlayerStateChange(self, paused, position):
        pauseChange = self.getPlayerPaused() != paused and self.getGlobalPaused() != paused
        _playerDiff = abs(self.getPlayerPosition() - position)
        _globalDiff = abs(self.getGlobalPosition() - position)
        seeked = _playerDiff > 1 and _globalDiff > 1
        return pauseChange, seeked

    def updatePlayerStatus(self, paused, position):
        pauseChange, seeked = self._determinePlayerStateChange(paused, position)     
        self._playerPosition = position
        self._playerPaused = paused
        if(self._lastGlobalUpdate):
            self._lastPlayerUpdate = time.time()
            if(pauseChange or seeked):
                self.playerPositionBeforeLastSeek = self.getGlobalPosition()
                if(self._protocol):
                    self._protocol.sendState(self.getPlayerPosition(), self.getPlayerPaused(), seeked, None, True)        

    def getLocalState(self):
        paused = self.getPlayerPaused()
        position = self.getPlayerPosition()
        pauseChange, seeked = self._determinePlayerStateChange(paused, position)  
        if(self._lastGlobalUpdate):
            return position, paused, seeked, pauseChange
        else:
            return None, None, None, None
    
    def _initPlayerState(self, position, paused):
        self._player.setPosition(position)
        self._player.setPaused(paused)
        madeChangeOnPlayer = True
        return madeChangeOnPlayer

    def _rewindPlayerDueToTimeDifference(self, position, setBy):
        self._player.setPosition(position)
        message = "Rewinded due to time difference with <{}>".format(setBy)
        self.ui.showMessage(message)
        madeChangeOnPlayer = True
        return madeChangeOnPlayer

    def _serverUnpaused(self, setBy):
        self._player.setPaused(False)
        madeChangeOnPlayer = True
        message = '<{}> unpaused'.format(setBy)
        self.ui.showMessage(message)
        return madeChangeOnPlayer

    def _serverPaused(self, setBy, diff):
        if (diff > 0):
            self._player.setPosition(self.getGlobalPosition())
        self._player.setPaused(True)
        madeChangeOnPlayer = True
        message = '<{}> paused'.format(setBy)
        self.ui.showMessage(message)
        return madeChangeOnPlayer

    def _serverSeeked(self, position, setBy):
        if(self.getUsername() <> setBy):
            self.playerPositionBeforeLastSeek = self.getPlayerPosition()
            self._player.setPosition(position)
            madeChangeOnPlayer = True
        else:
            madeChangeOnPlayer = False
        message = '<{}> jumped to {} from {}'.format(setBy, self.ui.formatTime(position), self.ui.formatTime(self.playerPositionBeforeLastSeek))
        self.ui.showMessage(message)
        return madeChangeOnPlayer

    def _slowDownToCoverTimeDifference(self, diff):
        if(0.4 < diff < 4):
            self._player.setSpeed(0.95)
            self._speedChanged = True
        elif(self._speedChanged):
            self._player.setSpeed(1.00)
            self._speedChanged = False
        madeChangeOnPlayer = True
        return madeChangeOnPlayer

    def _changePlayerStateAccordingToGlobalState(self, position, paused, doSeek, setBy):
        madeChangeOnPlayer = False
        pauseChanged = paused != self.getGlobalPaused()
        diff = self.getPlayerPosition() - position
        if(self._lastGlobalUpdate is None):
            madeChangeOnPlayer = self._initPlayerState(position, paused)
        self._globalPaused = paused
        self._globalPosition = position
        self._lastGlobalUpdate = time.time()
        if (doSeek):
            madeChangeOnPlayer = self._serverSeeked(position, setBy)
        if (diff > 4 and not doSeek):
            madeChangeOnPlayer = self._rewindPlayerDueToTimeDifference(position, setBy)
        if (self._player.speedSupported and not doSeek and not paused):
            madeChangeOnPlayer = self._slowDownToCoverTimeDifference(diff)
        if (paused == False and pauseChanged):
            madeChangeOnPlayer = self._serverUnpaused(setBy)
        elif (paused == True and pauseChanged):
            madeChangeOnPlayer = self._serverPaused(setBy, diff)
        return madeChangeOnPlayer

    def updateGlobalState(self, position, paused, doSeek, setBy, latency):
        madeChangeOnPlayer = False
        if(not paused):
            position += latency
        if(self._player):
            madeChangeOnPlayer = self._changePlayerStateAccordingToGlobalState(position, paused, doSeek, setBy)
        if(madeChangeOnPlayer):
            self.askPlayer()
        
    def getPlayerPosition(self):
        if(not self._lastPlayerUpdate):
            if(self._lastGlobalUpdate):
                return self.getGlobalPosition()
            else:
                return 0.0
        position = self._playerPosition
        if(not self._playerPaused):
            position += time.time() - self._lastPlayerUpdate
        return position

    def getPlayerPaused(self):
        if(not self._lastPlayerUpdate):
            if(self._lastGlobalUpdate):
                return self.getGlobalPaused()
            else:
                return True
        return self._playerPaused 
    
    def getGlobalPosition(self):
        if not self._lastGlobalUpdate:
            return 0.0
        position = self._globalPosition
        if not self._globalPaused:
            position += time.time() - self._lastGlobalUpdate
        return position
    
    def getGlobalPaused(self):
        if(not self._lastGlobalUpdate):
            return True
        return self._globalPaused 
    
    def updateFile(self, filename, duration, path):
        size = os.path.getsize(path)
        self.userlist.currentUser.setFile(filename, duration, size)
        self.sendFile()
            
    def sendFile(self):
        file_ = self.userlist.currentUser.file
        if(self._protocol and self._protocol.logged and file_):
            self._protocol.sendFileSetting(file_)
            
    def setUsername(self, username):
        self.userlist.currentUser.username = username
    
    def getUsername(self):
        return self.userlist.currentUser.username
    
    def setRoom(self, roomName):
        self.userlist.currentUser.room = roomName
    
    def sendRoom(self):
        room = self.userlist.currentUser.room
        if(self._protocol and self._protocol.logged and room):
            self._protocol.sendRoomSetting(room)
    
    def getRoom(self):
        return self.userlist.currentUser.room
    
    def getPassword(self):
        return self._serverPassword
    
    def setPosition(self, position):
        self._player.setPosition(position)
    
    def setPaused(self, paused):
        self._player.setPaused(paused)
    
    def start(self, host, port):
        if self._running:
            return
        if self._playerClass:
            self._playerClass.run(self, self._startupArgs.player_path, self._startupArgs.file, self._startupArgs._args)
            self._playerClass = None
        self.protocolFactory = SyncClientFactory(self)
        reactor.connectTCP(host, port, self.protocolFactory)
        self._running = True
        reactor.run()

    def stop(self, promptForAction = False):
        if not self._running:
            return
        self._running = False
        if self.protocolFactory:
            self.protocolFactory.stopRetrying()
        self.destroyProtocol()
        if self._player:
            self._player.drop()
        reactor.callLater(0.1, reactor.stop)
        if(promptForAction):
            self.ui.promptFor("Press enter to exit\n")

class SyncplayUser(object):
    def __init__(self, username = None, room = None, file_ = None):
        self.username = username
        self.room = room
        self.file = file_
    
    def setFile(self, filename, duration, size):
        file_ = {
                 "name": filename,
                 "duration": duration,
                 "size":size
                 }
        self.file = file_
    
    def isFileSame(self, file_):
        if(not self.file):
            return False
        sameName = self.file['name'] == file_['name']
        sameSize = self.file['size'] == file_['size']
        sameDuration = self.file['duration'] == file_['duration']
        return sameName and sameSize and sameDuration
      
    def __lt__(self, other):
        return self.username < other.username
      
class SyncplayUserlist(object):
    def __init__(self, ui):
        self.currentUser = SyncplayUser()
        self._users = {}
        self.ui = ui  

    def __showUserChangeMessage(self, username, room, file_):
        if (room and not file_):
            message = "<{}> has joined the room: '{}'".format(username, room)
            self.ui.showMessage(message)
        elif (room and file_):
            duration = self.ui.formatTime(file_['duration'])
            message = "<{}> is playing '{}' ({})".format(username, file_['name'], duration)
            if(self.currentUser.room <> room):
                message += " in room: '{}'".format(room)
            self.ui.showMessage(message)
            if(self.currentUser.file and not self.currentUser.isFileSame(file_)):
                message = "File you are playing appears to be different from <{}>'s".format(username)
                self.ui.showMessage(message)

    def addUser(self, username, room, file_, noMessage = False):
        if(username == self.currentUser.username):
            return
        user = SyncplayUser(username, room, file_)
        self._users[username] = user
        if(not noMessage):
            self.__showUserChangeMessage(username, room, file_)
            
    def removeUser(self, username):
        if(self._users.has_key(username)):
            self._users.pop(username)
            message = "<{}> has left".format(username)
            self.ui.showMessage(message)
            
    def __displayModUserMessage(self, username, room, file_, user):
        if (file_ and not user.isFileSame(file_)):
            self.__showUserChangeMessage(username, room, file_)
        elif (room and room != user.room):
            self.__showUserChangeMessage(username, room, None)

    def modUser(self, username, room, file_, noMessage = False):
        if(self._users.has_key(username)):
            user = self._users[username]
            if(not noMessage):
                self.__displayModUserMessage(username, room, file_, user)
        else:
            self.addUser(username, room, file_)

    def __addUserWithFileToList(self, rooms, user):
        file_key = '\'{}\' ({})'.format(user.file['name'], self.ui.formatTime(user.file['duration']))
        if (not rooms[user.room].has_key(file_key)):
            rooms[user.room][file_key] = {}
        rooms[user.room][file_key][user.username] = user

    def __addUserWithoutFileToList(self, rooms, user):
        if (not rooms[user.room].has_key("__noFile__")):
            rooms[user.room]["__noFile__"] = {}
        rooms[user.room]["__noFile__"][user.username] = user

    def __createListOfPeople(self, rooms):
        for user in self._users.itervalues():
            if (not rooms.has_key(user.room)):
                rooms[user.room] = {}
            if(user.file):
                self.__addUserWithFileToList(rooms, user)
            else:
                self.__addUserWithoutFileToList(rooms, user)
        return rooms

    def __addDifferentFileMessageIfNecessary(self, user, message):
        if(self.currentUser.file):
            fileHasSameSizeAsYour = user.file['size'] != self.currentUser.file['size']
            differentFileMessage = " (but their file size is different from yours!)"
            message += differentFileMessage if not fileHasSameSizeAsYour else ""
        return message

    def __displayFileWatchersInRoomList(self, key, users):
        self.ui.showMessage("File: {} is being played by:".format(key), True, True)
        for user in sorted(users.itervalues()):
            message = user.username
            message = self.__addDifferentFileMessageIfNecessary(user, message)
            self.ui.showMessage("\t<" + message + ">", True, True)

    def __displayPeopleInRoomWithNoFile(self, noFileList):
        if (noFileList):
            self.ui.showMessage("People who are not playing any file:",  True, True)
            for user in sorted(noFileList.itervalues()):
                self.ui.showMessage("\t<" + user.username + ">", True, True)

    def __displayListOfPeople(self, rooms):
        for roomName in sorted(rooms.iterkeys()):
            self.ui.showMessage("In room '{}':".format(roomName), True, False)
            noFileList = rooms[roomName].pop("__noFile__") if (rooms[roomName].has_key("__noFile__")) else None
            for key in sorted(rooms[roomName].iterkeys()):
                self.__displayFileWatchersInRoomList(key, rooms[roomName][key])
            self.__displayPeopleInRoomWithNoFile(noFileList)
            
    def showUserList(self):
        rooms = {} 
        self.__createListOfPeople(rooms)
        self.__displayListOfPeople(rooms)
                                       
class UiManager(object):
    def __init__(self, client, ui):
        self._client = client
        self.__ui = ui
    
    def showMessage(self, message, noPlayer = False, noTimestamp = False):
        if(self._client._player and not noPlayer): self._client._player.displayMessage(message)
        self.__ui.showMessage(message, noTimestamp)
    
    def showErrorMessage(self, message):
        self.__ui.showErrorMessage(message)

    def promptFor(self, prompt):
        return self.__ui.promptFor(prompt)

    def formatTime(self, value):
        weeks = value // 604800
        days = (value % 604800) // 86400
        hours = (value % 86400) // 3600
        minutes = (value % 3600) // 60
        seconds = value % 60
        if(weeks > 0):
            return '{0:.0f}w, {1:.0f}d, {2:02.0f}:{3:02.0f}:{4:02.0f}'.format(weeks, days, hours, minutes, seconds)
        elif(days > 0):
            return '{0:.0f}d, {1:02.0f}:{2:02.0f}:{3:02.0f}'.format(days, hours, minutes, seconds)
        elif(hours > 0):
            return '{0:02.0f}:{1:02.0f}:{2:02.0f}'.format(hours, minutes, seconds)
        else:
            return '{0:02.0f}:{1:02.0f}'.format(minutes, seconds)

