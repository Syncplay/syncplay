import hashlib
import os.path
import time
import re
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor, task
from functools import wraps
from syncplay.protocols import SyncClientProtocol
from syncplay import utils, constants
from syncplay.messages import getMissingStrings, getMessage
from syncplay.constants import PRIVACY_SENDHASHED_MODE, PRIVACY_DONTSEND_MODE, \
    PRIVACY_HIDDENFILENAME
import collections
class SyncClientFactory(ClientFactory):
    def __init__(self, client, retry=constants.RECONNECT_RETRIES):
        self._client = client
        self.retry = retry
        self._timesTried = 0
        self.reconnecting = False

    def buildProtocol(self, addr):
        self._timesTried = 0
        return SyncClientProtocol(self._client)

    def startedConnecting(self, connector):
        destination = connector.getDestination()
        message = getMessage("connection-attempt-notification").format(destination.host, destination.port)
        self._client.ui.showMessage(message)

    def clientConnectionLost(self, connector, reason):
        if self._timesTried == 0:
            self._client.onDisconnect()
        if self._timesTried < self.retry:
            self._timesTried += 1
            self._client.ui.showMessage(getMessage("reconnection-attempt-notification"))
            self.reconnecting = True
            reactor.callLater(0.1 * (2 ** self._timesTried), connector.connect)
        else:
            message = getMessage("disconnection-notification")
            self._client.ui.showErrorMessage(message)

    def clientConnectionFailed(self, connector, reason):
        if not self.reconnecting:
            reactor.callLater(0.1, self._client.ui.showErrorMessage, getMessage("connection-failed-notification"), True)
            reactor.callLater(0.1, self._client.stop, True)
        else:
            self.clientConnectionLost(connector, reason)

    def resetRetrying(self):
        self._timesTried = 0

    def stopRetrying(self):
        self._timesTried = self.retry

