#coding:utf8

en = {
     
      # Client notifications
      "connection-attempt-notification" : "Attempting to connect to {}:{}", #Port, IP
      "reconnection-attempt-notification" : "Connection with server lost, attempting to reconnect",
      "disconnection-notification" : "Disconnected from server",
      "connection-failed-notification" : "Connection with server failed",
      "connected-successful-notification" : "Successfully connected to server",
      "retrying-notification" : "%s, Retrying in %d seconds...", #Seconds
      
      "rewind-notification" : "Rewinded due to time difference with <{}>", #User
      "slowdown-notification" : "Slowing down due to time difference with <{}>", #User
      "revert-notification" : "Reverting speed back to normal", 
      
      "pause-notification" : "<{}> paused", #User
      "unpause-notification" : "<{}> unpaused", #User
      "seek-notification" : "<{}> jumped from {} to {}", #User, from time, to time
      
      "current-offset-notification" : "Current offset: {} seconds", #Offset
      
      "room-join-notification" : "<{}> has joined the room: '{}'", #User
      "left-notification" : "<{}> has left", #User
      "playing-notification" : "<{}> is playing '{}' ({})", #User, file, duration
      "playing-notification/room-addendum" :  " in room: '{}'", #Room
      
      "file-different-notification" : "File you are playing appears to be different from <{}>'s", #User
      "file-differences-notification" : "Your file differs in the following way(s): ",
      "room-files-not-same" : "Not all files played in the room are the same",
      "alone-in-the-room": "You're alone in the room",
      
      "different-filesize-notification" : " (their file size is different from yours!)",
      "file-played-by-notification" : "File: {} is being played by:", #File
      "notplaying-notification" : "People who are not playing any file:",
      "userlist-room-notification" :  "In room '{}':", #Room
      
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
      "syncplay-version-notification" : "Syncplay version: {}",    #syncplay.version
      "more-info-notification" : "More info available at: {}",    #projectURL
      
      "gui-data-cleared-notification" : "Syncplay has cleared the path and window state data used by the GUI.",
      
      "vlc-version-mismatch": "Warning: You are running VLC version {}, but Syncplay is designed to run on VLC {} and above.", # VLC version, VLC min version
      "vlc-interface-version-mismatch": "Warning: You are running version {} of the Syncplay interface module for VLC, but Syncplay is designed to run with version {} and above.", # VLC interface version, VLC interface min version
      "vlc-interface-oldversion-ignored": "Warning: Syncplay detected that an old version version of the Syncplay interface module for VLC was installed in the VLC directory. As such, if you are running VLC 2.0 then it will be ignored in favour of the syncplay.lua module contained within the Syncplay directory, but this will mean that other custom interface scripts and extensions will not work. Please refer to the Syncplay User Guide at http://syncplay.pl/guide/ for instructions on how to install syncplay.lua.",
      "vlc-interface-not-installed": "Warning: The Syncplay interface module for VLC was not found in the VLC directory. As such, if you are running VLC 2.0 then VLC will use the syncplay.lua module contained within the Syncplay directory, but this will mean that other custom interface scripts and extensions will not work. Please refer to the Syncplay User Guide at http://syncplay.pl/guide/ for instructions on how to install syncplay.lua.",
      
      "mal-noprivacy-notification": "Warning: The MyAnimeList updater does not support Syncplay's filename privacy settings. Filename information sent to Google.com, MAL-API.com and MyAnimeList.net will not be encrypted, masked or hashed. See http://syncplay.pl/tech/ for more details on MyAnimeList/libMal behaviour.",      

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
       "empty-error" : "{} can't be empty", #Configuration
       
       "arguments-missing-error" : "Some necessary arguments are missing, refer to --help",
       
       "unable-to-start-client-error" : "Unable to start client",
       
       "not-json-error" : "Not a json encoded string\n",
       "hello-arguments-error" : "Not enough Hello arguments\n",
       "version-mismatch-error" : "Mismatch between versions of client and server\n",
       "vlc-error-echo": "VLC error: {}", # VLC error line
       "vlc-unicode-loadfile-error" : "Cannot load file through Syncplay because it contains non-ASCII characters. Please load the file through VLC.",
       "vlc-failed-connection": "Failed to connect to VLC. If you have not installed syncplay.lua then please refer to http://syncplay.pl/LUA/ for instructions.",
       "vlc-failed-noscript": "VLC has reported that the syncplay.lua interface script has not been installed. Please refer to http://syncplay.pl/LUA/ for instructions.",                                                  
       "vlc-failed-versioncheck": "This version of VLC is not supported by Syncplay. Please use VLC 2.",
       "vlc-failed-other" : "When trying to load the syncplay.lua interface script VLC has provided the following error: {}", #Syncplay Error
      
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
      
      # Client labels
      "config-window-title" : "Syncplay configuration",
      
      "connection-group-title" : "Connection settings",
      "host-label" : "Server address: ",
      "username-label" :  "Username:",
      "password-label" :  "Server password (if any):",
      "room-label" : "Default room: ",
      
      "media-setting-title" : "Media player settings",
      "executable-path-label" : "Path to media player:",
      "media-path-label" : "Path to media file:",
      "browse-label" : "Browse",
      
      "more-title" : "Show more settings",
      "mal-username-label" : "MAL username:",
      "mal-password-label" : "MAL password:",
      "privacy-sendraw-option" : "Send raw",
      "privacy-sendhashed-option" : "Send hashed",
      "privacy-dontsend-option" : "Don't send",
      "filename-privacy-label" : "Filename information:",
      "filesize-privacy-label" : "File size information:",
      "slowdown-label" : "Slow down on desync",
      "pauseonleave-label" : "Pause when user leaves",
      "rewind-label" : "Rewind on major desync (highly recommended)",
      "alwayshow-label" : "Always show this dialog",
      "donotstore-label" : "Do not store this configuration",
      
      "help-label" : "Help",
      "run-label" : "Run Syncplay",
      "storeandrun-label" : "Store configuration and run Syncplay",
      
      "roomuser-heading-label" : "Room / User",
      "fileplayed-heading-label" : "File being played",
            
      # Tooltips
      
      "host-tooltip" : "Hostname or IP to connect to, optionally including port (e.g. syncplay.pl:8999). Only synchronised with people on same server/port.",
      "username-tooltip" : "Nickname you will be known by. There is no registration, so you can change this later.",
      "password-tooltip" : "Passwords are only needed for connecting to private servers.",
      "room-tooltip" : "Room to join upon connection can be almost anything, but you will only be synchronised with people in the same room.",
      
      "executable-path-tooltip" : "Location of your chosen supported media player (MPC-HC, VLC, mplayer2 or mpv).",
      "media-path-tooltip" : "Location of video or stream to be opened. Necessary for mpv and mplayer2.",
      
      "more-tooltip" : "Display less frequently used settings.",
      "mal-username-tooltip" : "Your MyAnimeList username. Note: MAL support is experimental!",
      "mal-password-tooltip" : "Your MyAnimeList password. Note: This is not encrypted!",
      "filename-privacy-tooltip" : "Privacy mode for sending currently playing filename to server.",
      "filesize-privacy-tooltip" : "Privacy mode for sending size of currently playing file to server.",
      "privacy-sendraw-tooltip" : "Send this information without obfuscation. This is the default option with most functionality.",
      "privacy-sendhashed-tooltip" : "Send a hashed version of the information, making it less visible to other clients.",
      "privacy-dontsend-tooltip" : "Do not send this information to the server. This provides for maximum privacy.",
      "slowdown-tooltip" : "Reduce playback rate temporarily when needed to bring you back in sync with other viewers.",
      "pauseonleave-tooltip" : "Pause playback if you get disconnected or someone leaves from your room.",
      "rewind-tooltip" : "Jump back when needed to get back in sync. Recommended.",
      "alwayshow-tooltip" : "Configuration dialogue is always shown, even when opening a file with Syncplay.",
      "donotstore-tooltip" : "Run Syncplay with the given configuration, but do not permanently store the changes.",
      
      "help-tooltip" : "Opens the Syncplay.pl user guide.",
      
      # Server messages to client
      "new-syncplay-available-motd-message" : "<NOTICE> You are using Syncplay {} but a newer version is available from http://syncplay.pl </NOTICE>", #ClientVersion
      
      # Server notifications
      "welcome-server-notification" : "Welcome to Syncplay server, ver. {0}", #version
      "client-connected-room-server-notification" : "{0}({2}) connected to room '{1}'", #username, host, room
      "client-left-server-notification" : "{0} left server", #name
      
      
      #Server arguments
      "server-argument-description" : 'Solution to synchronize playback of multiple MPlayer and MPC-HC instances over the network. Server instance',
      "server-argument-epilog" : 'If no options supplied _config values will be used',
      "server-port-argument" : 'server TCP port',
      "server-password-argument" : 'server password',
      "server-isolate-room-argument" : 'should rooms be isolated?',
      "server-motd-argument": "path to file from which motd will be fetched",
      "server-messed-up-motd-unescaped-placeholders": "Message of the Day has unescaped placeholders. All $ signs should be doubled ($$).",
      "server-messed-up-motd-too-long": "Message of the Day is too long - maximum of {} chars, {} given.",
      "server-http-reply-argument": "path to file from which http reply will be fetched",
      "server-default-http-reply": "This server should not be requested with your browser, but with Syncplay software available from http://syncplay.pl",
      "server-irc-verbose": "Should server actively report changes in rooms",
      "server-irc-config": "Path to irc bot config files",
      
      #Server errors
      "unknown-command-server-error" : "Unknown command {}", #message
      "not-json-server-error" : "Not a json encoded string {}", #message
      "not-known-server-error" : "You must be known to server before sending this command",
      "client-drop-server-error" : "Client drop: {} -- {}", #host, error
      "password-required-server-error" : "Password required",
      "wrong-password-server-error" : "Wrong password supplied",
      "hello-server-error" : "Not enough Hello arguments",
      "version-mismatch-server-error" : "Mismatch between versions of client and server",
      "wrong-password-server-error" : "Wrong password supplied"
     
      
      }

