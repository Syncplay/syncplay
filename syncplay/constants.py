# coding:utf8
# code needed to get customized constants for different OS
import sys

OS_WINDOWS = "win"
OS_LINUX = "linux"
OS_MACOS = "darwin"
OS_BSD = "freebsd"
OS_DRAGONFLY = "dragonfly"
OS_DEFAULT = "default"

def getValueForOS(constantDict):
    if sys.platform.startswith(OS_WINDOWS):
        return constantDict[OS_WINDOWS] if OS_WINDOWS in constantDict else constantDict[OS_DEFAULT]
    if sys.platform.startswith(OS_LINUX):
        return constantDict[OS_LINUX] if OS_LINUX in constantDict else constantDict[OS_DEFAULT]
    if sys.platform.startswith(OS_MACOS):
        return constantDict[OS_MACOS] if OS_MACOS in constantDict else constantDict[OS_DEFAULT]
    if OS_BSD in sys.platform or sys.platform.startswith(OS_DRAGONFLY):
        return constantDict[OS_BSD] if OS_BSD in constantDict else constantDict[OS_DEFAULT]

# You might want to change these
DEFAULT_PORT = 8999
OSD_DURATION = 3.0
OSD_WARNING_MESSAGE_DURATION = 5.0
NO_ALERT_OSD_WARNING_DURATION = 13.0
MPC_OSD_POSITION = 1  # Right corner, 1 for left
MPLAYER_OSD_LEVEL = 1
UI_TIME_FORMAT = "[%X] "
CONFIG_NAMES = [".syncplay", "syncplay.ini"]  # Syncplay searches first to last
DEFAULT_CONFIG_NAME = "syncplay.ini"
RECENT_CLIENT_THRESHOLD = "1.7.5"  # This and higher considered 'recent' clients (no warnings)
MUSIC_FORMATS = [".mp3", ".m4a", ".m4p", ".wav", ".aiff", ".r", ".ogg", ".flac"] # ALL LOWER CASE!
WARN_OLD_CLIENTS = True  # Use MOTD to inform old clients to upgrade
LIST_RELATIVE_CONFIGS = True  # Print list of relative configs loaded
SHOW_CONTACT_INFO = True  # Displays dev contact details below list in GUI
SHOW_TOOLTIPS = True
WARN_ABOUT_MISSING_STRINGS = False  # (If debug mode is enabled)
FALLBACK_INITIAL_LANGUAGE = "en"
FALLBACK_PUBLIC_SYNCPLAY_SERVERS = [
    ['syncplay.pl:8995 (France)', 'syncplay.pl:8995'],
    ['syncplay.pl:8996 (France)', 'syncplay.pl:8996'],
    ['syncplay.pl:8997 (France)', 'syncplay.pl:8997'],
    ['syncplay.pl:8998 (France)', 'syncplay.pl:8998'],
    ['syncplay.pl:8999 (France)', 'syncplay.pl:8999']]
PLAYLIST_LOAD_NEXT_FILE_MINIMUM_LENGTH = 10  # Seconds
PLAYLIST_LOAD_NEXT_FILE_TIME_FROM_END_THRESHOLD = 5  # Seconds (only triggered if file is paused, e.g. due to EOF)
EXECUTABLE_COMBOBOX_MINIMUM_LENGTH = 30 # Minimum number of characters that the combobox will make visible

# Overriden by config
SHOW_OSD = True  # Sends Syncplay messages to media player OSD
SHOW_OSD_WARNINGS = True  # Show warnings if playing different file, alone in room
SHOW_SLOWDOWN_OSD = True  # Show notifications of slowing down / reverting on time difference
SHOW_SAME_ROOM_OSD = True  # Show OSD notifications for events relating to room user is in
SHOW_NONCONTROLLER_OSD = False  # Show OSD notifications for non-controllers in controlled rooms
SHOW_DIFFERENT_ROOM_OSD = False  # Show OSD notifications for events relating to room user is not in
SHOW_DURATION_NOTIFICATION = True
DEBUG_MODE = False

