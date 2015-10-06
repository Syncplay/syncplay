# coding:utf8
from syncplay import constants

en = {
      "LANGUAGE" : "English",
      
      # Client notifications
      "config-cleared-notification" : "Settings cleared. Changes will be saved when you store a valid configuration.",

      "relative-config-notification" : u"Loaded relative configuration file(s): {}",

      "connection-attempt-notification" : "Attempting to connect to {}:{}",  # Port, IP
      "reconnection-attempt-notification" : "Connection with server lost, attempting to reconnect",
      "disconnection-notification" : "Disconnected from server",
      "connection-failed-notification" : "Connection with server failed",
      "connected-successful-notification" : "Successfully connected to server",
      "retrying-notification" : "%s, Retrying in %d seconds...",  # Seconds

      "rewind-notification" : "Rewinded due to time difference with <{}>",  # User
      "fastforward-notification" : "Fast-forwarded due to time difference with <{}>",  # User
      "slowdown-notification" : "Slowing down due to time difference with <{}>",  # User
      "revert-notification" : "Reverting speed back to normal",

      "pause-notification" : u"<{}> paused",  # User
      "unpause-notification" : u"<{}> unpaused",  # User
      "seek-notification" : u"<{}> jumped from {} to {}",  # User, from time, to time

      "current-offset-notification" : "Current offset: {} seconds",  # Offset

      "room-join-notification" : u"<{}> has joined the room: '{}'",  # User
      "left-notification" : u"<{}> has left",  # User
      "left-paused-notification" : u"<{}> left, <{}> paused",  # User who left, User who paused
      "playing-notification" : u"<{}> is playing '{}' ({})",  # User, file, duration
      "playing-notification/room-addendum" :  u" in room: '{}'",  # Room

      "not-all-ready" : u"Not ready: {}", # Usernames
      "all-users-ready" : u"Everyone is ready ({} users)", #Number of ready users
      "ready-to-unpause-notification" : u"You are now set as ready - unpause again to unpause",
      "set-as-ready-notification" : u"You are now set as ready",
      "set-as-not-ready-notification" : u"You are now set as not ready",
      "autoplaying-notification" : u"Auto-playing in {}...",  # Number of seconds until playback will start

      "identifying-as-controller-notification" : u"Identifying as room operator with password '{}'...",
      "failed-to-identify-as-controller-notification" : u"<{}> failed to identify as a room operator.",
      "authenticated-as-controller-notification" : u"<{}> authenticated as a room operator",
      "created-controlled-room-notification" : u"Created managed room '{}' with password '{}'. Please save this information for future reference!", # RoomName, operatorPassword

      "file-different-notification" : "File you are playing appears to be different from <{}>'s",  # User
      "file-differences-notification" : u"Your file differs in the following way(s): {}", # Differences
      "room-file-differences" : u"File differences: {}", # File differences (filename, size, and/or duration)
      "file-difference-filename" : u"name",
      "file-difference-filesize" : u"size",
      "file-difference-duration" : u"duration",
      "alone-in-the-room": u"You're alone in the room",

      "different-filesize-notification" : u" (their file size is different from yours!)",
      "userlist-playing-notification" : u"{} is playing:", #Username
      "file-played-by-notification" : u"File: {} is being played by:",  # File
      "no-file-played-notification" : u"{} is not playing a file", # Username
      "notplaying-notification" : "People who are not playing any file:",
      "userlist-room-notification" :  u"In room '{}':",  # Room
      "userlist-file-notification" : "File",
      "controller-userlist-userflag" : "Operator",
      "ready-userlist-userflag" : "Ready",
      
      "update-check-failed-notification" : u"Could not automatically check whether Syncplay {} is up to date. Want to visit http://syncplay.pl/ to manually check for updates?", #Syncplay version
      "syncplay-uptodate-notification" : u"Syncplay is up to date",
      "syncplay-updateavailable-notification" : u"A new version of Syncplay is available. Do you want to visit the release page?",

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
      "commandlist-notification/toggle" : u"\tt - toggles whether you are ready to watch or not",
      "commandlist-notification/create" : "\tc [name] - create managed room using name of current room",
      "commandlist-notification/auth" : "\ta [password] - authenticate as room operator with operator password",
      "syncplay-version-notification" : "Syncplay version: {}",  # syncplay.version
      "more-info-notification" : "More info available at: {}",  # projectURL

      "gui-data-cleared-notification" : "Syncplay has cleared the path and window state data used by the GUI.",
      "language-changed-msgbox-label" : "Language will be changed when you run Syncplay.",
      "promptforupdate-label" : u"Is it okay for Syncplay to automatically check for updates from time to time?",

      "vlc-version-mismatch": "Warning: You are running VLC version {}, but Syncplay is designed to run on VLC {} and above.",  # VLC version, VLC min version
      "vlc-interface-version-mismatch": "Warning: You are running version {} of the Syncplay interface module for VLC, but Syncplay is designed to run with version {} and above.",  # VLC interface version, VLC interface min version
      "vlc-interface-oldversion-warning": "Warning: Syncplay detected that an old version version of the Syncplay interface module for VLC was installed in the VLC directory. Please refer to the Syncplay User Guide at http://syncplay.pl/guide/ for instructions on how to install syncplay.lua.",
      "vlc-interface-not-installed": "Warning: The Syncplay interface module for VLC was not found in the VLC directory. As such, if you are running VLC 2.0 then VLC will use the syncplay.lua module contained within the Syncplay directory, but this will mean that other custom interface scripts and extensions will not work. Please refer to the Syncplay User Guide at http://syncplay.pl/guide/ for instructions on how to install syncplay.lua.",
      "media-player-latency-warning": u"Warning: The media player took {} seconds to respond. If you experience syncing issues then close applications to free up system resources, and if that doesn't work then try a different media player.", # Seconds to respond
      "mpv-unresponsive-error": u"mpv has not responded for {} seconds so appears to have malfunctioned. Please restart Syncplay.", # Seconds to respond

      # Client prompts
      "enter-to-exit-prompt" : "Press enter to exit\n",

      # Client errors
      "missing-arguments-error" : "Some necessary arguments are missing, refer to --help",
      "server-timeout-error" : "Connection with server timed out",
       "mpc-slave-error" : "Unable to start MPC in slave mode!",
       "mpc-version-insufficient-error" : "MPC version not sufficient, please use `mpc-hc` >= `{}`",
       "mpv-version-error" : "Syncplay is not compatible with this version of mpv. Please use a different version of mpv (e.g. Git HEAD).",
       "player-file-open-error" : "Player failed opening file",
       "player-path-error" : "Player path is not set properly",
       "hostname-empty-error" : "Hostname can't be empty",
       "empty-error" : "{} can't be empty",  # Configuration
       "media-player-error": "Media player error: \"{}\"",  # Error line
       "unable-import-gui-error": "Could not import GUI libraries. If you do not have PySide installed then you will need to install it for the GUI to work.",

       "arguments-missing-error" : "Some necessary arguments are missing, refer to --help",

       "unable-to-start-client-error" : "Unable to start client",

       "player-path-config-error": "Player path is not set properly",
       "no-file-path-config-error" :"File must be selected before starting your player",
       "no-hostname-config-error": "Hostname can't be empty",
       "invalid-port-config-error" : "Port must be valid",
       "empty-value-config-error" : "{} can't be empty", # Config option

       "not-json-error" : "Not a json encoded string\n",
       "hello-arguments-error" : "Not enough Hello arguments\n",
       "version-mismatch-error" : "Mismatch between versions of client and server\n",
       "vlc-failed-connection": "Failed to connect to VLC. If you have not installed syncplay.lua then please refer to http://syncplay.pl/LUA/ for instructions.",
       "vlc-failed-noscript": "VLC has reported that the syncplay.lua interface script has not been installed. Please refer to http://syncplay.pl/LUA/ for instructions.",
       "vlc-failed-versioncheck": "This version of VLC is not supported by Syncplay. Please use VLC 2.",
       "vlc-failed-other" : "When trying to load the syncplay.lua interface script VLC has provided the following error: {}",  # Syncplay Error

       "not-supported-by-server-error" : "This feature is not supported by the server. The feature requires a server running Syncplay {}+, but the server is running Syncplay {}.", #minVersion, serverVersion

       "invalid-seek-value" : u"Invalid seek value",
       "invalid-offset-value" : u"Invalid offset value",

      "switch-file-not-found-error" : u"Could not switch to file '{0}'. Syncplay looks in the folder of the currently playing file and specified media directories.", # File not found
      "folder-search-timeout-error" : u"The search for media in '{}' was aborted as it took too long. This will occur if you select a folder with too many sub-folders in your list of media folders to search through. Until Syncplay is restarted only the directory of the currently open file will be checked.", #Folder

      "failed-to-load-server-list-error" : u"Failed to load public server list. Please visit http://www.syncplay.pl/ in your browser.",

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
      "language-argument" :'language for Syncplay messages (de/en/ru)',

      "version-argument" : 'prints your version',
      "version-message" : "You're using Syncplay version {} ({})",

      # Client labels
      "config-window-title" : "Syncplay configuration",

      "connection-group-title" : "Connection settings",
      "host-label" : "Server address: ",
      "name-label" :  "Username (optional):",
      "password-label" :  "Server password (if any):",
      "room-label" : "Default room: ",

      "media-setting-title" : "Media player settings",
      "executable-path-label" : "Path to media player:",
      "media-path-label" : "Path to media file:",
      "player-arguments-label" : "Player arguments (if any):",
      "browse-label" : "Browse",
      "update-server-list-label" : u"Update list",

      "more-title" : "Show more settings",
      "never-rewind-value" : "Never",
      "seconds-suffix" : " secs",
      "privacy-sendraw-option" : "Send raw",
      "privacy-sendhashed-option" : "Send hashed",
      "privacy-dontsend-option" : "Don't send",
      "filename-privacy-label" : "Filename information:",
      "filesize-privacy-label" : "File size information:",
      "checkforupdatesautomatically-label" : "Check for Syncplay updates automatically",
      "slowondesync-label" : "Slow down on minor desync (not supported on MPC-HC)",
      "rewindondesync-label" : "Rewind on major desync (recommended)",
      "fastforwardondesync-label" : "Fast-forward if lagging behind (recommended)",
      "dontslowdownwithme-label" : "Never slow down or rewind others (experimental)",
      "pauseonleave-label" : "Pause when user leaves (e.g. if they are disconnected)",
      "readyatstart-label" : "Set me as 'ready to watch' by default",
      "forceguiprompt-label" : "Don't always show the Syncplay configuration window", # (Inverted)
      "nostore-label" : "Don't store this configuration", # (Inverted)
      "showosd-label" : "Enable OSD Messages",

      "showosdwarnings-label" : "Include warnings (e.g. when files are different, users not ready)",
      "showsameroomosd-label" : "Include events in your room",
      "shownoncontrollerosd-label" : "Include events from non-operators in managed rooms",
      "showdifferentroomosd-label" : "Include events in other rooms",
      "showslowdownosd-label" :"Include slowing down / reverting notifications",
      "language-label" : "Language:",
      "automatic-language" : "Default ({})", # Default language
      "showdurationnotification-label" : "Warn about media duration mismatches",
      "basics-label" : "Basics",
      "readiness-label" : u"Play/Pause",
      "misc-label" : u"Misc",
      "core-behaviour-title" : "Core room behaviour",
      "syncplay-internals-title" : u"Syncplay internals",
      "syncplay-mediasearchdirectories-title" : u"Directories to search for media (one path per line)",
      "sync-label" : "Sync",
      "sync-otherslagging-title" : "If others are lagging behind...",
      "sync-youlaggging-title" : "If you are lagging behind...",
      "messages-label" : "Messages",
      "messages-osd-title" : "On-screen Display settings",
      "messages-other-title" : "Other display settings",
      "privacy-label" : "Privacy", # Currently unused, but will be brought back if more space is needed in Misc tab
      "privacy-title" : "Privacy settings",
      "unpause-title" : u"If you press play, set as ready and:",
      "unpause-ifalreadyready-option" : u"Unpause if already set as ready",
      "unpause-ifothersready-option" : u"Unpause if already ready or others in room are ready (default)",
      "unpause-ifminusersready-option" : u"Unpause if already ready or if all others ready and min users ready",
      "unpause-always" : u"Always unpause",

      "help-label" : "Help",
      "reset-label" : "Restore defaults",
      "run-label" : "Run Syncplay",
      "storeandrun-label" : "Store configuration and run Syncplay",

      "contact-label" : "Feel free to e-mail <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a>, chat via the <a href=\"https://webchat.freenode.net/?channels=#syncplay\"><nobr>#Syncplay IRC channel</nobr></a> on irc.freenode.net, <a href=\"https://github.com/Uriziel/syncplay/issues\"><nobr>raise an issue</nobr></a> via GitHub, <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>like us on Facebook</nobr></a>, <a href=\"https://twitter.com/Syncplay/\"><nobr>follow us on Twitter</nobr></a>, or visit <a href=\"http://syncplay.pl/\"><nobr>http://syncplay.pl/</nobr></a>",

      "joinroom-menu-label" : "Join room",
      "seektime-menu-label" : "Seek to time",
      "undoseek-menu-label" : "Undo seek",
      "play-menu-label" : "Play",
      "pause-menu-label" : "Pause",
      "playbackbuttons-menu-label" : u"Show playback buttons",
      "autoplay-menu-label" : u"Show auto-play button",
      "autoplay-guipushbuttonlabel" : u"Play when all ready",
      "autoplay-minimum-label" : u"Min users:",

      "ready-guipushbuttonlabel" : u"I'm ready to watch!",

      "roomuser-heading-label" : "Room / User",
      "size-heading-label" : "Size",
      "duration-heading-label" : "Length",
      "filename-heading-label" : "Filename",
      "notifications-heading-label" : "Notifications",
      "userlist-heading-label" : "List of who is playing what",

      "browseformedia-label" : "Browse for media files",

      "file-menu-label" : "&File", # & precedes shortcut key
      "openmedia-menu-label" : "&Open media file",
      "openstreamurl-menu-label" : "Open &media stream URL",
      "exit-menu-label" : "E&xit",
      "advanced-menu-label" : "&Advanced",
      "window-menu-label" : "&Window",
      "setoffset-menu-label" : "Set &offset",
      "createcontrolledroom-menu-label" : "&Create managed room",
      "identifyascontroller-menu-label" : "&Identify as room operator",

      "playback-menu-label" : u"&Playback",

      "help-menu-label" : "&Help",
      "userguide-menu-label" : "Open user &guide",
      "update-menu-label" : "Check for &update",

      "setoffset-msgbox-label" : "Set offset",
      "offsetinfo-msgbox-label" : "Offset (see http://syncplay.pl/guide/ for usage instructions):",

      "promptforstreamurl-msgbox-label" : "Open media stream URL",
      "promptforstreamurlinfo-msgbox-label" : "Stream URL",

      "createcontrolledroom-msgbox-label" : "Create managed room",
      "controlledroominfo-msgbox-label" : "Enter name of managed room\r\n(see http://syncplay.pl/guide/ for usage instructions):",

      "identifyascontroller-msgbox-label" : "Identify as room operator",
      "identifyinfo-msgbox-label" : "Enter operator password for this room\r\n(see http://syncplay.pl/guide/ for usage instructions):",

      "public-server-msgbox-label" : u"Select the public server for this viewing session",

      "megabyte-suffix" : " MB",

      # Tooltips

      "host-tooltip" : "Hostname or IP to connect to, optionally including port (e.g. syncplay.pl:8999). Only synchronised with people on same server/port.",
      "name-tooltip" : "Nickname you will be known by. No registration, so can easily change later. Random name generated if none specified.",
      "password-tooltip" : "Passwords are only needed for connecting to private servers.",
      "room-tooltip" : "Room to join upon connection can be almost anything, but you will only be synchronised with people in the same room.",

      "executable-path-tooltip" : "Location of your chosen supported media player (MPC-HC, VLC, mplayer2 or mpv).",
      "media-path-tooltip" : "Location of video or stream to be opened. Necessary for mpv and mplayer2.",
      "player-arguments-tooltip" : "Additional command line arguments / switches to pass on to this media player.",
      "mediasearcdirectories-arguments-tooltip" : u"Directories where Syncplay will search for media files, e.g. when you are using the click to switch feature. Syncplay will look recursively through sub-folders.",

      "more-tooltip" : "Display less frequently used settings.",
      "filename-privacy-tooltip" : "Privacy mode for sending currently playing filename to server.",
      "filesize-privacy-tooltip" : "Privacy mode for sending size of currently playing file to server.",
      "privacy-sendraw-tooltip" : "Send this information without obfuscation. This is the default option with most functionality.",
      "privacy-sendhashed-tooltip" : "Send a hashed version of the information, making it less visible to other clients.",
      "privacy-dontsend-tooltip" : "Do not send this information to the server. This provides for maximum privacy.",
      "checkforupdatesautomatically-tooltip" : "Regularly check with the Syncplay website to see whether a new version of Syncplay is available.",
      "slowondesync-tooltip" : "Reduce playback rate temporarily when needed to bring you back in sync with other viewers. Not supported on MPC-HC.",
      "dontslowdownwithme-tooltip" : "Means others do not get slowed down or rewinded if your playback is lagging. Useful for room operators.",
      "pauseonleave-tooltip" : "Pause playback if you get disconnected or someone leaves from your room.",
      "readyatstart-tooltip" : "Set yourself as 'ready' at start (otherwise you are set as 'not ready' until you change your readiness state)",
      "forceguiprompt-tooltip" : "Configuration dialogue is not shown when opening a file with Syncplay.", # (Inverted)
      "nostore-tooltip" : "Run Syncplay with the given configuration, but do not permanently store the changes.", # (Inverted)
      "rewindondesync-tooltip" : "Jump back when needed to get back in sync. Disabling this option can result in major desyncs!",
      "fastforwardondesync-tooltip" : "Jump forward when out of sync with room operator (or your pretend position if 'Never slow down or rewind others' enabled).",
      "showosd-tooltip" : "Sends Syncplay messages to media player OSD.",
      "showosdwarnings-tooltip" : "Show warnings if playing different file, alone in room, users not ready, etc.",
      "showsameroomosd-tooltip" : "Show OSD notifications for events relating to room user is in.",
      "shownoncontrollerosd-tooltip" : "Show OSD notifications for events relating to non-operators who are in managed rooms.",
      "showdifferentroomosd-tooltip" : "Show OSD notifications for events relating to room user is not in.",
      "showslowdownosd-tooltip" : "Show notifications of slowing down / reverting on time difference.",
      "showdurationnotification-tooltip" : "Useful for when a segment in a multi-part file is missing, but can result in false positives.",
      "language-tooltip" : u"Language to be used by Syncplay.",
      "unpause-always-tooltip" : u"If you press unpause it always sets you as ready and unpause, rather than just setting you as ready.",
      "unpause-ifalreadyready-tooltip" : u"If you press unpause when not ready it will set you as ready - press unpause again to unpause.",
      "unpause-ifothersready-tooltip" : u"If you press unpause when not ready, it will only upause if others are ready.",
      "unpause-ifminusersready-tooltip" : u"If you press unpause when not ready, it will only upause if others are ready and minimum users threshold is met.",

      "help-tooltip" : "Opens the Syncplay.pl user guide.",
      "reset-tooltip" : "Reset all settings to the default configuration.",
      "update-server-list-tooltip" : u"Connect to syncplay.pl to update list of public servers.",

      "joinroom-tooltip" : "Leave current room and joins specified room.",
      "seektime-msgbox-label" : "Jump to specified time (in seconds / min:sec). Use +/- for relative seek.",
      "ready-tooltip" : "Indicates whether you are ready to watch.",
      "autoplay-tooltip" : "Auto-play when all users who have readiness indicator are ready and minimum user threshold met.",
      "switch-to-file-tooltip" : "Double click to switch to {}", # Filename

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
      "no-salt-notification" : "PLEASE NOTE: To allow room operator passwords generated by this server instance to still work when the server is restarted, please add the following command line argument when running the Syncplay server in the future: --salt {}", #Salt


      # Server arguments
      "server-argument-description" : 'Solution to synchronize playback of multiple MPlayer and MPC-HC instances over the network. Server instance',
      "server-argument-epilog" : 'If no options supplied _config values will be used',
      "server-port-argument" : 'server TCP port',
      "server-password-argument" : 'server password',
      "server-isolate-room-argument" : 'should rooms be isolated?',
      "server-salt-argument" : "random string used to generate managed room passwords",
      "server-disable-ready-argument" : u"disable readiness feature",
      "server-motd-argument": "path to file from which motd will be fetched",
      "server-messed-up-motd-unescaped-placeholders": "Message of the Day has unescaped placeholders. All $ signs should be doubled ($$).",
      "server-messed-up-motd-too-long": "Message of the Day is too long - maximum of {} chars, {} given.",

      # Server errors
      "unknown-command-server-error" : "Unknown command {}",  # message
      "not-json-server-error" : "Not a json encoded string {}",  # message
      "not-known-server-error" : "You must be known to server before sending this command",
      "client-drop-server-error" : "Client drop: {} -- {}",  # host, error
      "password-required-server-error" : "Password required",
      "wrong-password-server-error" : "Wrong password supplied",
      "hello-server-error" : "Not enough Hello arguments",
      }

