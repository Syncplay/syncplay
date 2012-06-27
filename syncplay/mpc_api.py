#coding:utf8

import win32con, win32api, win32gui, ctypes, ctypes.wintypes
import os, thread

class MPC_API:
    def __init__(self, enforce_custom_handler = False):
        self.enforce_custom_handler = enforce_custom_handler
        self.__listener = None
        thread.start_new_thread(self.__Listener, (self,))
        while(self.__listener == None): continue
        self.__position_request_warden = False
        self.__seek_warden = False
        self.__playpause_warden = False
        '''
        List of callbacks that can be set
        Each callback by default receives a tuple argument, can be empty though
            on_connected
            on_seek
            on_update_filename
            on_update_file_duration
            on_update_position
            on_update_playstate
            on_file_ready
            custom_handler    
        '''        
        self.callbacks = self.__CALLBACKS()
        self.loadstate = None
        self.playstate = None
        self.fileplaying = None
        self.fileduration = None
        '''
        Most likely won't be up to date unless you ask API to refresh it
        '''
        self.lastfileposition = None
    
    '''
    This is called from another thread and if it could it would be a private method
    Developers should not bother with it
    '''            
    def register_listener(self, listener):
        self.__listener = listener


    '''
    Given a path fo mpc-hc.exe and optional additional arguments in tuple
    will start mpc-hc in a slave mode
    '''
    def start_mpc(self, path, args = ()):
        is_starting = os.spawnl(os.P_NOWAIT, path,  ' ' + ' '.join(args),'/slave %s ' % str(self.__listener.hwnd)) #can be switched with win32api.ShellExecute
        while(self.__listener.mpc_handle == None and is_starting): continue
        

    '''
    Checks if api is ready to receive commands
    Throws MPC_API.NoSlaveDetectedException if mpc window is not found
    '''
    def is_api_ready(self):
        self.__mpc_ready_in_slave_mode()
        file_state_ok = self.loadstate == self.__MPC_LOADSTATE.MLS_CLOSED or self.loadstate == self.__MPC_LOADSTATE.MLS_LOADED or self.loadstate == None
        listener_ok = self.__listener <> None and self.__listener.mpc_handle <> None
        return (file_state_ok and listener_ok)
    
    '''
    Checks if file is loaded in player
    Throws MPC_API.NoSlaveDetectedException if mpc window is not found    
    '''
    def is_file_ready(self):
        self.__mpc_ready_in_slave_mode()
        return (self.loadstate == self.__MPC_LOADSTATE.MLS_LOADED and self.fileplaying and self.playstate <> None)
    
    '''
    Opens a file given in an argument in player
    Throws MPC_API.NoSlaveDetectedException if mpc window is not found    
    '''
    def open_file(self, file_path):
        self.__mpc_ready_in_slave_mode()
        self.__listener.SendCommand(MPC_API_COMMANDS.CMD_OPENFILE, file_path)
    
    '''
    Is player paused (Stop is considered pause)
    Throws MPC_API.NoSlaveDetectedException if mpc window is not found    
    '''
    def is_paused(self):
        self.__mpc_ready_in_slave_mode()
        return (self.playstate <> self.__MPC_PLAYSTATE.PS_PLAY and self.playstate <> None)
    
    '''
    Pause playing file
    Throws MPC_API.NoSlaveDetectedException if mpc window is not found    
    '''    
    def pause(self):
        self.__mpc_ready_in_slave_mode()
        while(self.playstate == None):self.__mpc_ready_in_slave_mode() 
        if(not self.is_paused() and self.__playpause_warden == False):
            self.__playpause_warden = True
            self.__listener.SendCommand(MPC_API_COMMANDS.CMD_PLAYPAUSE)
            while(not self.is_paused()): self.__mpc_ready_in_slave_mode()
            self.__playpause_warden = False
    
    '''
    Play paused file
    Throws MPC_API.NoSlaveDetectedException if mpc window is not found    
    '''  
    def unpause(self):
        self.__mpc_ready_in_slave_mode()
        while(self.playstate == None):self.__mpc_ready_in_slave_mode() 
        if(self.is_paused() and  self.__playpause_warden == False):
            self.__playpause_warden = True
            self.__listener.SendCommand(MPC_API_COMMANDS.CMD_PLAYPAUSE)
            while(self.is_paused()): self.__mpc_ready_in_slave_mode()
            self.__playpause_warden = False
    '''
    Toggle play/pause
    Throws MPC_API.NoSlaveDetectedException if mpc window is not found    
    '''  
    def playpause(self):
        self.__mpc_ready_in_slave_mode()
        tmp = self.playstate
        while(self.playstate == None):self.__mpc_ready_in_slave_mode() 
        if(self.__playpause_warden == False):
            self.__playpause_warden = True
            self.__listener.SendCommand(MPC_API_COMMANDS.CMD_PLAYPAUSE)
            while(tmp == self.playstate): self.__mpc_ready_in_slave_mode()
            self.__playpause_warden = False
    
    '''
    Asks mpc for it's current file position, if on_update_position callback is set
    developers should rather rely on that rather than on a return value
    Throws MPC_API.NoSlaveDetectedException if mpc window is not found    
    '''
    def ask_for_current_position(self):
        self.__mpc_ready_in_slave_mode()
        if(not self.__position_request_warden): 
            self.__position_request_warden = True
            self.__listener.SendCommand(MPC_API_COMMANDS.CMD_GETCURRENTPOSITION)
            while(self.__position_request_warden and not self.callbacks.on_update_position): self.__mpc_ready_in_slave_mode()
            return self.lastfileposition
    '''
    Given a position in seconds will ask client to seek there
    Throws MPC_API.NoSlaveDetectedException if mpc window is not found    
    '''  
    def seek(self, position):
        self.__mpc_ready_in_slave_mode()
        self.__seek_warden = True
        self.__listener.SendCommand(MPC_API_COMMANDS.CMD_SETPOSITION, unicode(position))
        while(self.__seek_warden): self.__mpc_ready_in_slave_mode()
    
    '''
    @param message: unicode string to display in player
    @param MsgPos: Either 1, left top corner or 2, right top corner, defaults to 2
    @param DurationMs: Duration of osd display, defaults to 3000 
    Throws MPC_API.NoSlaveDetectedException if mpc window is not found    
    '''  
    def send_osd(self, message, MsgPos = 2, DurationMs = 3000):
        self.__mpc_ready_in_slave_mode()        
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
    Throws MPC_API.NoSlaveDetectedException if mpc window is not found
    '''
    def send_raw_command(self, cmd, value):
        self.__mpc_ready_in_slave_mode()
        self.__listener.SendCommand(cmd, value)
    
    '''
    Callback function to intercept commands sent by MPC
    Handles only a handful of them
    If callbacks.custom_handler is provided all not recognized commands will be redirected to it
    If enforce_custom_handler is set it will redirect all the commands to it
    '''
    def handle_command(self,cmd, value, enforce_custom_handler = False):
        if((self.enforce_custom_handler or enforce_custom_handler) and self.callbacks.custom_handler <> None):
            self.callbacks.custom_handler((cmd, value,))
        else:
            if (cmd == MPC_API_COMMANDS.CMD_CONNECT): 
                self.__listener.mpc_handle = int(value)
                if(self.callbacks.on_connected):
                    self.callbacks.on_connected(())
                    
            elif(cmd == MPC_API_COMMANDS.CMD_STATE):
                self.loadstate = int(value)
                
            elif(cmd == MPC_API_COMMANDS.CMD_PLAYMODE):
                self.playstate = int(value)
                if(self.callbacks.on_update_playstate): self.callbacks.on_update_playstate((self.playstate,))
                
            elif(cmd == MPC_API_COMMANDS.CMD_NOWPLAYING):
                if(self.callbacks.on_file_ready): self.callbacks.on_file_ready(())
                self.fileplaying =  value.split('|')[3].split('\\').pop()
                if(self.callbacks.on_update_filename): self.callbacks.on_update_filename((self.fileplaying,))
                self.fileduration = int(value.split('|')[4])
                if(self.callbacks.on_update_file_duration): self.callbacks.on_update_file_duration((self.fileplaying,))
           
            elif(cmd == MPC_API_COMMANDS.CMD_CURRENTPOSITION):
                self.lastfileposition = float(value)
                self.__position_request_warden = False
                if(self.callbacks.on_update_position): self.callbacks.on_update_position((self.lastfileposition,))
            
            elif(cmd == MPC_API_COMMANDS.CMD_NOTIFYSEEK):
                self.__seek_warden = False
                if(self.lastfileposition <> float(value)): #Notify seek is sometimes sent twice
                    self.lastfileposition = float(value)
                    if(self.callbacks.on_seek): self.callbacks.on_seek((self.lastfileposition,))
            else:
                if(self.callbacks.custom_handler <> None):
                    self.callbacks.custom_handler((cmd, value,))
    
    class NoSlaveDetectedException(Exception):
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
            self.on_file_ready = None
            self.custom_handler = None       
            
    
    def __mpc_ready_in_slave_mode(self):
        if not win32gui.IsWindow(self.__listener.mpc_handle):
            raise MPC_API.NoSlaveDetectedException("MPC Slave Window not detected")
       
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

    class __Listener:
        def __init__(self, mpc_api):
            self.mpc_handle = None
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
            self.__PCOPYDATASTRUCT = ctypes.POINTER(self.__COPYDATASTRUCT)
            self.__mpc_api = mpc_api
            
            mpc_api.register_listener(self)
            win32gui.PumpMessages()
      
        def OnCopyData(self, hwnd, msg, wparam, lparam):
            pCDS = ctypes.cast(lparam, self.__PCOPYDATASTRUCT)
#            print ">>> 0x%X" % int(pCDS.contents.dwData), ctypes.wstring_at(pCDS.contents.lpData)
            self.__mpc_api.handle_command(pCDS.contents.dwData, ctypes.wstring_at(pCDS.contents.lpData))
    

        def SendCommand(self, cmd, message = u''):
#            print "<<< 0x%X" % int(cmd), message
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
    # Send after connection
    # Par 1 : MPC window handle (command should be send to this HWnd)
    CMD_CONNECT = 0x50000000
    # Send when opening or closing file
    # Par 1 : current state (see MPC_LOADSTATE enum)
    CMD_STATE = 0x50000001
    # Send when playing, pausing or closing file
    # Par 1 : current play mode (see MPC_PLAYSTATE enum)
    CMD_PLAYMODE = 0x50000002
    # Send after opening a new file
    # Par 1 : title
    # Par 2 : author
    # Par 3 : description
    # Par 4 : complete filename (path included)
    # Par 5 : duration in seconds
    CMD_NOWPLAYING = 0x50000003
    # List of subtitle tracks
    # Par 1 : Subtitle track name 0
    # Par 2 : Subtitle track name 1
    # ...
    # Par n : Active subtitle track, -1 if subtitles disabled
    #
    # if no subtitle track present, returns -1
    # if no file loaded, returns -2
    CMD_LISTSUBTITLETRACKS = 0x50000004
    # List of audio tracks
    # Par 1 : Audio track name 0
    # Par 2 : Audio track name 1
    # ...
    # Par n : Active audio track
    #
    # if no audio track present, returns -1
    # if no file loaded, returns -2
    CMD_LISTAUDIOTRACKS = 0x50000005
    # Send current playback position in responce
    # of CMD_GETCURRENTPOSITION.
    # Par 1 : current position in seconds
    CMD_CURRENTPOSITION = 0x50000007
    # Send the current playback position after a jump.
    # (Automatically sent after a seek event).
    # Par 1 : new playback position (in seconds).
    CMD_NOTIFYSEEK = 0x50000008
    # Notify the end of current playback
    # (Automatically sent).
    # Par 1 : none.
    CMD_NOTIFYENDOFSTREAM = 0x50000009
    # List of files in the playlist
    # Par 1 : file path 0
    # Par 2 : file path 1
    # ...
    # Par n : active file, -1 if no active file
    CMD_PLAYLIST = 0x50000006
    # ==== Commands from host to MPC
    # Open new file
    # Par 1 : file path
    CMD_OPENFILE = 0xA0000000
    # Stop playback, but keep file / playlist
    CMD_STOP = 0xA0000001
    # Stop playback and close file / playlist
    CMD_CLOSEFILE = 0xA0000002
    # Pause or restart playback
    CMD_PLAYPAUSE = 0xA0000003
    # Add a new file to playlist (did not start playing)
    # Par 1 : file path
    CMD_ADDTOPLAYLIST = 0xA0001000
    # Remove all files from playlist
    CMD_CLEARPLAYLIST = 0xA0001001
    # Start playing playlist
    CMD_STARTPLAYLIST = 0xA0001002
    CMD_REMOVEFROMPLAYLIST = 0xA0001003 # TODO
    # Cue current file to specific position
    # Par 1 : new position in seconds
    CMD_SETPOSITION = 0xA0002000
    # Set the audio delay
    # Par 1 : new audio delay in ms
    CMD_SETAUDIODELAY = 0xA0002001
    # Set the subtitle delay
    # Par 1 : new subtitle delay in ms
    CMD_SETSUBTITLEDELAY = 0xA0002002
    # Set the active file in the playlist
    # Par 1 : index of the active file, -1 for no file selected
    # DOESNT WORK
    CMD_SETINDEXPLAYLIST = 0xA0002003
    # Set the audio track
    # Par 1 : index of the audio track
    CMD_SETAUDIOTRACK = 0xA0002004
    # Set the subtitle track
    # Par 1 : index of the subtitle track, -1 for disabling subtitles
    CMD_SETSUBTITLETRACK = 0xA0002005
    # Ask for a list of the subtitles tracks of the file
    # return a CMD_LISTSUBTITLETRACKS
    CMD_GETSUBTITLETRACKS = 0xA0003000
    # Ask for the current playback position,
    # see CMD_CURRENTPOSITION.
    # Par 1 : current position in seconds
    CMD_GETCURRENTPOSITION = 0xA0003004
    # Jump forward/backward of N seconds,
    # Par 1 : seconds (negative values for backward)
    CMD_JUMPOFNSECONDS = 0xA0003005
    # Ask for a list of the audio tracks of the file
    # return a CMD_LISTAUDIOTRACKS
    CMD_GETAUDIOTRACKS = 0xA0003001
    # Ask for the properties of the current loaded file
    # return a CMD_NOWPLAYING
    CMD_GETNOWPLAYING = 0xA0003002
    # Ask for the current playlist
    # return a CMD_PLAYLIST
    CMD_GETPLAYLIST = 0xA0003003
    # Toggle FullScreen
    CMD_TOGGLEFULLSCREEN = 0xA0004000
    # Jump forward(medium)
    CMD_JUMPFORWARDMED = 0xA0004001
    # Jump backward(medium)
    CMD_JUMPBACKWARDMED = 0xA0004002
    # Increase Volume
    CMD_INCREASEVOLUME = 0xA0004003
    # Decrease volume
    CMD_DECREASEVOLUME = 0xA0004004
    # Shader toggle
    CMD_SHADER_TOGGLE = 0xA0004005
    # Close App
    CMD_CLOSEAPP = 0xA0004006
    # show host defined OSD message string
    CMD_OSDSHOWMESSAGE = 0xA0005000
        