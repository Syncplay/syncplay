#coding:utf8
import time
import threading
import thread
import win32con, win32api, win32gui, ctypes, ctypes.wintypes #@UnresolvedImport @UnusedImport
from functools import wraps
from syncplay.players.basePlayer import BasePlayer
import re
from syncplay.utils import retry
from syncplay import constants  
from syncplay.messages import getMessage
import os.path

class MpcHcApi:
    def __init__(self):
        self.callbacks = self.__Callbacks()
        self.loadState = None
        self.playState = None
        self.filePlaying = None
        self.fileDuration = None
        self.filePath = None
        self.lastFilePosition = None
        self.version = None
        self.__playpause_warden = False
        self.__locks = self.__Locks()
        self.__mpcExistenceChecking = threading.Thread(target=self.__mpcReadyInSlaveMode, name="Check MPC window")
        self.__mpcExistenceChecking.setDaemon(True)
        self.__listener = self.__Listener(self, self.__locks)
        self.__listener.setDaemon(True)
        self.__listener.start()
        self.__locks.listenerStart.wait()
    
    def waitForFileStateReady(f): #@NoSelf
        @wraps(f)
        def wrapper(self, *args, **kwds):
            if not self.__locks.fileReady.wait(constants.MPC_LOCK_WAIT_TIME):
                raise self.PlayerNotReadyException()
            return f(self, *args, **kwds)
        return wrapper
            
    def startMpc(self, path, args=()):
        args = "%s /slave %s" % (" ".join(args), str(self.__listener.hwnd))
        win32api.ShellExecute(0, "open", path, args, None, 1)
        if not self.__locks.mpcStart.wait(constants.MPC_OPEN_MAX_WAIT_TIME):
            raise self.NoSlaveDetectedException(getMessage("mpc-slave-error"))
        self.__mpcExistenceChecking.start() 

    def openFile(self, filePath):
        self.__listener.SendCommand(self.CMD_OPENFILE, filePath)
    
    def isPaused(self):
        return self.playState <> self.__MPC_PLAYSTATE.PS_PLAY and self.playState <> None
 
    def askForVersion(self):
        self.__listener.SendCommand(self.CMD_GETVERSION)
 
    @waitForFileStateReady
    def pause(self):
        self.__listener.SendCommand(self.CMD_PAUSE)
 
    @waitForFileStateReady
    def playPause(self):
        self.__listener.SendCommand(self.CMD_PLAYPAUSE)
     
    @waitForFileStateReady
    def unpause(self):
        self.__listener.SendCommand(self.CMD_PLAY)
 
    @waitForFileStateReady
    def askForCurrentPosition(self):
        self.__listener.SendCommand(self.CMD_GETCURRENTPOSITION)

    @waitForFileStateReady
    def seek(self, position):
        self.__listener.SendCommand(self.CMD_SETPOSITION, unicode(position))

    @waitForFileStateReady
    def setSpeed(self, rate):
        self.__listener.SendCommand(self.CMD_SETSPEED, unicode(rate))

    def sendOsd(self, message, MsgPos=constants.MPC_OSD_POSITION, DurationMs=(constants.OSD_DURATION*1000)):
        class __OSDDATASTRUCT(ctypes.Structure):
            _fields_ = [
                ('nMsgPos', ctypes.c_int32),
                ('nDurationMS', ctypes.c_int32),
                ('strMsg', ctypes.c_wchar * (len(message) + 1))
            ]    
        cmessage = __OSDDATASTRUCT() 
        cmessage.nMsgPos = MsgPos 
        cmessage.nDurationMS = DurationMs 
        cmessage.strMsg = message
        self.__listener.SendCommand(self.CMD_OSDSHOWMESSAGE, cmessage)
        
    def sendRawCommand(self, cmd, value):
        self.__listener.SendCommand(cmd, value)

    def handleCommand(self, cmd, value):
        if cmd == self.CMD_CONNECT:
            self.__listener.mpcHandle = int(value)
            self.__locks.mpcStart.set()
            if self.callbacks.onConnected:
               thread.start_new_thread(self.callbacks.onConnected, ())
                
        elif cmd == self.CMD_STATE:
            self.loadState = int(value)
            fileNotReady = self.loadState == self.__MPC_LOADSTATE.MLS_CLOSING or self.loadState == self.__MPC_LOADSTATE.MLS_LOADING
            if fileNotReady:
                self.playState = None
                self.__locks.fileReady.clear()
            else:
                self.__locks.fileReady.set()
            if self.callbacks.onFileStateChange:
               thread.start_new_thread(self.callbacks.onFileStateChange, (self.loadState,))
            
        elif cmd == self.CMD_PLAYMODE:
            self.playState = int(value)
            if self.callbacks.onUpdatePlaystate:
                thread.start_new_thread(self.callbacks.onUpdatePlaystate, (self.playState,))
            
        elif cmd == self.CMD_NOWPLAYING:
            value = re.split(r'(?<!\\)\|', value)
            if self.filePath == value[3]:
                return
            self.filePath = value[3]
            self.filePlaying = value[3].split('\\').pop()
            self.fileDuration = float(value[4])
            if self.callbacks.onUpdatePath:
               thread.start_new_thread(self.callbacks.onUpdatePath, (self.onUpdatePath,))
            if self.callbacks.onUpdateFilename:
               thread.start_new_thread(self.callbacks.onUpdateFilename, (self.filePlaying,))
            if self.callbacks.onUpdateFileDuration:
               thread.start_new_thread(self.callbacks.onUpdateFileDuration, (self.fileDuration,))
            
        elif cmd == self.CMD_CURRENTPOSITION:
            self.lastFilePosition = float(value)
            if self.callbacks.onGetCurrentPosition:
               thread.start_new_thread(self.callbacks.onGetCurrentPosition, (self.lastFilePosition,))
        
        elif cmd == self.CMD_NOTIFYSEEK:
            if self.lastFilePosition <> float(value): #Notify seek is sometimes sent twice
                self.lastFilePosition = float(value)
                if self.callbacks.onSeek:
                    thread.start_new_thread(self.callbacks.onSeek, (self.lastFilePosition,))
        
        elif cmd == self.CMD_DISCONNECT:
            if self.callbacks.onMpcClosed:
               thread.start_new_thread(self.callbacks.onMpcClosed, (None,))
    
        elif cmd == self.CMD_VERSION:
            if self.callbacks.onVersion:
               self.version = value
               thread.start_new_thread(self.callbacks.onVersion, (value,))
            
    class PlayerNotReadyException(Exception):
        pass
    
    class __Callbacks:
        def __init__(self):
            self.onConnected = None
            self.onSeek = None
            self.onUpdatePath = None
            self.onUpdateFilename = None
            self.onUpdateFileDuration = None
            self.onGetCurrentPosition = None
            self.onUpdatePlaystate = None
            self.onFileStateChange = None
            self.onMpcClosed = None
            self.onVersion = None
            
    class __Locks:
        def __init__(self):
            self.listenerStart = threading.Event()
            self.mpcStart = threading.Event()
            self.fileReady = threading.Event()
            
    def __mpcReadyInSlaveMode(self):
        while True:
            time.sleep(10)
            if not win32gui.IsWindow(self.__listener.mpcHandle):
                if self.callbacks.onMpcClosed:
                    self.callbacks.onMpcClosed(None)
                break
               
    CMD_CONNECT = 0x50000000
    CMD_STATE = 0x50000001
    CMD_PLAYMODE = 0x50000002
    CMD_NOWPLAYING = 0x50000003
    CMD_LISTSUBTITLETRACKS = 0x50000004
    CMD_LISTAUDIOTRACKS = 0x50000005
    CMD_CURRENTPOSITION = 0x50000007
    CMD_NOTIFYSEEK = 0x50000008
    CMD_NOTIFYENDOFSTREAM = 0x50000009
    CMD_PLAYLIST = 0x50000006
    CMD_OPENFILE = 0xA0000000
    CMD_STOP = 0xA0000001
    CMD_CLOSEFILE = 0xA0000002
    CMD_PLAYPAUSE = 0xA0000003
    CMD_ADDTOPLAYLIST = 0xA0001000
    CMD_CLEARPLAYLIST = 0xA0001001
    CMD_STARTPLAYLIST = 0xA0001002
    CMD_REMOVEFROMPLAYLIST = 0xA0001003 # TODO
    CMD_SETPOSITION = 0xA0002000
    CMD_SETAUDIODELAY = 0xA0002001
    CMD_SETSUBTITLEDELAY = 0xA0002002
    CMD_SETINDEXPLAYLIST = 0xA0002003 # DOESNT WORK
    CMD_SETAUDIOTRACK = 0xA0002004
    CMD_SETSUBTITLETRACK = 0xA0002005
    CMD_GETSUBTITLETRACKS = 0xA0003000
    CMD_GETCURRENTPOSITION = 0xA0003004
    CMD_JUMPOFNSECONDS = 0xA0003005
    CMD_GETAUDIOTRACKS = 0xA0003001
    CMD_GETNOWPLAYING = 0xA0003002
    CMD_GETPLAYLIST = 0xA0003003
    CMD_TOGGLEFULLSCREEN = 0xA0004000
    CMD_JUMPFORWARDMED = 0xA0004001
    CMD_JUMPBACKWARDMED = 0xA0004002
    CMD_INCREASEVOLUME = 0xA0004003
    CMD_DECREASEVOLUME = 0xA0004004
    CMD_SHADER_TOGGLE = 0xA0004005
    CMD_CLOSEAPP = 0xA0004006
    CMD_OSDSHOWMESSAGE = 0xA0005000
    CMD_VERSION = 0x5000000A
    CMD_DISCONNECT = 0x5000000B
    CMD_PLAY = 0xA0000004
    CMD_PAUSE = 0xA0000005
    CMD_GETVERSION = 0xA0003006
    CMD_SETSPEED = 0xA0004008
    
    class __MPC_LOADSTATE:
        MLS_CLOSED = 0
        MLS_LOADING = 1
        MLS_LOADED = 2
        MLS_CLOSING = 3
    
    class __MPC_PLAYSTATE:
        PS_PLAY = 0
        PS_PAUSE = 1
        PS_STOP = 2
        PS_UNUSED = 3

    class __Listener(threading.Thread):
        def __init__(self, mpcApi, locks):
            self.__mpcApi = mpcApi
            self.locks = locks
            self.mpcHandle = None
            self.hwnd = None
            self.__PCOPYDATASTRUCT = ctypes.POINTER(self.__COPYDATASTRUCT) 
            threading.Thread.__init__(self, name="MPC Listener")
            
        def run(self):   
            message_map = {
                win32con.WM_COPYDATA: self.OnCopyData
            }
            wc = win32gui.WNDCLASS()
            wc.lpfnWndProc = message_map
            wc.lpszClassName = 'MPCApiListener'
            hinst = wc.hInstance = win32api.GetModuleHandle(None)
            classAtom = win32gui.RegisterClass(wc)
            self.hwnd = win32gui.CreateWindow (
                classAtom,
                "ListenerGUI",
                0,
                0,
                0,
                win32con.CW_USEDEFAULT,
                win32con.CW_USEDEFAULT,
                0,
                0,
                hinst,
                None
            )
            self.locks.listenerStart.set()
            win32gui.PumpMessages()
            
      
        def OnCopyData(self, hwnd, msg, wparam, lparam):
            pCDS = ctypes.cast(lparam, self.__PCOPYDATASTRUCT)
            #print "API:\tin>\t 0x%X\t" % int(pCDS.contents.dwData), ctypes.wstring_at(pCDS.contents.lpData)
            self.__mpcApi.handleCommand(pCDS.contents.dwData, ctypes.wstring_at(pCDS.contents.lpData))
    
        def SendCommand(self, cmd, message=u''):
            #print "API:\t<out\t 0x%X\t" % int(cmd), message
            if not win32gui.IsWindow(self.mpcHandle):
                if self.__mpcApi.callbacks.onMpcClosed:
                    self.__mpcApi.callbacks.onMpcClosed(None)
            cs = self.__COPYDATASTRUCT()
            cs.dwData = cmd;

            if isinstance(message, (unicode, str)):
                message = ctypes.create_unicode_buffer(message, len(message) + 1)
            elif isinstance(message, ctypes.Structure):
                pass
            else:
                raise TypeError
            cs.lpData = ctypes.addressof(message)
            cs.cbData = ctypes.sizeof(message)
            ptr = ctypes.addressof(cs)
            win32api.SendMessage(self.mpcHandle, win32con.WM_COPYDATA, self.hwnd, ptr)    
            
        class __COPYDATASTRUCT(ctypes.Structure):
            _fields_ = [
                ('dwData', ctypes.wintypes.LPARAM),
                ('cbData', ctypes.wintypes.DWORD),
                ('lpData', ctypes.c_void_p)
            ]

