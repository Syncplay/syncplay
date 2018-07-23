# coding:utf8
from twisted.protocols.basic import LineReceiver
import json
import syncplay
from functools import wraps
import time
from syncplay.messages import getMessage
from syncplay.constants import PING_MOVING_AVERAGE_WEIGHT, CONTROLLED_ROOMS_MIN_VERSION, USER_READY_MIN_VERSION, SHARED_PLAYLIST_MIN_VERSION, CHAT_MIN_VERSION
from syncplay.utils import meetsMinVersion

class JSONCommandProtocol(LineReceiver):
    def handleMessages(self, messages):
        for message in messages.items():
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
            elif command == "Chat":
                self.handleChat(message[1])
            else:
                self.dropWithError(getMessage("unknown-command-server-error").format(message[1]))  # TODO: log, not drop

    def lineReceived(self, line):
        line = line.decode('utf-8').strip()
        if not line:
            return
        try:
            self.showDebugMessage("client/server << {}".format(line))
            messages = json.loads(line)
        except:
            self.dropWithError(getMessage("not-json-server-error").format(line))
            return
        self.handleMessages(messages)

    def sendMessage(self, dict_):
        line = json.dumps(dict_)
        self.sendLine(line.encode('utf-8'))
        self.showDebugMessage("client/server >> {}".format(line))

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

    def showDebugMessage(self, line):
        self._client.ui.showDebugMessage(line)

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
        username = hello["username"] if "username" in hello else None
        roomName = hello["room"]["name"] if "room" in hello else None
        version = hello["version"] if "version" in hello else None
        version = hello["realversion"] if "realversion" in hello else version # Used for 1.2.X compatibility
        motd = hello["motd"] if "motd" in hello else None
        features = hello["features"] if "features" in hello else None
        return username, roomName, version, motd, features

    def handleHello(self, hello):
        username, roomName, version, motd, featureList = self._extractHelloArguments(hello)
        if not username or not roomName or not version:
            self.dropWithError(getMessage("hello-server-error").format(hello))
        else:
            self._client.setUsername(username)
            self._client.setRoom(roomName)
        self.logged = True
        if motd:
            self._client.ui.showMessage(motd, True, True)
        self._client.ui.showMessage(getMessage("connected-successful-notification"))
        self._client.connected()
        self._client.sendFile()
        self._client.setServerVersion(version, featureList)

    def sendHello(self):
        hello = {}
        hello["username"] = self._client.getUsername()
        password = self._client.getPassword()
        if password: hello["password"] = password
        room = self._client.getRoom()
        if room: hello["room"] = {"name" :room}
        hello["version"] = "1.2.255" # Used so newer clients work on 1.2.X server
        hello["realversion"] = syncplay.version
        hello["features"] = self._client.getFeatures()
        self.sendMessage({"Hello": hello})

    def _SetUser(self, users):
        for user in users.items():
            username = user[0]
            settings = user[1]
            room = settings["room"]["name"] if "room" in settings else None
            file_ = settings["file"] if "file" in settings else None
            if "event" in settings:
                if "joined" in settings["event"]:
                    self._client.userlist.addUser(username, room, file_)
                elif "left" in settings["event"]:
                    self._client.removeUser(username)
            else:
                self._client.userlist.modUser(username, room, file_)

    def handleSet(self, settings):
        for (command, values) in settings.items():
            if command == "room":
                roomName = values["name"] if "name" in values else None
                self._client.setRoom(roomName)
            elif command == "user":
                self._SetUser(values)
            elif command == "controllerAuth":
                if values['success']:
                    self._client.controllerIdentificationSuccess(values["user"], values["room"])
                else:
                    self._client.controllerIdentificationError(values["user"], values["room"])
            elif command == "newControlledRoom":
                controlPassword = values['password']
                roomName = values['roomName']
                self._client.controlledRoomCreated(roomName, controlPassword)
            elif command == "ready":
                user, isReady = values["username"], values["isReady"]
                manuallyInitiated = values["manuallyInitiated"] if "manuallyInitiated" in values else True
                self._client.setReady(user, isReady, manuallyInitiated)
            elif command == "playlistIndex":
                self._client.playlist.changeToPlaylistIndex(values['index'], values['user'])
            elif command == "playlistChange":
                self._client.playlist.changePlaylist(values['files'], values['user'])
            elif command == "features":
                self._client.setUserFeatures(values["username"],values['features'])

    def sendFeaturesUpdate(self, features):
        self.sendSet({"features": features})

    def sendSet(self, setting):
        self.sendMessage({"Set": setting})

    def sendRoomSetting(self, roomName, password=None):
        setting = {}
        setting["name"] = roomName
        if password: setting["password"] = password
        self.sendSet({"room": setting})

    def sendFileSetting(self, file_):
        self.sendSet({"file": file_})
        self.sendList()

    def sendChatMessage(self,chatMessage):
        self.sendMessage({"Chat": chatMessage})

    def handleList(self, userList):
        self._client.userlist.clearList()
        for room in userList.items():
            roomName = room[0]
            for user in room[1].items():
                userName = user[0]
                file_ = user[1]['file'] if user[1]['file'] != {} else None
                isController = user[1]['controller'] if 'controller' in user[1] else False
                isReady = user[1]['isReady'] if 'isReady' in user[1] else None
                features = user[1]['features'] if 'features' in user[1] else None
                self._client.userlist.addUser(userName, roomName, file_, noMessage=True, isController=isController, isReady=isReady, features=features)
        self._client.userlist.showUserList()

    def sendList(self):
        self.sendMessage({"List": None})

    def _extractStatePlaystateArguments(self, state):
        position = state["playstate"]["position"] if "position" in state["playstate"] else 0
        paused = state["playstate"]["paused"] if "paused" in state["playstate"] else None
        doSeek = state["playstate"]["doSeek"] if "doSeek" in state["playstate"] else None
        setBy = state["playstate"]["setBy"] if "setBy" in state["playstate"] else None
        return position, paused, doSeek, setBy

    def _handleStatePing(self, state):
        if "latencyCalculation" in state["ping"]:
            latencyCalculation = state["ping"]["latencyCalculation"]
        if "clientLatencyCalculation" in state["ping"]:
            timestamp = state["ping"]["clientLatencyCalculation"]
            senderRtt = state["ping"]["serverRtt"]
            self._pingService.receiveMessage(timestamp, senderRtt)
        messageAge = self._pingService.getLastForwardDelay()
        return messageAge, latencyCalculation

    def handleState(self, state):
        position, paused, doSeek, setBy = None, None, None, None
        messageAge = 0
        if "ignoringOnTheFly" in state:
            ignore = state["ignoringOnTheFly"]
            if "server" in ignore:
                self.serverIgnoringOnTheFly = ignore["server"]
                self.clientIgnoringOnTheFly = 0
            elif "client" in ignore:
                if(ignore['client']) == self.clientIgnoringOnTheFly:
                    self.clientIgnoringOnTheFly = 0
        if "playstate" in state:
            position, paused, doSeek, setBy = self._extractStatePlaystateArguments(state)
        if "ping" in state:
            messageAge, latencyCalculation = self._handleStatePing(state)
        if position is not None and paused is not None and not self.clientIgnoringOnTheFly:
            self._client.updateGlobalState(position, paused, doSeek, setBy, messageAge)
        position, paused, doSeek, stateChange = self._client.getLocalState()
        self.sendState(position, paused, doSeek, latencyCalculation, stateChange)

    def sendState(self, position, paused, doSeek, latencyCalculation, stateChange=False):
        state = {}
        positionAndPausedIsSet = position is not None and paused is not None
        clientIgnoreIsNotSet = self.clientIgnoringOnTheFly == 0 or self.serverIgnoringOnTheFly != 0
        if clientIgnoreIsNotSet and positionAndPausedIsSet:
            state["playstate"] = {}
            state["playstate"]["position"] = position
            state["playstate"]["paused"] = paused
            if doSeek: state["playstate"]["doSeek"] = doSeek
        state["ping"] = {}
        if latencyCalculation:
            state["ping"]["latencyCalculation"] = latencyCalculation
        state["ping"]["clientLatencyCalculation"] = self._pingService.newTimestamp()
        state["ping"]["clientRtt"] = self._pingService.getRtt()
        if stateChange:
            self.clientIgnoringOnTheFly += 1
        if self.serverIgnoringOnTheFly or self.clientIgnoringOnTheFly:
            state["ignoringOnTheFly"] = {}
            if self.serverIgnoringOnTheFly:
                state["ignoringOnTheFly"]["server"] = self.serverIgnoringOnTheFly
                self.serverIgnoringOnTheFly = 0
            if self.clientIgnoringOnTheFly:
                state["ignoringOnTheFly"]["client"] = self.clientIgnoringOnTheFly
        self.sendMessage({"State": state})

    def requestControlledRoom(self, room, password):
        self.sendSet({
            "controllerAuth": {
                "room": room,
                "password": password
            }
        })
    def handleChat(self,message):
        username = message['username']
        userMessage = message['message']
        self._client.ui.showChatMessage(username, userMessage)

    def setReady(self, isReady, manuallyInitiated=True):
        self.sendSet({
            "ready": {
                "isReady": isReady,
                "manuallyInitiated": manuallyInitiated
            }
        })

    def setPlaylist(self, files):
        self.sendSet({
            "playlistChange": {
                "files": files
            }
        })

    def setPlaylistIndex(self, index):
        self.sendSet({
            "playlistIndex": {
                "index": index
            }
        })


    def handleError(self, error):
        self.dropWithError(error["message"])

    def sendError(self, message):
        self.sendMessage({"Error": {"message": message}})

