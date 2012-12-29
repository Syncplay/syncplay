#coding:utf8

en = {
     
      # Client notifications
      "connection-attempt-notification" : "Attempting to connect to {}:{}", #Port, IP
      "reconnection-attempt-notification" : "Connection with server lost, attempting to reconnect",
      "disconnection-notification" : "Disconnected from server",
      "connection-failed-notification" : "Connection with server failed",
      
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
      "file-played-by-notification" : "File: {} is being played by:", #User
      "notplaying-notification" : "People who are not playing any file:",
      "userlist-room-notification" :  "In room '{}':", #Room
      
      # Client prompts
      "enter-to-exit-prompt" : "Press enter to exit\n",
      
      # Client errors
      "server-timeout-error" : "Connection with server timed out"
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
      "file-played-by-notification" : "Plik: {} jest odtwarzany przez:", #User
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
