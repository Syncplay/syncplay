from syncplay.players.basePlayer import BasePlayer
from syncplay import constants
from mutagen.mp3 import MP3
from time import time
import requests
import os


class StreamData():
    def __init__(self):
        pass

    def close(self):
        pass

    '''
    @type file_name: string
    @type position: float
    @type speed: float
    @type paused: bool
    @type address: tuple

    Send formatted data to the given address
    '''

    def sendto(self, position, speed, paused, address):
        try:
            data = {"position": position, "speed": speed,
                    "paused": paused, "time": time()}
            requests.post(address, json=data)
        except:
            print("can't connect to the server right now")


class HttpPlayer(BasePlayer):
    speedSupported = True
    customOpenDialog = False
    chatOSDSupported = False
    alertOSDSupported = False
    osdMessageSeparator = ""

    SEND_ADDRESS = "http://127.0.0.1:5000/data"
    DEFAULT_PATH = "/HttpPlayer"
    DEFAULT_FILE = "want.mp3"

    def __init__(self, client, playerPath, filePath, args):
        self._stream = StreamData()
        self._client = client

        self._filepath = filePath if filePath else self.DEFAULT_FILE  # For the audio file
        self._position = 0.0  # In seconds
        self._speed = 1.0  # Percentage
        self._paused = False
        self._done = False
        self._last_send = time()

        try:
            self.openFile(self._filepath)
            self._client.updateFile(os.path.basename(self._filepath), MP3(
                self._filepath).info.length, self._filepath)
            self.setPaused(True)
            self.setPosition(0.0)
        except Exception as e:
            print(e)

        self._client.initPlayer(self)

    '''
    Send stream properties to the server through the StreamData object
    '''

    def streamUpdate(self):
        self._stream.sendto(self._position, self._speed,
                            self._paused, self.SEND_ADDRESS)

    '''
    This method is supposed to
    execute updatePlayerStatus(paused, position) on client
    Given the arguments: boolean paused and float position in seconds
    '''

    def askForStatus(self):
        if not self._client.userlist.currentUser.ready:
            self._client.toggleReady()
        if time() - self._last_send >= 5:
            self._position = self._client.getGlobalPosition()
            self._paused = self._client.getGlobalPaused()
            self.streamUpdate()
            self._last_send = time()

        self._client.updatePlayerStatus(
            self._client.getGlobalPaused(), self._client.getGlobalPosition())

    '''
    Display given message on player's OSD or similar means
    '''

    def displayMessage(
        self, message, duration=(constants.OSD_DURATION*1000), secondaryOSD=False, mood=constants.MESSAGE_NEUTRAL
    ):
        pass  # Nothing to see here

    '''
    Cleanup connection with player before syncplay will close down
    '''

    def drop(self):
        self._stream.close()
        self._done = True

    '''
    Start up the player, returns its instance
    '''
    @ staticmethod
    def run(client, playerPath, filePath, args):
        return HttpPlayer(client, playerPath, filePath, args)

    '''
    @type value: boolean
    '''

    def setPaused(self, value):
        print(f"set pause {value}")
        self._paused = value
        self.streamUpdate()

    '''
        @type value: list
        '''

    def setFeatures(self, featureList):
        pass  # Nothing to see here...

    '''
    @type value: float
    '''

    def setPosition(self, value):
        print(f"set position: {value}")
        self._position = value
        self.streamUpdate()

    '''
    @type value: float
    '''

    def setSpeed(self, value):
        print(f"set speed {value}")
        self._speed = value
        self.streamUpdate()

    '''
    @type filePath: string
    '''

    def openFile(self, filePath, resetPosition=False):
        print(f"open file: {filePath}")
        self._filepath = filePath
        self.streamUpdate()

    '''
    @return: list of strings
    '''
    @ staticmethod
    def getDefaultPlayerPathsList():
        pass

    '''
    @type path: string
    '''
    @ staticmethod
    def isValidPlayerPath(path):
        # Always true because it's really a player
        return path == HTTPPlayer.DEFAULT_PATH

    '''
    @type path: string
    @return: string
    '''
    @ staticmethod
    def getIconPath(path):
        return None  # Nothing to see here

    '''
    @type path: string
    @return: string
    '''
    @ staticmethod
    def getExpandedPath(path):
        return path  # Not really a player

    '''
    @type playerPath: string
    @type filePath: string
    @return errorMessage: string

    Checks if the player has any problems with the given player/file path
    '''
    @ staticmethod
    def getPlayerPathErrors(playerPath, filePath):
        return None  # Nothing to see here
