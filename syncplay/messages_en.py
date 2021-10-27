# coding:utf8

"""English dictionary"""

en = {
    "LANGUAGE": "English",

    # Client notifications
    "config-cleared-notification": "Settings cleared. Changes will be saved when you store a valid configuration.",

    "relative-config-notification": "Loaded relative configuration file(s): {}",

    "connection-attempt-notification": "Attempting to connect to {}:{}",  # Port, IP
    "reconnection-attempt-notification": "Connection with server lost, attempting to reconnect",
    "disconnection-notification": "Disconnected from server",
    "connection-failed-notification": "Connection with server failed",
    "connected-successful-notification": "Successfully connected to server",
    "retrying-notification": "%s, Retrying in %d seconds...",  # Seconds
    "reachout-successful-notification": "Successfully reached {} ({})",

    "rewind-notification": "Rewinded due to time difference with {}",  # User
    "fastforward-notification": "Fast-forwarded due to time difference with {}",  # User
    "slowdown-notification": "Slowing down due to time difference with {}",  # User
    "revert-notification": "Reverting speed back to normal",

    "pause-notification": "{} paused",  # User
    "unpause-notification": "{} unpaused",  # User
    "seek-notification": "{} jumped from {} to {}",  # User, from time, to time

    "current-offset-notification": "Current offset: {} seconds",  # Offset

    "media-directory-list-updated-notification": "Syncplay media directories have been updated.",

    "room-join-notification": "{} has joined the room: '{}'",  # User
    "left-notification": "{} has left",  # User
    "left-paused-notification": "{} left, {} paused",  # User who left, User who paused
    "playing-notification": "{} is playing '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum":  " in room: '{}'",  # Room

    "not-all-ready": "Not ready: {}",  # Usernames
    "all-users-ready": "Everyone is ready ({} users)",  # Number of ready users
    "ready-to-unpause-notification": "You are now set as ready - unpause again to unpause",
    "set-as-ready-notification": "You are now set as ready",
    "set-as-not-ready-notification": "You are now set as not ready",
    "autoplaying-notification": "Auto-playing in {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Identifying as room operator with password '{}'...",
    "failed-to-identify-as-controller-notification": "{} failed to identify as a room operator.",
    "authenticated-as-controller-notification": "{} authenticated as a room operator",
    "created-controlled-room-notification": "Created managed room '{}' with password '{}'. Please save this information for future reference!\n\nIn managed rooms everyone is kept in sync with the room operator(s) who are the only ones who can pause, unpause, seek, and change the playlist.\n\nYou should ask regular viewers to join the room '{}' but the room operators can join the room '{}' to automatically authenticate themselves.",  # RoomName, operatorPassword, roomName, roomName:operatorPassword

    "file-different-notification": "File you are playing appears to be different from {}'s",  # User
    "file-differences-notification": "Your file differs in the following way(s): {}",  # Differences
    "room-file-differences": "File differences: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "name",
    "file-difference-filesize": "size",
    "file-difference-duration": "duration",
    "alone-in-the-room": "You're alone in the room",

    "different-filesize-notification": " (their file size is different from yours!)",
    "userlist-playing-notification": "{} is playing:",  # Username
    "file-played-by-notification": "File: {} is being played by:",  # File
    "no-file-played-notification": "{} is not playing a file",  # Username
    "notplaying-notification": "People who are not playing any file:",
    "userlist-room-notification":  "In room '{}':",  # Room
    "userlist-file-notification": "File",
    "controller-userlist-userflag": "Operator",
    "ready-userlist-userflag": "Ready",

    "update-check-failed-notification": "Could not automatically check whether Syncplay {} is up to date. Want to visit https://syncplay.pl/ to manually check for updates?",  # Syncplay version
    "syncplay-uptodate-notification": "Syncplay is up to date",
    "syncplay-updateavailable-notification": "A new version of Syncplay is available. Do you want to visit the release page?",

    "mplayer-file-required-notification": "Syncplay using mplayer requires you to provide file when starting",
    "mplayer-file-required-notification/example": "Usage example: syncplay [options] [url|path/]filename",
    "mplayer2-required": "Syncplay is incompatible with MPlayer 1.x, please use mplayer2 or mpv",

    "unrecognized-command-notification": "Unrecognized command",
    "commandlist-notification": "Available commands:",
    "commandlist-notification/room": "\tr [name] - change room",
    "commandlist-notification/list": "\tl - show user list",
    "commandlist-notification/undo": "\tu - undo last seek",
    "commandlist-notification/pause": "\tp - toggle pause",
    "commandlist-notification/seek": "\t[s][+-]time - seek to the given value of time, if + or - is not specified it's absolute time in seconds or min:sec",
    "commandlist-notification/offset": "\to[+-]duration - offset local playback by the given duration (in seconds or min:sec) from the server seek position - this is a deprecated feature",
    "commandlist-notification/help": "\th - this help",
    "commandlist-notification/toggle": "\tt - toggles whether you are ready to watch or not",
    "commandlist-notification/create": "\tc [name] - create managed room using name of current room",
    "commandlist-notification/auth": "\ta [password] - authenticate as room operator with operator password",
    "commandlist-notification/chat": "\tch [message] - send a chat message in a room",
    "commandList-notification/queue": "\tqa [file/url] - add file or url to bottom of playlist",
    "commandList-notification/playlist": "\tql - show the current playlist",
    "commandList-notification/select": "\tqs [index] - select given entry in the playlist",
    "commandList-notification/delete": "\tqd [index] - delete the given entry from the playlist",
    "syncplay-version-notification": "Syncplay version: {}",  # syncplay.version
    "more-info-notification": "More info available at: {}",  # projectURL

    "gui-data-cleared-notification": "Syncplay has cleared the path and window state data used by the GUI.",
    "language-changed-msgbox-label": "Language will be changed when you run Syncplay.",
    "promptforupdate-label": "Is it okay for Syncplay to automatically check for updates from time to time?",

    "media-player-latency-warning": "Warning: The media player took {} seconds to respond. If you experience syncing issues then close applications to free up system resources, and if that doesn't work then try a different media player.",  # Seconds to respond
    "mpv-unresponsive-error": "mpv has not responded for {} seconds so appears to have malfunctioned. Please restart Syncplay.",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "Press enter to exit\n",

    # Client errors
    "missing-arguments-error": "Some necessary arguments are missing, refer to --help",
    "server-timeout-error": "Connection with server timed out",
    "mpc-slave-error": "Unable to start MPC in slave mode!",
    "mpc-version-insufficient-error": "MPC version not sufficient, please use `mpc-hc` >= `{}`",
    "mpc-be-version-insufficient-error": "MPC version not sufficient, please use `mpc-be` >= `{}`",
    "mpv-version-error": "Syncplay is not compatible with this version of mpv. Please use a different version of mpv (e.g. Git HEAD).",
    "mpv-failed-advice": "The reason mpv cannot start may be due to the use of unsupported command line arguments or an unsupported version of mpv.",
    "player-file-open-error": "Player failed opening file",
    "player-path-error": "Player path is not set properly. Supported players are: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2, and IINA",
    "hostname-empty-error": "Hostname can't be empty",
    "empty-error": "{} can't be empty",  # Configuration
    "media-player-error": "Media player error: \"{}\"",  # Error line
    "unable-import-gui-error": "Could not import GUI libraries. If you do not have PySide installed then you will need to install it for the GUI to work.",
    "unable-import-twisted-error": "Could not import Twisted. Please install Twisted v16.4.0 or later.",

    "arguments-missing-error": "Some necessary arguments are missing, refer to --help",

    "unable-to-start-client-error": "Unable to start client",

    "player-path-config-error": "Player path is not set properly. Supported players are: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2, and IINA.",
    "no-file-path-config-error": "File must be selected before starting your player",
    "no-hostname-config-error": "Hostname can't be empty",
    "invalid-port-config-error": "Port must be valid",
    "empty-value-config-error": "{} can't be empty",  # Config option

    "not-json-error": "Not a json encoded string\n",
    "hello-arguments-error": "Not enough Hello arguments\n",  # DO NOT TRANSLATE
    "version-mismatch-error": "Mismatch between versions of client and server\n",
    "vlc-failed-connection": "Failed to connect to VLC. If you have not installed syncplay.lua and are using the latest verion of VLC then please refer to https://syncplay.pl/LUA/ for instructions. Syncplay and VLC 4 are not currently compatible, so either use VLC 3 or an alternative such as mpv.",
    "vlc-failed-noscript": "VLC has reported that the syncplay.lua interface script has not been installed. Please refer to https://syncplay.pl/LUA/ for instructions.",
    "vlc-failed-versioncheck": "This version of VLC is not supported by Syncplay.",
    "vlc-initial-warning": 'VLC does not always provide accurate position information to Syncplay, especially for .mp4 and .avi files. If you experience problems with erroneous seeking then please try an alternative media player such as <a href="https://mpv.io/">mpv</a> (or <a href="https://github.com/stax76/mpv.net/">mpv.net</a> for Windows users).',

    "feature-sharedPlaylists": "shared playlists",  # used for not-supported-by-server-error
    "feature-chat": "chat",  # used for not-supported-by-server-error
    "feature-readiness": "readiness",  # used for not-supported-by-server-error
    "feature-managedRooms": "managed rooms",  # used for not-supported-by-server-error

    "not-supported-by-server-error": "The {} feature is not supported by this server..",  # feature
    "shared-playlists-not-supported-by-server-error": "The shared playlists feature may not be supported by the server. To ensure that it works correctly requires a server running Syncplay  {}+, but the server is running Syncplay {}.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "The shared playlist feature has been disabled in the server configuration. To use this feature you will need to connect to a different server.",

    "invalid-seek-value": "Invalid seek value",
    "invalid-offset-value": "Invalid offset value",

    "switch-file-not-found-error": "Could not switch to file '{0}'. Syncplay looks in specified media directories.",  # File not found
    "folder-search-timeout-error": "The search for media in media directories was aborted as it took too long to search through '{}'. This will occur if you select a folder with too many sub-folders in your list of media folders to search through. For automatic file switching to work again please select File->Set Media Directories in the menu bar and remove this directory or replace it with an appropriate sub-folder. If the folder is actually fine then you can re-enable it by selecting File->Set Media Directories and pressing 'OK'.",  # Folder
    "folder-search-first-file-timeout-error": "The search for media in '{}' was aborted as it took too long to access the directory. This could happen if it is a network drive or if you configure your drive to spin down after a period of inactivity. For automatic file switching to work again please go to File->Set Media Directories and either remove the directory or resolve the issue (e.g. by changing power saving settings).",  # Folder
    "added-file-not-in-media-directory-error": "You loaded a file in '{}' which is not a known media directory. You can add this as a media directory by selecting File->Set Media Directories in the menu bar.",  # Folder
    "no-media-directories-error": "No media directories have been set. For shared playlist and file switching features to work properly please select File->Set Media Directories and specify where Syncplay should look to find media files.",
    "cannot-find-directory-error": "Could not find media directory '{}'. To update your list of media directories please select File->Set Media Directories from the menu bar and specify where Syncplay should look to find media files.",

    "failed-to-load-server-list-error": "Failed to load public server list. Please visit https://www.syncplay.pl/ in your browser.",

    # Client arguments
    "argument-description": 'Solution to synchronize playback of multiple media player instances over the network.',
    "argument-epilog": 'If no options supplied _config values will be used',
    "nogui-argument": 'show no GUI',
    "host-argument": 'server\'s address',
    "name-argument": 'desired username',
    "debug-argument": 'debug mode',
    "force-gui-prompt-argument": 'make configuration prompt appear',
    "no-store-argument": 'don\'t store values in .syncplay',
    "room-argument": 'default room',
    "password-argument": 'server password',
    "player-path-argument": 'path to your player executable',
    "file-argument": 'file to play',
    "args-argument": 'player options, if you need to pass options starting with - prepend them with single \'--\' argument',
    "clear-gui-data-argument": 'resets path and window state GUI data stored as QSettings',
    "language-argument": 'language for Syncplay messages (de/en/ru/it/es/pt_BR/pt_PT/tr)',

    "version-argument": 'prints your version',
    "version-message": "You're using Syncplay version {} ({})",

    "load-playlist-from-file-argument": "loads playlist from text file (one entry per line)",


    # Client labels
    "config-window-title": "Syncplay configuration",

    "connection-group-title": "Connection settings",
    "host-label": "Server address: ",
    "name-label":  "Username (optional):",
    "password-label":  "Server password (if any):",
    "room-label": "Default room: ",
    "roomlist-msgbox-label": "Edit room list (one per line)",

    "media-setting-title": "Media player settings",
    "executable-path-label": "Path to media player:",
    "media-path-label": "Path to video (optional):",
    "player-arguments-label": "Player arguments (if any):",
    "browse-label": "Browse",
    "update-server-list-label": "Update list",

    "more-title": "Show more settings",
    "never-rewind-value": "Never",
    "seconds-suffix": " secs",
    "privacy-sendraw-option": "Send raw",
    "privacy-sendhashed-option": "Send hashed",
    "privacy-dontsend-option": "Don't send",
    "filename-privacy-label": "Filename information:",
    "filesize-privacy-label": "File size information:",
    "checkforupdatesautomatically-label": "Check for Syncplay updates automatically",
    "autosavejoinstolist-label": "Add rooms you join to the room list",
    "slowondesync-label": "Slow down on minor desync (not supported on MPC-HC/BE)",
    "rewindondesync-label": "Rewind on major desync (recommended)",
    "fastforwardondesync-label": "Fast-forward if lagging behind (recommended)",
    "dontslowdownwithme-label": "Never slow down or rewind others (experimental)",
    "pausing-title": "Pausing",
    "pauseonleave-label": "Pause when user leaves (e.g. if they are disconnected)",
    "readiness-title": "Initial readiness state",
    "readyatstart-label": "Set me as 'ready to watch' by default",
    "forceguiprompt-label": "Don't always show the Syncplay configuration window",  # (Inverted)
    "showosd-label": "Enable OSD Messages",

    "showosdwarnings-label": "Include warnings (e.g. when files are different, users not ready)",
    "showsameroomosd-label": "Include events in your room",
    "shownoncontrollerosd-label": "Include events from non-operators in managed rooms",
    "showdifferentroomosd-label": "Include events in other rooms",
    "showslowdownosd-label": "Include slowing down / reverting notifications",
    "language-label": "Language:",
    "automatic-language": "Default ({})",  # Default language
    "showdurationnotification-label": "Warn about media duration mismatches",
    "basics-label": "Basics",
    "readiness-label": "Play/Pause",
    "misc-label": "Misc",
    "core-behaviour-title": "Core room behaviour",
    "syncplay-internals-title": "Syncplay internals",
    "syncplay-mediasearchdirectories-title": "Directories to search for media",
    "syncplay-mediasearchdirectories-label": "Directories to search for media (one path per line)",
    "sync-label": "Sync",
    "sync-otherslagging-title": "If others are lagging behind...",
    "sync-youlaggging-title": "If you are lagging behind...",
    "messages-label": "Messages",
    "messages-osd-title": "On-screen Display settings",
    "messages-other-title": "Other display settings",
    "chat-label": "Chat",
    "privacy-label": "Privacy",  # Currently unused, but will be brought back if more space is needed in Misc tab
    "privacy-title": "Privacy settings",
    "unpause-title": "If you press play, set as ready and:",
    "unpause-ifalreadyready-option": "Unpause if already set as ready",
    "unpause-ifothersready-option": "Unpause if already ready or others in room are ready (default)",
    "unpause-ifminusersready-option": "Unpause if already ready or if all others ready and min users ready",
    "unpause-always": "Always unpause",
    "syncplay-trusteddomains-title": "Trusted domains (for streaming services and hosted content)",

    "chat-title": "Chat message input",
    "chatinputenabled-label": "Enable chat input via mpv",
    "chatdirectinput-label": "Allow instant chat input (bypass having to press enter key to chat)",
    "chatinputfont-label": "Chat input font",
    "chatfont-label": "Set font",
    "chatcolour-label": "Set colour",
    "chatinputposition-label": "Position of message input area in mpv",
    "chat-top-option": "Top",
    "chat-middle-option": "Middle",
    "chat-bottom-option": "Bottom",
    "chatoutputheader-label": "Chat message output",
    "chatoutputfont-label": "Chat output font",
    "chatoutputenabled-label": "Enable chat output in media player (mpv only for now)",
    "chatoutputposition-label": "Output mode",
    "chat-chatroom-option": "Chatroom style",
    "chat-scrolling-option": "Scrolling style",

    "mpv-key-tab-hint": "[TAB] to toggle access to alphabet row key shortcuts.",
    "mpv-key-hint": "[ENTER] to send message. [ESC] to escape chat mode.",
    "alphakey-mode-warning-first-line": "You can temporarily use old mpv bindings with a-z keys.",
    "alphakey-mode-warning-second-line": "Press [TAB] to return to Syncplay chat mode.",

    "help-label": "Help",
    "reset-label": "Restore defaults",
    "run-label": "Run Syncplay",
    "storeandrun-label": "Store configuration and run Syncplay",

    "contact-label": "Feel free to e-mail <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a>, <a href=\"https://github.com/Syncplay/syncplay/issues\"><nobr>create an issue</nobr></a> to report a bug/problem via GitHub, <a href=\"https://github.com/Syncplay/syncplay/discussions\"><nobr>start a discussion</nobr></a> to make a suggestion or ask a question via GitHub, <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>like us on Facebook</nobr></a>, <a href=\"https://twitter.com/Syncplay/\"><nobr>follow us on Twitter</nobr></a>, or visit <a href=\"https://syncplay.pl/\"><nobr>https://syncplay.pl/</nobr></a>. Do not use Syncplay to send sensitive information.",

    "joinroom-label": "Join room",
    "joinroom-menu-label": "Join room {}",
    "seektime-menu-label": "Seek to time",
    "undoseek-menu-label": "Undo seek",
    "play-menu-label": "Play",
    "pause-menu-label": "Pause",
    "playbackbuttons-menu-label": "Show playback buttons",
    "autoplay-menu-label": "Show auto-play button",
    "autoplay-guipushbuttonlabel": "Play when all ready",
    "autoplay-minimum-label": "Min users:",

    "sendmessage-label": "Send",

    "ready-guipushbuttonlabel": "I'm ready to watch!",

    "roomuser-heading-label": "Room / User",
    "size-heading-label": "Size",
    "duration-heading-label": "Length",
    "filename-heading-label": "Filename",
    "notifications-heading-label": "Notifications",
    "userlist-heading-label": "List of who is playing what",

    "browseformedia-label": "Browse for media files",

    "file-menu-label": "&File",  # & precedes shortcut key
    "openmedia-menu-label": "&Open media file",
    "openstreamurl-menu-label": "Open &media stream URL",
    "setmediadirectories-menu-label": "Set media &directories",
    "loadplaylistfromfile-menu-label": "&Load playlist from file",
    "saveplaylisttofile-menu-label": "&Save playlist to file",
    "exit-menu-label": "E&xit",
    "advanced-menu-label": "&Advanced",
    "window-menu-label": "&Window",
    "setoffset-menu-label": "Set &offset",
    "createcontrolledroom-menu-label": "&Create managed room",
    "identifyascontroller-menu-label": "&Identify as room operator",
    "settrusteddomains-menu-label": "Set &trusted domains",
    "addtrusteddomain-menu-label": "Add {} as trusted domain",  # Domain

    "edit-menu-label": "&Edit",
    "cut-menu-label": "Cu&t",
    "copy-menu-label": "&Copy",
    "paste-menu-label": "&Paste",
    "selectall-menu-label": "&Select All",

    "playback-menu-label": "&Playback",

    "help-menu-label": "&Help",
    "userguide-menu-label": "Open user &guide",
    "update-menu-label": "Check for &update",

    "startTLS-initiated": "Attempting secure connection",
    "startTLS-secure-connection-ok": "Secure connection established ({})",
    "startTLS-server-certificate-invalid": 'Secure connection failed. The server uses an invalid security certificate. This communication could be intercepted by a third party. For further details and troubleshooting see <a href="https://syncplay.pl/trouble">here</a>.',
    "startTLS-server-certificate-invalid-DNS-ID": "Syncplay does not trust this server because it uses a certificate that is not valid for its hostname.",
    "startTLS-not-supported-client": "This client does not support TLS",
    "startTLS-not-supported-server": "This server does not support TLS",

    # TLS certificate dialog
    "tls-information-title": "Certificate Details",
    "tls-dialog-status-label": "<strong>Syncplay is using an encrypted connection to {}.</strong>",
    "tls-dialog-desc-label": "Encryption with a digital certificate keeps information private as it is sent to or from the<br/>server {}.",
    "tls-dialog-connection-label": "Information encrypted using Transport Layer Security (TLS), version {} with the cipher<br/>suite: {}.",
    "tls-dialog-certificate-label": "Certificate issued by {} valid until {}.",

    # About dialog
    "about-menu-label": "&About Syncplay",
    "about-dialog-title": "About Syncplay",
    "about-dialog-release": "Version {} release {}",
    "about-dialog-license-text": "Licensed under the Apache&nbsp;License,&nbsp;Version 2.0",
    "about-dialog-license-button": "License",
    "about-dialog-dependencies": "Dependencies",

    "setoffset-msgbox-label": "Set offset",
    "offsetinfo-msgbox-label": "Offset (see https://syncplay.pl/guide/ for usage instructions):",

    "promptforstreamurl-msgbox-label": "Open media stream URL",
    "promptforstreamurlinfo-msgbox-label": "Stream URL",

    "addfolder-label": "Add folder",

    "adduris-msgbox-label": "Add URLs to playlist (one per line)",
    "editplaylist-msgbox-label": "Set playlist (one per line)",
    "trusteddomains-msgbox-label": "Domains it is okay to automatically switch to (one per line)",

    "createcontrolledroom-msgbox-label": "Create managed room",
    "controlledroominfo-msgbox-label": "Enter name of managed room\r\n(see https://syncplay.pl/guide/ for usage instructions):",

    "identifyascontroller-msgbox-label": "Identify as room operator",
    "identifyinfo-msgbox-label": "Enter operator password for this room\r\n(see https://syncplay.pl/guide/ for usage instructions):",

    "public-server-msgbox-label": "Select the public server for this viewing session",

    "megabyte-suffix": " MB",

    # Tooltips

    "host-tooltip": "Hostname or IP to connect to, optionally including port (e.g. syncplay.pl:8999). Only synchronised with people on same server/port.",
    "name-tooltip": "Nickname you will be known by. No registration, so can easily change later. Random name generated if none specified.",
    "password-tooltip": "Passwords are only needed for connecting to private servers.",
    "room-tooltip": "Room to join upon connection can be almost anything, but you will only be synchronised with people in the same room.",

    "edit-rooms-tooltip": "Edit room list.",

    "executable-path-tooltip": "Location of your chosen supported media player (mpv, mpv.net, VLC, MPC-HC/BE, mplayer2 or IINA).",
    "media-path-tooltip": "Location of video or stream to be opened. Necessary for mplayer2.",
    "player-arguments-tooltip": "Additional command line arguments / switches to pass on to this media player.",
    "mediasearcdirectories-arguments-tooltip": "Directories where Syncplay will search for media files, e.g. when you are using the click to switch feature. Syncplay will look recursively through sub-folders.",

    "more-tooltip": "Display less frequently used settings.",
    "filename-privacy-tooltip": "Privacy mode for sending currently playing filename to server.",
    "filesize-privacy-tooltip": "Privacy mode for sending size of currently playing file to server.",
    "privacy-sendraw-tooltip": "Send this information without obfuscation. This is the default option with most functionality.",
    "privacy-sendhashed-tooltip": "Send a hashed version of the information, making it less visible to other clients.",
    "privacy-dontsend-tooltip": "Do not send this information to the server. This provides for maximum privacy.",
    "checkforupdatesautomatically-tooltip": "Regularly check with the Syncplay website to see whether a new version of Syncplay is available.",
    "autosavejoinstolist-tooltip": "When you join a room in a server, automatically remember the room name in the list of rooms to join.",
    "slowondesync-tooltip": "Reduce playback rate temporarily when needed to bring you back in sync with other viewers. Not supported on MPC-HC/BE.",
    "dontslowdownwithme-tooltip": "Means others do not get slowed down or rewinded if your playback is lagging. Useful for room operators.",
    "pauseonleave-tooltip": "Pause playback if you get disconnected or someone leaves from your room.",
    "readyatstart-tooltip": "Set yourself as 'ready' at start (otherwise you are set as 'not ready' until you change your readiness state)",
    "forceguiprompt-tooltip": "Configuration dialogue is not shown when opening a file with Syncplay.",  # (Inverted)
    "nostore-tooltip": "Run Syncplay with the given configuration, but do not permanently store the changes.",  # (Inverted)
    "rewindondesync-tooltip": "Jump back when needed to get back in sync. Disabling this option can result in major desyncs!",
    "fastforwardondesync-tooltip": "Jump forward when out of sync with room operator (or your pretend position if 'Never slow down or rewind others' enabled).",
    "showosd-tooltip": "Sends Syncplay messages to media player OSD.",
    "showosdwarnings-tooltip": "Show warnings if playing different file, alone in room, users not ready, etc.",
    "showsameroomosd-tooltip": "Show OSD notifications for events relating to room user is in.",
    "shownoncontrollerosd-tooltip": "Show OSD notifications for events relating to non-operators who are in managed rooms.",
    "showdifferentroomosd-tooltip": "Show OSD notifications for events relating to room user is not in.",
    "showslowdownosd-tooltip": "Show notifications of slowing down / reverting on time difference.",
    "showdurationnotification-tooltip": "Useful for when a segment in a multi-part file is missing, but can result in false positives.",
    "language-tooltip": "Language to be used by Syncplay.",
    "unpause-always-tooltip": "If you press unpause it always sets you as ready and unpause, rather than just setting you as ready.",
    "unpause-ifalreadyready-tooltip": "If you press unpause when not ready it will set you as ready - press unpause again to unpause.",
    "unpause-ifothersready-tooltip": "If you press unpause when not ready, it will only unpause if others are ready.",
    "unpause-ifminusersready-tooltip": "If you press unpause when not ready, it will only unpause if others are ready and minimum users threshold is met.",
    "trusteddomains-arguments-tooltip": "Domains that it is okay for Syncplay to automatically switch to when shared playlists is enabled.",

    "chatinputenabled-tooltip": "Enable chat input in mpv (press enter to chat, enter to send, escape to cancel)",
    "chatdirectinput-tooltip": "Skip having to press 'enter' to go into chat input mode in mpv. Press TAB in mpv to temporarily disable this feature.",
    "font-label-tooltip": "Font used for when entering chat messages in mpv. Client-side only, so doesn't affect what other see.",
    "set-input-font-tooltip": "Font family used for when entering chat messages in mpv. Client-side only, so doesn't affect what other see.",
    "set-input-colour-tooltip": "Font colour used for when entering chat messages in mpv. Client-side only, so doesn't affect what other see.",
    "chatinputposition-tooltip": "Location in mpv where chat input text will appear when you press enter and type.",
    "chatinputposition-top-tooltip": "Place chat input at top of mpv window.",
    "chatinputposition-middle-tooltip": "Place chat input in dead centre of mpv window.",
    "chatinputposition-bottom-tooltip": "Place chat input at bottom of mpv window.",
    "chatoutputenabled-tooltip": "Show chat messages in OSD (if supported by media player).",
    "font-output-label-tooltip": "Chat output font.",
    "set-output-font-tooltip": "Font used for when displaying chat messages.",
    "chatoutputmode-tooltip": "How chat messages are displayed.",
    "chatoutputmode-chatroom-tooltip": "Display new lines of chat directly below previous line.",
    "chatoutputmode-scrolling-tooltip": "Scroll chat text from right to left.",

    "help-tooltip": "Opens the Syncplay.pl user guide.",
    "reset-tooltip": "Reset all settings to the default configuration.",
    "update-server-list-tooltip": "Connect to syncplay.pl to update list of public servers.",

    "sslconnection-tooltip": "Securely connected to server. Click for certificate details.",

    "joinroom-tooltip": "Leave current room and joins specified room.",
    "seektime-msgbox-label": "Jump to specified time (in seconds / min:sec). Use +/- for relative seek.",
    "ready-tooltip": "Indicates whether you are ready to watch.",
    "autoplay-tooltip": "Auto-play when all users who have readiness indicator are ready and minimum user threshold met.",
    "switch-to-file-tooltip": "Double click to switch to {}",  # Filename
    "sendmessage-tooltip": "Send message to room",

    # In-userlist notes (GUI)
    "differentsize-note": "Different size!",
    "differentsizeandduration-note": "Different size and duration!",
    "differentduration-note": "Different duration!",
    "nofile-note": "(No file being played)",

    # Server messages to client
    "new-syncplay-available-motd-message": "You are using Syncplay {} but a newer version is available from https://syncplay.pl",  # ClientVersion

    # Server notifications
    "welcome-server-notification": "Welcome to Syncplay server, ver. {0}",  # version
    "client-connected-room-server-notification": "{0}({2}) connected to room '{1}'",  # username, host, room
    "client-left-server-notification": "{0} left server",  # name
    "no-salt-notification": "PLEASE NOTE: To allow room operator passwords generated by this server instance to still work when the server is restarted, please add the following command line argument when running the Syncplay server in the future: --salt {}",  # Salt


    # Server arguments
    "server-argument-description": 'Solution to synchronize playback of multiple media player instances over the network. Server instance',
    "server-argument-epilog": 'If no options supplied _config values will be used',
    "server-port-argument": 'server TCP port',
    "server-password-argument": 'server password',
    "server-isolate-room-argument": 'should rooms be isolated?',
    "server-salt-argument": "random string used to generate managed room passwords",
    "server-disable-ready-argument": "disable readiness feature",
    "server-motd-argument": "path to file from which motd will be fetched",
    "server-chat-argument": "Should chat be disabled?",
    "server-chat-maxchars-argument": "Maximum number of characters in a chat message (default is {})", # Default number of characters
    "server-maxusernamelength-argument": "Maximum number of characters in a username (default is {})",
    "server-stats-db-file-argument": "Enable server stats using the SQLite db file provided",
    "server-startTLS-argument": "Enable TLS connections using the certificate files in the path provided",
    "server-messed-up-motd-unescaped-placeholders": "Message of the Day has unescaped placeholders. All $ signs should be doubled ($$).",
    "server-messed-up-motd-too-long": "Message of the Day is too long - maximum of {} chars, {} given.",

    # Server errors
    "unknown-command-server-error": "Unknown command {}",  # message
    "not-json-server-error": "Not a json encoded string {}",  # message
    "line-decode-server-error": "Not a utf-8 string",
    "not-known-server-error": "You must be known to server before sending this command",
    "client-drop-server-error": "Client drop: {} -- {}",  # host, error
    "password-required-server-error": "Password required",
    "wrong-password-server-error": "Wrong password supplied",
    "hello-server-error": "Not enough Hello arguments",  # DO NOT TRANSLATE

    # Playlists
    "playlist-selection-changed-notification":  "{} changed the playlist selection",  # Username
    "playlist-contents-changed-notification": "{} updated the playlist",  # Username
    "cannot-find-file-for-playlist-switch-error": "Could not find file {} in media directories for playlist switch!",  # Filename
    "cannot-add-duplicate-error": "Could not add second entry for '{}' to the playlist as no duplicates are allowed.",  # Filename
    "cannot-add-unsafe-path-error": "Could not automatically load {} because it is not on a trusted domain. You can switch to the URL manually by double clicking it in the playlist, and add trusted domains via File->Advanced->Set Trusted Domains. If you right click on a URL then you can add its domain as a trusted domain via the context menu.",  # Filename
    "sharedplaylistenabled-label": "Enable shared playlists",
    "removefromplaylist-menu-label": "Remove from playlist",
    "shuffleremainingplaylist-menu-label": "Shuffle remaining playlist",
    "shuffleentireplaylist-menu-label": "Shuffle entire playlist",
    "undoplaylist-menu-label": "Undo last change to playlist",
    "addfilestoplaylist-menu-label": "Add file(s) to bottom of playlist",
    "addurlstoplaylist-menu-label": "Add URL(s) to bottom of playlist",
    "editplaylist-menu-label": "Edit playlist",

    "open-containing-folder": "Open folder containing this file",
    "addyourfiletoplaylist-menu-label": "Add your file to playlist",
    "addotherusersfiletoplaylist-menu-label": "Add {}'s file to playlist",  # [Username]
    "addyourstreamstoplaylist-menu-label": "Add your stream to playlist",
    "addotherusersstreamstoplaylist-menu-label": "Add {}' stream to playlist",  # [Username]
    "openusersstream-menu-label": "Open {}'s stream",  # [username]'s
    "openusersfile-menu-label": "Open {}'s file",  # [username]'s

    "playlist-instruction-item-message": "Drag file here to add it to the shared playlist.",
    "sharedplaylistenabled-tooltip": "Room operators can add files to a synced playlist to make it easy for everyone to watching the same thing. Configure media directories under 'Misc'.",

    "playlist-empty-error": "Playlist is currently empty.",
    "playlist-invalid-index-error": "Invalid playlist index",
}