class SyncplayClient(object):
    def __init__(self, playerClass, ui, config):
        constants.SHOW_OSD = config['showOSD']
        constants.SHOW_OSD_WARNINGS = config['showOSDWarnings']
        constants.SHOW_SLOWDOWN_OSD = config['showSlowdownOSD']
        constants.SHOW_DIFFERENT_ROOM_OSD = config['showDifferentRoomOSD']
        constants.SHOW_SAME_ROOM_OSD = config['showSameRoomOSD']
        constants.SHOW_DURATION_NOTIFICATION = config['showDurationNotification']
        constants.DEBUG_MODE = config['debug']

        self.controlpasswords = {}
        self.lastControlPasswordAttempt = None
        self.serverVersion = "0.0.0"

        self.lastLeftTime = 0
        self.lastPausedOnLeaveTime = None
        self.lastLeftUser = u""
        self.protocolFactory = SyncClientFactory(self)
        self.ui = UiManager(self, ui)
        self.userlist = SyncplayUserlist(self.ui, self)
        self._protocol = None
        """:type : SyncClientProtocol|None"""
        self._player = None
        if config['room'] is None or config['room'] == '':
            config['room'] = config['name']  # ticket #58
        self.defaultRoom = config['room']
        self.playerPositionBeforeLastSeek = 0.0
        self.setUsername(config['name'])
        self.setRoom(config['room'])
        if config['password']:
            config['password'] = hashlib.md5(config['password']).hexdigest()
        self._serverPassword = config['password']
        if not config['file']:
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
        self.behindFirstDetected = None
        self.autoPlay = False
        self.autoPlayThreshold = None

        self.autoplayTimer = task.LoopingCall(self.autoplayCountdown)
        self.autoplayTimeLeft = constants.AUTOPLAY_DELAY

        self._warnings = self._WarningManager(self._player, self.userlist, self.ui, self)
        if constants.LIST_RELATIVE_CONFIGS and self._config.has_key('loadedRelativePaths') and self._config['loadedRelativePaths']:
            paths = "; ".join(self._config['loadedRelativePaths'])
            self.ui.showMessage(getMessage("relative-config-notification").format(paths), noPlayer=True, noTimestamp=True)

        if constants.DEBUG_MODE and constants.WARN_ABOUT_MISSING_STRINGS:
            missingStrings = getMissingStrings()
            if missingStrings is not None and missingStrings is not "":
                self.ui.showDebugMessage("MISSING/UNUSED STRINGS DETECTED:\n{}".format(missingStrings))

    def initProtocol(self, protocol):
        self._protocol = protocol

    def destroyProtocol(self):
        if self._protocol:
            self._protocol.drop()
        self._protocol = None

    def initPlayer(self, player):
        self._player = player
        if not self._player.secondaryOSDSupported:
            constants.OSD_WARNING_MESSAGE_DURATION = constants.NO_SECONDARY_OSD_WARNING_DURATION
        self.scheduleAskPlayer()

    def scheduleAskPlayer(self, when=constants.PLAYER_ASK_DELAY):
        self._askPlayerTimer = task.LoopingCall(self.askPlayer)
        self._askPlayerTimer.start(when)

    def askPlayer(self):
        if not self._running:
            return
        if self._player:
            self._player.askForStatus()
        self.checkIfConnected()

    def checkIfConnected(self):
        if self._lastGlobalUpdate and self._protocol and time.time() - self._lastGlobalUpdate > constants.PROTOCOL_TIMEOUT:
            self._lastGlobalUpdate = None
            self.ui.showErrorMessage(getMessage("server-timeout-error"))
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
        if pauseChange and utils.meetsMinVersion(self.serverVersion, constants.USER_READY_MIN_VERSION):
            if not paused and not self.instaplayConditionsMet():
                paused = True
                self._player.setPaused(paused)
                self._playerPaused = paused
                self.changeReadyState(True, manuallyInitiated=True)
                pauseChange = False
                self.ui.showMessage(getMessage("ready-to-unpause-notification"))
            else:
                lastPausedDiff = time.time() - self.lastPausedOnLeaveTime if self.lastPausedOnLeaveTime else None
                if lastPausedDiff is not None and lastPausedDiff < constants.LAST_PAUSED_DIFF_THRESHOLD:
                    self.lastPausedOnLeaveTime = None
                else:
                    self.changeReadyState(not self.getPlayerPaused(), manuallyInitiated=False)
        if self._lastGlobalUpdate:
            self._lastPlayerUpdate = time.time()
            if (pauseChange or seeked) and self._protocol:
                if seeked:
                    self.playerPositionBeforeLastSeek = self.getGlobalPosition()
                self._protocol.sendState(self.getPlayerPosition(), self.getPlayerPaused(), seeked, None, True)

    def getLocalState(self):
        paused = self.getPlayerPaused()
        if self._config['dontSlowDownWithMe']:
            position = self.getGlobalPosition()
        else:
            position = self.getPlayerPosition()
        pauseChange, _ = self._determinePlayerStateChange(paused, position)
        if self._lastGlobalUpdate:
            return position, paused, _, pauseChange
        else:
            return None, None, None, None

    def _initPlayerState(self, position, paused):
        if self.userlist.currentUser.file:
            self.setPosition(position)
            self._player.setPaused(paused)
            madeChangeOnPlayer = True
            return madeChangeOnPlayer

    def _rewindPlayerDueToTimeDifference(self, position, setBy):
        hideFromOSD = not constants.SHOW_SAME_ROOM_OSD
        self.setPosition(position)
        self.ui.showMessage(getMessage("rewind-notification").format(setBy), hideFromOSD)
        madeChangeOnPlayer = True
        return madeChangeOnPlayer

    def _fastforwardPlayerDueToTimeDifference(self, position, setBy):
        hideFromOSD = not constants.SHOW_SAME_ROOM_OSD
        self.setPosition(position + constants.FASTFORWARD_EXTRA_TIME)
        self.ui.showMessage(getMessage("fastforward-notification").format(setBy), hideFromOSD)
        madeChangeOnPlayer = True
        return madeChangeOnPlayer

    def _serverUnpaused(self, setBy):
        hideFromOSD = not constants.SHOW_SAME_ROOM_OSD
        self._player.setPaused(False)
        madeChangeOnPlayer = True
        self.ui.showMessage(getMessage("unpause-notification").format(setBy), hideFromOSD)
        return madeChangeOnPlayer

    def _serverPaused(self, setBy):
        hideFromOSD = not constants.SHOW_SAME_ROOM_OSD
        if constants.SYNC_ON_PAUSE:
            self.setPosition(self.getGlobalPosition())
        self._player.setPaused(True)
        madeChangeOnPlayer = True
        if (self.lastLeftTime < time.time() - constants.OSD_DURATION) or (hideFromOSD == True):
            self.ui.showMessage(getMessage("pause-notification").format(setBy), hideFromOSD)
        else:
            self.ui.showMessage(getMessage("left-paused-notification").format(self.lastLeftUser, setBy), hideFromOSD)
        return madeChangeOnPlayer

    def _serverSeeked(self, position, setBy):
        hideFromOSD = not constants.SHOW_SAME_ROOM_OSD
        if self.getUsername() <> setBy:
            self.playerPositionBeforeLastSeek = self.getPlayerPosition()
            self.setPosition(position)
            madeChangeOnPlayer = True
        else:
            madeChangeOnPlayer = False
        message = getMessage("seek-notification").format(setBy, utils.formatTime(self.playerPositionBeforeLastSeek), utils.formatTime(position))
        self.ui.showMessage(message, hideFromOSD)
        return madeChangeOnPlayer

    def _slowDownToCoverTimeDifference(self, diff, setBy):
        hideFromOSD = not constants.SHOW_SLOWDOWN_OSD
        if self._config['slowdownThreshold']  < diff and not self._speedChanged:
            self._player.setSpeed(constants.SLOWDOWN_RATE)
            self._speedChanged = True
            self.ui.showMessage(getMessage("slowdown-notification").format(setBy), hideFromOSD)
        elif self._speedChanged and diff < constants.SLOWDOWN_RESET_THRESHOLD:
            self._player.setSpeed(1.00)
            self._speedChanged = False
            self.ui.showMessage(getMessage("revert-notification"), hideFromOSD)
        madeChangeOnPlayer = True
        return madeChangeOnPlayer

    def _changePlayerStateAccordingToGlobalState(self, position, paused, doSeek, setBy):
        madeChangeOnPlayer = False
        pauseChanged = paused != self.getGlobalPaused() or paused != self.getPlayerPaused()
        diff = self.getPlayerPosition() - position
        if self._lastGlobalUpdate is None:
            madeChangeOnPlayer = self._initPlayerState(position, paused)
        self._globalPaused = paused
        self._globalPosition = position
        self._lastGlobalUpdate = time.time()
        if doSeek:
            madeChangeOnPlayer = self._serverSeeked(position, setBy)
        if diff > self._config['rewindThreshold'] and not doSeek and not self._config['rewindOnDesync'] == False:
            madeChangeOnPlayer = self._rewindPlayerDueToTimeDifference(position, setBy)
        if self._config['fastforwardOnDesync'] and (self.userlist.currentUser.canControl() == False or self._config['dontSlowDownWithMe'] == True):
            if diff < (constants.FASTFORWARD_BEHIND_THRESHOLD * -1) and not doSeek:
                if self.behindFirstDetected is None:
                    self.behindFirstDetected = time.time()
                else:
                    durationBehind = time.time() - self.behindFirstDetected
                    if (durationBehind > (self._config['fastforwardThreshold']-constants.FASTFORWARD_BEHIND_THRESHOLD)) and (diff < (self._config['fastforwardThreshold'] * -1)):
                        madeChangeOnPlayer = self._fastforwardPlayerDueToTimeDifference(position, setBy)
                        self.behindFirstDetected = time.time() + constants.FASTFORWARD_RESET_THRESHOLD
            else:
                self.behindFirstDetected = None
        if self._player.speedSupported and not doSeek and not paused and not self._config['slowOnDesync'] == False:
            madeChangeOnPlayer = self._slowDownToCoverTimeDifference(diff, setBy)
        if paused == False and pauseChanged:
            madeChangeOnPlayer = self._serverUnpaused(setBy)
        elif paused == True and pauseChanged:
            madeChangeOnPlayer = self._serverPaused(setBy)
        return madeChangeOnPlayer

    def _executePlaystateHooks(self, position, paused, doSeek, setBy, messageAge):
        if self.userlist.hasRoomStateChanged() and not paused:
            self._warnings.checkWarnings()
            self.userlist.roomStateConfirmed()

    def updateGlobalState(self, position, paused, doSeek, setBy, messageAge):
        if self.__getUserlistOnLogon:
            self.__getUserlistOnLogon = False
            self.getUserList()
        madeChangeOnPlayer = False
        if not paused:
            position += messageAge
        if self._player:
            madeChangeOnPlayer = self._changePlayerStateAccordingToGlobalState(position, paused, doSeek, setBy)
        if madeChangeOnPlayer:
            self.askPlayer()
        self._executePlaystateHooks(position, paused, doSeek, setBy, messageAge)

    def getUserOffset(self):
        return self._userOffset

    def setUserOffset(self, time):
        self._userOffset = time
        self.setPosition(self.getGlobalPosition())
        self.ui.showMessage(getMessage("current-offset-notification").format(self._userOffset))

    def onDisconnect(self):
        if self._config['pauseOnLeave']:
            self.setPaused(True)
            self.lastPausedOnLeaveTime = time.time()

    def removeUser(self, username):
        if self.userlist.isUserInYourRoom(username):
            self.onDisconnect()
        self.userlist.removeUser(username)

    def getPlayerPosition(self):
        if not self._lastPlayerUpdate:
            if self._lastGlobalUpdate:
                return self.getGlobalPosition()
            else:
                return 0.0
        position = self._playerPosition
        if not self._playerPaused:
            diff = time.time() - self._lastPlayerUpdate
            position += diff
        return position

    def getPlayerPaused(self):
        if not self._lastPlayerUpdate:
            if self._lastGlobalUpdate:
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
        if not self._lastGlobalUpdate:
            return True
        return self._globalPaused

    def updateFile(self, filename, duration, path):
        if not path:
            return
        try:
            size = os.path.getsize(path)
        except:
            try:
                path = path.decode('utf-8')
                size = os.path.getsize(path)
            except:
                size = 0
        filename, size = self.__executePrivacySettings(filename, size)
        self.userlist.currentUser.setFile(filename, duration, size)
        self.sendFile()

    def __executePrivacySettings(self, filename, size):
        if self._config['filenamePrivacyMode'] == PRIVACY_SENDHASHED_MODE:
            filename = utils.hashFilename(filename)
        elif self._config['filenamePrivacyMode'] == PRIVACY_DONTSEND_MODE:
            filename = PRIVACY_HIDDENFILENAME
        if self._config['filesizePrivacyMode'] == PRIVACY_SENDHASHED_MODE:
            size = utils.hashFilesize(size)
        elif self._config['filesizePrivacyMode'] == PRIVACY_DONTSEND_MODE:
            size = 0
        return filename, size

    def setServerVersion(self, version):
        self.serverVersion = version

    def sendFile(self):
        file_ = self.userlist.currentUser.file
        if self._protocol and self._protocol.logged and file_:
            self._protocol.sendFileSetting(file_)

    def setUsername(self, username):
        if username and username <> "":
            self.userlist.currentUser.username = username
        else:
            import random
            random.seed()
            random_number = random.randrange(1000, 9999)
            self.userlist.currentUser.username = "Anonymous" + str(random_number) # Not localised as this would give away locale

    def getUsername(self):
        return self.userlist.currentUser.username

    def setRoom(self, roomName, resetAutoplay=False):
        self.userlist.currentUser.room = roomName
        if resetAutoplay:
            self.resetAutoPlayState()

    def sendRoom(self):
        room = self.userlist.currentUser.room
        if self._protocol and self._protocol.logged and room:
            self._protocol.sendRoomSetting(room)
            self.getUserList()
        self.reIdentifyAsController()

    def reIdentifyAsController(self):
        room = self.userlist.currentUser.room
        if utils.RoomPasswordProvider.isControlledRoom(room):
            storedRoomPassword = self.getControlledRoomPassword(room)
            if storedRoomPassword:
                self.identifyAsController(storedRoomPassword)

    def connected(self):
        readyState = self._config['readyAtStart'] if self.userlist.currentUser.isReady() is None else self.userlist.currentUser.isReady()
        self._protocol.setReady(readyState, manuallyInitiated=False)
        self.reIdentifyAsController()

    def getRoom(self):
        return self.userlist.currentUser.room

    def getConfig(self):
        return self._config

    def getUserList(self):
        if self._protocol and self._protocol.logged:
            self._protocol.sendList()

    def showUserList(self):
        self.userlist.showUserList()

    def getPassword(self):
        return self._serverPassword

    def setPosition(self, position):
        position += self.getUserOffset()
        if self._player and self.userlist.currentUser.file:
            if position < 0:
                position = 0
                self._protocol.sendState(self.getPlayerPosition(), self.getPlayerPaused(), True, None, True)
            self._player.setPosition(position)

    def setPaused(self, paused):
        if self._player and self.userlist.currentUser.file:
            self._player.setPaused(paused)

    def start(self, host, port):
        if self._running:
            return
        self._running = True
        if self._playerClass:
            reactor.callLater(0.1, self._playerClass.run, self, self._config['playerPath'], self._config['file'], self._config['playerArgs'])
            self._playerClass = None
        self.protocolFactory = SyncClientFactory(self)
        port = int(port)
        reactor.connectTCP(host, port, self.protocolFactory)
        reactor.run()

    def stop(self, promptForAction=False):
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
        if promptForAction:
            self.ui.promptFor(getMessage("enter-to-exit-prompt"))

    def requireMinServerVersion(minVersion):
        def requireMinVersionDecorator(f):
            @wraps(f)
            def wrapper(self, *args, **kwds):
                if not utils.meetsMinVersion(self.serverVersion,minVersion):
                    if self.serverVersion != "0.0.0":
                        self.ui.showErrorMessage(getMessage("not-supported-by-server-error").format(minVersion, self.serverVersion))
                    else:
                        self.ui.showDebugMessage("Tried to check server version too soon (threshold: {})".format(minVersion))
                    return
                return f(self, *args, **kwds)
            return wrapper
        return requireMinVersionDecorator

    def changeAutoplayState(self, newState):
        self.autoPlay = newState
        self.autoplayCheck()
    
    def changeAutoPlayThrehsold(self, newThreshold):
        oldAutoplayConditionsMet = self.autoplayConditionsMet()
        self.autoPlayThreshold = newThreshold
        newAutoplayConditionsMet = self.autoplayConditionsMet()
        if oldAutoplayConditionsMet == False and newAutoplayConditionsMet == True:
            self.autoplayCheck()

    def autoplayCheck(self):
        if self.autoplayConditionsMet():
            self.startAutoplayCountdown()
        else:
            self.stopAutoplayCountdown()

    def instaplayConditionsMet(self):
        if self.userlist.currentUser.isReady() or self._config["alwaysUnpause"]:
            return True

    def autoplayConditionsMet(self):
        return self._playerPaused and self.autoPlay and self.userlist.currentUser.canControl() and self.userlist.isReadinessSupported() and self.userlist.areAllUsersInRoomReady() and self.autoPlayThreshold and self.userlist.usersInRoomCount() >= self.autoPlayThreshold

    def autoplayTimerIsRunning(self):
        return self.autoplayTimer.running

    def startAutoplayCountdown(self):
        if self.autoplayConditionsMet() and not self.autoplayTimer.running:
            self.autoplayTimeLeft = constants.AUTOPLAY_DELAY
            self.autoplayTimer.start(1)

    def stopAutoplayCountdown(self):
        if self.autoplayTimer.running:
            self.autoplayTimer.stop()
        self.autoplayTimeLeft = constants.AUTOPLAY_DELAY

    def autoplayCountdown(self):
        if not self.autoplayConditionsMet():
            self.stopAutoplayCountdown()
            return
        countdownMessage = u"{}{}{}".format(getMessage("all-users-ready").format(self.userlist.readyUserCount()),self._player.osdMessageSeparator, getMessage("autoplaying-notification").format(int(self.autoplayTimeLeft)))
        self.ui.showOSDMessage(countdownMessage, 1, secondaryOSD=True)
        if self.autoplayTimeLeft <= 0:
            self.setPaused(False)
            self.stopAutoplayCountdown()
        else:
            self.autoplayTimeLeft -= 1

    def resetAutoPlayState(self):
        self.autoPlay = False
        self.ui.updateAutoPlayState(False)
        self.stopAutoplayCountdown()

    @requireMinServerVersion(constants.USER_READY_MIN_VERSION)
    def toggleReady(self, manuallyInitiated=True):
        self._protocol.setReady(not self.userlist.currentUser.isReady(), manuallyInitiated)

    @requireMinServerVersion(constants.USER_READY_MIN_VERSION)
    def changeReadyState(self, newState, manuallyInitiated=True):
        oldState = self.userlist.currentUser.isReady()
        if newState != oldState:
            self.toggleReady(manuallyInitiated)

    def setReady(self, username, isReady, manuallyInitiated=True):
        oldReadyState = self.userlist.isReady(username)
        if oldReadyState is None:
            oldReadyState = False
        self.userlist.setReady(username, isReady)
        self.ui.userListChange()
        if oldReadyState != isReady:
            self._warnings.checkReadyStates()

    @requireMinServerVersion(constants.CONTROLLED_ROOMS_MIN_VERSION)
    def createControlledRoom(self, roomName):
        controlPassword = utils.RandomStringGenerator.generate_room_password()
        self.lastControlPasswordAttempt = controlPassword
        self._protocol.requestControlledRoom(roomName, controlPassword)

    def controlledRoomCreated(self, roomName, controlPassword):
        self.ui.showMessage(getMessage("created-controlled-room-notification").format(roomName, controlPassword))
        self.setRoom(roomName, resetAutoplay=True)
        self.sendRoom()
        self._protocol.requestControlledRoom(roomName, controlPassword)
        self.ui.updateRoomName(roomName)

    def stripControlPassword(self, controlPassword):
        if controlPassword:
            return re.sub(constants.CONTROL_PASSWORD_STRIP_REGEX, "", controlPassword).upper()
        else:
            return ""

    @requireMinServerVersion(constants.CONTROLLED_ROOMS_MIN_VERSION)
    def identifyAsController(self, controlPassword):
        controlPassword = self.stripControlPassword(controlPassword)
        self.ui.showMessage(getMessage("identifying-as-controller-notification").format(controlPassword))
        self.lastControlPasswordAttempt = controlPassword
        self._protocol.requestControlledRoom(self.getRoom(), controlPassword)

    def controllerIdentificationError(self, username, room):
        if username == self.getUsername():
            self.ui.showErrorMessage(getMessage("failed-to-identify-as-controller-notification").format(username))

    def controllerIdentificationSuccess(self, username, roomname):
        self.userlist.setUserAsController(username)
        if self.userlist.isRoomSame(roomname):
            hideFromOSD = not constants.SHOW_SAME_ROOM_OSD
            self.ui.showMessage(getMessage("authenticated-as-controller-notification").format(username), hideFromOSD)
            if username == self.userlist.currentUser.username:
                self.storeControlPassword(roomname, self.lastControlPasswordAttempt)
        self.ui.userListChange()

    def storeControlPassword(self, room, password):
        if password:
            self.controlpasswords[room] = password

    def getControlledRoomPassword(self, room):
        if self.controlpasswords.has_key(room):
            return self.controlpasswords[room]

    def checkForUpdate(self, userInitiated):
        try:
            import urllib, syncplay, sys, messages, json
            params = urllib.urlencode({'version': syncplay.version, 'milestone': syncplay.milestone, 'release_number': syncplay.release_number,
                                   'language': messages.messages["CURRENT"], 'platform': sys.platform, 'userInitiated': userInitiated})

            f = urllib.urlopen(constants.SYNCPLAY_UPDATE_URL.format(params))
            response = f.read()
            response = response.replace("<p>","").replace("</p>","").replace("<br />","").replace("&#8220;","\"").replace("&#8221;","\"") # Fix Wordpress
            response = json.loads(response)
            return response["version-status"], response["version-message"] if response.has_key("version-message") else None, response["version-url"] if response.has_key("version-url") else None
        except:
            return "failed", getMessage("update-check-failed-notification").format(syncplay.version), constants.SYNCPLAY_DOWNLOAD_URL

    class _WarningManager(object):
        def __init__(self, player, userlist, ui, client):
            self._client = client
            self._player = player
            self._userlist = userlist
            self._ui = ui
            self._warnings = {
                "room-file-differences": {
                    "timer": task.LoopingCall(self.__displayMessageOnOSD, "room-file-differences",
                                              lambda: self._checkRoomForSameFiles(OSDOnly=True),),
                    "displayedFor": 0,
                },
                "alone-in-the-room": {
                    "timer": task.LoopingCall(self.__displayMessageOnOSD, "alone-in-the-room",
                                              lambda: self._checkIfYouReAloneInTheRoom(OSDOnly=True)),
                    "displayedFor": 0,
                },
                "not-all-ready": {
                    "timer": task.LoopingCall(self.__displayMessageOnOSD, "not-all-ready",
                                              lambda: self.checkReadyStates(),),
                    "displayedFor": 0,
                },
            }
            self.pausedTimer = task.LoopingCall(self.__displayPausedMessagesOnOSD)
            self.pausedTimer.start(constants.WARNING_OSD_MESSAGES_LOOP_INTERVAL, True)

        def checkWarnings(self):
            if self._client.autoplayConditionsMet():
                return
            self._checkIfYouReAloneInTheRoom(OSDOnly=False)
            self._checkRoomForSameFiles(OSDOnly=False)
            self.checkReadyStates()

        def _checkRoomForSameFiles(self, OSDOnly):
            if not self._userlist.areAllFilesInRoomSame():
                self._displayReadySameWarning()
                if not OSDOnly and constants.SHOW_OSD_WARNINGS and not self._warnings["room-file-differences"]['timer'].running:
                    self._warnings["room-file-differences"]['timer'].start(constants.WARNING_OSD_MESSAGES_LOOP_INTERVAL, True)
            elif self._warnings["room-file-differences"]['timer'].running:
                self._warnings["room-file-differences"]['timer'].stop()

        def _checkIfYouAreOnlyUserInRoomWhoSupportsReadiness(self):
            self._userlist._onlyUserInRoomWhoSupportsReadiness()
        
        def _checkIfYouReAloneInTheRoom(self, OSDOnly):
            if self._userlist.areYouAloneInRoom():
                self._ui.showOSDMessage(getMessage("alone-in-the-room"), constants.WARNING_OSD_MESSAGES_LOOP_INTERVAL, secondaryOSD=True)
                if not OSDOnly:
                    self._ui.showMessage(getMessage("alone-in-the-room"), True)
                    if constants.SHOW_OSD_WARNINGS and not self._warnings["alone-in-the-room"]['timer'].running:
                        self._warnings["alone-in-the-room"]['timer'].start(constants.WARNING_OSD_MESSAGES_LOOP_INTERVAL, True)
            elif self._warnings["alone-in-the-room"]['timer'].running:
                self._warnings["alone-in-the-room"]['timer'].stop()

        def checkReadyStates(self):
            if not self._client:
                return
            if self._client.getPlayerPaused() or not self._userlist.currentUser.isReady():
                self._warnings["not-all-ready"]["displayedFor"] = 0
            if self._userlist.areYouAloneInRoom() or not self._userlist.currentUser.canControl():
                if self._warnings["not-all-ready"]['timer'].running:
                    self._warnings["not-all-ready"]['timer'].stop()
            elif not self._userlist.areAllUsersInRoomReady():
                self._displayReadySameWarning()
                if constants.SHOW_OSD_WARNINGS and not self._warnings["not-all-ready"]['timer'].running:
                    self._warnings["not-all-ready"]['timer'].start(constants.WARNING_OSD_MESSAGES_LOOP_INTERVAL, True)
            elif self._warnings["not-all-ready"]['timer'].running:
                self._warnings["not-all-ready"]['timer'].stop()
                self._displayReadySameWarning()
            elif self._client.getPlayerPaused() or not self._userlist.currentUser.isReady():
                self._displayReadySameWarning()

        def _displayReadySameWarning(self):
            if not self._client._player or self._client.autoplayTimerIsRunning():
                return
            osdMessage = None
            fileDifferencesForRoom = self._userlist.getFileDifferencesForRoom()
            if not self._userlist.areAllFilesInRoomSame() and fileDifferencesForRoom is not None:
                fileDifferencesMessage = getMessage("room-file-differences").format(fileDifferencesForRoom)
                if self._userlist.currentUser.canControl() and self._userlist.isReadinessSupported():
                    if self._userlist.areAllUsersInRoomReady():
                        osdMessage = u"{}{}{}".format(fileDifferencesMessage, self._client._player.osdMessageSeparator, getMessage("all-users-ready").format(self._userlist.readyUserCount()))
                    else:
                        osdMessage = u"{}{}{}".format(fileDifferencesMessage, self._client._player.osdMessageSeparator, getMessage("not-all-ready").format(self._userlist.usersInRoomNotReady()))
                else:
                    osdMessage = fileDifferencesMessage
            elif self._userlist.isReadinessSupported():
                if self._userlist.areAllUsersInRoomReady():
                    osdMessage = getMessage("all-users-ready").format(self._userlist.readyUserCount())
                else:
                    osdMessage = getMessage("not-all-ready").format(self._userlist.usersInRoomNotReady())
            if osdMessage:
                self._ui.showOSDMessage(osdMessage, constants.WARNING_OSD_MESSAGES_LOOP_INTERVAL, secondaryOSD=True)

        def __displayMessageOnOSD(self, warningName, warningFunction):
            if constants.OSD_WARNING_MESSAGE_DURATION > self._warnings[warningName]["displayedFor"]:
                warningFunction()
                self._warnings[warningName]["displayedFor"] += constants.WARNING_OSD_MESSAGES_LOOP_INTERVAL
            else:
                self._warnings[warningName]["displayedFor"] = 0
                try:
                    self._warnings[warningName]["timer"].stop()
                except:
                    pass

        def __displayPausedMessagesOnOSD(self):
            if self._client.autoplayConditionsMet():
                return
            if self._client and self._client._player and self._client.getPlayerPaused():
                self._checkRoomForSameFiles(OSDOnly=True)
                self.checkReadyStates()
            elif not self._userlist.currentUser.isReady(): # CurrentUser should always be reminded they are set to not ready
                self.checkReadyStates()