ru = {
      "LANGUAGE" : u"Русский", #  (Russian)

      # Client notifications
      "config-cleared-notification" : u"Настройки сброшены. Изменения вступят в силу при сохранении корректной конфигурации.",

      "relative-config-notification" : u"Загружен(ы) файл(ы) относительной конфигурации: {}",

      "connection-attempt-notification" : u"Подключение к {}:{}",  # Port, IP
      "reconnection-attempt-notification" : u"Соединение с сервером потеряно, переподключение",
      "disconnection-notification" : u"Отключились от сервера",
      "connection-failed-notification" : u"Не удалось подключиться к серверу",
      "connected-successful-notification" : u"Соединение с сервером установлено",
      "retrying-notification" : u"%s, следующая попытка через %d секунд(ы)...",  # Seconds

      "rewind-notification" : u"Перемотано из-за разницы во времени с <{}>",  # User
      "fastforward-notification" : u"Ускорено из-за разницы во времени с <{}>",  # User
      "slowdown-notification" : u"Воспроизведение замедлено из-за разницы во времени с <{}>",  # User
      "revert-notification" : u"Возвращаемся к нормальной скорости воспроизведения",

      "pause-notification" : u"<{}> приостановил(а) воспроизведение",  # User
      "unpause-notification" : u"<{}> возобновил(а) воспроизведение",  # User
      "seek-notification" : u"<{}> перемотал с {} на {}",  # User, from time, to time

      "current-offset-notification" : u"Текущее смещение: {} секунд(ы)",  # Offset

      "room-join-notification" : u"<{}> зашел(зашла) в комнату: '{}'",  # User
      "left-notification" : u"<{}> покинул(а) комнату",  # User
      "left-paused-notification" : u"<{}> покинул(а) комнату, <{}> приостановил(а) воспроизведение",  # User who left, User who paused
      "playing-notification" : u"<{}> включил '{}' ({})",  # User, file, duration
      "playing-notification/room-addendum" : u" в комнате: '{}'",  # Room

      "not-all-ready" : u"Не готовы: {}", # Usernames
      "all-users-ready" : u"Все пользователи готовы ({} чел.)", #Number of ready users
      "ready-to-unpause-notification" : u"Вы помечены как готовый - нажмите еще раз, чтобы продолжить воспроизведение",
      "set-as-ready-notification" : u"Вы помечены как готовый",
      "set-as-not-ready-notification" : u"Вы помечены как неготовый",
      "autoplaying-notification" : u"Автовоспроизведение через {}...",  # Number of seconds until playback will start

      "identifying-as-controller-notification" : u"Идентификация как оператора комнаты с паролем '{}'...",
      "failed-to-identify-as-controller-notification" : u"<{}> не прошел идентификацию в качестве оператора комнаты.",
      "authenticated-as-controller-notification" : u"<{}> вошел как оператор комнаты.",
      "created-controlled-room-notification" : u"Создана управляемая комната '{}' с паролем '{}'. Сохраните эти данные!", # RoomName, operatorPassword

      "file-different-notification" : u"Вероятно, файл, который Вы смотрите, отличается от того, который смотрит <{}>.",  # User
      "file-differences-notification" : u"Ваш файл отличается: {}", # Differences
      "room-file-differences" : u"Несовпадения файла: {}", # File differences (filename, size, and/or duration)
      "file-difference-filename" : u"имя",
      "file-difference-filesize" : u"размер",
      "file-difference-duration" : u"длительность",
      "alone-in-the-room" : u"В этой комнате кроме Вас никого нет.",

      "different-filesize-notification" : u" (размер Вашего файла не совпадает с размером их файла!)",
      "userlist-playing-notification" : u"{} смотрит:", #Username
      "file-played-by-notification" : u"Файл: {} просматривают:",  # File
      "no-file-played-notification" : u"{} не смотрит ничего", # Username
      "notplaying-notification" : u"Люди, которые не смотрят ничего:",
      "userlist-room-notification" : u"В комнате '{}':",  # Room
      "userlist-file-notification" : u"Файл",
      "controller-userlist-userflag" : u"Оператор",
      "ready-userlist-userflag" : u"Готов",
      
      "update-check-failed-notification" : u"Невозможно автоматически проверить, что версия Syncplay {} все еще актуальна. Хотите зайти на http://syncplay.pl/ и вручную проверить наличие обновлений?",
      "syncplay-uptodate-notification" : u"Syncplay обновлен",
      "syncplay-updateavailable-notification" : u"Доступна новая версия Syncplay. Хотите открыть страницу релиза?",

      "mplayer-file-required-notification" : u"Для использования Syncplay с mplayer необходимо передать файл в качестве параметра",
      "mplayer-file-required-notification/example" : u"Пример использования: syncplay [options] [url|path/]filename",
      "mplayer2-required" : u"Syncplay не совместим с MPlayer 1.x, пожалуйста, используйте mplayer2 или mpv",

      "unrecognized-command-notification" : u"Неизвестная команда.",
      "commandlist-notification" : u"Доступные команды:",
      "commandlist-notification/room" : u"\tr [name] - сменить комнату",
      "commandlist-notification/list" : u"\tl - показать список пользователей",
      "commandlist-notification/undo" : u"\tu - отменить последнюю перемотку",
      "commandlist-notification/pause" : u"\tp - вкл./выкл. паузу",
      "commandlist-notification/seek" : u"\t[s][+-]time - перемотать к заданному моменту времени, если не указан + или -, то время считается абсолютным (от начала файла) в секундах или мин:сек",
      "commandlist-notification/help" : u"\th - помощь",
      "commandlist-notification/toggle" : u"\tt - переключить статус готов/неготов к просмотру",
      "commandlist-notification/create" : u"\tc [name] - создать управляемую комнату с таким же именем, как у текущей",
      "commandlist-notification/auth" : u"\ta [password] - авторизоваться как оператор комнаты с помощью пароля",
      "syncplay-version-notification" : u"Версия Syncplay: {}",  # syncplay.version
      "more-info-notification" : u"Больше информации на {}",  # projectURL

      "gui-data-cleared-notification" : u"Syncplay очистил путь и информацию о состоянии окна, использованного GUI.",
      "language-changed-msgbox-label" : u"Язык переключится при следующем запуске SYncplay.",
      "promptforupdate-label" : u"Вы не против, если Syncplay будет автоматически изредка проверять наличие обновлений?",

      "vlc-version-mismatch" : u"Внимание: Вы используете VLC устаревшей версии {}. К сожалению, Syncplay способен работать с VLC {} и выше.",  # VLC version, VLC min version
      "vlc-interface-version-mismatch" : u"Внимание: В используете модуль интерфейса Syncplay устаревшей версии {} для VLC. К сожалению, Syncplay способен работать с версией {} и выше.",  # VLC interface version, VLC interface min version
      "vlc-interface-oldversion-warning" : u"Внимание: Syncplay обнаружил, что старая версия модуля интерфейса Syncplay для VLC уже установлена в директорию VLC. Пожалуйста, обратитесь к Руководству Пользователя Syncplay (http://syncplay.pl/guide/) за инструкциями о том, как установить syncplay.lua.",
      "vlc-interface-not-installed" : u"Внимание: Модуль интерфейса Syncplay для VLC не обнаружен в директории VLC. По существу, если Вы используете VLC 2.0, то VLC будет использовать модуль syncplay.lua из директории Syncplay, но в таком случае другие пользовательские скрипты и расширения интерфейса не будут работать. Пожалуйста, обратитесь к Руководству Пользователя Syncplay (http://syncplay.pl/guide/) за инструкциями о том, как установить syncplay.lua.",
      "media-player-latency-warning": u"Внимание: У Вашего проигрывателя слишком большой отклик ({} секунд). Если Вы замечаете проблемы с синхронизацией, то закройте ресурсоемкие приложения, а если это не помогло - попробуйте другой проигрыватель.", # Seconds to respond
      "mpv-unresponsive-error": u"mpv has not responded for {} seconds so appears to have malfunctioned. Please restart Syncplay.", # Seconds to respond # TODO: Translate to Russian

      # Client prompts
      "enter-to-exit-prompt" : u"Для выхода нажмите Enter\n",

      # Client errors
      "missing-arguments-error" : u"Некоторые необходимые аргументы отсутствуют, обратитесь к --help",
      "server-timeout-error" : u"Подключение к серверу превысило лимит времени",
      "mpc-slave-error" : u"Невозможно запустить MPC в slave режиме!",
      "mpc-version-insufficient-error" : u"Версия MPC слишком старая, пожалуйста, используйте `mpc-hc` >= `{}`",
      "mpv-version-error" : u"Syncplay не совместим с данной версией mpv. Пожалуйста, используйте другую версию mpv (лучше свежайшую).",
      "player-file-open-error" : u"Проигрыватель не может открыть файл.",
      "player-path-error" : u"Путь к проигрывателю задан неверно.",
      "hostname-empty-error" : u"Имя пользователя не может быть пустым.",
      "empty-error" : u"{} не может быть пустым.",  # Configuration
      "media-player-error" : u"Ошибка проигрывателя: \"{}\"",  # Error line
      "unable-import-gui-error" : u"Невозможно импортировать библиотеки GUI (графического интерфейса). Необходимо установить PySide, иначе графический интерфейс не будет работать.",

      "arguments-missing-error" : u"Некоторые необходимые аргументы отсутствуют, обратитесь к --help",

      "unable-to-start-client-error" : u"Невозможно запустить клиент",

      "player-path-config-error": u"Путь к проигрывателю установлен неверно",
      "no-file-path-config-error" : u"Файл должен быть указан до включения проигрывателя",
      "no-hostname-config-error": u"Имя сервера не может быть пустым",
      "invalid-port-config-error" : u"Неверный номер порта",
      "empty-value-config-error" : u"Поле '{}' не может быть пустым", # Config option

      "not-json-error" : u"Не является закодированной json-строкой\n",
      "hello-arguments-error" : u"Не хватает аргументов Hello\n",
      "version-mismatch-error" : u"Конфликт версий между клиентом и сервером\n",
      "vlc-failed-connection" : u"Ошибка подключения к VLC. Если у Вас не установлен syncplay.lua, то обратитесь к http://syncplay.pl/LUA/ за инструкциями.",
      "vlc-failed-noscript" : u"VLC сообщает, что скрипт интерфейса syncplay.lua не установлен. Пожалуйста, обратитесь к http://syncplay.pl/LUA/ за инструкциями.",
      "vlc-failed-versioncheck" : u"Данная версия VLC не поддерживается Syncplay. Пожалуйста, используйте VLC версии 2 или выше.",
      "vlc-failed-other" : u"Во время загрузки скрипта интерфейса syncplay.lua в VLC произошла следующая ошибка: {}",  # Syncplay Error

      "not-supported-by-server-error" : u"Эта возможность не поддерживается сервером. The feature requires a server running Syncplay {}+, but the server is running Syncplay {}.", #minVersion, serverVersion #TODO: Translate into Russian

      "invalid-seek-value" : u"Некорректное значение для перемотки",
      "invalid-offset-value" : u"Некорректное смещение",

      "switch-file-not-found-error" : u"Невозможно переключиться на файл '{0}'. Syncplay looks in the folder of the currently playing file and specified media directories.", # File not found # TODO: Translate last part into Russian
      "folder-search-timeout-error" : u"The search for media in '{}' was aborted as it took too long. This will occur if you select a folder with too many sub-folders in your list of media folders to search through. Until Syncplay is restarted only the directory of the currently open file will be checked.", #Folder # TODO: Translate into Russian

      "failed-to-load-server-list-error" : u"Failed to load public server list. Please visit http://www.syncplay.pl/ in your browser.", # TODO: Translate into Russian

      # Client arguments
      "argument-description" : u'Решение для синхронного воспроизведения в VLC, MPlayer или MPC-HC через Интернет.',
      "argument-epilog" : u'Если параметр не будет передан, то будет использоваться значение, указанное в _config.',
      "nogui-argument" : u'не использовать GUI',
      "host-argument" : u'адрес сервера',
      "name-argument" : u'желательное имя пользователя',
      "debug-argument" : u'режим отладки',
      "force-gui-prompt-argument" : u'показать окно настройки',
      "no-store-argument" : u'не сохранять данные в .syncplay',
      "room-argument" : u'начальная комната',
      "password-argument" : u'пароль для доступа к серверу',
      "player-path-argument" : u'путь к исполняемому файлу Вашего проигрывателя',
      "file-argument" : u'воспроизводимый файл',
      "args-argument" : u'параметры проигрывателя; если нужно передать параметры, начинающиеся с - , то сначала пишите \'--\'',
      "clear-gui-data-argument" : u'сбрасывает путь и данные о состоянии окна GUI, хранимые как QSettings',
      "language-argument" : u'язык сообщений Syncplay (de/en/ru)',

      "version-argument" : u'выводит номер версии',
      "version-message" : u"Вы используете Syncplay версии {} ({})",

      # Client labels
      "config-window-title" : u"Настройка Syncplay",

      "connection-group-title" : u"Параметры подключения",
      "host-label" : u"Адрес сервера: ",
      "name-label" : u"Имя пользователя (не обязательно):",
      "password-label" : u"Пароль к серверу (если требуется):",
      "room-label" : u"Начальная комната: ",

      "media-setting-title" : u"Параметры проигрывателя",
      "executable-path-label" : u"Путь к проигрывателю:",
      "media-path-label" : u"Путь к видеофайлу:",
      "player-arguments-label" : u"Аргументы для запуска проигрывателя:",
      "browse-label" : u"Выбрать",
      "update-server-list-label" : u"Update list", # TODO: Translate into Russian

      "more-title" : u"Больше настроек",
      "never-rewind-value" : u"Никогда",
      "seconds-suffix" : u" секунд(ы)",
      "privacy-sendraw-option" : u"отпр. как есть",
      "privacy-sendhashed-option" : u"отпр. хэш",
      "privacy-dontsend-option" : u"не отпр.",
      "filename-privacy-label" : u"Имя файла:",
      "filesize-privacy-label" : u"Размер файла:",
      "checkforupdatesautomatically-label" : u"Проверять обновления автоматически",
      "slowondesync-label" : u"Замедлять при небольших рассинхронизациях (не поддерживаетя в MPC-HC)",
      "rewindondesync-label" : u"Перемотка при больших рассинхронизациях (настоятельно рекомендуется)",
      "dontslowdownwithme-label" : u"Никогда не замедлять и не перематывать видео другим (функция тестируется)",
      "pauseonleave-label" : u"Приостанавливать, когда кто-то уходит (например, отключился)",
      "readyatstart-label" : u"Выставить статус 'готово к просмотру' по умолчанию",
      "fastforwardondesync-label" : u"Ускорять видео при отставании (рекомендуется)",
      "forceguiprompt-label" : u"Не показывать больше этот диалог", # (Inverted)
      "nostore-label" : u"Не сохранять текущую конфигурацию", # (Inverted)
      "showosd-label" : u"Включить экранные сообщения (поверх видео)",

      "showosdwarnings-label" : u"Показывать предупреждения (напр., когда файлы не совпадают)",
      "showsameroomosd-label" : u"Показывать события Вашей комнаты",
      "shownoncontrollerosd-label" : u"Включить события, связанные с не-операторами в управляемой комнате.",
      "showdifferentroomosd-label" : u"Показывать события других комнат",
      "showslowdownosd-label" : u"Показывать уведомления о замедлении/перемотке",
      "language-label" : u"Язык:",
      "automatic-language" : u"По умолчанию ({})", # Automatic language
      "showdurationnotification-label" : u"Предупреждать о несовпадении продолжительности видео",
      "basics-label" : u"Основное",
      "readiness-label" : u"Воспроизведение/Пауза", # TODO: Confirm translation of play/pause
      "misc-label" : u"Прочее",
      "core-behaviour-title" : u"Core room behaviour", # TODO: Translate into Russian
      "syncplay-internals-title" : u"Syncplay internals", # TODO: Translate into Russian
      "syncplay-mediasearchdirectories-title" : u"Directories to search for media (one path per line)", # TODO: Translate into Russian
      "sync-label" : u"Синхронизация",
      "sync-otherslagging-title" : u"При отставании других зрителей...",
      "sync-youlaggging-title" : u"Когда я отстаю ...",
      "messages-label" : u"Сообщения",
      "messages-osd-title" : u"Настройки OSD",
      "messages-other-title" : u"Другие настройки отображения",
      "privacy-label" : u"Приватность",
      "privacy-title" : u"Настройки приватности",
      "unpause-title" : u"If you press play, set as ready and:", # TODO: Translate into Russian
      "unpause-ifalreadyready-option" : u"Unpause if already set as ready", # TODO: Translate into Russian
      "unpause-ifothersready-option" : u"Unpause if already ready or others in room are ready (default)", # TODO: Translate into Russian
      "unpause-ifminusersready-option" : u"Unpause if already ready or if all others ready and min users ready", # TODO: Translate into Russian
      "unpause-always" : u"Always unpause", # TODO: Translate into Russian

      "help-label" : u"Помощь",
      "reset-label" : u"Сброс настроек",
      "run-label" : u"Запустить Syncplay",
      "storeandrun-label" : u"Сохранить настройки и зап. Syncplay",

      "contact-label" : u"Есть идея, нашли ошибку или хотите оставить отзыв? Пишите на <a href=\"mailto:dev@syncplay.pl\">dev@syncplay.pl</a>, в <a href=\"https://webchat.freenode.net/?channels=#syncplay\">IRC канал #Syncplay</a> на irc.freenode.net или <a href=\"https://github.com/Uriziel/syncplay/issues\">задавайте вопросы через GitHub</a>. Кроме того, заходите на <a href=\"http://syncplay.pl/\">http://syncplay.pl/</a> за инорфмацией, помощью и обновлениями!",

      "joinroom-menu-label" : u"Зайти в комнату",
      "seektime-menu-label" : u"Перемотать",
      "undoseek-menu-label" : u"Отменить перемотку",
      "play-menu-label" : u"Play",
      "pause-menu-label" : u"Пауза",
      "playbackbuttons-menu-label" : u"Показывать кнопки воспроизведения",
      "autoplay-menu-label" : u"Показывать кнопку автовоспроизведения",
      "autoplay-guipushbuttonlabel" : u"Воспроизвести автоматически, когда все будут готовы",
      "autoplay-minimum-label" : u"Минимум пользователей:",

      "ready-guipushbuttonlabel" : u"Я готов к просмотру!",

      "roomuser-heading-label" : u"Комната / Пользователь",
      "size-heading-label" : u"Размер",
      "duration-heading-label" : u"Длительность",
      "filename-heading-label" : u"Имя файла",
      "notifications-heading-label" : u"Уведомления",
      "userlist-heading-label" : u"Кто что смотрит",

      "browseformedia-label" : u"Выбрать видеофайл",

      "file-menu-label" : u"&Файл", # & precedes shortcut key
      "openmedia-menu-label" : u"&Открыть видеофайл",
      "openstreamurl-menu-label" : u"Открыть URL &потокового вещания",
      "exit-menu-label" : u"&Выход",
      "advanced-menu-label" : u"&Дополнительно",
      "window-menu-label" : u"&Окна",
      "setoffset-menu-label" : u"Установить &смещение",
      "createcontrolledroom-menu-label" : u"&Создать управляемую комнату",
      "identifyascontroller-menu-label" : u"&Войти как оператор комнаты",

      "playback-menu-label" : u"&Воспроизведение",

      "help-menu-label" : u"&Помощь",
      "userguide-menu-label" : u"&Руководство Пользователя",
      "update-menu-label" : u"Проверить &обновления",

      "setoffset-msgbox-label" : u"Установить смещение",
      "offsetinfo-msgbox-label" : u"Смещение (см. инструкцию на странице http://syncplay.pl/guide/):",

      "promptforstreamurl-msgbox-label" : u"Открыть URL потокового вещания",
      "promptforstreamurlinfo-msgbox-label" : u"URL потока",

      "createcontrolledroom-msgbox-label" : u"Создать управляемую комнату",
      "controlledroominfo-msgbox-label" : u"Введите имя управляемой комнаты\r\n(см. инструкцию на странице http://syncplay.pl/guide/):",

      "identifyascontroller-msgbox-label" : u"Войти как оператор комнаты",
      "identifyinfo-msgbox-label" : u"Введите пароль оператора комнаты\r\n(см. инструкцию на странице http://syncplay.pl/guide/):",

      "public-server-msgbox-label" : u"Select the public server for this viewing session", # TODO: Translate into Russian

      "megabyte-suffix" : u" МБ", # Technically it is a mebibyte

      # Tooltips

      "host-tooltip" : u"Имя или IP-адрес, к которому будет произведено подключение, может содержать номер порта (напр., syncplay.pl:8999). Синхронизация возможна только в рамках одного сервера/порта.",
      "name-tooltip" : u"Имя, под которым Вы будете известны. Регистриция не требуется, так что имя пользователя можно легко сменить в любой момент. Будет сгенерировано случайным образом, если не указать.",
      "password-tooltip" : u"Пароли нужны для подключения к приватным серверам.",
      "room-tooltip" : u"Комната, в которую Вы попадете сразу после подключения. Можно не указывать. Синхронизация возможна только между людьми в одной и той же комнате.",

      "executable-path-tooltip" : u"Расположение Вашего видеопроигрывателя (MPC-HC, VLC, mplayer2 или mpv).",
      "media-path-tooltip" : u"Расположение видеофайла или потока для просмотра. Обязательно для mpv и mplayer2.",
      "player-arguments-tooltip" : u"Передавать дополнительные аргументы командной строки этому проигрывателю.",
      "mediasearcdirectories-arguments-tooltip" : u"Directories where Syncplay will search for media files, e.g. when you are using the click to switch feature. Syncplay will look recursively through sub-folders.", # TODO: Translate into Russian

      "more-tooltip" : u"Показать дополнительные настройки.",
      "filename-privacy-tooltip" : u"Режим приватности для передачи имени воспроизводимого файла на сервер.",
      "filesize-privacy-tooltip" : u"Режим приватности для передачи размера воспроизводимого файла на сервер.",
      "privacy-sendraw-tooltip" : u"Отправляет эту информацию без шифрования. Рекомендуемая опция с наибольшей функциональностью.",
      "privacy-sendhashed-tooltip" : u"Отправляет хэш-сумму этой информации, делая ее невидимой для других пользователей.",
      "privacy-dontsend-tooltip" : u"Не отправлять эту информацию на сервер. Предоставляет наибольшую приватность.",
      "checkforupdatesautomatically-tooltip" : u"Syncplay будет регулярно заходить на сайт и проверять наличие новых версий.",
      "slowondesync-tooltip" : u"Временно уменьшить скорость воспроизведения в целях синхронизации с другими зрителями. Не поддерживается в MPC-HC.",
      "dontslowdownwithme-tooltip" : u"Ваши лаги не будут влиять на других зрителей.",
      "pauseonleave-tooltip" : u"Приостановить воспроизведение, если Вы покинули комнату или кто-то из зрителей отключился от сервера.",
      "readyatstart-tooltip" : u"Отметить Вас готовым к просмотру сразу же (по умолчанию Вы отмечены не готовым)",
      "forceguiprompt-tooltip" : u"Окно настройки не будет отображаться при открытии файла в Syncplay.", # (Inverted)
      "nostore-tooltip" : u"Запустить Syncplay с данной конфигурацией, но не сохранять изменения навсегда.", # (Inverted)
      "rewindondesync-tooltip" : u"Перематывать назад, когда это необходимо для синхронизации. Отключение этой опции может привести к большим рассинхронизациям!",
      "fastforwardondesync-tooltip" : u"Перематывать вперед при рассинхронизации с оператором комнаты (или если включена опция 'Никогда не замедлять и не перематывать видео другим').",
      "showosd-tooltip" : u"Отправлять сообщения Syncplay в видеопроигрыватель и отображать их поверх видео (OSD - On Screen Display).",
      "showosdwarnings-tooltip" : u"Показывать OSC-предупреждения, если проигрываются разные файлы или если Вы в комнате больше никого нет.",
      "showsameroomosd-tooltip" : u"Показывать OSD-уведомления о событиях, относящихся к комнате, в которой Вы находитесь.",
      "shownoncontrollerosd-tooltip" : u"Показывать OSD-уведомления о событиях, относящихся к не-операторам в управляемой комнате.",
      "showdifferentroomosd-tooltip" : u"Показывать OSD-уведомления о событиях, относящихся к любым другим комнатам.",
      "showslowdownosd-tooltip" : u"Показывать уведомления о замедлении или перемотке в целях синхронизации.",
      "showdurationnotification-tooltip" : u"Полезно, когда сегмент составного файла отсутствует. Возможны ложные срабатывания.",
      "language-tooltip" : u"Язык, используемый Syncplay.",
      "unpause-always-tooltip" : u"If you press unpause it always sets you as ready and unpause, rather than just setting you as ready.", # TODO: Translate into Russian
      "unpause-ifalreadyready-tooltip" : u"If you press unpause when not ready it will set you as ready - press unpause again to unpause.", # TODO: Translate into Russian
      "unpause-ifothersready-tooltip" : u"If you press unpause when not ready, it will only upause if others are ready.", # TODO: Translate into Russian
      "unpause-ifminusersready-tooltip" : u"If you press unpause when not ready, it will only upause if others are ready and minimum users threshold is met.", # TODO: Translate into Russian

      "help-tooltip" : u"Открыть Руководство Пользователя на Syncplay.pl.",
      "reset-tooltip" : u"Сбрасывает все настройки Syncplay в начальное состояние.",
      "update-server-list-tooltip" : u"Connect to syncplay.pl to update list of public servers.", # TODO: Translate to Russian

      "joinroom-tooltip" : u"Покинуть комнату и зайти в другую, указанную комнату.",
      "seektime-msgbox-label" : u"Перемотать к определенному моменту времени (указывать в секундах или мин:сек). Используйте +/-, чтобы перемотать вперед/назад относительно настоящего момента.",
      "ready-tooltip" : u"Показывает, готовы ли Вы к просмотру или нет.",
      "autoplay-tooltip" : u"Автоматическое воспроизведение, когда все пользователи с индикаторами готовности будут готовы и присутствует достаточное число пользователей.",
      "switch-to-file-tooltip" : u"Double click to switch to {}", # Filename # TODO: Translate to Russian

      # In-userlist notes (GUI)
      "differentsize-note" : u"Размер файла не совпадает!",
      "differentsizeandduration-note" : u"Размер и продолжительность файла не совпадают!",
      "differentduration-note" : u"Продолжительность файла не совпадает!",
      "nofile-note" : u"(Ничего не воспроизводим)",

      # Server messages to client
      "new-syncplay-available-motd-message" : u"<NOTICE> Вы используете Syncplay версии {}. Доступна более новая версия на http://syncplay.pl/ . </NOTICE>",  # ClientVersion

      # Server notifications
      "welcome-server-notification" : u"Добро пожаловать на сервер Syncplay версии {0}",  # version
      "client-connected-room-server-notification" : u"{0}({2}) подключился(-лась) к комнате '{1}'",  # username, host, room
      "client-left-server-notification" : u"{0} покинул(а) сервер",  # name
      "no-salt-notification" : u"ВНИМАНИЕ: Чтобы сгенерированные сервером пароли операторов комнат работали после перезагрузки сервера, необходимо указать следующий аргумент командной строки при запуске сервера Syncplay: --salt {}", #Salt

      # Server arguments
      "server-argument-description" : u'Решение для синхронного воспроизведения в VLC, MPlayer или MPC-HC через Интернет. Серверная часть',
      "server-argument-epilog" : u'Если параметр не будет передан, то будет использоваться значение, указанное в _config.',
      "server-port-argument" : u'номер TCP порта сервера',
      "server-password-argument" : u'пароль к серверу',
      "server-isolate-room-argument" : u'должны ли комнаты быть изолированными?',
      "server-salt-argument" : u"генерировать пароли к управляемым комнатам на основании указанной строки (соли)",
      "server-disable-ready-argument" : u"отключить статусы готов/не готов",
      "server-motd-argument" : u"путь к файлу, из которого будет извлекаться MOTD-сообщение",
      "server-messed-up-motd-unescaped-placeholders" : u"MOTD-сообщение содержит неэкранированные спец.символы. Все знаки $ должны быть продублированы ($$).",
      "server-messed-up-motd-too-long" : u"MOTD-сообщение слишком длинное: максимальная длина - {} символ(ов), текущая длина - {} символ(ов).",

      # Server errors
      "unknown-command-server-error" : u"Неизвестная команда: {}",  # message
      "not-json-server-error" : u"Не является закодированной json-строкой: {}",  # message
      "not-known-server-error" : u"Данную команду могут выполнять только авторизованные пользователи.",
      "client-drop-server-error" : u"Клиент отключен с ошибкой: {} -- {}",  # host, error
      "password-required-server-error" : u"Необходимо указать пароль.",
      "wrong-password-server-error" : u"Указан неверный пароль.",
      "hello-server-error" : u"Не хватает аргументов Hello.",

      }

