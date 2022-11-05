
import ast
import collections
import hashlib
import os
import os.path
import random
import re
import sys
import threading
import time
from copy import deepcopy
from functools import wraps
from urllib.parse import urlparse

from twisted.application.internet import ClientService
from twisted.internet.endpoints import HostnameEndpoint
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor, task, defer, threads

try:
    SSL_CERT_FILE = None
    import certifi
    import pem
    from twisted.internet.ssl import Certificate, optionsForClientTLS, trustRootFromCertificates
    certPath = certifi.where()
    if os.path.exists(certPath):
        SSL_CERT_FILE = certPath
    elif 'zip' in certPath:
        import tempfile
        import zipfile
        zipPath, memberPath = certPath.split('.zip/')
        zipPath += '.zip'
        archive = zipfile.ZipFile(zipPath, 'r')
        tmpDir = tempfile.gettempdir()
        extractedPath = archive.extract(memberPath, tmpDir)
        SSL_CERT_FILE = extractedPath
except:
    pass

from syncplay import utils, constants, version
from syncplay.constants import PRIVACY_SENDHASHED_MODE, PRIVACY_DONTSEND_MODE, \
    PRIVACY_HIDDENFILENAME
from syncplay.messages import getMissingStrings, getMessage, isNoOSDMessage
from syncplay.protocols import SyncClientProtocol
from syncplay.utils import isMacOS


class SyncClientFactory(ClientFactory):
    def __init__(self, client, retry=constants.RECONNECT_RETRIES):
        self._client = client
        self.retry = retry
        self._timesTried = 0

    def buildProtocol(self, addr):
        self._timesTried = 0
        return SyncClientProtocol(self._client)

    def stopRetrying(self):
        self._client._reconnectingService.stopService()
        self._client.ui.showErrorMessage(getMessage("disconnection-notification"))