class SyncplayUser(object):
    def __init__(self, username=None, room=None, file_=None):
        self.ready = None
        self.username = username
        self.room = room
        self.file = file_
        self._controller = False

    def setFile(self, filename, duration, size):
        file_ = {
            "name": filename,
            "duration": duration,
            "size": size
        }
        self.file = file_

    def isFileSame(self, file_):
        if not self.file:
            return False
        sameName = utils.sameFilename(self.file['name'], file_['name'])
        sameSize = utils.sameFilesize(self.file['size'], file_['size'])
        sameDuration = utils.sameFileduration(self.file['duration'], file_['duration'])
        return sameName and sameSize and sameDuration

    def __lt__(self, other):
        if self.isController() == other.isController():
            return self.username.lower() < other.username.lower()
        else:
            return self.isController() > other.isController()

    def __repr__(self, *args, **kwargs):
        if self.file:
            return "{}: {} ({}, {})".format(self.username, self.file['name'], self.file['duration'], self.file['size'])
        else:
            return "{}".format(self.username)

    def setControllerStatus(self, isController):
        self._controller = isController

    def isController(self):
        return self._controller

    def canControl(self):
        if self.isController() or not utils.RoomPasswordProvider.isControlledRoom(self.room):
            return True
        else:
            return False

    def isReadyWithFile(self):
        if self.file is None:
            return None
        return self.ready

    def isReady(self):
        return self.ready

    def setReady(self, ready):
        self.ready = ready

