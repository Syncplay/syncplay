#coding:utf8
#TODO: #12, #13, #8;
import hashlib
from twisted.internet import task, reactor
from twisted.internet.protocol import Factory
import syncplay
from syncplay.protocols import SyncServerProtocol
import time
from syncplay import constants
import threading
from syncplay.messages import getMessage

class SyncFactory(Factory):
    def __init__(self, password = ''):
        print getMessage("en", "welcome-server-notification").format(syncplay.version)
        if(password):
            password = hashlib.md5(password).hexdigest()
        self.password = password
        self._rooms = {}
        self._roomStates = {}
        self._roomUpdate = threading.RLock()

    def buildProtocol(self, addr):
        return SyncServerProtocol(self)        
        
    def _createRoomIfDoesntExist(self, roomName):
        if (not self._rooms.has_key(roomName)):
            with self._roomUpdate:
                self._rooms[roomName] = {}
                self._roomStates[roomName] = {
                                              "position": 0.0,
                                              "paused": True,
                                              "setBy": None,
                                              "lastUpdate": time.time()
                                             }

    def addWatcher(self, watcherProtocol, username, roomName, roomPassword):
        allnames = []
        for room in self._rooms.itervalues():
            for watcher in room.itervalues():
                allnames.append(watcher.name.lower()) 
        while username.lower() in allnames:
            username += '_'
        self._createRoomIfDoesntExist(roomName)
        watcher = Watcher(self, watcherProtocol, username, roomName)
        with self._roomUpdate:
            self._rooms[roomName][watcherProtocol] = watcher
        print getMessage("en", "client-connected-room-server-notification").format(username, roomName, watcherProtocol.transport.getPeer().host)    
        reactor.callLater(0.1, watcher.scheduleSendState)
        l = lambda w: w.sendUserSetting(username, roomName, None, {"joined": True})
        self.broadcast(watcherProtocol, l)

    def getWatcher(self, watcherProtocol):
        for room in self._rooms.itervalues():
            if(room.has_key(watcherProtocol)):
                return room[watcherProtocol]

    def getAllWatchers(self, watcherProtocol): #TODO: Optimize me
        watchers = {}
        for room in self._rooms.itervalues():
            for watcher in room.itervalues():
                watchers[watcher.watcherProtocol] = watcher
        return watchers

    def _removeWatcherFromTheRoom(self, watcherProtocol):
        for room in self._rooms.itervalues():
            with self._roomUpdate:
                watcher = room.pop(watcherProtocol, None)
            if(watcher):
                return watcher

    def _deleteRoomIfEmpty(self, room):
        if (self._rooms[room] == {}):
            with self._roomUpdate:
                self._rooms.pop(room)
                self._roomStates.pop(room)
    
    def getRoomPausedAndPosition(self, room):
        position = self._roomStates[room]["position"]
        paused = self._roomStates[room]["paused"]
        if (not paused):
            timePassedSinceSet = time.time() - self._roomStates[room]["lastUpdate"]
            position += timePassedSinceSet
        return paused, position

    def sendState(self, watcherProtocol, doSeek = False, senderLatency = 0, forcedUpdate = False):
        watcher = self.getWatcher(watcherProtocol)
        if(not watcher):
            return
        room = watcher.room
        paused, position = self.getRoomPausedAndPosition(room)
        setBy = self._roomStates[room]["setBy"]
        watcher.paused = paused
        watcher.position = position
        watcherProtocol.sendState(position, paused, doSeek, setBy, senderLatency, watcher.latency, forcedUpdate)
        if(time.time() - watcher.lastUpdate > constants.PROTOCOL_TIMEOUT):
            watcherProtocol.drop()
            self.removeWatcher(watcherProtocol)
        
    def __updateWatcherPing(self, latencyCalculation, watcher):
        if (latencyCalculation):
            ping = (time.time() - latencyCalculation) / 2
            if (watcher.latency):
                watcher.latency = watcher.latency * (constants.PING_MOVING_AVERAGE_WEIGHT) + ping * (1-constants.PING_MOVING_AVERAGE_WEIGHT) #Exponential moving average 
            else:
                watcher.latency = ping

    def __shouldServerForceUpdateOnRoom(self, pauseChanged, doSeek):
        return doSeek or pauseChanged
            
    def __updatePausedState(self, paused, watcher):
        watcher.paused = paused
        if(self._roomStates[watcher.room]["paused"] <> paused):
            self._roomStates[watcher.room]["setBy"] = watcher.name
            self._roomStates[watcher.room]["paused"] = paused
            self._roomStates[watcher.room]["lastUpdate"] = time.time()
            return True
    
    def __updatePositionState(self, position, doSeek, watcher):
        watcher.position = position
        if (doSeek):
            self._roomStates[watcher.room]["position"] = position
            self._roomStates[watcher.room]["setBy"] = watcher.name
            self._roomStates[watcher.room]["lastUpdate"] = time.time()
        else:
            setter = min(self._rooms[watcher.room].values())
            self._roomStates[watcher.room]["position"] = setter.position
            self._roomStates[watcher.room]["setBy"] = setter.name 
            self._roomStates[watcher.room]["lastUpdate"] = setter.lastUpdate
            
    def updateWatcherState(self, watcherProtocol, position, paused, doSeek, latencyCalculation):
        watcher = self.getWatcher(watcherProtocol)
        self.__updateWatcherPing(latencyCalculation, watcher)
        watcher.lastUpdate = time.time()
        if(watcher.file):
            if(position is not None):
                self.__updatePositionState(position, doSeek, watcher)
            pauseChanged = False
            if(paused is not None):
                pauseChanged = self.__updatePausedState(paused, watcher)
            forceUpdate = self.__shouldServerForceUpdateOnRoom(pauseChanged, doSeek)
            if(forceUpdate):
                l = lambda w: self.sendState(w, doSeek, watcher.latency, forceUpdate)
                self.broadcastRoom(watcher.watcherProtocol, l)

    def removeWatcher(self, watcherProtocol):
        watcher = self.getWatcher(watcherProtocol)
        if(not watcher):
            return
        l = lambda w: w.sendUserSetting(watcher.name, watcher.room, None, {"left": True})
        self.broadcast(watcherProtocol, l)
        self._removeWatcherFromTheRoom(watcherProtocol)
        watcher.deactivate()
        self._deleteRoomIfEmpty(watcher.room)
        print getMessage("en", "client-left-server-notification").format(watcher.name) 
        
    def watcherGetUsername(self, watcherProtocol):
        return self.getWatcher(watcherProtocol).name
    
    def watcherGetRoom(self, watcherProtocol):
        return self.getWatcher(watcherProtocol).room
    
    def watcherSetRoom(self, watcherProtocol, room):
        watcher = self._removeWatcherFromTheRoom(watcherProtocol)
        if(not watcher):
            return
        watcher.resetStateTimer()
        oldRoom = watcher.room
        self._createRoomIfDoesntExist(room)
        with self._roomUpdate:
            self._rooms[room][watcherProtocol] = watcher
        self._roomStates[room]["position"] = watcher.position
        self._roomStates[room]["setBy"] = watcher.name
        self._roomStates[room]["lastUpdate"] = time.time()
        self._deleteRoomIfEmpty(oldRoom)
        watcher.room = room
        l = lambda w: w.sendUserSetting(watcher.name, watcher.room, watcher.file, None)
        self.broadcast(watcherProtocol, l)
                
    def watcherSetFile(self, watcherProtocol, file_):
        watcher = self.getWatcher(watcherProtocol)
        watcher.file = file_
        l = lambda w: w.sendUserSetting(watcher.name, watcher.room, watcher.file, None)
        self.broadcast(watcherProtocol, l)
    
    def broadcastRoom(self, sender, what):
        room = self._rooms[self.watcherGetRoom(sender)]
        if(room):
            with self._roomUpdate:
                for receiver in room:
                    what(receiver)
                
    def broadcast(self, sender, what):
        with self._roomUpdate:
            for room in self._rooms.itervalues():
                    for receiver in room:
                        what(receiver)
    
