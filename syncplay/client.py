#coding:utf8
import hashlib
import os.path
import time
import re
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor, task
from syncplay.protocols import SyncClientProtocol
from syncplay import utils, constants
from syncplay.messages import getMessage
import threading
try:
    import libMal
except ImportError:
    libMal = None

class SyncClientFactory(ClientFactory):
    def __init__(self, client, retry = constants.RECONNECT_RETRIES):
        self._client = client
        self.retry = retry
        self._timesTried = 0
        self.reconnecting = False
        
    def buildProtocol(self, addr):
        self._timesTried = 0
        return SyncClientProtocol(self._client)

    def startedConnecting(self, connector):
        destination = connector.getDestination()
        message = getMessage("en", "connection-attempt-notification").format(destination.host, destination.port)
        self._client.ui.showMessage(message)

    def clientConnectionLost(self, connector, reason):
        if self._timesTried < self.retry:
            self._timesTried += 1
            self._client.ui.showMessage(getMessage("en", "reconnection-attempt-notification"))
            self.reconnecting = True
            reactor.callLater(0.1*(2**self._timesTried), connector.connect)
        else:
            message = getMessage("en", "disconnection-notification")
            self._client.ui.showErrorMessage(message)

    def clientConnectionFailed(self, connector, reason):
        if not self.reconnecting:
            self._client.ui.showErrorMessage(getMessage("en", "connection-failed-notification"))
        else:
            self.clientConnectionLost(connector, reason)
        
    def resetRetrying(self):
        self._timesTried = 0

    def stopRetrying(self):
        self._timesTried = self.retry
    