class SyncplayUserlist(object):
    def __init__(self, ui, client):
        self.currentUser = SyncplayUser()
        self._users = {}
        self.ui = ui
        self._client = client
        self._roomUsersChanged = True

    def isReadinessSupported(self):
        # TODO: Return False if server is run with --disable-ready
        if not utils.meetsMinVersion(self._client.serverVersion,constants.USER_READY_MIN_VERSION):
            return False
        elif self.onlyUserInRoomWhoSupportsReadiness():
            return False
        else:
            return True

    def isRoomSame(self, room):
        if room and self.currentUser.room and self.currentUser.room == room:
            return True
        else:
            return False

    def __showUserChangeMessage(self, username, room, file_, oldRoom=None):
        if room:
            if self.isRoomSame(room) or self.isRoomSame(oldRoom):
                showOnOSD = constants.SHOW_OSD_WARNINGS
            else:
                showOnOSD = constants.SHOW_DIFFERENT_ROOM_OSD
            if constants.SHOW_NONCONTROLLER_OSD == False and self.canControl(username) == False:
                showOnOSD = False
            hideFromOSD = not showOnOSD
            if not file_:
                message = getMessage("room-join-notification").format(username, room)
                self.ui.showMessage(message, hideFromOSD)
            else:
                duration = utils.formatTime(file_['duration'])
                message = getMessage("playing-notification").format(username, file_['name'], duration)
                if self.currentUser.room <> room or self.currentUser.username == username:
                    message += getMessage("playing-notification/room-addendum").format(room)
                self.ui.showMessage(message, hideFromOSD)
                if self.currentUser.file and not self.currentUser.isFileSame(file_) and self.currentUser.room == room:
                    fileDifferences = self.getFileDifferencesForUser(self.currentUser.file, file_)
                    if fileDifferences is not None:
                        message = getMessage("file-differences-notification").format(fileDifferences)
                        self.ui.showMessage(message, True)
                    
    def getFileDifferencesForUser(self, currentUserFile, otherUserFile):
        if not currentUserFile or not otherUserFile:
            return None
        differences = []
        differentName     = not utils.sameFilename(currentUserFile['name'], otherUserFile['name'])
        differentSize     = not utils.sameFilesize(currentUserFile['size'], otherUserFile['size'])                  
        differentDuration = not utils.sameFileduration(currentUserFile['duration'], otherUserFile['duration'])
        if differentName:     differences.append(getMessage("file-difference-filename"))
        if differentSize:     differences.append(getMessage("file-difference-filesize"))
        if differentDuration: differences.append(getMessage("file-difference-duration"))
        return ", ".join(differences)

    def getFileDifferencesForRoom(self):
        if not self.currentUser.file:
            return None
        differences = []
        differentName = False
        differentSize = False
        differentDuration = False
        for otherUser in self._users.itervalues():
            if otherUser.room == self.currentUser.room and otherUser.file:
                if not utils.sameFilename(self.currentUser.file['name'], otherUser.file['name']):
                    differentName = True
                if not utils.sameFilesize(self.currentUser.file['size'], otherUser.file['size']):
                    differentSize = True
                if not utils.sameFileduration(self.currentUser.file['duration'], otherUser.file['duration']):
                    differentDuration = True
        if differentName:     differences.append(getMessage("file-difference-filename"))
        if differentSize:     differences.append(getMessage("file-difference-filesize"))
        if differentDuration: differences.append(getMessage("file-difference-duration"))
        return ", ".join(differences)

    def addUser(self, username, room, file_, noMessage=False, isController=None, isReady=None):
        if username == self.currentUser.username:
            if isController is not None:
                self.currentUser.setControllerStatus(isController)
            self.currentUser.setReady(isReady)
            return
        user = SyncplayUser(username, room, file_)
        if isController is not None:
            user.setControllerStatus(isController)
        self._users[username] = user
        user.setReady(isReady)

        if not noMessage:
            self.__showUserChangeMessage(username, room, file_)
        self.userListChange(room)

    def removeUser(self, username):
        hideFromOSD = not constants.SHOW_DIFFERENT_ROOM_OSD
        if self._users.has_key(username):
            user = self._users[username]
            if user.room:
                if self.isRoomSame(user.room):
                    hideFromOSD = not constants.SHOW_SAME_ROOM_OSD
        if self._users.has_key(username):
            self._users.pop(username)
            message = getMessage("left-notification").format(username)
            self.ui.showMessage(message, hideFromOSD)
            self._client.lastLeftTime = time.time()
            self._client.lastLeftUser = username
        self.userListChange()

    def __displayModUserMessage(self, username, room, file_, user, oldRoom):
        if file_ and not user.isFileSame(file_):
            self.__showUserChangeMessage(username, room, file_, oldRoom)
        elif room and room != user.room:
            self.__showUserChangeMessage(username, room, None, oldRoom)

    def modUser(self, username, room, file_):
        if self._users.has_key(username):
            user = self._users[username]
            oldRoom = user.room if user.room else None
            if user.room != room:
                user.setControllerStatus(isController=False)
            self.__displayModUserMessage(username, room, file_, user, oldRoom)
            user.room = room
            if file_:
                user.file = file_
        elif username == self.currentUser.username:
            self.__showUserChangeMessage(username, room, file_)
        else:
            self.addUser(username, room, file_)
        self.userListChange(room)

    def setUserAsController(self, username):
        if self.currentUser.username == username:
            self.currentUser.setControllerStatus(True)
        elif self._users.has_key(username):
            user = self._users[username]
            user.setControllerStatus(True)

    def areAllUsersInRoomReady(self):
        if not self.currentUser.canControl():
            return True
        if not self.currentUser.isReady():
            return False
        for user in self._users.itervalues():
            if user.room == self.currentUser.room and user.isReadyWithFile() == False:
                return False
        return True

    def areAllOtherUsersInRoomReady(self):
        for user in self._users.itervalues():
            if user.room == self.currentUser.room and user.isReadyWithFile() == False:
                return False
        return True

    def readyUserCount(self):
        readyCount = 0
        if self.currentUser.isReady():
            readyCount += 1
        for user in self._users.itervalues():
            if user.room == self.currentUser.room and user.isReadyWithFile():
                readyCount += 1
        return readyCount
    
    def usersInRoomCount(self):
        userCount = 1
        for user in self._users.itervalues():
            if user.room == self.currentUser.room and user.isReadyWithFile():
                userCount += 1
        return userCount

    def usersInRoomNotReady(self):
        notReady = []
        if not self.currentUser.isReady():
            notReady.append(self.currentUser.username)
        for user in self._users.itervalues():
            if user.room == self.currentUser.room and user.isReadyWithFile() == False:
                notReady.append(user.username)
        return ", ".join(notReady)

    def areAllFilesInRoomSame(self):
        if self.currentUser.file:
            for user in self._users.itervalues():
                if user.room == self.currentUser.room and user.file and not self.currentUser.isFileSame(user.file):
                    if user.canControl():
                        return False
        return True

    def areYouAloneInRoom(self):
        for user in self._users.itervalues():
            if user.room == self.currentUser.room:
                return False
        return True
    
    def onlyUserInRoomWhoSupportsReadiness(self):
        for user in self._users.itervalues():
            if user.room == self.currentUser.room and user.isReadyWithFile() is not None:
                return False
        return True

    def isUserInYourRoom(self, username):
        for user in self._users.itervalues():
            if user.username == username and user.room == self.currentUser.room:
                return True
        return False

    def canControl(self, username):
        if self.currentUser.username == username and self.currentUser.canControl():
            return True

        for user in self._users.itervalues():
            if user.username == username and user.canControl():
                return True
        return False

    def isReadyWithFile(self, username):
        if self.currentUser.username == username:
            return self.currentUser.isReadyWithFile()

        for user in self._users.itervalues():
            if user.username == username:
                return user.isReadyWithFile()
        return None

    def isReady(self, username):
        if self.currentUser.username == username:
            return self.currentUser.isReady()

        for user in self._users.itervalues():
            if user.username == username:
                return user.isReady()
        return None

    def setReady(self, username, isReady):
        if self.currentUser.username == username:
            self.currentUser.setReady(isReady)
        elif self._users.has_key(username):
            self._users[username].setReady(isReady)
        self._client.autoplayCheck()

    def userListChange(self, room = None):
        if room is not None and self.isRoomSame(room):
            self._roomUsersChanged = True
        self.ui.userListChange()

    def roomStateConfirmed(self):
        self._roomUsersChanged = False

    def hasRoomStateChanged(self):
        return self._roomUsersChanged

    def showUserList(self):
        rooms = {}
        for user in self._users.itervalues():
            if user.room not in rooms:
                rooms[user.room] = []
            rooms[user.room].append(user)
        if self.currentUser.room not in rooms:
                rooms[self.currentUser.room] = []
        rooms[self.currentUser.room].append(self.currentUser)
        rooms = self.sortList(rooms)
        self.ui.showUserList(self.currentUser, rooms)
        self._client.autoplayCheck()

    def clearList(self):
        self._users = {}

    def sortList(self, rooms):
        for room in rooms:
            rooms[room] = sorted(rooms[room])
        rooms = collections.OrderedDict(sorted(rooms.items(), key=lambda s: s[0].lower()))
        return rooms

