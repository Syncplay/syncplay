import hashlib
import random
from twisted.internet import task, reactor
from twisted.internet.protocol import Factory
import syncplay
from syncplay.protocols import SyncServerProtocol
import time
from syncplay import constants
from syncplay.messages import getMessage
import codecs
import os
from string import Template
import argparse
from syncplay.utils import RoomPasswordProvider, NotControlledRoom, RandomStringGenerator, meetsMinVersion, playlistIsValid, truncateText

class SyncFactory(Factory):
    def __init__(self, password='', motdFilePath=None, isolateRooms=False, salt=None, disableReady=False,disableChat=False, maxChatMessageLength=constants.MAX_CHAT_MESSAGE_LENGTH):
        self.isolateRooms = isolateRooms
        print getMessage("welcome-server-notification").format(syncplay.version)
        if password:
            password = hashlib.md5(password).hexdigest()
        self.password = password
        if salt is None:
            salt = RandomStringGenerator.generate_server_salt()
            print getMessage("no-salt-notification").format(salt)
        self._salt = salt
        self._motdFilePath = motdFilePath
        self.disableReady = disableReady
        self.disableChat = disableChat
        self.maxChatMessageLength = maxChatMessageLength
        if not isolateRooms:
            self._roomManager = RoomManager()
        else:
            self._roomManager = PublicRoomManager()

    def buildProtocol(self, addr):
        return SyncServerProtocol(self)

    def sendState(self, watcher, doSeek=False, forcedUpdate=False):
        room = watcher.getRoom()
        if room:
            paused, position = room.isPaused(), room.getPosition()
            setBy = room.getSetBy()
            watcher.sendState(position, paused, doSeek, setBy, forcedUpdate)

    def getFeatures(self):
        features = dict()
        features["isolateRooms"] = self.isolateRooms
        features["readiness"] = not self.disableReady
        features["managedRooms"] = True
        features["chat"] = not self.disableChat
        features["maxChatMessageLength"] = self.maxChatMessageLength
        features["maxUsernameLength"] = constants.MAX_USERNAME_LENGTH
        features["maxRoomNameLength"] = constants.MAX_ROOM_NAME_LENGTH
        features["maxFilenameLength"] = constants.MAX_FILENAME_LENGTH

        return features

    def getMotd(self, userIp, username, room, clientVersion):
        oldClient = False
        if constants.WARN_OLD_CLIENTS:
            if not meetsMinVersion(clientVersion, constants.RECENT_CLIENT_THRESHOLD):
                oldClient = True
        if self._motdFilePath and os.path.isfile(self._motdFilePath):
            tmpl = codecs.open(self._motdFilePath, "r", "utf-8-sig").read()
            args = dict(version=syncplay.version, userIp=userIp, username=username, room=room)
            try:
                motd = Template(tmpl).substitute(args)
                if oldClient:
                    motdwarning = getMessage("new-syncplay-available-motd-message").format(clientVersion)
                    motd = "{}\n{}".format(motdwarning, motd)
                return motd if len(motd) < constants.SERVER_MAX_TEMPLATE_LENGTH else getMessage("server-messed-up-motd-too-long").format(constants.SERVER_MAX_TEMPLATE_LENGTH, len(motd))
            except ValueError:
                return getMessage("server-messed-up-motd-unescaped-placeholders")
        elif oldClient:
            return getMessage("new-syncplay-available-motd-message").format(clientVersion)
        else:
            return ""

    def addWatcher(self, watcherProtocol, username, roomName):
        roomName = truncateText(roomName, constants.MAX_ROOM_NAME_LENGTH)
        username = self._roomManager.findFreeUsername(username)
        watcher = Watcher(self, watcherProtocol, username)
        self.setWatcherRoom(watcher, roomName, asJoin=True)

    def setWatcherRoom(self, watcher, roomName, asJoin=False):
        roomName = truncateText(roomName, constants.MAX_ROOM_NAME_LENGTH)
        self._roomManager.moveWatcher(watcher, roomName)
        if asJoin:
            self.sendJoinMessage(watcher)
        else:
            self.sendRoomSwitchMessage(watcher)

        room = watcher.getRoom()
        roomSetByName = room.getSetBy().getName() if room.getSetBy() else None
        watcher.setPlaylist(roomSetByName, room.getPlaylist())
        watcher.setPlaylistIndex(roomSetByName, room.getPlaylistIndex())
        if RoomPasswordProvider.isControlledRoom(roomName):
            for controller in room.getControllers():
                watcher.sendControlledRoomAuthStatus(True, controller, roomName)

    def sendRoomSwitchMessage(self, watcher):
        l = lambda w: w.sendSetting(watcher.getName(), watcher.getRoom(), None, None)
        self._roomManager.broadcast(watcher, l)
        self._roomManager.broadcastRoom(watcher, lambda w: w.sendSetReady(watcher.getName(), watcher.isReady(), False))

    def removeWatcher(self, watcher):
        if watcher and watcher.getRoom():
            self.sendLeftMessage(watcher)
            self._roomManager.removeWatcher(watcher)

    def sendLeftMessage(self, watcher):
        l = lambda w: w.sendSetting(watcher.getName(), watcher.getRoom(), None, {"left": True})
        self._roomManager.broadcast(watcher, l)

    def sendJoinMessage(self, watcher):
        l = lambda w: w.sendSetting(watcher.getName(), watcher.getRoom(), None, {"joined": True, "version": watcher.getVersion(), "features": watcher.getFeatures()}) if w != watcher else None
        self._roomManager.broadcast(watcher, l)
        self._roomManager.broadcastRoom(watcher, lambda w: w.sendSetReady(watcher.getName(), watcher.isReady(), False))

    def sendFileUpdate(self, watcher):
        if watcher.getFile():
            l = lambda w: w.sendSetting(watcher.getName(), watcher.getRoom(), watcher.getFile(), None)
            self._roomManager.broadcast(watcher, l)

    def forcePositionUpdate(self, watcher, doSeek, watcherPauseState):
        room = watcher.getRoom()
        if room.canControl(watcher):
            paused, position = room.isPaused(), watcher.getPosition()
            setBy = watcher
            l = lambda w: w.sendState(position, paused, doSeek, setBy, True)
            room.setPosition(watcher.getPosition(), setBy)
            self._roomManager.broadcastRoom(watcher, l)
        else:
            watcher.sendState(room.getPosition(), watcherPauseState, False, watcher, True) # Fixes BC break with 1.2.x
            watcher.sendState(room.getPosition(), room.isPaused(), True, room.getSetBy(), True)

    def getAllWatchersForUser(self, forUser):
        return self._roomManager.getAllWatchersForUser(forUser)

    def authRoomController(self, watcher, password, roomBaseName=None):
        room = watcher.getRoom()
        roomName = roomBaseName if roomBaseName else room.getName()
        try:
            success = RoomPasswordProvider.check(roomName, password, self._salt)
            if success:
                watcher.getRoom().addController(watcher)
            self._roomManager.broadcast(watcher, lambda w: w.sendControlledRoomAuthStatus(success, watcher.getName(), room._name))
        except NotControlledRoom:
            newName = RoomPasswordProvider.getControlledRoomName(roomName, password, self._salt)
            watcher.sendNewControlledRoom(newName, password)
        except ValueError:
            self._roomManager.broadcastRoom(watcher, lambda w: w.sendControlledRoomAuthStatus(False, watcher.getName(), room._name))

    def sendChat(self,watcher,message):
        message = truncateText(message, constants.MAX_CHAT_MESSAGE_LENGTH)
        messageDict={"message":message,"username" : watcher.getName()}
        self._roomManager.broadcastRoom(watcher, lambda w: w.sendChatMessage(messageDict))

    def setReady(self, watcher, isReady, manuallyInitiated=True):
        watcher.setReady(isReady)
        self._roomManager.broadcastRoom(watcher, lambda w: w.sendSetReady(watcher.getName(), watcher.isReady(), manuallyInitiated))

    def setPlaylist(self, watcher, files):
        room = watcher.getRoom()
        if room.canControl(watcher) and playlistIsValid(files):
            watcher.getRoom().setPlaylist(files, watcher)
            self._roomManager.broadcastRoom(watcher, lambda w: w.setPlaylist(watcher.getName(), files))
        else:
            watcher.setPlaylist(room.getName(), room.getPlaylist())
            watcher.setPlaylistIndex(room.getName(), room.getPlaylistIndex())

    def setPlaylistIndex(self, watcher, index):
        room = watcher.getRoom()
        if room.canControl(watcher):
            watcher.getRoom().setPlaylistIndex(index, watcher)
            self._roomManager.broadcastRoom(watcher, lambda w: w.setPlaylistIndex(watcher.getName(), index))
        else:
            watcher.setPlaylistIndex(room.getName(), room.getPlaylistIndex())

