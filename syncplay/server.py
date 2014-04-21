import hashlib
from twisted.internet import task, reactor
from twisted.internet.protocol import Factory
import syncplay
from syncplay.protocols import SyncServerProtocol
import time
from syncplay import constants
import threading
from syncplay.messages import getMessage
import codecs
import os
from string import Template
import argparse
from pprint import pprint

class SyncFactory(Factory):
    def __init__(self, password='', motdFilePath=None, isolateRooms=False):
        print getMessage("en", "welcome-server-notification").format(syncplay.version)
        if(password):
            password = hashlib.md5(password).hexdigest()
        self.password = password
        self._motdFilePath = motdFilePath
        if(not isolateRooms):
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

    def getMotd(self, userIp, username, room, clientVersion):
        oldClient = False
        if constants.WARN_OLD_CLIENTS:
            if int(clientVersion.replace(".", "")) < int(constants.RECENT_CLIENT_THRESHOLD.replace(".", "")):
                oldClient = True
        if(self._motdFilePath and os.path.isfile(self._motdFilePath)):
            tmpl = codecs.open(self._motdFilePath, "r", "utf-8-sig").read()
            args = dict(version=syncplay.version, userIp=userIp, username=username, room=room)
            try:
                motd = Template(tmpl).substitute(args)
                if oldClient:
                    motdwarning = getMessage("en", "new-syncplay-available-motd-message").format(clientVersion)
                    motd = "{}\n{}".format(motdwarning, motd)
                return motd if len(motd) < constants.SERVER_MAX_TEMPLATE_LENGTH else getMessage("en", "server-messed-up-motd-too-long").format(constants.SERVER_MAX_TEMPLATE_LENGTH, len(motd))
            except ValueError:
                return getMessage("en", "server-messed-up-motd-unescaped-placeholders")
        elif oldClient:
            return getMessage("en", "new-syncplay-available-motd-message").format(clientVersion)
        else:
            return ""

    def addWatcher(self, watcherProtocol, username, roomName, roomPassword):
        username = self._roomManager.findFreeUsername(username)
        watcher = Watcher(self, watcherProtocol, username)
        self.setWatcherRoom(watcher, roomName)

    def setWatcherRoom(self, watcher, roomName):
        self._roomManager.moveWatcher(watcher, roomName)
        self.sendJoinMessage(watcher)

    def removeWatcher(self, watcher):
        self.sendLeftMessage(watcher)
        self._roomManager.removeWatcher(watcher)

    def sendLeftMessage(self, watcher):
        l = lambda w: w.sendSetting(watcher.getName(), watcher.getRoom(), None, {"left": True})
        self._roomManager.broadcast(watcher, l)

    def sendJoinMessage(self, watcher):
        l = lambda w: w.sendSetting(watcher.getName(), watcher.getRoom(), None, {"joined": True})
        self._roomManager.broadcast(watcher, l)

    def sendFileUpdate(self, watcher, file_):
        l = lambda w: w.sendSetting(watcher.getName(), watcher.getRoom(), watcher.getFile(), None)
        self._roomManager.broadcast(watcher, l)

    def forcePositionUpdate(self, room, watcher, doSeek):
        room = watcher.getRoom()
        paused, position = room.isPaused(), watcher.getPosition()
        setBy = watcher
        l = lambda w: w.sendState(position, paused, doSeek, setBy, True)
        self._roomManager.broadcastRoom(watcher, l)

    def getAllWatchersForUser(self, forUser):
        return self._roomManager.getAllWatchersForUser(forUser)

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

    def getAllWatchersForUser(self, watcher):
        watchers = []
        for room in self._rooms.itervalues():
            for watcher in room.getWatchers():
                watchers.append(watcher)
        return watchers

    def moveWatcher(self, watcher, roomName):
        self.removeWatcher(watcher)
        room = self._getRoom(roomName)
        room.addWatcher(watcher)
        l = lambda w: w.sendSetting(watcher.getName(), watcher.getRoom(), None, None)
        self.broadcast(watcher, l)

    def removeWatcher(self, watcher):
        oldRoom = watcher.getRoom()
        if(oldRoom):
            oldRoom.removeWatcher(watcher)
            self._deleteRoomIfEmpty(oldRoom)

    def _getRoom(self, roomName):
        if roomName in self._rooms:
            return self._rooms[roomName]
        else:
            room = Room(roomName)
            self._rooms[roomName] = room
            return room

    def _deleteRoomIfEmpty(self, room):
        if room.isEmpty() and room.getName() in self._rooms:
            del self._rooms[room.getName()]

    def findFreeUsername(self, username):
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

    def getAllWatchersForUser(self, watcher):
        room = sender.getRoom().getWatchers()

    def moveWatcher(self, watcher, room):
        oldRoom = watcher.room
        l = lambda w: w.sendSetting(watcher.getName(), oldRoom, None, {"left": True})
        self.broadcast(watcher, l)
        RoomManager.watcherSetRoom(self, watcher, room)
        watcher.setFile(watcher.getFile())