# Changing these might be ok
DELAYED_LOAD_WAIT_TIME = 2.5
AUTOMATIC_UPDATE_CHECK_FREQUENCY = 7 * 86400  # Days converted into seconds
DEFAULT_REWIND_THRESHOLD = 4
MINIMUM_REWIND_THRESHOLD = 3
DEFAULT_FASTFORWARD_THRESHOLD = 5
MINIMUM_FASTFORWARD_THRESHOLD = 4
FASTFORWARD_EXTRA_TIME = 0.25
FASTFORWARD_RESET_THRESHOLD = 3.0
FASTFORWARD_BEHIND_THRESHOLD = 1.75
SEEK_THRESHOLD = 1
SLOWDOWN_RATE = 0.95
DEFAULT_SLOWDOWN_KICKIN_THRESHOLD = 1.5
MINIMUM_SLOWDOWN_THRESHOLD = 1.3
SLOWDOWN_RESET_THRESHOLD = 0.1
DIFFERENT_DURATION_THRESHOLD = 2.5
PROTOCOL_TIMEOUT = 12.5
RECONNECT_RETRIES = 999
SERVER_STATE_INTERVAL = 1
SERVER_STATS_SNAPSHOT_INTERVAL = 3600
WARNING_OSD_MESSAGES_LOOP_INTERVAL = 1
AUTOPLAY_DELAY = 3.0
DO_NOT_RESET_POSITION_THRESHOLD = 1.0
SYNC_ON_PAUSE = True  # Client seek to global position - subtitles may disappear on some media players
PLAYLIST_MAX_CHARACTERS = 10000
PLAYLIST_MAX_ITEMS = 250
MAXIMUM_TAB_WIDTH = 350
TAB_PADDING = 30
MONOSPACE_FONT = getValueForOS({
    OS_DEFAULT: "Monospace",
    OS_MACOS: "Menlo",
    OS_WINDOWS: "Consolas"})
DEFAULT_CHAT_FONT_SIZE = 24
DEFAULT_CHAT_INPUT_FONT_COLOR = "#FFFF00"
DEFAULT_CHAT_OUTPUT_FONT_COLOR = "#FFFF00"
DEFAULT_CHAT_FONT_WEIGHT = 1

# Max numbers are used by server (and client pre-connection). Once connected client gets values from server featureList (or uses 'fallback' versions for old servers)
MAX_CHAT_MESSAGE_LENGTH = 150  # Number of displayed characters
MAX_USERNAME_LENGTH = 16  # Number of displayed characters
MAX_ROOM_NAME_LENGTH = 35  # Number of displayed characters
MAX_FILENAME_LENGTH = 250  # Number of displayed characters
FALLBACK_MAX_CHAT_MESSAGE_LENGTH = 50  # Number of displayed characters
FALLBACK_MAX_USERNAME_LENGTH = 16  # Number of displayed characters
FALLBACK_MAX_ROOM_NAME_LENGTH = 35  # Number of displayed characters
FALLBACK_MAX_FILENAME_LENGTH = 250  # Number of displayed characters

# Options for the File Switch feature:
FOLDER_SEARCH_FIRST_FILE_TIMEOUT = 25.0  # Secs - How long to wait to find the first file in folder search (to take account of HDD spin up)
FOLDER_SEARCH_TIMEOUT = 20.0  # Secs - How long to wait until searches in folder to update cache are aborted (after first file is found)
FOLDER_SEARCH_WARNING_THRESHOLD = 2.0 # Secs - how long until a warning saying how many files have been scanned
FOLDER_SEARCH_DOUBLE_CHECK_INTERVAL = 30.0  # Secs - Frequency of updating cache

# Usually there's no need to adjust these
DOUBLE_CHECK_REWIND = True
LAST_PAUSED_DIFF_THRESHOLD = 2
FILENAME_STRIP_REGEX = r"[-~_\.\[\](): ]"
CONTROL_PASSWORD_STRIP_REGEX = r"[^a-zA-Z0-9\-]"
ROOM_NAME_STRIP_REGEX = r"^(\+)(?P<roomnamebase>.*)(:)(\w{12})$"
ARGUMENT_SPLIT_REGEX = r'(?:[^\s"]+|"[^"]*")+'
COMMANDS_UNDO = ["u", "undo", "revert"]
COMMANDS_CHAT = ["ch", "chat"]
COMMANDS_LIST = ["l", "list", "users"]
COMMANDS_PAUSE = ["p", "play", "pause"]
COMMANDS_ROOM = ["r", "room"]
COMMANDS_HELP = ['help', 'h', '?', '/?', r'\?']
COMMANDS_CREATE = ['c', 'create']
COMMANDS_AUTH = ['a', 'auth']
COMMANDS_TOGGLE = ['t', 'toggle']
COMMANDS_QUEUE = ['queue', 'qa', 'add']
COMMANDS_QUEUEANDSELECT = ['queueandselect','qas']
COMMANDS_PLAYLIST = ['playlist', 'ql', 'pl']
COMMANDS_SELECT = ['select', 'qs']
COMMANDS_DELETE = ['delete', 'd', 'qd']
COMMANDS_NEXT = ["next", "qn"]
COMMANDS_SETREADY = ['setready', 'sr']
COMMANDS_SETNOTREADY = ['setready', 'snr']
MPC_MIN_VER = "1.6.4"
MPC_BE_MIN_VER = "1.5.2.3123"
VLC_MIN_VERSION = "2.2.1"
VLC_INTERFACE_VERSION = "0.3.7"
VLC_LATENCY_ERROR_THRESHOLD = 2.0
MPV_UNRESPONSIVE_THRESHOLD = 60.0
CONTROLLED_ROOMS_MIN_VERSION = "1.3.0"
USER_READY_MIN_VERSION = "1.3.0"
SHARED_PLAYLIST_MIN_VERSION = "1.4.0"
CHAT_MIN_VERSION = "1.5.0"
FEATURE_LIST_MIN_VERSION = "1.5.0"
SET_OTHERS_READINESS_MIN_VERSION = "1.7.2"

