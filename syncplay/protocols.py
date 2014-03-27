# coding:utf8
from twisted.protocols.basic import LineReceiver
import json
import syncplay
from functools import wraps
import time
from syncplay.messages import getMessage
from syncplay.constants import PING_MOVING_AVERAGE_WEIGHT


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
                self.handleError(message[1])
            else:
                self.dropWithError(getMessage("en", "unknown-command-server-error").format(message[1]))  # TODO: log, not drop

    def lineReceived(self, line):
        line = line.strip()
        if not line:
            return
        try:
            messages = json.loads(line)
        except:
            if ("GET / HTTP/1." in line):
                self.handleHttpRequest(line)
                self.drop()
            else:
                self.dropWithError(getMessage("en", "not-json-server-error").format(line))
            return
        self.handleMessages(messages)

    def sendMessage(self, dict_):
        line = json.dumps(dict_)
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
        self._pingService = PingService()

    def connectionMade(self):
        self._client.initProtocol(self)
        self.sendHello()

    def connectionLost(self, reason):
        self._client.destroyProtocol()

    def dropWithError(self, error):
        self._client.protocolFactory.stopRetrying()
        self.drop()
        self._client.stop(error)

    def _extractHelloArguments(self, hello):
        username = hello["username"] if hello.has_key("username") else None
        roomName = hello["room"]["name"] if hello.has_key("room") else None
        version = hello["version"] if hello.has_key("version") else None
        motd = hello["motd"] if hello.has_key("motd") else None
        return username, roomName, version, motd

    def handleHello(self, hello):
        username, roomName, version, motd = self._extractHelloArguments(hello)
        if(not username or not roomName or not version):
            self.dropWithError(getMessage("en", "hello-server-error").format(hello))
        elif(version.split(".")[0:2] != syncplay.version.split(".")[0:2]):
            self.dropWithError(getMessage("en", "version-mismatch-server-error".format(hello)))
        else:
            self._client.setUsername(username)
            self._client.setRoom(roomName)
        self.logged = True
        if(motd):
            self._client.ui.showMessage(motd, True, True)
        self._client.ui.showMessage(getMessage("en", "connected-successful-notification"))
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
                    self._client.removeUser(username)
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
        self.sendList()

    def handleList(self, userList):
        self._client.userlist.clearList()
        for room in userList.iteritems():
            roomName = room[0]
            for user in room[1].iteritems():
                userName = user[0]
                file_ = user[1]['file'] if user[1]['file'] <> {} else None
                position = user[1]['position']
                self._client.userlist.addUser(userName, roomName, file_, position, noMessage=True)
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
        if (state["ping"].has_key("latencyCalculation")):
            latencyCalculation = state["ping"]["latencyCalculation"]
        if ("clientLatencyCalculation" in state["ping"]):
            timestamp = state["ping"]["clientLatencyCalculation"]
            senderRtt = state["ping"]["serverRtt"]
            self._pingService.receiveMessage(timestamp, senderRtt)
        messageAge = self._pingService.getLastForwardDelay()
        return messageAge, latencyCalculation

    def handleState(self, state):
        position, paused, doSeek, setBy = None, None, None, None
        messageAge = 0
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
            messageAge, latencyCalculation = self._handleStatePing(state)
        if(position is not None and paused is not None and not self.clientIgnoringOnTheFly):
            self._client.updateGlobalState(position, paused, doSeek, setBy, messageAge)
        position, paused, doSeek, stateChange = self._client.getLocalState()
        self.sendState(position, paused, doSeek, latencyCalculation, stateChange)

    def handleHttpRequest(self, request):
        pass

    def sendState(self, position, paused, doSeek, latencyCalculation, stateChange=False):
        state = {}
        positionAndPausedIsSet = position is not None and paused is not None
        clientIgnoreIsNotSet = self.clientIgnoringOnTheFly == 0 or self.serverIgnoringOnTheFly != 0
        if(clientIgnoreIsNotSet and positionAndPausedIsSet):
            state["playstate"] = {}
            state["playstate"]["position"] = position
            state["playstate"]["paused"] = paused
            if(doSeek): state["playstate"]["doSeek"] = doSeek
        state["ping"] = {}
        if(latencyCalculation):
            state["ping"]["latencyCalculation"] = latencyCalculation
        state["ping"]["clientLatencyCalculation"] = self._pingService.newTimestamp()
        state["ping"]["clientRtt"] = self._pingService.getRtt()
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
        self.dropWithError(error["message"])  # TODO: more processing and fallbacking

    def sendError(self, message):
        self.sendMessage({"Error": {"message": message}})


