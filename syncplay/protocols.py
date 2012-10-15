#coding:utf8
from twisted.protocols.basic import LineReceiver
import json
import syncplay
from functools import wraps
import time

class JSONCommandProtocol(LineReceiver): 
    def handleMessages(self, messages):
        for message in messages.iteritems():
            command = message[0]
            if command == "Hello":
                self.handleHello(message[1])
            elif command == "Set":
                self.handleSet(message[1])
            elif command == "List":
                self.handleList(message[1])
            elif command == "State":
                self.handleState(message[1])
            elif command == "Error":
                self.handleState(message[1])
            else:
                self.dropWithError("Unknown Command") #TODO: log, not drop

    def printReceived(self, line): #TODO: remove
#        print ">>i", line
        pass
        
    def printSent(self, line):
#        print "o<<", line
        pass

    def lineReceived(self, line):
        line = line.strip()
        if not line:
            return
        self.printReceived(line)
        try:
            messages = json.loads(line)
        except:
            self.dropWithError("Not a json encoded string")
            return
        self.handleMessages(messages) 
    
    def sendMessage(self, dict_):
        line = json.dumps(dict_)
        self.printSent(line)    
        self.sendLine(line)

    def drop(self):
        self.transport.loseConnection()

    def dropWithError(self, error):
        raise NotImplementedError()

class SyncClientProtocol(JSONCommandProtocol):
    def __init__(self, client):
        self._client = client
        self.clientIgnoringOnTheFly = 0
        self.serverIgnoringOnTheFly = 0
        self.logged = False
        
    def connectionMade(self):
        self._client.initProtocol(self)
        self.sendHello()

    def connectionLost(self, reason):
        self._client.destroyProtocol()
        
    def dropWithError(self, error):
        self._client.ui.showErrorMessage(error)
        self._client.protocolFactory.stopRetrying()
        self.drop()
    
    def _extractHelloArguments(self, hello):
        username = hello["username"] if hello.has_key("username") else None
        roomName = hello["room"]["name"] if hello.has_key("room") else None
        version = hello["version"] if hello.has_key("version") else None
        return username, roomName, version

    def handleHello(self, hello):
        username, roomName, version = self._extractHelloArguments(hello)
        if(not username or not roomName or not version):
            self.dropWithError("Not enough Hello arguments")
        elif(version.split(".")[0:2] != syncplay.version.split(".")[0:2]):
            self.dropWithError("Mismatch between versions of client and server")
        else:    
            self._client.setUsername(username)
            self._client.setRoom(roomName)
        self.logged = True
        self._client.sendFile()
    
    def sendHello(self):
        hello = {}
        hello["username"] = self._client.getUsername()  
        password = self._client.getPassword()
        if(password): hello["password"] = password
        room = self._client.getRoom()
        if(room): hello["room"] = {"name" :room}
        hello["version"] = syncplay.version
        self.sendMessage({"Hello": hello})
        
    def _SetUser(self, users):
        for user in users.iteritems():
            username = user[0]
            settings = user[1]
            room = settings["room"]["name"] if settings.has_key("room") else None 
            file_ = settings["file"] if settings.has_key("file") else None
            if(settings.has_key("event")):
                if(settings["event"].has_key("joined")):
                    self._client.userlist.addUser(username, room, file_)
                elif(settings["event"].has_key("left")):
                    self._client.userlist.removeUser(username)
            else:
                self._client.userlist.modUser(username, room, file_)
                            
    def handleSet(self, settings):
        for set_ in settings.iteritems():
            command = set_[0]
            if command == "room":
                roomName = set_[1]["name"] if set_[1].has_key("name") else None
                self._client.setRoom(roomName)
            elif command == "user":
                self._SetUser(set_[1])

    def sendSet(self, setting):
        self.sendMessage({"Set": setting})

    def sendRoomSetting(self, roomName, password=None):
        setting = {}
        setting["name"] = roomName
        if(password): setting["password"] = password
        self.sendSet({"room": setting})
        
    def sendFileSetting(self, file_):
        self.sendSet({"file": file_})

    def handleList(self, userList):
        for room in userList.iteritems():
            roomName = room[0]
            for user in room[1].iteritems():
                userName = user[0]
                file_ = user[1] if user[1] <> {} else None
                self._client.userlist.addUser(userName, roomName, file_, noMessage=True)
        self._client.userlist.showUserList()
     
    def sendList(self):   
        self.sendMessage({"List": None})
        
    def _extractStatePlaystateArguments(self, state):
        position = state["playstate"]["position"] if state["playstate"].has_key("position") else 0
        paused = state["playstate"]["paused"] if state["playstate"].has_key("paused") else None
        doSeek = state["playstate"]["doSeek"] if state["playstate"].has_key("doSeek") else None
        setBy = state["playstate"]["setBy"] if state["playstate"].has_key("setBy") else None
        return position, paused, doSeek, setBy

    def _handleStatePing(self, state):
        yourLatency = state["ping"]["yourLatency"] if state["ping"].has_key("yourLatency") else 0
        senderLatency = state["ping"]["senderLatency"] if state["ping"].has_key("senderLatency") else 0
        if (state["ping"].has_key("latencyCalculation")):
            latencyCalculation = state["ping"]["latencyCalculation"]
        return yourLatency, senderLatency, latencyCalculation

    def handleState(self, state):
        position, paused, doSeek, setBy = None, None, None, None
        yourLatency, senderLatency = 0, 0
        if(state.has_key("ignoringOnTheFly")):
            ignore = state["ignoringOnTheFly"]
            if(ignore.has_key("server")):
                self.serverIgnoringOnTheFly = ignore["server"]
                self.clientIgnoringOnTheFly = 0
            elif(ignore.has_key("client")): 
                if(ignore['client']) == self.clientIgnoringOnTheFly:
                    self.clientIgnoringOnTheFly = 0
        if(state.has_key("playstate")):
            position, paused, doSeek, setBy = self._extractStatePlaystateArguments(state)
        if(state.has_key("ping")):
            yourLatency, senderLatency, latencyCalculation = self._handleStatePing(state)
        if(position is not None and paused is not None and not self.clientIgnoringOnTheFly):
            latency = yourLatency + senderLatency 
            self._client.updateGlobalState(position, paused, doSeek, setBy, latency)
        position, paused, doSeek, stateChange = self._client.getLocalState()
        self.sendState(position, paused, doSeek, latencyCalculation, stateChange)
    
    def sendState(self, position, paused, doSeek, latencyCalculation, stateChange = False):
        state = {}
        positionAndPausedIsSet = position is not None and paused is not None
        clientIgnoreIsNotSet = self.clientIgnoringOnTheFly == 0 or self.serverIgnoringOnTheFly != 0 
        if(clientIgnoreIsNotSet and positionAndPausedIsSet):
            state["playstate"] = {}
            state["playstate"]["position"] = position
            state["playstate"]["paused"] = paused
            if(doSeek): state["playstate"]["doSeek"] = doSeek
        if(latencyCalculation):
            state["ping"] = {"latencyCalculation": latencyCalculation}
        if(stateChange):
            self.clientIgnoringOnTheFly += 1 
        if(self.serverIgnoringOnTheFly or self.clientIgnoringOnTheFly):
            state["ignoringOnTheFly"] = {}
            if(self.serverIgnoringOnTheFly):
                state["ignoringOnTheFly"]["server"] = self.serverIgnoringOnTheFly
                self.serverIgnoringOnTheFly = 0
            if(self.clientIgnoringOnTheFly):
                state["ignoringOnTheFly"]["client"] = self.clientIgnoringOnTheFly
        self.sendMessage({"State": state})
        
    def handleError(self, error):
        self.dropWithError(error["message"]) #TODO: more processing and fallbacking
        
    def sendError(self, message):
        self.sendMessage({"Error": {"message": message}})
        
        
