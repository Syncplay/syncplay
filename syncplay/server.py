import argparse
import codecs
import hashlib
import os
import random
import time
import json
from string import Template

from twisted.enterprise import adbapi
from twisted.internet import task, reactor
from twisted.internet.protocol import Factory

try:
    from OpenSSL import crypto
    from OpenSSL.SSL import TLSv1_2_METHOD
    from twisted.internet import ssl
except:
    pass

import syncplay
from syncplay import constants
from syncplay.messages import getMessage
from syncplay.protocols import SyncServerProtocol
from syncplay.utils import RoomPasswordProvider, NotControlledRoom, RandomStringGenerator, meetsMinVersion, playlistIsValid, truncateText, getListAsMultilineString, convertMultilineStringToList

class SyncFactory(Factory):
    def __init__(self, port='', password='', motdFilePath=None, roomsDbFile=None, permanentRoomsFile=None, isolateRooms=False, salt=None,
                 disableReady=False, disableChat=False, maxChatMessageLength=constants.MAX_CHAT_MESSAGE_LENGTH,
                 maxUsernameLength=constants.MAX_USERNAME_LENGTH, statsDbFile=None, tlsCertPath=None):
        self.isolateRooms = isolateRooms
        syncplay.messages.setLanguage(syncplay.messages.getInitialLanguage())
        print(getMessage("welcome-server-notification").format(syncplay.version))
        self.port = port
        if password:
            password = password.encode('utf-8')
            password = hashlib.md5(password).hexdigest()
        self.password = password
        if salt is None:
            salt = RandomStringGenerator.generate_server_salt()
            print(getMessage("no-salt-notification").format(salt))
        self._salt = salt
        self._motdFilePath = motdFilePath
        self.roomsDbFile = roomsDbFile
        self.disableReady = disableReady
        self.disableChat = disableChat
        self.maxChatMessageLength = maxChatMessageLength if maxChatMessageLength is not None else constants.MAX_CHAT_MESSAGE_LENGTH
        self.maxUsernameLength = maxUsernameLength if maxUsernameLength is not None else constants.MAX_USERNAME_LENGTH
        self.permanentRoomsFile = permanentRoomsFile if permanentRoomsFile is not None and os.path.isfile(permanentRoomsFile) else None
        self.permanentRooms = self.loadListFromMultilineTextFile(self.permanentRoomsFile)
        if not isolateRooms:
            self._roomManager = RoomManager(self.roomsDbFile, self.permanentRooms)
        else:
            self._roomManager = PublicRoomManager()
        if statsDbFile is not None:
            self._statsDbHandle = StatsDBManager(statsDbFile)
            self._statsRecorder = StatsRecorder(self._statsDbHandle, self._roomManager)
            statsDelay = 5*(int(self.port)%10 + 1)
            self._statsRecorder.startRecorder(statsDelay)
        else:
            self._statsDbHandle = None
        if tlsCertPath is not None:
            self.certPath = tlsCertPath
            self._TLSattempts = 0
            self._allowTLSconnections(self.certPath)
        else:
            self.certPath = None
            self.options = None
            self.serverAcceptsTLS = False

    def loadListFromMultilineTextFile(self, path):
        if not os.path.isfile(path):
            return []
        with open(path) as f:
            multiline = f.read().splitlines()
        return multiline

    def loadRoom(self):
        rooms = self._roomsDbHandle.loadRooms()

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
        features["persistentRooms"] = self.roomsDbFile is not None
        features["chat"] = not self.disableChat
        features["maxChatMessageLength"] = self.maxChatMessageLength
        features["maxUsernameLength"] = self.maxUsernameLength
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
            watcher.sendState(room.getPosition(), watcherPauseState, False, watcher, True)  # Fixes BC break with 1.2.x
            watcher.sendState(room.getPosition(), room.isPaused(), True, room.getSetBy(), True)

    def getAllWatchersForUser(self, forUser):
        return self._roomManager.getAllWatchersForUser(forUser)

    def getEmptyPersistentRooms(self):
        return self._roomManager.getEmptyPersistentRooms()

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

    def sendChat(self, watcher, message):
        message = truncateText(message, self.maxChatMessageLength)
        messageDict = {"message": message, "username": watcher.getName()}
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

    def _allowTLSconnections(self, path):
        try:
            privKey = open(path+'/privkey.pem', 'rt').read()
            certif = open(path+'/cert.pem', 'rt').read()
            chain = open(path+'/chain.pem', 'rt').read()

            self.lastEditCertTime = os.path.getmtime(path+'/cert.pem')

            privKeyPySSL = crypto.load_privatekey(crypto.FILETYPE_PEM, privKey)
            certifPySSL = crypto.load_certificate(crypto.FILETYPE_PEM, certif)
            chainPySSL = [crypto.load_certificate(crypto.FILETYPE_PEM, chain)]

            cipherListString = "ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:"\
                               "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:"\
                               "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384"
            accCiphers = ssl.AcceptableCiphers.fromOpenSSLCipherString(cipherListString)

            try:
                contextFactory = ssl.CertificateOptions(privateKey=privKeyPySSL, certificate=certifPySSL,
                                                        extraCertChain=chainPySSL, acceptableCiphers=accCiphers,
                                                        raiseMinimumTo=ssl.TLSVersion.TLSv1_2)
            except AttributeError:
                contextFactory = ssl.CertificateOptions(privateKey=privKeyPySSL, certificate=certifPySSL,
                                                        extraCertChain=chainPySSL, acceptableCiphers=accCiphers,
                                                        method=TLSv1_2_METHOD)

            self.options = contextFactory
            self.serverAcceptsTLS = True
            self._TLSattempts = 0
            print("TLS support is enabled.")
        except Exception as e:
            self.options = None
            self.serverAcceptsTLS = False
            self.lastEditCertTime = None
            print("Error while loading the TLS certificates.")
            print(e)
            print("TLS support is not enabled.")

    def checkLastEditCertTime(self):
        try:
            outTime = os.path.getmtime(self.certPath+'/cert.pem')
        except:
            outTime = None
        return outTime

    def updateTLSContextFactory(self):
        self._allowTLSconnections(self.certPath)
        self._TLSattempts += 1
        if self._TLSattempts < constants.TLS_CERT_ROTATION_MAX_RETRIES:
            self.serverAcceptsTLS = True


