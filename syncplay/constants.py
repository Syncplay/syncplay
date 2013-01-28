#You might want to change these
DEFAULT_PORT = 8999
OSD_DURATION = 3
OSD_WARNING_MESSAGE_DURATION = 15
MPC_OSD_POSITION = 2 #Right corner, 1 for left
MPLAYER_OSD_LEVEL = 1
UI_TIME_FORMAT = "[%X] "
DEFAULT_CONFIG_NAME = ".syncplay"

#Changing these might be ok
REWIND_THRESHOLD = 4
SEEK_THRESHOLD = 1
SLOWDOWN_RATE = 0.95
SLOWDOWN_KICKIN_THRESHOLD = 1.5
SLOWDOWN_RESET_THRESHOLD = 0.1
DIFFFERENT_DURATION_THRESHOLD = 1
PROTOCOL_TIMEOUT = 12.5
RECONNECT_RETRIES = 10
SERVER_STATE_INTERVAL = 1
WARNING_OSD_MESSAGES_LOOP_INTERVAL = 1

#Usually there's no need to adjust these
COMMANDS_UNDO = ["u", "undo", "revert"]
COMMANDS_LIST = ["l", "list", "users"]
COMMANDS_PAUSE = ["p", "play", "pause"]
COMMANDS_ROOM = ["r", "room"]
COMMANDS_HELP = ['help', 'h', '?', '/?', r'\?']
MPC_MIN_VER = "1.6.4"
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
MPV_PATHS = ["mpv", "/opt/mpv/mpv"]
VLC_PATHS = [
             r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
             r"C:\Program Files\VideoLAN\VLC\vlc.exe"
            ]
#Changing these is usually not something you're looking for
PLAYER_ASK_DELAY = 0.1
PING_MOVING_AVERAGE_WEIGHT = 0.85
MPC_OPEN_MAX_WAIT_TIME = 10
MPC_LOCK_WAIT_TIME = 0.2
MPC_RETRY_WAIT_TIME = 0.01
MPC_MAX_RETRIES = 30
MPC_PAUSE_TOGGLE_DELAY = 0.05
VLC_OPEN_MAX_WAIT_TIME = 10
VLC_SOCKET_OPEN_WAIT_TIME = 0.5

#These are not changes you're looking for
MPLAYER_SLAVE_ARGS = [ '-slave', '-nomsgcolor', '-msglevel', 'all=1:global=4']
MPV_SLAVE_ARGS = [ '--slave-broken', '-msglevel', 'all=1:global=4']
MPLAYER_ANSWER_REGEX = "^ANS_([a-zA-Z_]+)=(.+)$"
UI_COMMAND_REGEX = r"^(?P<command>[^\ ]+)(?:\ (?P<parameter>.+))?"
UI_OFFSET_REGEX = r"^(?:o|offset)\ ?(?P<sign>[/+-])?(?P<time>\d{1,4}(?:[^\d\.](?:\d{1,6})){0,2}(?:\.(?:\d{1,3}))?)$"
UI_SEEK_REGEX = r"^(?:s|seek)?\ ?(?P<sign>[+-])?(?P<time>\d{1,4}(?:[^\d\.](?:\d{1,6})){0,2}(?:\.(?:\d{1,3}))?)$"
PARSE_TIME_REGEX = r'(:?(?:(?P<hours>\d+?)[^\d\.])?(?:(?P<minutes>\d+?))?[^\d\.])?(?P<seconds>\d+?)(?:\.(?P<miliseconds>\d+?))?$'
SERVER_MAX_TEMPLATE_LENGTH = 10000
