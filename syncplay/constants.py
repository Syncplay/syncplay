# You might want to change these
DEFAULT_PORT = 8999
OSD_DURATION = 3
OSD_WARNING_MESSAGE_DURATION = 15
MPC_OSD_POSITION = 2  #Right corner, 1 for left
MPLAYER_OSD_LEVEL = 1
UI_TIME_FORMAT = "[%X] "
CONFIG_NAMES = [".syncplay", "syncplay.ini"]  #Syncplay searches first to last
DEFAULT_CONFIG_NAME_WINDOWS = "syncplay.ini"
DEFAULT_CONFIG_NAME_LINUX = ".syncplay"
RECENT_CLIENT_THRESHOLD = "1.2.9"  #This and higher considered 'recent' clients (no warnings)
WARN_OLD_CLIENTS = True  #Use MOTD to inform old clients to upgrade
LIST_RELATIVE_CONFIGS = True  # Print list of relative configs loaded
SHOW_CONTACT_INFO = True  # Displays dev contact details below list in GUI
SHOW_BUTTON_LABELS = True  # If disabled, only shows icons for main GUI buttons
SHOW_TOOLTIPS = True
WARN_ABOUT_MISSING_STRINGS = False # (If debug mode is enabled)

#Overriden by config
SHOW_OSD = True  # Sends Syncplay messages to media player OSD
SHOW_OSD_WARNINGS = True  # Show warnings if playing different file, alone in room
SHOW_SLOWDOWN_OSD = True  # Show notifications of slowing down / reverting on time difference
SHOW_SAME_ROOM_OSD = True  # Show OSD notifications for events relating to room user is in
SHOW_DIFFERENT_ROOM_OSD = False  # Show OSD notifications for events relating to room user is not in
SHOW_DURATION_NOTIFICATION = True
DEBUG_MODE = False

#Changing these might be ok
DEFAULT_REWIND_THRESHOLD = 4
MINIMUM_REWIND_THRESHOLD = 3
DEFAULT_FASTFORWARD_THRESHOLD = 5
MINIMUM_FASTFORWARD_THRESHOLD = 2
FASTFORWARD_EXTRA_TIME = 0.25
SEEK_THRESHOLD = 1
SLOWDOWN_RATE = 0.95
DEFAULT_SLOWDOWN_KICKIN_THRESHOLD = 1.5
MINIMUM_SLOWDOWN_THRESHOLD = 1.3
SLOWDOWN_RESET_THRESHOLD = 0.1
DIFFFERENT_DURATION_THRESHOLD = 2.5
PROTOCOL_TIMEOUT = 12.5
RECONNECT_RETRIES = 10
SERVER_STATE_INTERVAL = 1
WARNING_OSD_MESSAGES_LOOP_INTERVAL = 1
MERGE_PLAYPAUSE_BUTTONS = False
SYNC_ON_PAUSE = True  # Client seek to global position - subtitles may disappear on some media players
#Usually there's no need to adjust these
FILENAME_STRIP_REGEX = u"[-~_\.\[\](): ]"
CONTROL_PASSWORD_STRIP_REGEX = u"[^a-zA-Z0-9\-]"
ROOM_NAME_STRIP_REGEX = u"^(\+)(?P<roomnamebase>.*)(:)(\w{12})$"
COMMANDS_UNDO = ["u", "undo", "revert"]
COMMANDS_LIST = ["l", "list", "users"]
COMMANDS_PAUSE = ["p", "play", "pause"]
COMMANDS_ROOM = ["r", "room"]
COMMANDS_HELP = ['help', 'h', '?', '/?', r'\?']
COMMANDS_CREATE = ['c','create']
COMMANDS_AUTH = ['a','auth']
MPC_MIN_VER = "1.6.4"
VLC_MIN_VERSION = "2.0.0"
VLC_INTERFACE_MIN_VERSION = "0.2.1"
CONTROLLED_ROOMS_MIN_VERSION = "1.3.0"
MPC_PATHS = [
    r"C:\Program Files (x86)\MPC-HC\mpc-hc.exe",
    r"C:\Program Files\MPC-HC\mpc-hc.exe",
    r"C:\Program Files\MPC-HC\mpc-hc64.exe",
    r"C:\Program Files\Media Player Classic - Home Cinema\mpc-hc.exe",
    r"C:\Program Files\Media Player Classic - Home Cinema\mpc-hc64.exe",
    r"C:\Program Files (x86)\Media Player Classic - Home Cinema\mpc-hc.exe",
    r"C:\Program Files (x86)\K-Lite Codec Pack\Media Player Classic\mpc-hc.exe",
    r"C:\Program Files\K-Lite Codec Pack\Media Player Classic\mpc-hc.exe",
    r"C:\Program Files (x86)\Combined Community Codec Pack\MPC\mpc-hc.exe",
    r"C:\Program Files\Combined Community Codec Pack\MPC\mpc-hc.exe",
    r"C:\Program Files\MPC HomeCinema (x64)\mpc-hc64.exe",
]
MPLAYER_PATHS = ["mplayer2", "mplayer"]
MPV_PATHS = ["mpv", "/opt/mpv/mpv", r"C:\Program Files\mpv\mpv.exe", r"C:\Program Files\mpv-player\mpv.exe",
             r"C:\Program Files (x86)\mpv\mpv.exe", r"C:\Program Files (x86)\mpv-player\mpv.exe",
             "/Applications/mpv.app/Contents/MacOS/mpv"]