class StatsRecorder(object):
    def __init__(self, dbHandle, roomManager):
        self._dbHandle = dbHandle
        self._roomManagerHandle = roomManager
        
    def startRecorder(self, delay):
        try:
            self._dbHandle.connect()
            reactor.callLater(delay, self._scheduleClientSnapshot)
        except:
            print("--- Error in initializing the stats database. Server Stats not enabled. ---")
    
    def _scheduleClientSnapshot(self):
        self._clientSnapshotTimer = task.LoopingCall(self._runClientSnapshot)
        self._clientSnapshotTimer.start(constants.SERVER_STATS_SNAPSHOT_INTERVAL)    
    
    def _runClientSnapshot(self):
        try:
            snapshotTime = int(time.time())
            rooms = self._roomManagerHandle.exportRooms()
            for room in rooms.values():
                for watcher in room.getWatchers():
                    self._dbHandle.addVersionLog(snapshotTime, watcher.getVersion())
        except:
            pass

class RoomsRecorder(StatsRecorder):
    def __init__(self, dbHandle, roomManager):
        self._dbHandle = dbHandle
        self._roomManagerHandle = roomManager

    def startRecorder(self, delay):
        try:
            self._dbHandle.connect()
            reactor.callLater(delay, self._scheduleClientSnapshot) # TODO: FIX THIS!
        except:
            print("--- Error in initializing the stats database. Server Stats not enabled. ---")

    def _scheduleClientSnapshot(self):
        self._clientSnapshotTimer = task.LoopingCall(self._runClientSnapshot)
        self._clientSnapshotTimer.start(constants.SERVER_STATS_SNAPSHOT_INTERVAL)

    def _runClientSnapshot(self):
        try:
            snapshotTime = int(time.time())
            rooms = self._roomManagerHandle.exportRooms()
            for room in rooms.values():
                for watcher in room.getWatchers():
                    self._dbHandle.addVersionLog(snapshotTime, watcher.getVersion())
        except:
            pass

