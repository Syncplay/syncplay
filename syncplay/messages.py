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
      
      "different-filesize-notification" : " (their file size is different from yours!)",
      "file-played-by-notification" : "File: {} is being played by:", #File
      "notplaying-notification" : "People who are not playing any file:",
      "userlist-room-notification" :  "In room '{}':", #Room
      
      "mplayer-file-required-notification" : "Syncplay using mplayer requires you to provide file when starting",
      "mplayer-file-required-notification/example" : "Usage example: syncplay [options] [url|path/]filename",
      
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

      # Client prompts
      "enter-to-exit-prompt" : "Press enter to exit\n",
      
      # Client errors
      "server-timeout-error" : "Connection with server timed out",
       "mpc-slave-error" : "Unable to start MPC in slave mode!",
       "mpc-version-insufficient-error" : "MPC version not sufficient, please use `mpc-hc` >= `1.6.4`",
       "player-file-open-error" : "Player failed opening file",
       "player-path-error" : "Player path is not set properly",
       "hostname-empty-error" : "Hostname can't be empty",
       "empty-error" : "{} can't be empty", #Configuration
       
       "arguments-missing-error" : "Some necessary arguments are missing, refer to --help",
       
       "unable-to-start-client-error" : "Unable to start client",
       
       "not-json-error" : "Not a json encoded string\n",
       "hello-arguments-error" : "Not enough Hello arguments\n",
       "version-mismatch-error" : "Mismatch between versions of client and server\n",
      
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
      
      # Client labels
      "host-label" : 'Host: ',
      "username-label" :  'Username: ',
      "room-label" : 'Default room (optional): ',
      "password-label" :  'Server password (optional): ',
      "path-label" : 'Path to player executable: ',
      
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
      
      #Server errors
      "not-known-server-error" : "You must be known to server before sending this command",
      "client-drop-server-error" : "Client drop: %s -- %s", #host, error
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
            return messages[locale][type_]
    if(messages["en"].has_key(type_)):
        return messages["en"][type_]
    else:
        raise KeyError()