VLC_PATHS = [
    r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
    r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "/usr/bin/vlc",
    "/usr/bin/vlc-wrapper",
    "/Applications/VLC.app/Contents/MacOS/VLC",
    "/usr/local/bin/vlc",
    "/usr/local/bin/vlc-wrapper"
]

VLC_ICONPATH = "vlc.png"
MPLAYER_ICONPATH = "mplayer.png"
MPV_ICONPATH = "mpv.png"
MPC_ICONPATH = "mpc-hc.png"
MPC64_ICONPATH = "mpc-hc64.png"

#Changing these is usually not something you're looking for
PLAYER_ASK_DELAY = 0.1
PING_MOVING_AVERAGE_WEIGHT = 0.85
MPC_OPEN_MAX_WAIT_TIME = 10
MPC_LOCK_WAIT_TIME = 0.2
MPC_RETRY_WAIT_TIME = 0.01
MPC_MAX_RETRIES = 30
MPC_PAUSE_TOGGLE_DELAY = 0.05
MPV_NEWFILE_IGNORE_TIME = 1
MPV_LOCK_WAIT_TIME = 0.2
VLC_OPEN_MAX_WAIT_TIME = 15
VLC_MIN_PORT = 10000
VLC_MAX_PORT = 55000

#These are not changes you're looking for
STYLE_TABLIST = "QListWidget::item { color: black; border-style: solid; border-width: 1px; border-radius: 2px; } QListWidget::item:selected { background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(242, 248, 255, 255), stop:1 rgba(208, 229, 255, 255)); border-color: #84ACDD; } QListWidget::item:!selected { border-color: transparent; } QListWidget::item:!selected:hover { background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(248, 248, 248, 255), stop:1 rgba(229, 229, 229, 255)); border-color: silver; }"
STYLE_SUBCHECKBOX  = "QCheckBox, QLabel {{ margin-left: 6px; padding-left: 21px; background:url('{}') left no-repeat }}" #Graphic path
STYLE_SUBLABEL  = "QCheckBox, QLabel {{ margin-left: 6px; padding-left: 16px; background:url('{}') left no-repeat }}" #Graphic path
STYLE_ERRORLABEL = "QLabel { color : black; border-style: outset; border-width: 2px; border-radius: 7px; border-color: red; padding: 2px; background: #FFAAAA; }"
STYLE_SUCCESSLABEL = "QLabel { color : black; border-style: outset; border-width: 2px; border-radius: 7px; border-color: green; padding: 2px; background: #AAFFAA; }"
STYLE_NOTIFICATIONBOX = "Username { color: #367AA9; font-weight:bold; }"
STYLE_USERNAME = "color: #367AA9; font-weight:bold;"
STYLE_ERRORNOTIFICATION = "color: red;"
STYLE_DIFFERENTITEM_COLOR = 'red'
STYLE_NOFILEITEM_COLOR = 'blue'
STYLE_NOTCONTROLLER_COLOR = 'grey'