class RoomManager(object):
    def __init__(self):
        self._rooms = {}

    def broadcastRoom(self, sender, whatLambda):
        room = sender.getRoom()
        if room and room.getName() in self._rooms:
            for receiver in room.getWatchers():
                whatLambda(receiver)

    def broadcast(self, sender, whatLambda):
        for room in self._rooms.itervalues():
            for receiver in room.getWatchers():
                whatLambda(receiver)

    def getAllWatchersForUser(self, sender):
        watchers = []
        for room in self._rooms.itervalues():
            for watcher in room.getWatchers():
                watchers.append(watcher)
        return watchers

    def moveWatcher(self, watcher, roomName):
        roomName = truncateText(roomName, constants.MAX_ROOM_NAME_LENGTH)
        self.removeWatcher(watcher)
        room = self._getRoom(roomName)
        room.addWatcher(watcher)

    def removeWatcher(self, watcher):
        oldRoom = watcher.getRoom()
        if oldRoom:
            oldRoom.removeWatcher(watcher)
            self._deleteRoomIfEmpty(oldRoom)

    def _getRoom(self, roomName):
        if roomName in self._rooms:
            return self._rooms[roomName]
        else:
            if RoomPasswordProvider.isControlledRoom(roomName):
                room = ControlledRoom(roomName)
            else:
                room = Room(roomName)
            self._rooms[roomName] = room
            return room

    def _deleteRoomIfEmpty(self, room):
        if room.isEmpty() and room.getName() in self._rooms:
            del self._rooms[room.getName()]

    def findFreeUsername(self, username):
        username = truncateText(username,constants.MAX_USERNAME_LENGTH)
        allnames = []
        for room in self._rooms.itervalues():
            for watcher in room.getWatchers():
                allnames.append(watcher.getName().lower())
        while username.lower() in allnames:
            username += '_'
        return username