class SyncIsolatedFactory(SyncFactory):
    def broadcast(self, sender, what):
        self.broadcastRoom(sender, what)
        
    def getAllWatchers(self, watcherProtocol):
        room = self.getWatcher(watcherProtocol).room
        if(self._rooms.has_key(room)):
            return self._rooms[room]
        else:
            return {}
        
    def watcherSetRoom(self, watcherProtocol, room):
        watcher = self.getWatcher(watcherProtocol)
        oldRoom = watcher.room
        l = lambda w: w.sendUserSetting(watcher.name, oldRoom, None, {"left": True})
        self.broadcast(watcherProtocol, l)
        SyncFactory.watcherSetRoom(self, watcherProtocol, room)


class Watcher(object):
    def __init__(self, factory, watcherProtocol, name, room):
        self.factory = factory
        self.watcherProtocol = watcherProtocol
        self.name = name
        self.room = room
        self.file = None
        self._sendStateTimer = None
        self.position = None
        self.latency = 0
        self.lastUpdate = time.time()

    def __lt__(self, b):
        if(self.position is None):
            return False
        elif(b.position is None):
            return True
        else:
            return self.position < b.position

    def getRoomPosition(self):
        _, position = self.factory.getRoomPausedAndPosition(self.room)
        return position
    
    def scheduleSendState(self):
        self._sendStateTimer = task.LoopingCall(self.sendState)
        self._sendStateTimer.start(constants.SERVER_STATE_INTERVAL, True)

    def sendState(self):
        self.factory.sendState(self.watcherProtocol)
    
    def resetStateTimer(self):
        if(self._sendStateTimer):
            self._sendStateTimer.stop()
            self._sendStateTimer.start(constants.SERVER_STATE_INTERVAL) 
            
    def deactivate(self):
        if(self._sendStateTimer):
            self._sendStateTimer.stop()
    