class UiManager(object):
    def __init__(self, client, ui):
        self._client = client
        self.__ui = ui
        self.lastPrimaryOSDMessage = None
        self.lastPrimaryOSDEndTime = None
        self.lastSecondaryOSDMessage = None
        self.lastSecondaryOSDEndTime = None
        self.lastError = ""

    def showDebugMessage(self, message):
        if constants.DEBUG_MODE and message.rstrip():
            print "{}{}".format(time.strftime(constants.UI_TIME_FORMAT, time.localtime()),message.rstrip())

    def showMessage(self, message, noPlayer=False, noTimestamp=False, secondaryOSD=False):
        if not noPlayer: self.showOSDMessage(message, duration=constants.OSD_DURATION, secondaryOSD=secondaryOSD)
        self.__ui.showMessage(message, noTimestamp)

    def updateAutoPlayState(self, newState):
        self.__ui.updateAutoPlayState(newState)

    def showUserList(self, currentUser, rooms):
        self.__ui.showUserList(currentUser, rooms)

    def showOSDMessage(self, message, duration=constants.OSD_DURATION, secondaryOSD=False):
        autoplayConditionsMet = self._client.autoplayConditionsMet()
        if secondaryOSD and not constants.SHOW_OSD_WARNINGS and not self._client.autoplayTimerIsRunning():
            return
        if not self._client._player:
            return
        if constants.SHOW_OSD and self._client and self._client._player:
            if not self._client._player.secondaryOSDSupported:
                if secondaryOSD:
                    self.lastSecondaryOSDMessage = message
                    if autoplayConditionsMet:
                        self.lastSecondaryOSDEndTime = time.time() + 1.0
                    else:
                        self.lastSecondaryOSDEndTime = time.time() + constants.NO_SECONDARY_OSD_WARNING_DURATION
                    if self.lastPrimaryOSDEndTime and time.time() < self.lastPrimaryOSDEndTime:
                        message = u"{}{}{}".format(message, self._client._player.osdMessageSeparator, self.lastPrimaryOSDMessage)
                else:
                    self.lastPrimaryOSDMessage = message
                    self.lastPrimaryOSDEndTime = time.time() + constants.OSD_DURATION
                    if self.lastSecondaryOSDEndTime and time.time() < self.lastSecondaryOSDEndTime:
                        message = u"{}{}{}".format(self.lastSecondaryOSDMessage, self._client._player.osdMessageSeparator, message)
            self._client._player.displayMessage(message, int(duration * 1000), secondaryOSD)

    def setControllerStatus(self, username, isController):
        self.__ui.setControllerStatus(username, isController)

    def showErrorMessage(self, message, criticalerror=False):
        if message <> self.lastError: # Avoid double call bug
            self.lastError = message
            self.__ui.showErrorMessage(message, criticalerror)

    def promptFor(self, prompt):
        return self.__ui.promptFor(prompt)

    def userListChange(self):
        self.__ui.userListChange()

    def markEndOfUserlist(self):
        self.__ui.markEndOfUserlist()

    def updateRoomName(self, room=""):
        self.__ui.updateRoomName(room)

    def drop(self):
        self.__ui.drop()


