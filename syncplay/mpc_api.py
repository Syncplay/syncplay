#coding:utf8

import threading,time,thread
import win32con, win32api, win32gui, ctypes, ctypes.wintypes #@UnresolvedImport @UnusedImport

class MPC_API:
    def __init__(self, enforce_custom_handler = False):
        self.enforce_custom_handler = enforce_custom_handler
        '''
        List of callbacks that can be set
            on_connected (0 args)
            on_seek (0 args)
            on_update_filename (filename)
            on_update_file_duration (duration)
            on_update_position (positon)
            on_update_playstate (playstate)
            on_file_ready (filename)
            custom_handler (cmd, value)
        '''    
        self.callbacks = self.__CALLBACKS()
        self.loadstate = None
        self.playstate = None
        self.fileplaying = None
        self.fileduration = None
        self.filepath = None
        '''
        Most likely won't be up to date unless you ask API to refresh it
        '''
        self.lastfileposition = None
        self.__playpause_warden = False
        self.__locks = self.__LOCKS()
        self.__mpc_ready_checking = threading.Thread(target = self.__mpc_ready_in_slave_mode, name ="Check MPC window")
        self.__mpc_ready_checking.setDaemon(True)
        self.__listener = self.__Listener(self, self.__locks)
        self.__listener.setDaemon(True)
        self.__listener.start()
        self.__locks.listner_start.wait()


    
    '''
    Given a path fo mpc-hc.exe and optional additional arguments in tuple
    will start mpc-hc in a slave mode
    '''
    def start_mpc(self, path, args = ()):
        args = "%s /slave %s" % (" ".join(args), str(self.__listener.hwnd))
        win32api.ShellExecute(0, "open", path, args, None, 1)
        if(not self.__locks.mpc_start.wait(10)):
            raise MPC_API.NoSlaveDetectedException("Unable to start MPC in slave mode!")
        self.__mpc_ready_checking.start() 

    '''
    Checks if api is ready to receive commands
    '''
    def is_api_ready(self):
        file_state_ok = self.loadstate == self.__MPC_LOADSTATE.MLS_CLOSED or self.loadstate == self.__MPC_LOADSTATE.MLS_LOADED or self.loadstate == None
        listener_ok = self.__listener <> None and self.__listener.mpc_handle <> None
        return (file_state_ok and listener_ok)
    
    '''
    Checks if file is loaded in player

    '''
    def is_file_ready(self):
        return (self.loadstate == self.__MPC_LOADSTATE.MLS_LOADED and self.fileplaying and self.playstate <> None)
    
    '''
    Opens a file given in an argument in player

    '''
    def open_file(self, file_path):
        self.__listener.SendCommand(MPC_API_COMMANDS.CMD_OPENFILE, file_path)
    
    '''
    Is player paused (Stop is considered pause)

    '''
    def is_paused(self):
        return (self.playstate <> self.__MPC_PLAYSTATE.PS_PLAY and self.playstate <> None)
    
    '''
    Pause playing file

    '''    
    def pause(self):
        if(not self.is_file_ready()): raise MPC_API.PlayerNotReadyException("Playstate change on no file")
        if(not self.is_paused()):
            self.playpause()
    '''
    Play paused file

    '''  
    def unpause(self):
        if(not self.is_file_ready()): raise MPC_API.PlayerNotReadyException("Playstate change on no file")
        if(self.is_paused()):
            self.playpause()
    '''
    Toggle play/pause

    '''  
    def playpause(self):
        if(not self.is_file_ready()): raise MPC_API.PlayerNotReadyException("Playstate change on no file")
        tmp = self.playstate
        if(self.__playpause_warden == False):
            self.__playpause_warden = True
            self.__listener.SendCommand(MPC_API_COMMANDS.CMD_PLAYPAUSE)
        while(tmp == self.playstate and self.__playpause_warden): continue
        self.__playpause_warden = False
        if(tmp == self.playstate): self.playpause() #playstate changed manualy after issuing a command

    
    '''
    Asks mpc for it's current file position, if on_update_position callback is set
    developers should rather rely on that rather than on a return value

    '''
    def ask_for_current_position(self):
        if(not self.is_file_ready()):
            raise MPC_API.PlayerNotReadyException("File not yet ready")
        self.__locks.positionget.clear()
        self.__listener.SendCommand(MPC_API_COMMANDS.CMD_GETCURRENTPOSITION)
        if(not self.callbacks.on_update_position): 
            if(not self.__locks.positionget.wait(0.2)):
                raise MPC_API.PlayerNotReadyException("Position get fail")
        return self.lastfileposition
    '''
    Given a position in seconds will ask client to seek there

    '''  
    def seek(self, position):
        self.__locks.seek.clear()
        self.__listener.SendCommand(MPC_API_COMMANDS.CMD_SETPOSITION, unicode(position))
        if(not self.__locks.seek.wait(0.2)):
                raise MPC_API.PlayerNotReadyException("Seek fail")
    '''
    @param message: unicode string to display in player
    @param MsgPos: Either 1, left top corner or 2, right top corner, defaults to 2
    @param DurationMs: Duration of osd display, defaults to 3000 

    '''  
    def send_osd(self, message, MsgPos = 2, DurationMs = 3000):
        class __OSDDATASTRUCT(ctypes.Structure):
            _fields_ = [
                ('nMsgPos', ctypes.c_int32),
                ('nDurationMS', ctypes.c_int32),
                ('strMsg', ctypes.c_wchar * (len(message)+1))
            ]    
        cmessage = __OSDDATASTRUCT() 
        cmessage.nMsgPos = MsgPos 
        cmessage.nDurationMS = DurationMs 
        cmessage.strMsg = message
        self.__listener.SendCommand(MPC_API_COMMANDS.CMD_OSDSHOWMESSAGE, cmessage)
        
    '''
    Send raw cmd and value to mpc
    Commands are available in MPC_API_COMMANDS class
    Value has to be either ctype.Structure or unicode string

    '''
    def send_raw_command(self, cmd, value):
        self.__listener.SendCommand(cmd, value)
    
    '''
    Callback function to intercept commands sent by MPC
    Handles only a handful of them
    If callbacks.custom_handler is provided all not recognized commands will be redirected to it
    If enforce_custom_handler is set it will redirect all the commands to it
    '''
    def handle_command(self,cmd, value, enforce_custom_handler = False):
        if((self.enforce_custom_handler or enforce_custom_handler) and self.callbacks.custom_handler <> None):
            thread.start_new_thread(self.callbacks.custom_handler,(cmd, value,))
        else:
            if (cmd == MPC_API_COMMANDS.CMD_CONNECT): 
                self.__listener.mpc_handle = int(value)
                self.__locks.mpc_start.set()
                if(self.callbacks.on_connected):
                    thread.start_new_thread(self.callbacks.on_connected, ())
                    
            elif(cmd == MPC_API_COMMANDS.CMD_STATE):
                self.loadstate = int(value)
                if(self.callbacks.on_fileStateChange): thread.start_new_thread(self.callbacks.on_fileStateChange, (self.loadstate,))
                
            elif(cmd == MPC_API_COMMANDS.CMD_PLAYMODE):
                self.playstate = int(value)
                if(self.callbacks.on_update_playstate):  thread.start_new_thread(self.callbacks.on_update_playstate,(self.playstate,))
                
            elif(cmd == MPC_API_COMMANDS.CMD_NOWPLAYING):
                self.filepath = value.split('|')[3]
                self.fileplaying =  value.split('|')[3].split('\\').pop()
                self.fileduration = value.split('|')[4]
                if(self.callbacks.on_update_filename): thread.start_new_thread(self.callbacks.on_update_filename,(self.fileplaying,))
                if(self.callbacks.on_update_file_duration): thread.start_new_thread(self.callbacks.on_update_file_duration,(self.fileduration,))
                
            elif(cmd == MPC_API_COMMANDS.CMD_CURRENTPOSITION):
                self.lastfileposition = float(value)
                self.__locks.positionget.set()
                if(self.callbacks.on_update_position): thread.start_new_thread(self.callbacks.on_update_position,(self.lastfileposition,))
            
            elif(cmd == MPC_API_COMMANDS.CMD_NOTIFYSEEK):
                self.__locks.seek.set()
                if(self.lastfileposition <> float(value)): #Notify seek is sometimes sent twice
                    self.lastfileposition = float(value)
                    if(self.callbacks.on_seek): thread.start_new_thread(self.callbacks.on_seek,(self.lastfileposition,))
            else:
                if(self.callbacks.custom_handler <> None):
                    thread.start_new_thread(self.callbacks.custom_handler,(cmd, value,))
    
    class NoSlaveDetectedException(Exception):
        def __init__(self, message):
            Exception.__init__(self, message)
    class PlayerNotReadyException(Exception):
        def __init__(self, message):
            Exception.__init__(self, message)
    
    class __CALLBACKS:
        def __init__(self):
            self.on_connected = None
            self.on_seek = None
            self.on_update_filename = None
            self.on_update_file_duration = None
            self.on_update_position = None
            self.on_update_playstate = None
            self.on_fileStateChange = None
            self.custom_handler = None       
            self.on_mpc_closed = None
            
    class __LOCKS:
        def __init__(self):
            self.listner_start = threading.Event()
            self.mpc_start = threading.Event()
            self.positionget = threading.Event()
            self.seek = threading.Event()
            
    def __mpc_ready_in_slave_mode(self):
        while(True):
            time.sleep(1)
            if not win32gui.IsWindow(self.__listener.mpc_handle):
                self.callbacks.on_mpc_closed()
                break
               
    class __MPC_LOADSTATE:
        MLS_CLOSED = 0
        MLS_LOADING = 1
        MLS_LOADED = 2
        MLS_CLOSING = 3
    
    class __MPC_PLAYSTATE:
        PS_PLAY   = 0
        PS_PAUSE  = 1
        PS_STOP   = 2
        PS_UNUSED = 3

    '''
    class __OSD_MESSAGEPOS:
        OSD_NOMESSAGE = 0
        OSD_TOPLEFT = 1
        OSD_TOPRIGHT = 2

    '''

    class __Listener(threading.Thread):
        def __init__(self, mpc_api, locks):
            self.__mpc_api = mpc_api
            self.locks = locks
            self.mpc_handle = None
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
            self.locks.listner_start.set()
            win32gui.PumpMessages()
            
      
        def OnCopyData(self, hwnd, msg, wparam, lparam):
            pCDS = ctypes.cast(lparam, self.__PCOPYDATASTRUCT)
            #print "API:\tin>\t 0x%X\t" % int(pCDS.contents.dwData), ctypes.wstring_at(pCDS.contents.lpData)
            self.__mpc_api.handle_command(pCDS.contents.dwData, ctypes.wstring_at(pCDS.contents.lpData))
    
        def SendCommand(self, cmd, message = u''):
            #print "API:\t<out\t 0x%X\t" % int(cmd), message
            if not win32gui.IsWindow(self.mpc_handle):
                raise MPC_API.NoSlaveDetectedException("MPC Slave Window not detected")
            cs = self.__COPYDATASTRUCT()
            cs.dwData = cmd;

            if(isinstance(message, (unicode, str))):
                message = ctypes.create_unicode_buffer(message, len(message)+1)
            elif(isinstance(message, ctypes.Structure)):
                pass
            else:
                raise TypeError
            cs.lpData = ctypes.addressof(message)
            cs.cbData = ctypes.sizeof(message)
            ptr= ctypes.addressof(cs)
            win32api.SendMessage(self.mpc_handle, win32con.WM_COPYDATA, self.hwnd, ptr)    
            
        class __COPYDATASTRUCT(ctypes.Structure):
            _fields_ = [
                ('dwData', ctypes.wintypes.LPARAM),
                ('cbData', ctypes.wintypes.DWORD),
                ('lpData', ctypes.c_void_p)
            ]

       
class MPC_API_COMMANDS():
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
       
    