class StatsDBManager(object):
    def __init__(self, dbpath):
        self._dbPath = dbpath
        self._connection = None

    def __del__(self):
        if self._connection is not None:
            self._connection.close()

    def connect(self):
        self._connection = adbapi.ConnectionPool("sqlite3", self._dbPath, check_same_thread=False)
        self._createSchema()

    def _createSchema(self):
        initQuery = 'create table if not exists clients_snapshots (snapshot_time INTEGER, version STRING)'
        return self._connection.runQuery(initQuery)

    def addVersionLog(self, timestamp, version):
        content = (timestamp, version, )
        self._connection.runQuery("INSERT INTO clients_snapshots VALUES (?, ?)", content)

class RoomDBManager(object):
    def __init__(self, dbpath, loadroomscallback):
        self._dbPath = dbpath
        self._connection = None
        self._loadRoomsCallback = loadroomscallback

    def __del__(self):
        if self._connection is not None:
            self._connection.close()

    def connect(self):
        self._connection = adbapi.ConnectionPool("sqlite3", self._dbPath, check_same_thread=False)
        self._createSchema().addCallback(self.loadRooms)

    def _createSchema(self):
        initQuery = 'create table if not exists persistent_rooms (name STRING PRIMARY KEY, playlist STRING, playlistIndex INTEGER, position REAL, lastSavedUpdate INTEGER)'
        return self._connection.runQuery(initQuery)

    def saveRoom(self, name, playlist, playlistIndex, position, lastUpdate):
        content = (name, playlist, playlistIndex, position, lastUpdate)
        self._connection.runQuery("INSERT OR REPLACE INTO persistent_rooms VALUES (?, ?, ?, ?, ?)", content)

    def deleteRoom(self, name):
        self._connection.runQuery("DELETE FROM persistent_rooms where name = ?", [name])

    def loadRooms(self, result=None):
        roomsQuery = "SELECT * FROM persistent_rooms"
        rooms = self._connection.runQuery(roomsQuery)
        rooms.addCallback(self.loadedRooms)

    def loadedRooms(self, rooms):
        self._loadRoomsCallback(rooms)