class SyncServerProtocol(JSONCommandProtocol):
    def __init__(self, factory):
        self._factory = factory
        self._logged = False
        self.clientIgnoringOnTheFly = 0
        self.serverIgnoringOnTheFly = 0
        
    def __hash__(self):
        return hash('|'.join((
            self.transport.getPeer().host,
            str(id(self)),
        )))
     
    def requireLogged(f): #@NoSelf
        @wraps(f)
        def wrapper(self, *args, **kwds):
            if(not self._logged):
                self.dropWithError("You must be known to server before sending this command")
            return f(self, *args, **kwds)
        return wrapper
        
    def dropWithError(self, error):
        print "Client drop: %s -- %s" % (self.transport.getPeer().host, error)
        self.drop()
        
    def connectionLost(self, reason):
        self._factory.removeWatcher(self)    

    def _extractHelloArguments(self, hello):
        roomName, roomPassword = None, None
        username = hello["username"] if hello.has_key("username") else None
        username = username.strip()
        serverPassword = hello["password"] if hello.has_key("password") else None
        room = hello["room"] if hello.has_key("room") else None
        if(room):
            roomName = room["name"] if room.has_key("name") else None
            roomName = roomName.strip()
            roomPassword = room["password"] if room.has_key("password") else None
        version = hello["version"] if hello.has_key("version") else None
        return username, serverPassword, roomName, roomPassword, version

    def _checkPassword(self, serverPassword):
        if(self._factory.password):
            if(not serverPassword):
                self.dropWithError("Password required")
                return False
            if(serverPassword != self._factory.password):
                self.dropWithError("Wrong password supplied")
                return False
        return True
            
    def handleHello(self, hello):
        username, serverPassword, roomName, roomPassword, version = self._extractHelloArguments(hello)
        if(not username or not roomName or not version):
            self.dropWithError("Not enough Hello arguments")
        elif(version.split(".")[0:2] != syncplay.version.split(".")[0:2]):
            self.dropWithError("Mismatch between versions of client and server")
        else:
            if(not self._checkPassword(serverPassword)):
                return
            self._factory.addWatcher(self, username, roomName, roomPassword)
            self._logged = True
            self.sendHello()
            self.sendList()
    
    def sendHello(self):
        hello = {}
        hello["username"] = self._factory.watcherGetUsername(self)  
        room = self._factory.watcherGetRoom(self)
        if(room): hello["room"] = {"name": room}
        hello["version"] = syncplay.version
        self.sendMessage({"Hello": hello})
            
    @requireLogged
    def handleSet(self, settings):
        for set_ in settings.iteritems():
            command = set_[0]
            if command == "room":
                roomName = set_[1]["name"] if set_[1].has_key("name") else None
                self._factory.watcherSetRoom(self, roomName)
            elif command == "file":
                self._factory.watcherSetFile(self, set_[1])

    def sendSet(self, setting):
        self.sendMessage({"Set": setting})
        
    def sendRoomSetting(self, roomName):
        self.sendSet({"room": {"name": roomName}})
        
    def sendUserSetting(self, username, roomName, file_, event):
        room = {"name": roomName}
        user = {}
        user[username] = {}
        user[username]["room"] = room
        if(file_):
            user[username]["file"] = file_
        if(event):
            user[username]["event"] = event
        self.sendSet({"user": user})
 
    def _addUserOnList(self, userlist, watcher):
        if (not userlist.has_key(watcher.room)):
            userlist[watcher.room] = {}
        userlist[watcher.room][watcher.name] = watcher.file if watcher.file else {}
         
    def sendList(self):
        userlist = {}
        watchers = self._factory.getAllWatchers(self)
        for watcher in watchers.itervalues():
            self._addUserOnList(userlist, watcher)
        self.sendMessage({"List": userlist})
    
    @requireLogged
    def handleList(self, _):
        self.sendList()
    
    def sendState(self, position, paused, doSeek, setBy, senderLatency, watcherLatency, forced = False):
        playstate = {
                     "position": position,
                     "paused": paused,
                     "doSeek": doSeek,
                     "setBy": setBy
                    }
        ping = {
                "yourLatency": watcherLatency,
                "senderLatency": senderLatency,
                "latencyCalculation": time.time()
                }
        state = {
                 "ping": ping,
                 "playstate": playstate,
                }
        if(forced):
            self.serverIgnoringOnTheFly += 1
        if(self.serverIgnoringOnTheFly or self.clientIgnoringOnTheFly):
            state["ignoringOnTheFly"] = {}
            if(self.serverIgnoringOnTheFly):
                state["ignoringOnTheFly"]["server"] = self.serverIgnoringOnTheFly
            if(self.clientIgnoringOnTheFly):
                state["ignoringOnTheFly"]["client"] = self.clientIgnoringOnTheFly
                self.clientIgnoringOnTheFly = 0
        if(self.serverIgnoringOnTheFly == 0 or forced):
            self.sendMessage({"State": state})
    
            
    def _extractStatePlaystateArguments(self, state):
        position = state["playstate"]["position"] if state["playstate"].has_key("position") else 0
        paused = state["playstate"]["paused"] if state["playstate"].has_key("paused") else None
        doSeek = state["playstate"]["doSeek"] if state["playstate"].has_key("doSeek") else None
        return position, paused, doSeek

    @requireLogged
    def handleState(self, state):
        position, paused, doSeek, latencyCalculation = None, None, None, None
        if(state.has_key("ignoringOnTheFly")):
            ignore = state["ignoringOnTheFly"]
            if(ignore.has_key("server")):
                if(self.serverIgnoringOnTheFly == ignore["server"]):
                    self.serverIgnoringOnTheFly = 0
            if(ignore.has_key("client")):
                self.clientIgnoringOnTheFly = ignore["client"] 
        if(state.has_key("playstate")):
            position, paused, doSeek = self._extractStatePlaystateArguments(state)
        if(state.has_key("ping")):
            latencyCalculation = state["ping"]["latencyCalculation"] if state["ping"].has_key("latencyCalculation") else None
        if(self.serverIgnoringOnTheFly == 0):
            self._factory.updateWatcherState(self, position, paused, doSeek, latencyCalculation)
   
    def handleError(self, error):
        self.dropWithError(error["message"]) #TODO: more processing and fallbacking
        
    def sendError(self, message):
        self.sendMessage({"Error": {"message": message}})
        