class SyncServerProtocol(JSONCommandProtocol):
    def __init__(self, factory):
        self._factory = factory
        self._logged = False
        self.clientIgnoringOnTheFly = 0
        self.serverIgnoringOnTheFly = 0
        self._pingService = PingService()
        self._clientLatencyCalculation = 0
        self._clientLatencyCalculationArrivalTime = 0
        
    def __hash__(self):
        return hash('|'.join((
            self.transport.getPeer().host,
            str(id(self)),
        )))

    def requireLogged(f):  # @NoSelf
        @wraps(f)
        def wrapper(self, *args, **kwds):
            if(not self._logged):
                self.dropWithError(getMessage("en", "not-known-server-error"))
            return f(self, *args, **kwds)
        return wrapper

    def dropWithError(self, error):
        print getMessage("en", "client-drop-server-error").format(self.transport.getPeer().host, error)
        self.sendError(error)
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
                self.dropWithError(getMessage("en", "password-required-server-error"))
                return False
            if(serverPassword != self._factory.password):
                self.dropWithError(getMessage("en", "wrong-password-server-error"))
                return False
        return True

    def handleHello(self, hello):
        username, serverPassword, roomName, roomPassword, version = self._extractHelloArguments(hello)
        if(not username or not roomName or not version):
            self.dropWithError(getMessage("en", "hello-server-error"))
        elif(version.split(".")[0:2] != syncplay.version.split(".")[0:2]):
            self.dropWithError(getMessage("en", "version-mismatch-server-error"))
        else:
            if(not self._checkPassword(serverPassword)):
                return
            self._factory.addWatcher(self, username, roomName, roomPassword)
            self._logged = True
            self.sendHello(version)

    def sendHello(self, clientVersion):
        hello = {}
        username = self._factory.watcherGetUsername(self)
        hello["username"] = username
        userIp = self.transport.getPeer().host
        room = self._factory.watcherGetRoom(self)
        if(room): hello["room"] = {"name": room}
        hello["version"] = syncplay.version
        hello["motd"] = self._factory.getMotd(userIp, username, room, clientVersion)
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

    def _addUserOnList(self, userlist, roomPositions, watcher):
        if (not userlist.has_key(watcher.room)):
            userlist[watcher.room] = {}
            roomPositions[watcher.room] = watcher.getRoomPosition()
        userlist[watcher.room][watcher.name] = {
                                                "file": watcher.file if watcher.file else {},
                                                "position": roomPositions[watcher.room] if roomPositions[watcher.room] else 0
                                                }
    def sendList(self):
        userlist = {}
        roomPositions = {}
        watchers = self._factory.getAllWatchers(self)
        for watcher in watchers.itervalues():
            self._addUserOnList(userlist, roomPositions, watcher)
        self.sendMessage({"List": userlist})

    @requireLogged
    def handleList(self, _):
        self.sendList()

    def sendState(self, position, paused, doSeek, setBy, forced=False):
        if(self._clientLatencyCalculationArrivalTime):
            processingTime = time.time() - self._clientLatencyCalculationArrivalTime
        else:
            processingTime = 0
        playstate = {
                     "position": position,
                     "paused": paused,
                     "doSeek": doSeek,
                     "setBy": setBy
                    }
        ping = {
                "latencyCalculation": self._pingService.newTimestamp(),
                "serverRtt": self._pingService.getRtt() 
                }
        if(self._clientLatencyCalculation):
            ping["clientLatencyCalculation"] = self._clientLatencyCalculation + processingTime
            self._clientLatencyCalculation = 0
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
            latencyCalculation = state["ping"]["latencyCalculation"] if state["ping"].has_key("latencyCalculation") else 0
            clientRtt = state["ping"]["clientRtt"] if state["ping"].has_key("clientRtt") else 0
            self._clientLatencyCalculation = state["ping"]["clientLatencyCalculation"] if state["ping"].has_key("clientLatencyCalculation") else 0
            self._clientLatencyCalculationArrivalTime = time.time()
            self._pingService.receiveMessage(latencyCalculation, clientRtt)
        if(self.serverIgnoringOnTheFly == 0):
            self._factory.updateWatcherState(self, position, paused, doSeek, self._pingService.getLastForwardDelay())

    def handleHttpRequest(self, request):
        self.sendLine(self._factory.gethttpRequestReply())

    def handleError(self, error):
        self.dropWithError(error["message"])  # TODO: more processing and fallbacking

    def sendError(self, message):
        self.sendMessage({"Error": {"message": message}})


class PingService(object):

    def __init__(self):
        self._rtt = 0
        self._fd = 0
        self._avrRtt = 0

    def newTimestamp(self):
        return time.time()

    def receiveMessage(self, timestamp, senderRtt):
        if(not timestamp):
            return
        self._rtt = time.time() - timestamp
        if(self._rtt < 0 or senderRtt < 0):
            return
        if(not self._avrRtt):
            self._avrRtt = self._rtt
        self._avrRtt = self._avrRtt * PING_MOVING_AVERAGE_WEIGHT + self._rtt * (1 - PING_MOVING_AVERAGE_WEIGHT)
        if(senderRtt < self._rtt):
            self._fd = self._avrRtt/2 + (self._rtt - senderRtt)
        else:
            self._fd = self._avrRtt/2

    def getLastForwardDelay(self):
        return self._fd

    def getRtt(self):
        return self._rtt