class RoomManager(object):
    def __init__(self, roomsdbfile=None, permanentRooms=[]):
        self._roomsDbFile = roomsdbfile
        self._rooms = {}
        self._permanentRooms = permanentRooms
        if self._roomsDbFile is not None:
            self._roomsDbHandle = RoomDBManager(self._roomsDbFile, self.loadRooms)
            self._roomsDbHandle.connect()
        else:
            self._roomsDbHandle = None

    def loadRooms(self, rooms):
        roomsLoaded = []
        for roomDetails in rooms:
            roomName = truncateText(roomDetails[0], constants.MAX_ROOM_NAME_LENGTH)
            room = Room(roomDetails[0], self._roomsDbHandle)
            room.loadRoom(roomDetails)
            if roomName in self._permanentRooms:
                room.setPermanent(True)
            self._rooms[roomName] = room
            roomsLoaded.append(roomName)
        for roomName in self._permanentRooms:
            if roomName not in roomsLoaded:
                roomDetails = (roomName, "", 0, 0, 0)
                room = Room(roomName, self._roomsDbHandle)
                room.loadRoom(roomDetails)
                room.setPermanent(True)
                self._rooms[roomName] = room

    def broadcastRoom(self, sender, whatLambda):
        room = sender.getRoom()
        if room and room.getName() in self._rooms:
            for receiver in room.getWatchers():
                whatLambda(receiver)

    def broadcast(self, sender, whatLambda):
        for room in self._rooms.values():
            for receiver in room.getWatchers():
                whatLambda(receiver)

    def getAllWatchersForUser(self, sender):
        watchers = []
        for room in self._rooms.values():
            for watcher in room.getWatchers():
                watchers.append(watcher)
        return watchers

    def getPersistentRooms(self, sender):
        persistentRooms = []
        for room in self._rooms.values():
            if room.isPersistent():
                persistentRooms.append(room.getName())
        return persistentRooms

    def getEmptyPersistentRooms(self):
        emptyPersistentRooms = []
        for room in self._rooms.values():
            if len(room.getWatchers()) == 0:
                emptyPersistentRooms.append(room.getName())
        return emptyPersistentRooms

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
                if roomName in self._rooms:
                    self._deleteRoomIfEmpty(self._rooms[roomName])
                room = Room(roomName, self._roomsDbHandle)
            self._rooms[roomName] = room
            return room

    def _deleteRoomIfEmpty(self, room):
        if room.isEmpty() and room.isNotPermanent() and room.getName() in self._rooms:
            if room.isPersistent():
                if room.isPlaylistEmpty():
                    self._roomsDbHandle.deleteRoom(room.getName())
                else:
                    return()
            del self._rooms[room.getName()]

    def findFreeUsername(self, username):
        username = truncateText(username, constants.MAX_USERNAME_LENGTH)
        allnames = []
        for room in self._rooms.values():
            for watcher in room.getWatchers():
                allnames.append(watcher.getName().lower())
        while username.lower() in allnames:
            username += '_'
        return username
    
    def exportRooms(self):
        return self._rooms


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

    def __init__(self, name, roomsdbhandle):
        self._name = name
        self._roomsDbHandle = roomsdbhandle
        self._watchers = {}
        self._playState = self.STATE_PAUSED
        self._setBy = None
        self._playlist = []
        self._playlistIndex = None
        self._lastUpdate = time.time()
        self._lastSavedUpdate = 0
        self._position = 0
        self._permanent = False

    def __str__(self, *args, **kwargs):
        return self.getName()

    def roomsCanPersist(self):
        return self._roomsDbHandle is not None

    def isPersistent(self):
        return self.roomsCanPersist() and not self.isMarkedAsTemporary()

    def isMarkedAsTemporary(self):
        return "-temp" in self.getName()

    def isPlaylistEmpty(self):
        return len(self._playlist) == 0

    def isPermanent(self):
        return self._permanent

    def isNotPermanent(self):
        return not self.isPermanent()

    def sanitizeFilename(self, filename, blacklist="<>:/\\|?*\"", placeholder="_"):
        return ''.join([c if c not in blacklist and ord(c) >= 32 else placeholder for c in filename])

    def writeToDb(self):
        if not self.isPersistent():
            return
        processed_playlist = getListAsMultilineString(self._playlist)
        self._roomsDbHandle.saveRoom(self._name, processed_playlist, self._playlistIndex, self._position, self._lastSavedUpdate)

    def loadRoom(self, room):
        name, playlist, playlistindex, position, lastupdate = room
        self._name = name
        self._playlist = convertMultilineStringToList(playlist)
        self._playlistIndex = playlistindex
        self._position = position
        self._lastSavedUpdate = lastupdate

    def getName(self):
        return self._name

    def getPosition(self):
        age = time.time() - self._lastUpdate
        if self._watchers and age > 1:
            watcher = min(self._watchers.values())
            self._setBy = watcher
            self._position = watcher.getPosition()
            self._lastSavedUpdate = self._lastUpdate = time.time()
            return self._position
        elif self._position is not None:
            return self._position + (age if self._playState == self.STATE_PLAYING else 0)
        else:
            return 0

    def setPaused(self, paused=STATE_PAUSED, setBy=None):
        self._playState = paused
        self._setBy = setBy
        self.writeToDb()

    def setPosition(self, position, setBy=None):
        self._position = position
        for watcher in self._watchers.values():
            watcher.setPosition(position)
            self._setBy = setBy
        self.writeToDb()

    def setPermanent(self, newState):
        self._permanent = newState

    def isPlaying(self):
        return self._playState == self.STATE_PLAYING

    def isPaused(self):
        return self._playState == self.STATE_PAUSED

    def getWatchers(self):
        return list(self._watchers.values())

    def addWatcher(self, watcher):
        if self._watchers or self.isPersistent():
            watcher.setPosition(self.getPosition())
        self._watchers[watcher.getName()] = watcher
        watcher.setRoom(self)

    def removeWatcher(self, watcher):
        if watcher.getName() not in self._watchers:
            return
        del self._watchers[watcher.getName()]
        watcher.setRoom(None)
        if not self._watchers and not self.isPersistent():
            self._position = 0
        self.writeToDb()

    def isEmpty(self):
        return not bool(self._watchers)

    def getSetBy(self):
        return self._setBy

    def canControl(self, watcher):
        return True

    def setPlaylist(self, files, setBy=None):
        self._playlist = files
        self.writeToDb()

    def setPlaylistIndex(self, index, setBy=None):
        self._playlistIndex = index
        self.writeToDb()

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
        if file_ and "name" in file_:
            file_["name"] = truncateText(file_["name"], constants.MAX_FILENAME_LENGTH)
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

    def sendChatMessage(self, message):
        if self._connector.meetsMinVersion(constants.CHAT_MIN_VERSION):
            self._connector.sendMessage({"Chat": message})

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
        self._argparser = argparse.ArgumentParser(
            description=getMessage("server-argument-description"),
            epilog=getMessage("server-argument-epilog"))
        self._argparser.add_argument('--port', metavar='port', type=str, nargs='?', help=getMessage("server-port-argument"))
        self._argparser.add_argument('--password', metavar='password', type=str, nargs='?', help=getMessage("server-password-argument"), default=os.environ.get('SYNCPLAY_PASSWORD'))
        self._argparser.add_argument('--isolate-rooms', action='store_true', help=getMessage("server-isolate-room-argument"))
        self._argparser.add_argument('--disable-ready', action='store_true', help=getMessage("server-disable-ready-argument"))
        self._argparser.add_argument('--disable-chat', action='store_true', help=getMessage("server-chat-argument"))
        self._argparser.add_argument('--salt', metavar='salt', type=str, nargs='?', help=getMessage("server-salt-argument"), default=os.environ.get('SYNCPLAY_SALT'))
        self._argparser.add_argument('--motd-file', metavar='file', type=str, nargs='?', help=getMessage("server-motd-argument"))
        self._argparser.add_argument('--rooms-db-file', metavar='rooms', type=str, nargs='?', help=getMessage("server-rooms-argument"))
        self._argparser.add_argument('--permanent-rooms-file', metavar='permanentrooms', type=str, nargs='?', help=getMessage("server-permanent-rooms-argument"))
        self._argparser.add_argument('--max-chat-message-length', metavar='maxChatMessageLength', type=int, nargs='?', help=getMessage("server-chat-maxchars-argument").format(constants.MAX_CHAT_MESSAGE_LENGTH))
        self._argparser.add_argument('--max-username-length', metavar='maxUsernameLength', type=int, nargs='?', help=getMessage("server-maxusernamelength-argument").format(constants.MAX_USERNAME_LENGTH))
        self._argparser.add_argument('--stats-db-file', metavar='file', type=str, nargs='?', help=getMessage("server-stats-db-file-argument"))
        self._argparser.add_argument('--tls', metavar='path', type=str, nargs='?', help=getMessage("server-startTLS-argument"))
