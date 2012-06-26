#coding:utf8

import win32con, win32api, win32gui, ctypes, ctypes.wintypes
import sys, os, thread

class MPC_API:
    def __init__(self):
        self.listener = None
        thread.start_new_thread(self.__Listener, (self,))
        while(self.listener == None): continue
    
        self.loadstate = None
        self.playstate = None
        self.fileplaying = None
        self.fileduration = None
        self.lastfileposition = None
        self.position_request_warden = False
        self.seek_warden = False
        self.callbacks = self.__CALLBACKS()
        
    def register_listener(self, listener):
        self.listener = listener

    def is_api_ready(self):
        self.__mpc_ready_in_slave_mode()
        file_state_ok = self.loadstate == self.__MPC_LOADSTATE.MLS_CLOSED or self.loadstate == self.__MPC_LOADSTATE.MLS_LOADED or self.loadstate == None
        listener_ok = self.listener <> None and self.listener.mpc_handle <> None
        return (file_state_ok and listener_ok)
    
    def is_file_ready(self):
        self.__mpc_ready_in_slave_mode()
        return (self.loadstate == self.__MPC_LOADSTATE.MLS_LOADED and self.fileplaying and self.playstate <> None)
    
    def start_mpc(self, path, args = ()):
        is_starting = os.spawnl(os.P_NOWAIT, path,  ' ' + ' '.join(args),' /open /new /slave %s ' % str(self.listener.hwnd)) #can be switched with win32api.ShellExecute
        while(self.listener.mpc_handle == None and is_starting): continue
        
    def open_file(self, file_path):
        self.__mpc_ready_in_slave_mode()
        self.listener.SendCommand(self.__API_COMMANDS.CMD_OPENFILE, file_path)
    
    def is_paused(self):
        self.__mpc_ready_in_slave_mode()
        return (self.playstate <> self.__MPC_PLAYSTATE.PS_PLAY and self.playstate <> None)
    
    def pause(self):
        self.__mpc_ready_in_slave_mode()
        if(not self.is_paused()):
            self.listener.SendCommand(self.__API_COMMANDS.CMD_PLAYPAUSE)
            while(not self.is_paused()): self.__mpc_ready_in_slave_mode()
    
    def unpause(self):
        self.__mpc_ready_in_slave_mode()
        if(self.is_paused()):
            self.listener.SendCommand(self.__API_COMMANDS.CMD_PLAYPAUSE)
            while(self.is_paused()): self.__mpc_ready_in_slave_mode()
    
    def playpause(self):
        self.__mpc_ready_in_slave_mode()
        tmp = self.playstate
        self.listener.SendCommand(self.__API_COMMANDS.CMD_PLAYPAUSE)
        while(tmp == self.playstate): self.__mpc_ready_in_slave_mode()
    
    def ask_for_current_position(self):
        self.__mpc_ready_in_slave_mode()
        if(not self.position_request_warden): 
            self.position_request_warden = True
            self.listener.SendCommand(self.__API_COMMANDS.CMD_GETCURRENTPOSITION)
            while(self.position_request_warden and not self.callbacks.on_update_position): self.__mpc_ready_in_slave_mode()
            return self.lastfileposition

    def seek(self, position):
        self.__mpc_ready_in_slave_mode()
        self.seek_warden = True
        self.listener.SendCommand(self.__API_COMMANDS.CMD_SETPOSITION, unicode(position))
        while(self.seek_warden):
            continue

    def __mpc_ready_in_slave_mode(self):
        if not win32gui.IsWindow(self.listener.mpc_handle):
                raise MPC_API.NoSlaveDetectedException("MPC Slave Window not detected")
            
    def handle_command(self,cmd, value):
        #print '>>>'+hex(cmd).upper(), value
        if (cmd == self.__API_COMMANDS.CMD_CONNECT): 
            self.listener.mpc_handle = int(value)
            if(self.callbacks.on_connected):
                self.callbacks.on_connected()
        elif(cmd == self.__API_COMMANDS.CMD_STATE):
            self.loadstate = int(value)
        elif(cmd == self.__API_COMMANDS.CMD_PLAYMODE):
            self.playstate = int(value)
            if(self.callbacks.on_update_playstate): self.callbacks.on_update_playstate(self.playstate)
        elif(cmd == self.__API_COMMANDS.CMD_NOWPLAYING):
            if(self.callbacks.on_file_ready): self.callbacks.on_file_ready()
            self.fileplaying =  value.split('|')[3].split('\\').pop()
            if(self.callbacks.on_update_filename): self.callbacks.on_update_filename(self.fileplaying)
            self.fileduration = int(value.split('|')[4])
            if(self.callbacks.on_update_file_duration): self.callbacks.on_update_file_duration(self.fileplaying)
        elif(cmd == self.__API_COMMANDS.CMD_CURRENTPOSITION):
            self.lastfileposition = float(value)
            self.position_request_warden = False
            if(self.callbacks.on_update_position): self.callbacks.on_update_position(self.lastfileposition)
        elif(cmd == self.__API_COMMANDS.CMD_NOTIFYSEEK):
            self.seek_warden = False
            if(self.lastfileposition <> float(value)): #Notify seek is sometimes sent twice
                self.lastfileposition = float(value)
                if(self.callbacks.on_seek): self.callbacks.on_seek(self.lastfileposition)
        else:
            pass
    
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
    class MPC_OSDDATA():
        _fields_ = [
            ('nMsgPos'),
            ('nDurationMS'),
            ('strMsg')
        ]
    '''
    class __API_COMMANDS():
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

    class __Listener:
        def SendCommand(self, cmd, message = ''):
            #print "<<<" + (hex(cmd).upper()), str(message)
            if not win32gui.IsWindow(self.mpc_handle):
                raise MPC_API.NoSlaveDetectedException("MPC Slave Window not detected")
            cs = self.__COPYDATASTRUCT()
            cs.dwData = cmd;
            cs.lpData = ctypes.cast(ctypes.c_wchar_p(message), ctypes.c_void_p)
            utf_size_multiplier = 2 if sys.maxunicode < 65536 else 4
            cs.cbData = utf_size_multiplier*len(message)+1
            ptr= ctypes.addressof(cs)
            win32api.SendMessage(self.mpc_handle, win32con.WM_COPYDATA, self.hwnd, ptr)      
        class __COPYDATASTRUCT(ctypes.Structure):
            _fields_ = [
                ('dwData', ctypes.wintypes.LPARAM),
                ('cbData', ctypes.wintypes.DWORD),
                ('lpData', ctypes.c_void_p)
            ]
        def __init__(self, mpc_api):
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
            self.mpc_api = mpc_api
            self.mpc_handle = None
            mpc_api.register_listener(self)
            win32gui.PumpMessages()
            
        def OnCopyData(self, hwnd, msg, wparam, lparam):
            pCDS = ctypes.cast(lparam, self.__PCOPYDATASTRUCT)
            self.mpc_api.handle_command(pCDS.contents.dwData, ctypes.wstring_at(pCDS.contents.lpData))