IINA_PATHS = ['/Applications/IINA.app/Contents/MacOS/IINA']
MPC_PATHS = [
    r"c:\program files (x86)\mpc-hc\mpc-hc.exe",
    r"c:\program files\mpc-hc\mpc-hc.exe",
    r"c:\program files\mpc-hc\mpc-hc64.exe",
    r"c:\program files\media player classic - home cinema\mpc-hc.exe",
    r"c:\program files\media player classic - home cinema\mpc-hc64.exe",
    r"c:\program files (x86)\media player classic - home cinema\mpc-hc.exe",
    r"c:\program files (x86)\k-lite codec pack\media player classic\mpc-hc.exe",
    r"c:\program files\k-lite codec pack\media Player classic\mpc-hc.exe",
    r"c:\program files\k-lite codec pack\mpc-hc64\mpc-hc64.exe",
    r"c:\program files (x86)\k-lite codec pack\mpc-hc64\mpc-hc64.exe",
    r"c:\program files (x86)\combined community codec pack\mpc\mpc-hc.exe",
    r"c:\program files\combined community codec pack\mpc\mpc-hc.exe",
    r"c:\program files\mpc homecinema (x64)\mpc-hc64.exe",
    r"c:\program files (x86)\lav filters\x86\mpc-hc\shoukaku.exe",
    r"c:\program files (x86)\lav filters\x64\mpc-hc\shoukaku.exe"
]

MPC_EXECUTABLES = ["mpc-hc.exe", "mpc-hc64.exe", "mpc-hcportable.exe", "mpc-hc_nvo.exe", "mpc-hc64_nvo.exe", "shoukaku.exe"]
MPC64_EXECUTABLES = ["mpc-hc64.exe", "mpc-hc64_nvo.exe", r"x64\mpc-hc\shoukaku.exe"]

MPC_BE_PATHS = [
    r"c:\program files\mpc-be x64\mpc-be64.exe",
    r"c:\program files\mpc-be x64\mpc-be.exe",
    r"c:\program files\mpc-be\mpc-be64.exe",
    r"c:\program files\mpc-be\mpc-be.exe"
]
MPLAYER_PATHS = ["mplayer2", "mplayer"]
MPV_PATHS = ["mpv", "/opt/mpv/mpv", r"c:\program files\mpv\mpv.exe", r"c:\program files\mpv-player\mpv.exe",
             r"c:\program Files (x86)\mpv\mpv.exe", r"c:\program Files (x86)\mpv-player\mpv.exe",
             "/Applications/mpv.app/Contents/MacOS/mpv"]
MPVNET_PATHS = [r"c:\program files\mpv.net\mpvnet.exe", r"c:\program Files (x86)\mpv.net\mpvnet.exe"]
MEMENTO_PATHS = ["memento", "/usr/bin/memento", "/usr/local/bin/memento", r"C:\Program Files\Memento\memento.exe"]

