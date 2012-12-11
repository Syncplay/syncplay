#coding:utf8
import time
import threading
import thread
import win32con, win32api, win32gui, ctypes, ctypes.wintypes #@UnresolvedImport @UnusedImport
from functools import wraps
from syncplay.players.basePlayer import BasePlayer

class MPCHCAPIPlayer(BasePlayer):
    speedSupported = False
    
    def __init__(self, client):
        self.__client = client
        self._mpcApi = MpcHcApi()
        self._mpcApi.callbacks.onUpdateFilename = lambda _: self.__makePing()
        self._mpcApi.callbacks.onMpcClosed = lambda _: self.__client.stop(False)
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
    def run(client, playerPath, filePath, args):
        mpc = MPCHCAPIPlayer(client)
        mpc._mpcApi.callbacks.onConnected = lambda: mpc.initPlayer(filePath if(filePath) else None)
        mpc._mpcApi.startMpc(playerPath, args)
        return mpc

    def __lockAsking(self):
        self.__preventAsking.clear()
        
    def __unlockAsking(self):
        self.__preventAsking.set()
    
    def __onGetPosition(self):
        self.__positionUpdate.set()
    
    def setSpeed(self, value):
        self._mpcApi.setSpeed(value)
    
    def __dropIfNotSufficientVersion(self):
        self._mpcApi.askForVersion()
        if(not self.__versionUpdate.wait(0.1) and self._mpcApi.version):
            self.__mpcError("MPC version not sufficient, please use `mpc-hc` >= `1.6.4`")

    def __testMpcReady(self):
        if(not self.__preventAsking.wait(10)):
            raise Exception("Player failed opening file")
        
    def __makePing(self):
        try:
            self.__testMpcReady()
            self._mpcApi.callbacks.onUpdateFilename = lambda _: self.__handleUpdatedFilename()
            self.__client.initPlayer(self)
            self.__handleUpdatedFilename()
            self.askForStatus()
        except Exception, err:
            self.__client.ui.showErrorMessage(err.message)
            self.__client.stop()
            
    def initPlayer(self, filePath): 
        self.__dropIfNotSufficientVersion()
        self.__mpcVersion = self._mpcApi.version.split('.')
        if(self.__mpcVersion[0:3] == ['1', '6', '4']):
            self.__switchPauseCalls = True
        if(False and self.__mpcVersion[0:3] >= ['1', '6', '5']): #disabled!
            self.speedSupported = True            
        if(filePath):
            self._mpcApi.openFile(filePath)
        
    def displayMessage(self, message):
        self._mpcApi.sendOsd(message, 2, 3000)

    def setPaused(self, value):
        try:
            if self.__switchPauseCalls:
                value = not value
            if value:
                self._mpcApi.pause()
            else:
                self._mpcApi.unpause()
        except MpcHcApi.PlayerNotReadyException:
            self.setPaused(value)

    def setPosition(self, value):
        try:
            self._mpcApi.seek(value)
        except MpcHcApi.PlayerNotReadyException:
            self.setPosition(value)
        
    def __getPosition(self):
        self.__positionUpdate.clear()
        self._mpcApi.askForCurrentPosition()
        self.__positionUpdate.wait(0.2)
        return self._mpcApi.lastFilePosition
    
    def askForStatus(self):
        try:
            if(self.__preventAsking.wait(0)):
                position = self.__getPosition()
                paused = self._mpcApi.isPaused()
                position = float(position)
                if(self.__fileUpdate.acquire(0)):
                    self.__client.updatePlayerStatus(paused, position)
                    self.__fileUpdate.release()
                    return
            self.__echoGlobalStatus()
        except MpcHcApi.PlayerNotReadyException:
            self.askForStatus()
            
    def __echoGlobalStatus(self):
        self.__client.updatePlayerStatus(self.__client.getGlobalPaused(), self.__client.getGlobalPosition())

    def __forcePause(self, paused):
        for _ in xrange(25):
            self.setPaused(paused)
            time.sleep(0.005)
        
    def __setUpStateForNewlyOpenedFile(self):
        try:
            self.__forcePause(self.__client.getGlobalPaused())
            self._mpcApi.seek(self.__client.getGlobalPosition())
            if(self._mpcApi.isPaused() <> self.__client.getGlobalPaused()):
                self._mpcApi.playPause()
                time.sleep(0.001)
                self._mpcApi.playPause()
                time.sleep(0.001)
                if(self._mpcApi.isPaused() <> self.__client.getGlobalPaused()):
                    self.__setUpStateForNewlyOpenedFile()
        except MpcHcApi.PlayerNotReadyException:
            time.sleep(0.1)
            self.__setUpStateForNewlyOpenedFile()
        
    def __handleUpdatedFilename(self):
        with self.__fileUpdate:
            self.__setUpStateForNewlyOpenedFile()
            self.__client.updateFile(self._mpcApi.filePlaying, self._mpcApi.fileDuration, self._mpcApi.filePath)
    
    def __mpcError(self, err=""):
        self.__client.ui.showErrorMessage(err)
        self.__client.stop()

    def sendCustomCommand(self, cmd, val):
        self._mpcApi.sendRawCommand(cmd, val)
        
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
            if(not self.__locks.fileReady.wait(0.2)):
                raise self.PlayerNotReadyException()
            return f(self, *args, **kwds)
        return wrapper
            
    def startMpc(self, path, args=()):
        args = "%s /slave %s" % (" ".join(args), str(self.__listener.hwnd))
        win32api.ShellExecute(0, "open", path, args, None, 1)
        if(not self.__locks.mpcStart.wait(10)):
            raise self.NoSlaveDetectedException("Unable to start MPC in slave mode!")
        self.__mpcExistenceChecking.start() 

    def openFile(self, filePath):
        self.__listener.SendCommand(self.CMD_OPENFILE, filePath)
    
    def isPaused(self):
        return (self.playState <> self.__MPC_PLAYSTATE.PS_PLAY and self.playState <> None)
 
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

    def sendOsd(self, message, MsgPos=2, DurationMs=3000):
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
        if (cmd == self.CMD_CONNECT): 
            self.__listener.mpcHandle = int(value)
            self.__locks.mpcStart.set()
            if(self.callbacks.onConnected): 
                thread.start_new_thread(self.callbacks.onConnected, ())
                
        elif(cmd == self.CMD_STATE):
            self.loadState = int(value)
            fileNotReady = self.loadState == self.__MPC_LOADSTATE.MLS_CLOSING or self.loadState == self.__MPC_LOADSTATE.MLS_LOADING
            if(fileNotReady):
                self.playState = None
                self.__locks.fileReady.clear()
            else:
                self.__locks.fileReady.set()
            if(self.callbacks.onFileStateChange): 
                thread.start_new_thread(self.callbacks.onFileStateChange, (self.loadState,))
            
        elif(cmd == self.CMD_PLAYMODE):
            self.playState = int(value)
            if(self.callbacks.onUpdatePlaystate):  
                thread.start_new_thread(self.callbacks.onUpdatePlaystate, (self.playState,))
            
        elif(cmd == self.CMD_NOWPLAYING):
            value = value.split('|')
            self.filePath = value[3]
            self.filePlaying = value[3].split('\\').pop()
            self.fileDuration = float(value[4])
            if(self.callbacks.onUpdatePath): 
                thread.start_new_thread(self.callbacks.onUpdatePath, (self.onUpdatePath,))
            if(self.callbacks.onUpdateFilename): 
                thread.start_new_thread(self.callbacks.onUpdateFilename, (self.filePlaying,))
            if(self.callbacks.onUpdateFileDuration): 
                thread.start_new_thread(self.callbacks.onUpdateFileDuration, (self.fileDuration,))
            
        elif(cmd == self.CMD_CURRENTPOSITION):
            self.lastFilePosition = float(value)
            if(self.callbacks.onGetCurrentPosition): 
                thread.start_new_thread(self.callbacks.onGetCurrentPosition, (self.lastFilePosition,))
        
        elif(cmd == self.CMD_NOTIFYSEEK):
            if(self.lastFilePosition <> float(value)): #Notify seek is sometimes sent twice
                self.lastFilePosition = float(value)
                if(self.callbacks.onSeek): 
                    thread.start_new_thread(self.callbacks.onSeek, (self.lastFilePosition,))
        
        elif(cmd == self.CMD_DISCONNECT):
            if(self.callbacks.onMpcClosed): 
                thread.start_new_thread(self.callbacks.onMpcClosed, (None,))
    
        elif(cmd == self.CMD_VERSION):
            if(self.callbacks.onVersion): 
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
        while(True):
            time.sleep(10)
            if not win32gui.IsWindow(self.__listener.mpcHandle):
                if(self.callbacks.onMpcClosed):
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
                if(self.__mpcApi.callbacks.onMpcClosed):
                    self.__mpcApi.callbacks.onMpcClosed(None)
            cs = self.__COPYDATASTRUCT()
            cs.dwData = cmd;

            if(isinstance(message, (unicode, str))):
                message = ctypes.create_unicode_buffer(message, len(message) + 1)
            elif(isinstance(message, ctypes.Structure)):
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

       

    