class SyncServerProtocol(JSONCommandProtocol):
    def __init__(self, factory):
        self._factory = factory
        self._version = None
        self._features = None
        self._logged = False
        self.clientIgnoringOnTheFly = 0
        self.serverIgnoringOnTheFly = 0
        self._pingService = PingService()
        self._clientLatencyCalculation = 0
        self._clientLatencyCalculationArrivalTime = 0
        self._watcher = None

    def __hash__(self):
        return hash('|'.join((
            self.transport.getPeer().host,
            str(id(self)),
        )))

    def requireLogged(f):  # @NoSelf
        @wraps(f)
        def wrapper(self, *args, **kwds):
            if not self._logged:
                self.dropWithError(getMessage("not-known-server-error"))
            return f(self, *args, **kwds)
        return wrapper

    def showDebugMessage(self, line):
        pass

    def dropWithError(self, error):
        print(getMessage("client-drop-server-error").format(self.transport.getPeer().host, error))
        self.sendError(error)
        self.drop()

    def connectionLost(self, reason):
        self._factory.removeWatcher(self._watcher)

    def getFeatures(self):
        if not self._features:
            self._features = {}
            self._features["sharedPlaylists"] = meetsMinVersion(self._version, SHARED_PLAYLIST_MIN_VERSION)
            self._features["chat"] = meetsMinVersion(self._version, CHAT_MIN_VERSION)
            self._features["featureList"] = False
            self._features["readiness"] = meetsMinVersion(self._version, USER_READY_MIN_VERSION)
            self._features["managedRooms"] = meetsMinVersion(self._version, CONTROLLED_ROOMS_MIN_VERSION)
        return self._features

    def isLogged(self):
        return self._logged

    def meetsMinVersion(self, version):
        return self._version >= version

    def getVersion(self):
        return self._version

    def _extractHelloArguments(self, hello):
        roomName = None
        if "username" in hello:
            username = hello["username"]
            username = username.strip()
        else:
            username = None
        serverPassword = hello["password"] if "password" in hello else None
        room = hello["room"] if "room" in hello else None
        if room:
            if "name" in room:
                roomName = room["name"]
                roomName = roomName.strip()
            else:
                roomName = None
        version = hello["version"] if "version" in hello else None
        version = hello["realversion"] if "realversion" in hello else version
        features = hello["features"] if "features" in hello else None
        return username, serverPassword, roomName, version, features

    def _checkPassword(self, serverPassword):
        if self._factory.password:
            if not serverPassword:
                self.dropWithError(getMessage("password-required-server-error"))
                return False
            if serverPassword != self._factory.password:
                self.dropWithError(getMessage("wrong-password-server-error"))
                return False
        return True

    def handleHello(self, hello):
        username, serverPassword, roomName, version, features = self._extractHelloArguments(hello)
        if not username or not roomName or not version:
            self.dropWithError(getMessage("hello-server-error"))
            return
        else:
            if not self._checkPassword(serverPassword):
                return
            self._version = version
            self.setFeatures(features)
            self._factory.addWatcher(self, username, roomName)
            self._logged = True
            self.sendHello(version)

    @requireLogged
    def handleChat(self,chatMessage):
        if not self._factory.disableChat:
            self._factory.sendChat(self._watcher,chatMessage)

    def setFeatures(self, features):
        self._features = features

    def sendFeaturesUpdate(self):
        self.sendSet({"features": self.getFeatures()})

    def setWatcher(self, watcher):
        self._watcher = watcher

    def sendHello(self, clientVersion):
        hello = {}
        username = self._watcher.getName()
        hello["username"] = username
        userIp = self.transport.getPeer().host
        room = self._watcher.getRoom()
        if room: hello["room"] = {"name": room.getName()}
        hello["version"] = clientVersion # Used so 1.2.X client works on newer server
        hello["realversion"] = syncplay.version
        hello["motd"] = self._factory.getMotd(userIp, username, room, clientVersion)
        hello["features"] = self._factory.getFeatures()
        self.sendMessage({"Hello": hello})

    @requireLogged
    def handleSet(self, settings):
        for set_ in settings.items():
            command = set_[0]
            if command == "room":
                roomName = set_[1]["name"] if "name" in set_[1] else None
                self._factory.setWatcherRoom(self._watcher, roomName)
            elif command == "file":
                self._watcher.setFile(set_[1])
            elif command == "controllerAuth":
                password = set_[1]["password"] if "password" in set_[1] else None
                room = set_[1]["room"] if "room" in set_[1] else None
                self._factory.authRoomController(self._watcher, password, room)
            elif command == "ready":
                manuallyInitiated = set_[1]['manuallyInitiated'] if "manuallyInitiated" in set_[1] else False
                self._factory.setReady(self._watcher, set_[1]['isReady'], manuallyInitiated=manuallyInitiated)
            elif command ==  "playlistChange":
                self._factory.setPlaylist(self._watcher, set_[1]['files'])
            elif command == "playlistIndex":
                self._factory.setPlaylistIndex(self._watcher, set_[1]['index'])
            elif command == "features":
                #TODO: Check
                self._watcher.setFeatures(set_[1])

    def sendSet(self, setting):
        self.sendMessage({"Set": setting})

    def sendNewControlledRoom(self, roomName, password):
        self.sendSet({
            "newControlledRoom": {
                "password": password,
                "roomName": roomName
            }
        })

    def sendControlledRoomAuthStatus(self, success, username, roomname):
        self.sendSet({
            "controllerAuth": {
                "user": username,
                "room": roomname,
                "success": success
            }
        })


    def sendSetReady(self, username, isReady, manuallyInitiated=True):
        self.sendSet({
            "ready": {
                "username": username,
                "isReady": isReady,
                "manuallyInitiated": manuallyInitiated
            }
        })

    def setPlaylist(self, username, files):
        self.sendSet({
            "playlistChange": {
                "user": username,
                "files": files
            }
        })

    def setPlaylistIndex(self, username, index):
        self.sendSet({
            "playlistIndex": {
                "user": username,
                "index": index
            }
        })

    def sendUserSetting(self, username, room, file_, event):
        room = {"name": room.getName()}
        user = {username: {}}
        user[username]["room"] = room
        if file_:
            user[username]["file"] = file_
        if event:
            user[username]["event"] = event
        self.sendSet({"user": user})

    def _addUserOnList(self, userlist, watcher):
        room = watcher.getRoom()
        if room:
            if room.getName() not in userlist:
                userlist[room.getName()] = {}
            userFile = {
                "position": 0,
                "file": watcher.getFile() if watcher.getFile() else {},
                "controller": watcher.isController(),
                "isReady": watcher.isReady(),
                "features": watcher.getFeatures()
            }
            userlist[room.getName()][watcher.getName()] = userFile

    def sendList(self):
        userlist = {}
        watchers = self._factory.getAllWatchersForUser(self._watcher)
        for watcher in watchers:
            self._addUserOnList(userlist, watcher)
        self.sendMessage({"List": userlist})

    @requireLogged
    def handleList(self, _):
        self.sendList()

    def sendState(self, position, paused, doSeek, setBy, forced=False):
        if self._clientLatencyCalculationArrivalTime:
            processingTime = time.time() - self._clientLatencyCalculationArrivalTime
        else:
            processingTime = 0
        playstate = {
                     "position": position if position else 0,
                     "paused": paused,
                     "doSeek": doSeek,
                     "setBy": setBy.getName() if setBy else None
        }
        ping = {
                "latencyCalculation": self._pingService.newTimestamp(),
                "serverRtt": self._pingService.getRtt()
                }
        if self._clientLatencyCalculation:
            ping["clientLatencyCalculation"] = self._clientLatencyCalculation + processingTime
            self._clientLatencyCalculation = 0
        state = {
                 "ping": ping,
                 "playstate": playstate,
                }
        if forced:
            self.serverIgnoringOnTheFly += 1
        if self.serverIgnoringOnTheFly or self.clientIgnoringOnTheFly:
            state["ignoringOnTheFly"] = {}
            if self.serverIgnoringOnTheFly:
                state["ignoringOnTheFly"]["server"] = self.serverIgnoringOnTheFly
            if self.clientIgnoringOnTheFly:
                state["ignoringOnTheFly"]["client"] = self.clientIgnoringOnTheFly
                self.clientIgnoringOnTheFly = 0
        if self.serverIgnoringOnTheFly == 0 or forced:
            self.sendMessage({"State": state})


    def _extractStatePlaystateArguments(self, state):
        position = state["playstate"]["position"] if "position" in state["playstate"] else 0
        paused = state["playstate"]["paused"] if "paused" in state["playstate"] else None
        doSeek = state["playstate"]["doSeek"] if "doSeek" in state["playstate"] else None
        return position, paused, doSeek

    @requireLogged
    def handleState(self, state):
        position, paused, doSeek, latencyCalculation = None, None, None, None
        if "ignoringOnTheFly" in state:
            ignore = state["ignoringOnTheFly"]
            if "server" in ignore:
                if self.serverIgnoringOnTheFly == ignore["server"]:
                    self.serverIgnoringOnTheFly = 0
            if "client" in ignore:
                self.clientIgnoringOnTheFly = ignore["client"]
        if "playstate" in state:
            position, paused, doSeek = self._extractStatePlaystateArguments(state)
        if "ping" in state:
            latencyCalculation = state["ping"]["latencyCalculation"] if "latencyCalculation" in state["ping"] else 0
            clientRtt = state["ping"]["clientRtt"] if "clientRtt" in state["ping"] else 0
            self._clientLatencyCalculation = state["ping"]["clientLatencyCalculation"] if "clientLatencyCalculation" in state["ping"] else 0
            self._clientLatencyCalculationArrivalTime = time.time()
            self._pingService.receiveMessage(latencyCalculation, clientRtt)
        if self.serverIgnoringOnTheFly == 0:
            self._watcher.updateState(position, paused, doSeek, self._pingService.getLastForwardDelay())

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
        if not timestamp:
            return
        self._rtt = time.time() - timestamp
        if self._rtt < 0 or senderRtt < 0:
            return
        if not self._avrRtt:
            self._avrRtt = self._rtt
        self._avrRtt = self._avrRtt * PING_MOVING_AVERAGE_WEIGHT + self._rtt * (1 - PING_MOVING_AVERAGE_WEIGHT)
        if senderRtt < self._rtt:
            self._fd = self._avrRtt / 2 + (self._rtt - senderRtt)
        else:
            self._fd = self._avrRtt / 2

    def getLastForwardDelay(self):
        return self._fd

    def getRtt(self):
        return self._rtt