class Room(object):
    STATE_PAUSED = 0
    STATE_PLAYING = 1

    def __init__(self, name):
        self._name = name
        self._watchers = {}
        self._playState = self.STATE_PAUSED
        self._setBy = None

    def __str__(self, *args, **kwargs):
        return self.getName()

    def getName(self):
        return self._name

    def getPosition(self):
        watcher = min(self._watchers.values())
        self._setBy = watcher
        return watcher.getPosition()

    def setPaused(self, paused=STATE_PAUSED, setBy=None):
        self._playState = paused
        self._setBy = setBy

    def isPlaying(self):
        return self._playState == self.STATE_PLAYING

    def isPaused(self):
        return self._playState == self.STATE_PAUSED

    def getWatchers(self):
        return self._watchers.values()

    def addWatcher(self, watcher):
        self._watchers[watcher.getName()] = watcher
        watcher.setRoom(self)

    def removeWatcher(self, watcher):
        if(watcher.getName() not in self._watchers):
            return
        del self._watchers[watcher.getName()]
        watcher.setRoom(None)

    def isEmpty(self):
        return bool(self._watchers)

    def getSetBy(self):
        return self._setBy

class Watcher(object):
    def __init__(self, server, connector, name):
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

    def setFile(self, file):
        self._file = file
        self._server.sendFileUpdate(self, file)

    def setRoom(self, room):
        self._room = room
        if room is None:
            self._deactivateStateTimer()
        else:
            self._resetStateTimer()
            self._askForStateUpdate(True, True)

    def getRoom(self):
        return self._room

    def getName(self):
        return self._name

    def getFile(self):
        return self._file

    def getPosition(self):
        if self._position is None:
            return None
        if self._room.isPlaying():
            timePassedSinceSet = time.time() - self._lastUpdatedOn
        else:
            timePassedSinceSet = 0
        return self._position + timePassedSinceSet

    def sendSetting(self, username, roomName, file_, event):
        self._connector.sendUserSetting(username, roomName, file_, event)

    def __lt__(self, b):
        if self.getPosition() is None:
            return False
        if b.getPosition is None:
            return True
        return self.getPosition() < b.getPosition()

    def _scheduleSendState(self):
        self._sendStateTimer = task.LoopingCall(self._askForStateUpdate)
        self._sendStateTimer.start(constants.SERVER_STATE_INTERVAL, True)

    def _askForStateUpdate(self, doSeek=False, forcedUpdate=False):
        self._server.sendState(self, doSeek, forcedUpdate)

    def _resetStateTimer(self):
        if self._sendStateTimer:
            if self._sendStateTimer.running:
                self._sendStateTimer.stop()
            self._sendStateTimer.start(constants.SERVER_STATE_INTERVAL)

    def _deactivateStateTimer(self):
        if(self._sendStateTimer and self._sendStateTimer.running):
            self._sendStateTimer.stop()

    def sendState(self, position, paused, doSeek, setBy, forcedUpdate):
        self._connector.sendState(position, paused, doSeek, setBy, forcedUpdate)
        if time.time() - self._lastUpdatedOn > constants.PROTOCOL_TIMEOUT:
            self._server.removeWatcher(self)
            self._connector.drop()

    def __hasPauseChanged(self, paused):
        return self._room.isPaused() and not paused or not self._room.isPaused() and paused

    def updateState(self, position, paused, doSeek, messageAge):
        if(self._file):
            oldPosition = self.getPosition()
            pauseChanged = False
            if(paused is not None):
                pauseChanged = self.__hasPauseChanged(paused)
                if pauseChanged:
                    self.getRoom().setPaused(Room.STATE_PAUSED if paused else Room.STATE_PLAYING, self)
            if(position is not None):
                if(not paused):
                    position += messageAge
                self._position = position
                self._lastUpdatedOn = time.time()
            if(doSeek or pauseChanged):
                self._server.forcePositionUpdate(self._room, self, doSeek)


class ConfigurationGetter(object):
    def getConfiguration(self):
        self._prepareArgParser()
        self._args = self._argparser.parse_args()
        if(self._args.port == None):
            self._args.port = constants.DEFAULT_PORT
        return self._args

    def _prepareArgParser(self):
        self._argparser = argparse.ArgumentParser(description=getMessage("en", "server-argument-description"),
                                         epilog=getMessage("en", "server-argument-epilog"))
        self._argparser.add_argument('--port', metavar='port', type=str, nargs='?', help=getMessage("en", "server-port-argument"))
        self._argparser.add_argument('--password', metavar='password', type=str, nargs='?', help=getMessage("en", "server-password-argument"))
        self._argparser.add_argument('--isolate-rooms', action='store_true', help=getMessage("en", "server-isolate-room-argument"))
        self._argparser.add_argument('--motd-file', metavar='file', type=str, nargs='?', help=getMessage("en", "server-motd-argument"))