class PublicRoomManager(RoomManager):
    def broadcast(self, sender, what):
        self.broadcastRoom(sender, what)

    def getAllWatchersForUser(self, sender):
        return sender.getRoom().getWatchers()

    def moveWatcher(self, watcher, room):
        oldRoom = watcher.getRoom()
        l = lambda w: w.sendSetting(watcher.getName(), oldRoom, None, {"left": True})
        self.broadcast(watcher, l)
        RoomManager.moveWatcher(self, watcher, room)
        watcher.setFile(watcher.getFile())


class Room(object):
    STATE_PAUSED = 0
    STATE_PLAYING = 1

    def __init__(self, name):
        self._name = name
        self._watchers = {}
        self._playState = self.STATE_PAUSED
        self._setBy = None
        self._playlist = []
        self._playlistIndex = None
        self._lastUpdate = time.time()
        self._position = 0

    def __str__(self, *args, **kwargs):
        return self.getName()

    def getName(self):
        return self._name

    def getPosition(self):
        age = time.time() - self._lastUpdate
        if self._watchers and age > 1:
            watcher = min(self._watchers.values())
            self._setBy = watcher
            self._position = watcher.getPosition()
            self._lastUpdate = time.time()
            return self._position
        elif self._position is not None:
            return self._position + (age if self._playState == self.STATE_PLAYING else 0)
        else:
            return 0

    def setPaused(self, paused=STATE_PAUSED, setBy=None):
        self._playState = paused
        self._setBy = setBy

    def setPosition(self, position, setBy=None):
        self._position = position
        for watcher in self._watchers.itervalues():
            watcher.setPosition(position)
            self._setBy = setBy

    def isPlaying(self):
        return self._playState == self.STATE_PLAYING

    def isPaused(self):
        return self._playState == self.STATE_PAUSED

    def getWatchers(self):
        return self._watchers.values()

    def addWatcher(self, watcher):
        if self._watchers:
            watcher.setPosition(self.getPosition())
        self._watchers[watcher.getName()] = watcher
        watcher.setRoom(self)

    def removeWatcher(self, watcher):
        if watcher.getName() not in self._watchers:
            return
        del self._watchers[watcher.getName()]
        watcher.setRoom(None)
        if not self._watchers:
            self._position = 0

    def isEmpty(self):
        return not bool(self._watchers)

    def getSetBy(self):
        return self._setBy

    def canControl(self, watcher):
        return True

    def setPlaylist(self, files, setBy=None):
        self._playlist = files

    def setPlaylistIndex(self, index, setBy=None):
        self._playlistIndex = index

    def getPlaylist(self):
        return self._playlist

    def getPlaylistIndex(self):
        return self._playlistIndex

