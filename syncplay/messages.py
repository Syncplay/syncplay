# coding:utf8
from syncplay import constants

en = {

      # Client notifications
      "relative-config-notification" : "Loaded relative configuration file(s): {}",

      "connection-attempt-notification" : "Attempting to connect to {}:{}",  # Port, IP
      "reconnection-attempt-notification" : "Connection with server lost, attempting to reconnect",
      "disconnection-notification" : "Disconnected from server",
      "connection-failed-notification" : "Connection with server failed",
      "connected-successful-notification" : "Successfully connected to server",
      "retrying-notification" : "%s, Retrying in %d seconds...",  # Seconds

      "rewind-notification" : "Rewinded due to time difference with <{}>",  # User
      "slowdown-notification" : "Slowing down due to time difference with <{}>",  # User
      "revert-notification" : "Reverting speed back to normal",

      "pause-notification" : "<{}> paused",  # User
      "unpause-notification" : "<{}> unpaused",  # User
      "seek-notification" : "<{}> jumped from {} to {}",  # User, from time, to time

      "current-offset-notification" : "Current offset: {} seconds",  # Offset

      "room-join-notification" : "<{}> has joined the room: '{}'",  # User
      "left-notification" : "<{}> has left",  # User
      "left-paused-notification" : "<{}> left, <{}> paused",  # User who left, User who paused
      "playing-notification" : "<{}> is playing '{}' ({})",  # User, file, duration
      "playing-notification/room-addendum" :  " in room: '{}'",  # Room

      "file-different-notification" : "File you are playing appears to be different from <{}>'s",  # User
      "file-differences-notification" : "Your file differs in the following way(s): ",
      "room-files-not-same" : "Not all files played in the room are the same",
      "alone-in-the-room": "You're alone in the room",

      "different-filesize-notification" : " (their file size is different from yours!)",
      "file-played-by-notification" : "File: {} is being played by:",  # File
      "notplaying-notification" : "People who are not playing any file:",
      "userlist-room-notification" :  "In room '{}':",  # Room

      "mplayer-file-required-notification" : "Syncplay using mplayer requires you to provide file when starting",
      "mplayer-file-required-notification/example" : "Usage example: syncplay [options] [url|path/]filename",
      "mplayer2-required" : "Syncplay is incompatible with MPlayer 1.x, please use mplayer2 or mpv",

      "unrecognized-command-notification" : "Unrecognized command",
      "commandlist-notification" : "Available commands:",
      "commandlist-notification/room" : "\tr [name] - change room",
      "commandlist-notification/list" : "\tl - show user list",
      "commandlist-notification/undo" : "\tu - undo last seek",
      "commandlist-notification/pause" : "\tp - toggle pause",
      "commandlist-notification/seek" : "\t[s][+-]time - seek to the given value of time, if + or - is not specified it's absolute time in seconds or min:sec",
      "commandlist-notification/help" : "\th - this help",
      "syncplay-version-notification" : "Syncplay version: {}",  # syncplay.version
      "more-info-notification" : "More info available at: {}",  # projectURL

      "gui-data-cleared-notification" : "Syncplay has cleared the path and window state data used by the GUI.",

      "vlc-version-mismatch": "Warning: You are running VLC version {}, but Syncplay is designed to run on VLC {} and above.",  # VLC version, VLC min version
      "vlc-interface-version-mismatch": "Warning: You are running version {} of the Syncplay interface module for VLC, but Syncplay is designed to run with version {} and above.",  # VLC interface version, VLC interface min version
      "vlc-interface-oldversion-ignored": "Warning: Syncplay detected that an old version version of the Syncplay interface module for VLC was installed in the VLC directory. As such, if you are running VLC 2.0 then it will be ignored in favour of the syncplay.lua module contained within the Syncplay directory, but this will mean that other custom interface scripts and extensions will not work. Please refer to the Syncplay User Guide at http://syncplay.pl/guide/ for instructions on how to install syncplay.lua.",
      "vlc-interface-not-installed": "Warning: The Syncplay interface module for VLC was not found in the VLC directory. As such, if you are running VLC 2.0 then VLC will use the syncplay.lua module contained within the Syncplay directory, but this will mean that other custom interface scripts and extensions will not work. Please refer to the Syncplay User Guide at http://syncplay.pl/guide/ for instructions on how to install syncplay.lua.",

      # Client prompts
      "enter-to-exit-prompt" : "Press enter to exit\n",

      # Client errors
      "missing-arguments-error" : "Some necessary arguments are missing, refer to --help",
      "server-timeout-error" : "Connection with server timed out",
       "mpc-slave-error" : "Unable to start MPC in slave mode!",
       "mpc-version-insufficient-error" : "MPC version not sufficient, please use `mpc-hc` >= `{}`",
       "player-file-open-error" : "Player failed opening file",
       "player-path-error" : "Player path is not set properly",
       "hostname-empty-error" : "Hostname can't be empty",
       "empty-error" : "{} can't be empty",  # Configuration
       "media-player-error": "Media player error: \"{}\"",  # Error line

       "arguments-missing-error" : "Some necessary arguments are missing, refer to --help",

       "unable-to-start-client-error" : "Unable to start client",

       "not-json-error" : "Not a json encoded string\n",
       "hello-arguments-error" : "Not enough Hello arguments\n",
       "version-mismatch-error" : "Mismatch between versions of client and server\n",
       "vlc-failed-connection": "Failed to connect to VLC. If you have not installed syncplay.lua then please refer to http://syncplay.pl/LUA/ for instructions.",
       "vlc-failed-noscript": "VLC has reported that the syncplay.lua interface script has not been installed. Please refer to http://syncplay.pl/LUA/ for instructions.",
       "vlc-failed-versioncheck": "This version of VLC is not supported by Syncplay. Please use VLC 2.",
       "vlc-failed-other" : "When trying to load the syncplay.lua interface script VLC has provided the following error: {}",  # Syncplay Error

      # Client arguments
      "argument-description" : 'Solution to synchronize playback of multiple MPlayer and MPC-HC instances over the network.',
      "argument-epilog" : 'If no options supplied _config values will be used',
      "nogui-argument" : 'show no GUI',
      "host-argument" : 'server\'s address',
      "name-argument" : 'desired username',
      "debug-argument" : 'debug mode',
      "force-gui-prompt-argument" : 'make configuration prompt appear',
      "no-store-argument" : 'don\'t store values in .syncplay',
      "room-argument" : 'default room',
      "password-argument" : 'server password',
      "player-path-argument" : 'path to your player executable',
      "file-argument" : 'file to play',
      "args-argument" : 'player options, if you need to pass options starting with - prepend them with single \'--\' argument',
      "clear-gui-data-argument" : 'resets path and window state GUI data stored as QSettings',
      "language-argument" :'language for Syncplay messages (en/pl)',

      # Client labels
      "config-window-title" : "Syncplay configuration",

      "connection-group-title" : "Connection settings",
      "host-label" : "Server address: ",
      "username-label" :  "Username (optional):",
      "password-label" :  "Server password (if any):",
      "room-label" : "Default room: ",

      "media-setting-title" : "Media player settings",
      "executable-path-label" : "Path to media player:",
      "media-path-label" : "Path to media file:",
      "browse-label" : "Browse",

      "more-title" : "Show more settings",
      "slowdown-threshold-label" : "Slow down threshold:",
      "rewind-threshold-label" : "Rewind threshold:",
      "never-rewind-value" : "Never",
      "seconds-suffix" : " secs",
      "privacy-sendraw-option" : "Send raw",
      "privacy-sendhashed-option" : "Send hashed",
      "privacy-dontsend-option" : "Don't send",
      "filename-privacy-label" : "Filename information:",
      "filesize-privacy-label" : "File size information:",
      "slowdown-label" : "Slow down on desync:",
      "slowdown-auto-option" : "Automatic",
      "slowdown-always-option" : "Always",
      "slowdown-never-option" : "Never",
      "dontslowwithme-label" : "Never slow down or rewind others",
      "pauseonleave-label" : "Pause when user leaves",
      "alwayshow-label" : "Do not always show this dialog",
      "donotstore-label" : "Do not store this configuration",

      "help-label" : "Help",
      "run-label" : "Run Syncplay",
      "storeandrun-label" : "Store configuration and run Syncplay",

      "contact-label" : "Have an idea, bug report or feedback? E-mail <a href=\"mailto:dev@syncplay.pl\">dev@syncplay.pl</a>, chat via the <a href=\"https://webchat.freenode.net/?channels=#syncplay\">#Syncplay IRC channel</a> on irc.freenode.net or <a href=\"https://github.com/Uriziel/syncplay/issues/new\">raise an issue via GitHub</a>. Also check out <a href=\"http://syncplay.pl/\">http://syncplay.pl/</a> for info, help and updates.",

      "joinroom-guibuttonlabel" : "Join room",
      "seektime-guibuttonlabel" : "Seek to time",
      "undoseek-guibuttonlabel" : "Undo seek",
      "togglepause-guibuttonlabel" : "Toggle pause",
      "play-guibuttonlabel" : "Play",
      "pause-guibuttonlabel" : "Play",

      "roomuser-heading-label" : "Room / User",
      "fileplayed-heading-label" : "File being played",
      "notifications-heading-label" : "Notifications",
      "userlist-heading-label" : "List of who is playing what",
      "othercommands-heading-label" :  "Other commands",
      "room-heading-label" :  "Room",
      "seek-heading-label" :  "Seek",

      "browseformedia-label" : "Browse for media files",

      "file-menu-label" : "&File", # & precedes shortcut key
      "openmedia-menu-label" : "&Open media file",
      "exit-menu-label" : "E&xit",
      "advanced-menu-label" : "&Advanced",
      "setoffset-menu-label" : "Set &offset",
      "help-menu-label" : "&Help",
      "userguide-menu-label" : "Open user &guide",

      "setoffset-msgbox-label" : "Set offset",
      "offsetinfo-msgbox-label" : "Offset (see http://syncplay.pl/guide/ for usage instructions):",

      # Tooltips

      "host-tooltip" : "Hostname or IP to connect to, optionally including port (e.g. syncplay.pl:8999). Only synchronised with people on same server/port.",
      "username-tooltip" : "Nickname you will be known by. No registration, so can easily change later. Random name generated if none specified.",
      "password-tooltip" : "Passwords are only needed for connecting to private servers.",
      "room-tooltip" : "Room to join upon connection can be almost anything, but you will only be synchronised with people in the same room.",

      "executable-path-tooltip" : "Location of your chosen supported media player (MPC-HC, VLC, mplayer2 or mpv).",
      "media-path-tooltip" : "Location of video or stream to be opened. Necessary for mpv and mplayer2.",

      "more-tooltip" : "Display less frequently used settings.",
      "slowdown-threshold-tooltip" : "Time ahead of slowest client before temporarily reducing playback speed (default: {} secs).".format(constants.DEFAULT_SLOWDOWN_KICKIN_THRESHOLD),
      "rewind-threshold-tooltip" : "Time ahead slowest client before seeking to get back in sync (default: {} secs). 'Never' can result in major desync!".format(constants.DEFAULT_REWIND_THRESHOLD),
      "filename-privacy-tooltip" : "Privacy mode for sending currently playing filename to server.",
      "filesize-privacy-tooltip" : "Privacy mode for sending size of currently playing file to server.",
      "privacy-sendraw-tooltip" : "Send this information without obfuscation. This is the default option with most functionality.",
      "privacy-sendhashed-tooltip" : "Send a hashed version of the information, making it less visible to other clients.",
      "privacy-dontsend-tooltip" : "Do not send this information to the server. This provides for maximum privacy.",
      "slowdown-tooltip" : "Reduce playback rate temporarily when needed to bring you back in sync with other viewers.",
      "slowdown-auto-tooltip" : "Slow down on desync unless it causes problems (i.e. MPC-HC).",
      "slowdown-always-tooltip" : "Always slow down on desync (even on players where this causes playback issues).",
      "slowdown-never-tooltip" : "Never slow down on desync (even on players where this is probably better than rewinding).",
      "dontslowwithme-tooltip" : "Means others do not get slowed down or rewinded if your playback is lagging.",
      "pauseonleave-tooltip" : "Pause playback if you get disconnected or someone leaves from your room.",
      "alwayshow-tooltip" : "Configuration dialogue is not shown when opening a file with Syncplay.",
      "donotstore-tooltip" : "Run Syncplay with the given configuration, but do not permanently store the changes.",

      "help-tooltip" : "Opens the Syncplay.pl user guide.",

      "togglepause-tooltip" : "Pause/unpause media.",
      "play-tooltip" : "Unpause media.",
      "pause-tooltip" : "Pause media.",
      "undoseek-tooltip" : "Seek to where you were before the most recent seek.",
      "joinroom-tooltip" : "Leave current room and joins specified room.",
      "seektime-tooltip" : "Jump to specified time (in seconds / min:sec). Use +/- for relative seek.",

      # In-userlist notes (GUI)
      "differentsize-note" : "Different size!",
      "differentsizeandduration-note" : "Different size and duration!",
      "differentduration-note" : "Different duration!",
      "nofile-note" : "(No file being played)",

      # Server messages to client
      "new-syncplay-available-motd-message" : "<NOTICE> You are using Syncplay {} but a newer version is available from http://syncplay.pl </NOTICE>",  # ClientVersion

      # Server notifications
      "welcome-server-notification" : "Welcome to Syncplay server, ver. {0}",  # version
      "client-connected-room-server-notification" : "{0}({2}) connected to room '{1}'",  # username, host, room
      "client-left-server-notification" : "{0} left server",  # name


      # Server arguments
      "server-argument-description" : 'Solution to synchronize playback of multiple MPlayer and MPC-HC instances over the network. Server instance',
      "server-argument-epilog" : 'If no options supplied _config values will be used',
      "server-port-argument" : 'server TCP port',
      "server-password-argument" : 'server password',
      "server-isolate-room-argument" : 'should rooms be isolated?',
      "server-motd-argument": "path to file from which motd will be fetched",
      "server-messed-up-motd-unescaped-placeholders": "Message of the Day has unescaped placeholders. All $ signs should be doubled ($$).",
      "server-messed-up-motd-too-long": "Message of the Day is too long - maximum of {} chars, {} given.",
      "server-irc-verbose": "Should server actively report changes in rooms",
      "server-irc-config": "Path to irc bot config files",

      # Server errors
      "unknown-command-server-error" : "Unknown command {}",  # message
      "not-json-server-error" : "Not a json encoded string {}",  # message
      "not-known-server-error" : "You must be known to server before sending this command",
      "client-drop-server-error" : "Client drop: {} -- {}",  # host, error
      "password-required-server-error" : "Password required",
      "wrong-password-server-error" : "Wrong password supplied",
      "hello-server-error" : "Not enough Hello arguments",
      "version-mismatch-server-error" : "Mismatch between versions of client and server"


      }

