# coding:utf8
from syncplay import constants

en = {
      "LANGUAGE" : "English",
      
      # Client notifications
      "config-cleared-notification" : "Settings cleared. Changes will be saved when you store a valid configuration.",

      "relative-config-notification" : "Loaded relative configuration file(s): {}",

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

      "pause-notification" : "<{}> paused",  # User
      "unpause-notification" : "<{}> unpaused",  # User
      "seek-notification" : "<{}> jumped from {} to {}",  # User, from time, to time

      "current-offset-notification" : "Current offset: {} seconds",  # Offset

      "room-join-notification" : "<{}> has joined the room: '{}'",  # User
      "left-notification" : "<{}> has left",  # User
      "left-paused-notification" : "<{}> left, <{}> paused",  # User who left, User who paused
      "playing-notification" : "<{}> is playing '{}' ({})",  # User, file, duration
      "playing-notification/room-addendum" :  " in room: '{}'",  # Room

      "identifying-as-controller-notification" : u"Identifying as room controller with password '{}'...",
      "failed-to-identify-as-controller-notification" : u"<{}> failed to identify as a room controller.",
      "authenticated-as-controller-notification" : u"<{}> authenticated as a room controller",

      "file-different-notification" : "File you are playing appears to be different from <{}>'s",  # User
      "file-differences-notification" : "Your file differs in the following way(s): ", # controlPassword
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
      "commandlist-notification/create" : "\tc [name] - create controlled room using name of current room",
      "commandlist-notification/auth" : "\ta [password] - authenticate as room controller with controller password",
      "syncplay-version-notification" : "Syncplay version: {}",  # syncplay.version
      "more-info-notification" : "More info available at: {}",  # projectURL

      "gui-data-cleared-notification" : "Syncplay has cleared the path and window state data used by the GUI.",
      "language-changed-msgbox-label" : "Language will be changed when you run Syncplay.",

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
       "mpv-version-error" : "Syncplay is not compatible with this version of mpv. Please use a different version of mpv (e.g. Git HEAD).",
       "player-file-open-error" : "Player failed opening file",
       "player-path-error" : "Player path is not set properly",
       "hostname-empty-error" : "Hostname can't be empty",
       "empty-error" : "{} can't be empty",  # Configuration
       "media-player-error": "Media player error: \"{}\"",  # Error line
       "unable-import-gui-error": "Could not import GUI libraries. If you do not have PySide installed then you will need to install it for the GUI to work.",

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
      "language-argument" :'language for Syncplay messages (de/en/pl/ru)',

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
      "browse-label" : "Browse",

      "more-title" : "Show more settings",
      "slowdown-threshold-label" : "Slow down threshold:",
      "rewind-threshold-label" : "Rewind threshold:",
      "fastforward-threshold-label" : "Fast-forward threshold:",
      "never-rewind-value" : "Never",
      "seconds-suffix" : " secs",
      "privacy-sendraw-option" : "Send raw",
      "privacy-sendhashed-option" : "Send hashed",
      "privacy-dontsend-option" : "Don't send",
      "filename-privacy-label" : "Filename information:",
      "filesize-privacy-label" : "File size information:",
      "slowondesync-label" : "Slow down on minor desync (not supported on MPC-HC)",
      "dontslowdownwithme-label" : "Never slow down or rewind others",
      "pauseonleave-label" : "Pause when user leaves (e.g. if they are disconnected)",
      "forceguiprompt-label" : "Don't always show this dialog", # (Inverted)
      "nostore-label" : "Don't store this configuration", # (Inverted)
      "showosd-label" : "Enable OSD Messages",

      "showosdwarnings-label" : "Include warnings (e.g. when files are different)",
      "showsameroomosd-label" : "Include events in your room",
      "showdifferentroomosd-label" : "Include events in other rooms",
      "showslowdownosd-label" :"Include slowing down / reverting notification",
      "showcontactinfo-label" : "Show contact info box",
      "language-label" : "Language",
      "showdurationnotification-label" : "Warn about media duration mismatches",
      "basics-label" : "Basics",
      "sync-label" : "Sync",
      "sync-lagging-title" : "If others are lagging behind...",
      "sync-other-title" : "Other sync options",
      "messages-label" : "Messages",
      "messages-osd-title" : "On-screen Display settings",
      "messages-other-title" : "Other display settings",
      "privacy-label" : "Privacy",
      "privacy-title" : "Privacy settings",

      "help-label" : "Help",
      "reset-label" : "Restore defaults",
      "run-label" : "Run Syncplay",
      "storeandrun-label" : "Store configuration and run Syncplay",

      "contact-label" : "Have an idea, bug report or feedback? E-mail <a href=\"mailto:dev@syncplay.pl\">dev@syncplay.pl</a>, chat via the <a href=\"https://webchat.freenode.net/?channels=#syncplay\">#Syncplay IRC channel</a> on irc.freenode.net or <a href=\"https://github.com/Uriziel/syncplay/issues/new\">raise an issue via GitHub</a>. Also check out <a href=\"http://syncplay.pl/\">http://syncplay.pl/</a> for info, help and updates.",

      "joinroom-guibuttonlabel" : "Join room",
      "seektime-guibuttonlabel" : "Seek to time",
      "undoseek-guibuttonlabel" : "Undo seek",
      "togglepause-guibuttonlabel" : "Toggle pause",
      "play-guibuttonlabel" : "Play",
      "pause-guibuttonlabel" : "Pause",

      "roomuser-heading-label" : "Room / User",
      "size-heading-label" : "Size",
      "duration-heading-label" : "Length",
      "filename-heading-label" : "Filename",
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
      "createcontrolledroom-menu-label" : "&Create controlled room",
      "identifyascontroller-menu-label" : "&Identify as room controller",

      "help-menu-label" : "&Help",
      "userguide-menu-label" : "Open user &guide",

      "setoffset-msgbox-label" : "Set offset",
      "offsetinfo-msgbox-label" : "Offset (see http://syncplay.pl/guide/ for usage instructions):",


      "createcontrolledroom-msgbox-label" : "Create controlled room",
      "controlledroominfo-msgbox-label" : "Enter name of controlled room\r\n(see http://syncplay.pl/guide/ for usage instructions):",

      "identifyascontroller-msgbox-label" : "Identify as Room Controller",
      "identifyinfo-msgbox-label" : "Enter controller password for this room\r\n(see http://syncplay.pl/guide/ for usage instructions):",

      "megabyte-suffix" : " MB",

      # Tooltips

      "host-tooltip" : "Hostname or IP to connect to, optionally including port (e.g. syncplay.pl:8999). Only synchronised with people on same server/port.",
      "name-tooltip" : "Nickname you will be known by. No registration, so can easily change later. Random name generated if none specified.",
      "password-tooltip" : "Passwords are only needed for connecting to private servers.",
      "room-tooltip" : "Room to join upon connection can be almost anything, but you will only be synchronised with people in the same room.",

      "executable-path-tooltip" : "Location of your chosen supported media player (MPC-HC, VLC, mplayer2 or mpv).",
      "media-path-tooltip" : "Location of video or stream to be opened. Necessary for mpv and mplayer2.",

      "more-tooltip" : "Display less frequently used settings.",
      "slowdown-threshold-tooltip" : "Time ahead of slowest client before temporarily reducing playback speed (default: {} secs).".format(constants.DEFAULT_SLOWDOWN_KICKIN_THRESHOLD),
      "rewind-threshold-tooltip" : "Time ahead slowest client before seeking to get back in sync (default: {} secs).".format(constants.DEFAULT_REWIND_THRESHOLD),
      "fastforward-threshold-tooltip" : "Time behind room controller before seeking to get back in sync (default: {} secs).".format(constants.DEFAULT_FASTFORWARD_THRESHOLD),
      "filename-privacy-tooltip" : "Privacy mode for sending currently playing filename to server.",
      "filesize-privacy-tooltip" : "Privacy mode for sending size of currently playing file to server.",
      "privacy-sendraw-tooltip" : "Send this information without obfuscation. This is the default option with most functionality.",
      "privacy-sendhashed-tooltip" : "Send a hashed version of the information, making it less visible to other clients.",
      "privacy-dontsend-tooltip" : "Do not send this information to the server. This provides for maximum privacy.",
      "slowondesync-tooltip" : "Reduce playback rate temporarily when needed to bring you back in sync with other viewers. Not supported on MPC-HC.",
      "dontslowdownwithme-tooltip" : "Means others do not get slowed down or rewinded if your playback is lagging. Useful for room controllers.",
      "pauseonleave-tooltip" : "Pause playback if you get disconnected or someone leaves from your room.",
      "rewindondesync-label" : "Rewind on major desync (highly recommended)",
      "fastforwardondesync-label" : "Fast-forward if lagging behind room controller (recommended)",
      "forceguiprompt-tooltip" : "Configuration dialogue is not shown when opening a file with Syncplay.", # (Inverted)
      "nostore-tooltip" : "Run Syncplay with the given configuration, but do not permanently store the changes.", # (Inverted)
      "rewindondesync-tooltip" : "Jump back when needed to get back in sync. Disabling this option can result in major desyncs!",
      "fastforwardondesync-tooltip" : "Jump forward when needed to get back in sync. Disabling this option can result in major desyncs!",
      "showosd-tooltip" : "Sends Syncplay messages to media player OSD.",
      "showosdwarnings-tooltip" : "Show warnings if playing different file, alone in room.",
      "showsameroomosd-tooltip" : "Show OSD notifications for events relating to room user is in.",
      "showdifferentroomosd-tooltip" : "Show OSD notifications for events relating to room user is not in.",
      "showslowdownosd-tooltip" :"Show notifications of slowing down / reverting on time difference.",
      "showcontactinfo-tooltip" : "Show information box about contacting Syncplay developers in main Syncplay window.",
      "showbuttonlabels-tooltip" : "Show the text alongside the icons for buttons in the main UI.",
      "showtooltips-tooltip" : "Show tooltip help messages when you mouseover an input element in Syncplay.",
      "showdurationnotification-tooltip" : "Useful for when a segment in a multi-part file is missing, but can result in false positives.",
      "language-tooltip" : u"Language to be used by Syncplay.",

      "help-tooltip" : "Opens the Syncplay.pl user guide.",
      "reset-tooltip" : "Reset all settings to the default configuration.",

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
      "no-salt-notification" : "PLEASE NOTE: To allow room control passwords generated by this server instance to still work when the server is restarted, please add the following command line argument when running the Syncplay server in the future: --salt {}", #Salt


      # Server arguments
      "server-argument-description" : 'Solution to synchronize playback of multiple MPlayer and MPC-HC instances over the network. Server instance',
      "server-argument-epilog" : 'If no options supplied _config values will be used',
      "server-port-argument" : 'server TCP port',
      "server-password-argument" : 'server password',
      "server-isolate-room-argument" : 'should rooms be isolated?',
      "server-salt-argument" : "random string used to generate controlled room passwords",
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

pl = {

      "LANGUAGE" : "Polski", # (Polish)

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

      "file-different-notification" : u"Вероятно, файл, который Вы смотрите, отличается от того, который смотрит <{}>.",  # User
      "file-differences-notification" : u"Ваш файл отличается: ",
      "room-files-not-same" : u"Не все пользователи в этой комнате смотрят один и тот же файл.",
      "alone-in-the-room" : u"В этой комнате кроме Вас никого нет.",

      "different-filesize-notification" : u" (размер Вашего файла не совпадает с размером их файла!)",
      "file-played-by-notification" : u"Файл: {} просматривают:",  # File
      "notplaying-notification" : u"Люди, которые не смотрят ничего:",
      "userlist-room-notification" : u"В комнате '{}':",  # Room

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
      "syncplay-version-notification" : u"Версия Syncplay: {}",  # syncplay.version
      "more-info-notification" : u"Больше информации на {}",  # projectURL

      "gui-data-cleared-notification" : u"Syncplay очистил путь и информацию о состоянии окна, использованного GUI.",

      "vlc-version-mismatch" : u"Внимание: Вы используете VLC устаревшей версии {}. К сожалению, Syncplay способен работать с VLC {} и выше.",  # VLC version, VLC min version
      "vlc-interface-version-mismatch" : u"Внимание: В используете модуль интерфейса Syncplay устаревшей версии {} для VLC. К сожалению, Syncplay способен работать с версией {} и выше.",  # VLC interface version, VLC interface min version
      "vlc-interface-oldversion-ignored" : u"Внимание: Syncplay обнаружил, что старая версия модуля интерфейса Syncplay для VLC уже установлена в директорию VLC. По существу, если Вы используете VLC 2.0, то предпочтение будет отдано файлу syncplay.lua, содержащемуся в директории Syncplay, но в таком случае другие пользовательские скрипты и расширения интерфейса не будут работать. Пожалуйста, обратитесь к Руководству Пользователя Syncplay (http://syncplay.pl/guide/) за инструкциями о том, как установить syncplay.lua.",
      "vlc-interface-not-installed" : u"Внимание: Модуль интерфейса Syncplay для VLC не обнаружен в директории VLC. По существу, если Вы используете VLC 2.0, то VLC будет использовать модуль syncplay.lua из директории Syncplay, но в таком случае другие пользовательские скрипты и расширения интерфейса не будут работать. Пожалуйста, обратитесь к Руководству Пользователя Syncplay (http://syncplay.pl/guide/) за инструкциями о том, как установить syncplay.lua.",

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
      "media-player-error" : u"Ошибка Media player: \"{}\"",  # Error line
      "unable-import-gui-error" : u"Невозможно импортировать библиотеки GUI (графического интерфейса). Необходимо установить PySide, иначе графический интерфейс не будет работать.",

      "arguments-missing-error" : u"Некоторые необходимые аргументы отсутствуют, обратитесь к --help",

      "unable-to-start-client-error" : u"Невозможно запустить клиент",

      "not-json-error" : u"Не является закодированной json-строкой\n",
      "hello-arguments-error" : u"Не хватает аргументов Hello\n",
      "version-mismatch-error" : u"Конфликт версий между клиентом и сервером\n",
      "vlc-failed-connection" : u"Ошибка подключения к VLC. Если у Вас не установлен syncplay.lua, то обратитесь к http://syncplay.pl/LUA/ за инструкциями.",
      "vlc-failed-noscript" : u"VLC сообщает, что скрипт интерфейса syncplay.lua не установлен. Пожалуйста, обратитесь к http://syncplay.pl/LUA/ за инструкциями.",
      "vlc-failed-versioncheck" : u"Данная версия VLC не поддерживается Syncplay. Пожалуйста, используйте VLC версии 2 или выше.",
      "vlc-failed-other" : u"Во время загрузки скрипта интерфейса syncplay.lua в VLC произошла следующая ошибка: {}",  # Syncplay Error

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
      "language-argument" : u'язык сообщений Syncplay (en/pl/ru)',

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
      "browse-label" : u"Выбрать",

      "more-title" : u"Больше настроек",
      "slowdown-threshold-label" : u"Предел для замедления:",
      "rewind-threshold-label" : u"Предел для перемотки:",
      "never-rewind-value" : u"Никогда",
      "seconds-suffix" : u" секунд(ы)",
      "privacy-sendraw-option" : u"отпр. как есть",
      "privacy-sendhashed-option" : u"отпр. хэш",
      "privacy-dontsend-option" : u"не отпр.",
      "filename-privacy-label" : u"Имя файла:",
      "filesize-privacy-label" : u"Размер файла:",
      "slowondesync-label" : u"Замедлять при небольших рассинхронизациях (не поддерживаетя в MPC-HC)",
      "rewindondesync-label" : u"Перемотка при больших рассинхронизациях (настоятельно рекомендуется)",
      "dontslowdownwithme-label" : u"Никогда не замедлять или перематывать видео другим",
      "pauseonleave-label" : u"Приостанавливать, когда кто-то уходит (например, отключился)",
      "forceguiprompt-label" : u"Не показывать больше этот диалог", # (Inverted)
      "nostore-label" : u"Не сохранять текущую конфигурацию", # (Inverted)
      "showosd-label" : u"Включить экранные сообщения (поверх видео)",

      "showosdwarnings-label" : u"Показывать предупреждения (напр., когда файлы не совпадают)",
      "showsameroomosd-label" : u"Показывать события Вашей комнаты",
      "showdifferentroomosd-label" : u"Показывать события других комнат",
      "showslowdownosd-label" : u"Показывать уведомления о замедлении/перемотке",
      "showcontactinfo-label" : u"Отображать контактную информацию разработчиков",
      "showdurationnotification-label" : u"Предупреждать о несовпадении продолжительности видео",
      "basics-label" : u"Основное",
      "sync-label" : u"Синхронизация",
      "messages-label" : u"Сообщения",
      "privacy-label" : u"Приватность",

      "help-label" : u"Помощь",
      "reset-label" : u"Сброс настроек",
      "run-label" : u"Запустить Syncplay",
      "storeandrun-label" : u"Сохранить настройки и зап. Syncplay",

      "contact-label" : u"Есть идея, нашли ошибку или хотите оставить отзыв? Пишите на <a href=\"mailto:dev@syncplay.pl\">dev@syncplay.pl</a>, в <a href=\"https://webchat.freenode.net/?channels=#syncplay\">IRC канал #Syncplay</a> на irc.freenode.net или <a href=\"https://github.com/Uriziel/syncplay/issues/new\">задавайте вопросы через GitHub</a>. Кроме того, заходите на <a href=\"http://syncplay.pl/\">http://syncplay.pl/</a> за инорфмацией, помощью и обновлениями!",

      "joinroom-guibuttonlabel" : u"Зайти в комнату",
      "seektime-guibuttonlabel" : u"Перемотать",
      "undoseek-guibuttonlabel" : u"Отменить перемотку",
      "togglepause-guibuttonlabel" : u"Вкл./выкл. паузу",
      "play-guibuttonlabel" : u"Play",
      "pause-guibuttonlabel" : u"Пауза",

      "roomuser-heading-label" : u"Комната / Пользователь",
      "fileplayed-heading-label" : u"Воспроизводимый файл",
      "notifications-heading-label" : u"Уведомления",
      "userlist-heading-label" : u"Кто что смотрит",
      "othercommands-heading-label" : u"Другие команды",
      "room-heading-label" : u"Комната",
      "seek-heading-label" : u"Перемотка",

      "browseformedia-label" : u"Выбрать видеофайл",

      "file-menu-label" : u"&Файл", # & precedes shortcut key
      "openmedia-menu-label" : u"&Открыть видеофайл",
      "exit-menu-label" : u"&Выход",
      "advanced-menu-label" : u"&Дополнительно",
      "setoffset-menu-label" : u"Установить &смещение",
      "help-menu-label" : u"&Помощь",
      "userguide-menu-label" : u"&Руководство Пользователя",

      "setoffset-msgbox-label" : u"Установить смещение",
      "offsetinfo-msgbox-label" : u"Смещение (см. как использовать на http://syncplay.pl/guide/):",

      # Tooltips

      "host-tooltip" : u"Имя или IP-адрес, к которому будет произведено подключение, может содержать номер порта (напр., syncplay.pl:8999). Синхронизация возможна только в рамках одного сервера/порта.",
      "name-tooltip" : u"Имя, под которым Вы будете известны. Регистриция не требуется, так что имя пользователя можно легко сменить в любой момент. Будет сгенерировано случайным образом, если не указать.",
      "password-tooltip" : u"Пароли нужны для подключения к приватным серверам.",
      "room-tooltip" : u"Комната, в которую Вы попадете сразу после подключения. Можно не указывать. Синхронизация возможна только между людьми в одной и той же комнате.",

      "executable-path-tooltip" : u"Расположение Вашего видеопроигрывателя (MPC-HC, VLC, mplayer2 или mpv).",
      "media-path-tooltip" : u"Расположение видеофайла или потока для просмотра. Обязательно для mpv и mplayer2.",

      "more-tooltip" : u"Показать дополнительные настройки.",
      "slowdown-threshold-tooltip" : u"Отставание самого медленного клиента, необходимое для временного уменьшения скорости видео (по умолчанию: {} сек.).".format(constants.DEFAULT_SLOWDOWN_KICKIN_THRESHOLD),
      "rewind-threshold-tooltip" : u"Отставание самого медленного клиента, необходимое для перемотки назад в целях синхронизации (по умолчанию: {} сек.).".format(constants.DEFAULT_REWIND_THRESHOLD),
      "filename-privacy-tooltip" : u"Режим приватности для передачи имени воспроизводимого файла на сервер.",
      "filesize-privacy-tooltip" : u"Режим приватности для передачи размера воспроизводимого файла на сервер.",
      "privacy-sendraw-tooltip" : u"Отправляет эту информацию без шифрования. Рекомендуемая опция с наибольшей функциональностью.",
      "privacy-sendhashed-tooltip" : u"Отправляет хэш-сумму этой информации, делая ее невидимой для других пользователей.",
      "privacy-dontsend-tooltip" : u"Не отправлять эту информацию на сервер. Предоставляет наибольшую приватность.",
      "slowondesync-tooltip" : u"Временно уменьшить скорость воспроизведения в целях синхронизации с другими зрителями. Не поддерживается в MPC-HC.",
      "dontslowdownwithme-tooltip" : u"Ваши лаги не будут влиять на других зрителей.",
      "pauseonleave-tooltip" : u"Приостановить воспроизведение, если Вы покинули комнату или кто-то из зрителей отключился от сервера.",
      "forceguiprompt-tooltip" : u"Окно настройки не будет отображаться при открытии файла в Syncplay.", # (Inverted)
      "nostore-tooltip" : u"Запустить Syncplay с данной конфигурацией, но не сохранять изменения навсегда.", # (Inverted)
      "rewindondesync-tooltip" : u"Перематывать назад, когда это необходимо для синхронизации. Отключение этой опции может привести к большим рассинхронизациям!",
      "showosd-tooltip" : u"Отправлять сообщения Syncplay в видеопроигрыватель и отображать их поверх видео (OSD - On Screen Display).",
      "showosdwarnings-tooltip" : u"Показывать OSC-предупреждения, если проигрываются разные файлы или если Вы в комнате больше никого нет.",
      "showsameroomosd-tooltip" : u"Показывать OSD-уведомления о событиях, относящихся к комнате, в которой Вы находитесь.",
      "showdifferentroomosd-tooltip" : u"Показывать OSD-уведомления о событиях, относящихся к любым другим комнатам.",
      "showslowdownosd-tooltip" : u"Показывать уведомления о замедлении или перемотке в целях синхронизации.",
      "showcontactinfo-tooltip" : u"Показывать информационных блок с контактной информацией разработчиков Syncplay на главном окне Syncplay.",
      "showbuttonlabels-tooltip" : u"Показывать текст рядом с иконками на кнопках в основном пользовательском интерфейсе.",
      "showtooltips-tooltip" : u"Показывать всплывающие подсказки при наведении мыши на некоторые элементы в окне Syncplay.",
      "showdurationnotification-tooltip" : u"Полезно, когда сегмент составного файла отсутствует. Возможны ложные срабатывания.",

      "help-tooltip" : u"Открыть Руководство Пользователя на Syncplay.pl.",
      "reset-tooltip" : u"Сбрасывает все настройки Syncplay в начальное состояние.",

      "togglepause-tooltip" : u"Приостановить/продолжить просмотр.",
      "play-tooltip" : u"Продолжить просмотр.",
      "pause-tooltip" : u"Приостановить просмотр.",
      "undoseek-tooltip" : u"Перейти к тому месту, которое Вы просматривали до перемотки.",
      "joinroom-tooltip" : u"Покинуть комнату и зайти в другую, указанную комнату.",
      "seektime-tooltip" : u"Перемотать к определенному моменту времени (указывать в секундах или мин:сек). Используйте +/-, чтобы перемотать вперед/назад относительно настоящего момента.",

      # In-userlist notes (GUI)
      "differentsize-note" : u"Размер файла не совпадает!",
      "differentsizeandduration-note" : u"Размер и продолжительность файла не совпадают!",
      "differentduration-note" : u"Продолжительность файла не совпадает!",
      "nofile-note" : u"(Ничего не воспроизводим)",

      # Server messages to client
      "new-syncplay-available-motd-message" : u"<NOTICE> Вы используете Syncplay версии {}. Доступна более новая версия на http://syncplay.pl/ . </NOTICE>",  # ClientVersion
		
      # Server arguments
      "server-argument-description" : u'Решение для синхронного воспроизведения в VLC, MPlayer или MPC-HC через Интернет. Серверная часть',
      "server-argument-epilog" : u'Если параметр не будет передан, то будет использоваться значение, указанное в _config.',
      "server-port-argument" : u'номер TCP порта сервера',
      "server-password-argument" : u'пароль к серверу',
      "server-isolate-room-argument" : u'должны ли комнаты быть изолированными?',
      "server-motd-argument" : u"путь к файлу, из которого будет извлекаться MOTD-сообщение",
      "server-messed-up-motd-unescaped-placeholders" : u"MOTD-сообщение содержит неэкранированные спец.символы. Все знаки $ должны быть продублированы ($$).",
      "server-messed-up-motd-too-long" : u"MOTD-сообщение слишком длинное: максимальная длина - {} символ(ов), текущая длина - {} символ(ов).",
      "server-irc-verbose" : u"Должен ли сервер активно сообщать о всех событиях в комнатах?",
      "server-irc-config" : u"Путь к конфигурационным файлам IRC-бота.",

      # Server errors
      "unknown-command-server-error" : u"Неизвестная команда: {}",  # message
      "not-json-server-error" : u"Не является закодированной json-строкой: {}",  # message
      "not-known-server-error" : u"Данную команду могут выполнять только авторизованные пользователи.",
      "client-drop-server-error" : u"Клиент отключен с ошибкой: {} -- {}",  # host, error
      "password-required-server-error" : u"Необходимо указать пароль.",
      "wrong-password-server-error" : u"Указан неверный пароль.",
      "hello-server-error" : u"Не хватает аргументов Hello.",
      "version-mismatch-server-error" : u"Конфликт версий между клиентом и сервером."

      }

de = {
      "LANGUAGE" : u"Deutsch", # (German)

      # Client notifications
      "relative-config-notification" : u"Relative Konfigurationsdatei(en) geladen: {}",

      "connection-attempt-notification" : u"Versuche zu verbinden nach {}:{}",  # Port, IP
      "reconnection-attempt-notification" : u"Verbindung zum Server verloren, versuche erneut",
      "disconnection-notification" : u"Verbindung zum Server beendet",
      "connection-failed-notification" : u"Verbindung zum Server fehlgeschlagen",
      "connected-successful-notification" : u"Erfolgreich mit Server verbunden",
      "retrying-notification" : u"%s, versuche erneut in %d Sekunden...",  # Seconds

      "rewind-notification" : u"Zurückgespult wegen Zeitdifferenz mit <{}>",  # User
      "slowdown-notification" : u"Verlangsamt wegen Zeitdifferenz mit <{}>",  # User
      "revert-notification" : u"Normalgeschwindigkeit",

      "pause-notification" : u"<{}> pausierte",  # User
      "unpause-notification" : u"<{}> startete",  # User
      "seek-notification" : u"<{}> sprang von {} nach {}",  # User, from time, to time

      "current-offset-notification" : u"Aktueller Offset: {} Sekunden",  # Offset

      "room-join-notification" : u"<{}> hat den Raum '{}' betreten",  # User
      "left-notification" : u"<{}> ist gegangen",  # User
      "playing-notification" : u"<{}> spielt '{}' ({})",  # User, file, duration
      "playing-notification/room-addendum" :  u" in Raum: '{}'",  # Room

      "file-different-notification" : u"Deine Datei scheint sich von <{}>s zu unterscheiden",  # User
      "file-differences-notification" : u"Deine Datei unterscheidet sich auf folgende Art: ",
      "room-files-not-same" : u"Nicht alle Dateien im Raum sind gleich",
      "alone-in-the-room": u"Du bist alleine im Raum",

      "different-filesize-notification" : u" (ihre Dateigröße ist anders als deine!)",
      "file-played-by-notification" : u"Datei: {} wird gespielt von:",  # File
      "notplaying-notification" : u"Personen im Raum, die keine Dateien spielen:",
      "userlist-room-notification" :  u"In Raum '{}':",  # Room

      "mplayer-file-required-notification" : u"Syncplay für mplayer benötigt eine Datei-Angabe beim Start",
      "mplayer-file-required-notification/example" : u"Nutzungsbeispiel: syncplay [optionen] [url|pfad/]dateiname",
      "mplayer2-required" : u"Syncplay ist inkompatibel zu MPlayer 1.x, bitte nutze MPlayer2 oder mpv",

      "unrecognized-command-notification" : u"Unbekannter Befehl",
      "commandlist-notification" : u"Verfügbare Befehle:",
      "commandlist-notification/room" : u"\tr [Name] - Raum ändern",
      "commandlist-notification/list" : u"\tl - Nutzerliste anzeigen",
      "commandlist-notification/undo" : u"\tu - Letzter Zeitsprung rückgängig",
      "commandlist-notification/pause" : u"\tp - Pausieren / weiter",
      "commandlist-notification/seek" : u"\t[s][+-]Zeit - zu einer bestimmten Zeit spulen, ohne + oder - wird als absolute Zeit gewertet; Angabe in Sekungen oder Minuten:Sekunden",
      "commandlist-notification/help" : u"\th - Diese Hilfe",
      "syncplay-version-notification" : u"Syncplay Version: {}",  # syncplay.version
      "more-info-notification" : u"Weitere Informationen auf: {}",  # projectURL

      "gui-data-cleared-notification" : u"Syncplay hat die Pfad und Fensterdaten der Syncplay-GUI zurückgesetzt.",

      "vlc-version-mismatch": u"Warnung: Du nutzt VLC Version {}, aber Syncplay wurde für VLC ab Version {} entwickelt.",  # VLC version, VLC min version
      "vlc-interface-version-mismatch": u"Warnung: Du nutzt Version {} des VLC-Syncplay Interface-Moduls, Syncplay benötigt aber mindestens Version {}.",  # VLC interface version, VLC interface min version
      "vlc-interface-oldversion-ignored": u"Warnung: Syncplay hat bemerkt, dass eine alte Version des Syncplay Interface-Moduls für VLC im VLC-Verzeichnis installiert ist. Daher wird, wenn du VLC 2.0 nutzt, die syncplay.lua die mit Syncplay mitgeliefert wurde, verwendet. Dies bedeutet allerdings, dass keine anderen Interface-Skripts und Erweiterungen geladen werden. In der Syncplay-Anleitung unter http://syncplay.pl/guide/ [Englisch] findest du Details zur Installation des syncplay.lua-Skripts.",
      "vlc-interface-not-installed": u"Warnung: Es wurde kein Syncplay Interface-Modul für VLC im VLC-Verzeichnis gefunden. Daher wird, wenn du VLC 2.0 nutzt, die syncplay.lua die mit Syncplay mitgeliefert wurde, verwendet. Dies bedeutet allerdings, dass keine anderen Interface-Skripts und Erweiterungen geladen werden. In der Syncplay-Anleitung unter http://syncplay.pl/guide/ [Englisch] findest du  Details zur Installation des syncplay.lua-Skripts.",

      # Client prompts
      "enter-to-exit-prompt" : u"Enter drücken zum Beenden\n",

      # Client errors
      "missing-arguments-error" : u"Notwendige Argumente fehlen, siehe --help",
      "server-timeout-error" : u"Timeout: Verbindung zum Server fehlgeschlagen",
       "mpc-slave-error" : u"Kann MPC nicht im Slave-Modus starten!",
       "mpc-version-insufficient-error" : u"MPC-Version nicht ausreichend, bitte nutze `mpc-hc` >= `{}`",
       "player-file-open-error" : u"Fehler beim Öffnen der Datei durch den Player",
       "player-path-error" : u"Ungültiger Player-Pfad",
       "hostname-empty-error" : u"Hostname darf nicht leer sein",
       "empty-error" : u"{} darf nicht leer sein",  # Configuration

       "arguments-missing-error" : u"Notwendige Argumente fehlen, siehe --help",

       "unable-to-start-client-error" : u"Client kann nicht gestartet werden",

       "not-json-error" : u"Kein JSON-String\n",
       "hello-arguments-error" : u"Zu wenige Hello-Argumente\n",
       "version-mismatch-error" : u"Verschiedene Versionen auf Client und Server\n",
       "vlc-error-echo": u"VLC-Fehler: {}",  # VLC error line
       "vlc-unicode-loadfile-error" : u"Die Datei kann nicht durch Syncplay geladen werden, da sie nicht-ASCII Zeichen enthält. Bitte öffne die Datei mit VLC.",
       "vlc-failed-connection": u"Kann nicht zu VLC verbinden. Wenn du syncplay.lua nicht installiert hast, findest du auf http://syncplay.pl/LUA/ für eine Anleitung.",
       "vlc-failed-noscript": u"Laut VLC ist das syncplay.lua Interface-Skript nicht installiert. Auf http://syncplay.pl/LUA/ findest du eine Anleitung.",
       "vlc-failed-versioncheck": u"Diese VLC-Version wird von Syncplay nicht unterstützt. Bitte nutze VLC 2.0",
       "vlc-failed-other" : u"Beim Laden des syncplay.lua Interface-Skripts durch VLC trat folgender Fehler auf: {}",  # Syncplay Error

      # Client arguments
      "argument-description" : u'Anwendung, um mehrere MPlayer, MPC-HC und VLC-Instanzen über das Internet zu synchronisieren.',
      "argument-epilog" : u'Wenn keine Optionen angegeben sind, werden die _config-Werte verwendet',
      "nogui-argument" : u'Keine GUI anzeigen',
      "host-argument" : u'Server\'-Addresse',
      "name-argument" : u'Gewünschter Nutzername',
      "debug-argument" : u'Debug-Modus',
      "force-gui-prompt-argument" : u'Einstellungsfenster anzeigen',
      "no-store-argument" : u'keine Werte in .syncplay speichern',
      "room-argument" : u'Standard-Raum',
      "password-argument" : u'Server-Passwort',
      "player-path-argument" : u'Pfad zum Player',
      "file-argument" : u'Zu spielende Datei',
      "args-argument" : u'Player-Einstellungen; Wenn du Einstellungen, die mit - beginnen, nutzen willst, stelle ein einzelnes \'--\'-Argument davor',
      "clear-gui-data-argument" : u'Setzt die Pfad- und GUI-Fenster-Daten, die in den QSettings gespeichert sind, zurück',

      # Client labels
      "config-window-title" : u"Syncplay Konfiguration",

      "connection-group-title" : u"Verbindungseinstellungen",
      "host-label" : u"Server-Adresse: ",
      "name-label" :  u"Benutzername (optional):",
      "password-label" :  u"Server-Passwort (falls nötig):",
      "room-label" : u"Standard-Raum: ",

      "media-setting-title" : u"Media-Player Einstellungen",
      "executable-path-label" : u"Pfad zum Media-Player:",
      "media-path-label" : u"Pfad zur Datei:",
      "browse-label" : u"Durchsuchen",

      "more-title" : u"Mehr Einstellungen zeigen",
      "privacy-sendraw-option" : u"Klartext senden",
      "privacy-sendhashed-option" : u"Hash senden",
      "privacy-dontsend-option" : u"Nicht senden",
      "filename-privacy-label" : u"Dateiname:",
      "filesize-privacy-label" : u"Dateigröße:",
      "slowdown-label" : u"Verlangsamen wenn nicht synchron",
      "dontslowwithme-label" : u"Nie verlangsamen oder andere zurückspulen",
      "pauseonleave-label" : u"Pausieren wenn ein Benutzer austritt",
      "rewind-label" : u"Zurückspulen bei großer Zeitdifferent (empfohlen)",
      "alwayshow-label" : u"Diesen Dialog immer anzeigen",
      "donotstore-label" : u"Diese Konfiguration nicht speichern",

      "help-label" : u"Hilfe",
      "run-label" : u"Syncplay starten",
      "storeandrun-label" : u"Konfiguration speichern und Syncplay starten",

      "roomuser-heading-label" : u"Raum / Benutzer",
      "fileplayed-heading-label" : u"Gespielte Datei",

      # Tooltips

      "host-tooltip" : u"Hostname oder IP zu der verbunden werden soll. Ptional mit Port (z.B.. syncplay.pl:8999). Synchronisation findet nur mit Personen auf dem selben Server und Port statt.",
      "name-tooltip" : u"Dein Benutzername. Keine Registrierung, kann einfach geändert werden. Bei fehlender Angabe wird ein zufälliger Name generiert.",
      "password-tooltip" : u"Passwörter sind nur bei Verbindung zu privaten Servern nötig.",
      "room-tooltip" : u"Der Raum, der betreten werden soll, kann ein x-beliebiger sein. Allerdings werden nur Clients im selben Raum synchronisiert.",

      "executable-path-tooltip" : u"Pfad zum ausgewählten, unterstützten Mediaplayer (MPC-HC, VLC, mplayer2 or mpv).",
      "media-path-tooltip" : u"Pfad zum wiederzugebenden Video oder Stream. Notwendig für mpv und mplayer2.",

      "more-tooltip" : u"Weitere Einstellungen anzeigen.",
      "filename-privacy-tooltip" : u"Privat-Modus beim senden des Namens der aktuellen Datei zum Server.",
      "filesize-privacy-tooltip" : u"Privat-Modus beim senden der Größe der aktuellen Datei zum Server.",
      "privacy-sendraw-tooltip" : u"Die Information im Klartext übertragen. Dies ist die Standard-Einstellung mit der besten Funktionalität.",
      "privacy-sendhashed-tooltip" : u"Die Informationen gehasht übertragen, um sie für andere Clients schwerer lesbar zu machen.",
      "privacy-dontsend-tooltip" : u"Diese Information nicht übertragen. Dies garantiert den größtmöglichen Datanschutz.",
      "slowdown-tooltip" : u"Reduziert die Abspielgeschwindigkeit zeitweise, um dich wieder synchron zu den anderen Clients zu machen.",
      "dontslowwithme-tooltip" : u"Lässt andere nicht langsamer werden oder zurückspringen, wenn deine Wiedergabe hängt.",
      "pauseonleave-tooltip" : u"Wiedergabe anhalten, wenn deine Verbindung verloren geht oder jemand den Raum verlässt.",
      "rewind-tooltip" : u"In der Zeit zurückspringen zum wiederherstellen der Synchronität. Empfohlen.",
      "alwayshow-tooltip" : u"Der Konfigurations-Dislog wird immer angezeigt. Sogar, wenn du eine Datei mit Syncplay öffnest.",
      "donotstore-tooltip" : u"Syncplay mit den angegebenen Einstellungen starten, diese aber nicht fauerhaft speichern.",

      "help-tooltip" : u"Öffnet Hilfe auf syncplay.pl [Englisch]",

      # Server messages to client
      "new-syncplay-available-motd-message" : u"<NOTICE> Du nutzt Syncplay Version {}, aber es gibt eine neuere Version auf http://syncplay.pl</NOTICE>",  # ClientVersion

      # Server notifications
      "welcome-server-notification" : u"Willkommen zum Syncplay-Server, v. {0}",  # version
      "client-connected-room-server-notification" : u"{0}({2}) hat den Raum '{1}' betreten",  # username, host, room
      "client-left-server-notification" : u"{0} hat den Server verlassen",  # name


      # Server arguments
      "server-argument-description" : u'Anwendung, um mehrere MPlayer, MPC-HC und VLC-Instanzen über das Internet zu synchronisieren. Server',
      "server-argument-epilog" : u'Wenn keine Optionen angegeben sind, werden die _config-Werte verwendet',
      "server-port-argument" : u'Server TCP-Port',
      "server-password-argument" : u'Server Passwort',
      "server-isolate-room-argument" : u'Sollen die Räume isoliert sein?',
      "server-motd-argument": u"Pfad zur Datei, von der die Nachricht des Tages geladen wird",
      "server-messed-up-motd-unescaped-placeholders": u"Die Nachricht des Tages hat unmaskierte Platzhalter. Alle $-Zeichen sollten verdoppelt werden ($$).",
      "server-messed-up-motd-too-long": u"Die Nachricht des Tages ist zu lang - Maximal {} Zeichen, aktuell {}.",
      "server-irc-verbose": u"Soll der Server aktiv über Änderungen in den Räumen informieren",
      "server-irc-config": u"Pfad zu den config-Dateien des irc bot",

      # Server errors
      "unknown-command-server-error" : u"Unbekannter Befehl {}",  # message
      "not-json-server-error" : u"Kein JSON-String {}",  # message
      "not-known-server-error" : u"Der Server muss dich kennen, bevor du diesen Befehl nutzen kannst",
      "client-drop-server-error" : u"Client verloren: {} -- {}",  # host, error
      "password-required-server-error" : u"Passwort nötig",
      "hello-server-error" : u"Zu wenige Hello-Argumente",
      "version-mismatch-server-error" : u"Verschiedene Versionen auf Client und Server",
      "wrong-password-server-error" : u"Ungültiges Passwort"
      }

messages = {
           "en": en,
           "pl": pl,
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

def getMessage(type_, locale=None):
    if constants.SHOW_BUTTON_LABELS == False:
        if "-guibuttonlabel" in type_:
            return ""
    if constants.SHOW_TOOLTIPS == False:
        if "-tooltip" in type_:
            return ""
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
        raise KeyError()