pl = {
     
      # Client notifications
      "connection-attempt-notification" : "Próba połączenia z {}:{}", #Port, IP
      "reconnection-attempt-notification" : "Połączenie z serwerem zostało przerwane, ponowne łączenie",
      "disconnection-notification" : "Odłączono od serwera",
      "connection-failed-notification" : "Połączenie z serwerem zakończone fiaskiem",
      
      "rewind-notification" : "Cofnięto z powodu różnicy czasu z <{}>", #User
      "slowdown-notification" : "Zwolniono z powodu różnicy czasu z <{}>", #User
      "revert-notification" : "Przywrócono normalną prędkość odtwarzania",
      
      "pause-notification" : "<{}> zatrzymał odtwarzanie", #User
      "unpause-notification" : "<{}> wznowił odtwarzanie", #User
      "seek-notification" : "<{}> skoczył z {} do {}", #User, from time, to time
      
      "current-offset-notification" : "Obecny offset: {} seconds", #Offset
      
      "room-join-notification" : "<{}> dołączył do pokoju: '{}'", #User
      "left-notification" : "<{}> wyszedł", #User
      "playing-notification" : "<{}> odtwarza '{}' ({})", #User, file, duration
      "playing-notification/room-addendum" : " w pokoju: '{}'", #Room
      
      "file-different-notification" : "Plik, który odtwarzasz wydaje się być różny od <{}>", #User
      "file-differences-notification" : "Twój plik różni się następującymi parametrami: ",
      
      "different-filesize-notification" : " (inny rozmiar pliku!)",
      "file-played-by-notification" : "Plik: {} jest odtwarzany przez:", #File
      "notplaying-notification" : "Osoby, które nie odtwarzają żadnych plików:",
      "userlist-room-notification" :  "W pokoju '{}':", #Room
      # Client prompts
      "enter-to-exit-prompt" : "Wciśnij Enter, aby zakończyć działanie programu\n",
      
      # Client errors
      "server-timeout-error" : "Przekroczono czas oczekiwania na odpowiedź serwera"
      }

messages = {
           "en": en,
           "pl": pl
           }

def getMessage(locale, type_):
    if(messages.has_key(locale)):
        if(messages[locale].has_key(type_)):
            return unicode(messages[locale][type_])
    if(messages["en"].has_key(type_)):
        return unicode(messages["en"][type_])
    else:
        raise KeyError()