class SyncplayClient(object):
    def __init__(self, playerClass, ui, config):
        self.delayedLoadPath = None
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

        self.serverFeatures = {}

        self.lastRewindTime = None
        self.lastUpdatedFileTime = None
        self.lastAdvanceTime = None
        self.lastConnectTime = None
        self.lastSetRoomTime = None
        self.hadFirstPlaylistIndex = False
        self.hadFirstStateUpdate = False
        self.lastLeftTime = 0
        self.lastPausedOnLeaveTime = None
        self.lastLeftUser = ""
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
            config['password'] = hashlib.md5(config['password'].encode('utf-8')).hexdigest()
        self._serverPassword = config['password']
        self._host = "{}:{}".format(config['host'], config['port'])
        self._publicServers = config["publicServers"]
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

        self.__playerReady = defer.Deferred()

        self._warnings = self._WarningManager(self._player, self.userlist, self.ui, self)
        self.fileSwitch = FileSwitchManager(self)
        self.playlist = SyncplayPlaylist(self)

        self._serverSupportsTLS = True

        if constants.LIST_RELATIVE_CONFIGS and 'loadedRelativePaths' in self._config and self._config['loadedRelativePaths']:
            paths = "; ".join(self._config['loadedRelativePaths'])
            self.ui.showMessage(getMessage("relative-config-notification").format(paths), noPlayer=True, noTimestamp=True)

        if constants.DEBUG_MODE and constants.WARN_ABOUT_MISSING_STRINGS:
            missingStrings = getMissingStrings()
            if missingStrings is not None and missingStrings != "":
                self.ui.showDebugMessage("MISSING/UNUSED STRINGS DETECTED:\n{}".format(missingStrings))

    def initProtocol(self, protocol):
        self._protocol = protocol

    def destroyProtocol(self):
        if self._protocol:
            self._protocol.drop()
        self._protocol = None

    def initPlayer(self, player):
        self._player = player
        if not self._player.alertOSDSupported:
            constants.OSD_WARNING_MESSAGE_DURATION = constants.NO_ALERT_OSD_WARNING_DURATION
        self.scheduleAskPlayer()
        self.__playerReady.callback(player)

    def addPlayerReadyCallback(self, lambdaToCall):
        self.__playerReady.addCallback(lambdaToCall)

    def playerIsNotReady(self):
        return self._player is None

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

    def rewindFile(self):
        self.setPosition(0)
        self.establishRewindDoubleCheck()

    def establishRewindDoubleCheck(self):
        if constants.DOUBLE_CHECK_REWIND:
            reactor.callLater(0.5, self.doubleCheckRewindFile,)
            reactor.callLater(1, self.doubleCheckRewindFile,)
            reactor.callLater(1.5, self.doubleCheckRewindFile,)
        return

    def doubleCheckRewindFile(self):
        if self.getStoredPlayerPosition() > 5:
            self.setPosition(0)
            self.ui.showDebugMessage("Rewinded after double-check")

    def isPlayingMusic(self):
        if self.userlist.currentUser.file:
            for musicFormat in constants.MUSIC_FORMATS:
                if self.userlist.currentUser.file['name'].lower().endswith(musicFormat):
                    return True

    def seamlessMusicOveride(self):
        return self.isPlayingMusic() and self._recentlyAdvanced()

    def updatePlayerStatus(self, paused, position):
        position -= self.getUserOffset()
        pauseChange, seeked = self._determinePlayerStateChange(paused, position)
        positionBeforeSeek = self._playerPosition
        self._playerPosition = position
        self._playerPaused = paused
        currentLength = self.userlist.currentUser.file["duration"] if self.userlist.currentUser.file else 0
        if (
            pauseChange and paused and currentLength > constants.PLAYLIST_LOAD_NEXT_FILE_MINIMUM_LENGTH
            and abs(position - currentLength) < constants.PLAYLIST_LOAD_NEXT_FILE_TIME_FROM_END_THRESHOLD
        ):
            self.playlist.advancePlaylistCheck()
        elif pauseChange and "readiness" in self.serverFeatures and self.serverFeatures["readiness"]:
            if (
                currentLength == 0 or currentLength == -1 or
                not (
                    not self.playlist.notJustChangedPlaylist() and
                    abs(position - currentLength) < constants.PLAYLIST_LOAD_NEXT_FILE_TIME_FROM_END_THRESHOLD
                )
            ):
                pauseChange = self._toggleReady(pauseChange, paused)

        if self._lastGlobalUpdate:
            self._lastPlayerUpdate = time.time()
            if (pauseChange or seeked) and self._protocol:
                if seeked:
                    self.playerPositionBeforeLastSeek = self.getGlobalPosition()
                self._protocol.sendState(self.getPlayerPosition(), self.getPlayerPaused(), seeked, None, True)

    def prepareToAdvancePlaylist(self):
        if self.playlist.canSwitchToNextPlaylistIndex():
            self.ui.showDebugMessage("Preparing to advance playlist...")
            self.lastAdvanceTime = time.time()
            self._protocol.sendState(0, True, True, None, True)
        else:
            self.ui.showDebugMessage("Not preparing to advance playlist because the next file cannot be switched to")

    def _recentlyAdvanced(self):
        lastAdvandedDiff = time.time() - self.lastAdvanceTime if self.lastAdvanceTime else None
        if lastAdvandedDiff is not None and lastAdvandedDiff < constants.AUTOPLAY_DELAY + 5:
            return True

    def recentlyConnected(self):
        connectDiff = time.time() - self.lastConnectTime if self.lastConnectTime else None
        if connectDiff is None or connectDiff < constants.LAST_PAUSED_DIFF_THRESHOLD:
            return True

    def recentlyRewound(self, recentRewindThreshold = 5.0):
        lastRewindTime = self.lastRewindTime
        if lastRewindTime and self.lastUpdatedFileTime and self.lastUpdatedFileTime > lastRewindTime:
            lastRewindTime = self.lastRewindTime - 4.5
        return lastRewindTime is not None and abs(time.time() - lastRewindTime) < recentRewindThreshold

    def _toggleReady(self, pauseChange, paused):
        if not self.userlist.currentUser.canControl():
            self._player.setPaused(self._globalPaused)
            if not self.recentlyRewound() and not ((self._globalPaused == True) and not self._recentlyAdvanced()):
                self.toggleReady(manuallyInitiated=True)
            self._playerPaused = self._globalPaused
            pauseChange = False
            if self.userlist.currentUser.isReady():
                self.ui.showMessage(getMessage("set-as-not-ready-notification"))
            else:
                self.ui.showMessage(getMessage("set-as-ready-notification"))
        elif self.seamlessMusicOveride():
            self.ui.showDebugMessage("Readiness toggle ignored due to seamless music override")
            self._player.setPaused(paused)
            self._playerPaused = paused
        elif (self.recentlyRewound() and (self._globalPaused == True) and not self._recentlyAdvanced()):
            self._player.setPaused(self._globalPaused)
            self._playerPaused = self._globalPaused
            pauseChange = False
        elif not paused and not self.instaplayConditionsMet():
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
        return pauseChange

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
        madeChangeOnPlayer = False
        if self.getUsername() == setBy:
            self.ui.showDebugMessage("Caught attempt to rewind due to time difference with self")
        else:
            hideFromOSD = not constants.SHOW_SAME_ROOM_OSD
            self.setPosition(position)
            self.ui.showMessage(getMessage("rewind-notification").format(setBy), hideFromOSD)
            madeChangeOnPlayer = True
        return madeChangeOnPlayer

    def _fastforwardPlayerDueToTimeDifference(self, position, setBy):
        madeChangeOnPlayer = False
        if self.getUsername() == setBy:
            self.ui.showDebugMessage("Caught attempt to fastforward due to time difference with self")
        else:
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
        if constants.SYNC_ON_PAUSE and self.getUsername() != setBy:
            self.setPosition(self.getGlobalPosition())
        self._player.setPaused(True)
        madeChangeOnPlayer = True
        if (self.lastLeftTime < time.time() - constants.OSD_DURATION) or hideFromOSD == True:
            self.ui.showMessage(getMessage("pause-notification").format(setBy, utils.formatTime(self.getGlobalPosition())), hideFromOSD)
        else:
            self.ui.showMessage(getMessage("left-paused-notification").format(self.lastLeftUser, setBy), hideFromOSD)
        return madeChangeOnPlayer

    def _serverSeeked(self, position, setBy):
        hideFromOSD = not constants.SHOW_SAME_ROOM_OSD
        if self.getUsername() != setBy:
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
        madeChangeOnPlayer = False
        if self._config['slowdownThreshold'] < diff and not self._speedChanged:
            if self.getUsername() == setBy:
                self.ui.showDebugMessage("Caught attempt to slow down due to time difference with self")
            else:
                self._player.setSpeed(constants.SLOWDOWN_RATE)
                self._speedChanged = True
                self.ui.showMessage(getMessage("slowdown-notification").format(setBy), hideFromOSD)
                madeChangeOnPlayer = True
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
                    if (durationBehind > (self._config['fastforwardThreshold']-constants.FASTFORWARD_BEHIND_THRESHOLD))\
                            and (diff < (self._config['fastforwardThreshold'] * -1)):
                        madeChangeOnPlayer = self._fastforwardPlayerDueToTimeDifference(position, setBy)
                        self.behindFirstDetected = time.time() + constants.FASTFORWARD_RESET_THRESHOLD
            else:
                self.behindFirstDetected = None
        if self._player.speedSupported and not doSeek and not paused and  not self._config['slowOnDesync'] == False:
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

    def getStoredPlayerPosition(self):
        return self._playerPosition if self._playerPosition is not None else None

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

    def eofReportedByPlayer(self):
        if self.playlist.notJustChangedPlaylist() and self.userlist.currentUser.file:
            self.ui.showDebugMessage("Fixing file duration to allow for playlist advancement")
            self.userlist.currentUser.file["duration"] = self._playerPosition

    def updateFile(self, filename, duration, path):
        self.lastUpdatedFileTime = time.time()
        newPath = ""
        if utils.isURL(path):
            filename = path
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
        if not utils.isURL(path) and os.path.exists(path):
            self.fileSwitch.notifyUserIfFileNotInMediaDirectory(filename, path)
        filename, size = self.__executePrivacySettings(filename, size)
        self.userlist.currentUser.setFile(filename, duration, size, path)
        self.sendFile()
        self.playlist.changeToPlaylistIndexFromFilename(filename)

    def setTrustedDomains(self, newTrustedDomains):
        from syncplay.ui.ConfigurationGetter import ConfigurationGetter
        ConfigurationGetter().setConfigOption("trustedDomains", newTrustedDomains)
        oldTrustedDomains = self._config['trustedDomains']
        if oldTrustedDomains != newTrustedDomains:
            self._config['trustedDomains'] = newTrustedDomains
            self.fileSwitchFoundFiles()
            self.ui.showMessage("Trusted domains updated")
            # TODO: Properly add message for setting trusted domains!
            # TODO: Handle cases where users add www. to start of domain

    def setRoomList(self, newRoomList):
        newRoomList = sorted(newRoomList)
        from syncplay.ui.ConfigurationGetter import ConfigurationGetter
        ConfigurationGetter().setConfigOption("roomList", newRoomList)
        oldRoomList = self._config['roomList']
        if oldRoomList != newRoomList:
            self._config['roomList'] = newRoomList

    def _isURITrustableAndTrusted(self, URIToTest):
        """Returns a tuple of booleans: (trustable, trusted).
        
        A given URI is "trustable" if it uses HTTP or HTTPS (constants.TRUSTABLE_WEB_PROTOCOLS).
        A given URI is "trusted" if it matches an entry in the trustedDomains config.
        Such an entry is considered matching if the domain is the same and the path
        is a prefix of the given URI's path.
        A "trustable" URI is always "trusted" if the config onlySwitchToTrustedDomains is false.
        """
        o = urlparse(URIToTest)
        trustable = o.scheme in constants.TRUSTABLE_WEB_PROTOCOLS
        if not trustable:
            # untrustable URIs are never trusted, return early
            return False, False
        if not self._config['onlySwitchToTrustedDomains']:
            # trust all trustable URIs in this case
            return trustable, True
        # check for matching trusted domains
        if self._config['trustedDomains']:
            for entry in self._config['trustedDomains']:
                trustedDomain, _, path = entry.partition('/')
                if o.hostname not in (trustedDomain, "www." + trustedDomain):
                    # domain does not match
                    continue
                if path and not o.path.startswith('/' + path):
                    # trusted domain has a path component and it does not match
                    continue
                # match found, trust this domain
                return trustable, True
        # no matches found, do not trust this domain
        return trustable, False

    def isUntrustedTrustableURI(self, URIToTest):
        if utils.isURL(URIToTest):
            trustable, trusted = self._isURITrustableAndTrusted(URIToTest)
            return trustable and not trusted
        return False

    def isURITrusted(self, URIToTest):
        trustable, trusted = self._isURITrustableAndTrusted(URIToTest)
        return trustable and trusted

    def openFile(self, filePath, resetPosition=False, fromUser=False):
        if not (filePath.startswith("http://") or filePath.startswith("https://"))\
                and ((fromUser and filePath.endswith(".txt")) or filePath.endswith(".m3u") or filePath.endswith(".m3u8")):
            self.playlist.loadPlaylistFromFile(filePath, resetPosition)
            return

        self.playlist.openedFile()
        self._player.openFile(filePath, resetPosition)
        if resetPosition:
            self.rewindFile()
            self.establishRewindDoubleCheck()
            self.lastRewindTime = time.time()
            self.autoplayCheck()

    def fileSwitchFoundFiles(self):
        self.ui.fileSwitchFoundFiles()
        self.playlist.loadCurrentPlaylistIndex()

    def setPlaylistIndex(self, index):
        self._protocol.setPlaylistIndex(index)

    def changeToPlaylistIndex(self, *args, **kwargs):
        self.playlist.changeToPlaylistIndex(*args, **kwargs)

    def loopSingleFiles(self):
        return self._config["loopSingleFiles"] or self.isPlayingMusic()

    def isPlaylistLoopingEnabled(self):
        return self._config["loopAtEndOfPlaylist"] or self.isPlayingMusic()

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

    def setServerVersion(self, version, featureList):
        self.serverVersion = version
        self.checkForFeatureSupport(featureList)

    def checkForFeatureSupport(self, featureList):
        self.serverFeatures = {
            "featureList": utils.meetsMinVersion(self.serverVersion, constants.FEATURE_LIST_MIN_VERSION),
            "sharedPlaylists": utils.meetsMinVersion(self.serverVersion, constants.SHARED_PLAYLIST_MIN_VERSION),
            "chat": utils.meetsMinVersion(self.serverVersion, constants.CHAT_MIN_VERSION),
            "readiness": utils.meetsMinVersion(self.serverVersion, constants.USER_READY_MIN_VERSION),
            "managedRooms": utils.meetsMinVersion(self.serverVersion, constants.CONTROLLED_ROOMS_MIN_VERSION),
            "persistentRooms": False,
            "maxChatMessageLength": constants.FALLBACK_MAX_CHAT_MESSAGE_LENGTH,
            "maxUsernameLength": constants.FALLBACK_MAX_USERNAME_LENGTH,
            "maxRoomNameLength": constants.FALLBACK_MAX_ROOM_NAME_LENGTH,
            "maxFilenameLength": constants.FALLBACK_MAX_FILENAME_LENGTH
        }

        if featureList:
            self.serverFeatures.update(featureList)
        if not utils.meetsMinVersion(self.serverVersion, constants.SHARED_PLAYLIST_MIN_VERSION):
            self.ui.showErrorMessage(getMessage("shared-playlists-not-supported-by-server-error").format(constants.SHARED_PLAYLIST_MIN_VERSION, self.serverVersion))
        elif not self.serverFeatures["sharedPlaylists"]:
            self.ui.showErrorMessage(getMessage("shared-playlists-disabled-by-server-error"))
        # TODO: Have messages for all unsupported & disabled features
        if self.serverFeatures["maxChatMessageLength"] is not None:
            constants.MAX_CHAT_MESSAGE_LENGTH = self.serverFeatures["maxChatMessageLength"]
        if self.serverFeatures["maxUsernameLength"] is not None:
            constants.MAX_USERNAME_LENGTH = self.serverFeatures["maxUsernameLength"]
        if self.serverFeatures["maxRoomNameLength"] is not None:
            constants.MAX_ROOM_NAME_LENGTH = self.serverFeatures["maxRoomNameLength"]
        if self.serverFeatures["maxFilenameLength"] is not None:
            constants.MAX_FILENAME_LENGTH = self.serverFeatures["maxFilenameLength"]
        constants.MPV_SYNCPLAYINTF_CONSTANTS_TO_SEND = [
            "MaxChatMessageLength={}".format(constants.MAX_CHAT_MESSAGE_LENGTH),
            "inputPromptStartCharacter={}".format(constants.MPV_INPUT_PROMPT_START_CHARACTER),
            "inputPromptEndCharacter={}".format(constants.MPV_INPUT_PROMPT_END_CHARACTER),
            "backslashSubstituteCharacter={}".format(constants.MPV_INPUT_BACKSLASH_SUBSTITUTE_CHARACTER)]
        self.ui.setFeatures(self.serverFeatures)
        if self._player:
            self._player.setFeatures(self.serverFeatures)

    def getSanitizedCurrentUserFile(self):
        if self.userlist.currentUser.file:
            file_ = deepcopy(self.userlist.currentUser.file)
            if constants.PRIVATE_FILE_FIELDS:
                for PrivateField in constants.PRIVATE_FILE_FIELDS:
                    if PrivateField in file_:
                        file_.pop(PrivateField)
            return file_
        else:
            return None

    def sendFile(self):
        file_ = self.getSanitizedCurrentUserFile()
        if self._protocol and self._protocol.logged and file_:
            self._protocol.sendFileSetting(file_)

    def setUsername(self, username):
        if username and username != "":
            self.userlist.currentUser.username = username
        else:
            random_number = random.randrange(1000, 9999)
            self.userlist.currentUser.username = "Anonymous" + str(random_number)  # Not localised as this would give away locale

    def getUsername(self):
        return self.userlist.currentUser.username

    def chatIsEnabled(self):
        return True
        # TODO: Allow chat to be disabled

    def getFeatures(self):
        features = dict()

        # Can change during runtime:
        features["sharedPlaylists"] = self.sharedPlaylistIsEnabled()  # Can change during runtime
        features["chat"] = self.chatIsEnabled()  # Can change during runtime
        features["uiMode"] = self.ui.getUIMode()

        # Static for this version/release of Syncplay:
        features["featureList"] = True
        features["readiness"] = True
        features["managedRooms"] = True
        features["persistentRooms"] = True

        return features

    def setRoom(self, roomName, resetAutoplay=False):
        self.lastSetRoomTime = time.time()
        roomSplit = roomName.split(":")
        if roomName.startswith("+") and len(roomSplit) > 2:
            roomName = roomSplit[0] + ":" + roomSplit[1]
            password = roomSplit[2]
            self.storeControlPassword(roomName, password)
            self.ui.updateRoomName(roomName)
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
        self.setRoom(self.userlist.currentUser.room)
        room = self.userlist.currentUser.room
        if utils.RoomPasswordProvider.isControlledRoom(room):
            storedRoomPassword = self.getControlledRoomPassword(room)
            if storedRoomPassword:
                self.identifyAsController(storedRoomPassword)

    def isConnectedAndInARoom(self):
        return self._protocol and self._protocol.logged and self.userlist.currentUser.room

    def sharedPlaylistIsEnabled(self):
        if "sharedPlaylists" in self.serverFeatures and not self.serverFeatures["sharedPlaylists"]:
            sharedPlaylistEnabled = False
        else:
            sharedPlaylistEnabled = self._config['sharedPlaylistEnabled']
        return sharedPlaylistEnabled

    def connected(self):
        self.lastConnectTime = time.time()
        readyState = self._config['readyAtStart'] if self.userlist.currentUser.isReady() is None else self.userlist.currentUser.isReady()
        self._protocol.setReady(readyState, manuallyInitiated=False)
        self.reIdentifyAsController()
        if self._config["loadPlaylistFromFile"]:
            self.playlist.loadPlaylistFromFile(self._config["loadPlaylistFromFile"])
            self._config["loadPlaylistFromFile"] = None

    def getRoom(self):
        return self.userlist.currentUser.room

    def getConfig(self):
        return self._config

    def getUserList(self):
        if self._protocol and self._protocol.logged:
            self._protocol.sendList()

    def showUserList(self, altUI=None):
        self.userlist.showUserList(altUI)

    def getPassword(self):
        if self.thisIsPublicServer():
            return ""
        else:
            return self._serverPassword

    def thisIsPublicServer(self):
        self._publicServers = []
        if self._publicServers and self._host in self._publicServers:
            return True
        i = 0
        for server in constants.FALLBACK_PUBLIC_SYNCPLAY_SERVERS:
            if server[1] == self._host:
                return True
            i += 1

    def setPosition(self, position):
        if self._lastPlayerUpdate:
            self._lastPlayerUpdate = time.time()
        if self.lastRewindTime is not None and abs(time.time() - self.lastRewindTime) < 1.0 and position > 5:
            self.ui.showDebugMessage("Ignored seek to {} after rewind".format(position))
            return
        position += self.getUserOffset()
        if self._player and self.userlist.currentUser.file:
            if position < 0:
                position = 0
                self._protocol.sendState(self.getPlayerPosition(), self.getPlayerPaused(), True, None, True)
            self._player.setPosition(position)

    def setPaused(self, paused):
        if self._player and self.userlist.currentUser.file:
            if self._lastPlayerUpdate and not paused:
                self._lastPlayerUpdate = time.time()
            self._player.setPaused(paused)

    def start(self, host, port):
        if self._running:
            return
        self._running = True
        if self._playerClass:
            perPlayerArguments = utils.getPlayerArgumentsByPathAsArray(self._config['perPlayerArguments'], self._config['playerPath'])
            if perPlayerArguments:
                self._config['playerArgs'].extend(perPlayerArguments)
            filePath = self._config['file']
            if self._config['sharedPlaylistEnabled'] and filePath is not None:
                self.delayedLoadPath = filePath
                filePath = ""
            reactor.callLater(0.1, self._playerClass.run, self, self._config['playerPath'], filePath, self._config['playerArgs'], )
            self._playerClass = None
        self.protocolFactory = SyncClientFactory(self)
        if '[' in host:
            host = host.strip('[]')
        port = int(port)
        self._endpoint = HostnameEndpoint(reactor, host, port)
        try:
            certs = pem.parse_file(SSL_CERT_FILE)
            trustRoot = trustRootFromCertificates([Certificate.loadPEM(str(cert)) for cert in certs])
            self.protocolFactory.options = optionsForClientTLS(hostname=host, trustRoot=trustRoot)
            self._clientSupportsTLS = True
        except Exception as e:
            self.ui.showDebugMessage(str(e))
            self.protocolFactory.options = None
            self._clientSupportsTLS = False

        def retry(retries):
            self._lastGlobalUpdate = None
            self.ui.setSSLMode(False)
            if retries == 0:
                self.onDisconnect()
            if retries > constants.RECONNECT_RETRIES:
                reactor.callLater(0.1, self.ui.showErrorMessage, getMessage("connection-failed-notification"),
                                  True)
                reactor.callLater(0.1, self.stop, True)
                return None

            self.ui.showMessage(getMessage("reconnection-attempt-notification"))
            self.reconnecting = True
            return(0.1 * (2 ** min(retries, 5)))

        self._reconnectingService = ClientService(self._endpoint, self.protocolFactory, retryPolicy=retry)
        try:
            waitForConnection = self._reconnectingService.whenConnected(failAfterFailures=1)
        except TypeError:
            waitForConnection = self._reconnectingService.whenConnected()
        self._reconnectingService.startService()

        def connectedNow(f):
            hostIP = connectionHandle.result.transport.addr[0]
            self.ui.showMessage(getMessage("reachout-successful-notification").format(host, hostIP))
            return

        def failed(f):
            reactor.callLater(0.1, self.ui.showErrorMessage, getMessage("connection-failed-notification"), True)
            reactor.callLater(0.1, self.stop, True)

        connectionHandle = waitForConnection.addCallbacks(connectedNow, failed)
        message = getMessage("connection-attempt-notification").format(host, port)
        self.ui.showMessage(message)
        reactor.run()

    def stop(self, promptForAction=False):
        if not self._running:
            return
        self._running = False
        self.destroyProtocol()
        if self._player:
            self._player.drop()
        if self.ui:
            self.ui.drop()
        reactor.callLater(0.1, reactor.stop)
        if promptForAction:
            self.ui.promptFor(getMessage("enter-to-exit-prompt"))

    def requireServerFeature(featureRequired):
        def requireServerFeatureDecorator(f):
            @wraps(f)
            def wrapper(self, *args, **kwds):
                if self.serverVersion == "0.0.0":
                    self.ui.showDebugMessage(
                        "Tried to check server version too soon (testing support for: {})".format(featureRequired))
                    return None
                if featureRequired not in self.serverFeatures or not self.serverFeatures[featureRequired]:
                    featureName = getMessage("feature-{}".format(featureRequired))
                    self.ui.showErrorMessage(getMessage("not-supported-by-server-error").format(featureName))
                    return
                return f(self, *args, **kwds)
            return wrapper
        return requireServerFeatureDecorator

    @requireServerFeature("chat")
    def sendChat(self, message):
        if self._protocol and self._protocol.logged:
            try:
                message = message.replace("\n", "").replace("\r", "")
            except:
                pass
            message = utils.truncateText(message, constants.MAX_CHAT_MESSAGE_LENGTH)
            self._protocol.sendChatMessage(message)

    def sendFeaturesUpdate(self, features):
        self._protocol.sendFeaturesUpdate(features)

    def changePlaylistEnabledState(self, newState):
        oldState = self.sharedPlaylistIsEnabled()
        from syncplay.ui.ConfigurationGetter import ConfigurationGetter
        ConfigurationGetter().setConfigOption("sharedPlaylistEnabled", newState)
        self._config["sharedPlaylistEnabled"] = newState
        if oldState == False and newState == True:
            self.playlist.loadCurrentPlaylistIndex()

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
        if self.isPlayingMusic():
            return True
        if self.autoplayConditionsMet():
            self.startAutoplayCountdown()
        else:
            self.stopAutoplayCountdown()

    def instaplayConditionsMet(self):
        if self.isPlayingMusic():
            return True
        if not self.userlist.currentUser.canControl():
            return False

        unpauseAction = self._config['unpauseAction']
        if self.userlist.currentUser.isReady() or unpauseAction == constants.UNPAUSE_ALWAYS_MODE:
            return True
        elif unpauseAction == constants.UNPAUSE_IFOTHERSREADY_MODE and self.userlist.areAllOtherUsersInRoomReady():
            return True
        elif unpauseAction == constants.UNPAUSE_IFMINUSERSREADY_MODE and self.userlist.areAllOtherUsersInRoomReady()\
                and self.autoPlayThreshold and self.userlist.usersInRoomCount() >= self.autoPlayThreshold:
            return True
        else:
            return False

    def autoplayConditionsMet(self):
        if self.seamlessMusicOveride():
            self.setPaused(False)
        recentlyAdvanced = self._recentlyAdvanced()
        return (
            self._playerPaused and (self.autoPlay or recentlyAdvanced) and
            self.userlist.currentUser.canControl() and self.userlist.isReadinessSupported()
            and self.userlist.areAllUsersInRoomReady(requireSameFilenames=self._config["autoplayRequireSameFilenames"])
            and ((self.autoPlayThreshold and self.userlist.usersInRoomCount() >= self.autoPlayThreshold) or recentlyAdvanced)
        )

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
        allReadyMessage = getMessage("all-users-ready").format(self.userlist.readyUserCount())
        autoplayingMessage = getMessage("autoplaying-notification").format(int(self.autoplayTimeLeft))
        countdownMessage = "{}{}{}".format(allReadyMessage, self._player.osdMessageSeparator, autoplayingMessage)
        self.ui.showOSDMessage(countdownMessage, 1, OSDType=constants.OSD_ALERT, mood=constants.MESSAGE_GOODNEWS)
        if self.autoplayTimeLeft <= 0:
            self.setPaused(False)
            self.stopAutoplayCountdown()
        else:
            self.autoplayTimeLeft -= 1

    def resetAutoPlayState(self):
        self.autoPlay = False
        self.ui.updateAutoPlayState(False)
        self.stopAutoplayCountdown()

    @requireServerFeature("readiness")
    def toggleReady(self, manuallyInitiated=True):
        self._protocol.setReady(not self.userlist.currentUser.isReady(), manuallyInitiated)

    @requireServerFeature("readiness")
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

    @requireServerFeature("managedRooms")
    def setUserFeatures(self, username, features):
        self.userlist.setFeatures(username, features)
        self.ui.userListChange()

    @requireServerFeature("managedRooms")
    def createControlledRoom(self, roomName):
        controlPassword = utils.RandomStringGenerator.generate_room_password()
        self.lastControlPasswordAttempt = controlPassword
        self._protocol.requestControlledRoom(roomName, controlPassword)

    def controlledRoomCreated(self, roomName, controlPassword):
        self.ui.showMessage(getMessage("created-controlled-room-notification").format(roomName, controlPassword, roomName, roomName + ":" + controlPassword))
        self.setRoom(roomName, resetAutoplay=True)
        self.sendRoom()
        self._protocol.requestControlledRoom(roomName, controlPassword)
        self.ui.updateRoomName(roomName)

    def stripControlPassword(self, controlPassword):
        if controlPassword:
            return re.sub(constants.CONTROL_PASSWORD_STRIP_REGEX, "", controlPassword).upper()
        else:
            return ""

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
            try:
                if self._config['autosaveJoinsToList']:
                    self.ui.addRoomToList(room+":"+password)
            except:
                pass

    def getControlledRoomPassword(self, room):
        if room in self.controlpasswords:
            return self.controlpasswords[room]

    def checkForUpdate(self, userInitiated):
        try:
            import urllib.request, urllib.parse, urllib.error, syncplay, sys, json, platform
            try:
                architecture = platform.architecture()[0]
            except:
                architecture = "Unknown"
            try:
                machine = platform.machine()
            except:
                machine = "Unknown"
            params = urllib.parse.urlencode({'version': syncplay.version, 'milestone': syncplay.milestone, 'release_number': syncplay.release_number, 'language': syncplay.messages.messages["CURRENT"], 'platform': sys.platform, 'architecture': architecture, 'machine': machine, 'userInitiated': userInitiated})
            if isMacOS():
                import requests
                response = requests.get(constants.SYNCPLAY_UPDATE_URL.format(params))
                response = response.text
            else:
                f = urllib.request.urlopen(constants.SYNCPLAY_UPDATE_URL.format(params))
                response = f.read()
                response = response.decode('utf-8')
            response = response.replace("<p>", "").replace("</p>", "").replace("<br />", "").replace("&#8220;", "\"").replace("&#8221;", "\"")  # Fix Wordpress
            response = json.loads(response)
            publicServers = None
            if response["public-servers"]:
                publicServers = response["public-servers"].\
                    replace("&#8221;", "'").replace(":&#8217;", "'").replace("&#8217;", "'").replace("&#8242;", "'").replace("\n", "").replace("\r", "")
                publicServers = ast.literal_eval(publicServers)
            return response["version-status"], response["version-message"] if "version-message" in response\
                else None, response["version-url"] if "version-url" in response else None, publicServers
        except:
            return "failed", getMessage("update-check-failed-notification").format(syncplay.version), constants.SYNCPLAY_DOWNLOAD_URL, None

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
                self._ui.showOSDMessage(getMessage("alone-in-the-room"), constants.WARNING_OSD_MESSAGES_LOOP_INTERVAL, OSDType=constants.OSD_ALERT, mood=constants.MESSAGE_BADNEWS)
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
            messageMood = constants.MESSAGE_GOODNEWS
            fileDifferencesForRoom = self._userlist.getFileDifferencesForRoom()
            if not self._userlist.areAllFilesInRoomSame() and fileDifferencesForRoom is not None:
                messageMood = constants.MESSAGE_BADNEWS
                fileDifferencesMessage = getMessage("room-file-differences").format(fileDifferencesForRoom)
                if self._userlist.currentUser.canControl() and self._userlist.isReadinessSupported():
                    if self._userlist.areAllUsersInRoomReady():
                        allReadyMessage = getMessage("all-users-ready").format(self._userlist.readyUserCount())
                        osdMessage = "{}{}{}".format(fileDifferencesMessage, self._client._player.osdMessageSeparator, allReadyMessage)
                    else:
                        notAllReadyMessage = getMessage("not-all-ready").format(self._userlist.usersInRoomNotReady())
                        osdMessage = "{}{}{}".format(fileDifferencesMessage, self._client._player.osdMessageSeparator, notAllReadyMessage)
                else:
                    osdMessage = fileDifferencesMessage
            elif self._userlist.isReadinessSupported():
                if self._userlist.areAllUsersInRoomReady():
                    osdMessage = getMessage("all-users-ready").format(self._userlist.readyUserCount())
                else:
                    messageMood = constants.MESSAGE_BADNEWS
                    osdMessage = getMessage("not-all-ready").format(self._userlist.usersInRoomNotReady())
            if osdMessage:
                self._ui.showOSDMessage(osdMessage, constants.WARNING_OSD_MESSAGES_LOOP_INTERVAL, OSDType=constants.OSD_ALERT, mood=messageMood)

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
            elif not self._userlist.currentUser.isReady():  # CurrentUser should always be reminded they are set to not ready
                self.checkReadyStates()