pl = {

      # Client notifications
      "connection-attempt-notification" : u"Próba połączenia z {}:{}", # Port, IP
      "reconnection-attempt-notification" : u"Połączenie z serwerem zostało przerwane, ponowne łączenie",
      "disconnection-notification" : u"Odłączono od serwera",
      "connection-failed-notification" : u"Połączenie z serwerem zakończone fiaskiem",

      "rewind-notification" : u"Cofnięto z powodu różnicy czasu z <{}>", # User
      "slowdown-notification" : u"Zwolniono z powodu różnicy czasu z <{}>", # User
      "revert-notification" : u"Przywrócono normalną prędkość odtwarzania",

      "pause-notification" : u"<{}> zatrzymał odtwarzanie", # User
      "unpause-notification" : u"<{}> wznowił odtwarzanie", # User
      "seek-notification" : u"<{}> skoczył z {} do {}", # User, from time, to time

      "current-offset-notification" : u"Obecny offset: {} seconds",  # Offset

      "room-join-notification" : u"<{}> dołączył do pokoju: '{}'", # User
      "left-notification" : u"<{}> wyszedł", # User
      "playing-notification" : u"<{}> odtwarza '{}' ({})",  # User, file, duration
      "playing-notification/room-addendum" : u" w pokoju: '{}'",  # Room

      "file-different-notification" : u"Plik, który odtwarzasz wydaje się być różny od <{}>", # User
      "file-differences-notification" : u"Twój plik różni się następującymi parametrami: ",

      "different-filesize-notification" : u" (inny rozmiar pliku!)",
      "file-played-by-notification" : u"Plik: {} jest odtwarzany przez:",  # File
      "notplaying-notification" : u"Osoby, które nie odtwarzają żadnych plików:",
      "userlist-room-notification" :  u"W pokoju '{}':",  # Room
      # Client prompts
      "enter-to-exit-prompt" : u"Wciśnij Enter, aby zakończyć działanie programu\n",

      # Client errors
      "server-timeout-error" : u"Przekroczono czas oczekiwania na odpowiedź serwera"
      }

messages = {
           "en": en,
           "pl": pl,
           "current": None
           }

def setLanguage(lang):
    messages["current"] = lang

def getMessage(type_, locale=None):
    if constants.SHOW_BUTTON_LABELS == False:
        if "-guibuttonlabel" in type_:
            return ""
    if constants.SHOW_TOOLTIPS == False:
        if "-tooltip" in type_:
            return ""
    lang = messages["current"]
    if locale and messages.has_key(locale):
        if messages[locale].has_key(type_):
            return unicode(messages[locale][type_])
    if lang and messages.has_key(lang):
        if messages[lang].has_key(type_):
            return unicode(messages[lang][type_])
    if messages["en"].has_key(type_):
        return unicode(messages["en"][type_])
    else:
        raise KeyError()