de = {
      "LANGUAGE" : u"Deutsch", # (German)

      # Client notifications
      "config-cleared-notification" : u"Einstellungen gelöscht. Änderungen werden gespeichert, wenn du eine gültige Konfiguration speicherst.",

      "relative-config-notification" : u"Relative Konfigurationsdatei(en) geladen: {}",

      "connection-attempt-notification" : u"Verbinde mit {}:{}",  # Port, IP
      "reconnection-attempt-notification" : u"Verbindung zum Server verloren, versuche erneut",
      "disconnection-notification" : u"Verbindung zum Server beendet",
      "connection-failed-notification" : u"Verbindung zum Server fehlgeschlagen",
      "connected-successful-notification" : u"Erfolgreich mit Server verbunden",
      "retrying-notification" : u"%s, versuche erneut in %d Sekunden...",  # Seconds

      "rewind-notification" : u"Zurückgespult wegen Zeitdifferenz mit <{}>",  # User
      "fastforward-notification" : u"Vorgespult wegen Zeitdifferenz mit <{}>",  # User
      "slowdown-notification" : u"Verlangsamt wegen Zeitdifferenz mit <{}>",  # User
      "revert-notification" : u"Normalgeschwindigkeit",

      "pause-notification" : u"<{}> pausierte",  # User
      "unpause-notification" : u"<{}> startete",  # User
      "seek-notification" : u"<{}> sprang von {} nach {}",  # User, from time, to time

      "current-offset-notification" : u"Aktueller Offset: {} Sekunden",  # Offset

      "room-join-notification" : u"<{}> hat den Raum '{}' betreten",  # User
      "left-notification" : u"<{}> ist gegangen",  # User
      "left-paused-notification" : u"<{}> ist gegangen, <{}> pausierte",  # User who left, User who paused
      "playing-notification" : u"<{}> spielt '{}' ({})",  # User, file, duration
      "playing-notification/room-addendum" :  u" in Raum: '{}'",  # Room

      "not-all-ready" : u"Noch nicht bereit: {}", # Usernames
      "all-users-ready" : u"Alle sind bereit ({} Nutzer)", #Number of ready users
      "ready-to-unpause-notification" : u"Du bist bereit - noch einmal fortsetzen klicken zum abspielen",
      "set-as-ready-notification" : u"Du bist bereit",
      "set-as-not-ready-notification" : u"Du bist nicht bereit",
      "autoplaying-notification" : u"Starte in {}...", # Number of seconds until playback will start

      "identifying-as-controller-notification" : u"Identifiziere als Raumleiter mit Passwort '{}'...",  # TODO: find a better translation to "room operator"
      "failed-to-identify-as-controller-notification" : u"<{}> konnte sich nicht als Raumleiter identifizieren.",
      "authenticated-as-controller-notification" : u"<{}> authentifizierte sich als Raumleiter",
      "created-controlled-room-notification" : u"Gesteuerten Raum '{}' mit Passwort '{}' erstellt. Bitte diese Informationen für die Zukunft aufheben!", # RoomName, operatorPassword

      "file-different-notification" : u"Deine Datei scheint sich von <{}>s zu unterscheiden",  # User
      "file-differences-notification" : u"Deine Datei unterscheidet sich auf folgende Art: {}",
      "room-file-differences" : u"Unterschiedlich in: {}", # File differences (filename, size, and/or duration)
      "file-difference-filename" : u"Name",
      "file-difference-filesize" : u"Größe",
      "file-difference-duration" : u"Dauer",
      "alone-in-the-room": u"Du bist alleine im Raum",

      "different-filesize-notification" : u" (ihre Dateigröße ist anders als deine!)",
      "userlist-playing-notification" : u"{} spielt:", #Username
      "file-played-by-notification" : u"Datei: {} wird gespielt von:",  # File
      "no-file-played-notification" : u"{} spielt keine Datei ab", # Username
      "notplaying-notification" : u"Personen im Raum, die keine Dateien spielen:",
      "userlist-room-notification" :  u"In Raum '{}':",  # Room
      "userlist-file-notification" : u"Datei",
      "controller-userlist-userflag" : u"Raumleiter",
      "ready-userlist-userflag" : u"Bereit",
      
      "update-check-failed-notification" : u"Konnte nicht automatisch prüfen, ob Syncplay {} aktuell ist. Soll http://syncplay.pl/ geöffnet werden, um manuell nach Updates zu suchen?", #Syncplay version
        "syncplay-uptodate-notification" : u"Syncplay ist aktuell",
      "syncplay-updateavailable-notification" : u"Eine neuere Version von Syncplay ist verfügbar. Soll die Download-Seite geöffnet werden?",

      "mplayer-file-required-notification" : u"Syncplay für mplayer benötigt eine Dateiangabe beim Start",
      "mplayer-file-required-notification/example" : u"Anwendungsbeispiel: syncplay [optionen] [url|pfad/]Dateiname",
      "mplayer2-required" : u"Syncplay ist inkompatibel zu MPlayer 1.x, bitte nutze MPlayer2 oder mpv",

      "unrecognized-command-notification" : u"Unbekannter Befehl",
      "commandlist-notification" : u"Verfügbare Befehle:",
      "commandlist-notification/room" : u"\tr [Name] - Raum ändern",
      "commandlist-notification/list" : u"\tl - Nutzerliste anzeigen",
      "commandlist-notification/undo" : u"\tu - Letzter Zeitsprung rückgängig",
      "commandlist-notification/pause" : u"\tp - Pausieren / weiter",
      "commandlist-notification/seek" : u"\t[s][+-]Zeit - zu einer bestimmten Zeit spulen, ohne + oder - wird als absolute Zeit gewertet; Angabe in Sekunden oder Minuten:Sekunden",
      "commandlist-notification/help" : u"\th - Diese Hilfe",
      "commandlist-notification/toggle" : u"\tt - Bereitschaftsanzeige umschalten",
      "commandlist-notification/create" : u"\tc [name] - erstelle zentral gesteuerten Raum mit dem aktuellen Raumnamen",
      "commandlist-notification/auth" : u"\ta [password] - authentifiziere als Raumleiter mit Passwort",
      "syncplay-version-notification" : u"Syncplay Version: {}",  # syncplay.version
      "more-info-notification" : u"Weitere Informationen auf: {}",  # projectURL

      "gui-data-cleared-notification" : u"Syncplay hat die Pfad und Fensterdaten der Syncplay-GUI zurückgesetzt.",
      "language-changed-msgbox-label" : u"Die Sprache wird geändert, wenn du Syncplay neu startest.",
      "promptforupdate-label" : u"Soll Syncplay regelmäßig nach Updates suchen?",

      "vlc-version-mismatch": u"Warnung: Du nutzt VLC Version {}, aber Syncplay wurde für VLC ab Version {} entwickelt.",  # VLC version, VLC min version
      "vlc-interface-version-mismatch": u"Warnung: Du nutzt Version {} des VLC-Syncplay Interface-Moduls, Syncplay benötigt aber mindestens Version {}.",  # VLC interface version, VLC interface min version
      "vlc-interface-oldversion-warning": u"Warnung: Es ist eine alte Version des Syncplay Interface-Moduls für VLC im VLC-Verzeichnis installiert. In der Syncplay-Anleitung unter http://syncplay.pl/guide/ [Englisch] findest du Details zur Installation des syncplay.lua-Skripts.",
      "vlc-interface-not-installed": u"Warnung: Es wurde kein Syncplay Interface-Modul für VLC im VLC-Verzeichnis gefunden. Daher wird, wenn du VLC 2.0 nutzt, die syncplay.lua die mit Syncplay mitgeliefert wurde, verwendet. Dies bedeutet allerdings, dass keine anderen Interface-Skripts und Erweiterungen geladen werden. In der Syncplay-Anleitung unter http://syncplay.pl/guide/ [Englisch] findest du  Details zur Installation des syncplay.lua-Skripts.",
      "media-player-latency-warning": u"Warnung: Der Mediaplayer brauchte {} Sekunden zum Antworten. Wenn Probleme bei der Synchronisation auftreten, schließe bitte andere Anwendungen, um Ressourcen freizugeben. Sollte das nicht funktionieren, versuche es mit einem anderen Media-Player.", # Seconds to respond
      "mpv-unresponsive-error": u"MPV hat für {} Sekunden nicht geantwortet und scheint abgestürzt zu sein. Bitte starte Syncplay neu.", # Seconds to respond

      # Client prompts
      "enter-to-exit-prompt" : u"Enter drücken zum Beenden\n",

      # Client errors
      "missing-arguments-error" : u"Notwendige Argumente fehlen, siehe --help",
      "server-timeout-error" : u"Timeout: Verbindung zum Server fehlgeschlagen",
       "mpc-slave-error" : u"Kann MPC nicht im Slave-Modus starten!",
       "mpc-version-insufficient-error" : u"MPC-Version nicht ausreichend, bitte nutze `mpc-hc` >= `{}`",
       "mpv-version-error" : u"Syncplay ist nicht kompatibel mit dieser Version von mpv.  Bitte benutze eine andere Version (z.B. Git HEAD).",
       "player-file-open-error" : u"Fehler beim Öffnen der Datei durch den Player",
       "player-path-error" : u"Ungültiger Player-Pfad",
       "hostname-empty-error" : u"Hostname darf nicht leer sein",
       "empty-error" : u"{} darf nicht leer sein",  # Configuration
       "media-player-error": u"Player-Fehler: \"{}\"",  # Error line
       "unable-import-gui-error": u"Konnte die GUI-Bibliotheken nicht importieren. PySide muss installiert sein, damit die grafische Oberfläche funktioniert.",

       "arguments-missing-error" : u"Notwendige Argumente fehlen, siehe --help",

       "unable-to-start-client-error" : u"Client kann nicht gestartet werden",

       "player-path-config-error": u"Player-Pfad ist nicht ordnungsgemäß gesetzt.",
       "no-file-path-config-error": u"Es muss eine Datei ausgewählt werden, bevor der Player gestartet wird.",
       "no-hostname-config-error": u"Hostname darf nicht leer sein",
       "invalid-port-config-error" : u"Port muss gültig sein",
       "empty-value-config-error" : u"{} darf nicht leer sein", # Config option

       "not-json-error" : u"Kein JSON-String\n",
       "hello-arguments-error" : u"Zu wenige Hello-Argumente\n",
       "version-mismatch-error" : u"Verschiedene Versionen auf Client und Server\n",
       "vlc-failed-connection": u"Kann nicht zu VLC verbinden. Wenn du syncplay.lua nicht installiert hast, findest du auf http://syncplay.pl/LUA/ [Englisch] eine Anleitung.",
       "vlc-failed-noscript": u"Laut VLC ist das syncplay.lua Interface-Skript nicht installiert. Auf http://syncplay.pl/LUA/ [Englisch] findest du eine Anleitung.",
       "vlc-failed-versioncheck": u"Diese VLC-Version wird von Syncplay nicht unterstützt. Bitte nutze VLC 2.0",
       "vlc-failed-other" : u"Beim Laden des syncplay.lua Interface-Skripts durch VLC trat folgender Fehler auf: {}",  # Syncplay Error

       "not-supported-by-server-error" : u"Dieses Feature wird vom Server nicht unterstützt. Es wird ein Server mit Syncplay Version {}+ benötigt, aktuell verwendet wird jedoch Version {}.", #minVersion, serverVersion

       "invalid-seek-value" : u"Ungültige Zeitangabe",
       "invalid-offset-value" : u"Ungültiger Offset-Wert",

      "switch-file-not-found-error" : u"Konnte nicht zur Datei '{0}' wechseln. Syncplay sucht im Ordner der aktuellen Datei und angegebenen Medien-Verzeichnissen.", # File not found, folder it was not found in
      "folder-search-timeout-error" : u"Die Suche nach Mediendateien in '{}' wurde abgebrochen weil sie zu lange gedauert hat. Dies tritt auf, wenn ein zu durchsuchender Medienordner zu viele Unterordner hat. Syncplay wird bis zum Neustart nur noch das Verzeichnis der aktuellen Datei durchsuchen.", #Folder

      "failed-to-load-server-list-error" : u"Konnte die Liste der öffentlichen Server nicht laden. Bitte besuche http://www.syncplay.pl/ [Englisch] mit deinem Browser.",

      # Client arguments
      "argument-description" : u'Syncplay ist eine Anwendung um mehrere MPlayer, MPC-HC und VLC-Instanzen über das Internet zu synchronisieren.',
      "argument-epilog" : u'Wenn keine Optionen angegeben sind, werden die _config-Werte verwendet',
      "nogui-argument" : u'Keine GUI anzeigen',
      "host-argument" : u'Server-Adresse',
      "name-argument" : u'Gewünschter Nutzername',
      "debug-argument" : u'Debug-Modus',
      "force-gui-prompt-argument" : u'Einstellungsfenster anzeigen',
      "no-store-argument" : u'keine Werte in .syncplay speichern',
      "room-argument" : u'Standard-Raum',
      "password-argument" : u'Server-Passwort',
      "player-path-argument" : u'Pfad zum Player',
      "file-argument" : u'Abzuspielende Datei',
      "args-argument" : u'Player-Einstellungen; Wenn du Einstellungen, die mit - beginnen, nutzen willst, stelle ein einzelnes \'--\'-Argument davor',
      "clear-gui-data-argument" : u'Setzt die Pfad- und GUI-Fenster-Daten die in den QSettings gespeichert sind zurück',
      "language-argument" : u'Sprache für Syncplay-Nachrichten (de/en/ru)',

      "version-argument" : u'gibt die aktuelle Version aus',
      "version-message" : u"Du verwendest Syncplay v. {} ({})",

      # Client labels
      "config-window-title" : u"Syncplay Konfiguration",

      "connection-group-title" : u"Verbindungseinstellungen",
      "host-label" : u"Server-Adresse:",
      "name-label" :  u"Benutzername (optional):",
      "password-label" :  u"Server-Passwort (falls nötig):",
      "room-label" : u"Standard-Raum:",

      "media-setting-title" : u"Media-Player Einstellungen",
      "executable-path-label" : u"Pfad zum Media-Player:",
      "media-path-label" : u"Pfad zur Datei:",
      "player-arguments-label" : u"Playerparameter:",
      "browse-label" : u"Durchsuchen",
      "update-server-list-label" : u"Liste aktualisieren",

      "more-title" : u"Mehr Einstellungen zeigen",
      "never-rewind-value" : u"Niemals",
      "seconds-suffix" : u" sek",
      "privacy-sendraw-option" : u"Klartext senden",
      "privacy-sendhashed-option" : u"Hash senden",
      "privacy-dontsend-option" : u"Nicht senden",
      "filename-privacy-label" : u"Dateiname:",
      "filesize-privacy-label" : u"Dateigröße:",
      "checkforupdatesautomatically-label" : u"Automatisch nach Updates suchen",
      "slowondesync-label" : u"Verlangsamen wenn nicht synchron (nicht unterstützt mit MPC-HC)",
       "dontslowdownwithme-label" : u"Nie verlangsamen oder andere zurückspulen (Experimentell)",
      "pauseonleave-label" : u"Pausieren wenn ein Benutzer austritt",
      "readyatstart-label" : u"Standardmäßig auf \'Bereit\' stellen",
      "forceguiprompt-label" : u"Diesen Dialog nicht mehr anzeigen",
      "nostore-label" : u"Diese Konfiguration nicht speichern",
      "showosd-label" : u"OSD-Nachrichten anzeigen",

      "showosdwarnings-label" : u"Zeige Warnungen (z.B. wenn Dateien verschieden)",
      "showsameroomosd-label" : u"Zeige Ereignisse in deinem Raum",
      "shownoncontrollerosd-label" : u"Zeige Ereignisse von nicht geführten Räumen in geführten Räumen.",
      "showdifferentroomosd-label" : u"Zeige Ereignisse in anderen Räumen",
      "showslowdownosd-label" : u"Zeige Verlangsamungs/Zurücksetzungs-Benachrichtigung",
      "language-label" : u"Sprache:",
      "automatic-language" : u"Automatisch ({})", # Default language
      "showdurationnotification-label" : u"Zeige Warnung wegen unterschiedlicher Dauer",
      "basics-label" : u"Grundlagen",
      "readiness-label" : u"Play/Pause",
      "misc-label" : u"Diverse",
      "core-behaviour-title" : u"Verhalten des Raumes",
      "syncplay-internals-title" : u"Syncplay intern",
      "syncplay-mediasearchdirectories-title" : u"In diesen Verzeichnissen nach Medien suchen (ein Pfad pro Zeile)",
      "sync-label" : u"Synchronisation",
      "sync-otherslagging-title" : u"Wenn andere laggen...",
      "sync-youlaggging-title" : u"Wenn du laggst...",
      "messages-label" : u"Nachrichten",
      "messages-osd-title" : u"OSD-(OnScreenDisplay)-Einstellungen",
      "messages-other-title" : u"Weitere Display-Einstellungen",
      "privacy-label" : u"Privatsphäre",
      "privacy-title" : u"Privatsphäreneinstellungen",
      "unpause-title" : u"Wenn du Play drückst, auf Bereit setzen und:",
      "unpause-ifalreadyready-option" : u"Wiedergeben wenn bereits als Bereit gesetzt",
      "unpause-ifothersready-option" : u"Wiedergeben wenn bereits als Bereit gesetzt oder alle anderen bereit sind (Standard)",
      "unpause-ifminusersready-option" : u"Wiedergeben wenn bereits als Bereit gesetzt oder die minimale Anzahl anderer Nutzer bereit ist",
      "unpause-always" : u"Immer wiedergeben",

      "help-label" : u"Hilfe",
      "reset-label" : u"Standardwerte zurücksetzen",
      "run-label" : u"Syncplay starten",
      "storeandrun-label" : u"Konfiguration speichern und Syncplay starten",

      "contact-label" : u"Du hast eine Idee, einen Bug gefunden oder möchtest Feedback geben? Sende eine E-Mail an <a href=\"mailto:dev@syncplay.pl\">dev@syncplay.pl</a>, chatte auf dem <a href=\"https://webchat.freenode.net/?channels=#syncplay\">#Syncplay IRC-Kanal</a> auf irc.freenode.net oder <a href=\"https://github.com/Uriziel/syncplay/issues\">öffne eine Fehlermeldung auf GitHub</a>. Außerdem findest du auf <a href=\"http://syncplay.pl/\">http://syncplay.pl/</a> weitere Informationen, Hilfestellungen und Updates.",

      "joinroom-menu-label" : u"Raum beitreten",
      "seektime-menu-label" : u"Spule zu Zeit",
      "undoseek-menu-label" : u"Rückgängig",
      "play-menu-label" : u"Wiedergabe",
      "pause-menu-label" : u"Pause",
      "playbackbuttons-menu-label" : u"Wiedergabesteuerung anzeigen",
      "autoplay-menu-label" : u"Auto-Play-Knopf anzeigen",
      "autoplay-guipushbuttonlabel" : u"Automatisch abspielen wenn alle bereit sind",
      "autoplay-minimum-label" : u"Minimum an Nutzern:",

      "ready-guipushbuttonlabel" : u"Ich bin bereit den Film anzuschauen!",

      "roomuser-heading-label" : u"Raum / Benutzer",
      "size-heading-label" : u"Größe",
      "duration-heading-label" : u"Länge",
      "filename-heading-label" : u"Dateiname",
      "notifications-heading-label" : u"Benachrichtigungen",
      "userlist-heading-label" : u"Liste der gespielten Dateien",

      "browseformedia-label" : u"Nach Mediendateien durchsuchen",

      "file-menu-label" : u"&Datei", # & precedes shortcut key
      "openmedia-menu-label" : u"&Mediendatei öffnen...",
      "openstreamurl-menu-label" : u"&Stream URL öffnen",
      "exit-menu-label" : u"&Beenden",
      "advanced-menu-label" : u"&Erweitert",
      "window-menu-label" : u"&Fenster",
      "setoffset-menu-label" : u"&Offset einstellen",
      "createcontrolledroom-menu-label" : u"&Zentral gesteuerten Raum erstellen",
      "identifyascontroller-menu-label" : u"Als Raumleiter &identifizieren",

      "playback-menu-label" : u"&Wiedergabe",

      "help-menu-label" : u"&Hilfe",
      "userguide-menu-label" : u"&Benutzerhandbuch öffnen",
      "update-menu-label" : u"auf &Aktualisierung prüfen",

      "setoffset-msgbox-label" : u"Offset einstellen",
      "offsetinfo-msgbox-label" : u"Offset (siehe http://syncplay.pl/guide/ für eine Anleitung [Englisch]):",

      "promptforstreamurl-msgbox-label" : u"Stream URL öffnen",
      "promptforstreamurlinfo-msgbox-label" : u"Stream URL",

      "createcontrolledroom-msgbox-label" : u"Zentral gesteuerten Raum erstellen",
      "controlledroominfo-msgbox-label" : u"Namen des zentral gesteuerten Raums eingeben\r\n(siehe http://syncplay.pl/guide/ für eine Anleitung [Englisch]):",

      "identifyascontroller-msgbox-label" : u"Als Raumleiter identifizieren",
      "identifyinfo-msgbox-label" : u"Passwort des zentral gesteuerten Raums eingeben\r\n(siehe http://syncplay.pl/guide/ für eine Anleitung [Englisch]):",

      "public-server-msgbox-label" : u"Einen öffentlichen Server für diese Sitzung auswählen",

      "megabyte-suffix" : u" MB",

      # Tooltips

      "host-tooltip" : u"Hostname oder IP zu der verbunden werden soll. Optional mit Port (z.B.. syncplay.pl:8999). Synchronisation findet nur mit Personen auf dem selben Server und Port statt.",
      "name-tooltip" : u"Dein Benutzername. Keine Registrierung, kann einfach geändert werden. Bei fehlender Angabe wird ein zufälliger Name generiert.",
      "password-tooltip" : u"Passwörter sind nur bei Verbindung zu privaten Servern nötig.",
      "room-tooltip" : u"Der Raum, der betreten werden soll, kann ein x-beliebiger sein. Allerdings werden nur Clients im selben Raum synchronisiert.",

      "executable-path-tooltip" : u"Pfad zum ausgewählten, unterstützten Mediaplayer (MPC-HC, VLC, mplayer2 or mpv).",
      "media-path-tooltip" : u"Pfad zum wiederzugebenden Video oder Stream. Notwendig für mpv und mplayer2.",
      "player-arguments-tooltip" : u"Zusätzliche Kommandozeilenparameter / -schalter für diesen Mediaplayer.",
      "mediasearcdirectories-arguments-tooltip" : u"Verzeichnisse, in denen Syncplay nach Mediendateien suchen soll, z.B. wenn du das Click-to-switch-Feature verwendest. Syncplay wird rekursiv Unterordner durchsuchen.", # TODO: Translate Click-to-switch? (or use as name for feature)

      "more-tooltip" : u"Weitere Einstellungen anzeigen.",
      "filename-privacy-tooltip" : u"Privatheitsmodus beim Senden des Namens der aktuellen Datei zum Server.",
      "filesize-privacy-tooltip" : u"Privatheitsmodus beim Senden der Größe der aktuellen Datei zum Server.",
      "privacy-sendraw-tooltip" : u"Die Information im Klartext übertragen. Dies ist die Standard-Einstellung mit der besten Funktionalität.",
      "privacy-sendhashed-tooltip" : u"Die Informationen gehasht übertragen, um sie für andere Clients schwerer lesbar zu machen.",
      "privacy-dontsend-tooltip" : u"Diese Information nicht übertragen. Dies garantiert den größtmöglichen Datanschutz.",
      "checkforupdatesautomatically-tooltip" : u"Regelmäßig auf der Syncplay-Website nach Updates suchen.",
      "slowondesync-tooltip" : u"Reduziert die Abspielgeschwindigkeit zeitweise, um die Synchronität zu den anderen Clients wiederherzustellen.",
      "rewindondesync-label" : u"Zurückspulen bei großer Zeitdifferenz (empfohlen)",
      "fastforwardondesync-label" : u"Vorspulen wenn das Video laggt (empfohlen)",
      "dontslowdownwithme-tooltip" : u"Lässt andere nicht langsamer werden oder zurückspringen, wenn deine Wiedergabe hängt.",
      "pauseonleave-tooltip" : u"Wiedergabe anhalten, wenn deine Verbindung verloren geht oder jemand den Raum verlässt.",
      "readyatstart-tooltip" : u"Zu Beginn auf 'Bereit' setzen (sonst bist du als 'Nicht Bereit' gesetzt, bis du den Status änderst)",
      "forceguiprompt-tooltip" : u"Der Konfigurationsdialog wird nicht angezeigt, wenn eine Datei mit Syncplay geöffnet wird.",
      "nostore-tooltip" : u"Syncplay mit den angegebenen Einstellungen starten, diese aber nicht dauerhaft speichern.",
      "rewindondesync-tooltip" : u"Zum Wiederherstellen der Synchronität in der Zeit zurückspringen (empfohlen)",
      "fastforwardondesync-tooltip" : u"Nach vorne springen, wenn asynchron zum Raumleiter (oder deine vorgetäuschte Position, falls 'Niemals verlangsamen oder andere zurückspulen' aktiviert ist).",
      "showosd-tooltip" : u"Syncplay-Nachrichten auf dem OSD (= OnScreenDisplay, ein eingeblendetes Textfeld) des Players anzeigen.",
      "showosdwarnings-tooltip" : u"Warnungen bei Unterschiedlichen Dateien oder Alleinsein im Raum anzeigen.",
      "showsameroomosd-tooltip" : u"OSD-Meldungen über Ereignisse im selben Raum anzeigen.",
      "shownoncontrollerosd-tooltip" : u"OSD-Meldungen bei Ereignissen verursacht durch nicht-Raumleiter in zentral gesteuerten Räumen anzeigen.",
      "showdifferentroomosd-tooltip" : u"OSD-Meldungen zu anderen Räumen als dem aktuell betretenen anzeigen.",
      "showslowdownosd-tooltip" : u"Meldungen bei Geschwindigkeitsänderung anzeigen.",
      "showdurationnotification-tooltip" : u"Nützlich, wenn z.B. ein Teil eines mehrteiligen Videos fehlt, kann jedoch auch fehlerhaft anschlagen.",
      "language-tooltip" : u"Die verwendete Sprache von Syncplay",
      "unpause-always-tooltip" : u"Wiedergabe startet immer (anstatt nur den Bereitschaftsstatus zu ändern)",
      "unpause-ifalreadyready-tooltip" : u"Wenn du nicht bereit bist und Play drückst wirst du als bereit gesetzt - zum Starten der Wiedergabe nochmal drücken.",
      "unpause-ifothersready-tooltip" : u"Wenn du Play drückst und nicht bereit bist, wird nur gestartet, wenn alle anderen bereit sind.",
      "unpause-ifminusersready-tooltip" : u"Wenn du Play drückst und nicht bereit bist, wird nur gestartet, wenn die minimale Anzahl anderer Benutzer bereit ist.",

      "help-tooltip" : u"Öffnet Hilfe auf syncplay.pl [Englisch]",
      "reset-tooltip" : u"Alle Einstellungen auf Standardwerte zurücksetzen.",
      "update-server-list-tooltip" : u"Mit syncplay.pl verbinden um die Liste öffentlicher Server zu aktualisieren.",

      "joinroom-tooltip" : u"Den aktuellen Raum verlassen und stattdessen den angegebenen betreten.",
      "seektime-msgbox-label" : u"Springe zur angegebenen Zeit (in Sekunden oder min:sek).  Verwende +/- zum relativen Springen.",
      "ready-tooltip" : u"Zeigt an, ob du bereit zum anschauen bist",
      "autoplay-tooltip" : u"Automatisch abspielen, wenn alle Nutzer bereit sind oder die minimale Nutzerzahl erreicht ist.",
      "switch-to-file-tooltip" : u"Doppelklicken um zu {} zu wechseln", # Filename

      # In-userlist notes (GUI)
      "differentsize-note" : u"Verschiedene Größe!",
      "differentsizeandduration-note" : u"Verschiedene Größe und Dauer!",
      "differentduration-note" : u"Verschiedene Dauer!",
      "nofile-note" : u"(keine Datei wird abgespielt)",

      # Server messages to client
      "new-syncplay-available-motd-message" : u"<NOTICE> Du nutzt Syncplay Version {}, aber es gibt eine neuere Version auf http://syncplay.pl</NOTICE>",  # ClientVersion

      # Server notifications
      "welcome-server-notification" : u"Willkommen zum Syncplay-Server, v. {0}",  # version
      "client-connected-room-server-notification" : u"{0}({2}) hat den Raum '{1}' betreten",  # username, host, room
      "client-left-server-notification" : u"{0} hat den Server verlassen",  # name
      "no-salt-notification" : u"WICHTIGER HINWEIS: Damit von dem Server generierte Passwörter für geführte Räume auch nach einem Serverneustart funktionieren, starte den Server mit dem folgenden Parameter: --salt {}", #Salt

      # Server arguments
      "server-argument-description" : u'Anwendung, um mehrere MPlayer, MPC-HC und VLC-Instanzen über das Internet zu synchronisieren. Server',
      "server-argument-epilog" : u'Wenn keine Optionen angegeben sind, werden die _config-Werte verwendet',
      "server-port-argument" : u'Server TCP-Port',
      "server-password-argument" : u'Server Passwort',
      "server-isolate-room-argument" : u'Sollen die Räume isoliert sein?',
      "server-salt-argument" : u"zufällige Zeichenkette, die zur Erstellung von Passwörtern verwendet wird",
      "server-disable-ready-argument" : u"Bereitschaftsfeature deaktivieren",
      "server-motd-argument": u"Pfad zur Datei, von der die Nachricht des Tages geladen wird",
      "server-messed-up-motd-unescaped-placeholders": u"Die Nachricht des Tages hat unmaskierte Platzhalter. Alle $-Zeichen sollten verdoppelt werden ($$).",
      "server-messed-up-motd-too-long": u"Die Nachricht des Tages ist zu lang - Maximal {} Zeichen, aktuell {}.",

      # Server errors
      "unknown-command-server-error" : u"Unbekannter Befehl {}",  # message
      "not-json-server-error" : u"Kein JSON-String {}",  # message
      "not-known-server-error" : u"Der Server muss dich kennen, bevor du diesen Befehl nutzen kannst",
      "client-drop-server-error" : u"Client verloren: {} -- {}",  # host, error
      "password-required-server-error" : u"Passwort nötig",
      "wrong-password-server-error" : u"Ungültiges Passwort",
      "hello-server-error" : u"Zu wenige Hello-Argumente"
      }