USERLIST_GUI_USERNAME_OFFSET = 21 # Pixels

MPLAYER_SLAVE_ARGS = ['-slave', '--hr-seek=always', '-nomsgcolor', '-msglevel', 'all=1:global=4:cplayer=4', '-af', 'scaletempo']
# --quiet works with both mpv 0.2 and 0.3
MPV_SLAVE_ARGS = ['--hr-seek=always', '--quiet', '--keep-open', '-af', 'scaletempo']
MPV_SLAVE_ARGS_WINDOWS = ['--slave-broken']
MPV_SLAVE_ARGS_NONWINDOWS = ['--input-terminal=no','--input-file=/dev/stdin']
MPV_SLAVE_ARGS_NEW = ['--term-playing-msg=<SyncplayUpdateFile>\nANS_filename=${filename}\nANS_length=${=length}\nANS_path=${path}\n</SyncplayUpdateFile>']
MPV_NEW_VERSION = False
VLC_SLAVE_ARGS = ['--extraintf=luaintf', '--lua-intf=syncplay', '--no-quiet', '--no-input-fast-seek',
                  '--play-and-pause', '--start-time=0']
VLC_SLAVE_NONOSX_ARGS = ['--no-one-instance', '--no-one-instance-when-started-from-file']
MPLAYER_ANSWER_REGEX = "^ANS_([a-zA-Z_-]+)=(.+)$|^(Exiting)\.\.\. \((.+)\)$"
VLC_ANSWER_REGEX = r"(?:^(?P<command>[a-zA-Z_]+)(?:\: )?(?P<argument>.*))"
UI_COMMAND_REGEX = r"^(?P<command>[^\ ]+)(?:\ (?P<parameter>.+))?"
UI_OFFSET_REGEX = r"^(?:o|offset)\ ?(?P<sign>[/+-])?(?P<time>\d{1,4}(?:[^\d\.](?:\d{1,6})){0,2}(?:\.(?:\d{1,3}))?)$"
UI_SEEK_REGEX = r"^(?:s|seek)?\ ?(?P<sign>[+-])?(?P<time>\d{1,4}(?:[^\d\.](?:\d{1,6})){0,2}(?:\.(?:\d{1,3}))?)$"
PARSE_TIME_REGEX = r'(:?(?:(?P<hours>\d+?)[^\d\.])?(?:(?P<minutes>\d+?))?[^\d\.])?(?P<seconds>\d+?)(?:\.(?P<miliseconds>\d+?))?$'
SERVER_MAX_TEMPLATE_LENGTH = 10000
PRIVACY_SENDRAW_MODE = "SendRaw"
PRIVACY_SENDHASHED_MODE = "SendHashed"
PRIVACY_DONTSEND_MODE = "DoNotSend"
PRIVACY_HIDDENFILENAME = "**Hidden filename**"
INVERTED_STATE_MARKER = "*"
ERROR_MESSAGE_MARKER = "*"
LOAD_SAVE_MANUALLY_MARKER = "!"
CONFIG_NAME_MARKER = ":"
CONFIG_VALUE_MARKER = "="
USERITEM_CONTROLLER_ROLE = 0
USERITEM_READY_ROLE = 1