class ControlledRoom(Room):
    def __init__(self, name):
        Room.__init__(self, name)
        self._controllers = {}

    def getPosition(self):
        age = time.time() - self._lastUpdate
        if self._controllers and age > 1:
            watcher = min(self._controllers.values())
            self._setBy = watcher
            self._position = watcher.getPosition()
            self._lastUpdate = time.time()
            return self._position
        elif self._position is not None:
            return self._position + (age if self._playState == self.STATE_PLAYING else 0)
        else:
            return 0

    def addController(self, watcher):
        self._controllers[watcher.getName()] = watcher

    def removeWatcher(self, watcher):
        Room.removeWatcher(self, watcher)
        if watcher.getName() in self._controllers:
            del self._controllers[watcher.getName()]

    def setPaused(self, paused=Room.STATE_PAUSED, setBy=None):
        if self.canControl(setBy):
            Room.setPaused(self, paused, setBy)

    def setPosition(self, position, setBy=None):
        if self.canControl(setBy):
            Room.setPosition(self, position, setBy)

    def setPlaylist(self, files, setBy=None):
        if self.canControl(setBy) and playlistIsValid(files):
            self._playlist = files

    def setPlaylistIndex(self, index, setBy=None):
        if self.canControl(setBy):
            self._playlistIndex = index

    def canControl(self, watcher):
        return watcher.getName() in self._controllers

    def getControllers(self):
        return self._controllers