class SyncplayClient(object):
    def __init__(self, playerClass, ui, config):
        self.protocolFactory = SyncClientFactory(self)
        self.ui = UiManager(self, ui)
        self.userlist = SyncplayUserlist(self.ui, self)
        self._protocol = None
        self._player = None
        if(config['room'] == None or config['room'] == ''):
            config['room'] = config['name'] # ticket #58
        self.defaultRoom = config['room']
        self.playerPositionBeforeLastSeek = 0.0
        self.setUsername(config['name'])
        self.setRoom(config['room'])
        if(config['password']):
            config['password'] = hashlib.md5(config['password']).hexdigest()
        self._serverPassword = config['password']
        if(not config['file']):
            self.__getUserlistOnLogon = True
        else:
            self.__getUserlistOnLogon = False
        self._playerClass = playerClass
        self._config = config
        
        self._running = False
        self._askPlayerTimer = None
        
        self._lastPlayerUpdate = None
        self._playerPosition = 0.0
        self._playerPaused = True
        
        self._lastGlobalUpdate = None
        self._globalPosition = 0.0
        self._globalPaused = 0.0
        self._userOffset = 0.0
        self._speedChanged = False
        
        self._warnings = self._WarningManager(self._player, self.userlist, self.ui)
        self._malUpdater = MalUpdater(config["malUsername"], config["malPassword"], self.ui)
        
    def initProtocol(self, protocol):
        self._protocol = protocol
        
    def destroyProtocol(self):
        if(self._protocol):
            self._protocol.drop()
        self._protocol = None
        
    def initPlayer(self, player):
        self._player = player
        self.scheduleAskPlayer()
    
    def scheduleAskPlayer(self, when=constants.PLAYER_ASK_DELAY):
        self._askPlayerTimer = task.LoopingCall(self.askPlayer)
        self._askPlayerTimer.start(when)
        
    def askPlayer(self):
        if(not self._running):
            return
        if(self._player):
            self._player.askForStatus()
        self.checkIfConnected()

    def checkIfConnected(self):
        if(self._lastGlobalUpdate and self._protocol and time.time() - self._lastGlobalUpdate > constants.PROTOCOL_TIMEOUT):
            self._lastGlobalUpdate = None
            self.ui.showErrorMessage(getMessage("en", "server-timeout-error"))
            self._protocol.drop()
            return False
        return True

    def _determinePlayerStateChange(self, paused, position):
        pauseChange = self.getPlayerPaused() != paused and self.getGlobalPaused() != paused
        _playerDiff = abs(self.getPlayerPosition() - position)
        _globalDiff = abs(self.getGlobalPosition() - position)
        seeked = _playerDiff > constants.SEEK_THRESHOLD and _globalDiff > constants.SEEK_THRESHOLD
        return pauseChange, seeked 

    def updatePlayerStatus(self, paused, position):
        position -= self.getUserOffset()
        pauseChange, seeked = self._determinePlayerStateChange(paused, position)
        self._playerPosition = position
        self._playerPaused = paused
        if(self._lastGlobalUpdate):
            self._lastPlayerUpdate = time.time()
            if((pauseChange or seeked) and self._protocol):
                if(seeked):
                    self.playerPositionBeforeLastSeek = self.getGlobalPosition()
                self._protocol.sendState(self.getPlayerPosition(), self.getPlayerPaused(), seeked, None, True)        

    def getLocalState(self):
        paused = self.getPlayerPaused()
        position = self.getPlayerPosition()
        pauseChange, _ = self._determinePlayerStateChange(paused, position)
        if(self._lastGlobalUpdate):
            return position, paused, _, pauseChange
        else:
            return None, None, None, None
    
    def _initPlayerState(self, position, paused):
        if(self.userlist.currentUser.file):
            self.setPosition(position)
            self._player.setPaused(paused)
            madeChangeOnPlayer = True
            return madeChangeOnPlayer

    def _rewindPlayerDueToTimeDifference(self, position, setBy):
        self.setPosition(position)
        self.ui.showMessage(getMessage("en", "rewind-notification").format(setBy))
        madeChangeOnPlayer = True
        return madeChangeOnPlayer

    def _serverUnpaused(self, setBy):
        self._player.setPaused(False)
        madeChangeOnPlayer = True
        self.ui.showMessage(getMessage("en", "unpause-notification").format(setBy))
        return madeChangeOnPlayer

    def _serverPaused(self, setBy):
        self.setPosition(self.getGlobalPosition())
        self._player.setPaused(True)
        madeChangeOnPlayer = True
        self.ui.showMessage(getMessage("en", "pause-notification").format(setBy))
        return madeChangeOnPlayer

    def _serverSeeked(self, position, setBy):
        if(self.getUsername() <> setBy):
            self.playerPositionBeforeLastSeek = self.getPlayerPosition()
            self.setPosition(position)
            madeChangeOnPlayer = True
        else:
            madeChangeOnPlayer = False
        message = getMessage("en", "seek-notification").format(setBy, utils.formatTime(self.playerPositionBeforeLastSeek), utils.formatTime(position))
        self.ui.showMessage(message)
        return madeChangeOnPlayer

    def _slowDownToCoverTimeDifference(self, diff, setBy):
        if(constants.SLOWDOWN_KICKIN_THRESHOLD < diff and not self._speedChanged):
            self._player.setSpeed(constants.SLOWDOWN_RATE)
            self._speedChanged = True
            self.ui.showMessage(getMessage("en", "slowdown-notification").format(setBy))
        elif(self._speedChanged and diff < constants.SLOWDOWN_RESET_THRESHOLD):
            self._player.setSpeed(1.00)
            self._speedChanged = False
            self.ui.showMessage(getMessage("en", "revert-notification"))
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
        if (diff > constants.REWIND_THRESHOLD and not doSeek and not self._config['rewindOnDesync'] == False):
            madeChangeOnPlayer = self._rewindPlayerDueToTimeDifference(position, setBy)
        if (self._player.speedSupported and not doSeek and not paused and not self._config['slowOnDesync'] == False):
            madeChangeOnPlayer = self._slowDownToCoverTimeDifference(diff, setBy)
        if (paused == False and pauseChanged):
            madeChangeOnPlayer = self._serverUnpaused(setBy)
        elif (paused == True and pauseChanged):
            madeChangeOnPlayer = self._serverPaused(setBy)
        return madeChangeOnPlayer

    def _executePlaystateHooks(self, position, paused, doSeek, setBy, latency):
        if(self.userlist.hasRoomStateChanged() and not paused):
            self._warnings.checkWarnings()
            self.userlist.roomStateConfirmed()
        self._malUpdater.playingHook(position, paused)

    def updateGlobalState(self, position, paused, doSeek, setBy, latency):
        if(self.__getUserlistOnLogon):
            self.__getUserlistOnLogon = False
            self.getUserList()
        madeChangeOnPlayer = False
        if(not paused):
            position += latency
        if(self._player):
            madeChangeOnPlayer = self._changePlayerStateAccordingToGlobalState(position, paused, doSeek, setBy)
        if(madeChangeOnPlayer):
            self.askPlayer()
        self._executePlaystateHooks(position, paused, doSeek, setBy, latency)
        
    def getUserOffset(self):
        return self._userOffset
     
    def setUserOffset(self, time):
        self._userOffset = time
        self.setPosition(self.getGlobalPosition())
        self.ui.showMessage(getMessage("en", "current-offset-notification").format(self._userOffset))
        
    def getPlayerPosition(self):
        if(not self._lastPlayerUpdate):
            if(self._lastGlobalUpdate):
                return self.getGlobalPosition()
            else:
                return 0.0
        position = self._playerPosition
        if(not self._playerPaused):
            diff = time.time() - self._lastPlayerUpdate
            position += diff 
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
        if not path:
            return
        try:
            size = os.path.getsize(path)
        except OSError: #file not accessible (stream?)
            size = 0
        self.userlist.currentUser.setFile(filename, duration, size)
        self.sendFile()
        self._malUpdater.fileChangeHook(filename, duration)
            
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
            self.getUserList()
            
    def getRoom(self):
        return self.userlist.currentUser.room
    
    def getUserList(self):
        if(self._protocol and self._protocol.logged):
            self._protocol.sendList()
    
    def showUserList(self):
        self.userlist.showUserList()
    
    def getPassword(self):
        return self._serverPassword
    
    def setPosition(self, position):
        position += self.getUserOffset() 
        if(self._player):
            if(position < 0):
                position = 0
                self._protocol.sendState(self.getPlayerPosition(), self.getPlayerPaused(), True, None, True) 
            self._player.setPosition(position)
    
    def setPaused(self, paused):
        if(self._player):
            self._player.setPaused(paused)
    
    def start(self, host, port):
        if self._running:
            return
        self._running = True
        if self._playerClass:
            self._playerClass.run(self, self._config['playerPath'], self._config['file'], self._config['playerArgs'])
            self._playerClass = None
        self.protocolFactory = SyncClientFactory(self)
        reactor.connectTCP(host, port, self.protocolFactory)
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
        if self.ui:
            self.ui.drop()
        reactor.callLater(0.1, reactor.stop)
        if(promptForAction):
            self.ui.promptFor(getMessage("en", "enter-to-exit-prompt"))

    class _WarningManager(object):
        def __init__(self, player, userlist, ui):
            self._player = player
            self._userlist = userlist
            self._ui = ui
            self._warnings = {
                            "room-files-not-same": {
                                                     "timer": task.LoopingCall(self.__displayMessageOnOSD, ("room-files-not-same"),),
                                                     "displayedFor": 0,
                                                    },
                            "alone-in-the-room": {
                                                     "timer": task.LoopingCall(self.__displayMessageOnOSD, ("alone-in-the-room"),),
                                                     "displayedFor": 0,
                                                    },
                            }
        def checkWarnings(self):
            self._checkIfYouReAloneInTheRoom()
            self._checkRoomForSameFiles()
                
        def _checkRoomForSameFiles(self):
            if (not self._userlist.areAllFilesInRoomSame()):
                self._ui.showMessage(getMessage("en", "room-files-not-same"), True)
                if(not self._warnings["room-files-not-same"]['timer'].running):
                    self._warnings["room-files-not-same"]['timer'].start(constants.WARNING_OSD_MESSAGES_LOOP_INTERVAL, True)
            elif(self._warnings["room-files-not-same"]['timer'].running):
                self._warnings["room-files-not-same"]['timer'].stop()
                
        def _checkIfYouReAloneInTheRoom(self):
            if (self._userlist.areYouAloneInRoom()):
                self._ui.showMessage(getMessage("en", "alone-in-the-room"), True)
                if(not self._warnings["alone-in-the-room"]['timer'].running):
                    self._warnings["alone-in-the-room"]['timer'].start(constants.WARNING_OSD_MESSAGES_LOOP_INTERVAL, True)
            elif(self._warnings["alone-in-the-room"]['timer'].running):
                self._warnings["alone-in-the-room"]['timer'].stop()
                
        def __displayMessageOnOSD(self, warningName):
            if (constants.OSD_WARNING_MESSAGE_DURATION > self._warnings[warningName]["displayedFor"]):
                self._ui.showOSDMessage(getMessage("en", warningName ), constants.WARNING_OSD_MESSAGES_LOOP_INTERVAL)
                self._warnings[warningName]["displayedFor"] += constants.WARNING_OSD_MESSAGES_LOOP_INTERVAL
            else:
                self._warnings[warningName]["displayedFor"] = 0
                self._warnings[warningName]["timer"].stop()
            