try:
    import os
    MPVNET_PATHS.append(os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WindowsApps\mpvnet.exe'))
    MPVNET_PATHS.append(os.path.expandvars(r'%LOCALAPPDATA%\Programs\mpv.net\mpvnet.exe'))
    MPV_PATHS.append(os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WindowsApps\mpv.exe'))
except:
    pass
VLC_PATHS = [
    r"c:\program files (x86)\videolan\vlc\vlc.exe",
    r"c:\program files\videolan\vlc\vlc.exe",
    "/usr/bin/vlc",
    "/usr/bin/vlc-wrapper",
    "/Applications/VLC.app/Contents/MacOS/VLC",
    "/usr/local/bin/vlc",
    "/usr/local/bin/vlc-wrapper",
    "/snap/bin/vlc"
]

VLC_ICONPATH = "vlc.png"
IINA_ICONPATH = "iina.png"
MPLAYER_ICONPATH = "mplayer.png"
MPV_ICONPATH = "mpv.png"
MPVNET_ICONPATH = "mpvnet.png"
MEMENTO_ICONPATH = "memento.png"
MPC_ICONPATH = "mpc-hc.png"
MPC64_ICONPATH = "mpc-hc64.png"
MPC_BE_ICONPATH = "mpc-be.png"

MPV_ERROR_MESSAGES_TO_REPEAT = ['[ytdl_hook] Your version of youtube-dl is too old', '[ytdl_hook] youtube-dl failed', 'Failed to recognize file format.', '[syncplayintf] Lua error']

# Changing these is usually not something you're looking for
PLAYER_ASK_DELAY = 0.1
PING_MOVING_AVERAGE_WEIGHT = 0.85
MPC_OPEN_MAX_WAIT_TIME = 10
MPC_LOCK_WAIT_TIME = 0.2
MPC_RETRY_WAIT_TIME = 0.01
MPC_MAX_RETRIES = 30
MPC_PAUSE_TOGGLE_DELAY = 0.05
MPV_NEWFILE_IGNORE_TIME = 1
MPV_SENDMESSAGE_COOLDOWN_TIME = 0.05
MPV_MAX_NEWFILE_COOLDOWN_TIME = 3
STREAM_ADDITIONAL_IGNORE_TIME = 10
MPV_LOCK_WAIT_TIME = 0.05
VLC_OPEN_MAX_WAIT_TIME = 20
VLC_MIN_PORT = 10000
VLC_MAX_PORT = 55000

# These are not changes you're looking for
STYLE_TABLIST = "QListWidget::item { border-style: solid; border-width: 1px; border-radius: 2px; } QListWidget::item:selected { color: black; background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(242, 248, 255, 255), stop:1 rgba(208, 229, 255, 255)); border-color: #84ACDD; } QListWidget::item:!selected { border-color: transparent; } QListWidget::item:!selected:hover { color: black; background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(248, 248, 248, 255), stop:1 rgba(229, 229, 229, 255)); border-color: silver; }"
STYLE_SUBCHECKBOX = "QCheckBox, QLabel, QRadioButton {{ margin-left: 6px; padding-left: 21px; background:url('{}') left no-repeat }}"  # Graphic path
STYLE_SUBLABEL = "QCheckBox, QLabel {{ margin-left: 6px; padding-left: 16px; background:url('{}') left no-repeat }}"  # Graphic path
STYLE_ERRORLABEL = "QLabel { color : black; border-style: outset; border-width: 2px; border-radius: 7px; border-color: red; padding: 2px; background: #FFAAAA; }"
STYLE_SUCCESSLABEL = "QLabel { color : black; border-style: outset; border-width: 2px; border-radius: 7px; border-color: green; padding: 2px; background: #AAFFAA; }"
STYLE_READY_PUSHBUTTON = getValueForOS({
    OS_DEFAULT: "QPushButton { text-align: left; padding: 10px 5px 10px 5px;}",
    OS_MACOS: "QPushButton { text-align: left; padding: 10px 5px 10px 15px; margin: 0px 3px 0px 2px}"})
STYLE_AUTO_PLAY_PUSHBUTTON = getValueForOS({
    OS_DEFAULT: "QPushButton { text-align: left; padding: 5px 5px 5px 5px; }",
    OS_MACOS: "QPushButton { text-align: left; padding: 10px 5px 10px 15px; margin: 0px 0px 0px -4px}"})
STYLE_NOTIFICATIONBOX = "Username { color: #367AA9; font-weight:bold; }"
STYLE_CONTACT_INFO = "<span style=\"color: grey\"><strong><small>{}</span><br /><br />"  # Contact info message
STYLE_USER_MESSAGE = "<span style=\"{}\">&lt;{}&gt;</span> {}"
STYLE_USERNAME = "color: #367AA9; font-weight:bold;"
STYLE_ERRORNOTIFICATION = "color: red;"
STYLE_DIFFERENTITEM_COLOR = 'red'
STYLE_NOFILEITEM_COLOR = 'blue'
STYLE_NOTCONTROLLER_COLOR = 'grey'
STYLE_UNTRUSTEDITEM_COLOR = 'purple'

STYLE_DARK_LINKS_COLOR = "a {color: #1A78D5; }"
STYLE_DARK_ABOUT_LINK_COLOR = "color: #1A78D5;"
STYLE_DARK_ERRORNOTIFICATION = "color: #E94F64;"
STYLE_DARK_DIFFERENTITEM_COLOR = '#E94F64'
STYLE_DARK_NOFILEITEM_COLOR = '#1A78D5'
STYLE_DARK_NOTCONTROLLER_COLOR = 'grey'
STYLE_DARK_UNTRUSTEDITEM_COLOR = '#882fbc'

TLS_CERT_ROTATION_MAX_RETRIES = 10

USERLIST_GUI_USERNAME_OFFSET = getValueForOS({
    OS_DEFAULT: 21,
    OS_MACOS: 26})  # Pixels
USERLIST_GUI_USERNAME_COLUMN = 0
USERLIST_GUI_FILENAME_COLUMN = 3

MPLAYER_SLAVE_ARGS = ['-slave', '--hr-seek=always', '-nomsgcolor', '-msglevel', 'all=1:global=4:cplayer=4', '-af-add', 'scaletempo']
MPV_ARGS = {'force-window': 'yes',
            'idle': 'yes',
            'hr-seek': 'always',
            'keep-open': 'always',
            'input-terminal': 'no',
            'term-playing-msg': '<SyncplayUpdateFile>\nANS_filename=${filename}\nANS_length=${=duration:${=length:0}}\nANS_path=${path}\n</SyncplayUpdateFile>',
            'keep-open-pause': 'yes'
            }
MPV_NET_EXTRA_ARGS = { 'auto-load-folder': 'no' }

IINA_PROPERTIES = {'geometry': '25%+100+100', 
                   'idle': 'yes',
                   'hr-seek': 'always',
                   'input-terminal': 'no',
                   'term-playing-msg': '<SyncplayUpdateFile>\nANS_filename=${filename}\nANS_length=${=duration:${=length:0}}\nANS_path=${path}\n</SyncplayUpdateFile>',
                   'keep-open-pause': 'yes',
                   }

MPV_NEW_VERSION = False
MPV_OSC_VISIBILITY_CHANGE_VERSION = False
MPV_INPUT_PROMPT_START_CHARACTER = "〉"
MPV_INPUT_PROMPT_END_CHARACTER = " 〈"
MPV_INPUT_BACKSLASH_SUBSTITUTE_CHARACTER = "＼"
MPV_SYNCPLAYINTF_OPTIONS_TO_SEND = ["chatInputEnabled", "chatInputFontFamily", "chatInputRelativeFontSize", "chatInputFontWeight", "chatInputFontUnderline",
                                    "chatInputFontColor", "chatInputPosition", "chatOutputFontFamily", "chatOutputRelativeFontSize",
                                    "chatOutputFontWeight", "chatOutputFontUnderline", "chatOutputMode", "chatMaxLines",
                                    "chatTopMargin", "chatLeftMargin", "chatBottomMargin", "chatDirectInput",
                                    "notificationTimeout", "alertTimeout", "chatTimeout", "chatOutputEnabled"]

MPV_SYNCPLAYINTF_CONSTANTS_TO_SEND = [
    "MaxChatMessageLength={}".format(MAX_CHAT_MESSAGE_LENGTH),
    "inputPromptStartCharacter={}".format(MPV_INPUT_PROMPT_START_CHARACTER),
    "inputPromptEndCharacter={}".format(MPV_INPUT_PROMPT_END_CHARACTER),
    "backslashSubstituteCharacter={}".format(MPV_INPUT_BACKSLASH_SUBSTITUTE_CHARACTER)]
# Note: Constants updated in client.py->checkForFeatureSupport
MPV_SYNCPLAYINTF_LANGUAGE_TO_SEND = ["mpv-key-tab-hint", "mpv-key-hint", "alphakey-mode-warning-first-line", "alphakey-mode-warning-second-line"]
VLC_SLAVE_ARGS = ['--extraintf=luaintf', '--lua-intf=syncplay', '--no-quiet', '--no-input-fast-seek',
                  '--play-and-pause', '--start-time=0']
VLC_SLAVE_EXTRA_ARGS = getValueForOS({
     OS_DEFAULT: ['--no-one-instance', '--no-one-instance-when-started-from-file'],
     OS_MACOS: ['--verbose=2', '--no-file-logging']})
MPV_SUPERSEDE_IF_DUPLICATE_COMMANDS = ["set_property time-pos ", "loadfile "]
MPV_REMOVE_BOTH_IF_DUPLICATE_COMMANDS = ["cycle pause"]
MPLAYER_ANSWER_REGEX = r"^ANS_([a-zA-Z_-]+)=(.+)$|^(Exiting)\.\.\. \((.+)\)$"
VLC_ANSWER_REGEX = r"(?:^(?P<command>[a-zA-Z_-]+)(?:\: )?(?P<argument>.*))"
UI_COMMAND_REGEX = r"^(?P<command>[^\ ]+)(?:\ (?P<parameter>.+))?"
UI_OFFSET_REGEX = r"^(?:o|offset)\ ?(?P<sign>[/+-])?(?P<time>\d{1,9}(?:[^\d\.](?:\d{1,9})){0,2}(?:\.(?:\d{1,3}))?)$"
UI_SEEK_REGEX = r"^(?:s|seek)?\ ?(?P<sign>[+-])?(?P<time>\d{1,4}(?:[^\d\.](?:\d{1,6})){0,2}(?:\.(?:\d{1,3}))?)$"
PARSE_TIME_REGEX = r'(:?(?:(?P<hours>\d+?)[^\d\.])?(?:(?P<minutes>\d+?))?[^\d\.])?(?P<seconds>\d+?)(?:\.(?P<miliseconds>\d+?))?$'
MESSAGE_WITH_USERNAME_REGEX = "^(<(?P<username>[^<>]+)>)(?P<message>.*)"
SERVER_MAX_TEMPLATE_LENGTH = 10000
PRIVACY_SENDRAW_MODE = "SendRaw"
PRIVACY_SENDHASHED_MODE = "SendHashed"
PRIVACY_DONTSEND_MODE = "DoNotSend"
UNPAUSE_IFALREADYREADY_MODE = "IfAlreadyReady"
UNPAUSE_IFOTHERSREADY_MODE = "IfOthersReady"
UNPAUSE_IFMINUSERSREADY_MODE = "IfMinUsersReady"
UNPAUSE_ALWAYS_MODE = "Always"
INPUT_POSITION_TOP = "Top"
INPUT_POSITION_MIDDLE = "Middle"
INPUT_POSITION_BOTTOM = "Bottom"

VLC_EOF_DURATION_THRESHOLD = 2.0

PRIVACY_HIDDENFILENAME = "**Hidden filename**"
INVERTED_STATE_MARKER = "*"
ERROR_MESSAGE_MARKER = "*"
LOAD_SAVE_MANUALLY_MARKER = "!"
CONFIG_NAME_MARKER = ":"
CONFIG_VALUE_MARKER = "="
USERITEM_CONTROLLER_ROLE = 0
USERITEM_READY_ROLE = 1
FILEITEM_SWITCH_ROLE = 1
FILEITEM_SWITCH_NO_SWITCH = 0
FILEITEM_SWITCH_FILE_SWITCH = 1
FILEITEM_SWITCH_STREAM_SWITCH = 2
PLAYLISTITEM_CURRENTLYPLAYING_ROLE = 3

MESSAGE_NEUTRAL = "neutral"
MESSAGE_BADNEWS = "bad"
MESSAGE_GOODNEWS = "good"

OSD_NOTIFICATION = "notification"  # Also known as PrimaryOSD
OSD_ALERT = "alert"  # Also known as SecondaryOSD
OSD_CHAT = "chat"

CHATROOM_MODE = "Chatroom"
SCROLLING_MODE = "Scrolling"

SYNCPLAY_UPDATE_URL = "https://syncplay.pl/checkforupdate?{}"  # Params
SYNCPLAY_DOWNLOAD_URL = "https://syncplay.pl/download/"
SYNCPLAY_PUBLIC_SERVER_LIST_URL = "https://syncplay.pl/listpublicservers?{}"  # Params

DEFAULT_TRUSTED_DOMAINS = ["youtube.com", "youtu.be"]
TRUSTABLE_WEB_PROTOCOLS = ["http", "https"]

PRIVATE_FILE_FIELDS = ["path"]

CONSOLE_UI_MODE = "CLI"
GRAPHICAL_UI_MODE = "GUI"
UNKNOWN_UI_MODE = "Unknown"
FALLBACK_ASSUMED_UI_MODE = GRAPHICAL_UI_MODE