class MPCHCAPIPlayer(BasePlayer):
    speedSupported = False
    secondaryOSDSupported = False
    customOpenDialog = False
    osdMessageSeparator = "; "
    
    def __init__(self, client):
        from twisted.internet import reactor
        self.reactor = reactor
        self.__client = client
        self._mpcApi = MpcHcApi()
        self._mpcApi.callbacks.onUpdateFilename = lambda _: self.__makePing()
        self._mpcApi.callbacks.onMpcClosed = lambda _: self.reactor.callFromThread(self.__client.stop, False,)
        self._mpcApi.callbacks.onFileStateChange = lambda _: self.__lockAsking()
        self._mpcApi.callbacks.onUpdatePlaystate = lambda _: self.__unlockAsking()
        self._mpcApi.callbacks.onGetCurrentPosition = lambda _: self.__onGetPosition()
        self._mpcApi.callbacks.onVersion = lambda _: self.__versionUpdate.set()
        self.__switchPauseCalls = False
        self.__preventAsking = threading.Event()
        self.__positionUpdate = threading.Event()
        self.__versionUpdate = threading.Event()
        self.__fileUpdate = threading.RLock()
        self.__versionUpdate.clear()
        
    def drop(self):
        self.__preventAsking.set()
        self.__positionUpdate.set()
        self.__versionUpdate.set()
        self._mpcApi.sendRawCommand(MpcHcApi.CMD_CLOSEAPP, "")

    @staticmethod
    def getPlayerPathErrors(playerPath, filePath):
        return None

    @staticmethod
    def run(client, playerPath, filePath, args):
        args.extend(['/open', '/new'])
        mpc = MPCHCAPIPlayer(client)
        mpc._mpcApi.callbacks.onConnected = lambda: mpc.initPlayer(filePath if filePath else None)
        mpc._mpcApi.startMpc(MPCHCAPIPlayer.getExpandedPath(playerPath), args)
        client.initPlayer(mpc)
        return mpc

    def __lockAsking(self):
        self.__preventAsking.clear()
        
    def __unlockAsking(self):
        self.__preventAsking.set()
    
    def __onGetPosition(self):
        self.__positionUpdate.set()
    
    def setSpeed(self, value):
        try:
            self._mpcApi.setSpeed(value)
        except MpcHcApi.PlayerNotReadyException:
            self.setSpeed(value)
            
    def __dropIfNotSufficientVersion(self):
        self._mpcApi.askForVersion()
        if not self.__versionUpdate.wait(0.1) or not self._mpcApi.version:
            self.reactor.callFromThread(self.__client.ui.showErrorMessage, getMessage("mpc-version-insufficient-error").format(constants.MPC_MIN_VER), True)
            self.reactor.callFromThread(self.__client.stop, True)
            
    def __testMpcReady(self):
        if not self.__preventAsking.wait(10):
            raise Exception(getMessage("player-file-open-error"))
        
    def __makePing(self):
        try:
            self.__testMpcReady()
            self._mpcApi.callbacks.onUpdateFilename = lambda _: self.__handleUpdatedFilename()
            self.__handleUpdatedFilename()
            self.askForStatus()
        except Exception, err:
            self.reactor.callFromThread(self.__client.ui.showErrorMessage, err.message, True)
            self.reactor.callFromThread(self.__client.stop)
            
    def initPlayer(self, filePath): 
        self.__dropIfNotSufficientVersion()
        if not self._mpcApi.version:
            return
        self.__mpcVersion = self._mpcApi.version.split('.')
        if self.__mpcVersion[0:3] == ['1', '6', '4']:
            self.__switchPauseCalls = True
        if filePath:
            self.openFile(filePath)
    
    def openFile(self, filePath, resetPosition=False):
        self._mpcApi.openFile(filePath)
        
    def displayMessage(self, message, duration = (constants.OSD_DURATION*1000), secondaryOSD=False):
        self._mpcApi.sendOsd(message, constants.MPC_OSD_POSITION, duration)

    @retry(MpcHcApi.PlayerNotReadyException, constants.MPC_MAX_RETRIES, constants.MPC_RETRY_WAIT_TIME, 1)
    def setPaused(self, value):
        if self._mpcApi.filePlaying:
            if self.__switchPauseCalls:
                value = not value
            if value:
                self._mpcApi.pause()
            else:
                self._mpcApi.unpause()
            
    @retry(MpcHcApi.PlayerNotReadyException, constants.MPC_MAX_RETRIES, constants.MPC_RETRY_WAIT_TIME, 1)
    def setPosition(self, value):
        if self._mpcApi.filePlaying:
            self._mpcApi.seek(value)
        
    def __getPosition(self):
        self.__positionUpdate.clear()
        self._mpcApi.askForCurrentPosition()
        self.__positionUpdate.wait(constants.MPC_LOCK_WAIT_TIME)
        return self._mpcApi.lastFilePosition
    
    @retry(MpcHcApi.PlayerNotReadyException, constants.MPC_MAX_RETRIES, constants.MPC_RETRY_WAIT_TIME, 1)
    def askForStatus(self):
        if self._mpcApi.filePlaying and self.__preventAsking.wait(0) and self.__fileUpdate.acquire(0):
            self.__fileUpdate.release()
            position = self.__getPosition()
            paused = self._mpcApi.isPaused()
            position = float(position)
            if self.__preventAsking.wait(0) and self.__fileUpdate.acquire(0):
                self.__client.updatePlayerStatus(paused, position)
                self.__fileUpdate.release()
            return
        self.__echoGlobalStatus()
            
    def __echoGlobalStatus(self):
        self.__client.updatePlayerStatus(self.__client.getGlobalPaused(), self.__client.getGlobalPosition())

    def __forcePause(self):
        for _ in xrange(constants.MPC_MAX_RETRIES):
            self.setPaused(True)
            time.sleep(constants.MPC_RETRY_WAIT_TIME)
        
    def __refreshMpcPlayState(self):
        for _ in xrange(2): 
            self._mpcApi.playPause()
            time.sleep(constants.MPC_PAUSE_TOGGLE_DELAY)

    def _setPausedAccordinglyToServer(self):
        self.__forcePause()
        self.setPaused(self.__client.getGlobalPaused())
        if self._mpcApi.isPaused() <> self.__client.getGlobalPaused():
            self.__refreshMpcPlayState()
            if self._mpcApi.isPaused() <> self.__client.getGlobalPaused():
                self.__setUpStateForNewlyOpenedFile()
    
    @retry(MpcHcApi.PlayerNotReadyException, constants.MPC_MAX_RETRIES, constants.MPC_RETRY_WAIT_TIME, 1)                
    def __setUpStateForNewlyOpenedFile(self):
        self._setPausedAccordinglyToServer()
        self._mpcApi.seek(self.__client.getGlobalPosition())
 
    def __handleUpdatedFilename(self):
        with self.__fileUpdate:
            self.__setUpStateForNewlyOpenedFile()
            args = (self._mpcApi.filePlaying, self._mpcApi.fileDuration, self._mpcApi.filePath)
            self.reactor.callFromThread(self.__client.updateFile, *args)

    def sendCustomCommand(self, cmd, val):
        self._mpcApi.sendRawCommand(cmd, val)
        
    @staticmethod
    def getDefaultPlayerPathsList():
        return constants.MPC_PATHS
    
    @staticmethod
    def getIconPath(path):
        if MPCHCAPIPlayer.getExpandedPath(path).lower().endswith(u'mpc-hc64.exe'.lower()):
            return constants.MPC64_ICONPATH
        else:
            return constants.MPC_ICONPATH
    
    @staticmethod
    def isValidPlayerPath(path):
        if MPCHCAPIPlayer.getExpandedPath(path):
            return True
        return False

    @staticmethod
    def getExpandedPath(path):
        if os.path.isfile(path):
            if path.lower().endswith(u'mpc-hc.exe'.lower()) or path.lower().endswith(u'mpc-hc64.exe'.lower()):
                return path
        if os.path.isfile(path + u"mpc-hc.exe"):
            path += u"mpc-hc.exe"
            return path
        if os.path.isfile(path + u"\\mpc-hc.exe"):
            path += u"\\mpc-hc.exe"
            return path
        if os.path.isfile(path + u"mpc-hc64.exe"):
            path += u"mpc-hc64.exe"
            return path
        if os.path.isfile(path + u"\\mpc-hc64.exe"):
            path += u"\\mpc-hc64.exe"
            return path