class SyncplayUser(object):
    def __init__(self, username = None, room = None, file_ = None, position = 0):
        self.username = username
        self.room = room
        self.file = file_
        self.lastPosition = position
        
    def setFile(self, filename, duration, size):
        file_ = {
                 "name": filename,
                 "duration": duration,
                 "size":size
                 }
        self.file = file_
    
    def isFileSame(self, file_):
        def stripfilename(filename): #TODO: Add proper Unicode support
            return re.sub(constants.FILENAME_STRIP_REGEX,"",filename) 
        
        if(not self.file):
            return False
        sameName = stripfilename(self.file['name']) == stripfilename(file_['name'])
        sameSize = self.file['size'] == file_['size']
        sameDuration = abs(int(self.file['duration']) - int(file_['duration'])) < constants.DIFFFERENT_DURATION_THRESHOLD
        return sameName and sameSize and sameDuration
      
    def __lt__(self, other):
        return self.username < other.username
      
      
class MalUpdater(object):
    def __init__(self, username, password, ui):
        self._filePlayingFor = 0.0
        self._lastHookUpdate = None
        self._fileDuration = 0
        self._filename = ""
        self.__username = username
        self.__password = password
        self._ui = ui

    def _updatePlayingTime(self, paused):
        if (not self._lastHookUpdate):
            self._lastHookUpdate = time.time()
        if (not paused):
            self._filePlayingFor += time.time() - self._lastHookUpdate
        self._lastHookUpdate = time.time()

    def playingHook(self, position, paused):
        if(self._fileDuration == 0):
            return
        self._updatePlayingTime(paused)
        pastMark = position / self._fileDuration > 0.4
        if self._filePlayingFor > 30 and pastMark:
            threading.Thread(target=self._updateMal).start()

    def fileChangeHook(self, filename, duration):
        self._fileDuration = duration
        self._filename = filename
        self._filePlayingFor = 0.0
        self._lastHookUpdate = None
        
    def _updateMal(self):
        try:
            self._fileDuration = 0  # Disable playingHook
            if(libMal and self._filename and self.__username and self.__password):
                manager = libMal.Manager(self.__username, self.__password)
                results = manager.findEntriesOnMal(self._filename)
                if(len(results) > 0):
                    result = results[0]
                    message = "Updating MAL with: \"{}\", episode: {}".format(result.mainTitle, result.episodeBeingWatched)
                    reactor.callFromThread(self._ui.showMessage,(message),)
                    options = {"tags": ["syncplay"]}
                    manager.updateEntryOnMal(result, options)
            self._filename = ""  # Make sure no updates will be performed until switch
        except:
            reactor.callFromThread(self._ui.showMessage, ("MAL Update failure"),) 
        