class Watcher(object):
    def __init__(self, server, connector, name):
        self._ready = None
        self._server = server
        self._connector = connector
        self._name = name
        self._room = None
        self._file = None
        self._position = None
        self._lastUpdatedOn = time.time()
        self._sendStateTimer = None
        self._connector.setWatcher(self)
        reactor.callLater(0.1, self._scheduleSendState)

    def setFile(self, file_):
        if file_ and file_.has_key("name"):
            file_["name"] = truncateText(file_["name"],constants.MAX_FILENAME_LENGTH)
        self._file = file_
        self._server.sendFileUpdate(self)

    def setRoom(self, room):
        self._room = room
        if room is None:
            self._deactivateStateTimer()
        else:
            self._resetStateTimer()
            self._askForStateUpdate(True, True)

    def setReady(self, ready):
        self._ready = ready

    def getFeatures(self):
        features = self._connector.getFeatures()
        return features

    def isReady(self):
        if self._server.disableReady:
            return None
        return self._ready

    def getRoom(self):
        return self._room

    def getName(self):
        return self._name

    def getVersion(self):
        return self._connector.getVersion()

    def getFile(self):
        return self._file

    def setPosition(self, position):
        self._position = position

    def getPosition(self):
        if self._position is None:
            return None
        if self._room.isPlaying():
            timePassedSinceSet = time.time() - self._lastUpdatedOn
        else:
            timePassedSinceSet = 0
        return self._position + timePassedSinceSet

    def sendSetting(self, user, room, file_, event):
        self._connector.sendUserSetting(user, room, file_, event)

    def sendNewControlledRoom(self, roomBaseName, password):
        self._connector.sendNewControlledRoom(roomBaseName, password)

    def sendControlledRoomAuthStatus(self, success, username, room):
        self._connector.sendControlledRoomAuthStatus(success, username, room)

    def sendChatMessage(self,message):
        if self._connector.meetsMinVersion(constants.CHAT_MIN_VERSION):
            self._connector.sendMessage({"Chat" : message})

    def sendSetReady(self, username, isReady, manuallyInitiated=True):
        self._connector.sendSetReady(username, isReady, manuallyInitiated)

    def setPlaylistIndex(self, username, index):
         self._connector.setPlaylistIndex(username, index)

    def setPlaylist(self, username, files):
        self._connector.setPlaylist(username, files)

    def __lt__(self, b):
        if self.getPosition() is None or self._file is None:
            return False
        if b.getPosition() is None or b.getFile() is None:
            return True
        return self.getPosition() < b.getPosition()

    def _scheduleSendState(self):
        self._sendStateTimer = task.LoopingCall(self._askForStateUpdate)
        self._sendStateTimer.start(constants.SERVER_STATE_INTERVAL)

    def _askForStateUpdate(self, doSeek=False, forcedUpdate=False):
        self._server.sendState(self, doSeek, forcedUpdate)

    def _resetStateTimer(self):
        if self._sendStateTimer:
            if self._sendStateTimer.running:
                self._sendStateTimer.stop()
            self._sendStateTimer.start(constants.SERVER_STATE_INTERVAL)

    def _deactivateStateTimer(self):
        if self._sendStateTimer and self._sendStateTimer.running:
            self._sendStateTimer.stop()

    def sendState(self, position, paused, doSeek, setBy, forcedUpdate):
        if self._connector.isLogged():
            self._connector.sendState(position, paused, doSeek, setBy, forcedUpdate)
        if time.time() - self._lastUpdatedOn > constants.PROTOCOL_TIMEOUT:
            self._server.removeWatcher(self)
            self._connector.drop()

    def __hasPauseChanged(self, paused):
        if paused is None:
            return False
        return self._room.isPaused() and not paused or not self._room.isPaused() and paused

    def _updatePositionByAge(self, messageAge, paused, position):
        if not paused:
            position += messageAge
        return position

    def updateState(self, position, paused, doSeek, messageAge):
        pauseChanged = self.__hasPauseChanged(paused)
        self._lastUpdatedOn = time.time()
        if pauseChanged:
            self.getRoom().setPaused(Room.STATE_PAUSED if paused else Room.STATE_PLAYING, self)
        if position is not None:
            position = self._updatePositionByAge(messageAge, paused, position)
            self.setPosition(position)
        if doSeek or pauseChanged:
            self._server.forcePositionUpdate(self, doSeek, paused)

    def isController(self):
        return RoomPasswordProvider.isControlledRoom(self._room.getName()) \
            and self._room.canControl(self)

class ConfigurationGetter(object):
    def getConfiguration(self):
        self._prepareArgParser()
        args = self._argparser.parse_args()
        if args.port is None:
            args.port = constants.DEFAULT_PORT
        return args

    def _prepareArgParser(self):
        self._argparser = argparse.ArgumentParser(description=getMessage("server-argument-description"),
                                         epilog=getMessage("server-argument-epilog"))
        self._argparser.add_argument('--port', metavar='port', type=str, nargs='?', help=getMessage("server-port-argument"))
        self._argparser.add_argument('--password', metavar='password', type=str, nargs='?', help=getMessage("server-password-argument"))
        self._argparser.add_argument('--isolate-rooms', action='store_true', help=getMessage("server-isolate-room-argument"))
        self._argparser.add_argument('--disable-ready', action='store_true', help=getMessage("server-disable-ready-argument"))
        self._argparser.add_argument('--disable-chat', action='store_true', help=getMessage("server-chat-argument"))
        self._argparser.add_argument('--salt', metavar='salt', type=str, nargs='?', help=getMessage("server-salt-argument"))
        self._argparser.add_argument('--motd-file', metavar='file', type=str, nargs='?', help=getMessage("server-motd-argument"))
        self._argparser.add_argument('--max-chat-message-length', metavar='maxChatMessageLength', type=int, nargs='?',help=getMessage("server-chat-maxchars-argument").format(constants.MAX_CHAT_MESSAGE_LENGTH))