class SyncplayUser(object):
    def __init__(self, username=None, room=None, file_=None):
        self.ready = None
        self.username = username
        self.room = room
        self.file = file_
        self._controller = False
        self._features = {}

    def setFile(self, filename, duration, size, path=None):
        file_ = {
            "name": filename,
            "duration": duration,
            "size": size,
            "path": path
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

    def setFeatures(self, features):
        self._features = features


class SyncplayUserlist(object):
    def __init__(self, ui, client):
        self.currentUser = SyncplayUser()
        self._users = {}
        self.ui = ui
        self._client = client
        self._roomUsersChanged = True

    def isReadinessSupported(self):
        if not utils.meetsMinVersion(self._client.serverVersion, constants.USER_READY_MIN_VERSION):
            return False
        elif self.onlyUserInRoomWhoSupportsReadiness():
            return False
        else:
            return self._client.serverFeatures["readiness"]

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
                if self.currentUser.room != room or self.currentUser.username == username:
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
        differentName = not utils.sameFilename(currentUserFile['name'], otherUserFile['name'])
        differentSize = not utils.sameFilesize(currentUserFile['size'], otherUserFile['size'])
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
        for otherUser in self._users.values():
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

    def addUser(self, username, room, file_, noMessage=False, isController=None, isReady=None, features={}):
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
        user.setFeatures(features)
        if not noMessage:
            self.__showUserChangeMessage(username, room, file_)
        self.userListChange(room)

    def removeUser(self, username):
        hideFromOSD = not constants.SHOW_DIFFERENT_ROOM_OSD
        if username in self._users:
            user = self._users[username]
            if user.room:
                if self.isRoomSame(user.room):
                    hideFromOSD = not constants.SHOW_SAME_ROOM_OSD
        if username in self._users:
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
        if username in self._users:
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
        elif username in self._users:
            user = self._users[username]
            user.setControllerStatus(True)

    def areAllUsersInRoomReady(self, requireSameFilenames=False):
        if not self.currentUser.canControl():
            return True
        if not self.currentUser.isReady():
            return False
        for user in self._users.values():
            if user.room == self.currentUser.room:
                if user.isReadyWithFile() == False:
                    return False
                elif (
                    requireSameFilenames and
                    (
                        self.currentUser.file is None
                        or user.file is None
                        or not utils.sameFilename(self.currentUser.file['name'], user.file['name'])
                    )
                ):
                    return False
        return True

    def areAllOtherUsersInRoomReady(self):
        for user in self._users.values():
            if user.room == self.currentUser.room and user.isReadyWithFile() == False:
                return False
        return True

    def readyUserCount(self):
        readyCount = 0
        if self.currentUser.isReady():
            readyCount += 1
        for user in self._users.values():
            if user.room == self.currentUser.room and user.isReadyWithFile():
                readyCount += 1
        return readyCount

    def usersInRoomCount(self):
        userCount = 1
        for user in self._users.values():
            if user.room == self.currentUser.room and user.isReadyWithFile():
                userCount += 1
        return userCount

    def usersInRoomNotReady(self):
        notReady = []
        if not self.currentUser.isReady():
            notReady.append(self.currentUser.username)
        for user in self._users.values():
            if user.room == self.currentUser.room and user.isReadyWithFile() == False:
                notReady.append(user.username)
        return ", ".join(notReady)

    def areAllFilesInRoomSame(self):
        if self.currentUser.file:
            for user in self._users.values():
                if user.room == self.currentUser.room and user.file and not self.currentUser.isFileSame(user.file):
                    if user.canControl():
                        return False
        return True

    def areYouAloneInRoom(self):
        if self._client.recentlyConnected():
            return False
        for user in self._users.values():
            if user.room == self.currentUser.room:
                return False
        return True

    def onlyUserInRoomWhoSupportsReadiness(self):
        for user in self._users.values():
            if user.room == self.currentUser.room and user.isReadyWithFile() is not None:
                return False
        return True

    def isUserInYourRoom(self, username):
        for user in self._users.values():
            if user.username == username and user.room == self.currentUser.room:
                return True
        return False

    def canControl(self, username):
        if self.currentUser.username == username and self.currentUser.canControl():
            return True

        for user in self._users.values():
            if user.username == username and user.canControl():
                return True
        return False

    def isReadyWithFile(self, username):
        if self.currentUser.username == username:
            return self.currentUser.isReadyWithFile()

        for user in self._users.values():
            if user.username == username:
                return user.isReadyWithFile()
        return None

    def isReady(self, username):
        if self.currentUser.username == username:
            return self.currentUser.isReady()

        for user in self._users.values():
            if user.username == username:
                return user.isReady()
        return None

    def setReady(self, username, isReady):
        if self.currentUser.username == username:
            self.currentUser.setReady(isReady)
        elif username in self._users:
            self._users[username].setReady(isReady)
        self._client.autoplayCheck()

    def userListChange(self, room=None):
        if room is not None and self.isRoomSame(room):
            self._roomUsersChanged = True
        self.ui.userListChange()

    def roomStateConfirmed(self):
        self._roomUsersChanged = False

    def hasRoomStateChanged(self):
        return self._roomUsersChanged

    def showUserList(self, altUI=None):
        rooms = {}
        for user in self._users.values():
            if user.room not in rooms:
                rooms[user.room] = []
            rooms[user.room].append(user)
        if self.currentUser.room not in rooms:
                rooms[self.currentUser.room] = []
        rooms[self.currentUser.room].append(self.currentUser)
        rooms = self.sortList(rooms)
        if altUI:
            altUI.showUserList(self.currentUser, rooms)
        else:
            self.ui.showUserList(self.currentUser, rooms)
        self._client.autoplayCheck()

    def clearList(self):
        self._users = {}

    def sortList(self, rooms):
        for room in rooms:
            rooms[room] = sorted(rooms[room])
        rooms = collections.OrderedDict(sorted(list(rooms.items()), key=lambda s: s[0].lower()))
        return rooms


class UiManager(object):
    def __init__(self, client, ui):
        self._client = client
        self.__ui = ui
        self.lastNotificatinOSDMessage = None
        self.lastNotificationOSDEndTime = None
        self.lastAlertOSDMessage = None
        self.lastAlertOSDEndTime = None
        self.lastError = ""

    def getUIMode(self):
        return self.__ui.uiMode

    def addFileToPlaylist(self, newPlaylistItem):
        self.__ui.addFileToPlaylist(newPlaylistItem)

    def setPlaylist(self, newPlaylist, newIndexFilename=None):
        self.__ui.setPlaylist(newPlaylist, newIndexFilename)

    def setPlaylistIndexFilename(self, filename):
        self.__ui.setPlaylistIndexFilename(filename)

    def fileSwitchFoundFiles(self):
        self.__ui.fileSwitchFoundFiles()

    def setFeatures(self, featureList):
        self.__ui.setFeatures(featureList)

    def showDebugMessage(self, message):
        if constants.DEBUG_MODE and message.rstrip():
            sys.stderr.write("{}{}\n".format(time.strftime(constants.UI_TIME_FORMAT, time.localtime()), message.rstrip()))

    def showChatMessage(self, username, userMessage):
        messageString = "<{}> {}".format(username, userMessage)
        if self._client._player.chatOSDSupported and self._client._config["chatOutputEnabled"]:
            self._client._player.displayChatMessage(username, userMessage)
        else:
            self.showOSDMessage(messageString, duration=constants.OSD_DURATION)
        self.__ui.showMessage(messageString)

    def setSSLMode(self, sslMode, sslInformation=""):
        self.__ui.setSSLMode(sslMode, sslInformation)

    def showMessage(self, message, noPlayer=False, noTimestamp=False, OSDType=constants.OSD_NOTIFICATION, mood=constants.MESSAGE_NEUTRAL):
        if not noPlayer:
            self.showOSDMessage(message, duration=constants.OSD_DURATION, OSDType=OSDType, mood=mood)
        self.__ui.showMessage(message, noTimestamp)

    def updateAutoPlayState(self, newState):
        self.__ui.updateAutoPlayState(newState)

    def showUserList(self, currentUser, rooms):
        self.__ui.showUserList(currentUser, rooms)

    def showOSDMessage(self, message, duration=constants.OSD_DURATION, OSDType=constants.OSD_NOTIFICATION, mood=constants.MESSAGE_NEUTRAL):
        if(isNoOSDMessage(message)):
            return

        autoplayConditionsMet = self._client.autoplayConditionsMet()
        if OSDType == constants.OSD_ALERT and not constants.SHOW_OSD_WARNINGS and not self._client.autoplayTimerIsRunning():
            return
        if not self._client._player:
            return
        if constants.SHOW_OSD and self._client and self._client._player:
            if not self._client._player.alertOSDSupported:
                if OSDType == constants.OSD_ALERT:
                    self.lastAlertOSDMessage = message
                    if autoplayConditionsMet:
                        self.lastAlertOSDEndTime = time.time() + 1.0
                    else:
                        self.lastAlertOSDEndTime = time.time() + constants.NO_ALERT_OSD_WARNING_DURATION
                    if self.lastNotificationOSDEndTime and time.time() < self.lastNotificationOSDEndTime:
                        message = "{}{}{}".format(message, self._client._player.osdMessageSeparator, self.lastNotificatinOSDMessage)
                else:
                    self.lastNotificatinOSDMessage = message
                    self.lastNotificationOSDEndTime = time.time() + constants.OSD_DURATION
                    if self.lastAlertOSDEndTime and time.time() < self.lastAlertOSDEndTime:
                        message = "{}{}{}".format(self.lastAlertOSDMessage, self._client._player.osdMessageSeparator, message)
            self._client._player.displayMessage(message, int(duration * 1000), OSDType, mood)

    def setControllerStatus(self, username, isController):
        self.__ui.setControllerStatus(username, isController)

    def showErrorMessage(self, message, criticalerror=False):
        if message != self.lastError:  # Avoid double call bug
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

    def addRoomToList(self, room):
        self.__ui.addRoomToList(room)

    def executeCommand(self, command):
        self.__ui.executeCommand(command)

    def drop(self):
        self.__ui.drop()


class SyncplayPlaylist():
    def __init__(self, client):
        self.queuedIndex = None
        self._client = client
        self._ui = self._client.ui
        self._previousPlaylist = None
        self._previousPlaylistRoom = None
        self._playlist = []
        self._playlistIndex = None
        self.addedChangeListCallback = False
        self.switchToNewPlaylistItem = False
        self._lastPlaylistIndexChange = time.time()

    def needsSharedPlaylistsEnabled(f):  # @NoSelf
        @wraps(f)
        def wrapper(self, *args, **kwds):
            if not self._client.sharedPlaylistIsEnabled():
                self._ui.showDebugMessage("Tried to use shared playlists when it was disabled!")
                return
            return f(self, *args, **kwds)
        return wrapper

    def openedFile(self):
        self._lastPlaylistIndexChange = time.time()

    def removeDirsFromPath(self, filePath):
        if os.path.isfile(filePath):
            return os.path.basename(filePath)
        elif utils.isURL(filePath):
            return filePath
        self._ui.showDebugMessage("Could not find path: {}".format(filePath))

    def getPlaylistIndexFromPath(self, filePath):
        filePath = self.removeDirsFromPath(filePath)
        try:
            return self._playlist.index(filePath)
        except ValueError:
            return

    def changeToPlaylistIndexFromFilename(self, filename):
        try:
            index = self._playlist.index(filename)
            if index != self._playlistIndex:
                self.changeToPlaylistIndex(index, resetPosition=True)
            else:
                if filename == self.queuedIndexFilename:
                    return
                self._client.rewindFile()
        except ValueError:
            pass

    def loadDelayedPath(self, changeToIndex):
        # Implementing the behaviour set out at https://github.com/Syncplay/syncplay/issues/315

        if self._client.playerIsNotReady():
            self._client.addPlayerReadyCallback(lambda x: self.loadDelayedPath(changeToIndex))
            return

        if self._client._protocol.hadFirstPlaylistIndex and self._client.delayedLoadPath:
            delayedLoadPath = str(self._client.delayedLoadPath)
            self._client.delayedLoadPath = None
            if self._client.sharedPlaylistIsEnabled():
                pathWithoutDirs = self.removeDirsFromPath(delayedLoadPath)
                if len(self._playlist) == 0:
                    self._client.openFile(delayedLoadPath, resetPosition=True, fromUser=True)
                    self._client.ui.addFileToPlaylist(delayedLoadPath)
                else:
                    try:
                        currentPlaylistFilename = self._playlist[changeToIndex]
                    except TypeError:
                        currentPlaylistFilename = None
                    if currentPlaylistFilename != pathWithoutDirs:
                        if pathWithoutDirs not in self._playlist:
                            if utils.isURL(delayedLoadPath) or utils.isURL(currentPlaylistFilename):
                                self._client.ui.addFileToPlaylist(delayedLoadPath)
                            else:
                                foundFilePath = self._client.fileSwitch.findFilepath(currentPlaylistFilename, highPriority=True)
                                if foundFilePath is None:
                                    self._client.openFile(delayedLoadPath, resetPosition=False)
                                else:
                                    self._client.ui.showMessage("{}: {}...".format(getMessage("addfilestoplaylist-menu-label"), pathWithoutDirs))
                                    reactor.callLater(constants.DELAYED_LOAD_WAIT_TIME, self._client.ui.addFileToPlaylist, delayedLoadPath, ) # TODO: Avoid arbitary pause
                        else:
                            self._client.ui.showErrorMessage(getMessage("cannot-add-duplicate-error").format(pathWithoutDirs))

            else:
                self._client.openFile(delayedLoadPath)

    def changeToPlaylistIndex(self, index, username=None, resetPosition=False):
        if self.loadDelayedPath(index):
            return
        if self._playlist is None or len(self._playlist) == 0:
            return
        if index is None:
            return
        if username is None and not self._client.sharedPlaylistIsEnabled():
            return
        self._lastPlaylistIndexChange = time.time()
        if self._client.playerIsNotReady():
            if not self.addedChangeListCallback:
                self.addedChangeListCallback = True
                self._client.addPlayerReadyCallback(lambda x: self.changeToPlaylistIndex(index, username))
            return
        try:
            filename = self._playlist[index]
            self._ui.setPlaylistIndexFilename(filename)
            if not self._client.sharedPlaylistIsEnabled():
                self._playlistIndex = index
            if username is not None and self._client.userlist.currentUser.file and filename == self._client.userlist.currentUser.file['name']:
                self._playlistIndex = index
                return
        except IndexError:
            pass

        self._playlistIndex = index
        if username is None:
            if self._client.isConnectedAndInARoom() and self._client.sharedPlaylistIsEnabled():
                if resetPosition:
                    self._client.rewindFile()
                self._client.setPlaylistIndex(index)
        elif index is not None:
            self._ui.showMessage(getMessage("playlist-selection-changed-notification").format(username))
            self.switchToNewPlaylistIndex(index, resetPosition=resetPosition)

    def canSwitchToNextPlaylistIndex(self):
        if self._thereIsNextPlaylistIndex() and self._client.sharedPlaylistIsEnabled():
            try:
                index = self._nextPlaylistIndex()
                if index is None:
                    return False
                filename = self._playlist[index]
                if utils.isURL(filename):
                    return True if self._client.isURITrusted(filename) else False
                else:
                    path = self._client.fileSwitch.findFilepath(filename, highPriority=True)
                return True if path else False
            except:
                return False
        return False

    @needsSharedPlaylistsEnabled
    def switchToNewPlaylistIndex(self, index, resetPosition = False):
        try:
            self.queuedIndexFilename = self._playlist[index]
        except:
            self.queuedIndexFilename = None
            self._ui.showDebugMessage("Failed to find index {} in plauylist".format(index))
        self._lastPlaylistIndexChange = time.time()
        if self._client.playerIsNotReady():
            self._client.addPlayerReadyCallback(lambda x: self.switchToNewPlaylistIndex(index, resetPosition))
            return

        try:
            if index is None:
                self._ui.showDebugMessage("Cannot switch to None index in playlist")
                return
            filename = self._playlist[index]
            # TODO: Handle isse with index being None
            if utils.isURL(filename):
                if self._client.isURITrusted(filename):
                    self._client.openFile(filename, resetPosition=resetPosition)
                else:
                    self._ui.showErrorMessage(getMessage("cannot-add-unsafe-path-error").format(filename))
                return
            else:
                path = self._client.fileSwitch.findFilepath(filename, highPriority=True)
            if path:
                self._client.openFile(path, resetPosition)
            else:
                self._ui.showErrorMessage(getMessage("cannot-find-file-for-playlist-switch-error").format(filename))
                return
        except IndexError:
            self._ui.showDebugMessage("Could not change playlist index due to IndexError")

    def _getValidIndexFromNewPlaylist(self, newPlaylist=None):
        if self.switchToNewPlaylistItem:
            self.switchToNewPlaylistItem = False
            return len(self._playlist)

        if self._playlistIndex is None or not newPlaylist or len(newPlaylist) <= 1:
            return 0

        i = self._playlistIndex
        while i <= len(self._playlist):
            try:
                filename = self._playlist[i]
                validIndex = newPlaylist.index(filename)
                return validIndex
            except:
                i += 1

        i = self._playlistIndex
        while i > 0:
            try:
                filename = self._playlist[i]
                validIndex = newPlaylist.index(filename)
                return validIndex+1 if validIndex < len(newPlaylist)-1 else validIndex
            except:
                i -= 1
        return 0

    def _getFilenameFromIndexInGivenPlaylist(self, _playlist, _index):
        if not _index or not _playlist:
            return None
        filename = _playlist[_index] if len(_playlist) > _index else None
        return filename

    def loadPlaylistFromFile(self, path, shuffle=False):
        if not os.path.isfile(path):
            self._ui.showDebugMessage("Not loading {} as file could not be found".format(path))
            return

        with open(path) as f:
            newPlaylist = f.read().splitlines()
            if shuffle:
                random.shuffle(newPlaylist)
            if newPlaylist:
                self.changePlaylist(newPlaylist, username=None, resetIndex=True)

    def savePlaylistToFile(self, path):
        with open(path, 'w') as playlistFile:
            playlistToSave = utils.getListAsMultilineString(self._playlist)
            playlistFile.write(playlistToSave)
            self._ui.showMessage("Playlist saved as {}".format(path)) # TODO: Move to messages_en


    def changePlaylist(self, files, username=None, resetIndex=False):
        self.queuedIndexFilename = None
        if self._playlist == files:
            if self._playlistIndex != 0 and resetIndex:
                self.changeToPlaylistIndex(0)
            return

        if resetIndex:
            newIndex = 0
            filename = files[0] if files and len(files) > 0 else None
        else:
            newIndex = self._getValidIndexFromNewPlaylist(files)
            filename = self._getFilenameFromIndexInGivenPlaylist(files, newIndex)

        self._updateUndoPlaylistBuffer(newPlaylist=files, newRoom=self._client.userlist.currentUser.room)
        self._playlist = files

        if username is None:
            if self._client.isConnectedAndInARoom() and self._client.sharedPlaylistIsEnabled():
                self._client._protocol.setPlaylist(files)
                self.changeToPlaylistIndex(newIndex)
                self._ui.setPlaylist(self._playlist, filename)
                self._ui.showMessage(getMessage("playlist-contents-changed-notification").format(self._client.getUsername()))
        else:
            self._ui.setPlaylist(self._playlist)
            self._ui.showMessage(getMessage("playlist-contents-changed-notification").format(username))

    def addToPlaylist(self, file):
        self.changePlaylist([*self._playlist, file])

    def deleteAtIndex(self, index):
        new_playlist = self._playlist.copy()
        if index >= 0 and index < len(new_playlist):
            del new_playlist[index]
            self.changePlaylist(new_playlist)
        else:
            raise TypeError("Invalid index")


    @needsSharedPlaylistsEnabled
    def undoPlaylistChange(self):
        if self.canUndoPlaylist(self._playlist):
            newPlaylist = self._getPreviousPlaylist()
            self.changePlaylist(newPlaylist, username=None)

    @needsSharedPlaylistsEnabled
    def shuffleRemainingPlaylist(self):
        if self._playlist and len(self._playlist) > 0:
            shuffledPlaylist = deepcopy(self._playlist)
            shufflePoint = self._playlistIndex + 1
            partToKeep = shuffledPlaylist[:shufflePoint]
            partToShuffle = shuffledPlaylist[shufflePoint:]
            random.shuffle(partToShuffle)
            shuffledPlaylist = partToKeep + partToShuffle
            self.changePlaylist(shuffledPlaylist, username=None, resetIndex=False)

    @needsSharedPlaylistsEnabled
    def shuffleEntirePlaylist(self):
        if self._playlist and len(self._playlist) > 0:
            shuffledPlaylist = deepcopy(self._playlist)
            random.shuffle(shuffledPlaylist)
            self.changePlaylist(shuffledPlaylist, username=None, resetIndex=True)
            self.switchToNewPlaylistIndex(0, resetPosition=True)

    def canUndoPlaylist(self, currentPlaylist):
        return self._previousPlaylist is not None and currentPlaylist != self._previousPlaylist

    def loadCurrentPlaylistIndex(self):
        if self._notPlayingCurrentIndex():
            self.switchToNewPlaylistIndex(self._playlistIndex)

    @needsSharedPlaylistsEnabled
    def advancePlaylistCheck(self):
        position = self._client.getStoredPlayerPosition()
        currentLength = self._client.userlist.currentUser.file["duration"] if self._client.userlist.currentUser.file else 0
        if (
            currentLength > constants.PLAYLIST_LOAD_NEXT_FILE_MINIMUM_LENGTH and
            abs(position - currentLength) < constants.PLAYLIST_LOAD_NEXT_FILE_TIME_FROM_END_THRESHOLD and
            self.notJustChangedPlaylist()
        ):
                self.loadNextFileInPlaylist()

    def notJustChangedPlaylist(self):
        secondsSinceLastChange = time.time() - self._lastPlaylistIndexChange
        return secondsSinceLastChange > constants.PLAYLIST_LOAD_NEXT_FILE_TIME_FROM_END_THRESHOLD

    @needsSharedPlaylistsEnabled
    def loadNextFileInPlaylist(self):
        if self._notPlayingCurrentIndex():
            return

        if len(self._playlist) == 1 and self._client.loopSingleFiles():
            self._lastPlaylistIndexChange = time.time()
            self._client.rewindFile()
            self._client.setPaused(False)
            reactor.callLater(0.5, self._client.setPaused, False,)

        elif self._thereIsNextPlaylistIndex():
            self._client.prepareToAdvancePlaylist()
            self.switchToNewPlaylistIndex(self._nextPlaylistIndex(), resetPosition=True)

    def _updateUndoPlaylistBuffer(self, newPlaylist, newRoom):
        if self._playlistBufferIsFromOldRoom(newRoom):
            self._movePlaylistBufferToNewRoom(newRoom)
        elif self._playlistBufferNeedsUpdating(newPlaylist):
            self._previousPlaylist = self._playlist

    def _getPreviousPlaylist(self):
        return self._previousPlaylist

    def _notPlayingCurrentIndex(self):
        if self._playlistIndex is None or self._playlist is None or len(self._playlist) <= self._playlistIndex:
            self._ui.showDebugMessage("Not playing current index - Index none or length issue")
            return True
        currentPlaylistFilename = self._playlist[self._playlistIndex]
        if self._client.userlist.currentUser.file and currentPlaylistFilename == self._client.userlist.currentUser.file['name']:
            return False
        else:
            self._ui.showDebugMessage("Not playing current index - Filename mismatch or no file")
            return True

    def _thereIsNextPlaylistIndex(self):
        if self._playlistIndex is None:
            return False
        elif len(self._playlist) == 1 and not self._client.loopSingleFiles():
            return False
        elif self._playlistIsAtEnd():
            return self._client.isPlaylistLoopingEnabled()
        else:
            return True

    def _nextPlaylistIndex(self):
        if self._playlistIsAtEnd():
            return 0
        else:
            return self._playlistIndex+1

    def _playlistIsAtEnd(self):
        return len(self._playlist) <= self._playlistIndex+1

    def _playlistBufferIsFromOldRoom(self, newRoom):
        return self._previousPlaylistRoom != newRoom

    def _movePlaylistBufferToNewRoom(self, currentRoom):
        self._previousPlaylist = None
        self._previousPlaylistRoom = currentRoom

    def _playlistBufferNeedsUpdating(self, newPlaylist):
        return self._previousPlaylist != self._playlist and self._playlist != newPlaylist


class FileSwitchManager(object):
    def __init__(self, client):
        self._client = client
        self.mediaFilesCache = {}
        self.filenameWatchlist = []
        self.currentDirectory = None
        self.mediaDirectories = client.getConfig().get('mediaSearchDirectories')
        self.lock = threading.Lock()
        self.folderSearchEnabled = True
        self.directorySearchError = None
        self.newInfo = False
        self.currentlyUpdating = False
        self.newWatchlist = []
        self.fileSwitchTimer = task.LoopingCall(self.updateInfo)
        self.fileSwitchTimer.start(constants.FOLDER_SEARCH_DOUBLE_CHECK_INTERVAL, True)
        self.mediaDirectoriesNotFound = []

    def setClient(self, newClient):
        self._client = newClient

    def setCurrentDirectory(self, curDir):
        self.currentDirectory = curDir

    def changeMediaDirectories(self, mediaDirs):
        from syncplay.ui.ConfigurationGetter import ConfigurationGetter
        ConfigurationGetter().setConfigOption("mediaSearchDirectories", mediaDirs)
        self._client._config["mediaSearchDirectories"] = mediaDirs
        self._client.ui.showMessage(getMessage("media-directory-list-updated-notification"))
        self.mediaDirectoriesNotFound = []
        self.folderSearchEnabled = True
        self.setMediaDirectories(mediaDirs)
        if mediaDirs == "":
            self._client.ui.showErrorMessage(getMessage("no-media-directories-error"))
            self.mediaFilesCache = {}
            self.newInfo = True
            self.checkForFileSwitchUpdate()

    def setMediaDirectories(self, mediaDirs):
        self.mediaDirectories = mediaDirs
        self.updateInfo()

    def checkForFileSwitchUpdate(self):
        if self.newInfo:
            self.newInfo = False
            self.infoUpdated()
        if self.directorySearchError:
            self._client.ui.showErrorMessage(self.directorySearchError)
            self.directorySearchError = None

    def updateInfo(self):
        if not self.currentlyUpdating and self.mediaDirectories:
            threads.deferToThread(self._updateInfoThread).addCallback(lambda x: self.checkForFileSwitchUpdate())

    def setFilenameWatchlist(self, unfoundFilenames):
        self.filenameWatchlist = unfoundFilenames

    def _updateInfoThread(self):
        with self.lock:
            try:
                self.currentlyUpdating = True
                dirsToSearch = self.mediaDirectories

                if dirsToSearch:
                    # Spin up hard drives to prevent premature timeout
                    randomFilename = "RandomFile"+str(random.randrange(10000, 99999))+".txt"
                    for directory in dirsToSearch:
                        if not os.path.isdir(directory):
                            self.directorySearchError = getMessage("cannot-find-directory-error").format(directory)

                        startTime = time.time()
                        if os.path.isfile(os.path.join(directory, randomFilename)):
                            randomFilename = "RandomFile"+str(random.randrange(10000, 99999))+".txt"
                            print("Found random file (?)")
                        if time.time() - startTime > constants.FOLDER_SEARCH_FIRST_FILE_TIMEOUT:
                            self.folderSearchEnabled = False
                            self.directorySearchError = getMessage("folder-search-first-file-timeout-error").format(directory)
                            return

                    # Actual directory search
                    newMediaFilesCache = {}
                    startTime = time.time()
                    for directory in dirsToSearch:
                        for root, dirs, files in os.walk(directory):
                            newMediaFilesCache[root] = files
                            if time.time() - startTime > constants.FOLDER_SEARCH_TIMEOUT:
                                self.directorySearchError = getMessage("folder-search-timeout-error").format(directory)
                                self.folderSearchEnabled = False
                                return

                    if self.mediaFilesCache != newMediaFilesCache:
                        self.mediaFilesCache = newMediaFilesCache
                        self.newInfo = True
            except Exception as e:
                self._client.ui.showDebugMessage(str(e))
            finally:
                self.currentlyUpdating = False

    def infoUpdated(self):
        self._client.fileSwitchFoundFiles()

    def findFilepath(self, filename, highPriority=False):
        if filename is None:
            return

        if self._client.userlist.currentUser.file and utils.sameFilename(filename, self._client.userlist.currentUser.file['name']):
            return self._client.userlist.currentUser.file['path']

        if self.mediaFilesCache is not None:
            for directory in self.mediaFilesCache:
                files = self.mediaFilesCache[directory]
                if len(files) > 0 and filename in files:
                    filepath = os.path.join(directory, filename)
                    if os.path.isfile(filepath):
                        return filepath

        if highPriority and self.folderSearchEnabled and self.mediaDirectories is not None:
            directoryList = self.mediaDirectories
            # Spin up hard drives to prevent premature timeout
            randomFilename = "RandomFile"+str(random.randrange(10000, 99999))+".txt"
            for directory in directoryList:
                startTime = time.time()
                if os.path.isfile(os.path.join(directory, randomFilename)):
                    randomFilename = "RandomFile"+str(random.randrange(10000, 99999))+".txt"
                    print("Found random file (?)")
                if not self.folderSearchEnabled:
                    return
                if time.time() - startTime > constants.FOLDER_SEARCH_FIRST_FILE_TIMEOUT:
                    self.folderSearchEnabled = False
                    self.directorySearchError = getMessage("folder-search-first-file-timeout-error").format(directory)
                    return

            startTime = time.time()
            if filename and directoryList:
                for directory in directoryList:
                    for root, dirs, files in os.walk(directory):
                        if filename in files:
                            return os.path.join(root, filename)
                        if time.time() - startTime > constants.FOLDER_SEARCH_TIMEOUT:
                            self.folderSearchEnabled = False
                            self.directorySearchError = getMessage("folder-search-timeout-error").format(directory)
                            return None
            return None

    def areWatchedFilenamesInCache(self):
        if self.filenameWatchlist is not None:
            for filename in self.filenameWatchlist:
                if self.isFilenameInCache(filename):
                    return True

    def isFilenameInCache(self, filename):
        if filename is not None and self.mediaFilesCache is not None:
            for directory in self.mediaFilesCache:
                files = self.mediaFilesCache[directory]
                if filename in files:
                    return True

    def getDirectoryOfFilenameInCache(self, filename):
        if filename is not None and self.mediaFilesCache is not None:
            for directory in self.mediaFilesCache:
                files = self.mediaFilesCache[directory]
                if filename in files:
                    return directory
        return None

    def isDirectoryInList(self, directoryToFind, folderList):
        if directoryToFind and folderList:
            normedDirectoryToFind = os.path.normcase(os.path.normpath(directoryToFind))
            for listedFolder in folderList:
                normedListedFolder = os.path.normcase(os.path.normpath(listedFolder))
                if normedDirectoryToFind.startswith(normedListedFolder):
                    return True
            return False

    def notifyUserIfFileNotInMediaDirectory(self, filenameToFind, path):
        directoryToFind = os.path.dirname(path)
        if directoryToFind in self.mediaDirectoriesNotFound:
            return
        if self.mediaDirectories is not None and self.mediaFilesCache is not None:
            if directoryToFind in self.mediaFilesCache:
                return
            for directory in self.mediaFilesCache:
                files = self.mediaFilesCache[directory]
                if filenameToFind in files:
                    return
                if directoryToFind in self.mediaFilesCache:
                    return
        if self.isDirectoryInList(directoryToFind, self.mediaDirectories):
            return
        directoryToFind = str(directoryToFind)
        self._client.ui.showErrorMessage(getMessage("added-file-not-in-media-directory-error").format(directoryToFind))
        self.mediaDirectoriesNotFound.append(directoryToFind)