class SyncplayUserlist(object):
    def __init__(self, ui, client):
        self.currentUser = SyncplayUser()
        self._users = {}
        self.ui = ui
        self._client = client
        self._roomUsersChanged = True

    def __showUserChangeMessage(self, username, room, file_):
        if(room and not file_):
            message = getMessage("en", "room-join-notification").format(username, room)
            self.ui.showMessage(message)
        elif (room and file_):
            duration = utils.formatTime(file_['duration'])
            message = getMessage("en", "playing-notification").format(username, file_['name'], duration)
            if(self.currentUser.room <> room or self.currentUser.username == username):
                message += getMessage("en", "playing-notification/room-addendum").format(room)
            self.ui.showMessage(message)
            if(self.currentUser.file and not self.currentUser.isFileSame(file_) and self.currentUser.room == room):
                message = getMessage("en", "file-different-notification").format(username)
                self.ui.showMessage(message)
                differences = []
                if(self.currentUser.file['name'] <> file_['name']):
                    differences.append("filename") 
                if(self.currentUser.file['size'] <> file_['size']):
                    differences.append("size")
                if(self.currentUser.file['duration'] <> file_['duration']):
                    differences.append("duration")
                message = getMessage("en", "file-differences-notification") + ", ".join(differences)
                self.ui.showMessage(message)

    def addUser(self, username, room, file_, position = 0, noMessage = False):
        if(username == self.currentUser.username):
            self.currentUser.lastPosition = position
            return
        user = SyncplayUser(username, room, file_, position)
        self._users[username] = user
        if(not noMessage):
            self.__showUserChangeMessage(username, room, file_)
        self.userListChange()
            
    def removeUser(self, username):
        if(self._users.has_key(username)):
            self._users.pop(username)
            message = getMessage("en", "left-notification").format(username)
            self.ui.showMessage(message)
        self.userListChange()
        
    def __displayModUserMessage(self, username, room, file_, user):
        if (file_ and not user.isFileSame(file_)):
            self.__showUserChangeMessage(username, room, file_)
        elif (room and room != user.room):
            self.__showUserChangeMessage(username, room, None)

    def modUser(self, username, room, file_):
        if(self._users.has_key(username)):
            user = self._users[username]
            self.__displayModUserMessage(username, room, file_, user)
            user.room = room
            if file_:
                user.file = file_
        elif(username == self.currentUser.username):
            self.__showUserChangeMessage(username, room, file_)
        else:
            self.addUser(username, room, file_)
        self.userListChange()
                    
    def areAllFilesInRoomSame(self):
        for user in self._users.itervalues():
            if(user.room == self.currentUser.room and user.file and not self.currentUser.isFileSame(user.file)):
                return False
        return True
    
    def areYouAloneInRoom(self):
        for user in self._users.itervalues():
            if(user.room == self.currentUser.room):
                return False
        return True
    
    def userListChange(self):
        self._roomUsersChanged = True
        self.ui.userListChange()
        
    def roomStateConfirmed(self):
        self._roomUsersChanged = False
    
    def hasRoomStateChanged(self):
        return self._roomUsersChanged
        
    def showUserList(self):
        rooms = {}
        for user in self._users.itervalues():
            if(user.room not in rooms):
                rooms[user.room] = []
            rooms[user.room].append(user)
        if(self.currentUser.room not in rooms):
                rooms[self.currentUser.room] = []
        rooms[self.currentUser.room].append(self.currentUser)
        
        self.ui.showUserList(self.currentUser, rooms)
        
    def clearList(self):
        self._users = {}
              
class UiManager(object):
    def __init__(self, client, ui):
        self._client = client
        self.__ui = ui
    
    def showMessage(self, message, noPlayer = False, noTimestamp = False):
        if(not noPlayer): self.showOSDMessage(message)
        self.__ui.showMessage(message, noTimestamp)
    
    def showUserList(self, currentUser, rooms):
        self.__ui.showUserList(currentUser, rooms)
        
    def showOSDMessage(self, message, duration = constants.OSD_DURATION):
        if(self._client._player):
            self._client._player.displayMessage(message, duration * 1000)
    
    def showErrorMessage(self, message, criticalerror = False):
        self.__ui.showErrorMessage(message, criticalerror)

    def promptFor(self, prompt):
        return self.__ui.promptFor(prompt)
    
    def userListChange(self):
        self.__ui.userListChange()

    def markEndOfUserlist(self):
        self.__ui.markEndOfUserlist()
    
    def drop(self):
        self.__ui.drop()

    