messages = {
           "en": en,
           "ru": ru,
           "de": de,
           "CURRENT": None
           }

def getLanguages():
    langList = {}
    for lang in messages:
        if lang != "CURRENT":
            langList[lang] = getMessage("LANGUAGE", lang)
    return langList

def setLanguage(lang):
    messages["CURRENT"] = lang

def getMissingStrings():
    missingStrings = ""
    for lang in messages:
        if lang != "en" and lang != "CURRENT":
            for message in messages["en"]:
                if not messages[lang].has_key(message):
                    missingStrings = missingStrings + "({}) Missing: {}\n".format(lang, message)
            for message in messages[lang]:
                if not messages["en"].has_key(message):
                    missingStrings = missingStrings + "({}) Unused: {}\n".format(lang, message)

    return missingStrings

def getInitialLanguage():
    import locale
    try:
        initialLanguage = locale.getdefaultlocale()[0].split("_")[0]
        if not messages.has_key(initialLanguage):
            initialLanguage = constants.FALLBACK_INITIAL_LANGUAGE
    except:
        initialLanguage = constants.FALLBACK_INITIAL_LANGUAGE
    return initialLanguage

def isValidLanguage(language):
    return messages.has_key(language)

def getMessage(type_, locale=None):
    if constants.SHOW_TOOLTIPS == False:
        if "-tooltip" in type_:
            return ""

    if not isValidLanguage(messages["CURRENT"]):
        setLanguage(getInitialLanguage())

    lang = messages["CURRENT"]
    if locale and messages.has_key(locale):
        if messages[locale].has_key(type_):
            return unicode(messages[locale][type_])
    if lang and messages.has_key(lang):
        if messages[lang].has_key(type_):
            return unicode(messages[lang][type_])
    if messages["en"].has_key(type_):
        return unicode(messages["en"][type_])
    else:
        raise KeyError(type_)
