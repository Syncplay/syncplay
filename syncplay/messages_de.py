# coding:utf8

"""Deutsch dictionary"""

de = {
    "LANGUAGE": "Deutsch",  # (German)

    # Client notifications
    "config-cleared-notification": "Einstellungen gelöscht. Änderungen werden gespeichert, wenn du eine gültige Konfiguration speicherst.",

    "relative-config-notification": "Relative Konfigurationsdatei(en) geladen: {}",

    "connection-attempt-notification": "Verbinde mit {}:{}",  # Port, IP
    "reconnection-attempt-notification": "Verbindung zum Server verloren, versuche erneut",
    "disconnection-notification": "Verbindung zum Server beendet",
    "connection-failed-notification": "Verbindung zum Server fehlgeschlagen",
    "connected-successful-notification": "Erfolgreich mit Server verbunden",
    "retrying-notification": "%s, versuche erneut in %d Sekunden...",  # Seconds
    "reachout-successful-notification": "Successfully reached {} ({})", # TODO: Translate

    "rewind-notification": "Zurückgespult wegen Zeitdifferenz mit {}",  # User
    "fastforward-notification": "Vorgespult wegen Zeitdifferenz mit {}",  # User
    "slowdown-notification": "Verlangsamt wegen Zeitdifferenz mit {}",  # User
    "revert-notification": "Normalgeschwindigkeit",

    "pause-notification": "{} pausierte",  # User
    "unpause-notification": "{} startete",  # User
    "seek-notification": "{} sprang von {} nach {}",  # User, from time, to time

    "current-offset-notification": "Aktueller Offset: {} Sekunden",  # Offset

    "media-directory-list-updated-notification": "Syncplay media directories have been updated.",  # TODO: Translate

    "room-join-notification": "{} hat den Raum '{}' betreten",  # User
    "left-notification": "{} ist gegangen",  # User
    "left-paused-notification": "{} ist gegangen, {} pausierte",  # User who left, User who paused
    "playing-notification": "{} spielt '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum":  " in Raum: '{}'",  # Room

    "not-all-ready": "Noch nicht bereit: {}",  # Usernames
    "all-users-ready": "Alle sind bereit ({} Nutzer)",  # Number of ready users
    "ready-to-unpause-notification": "Du bist bereit - noch einmal fortsetzen klicken zum abspielen",
    "set-as-ready-notification": "Du bist bereit",
    "set-as-not-ready-notification": "Du bist nicht bereit",
    "autoplaying-notification": "Starte in {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Identifiziere als Raumleiter mit Passwort '{}'...",  # TODO: find a better translation to "room operator"
    "failed-to-identify-as-controller-notification": "{} konnte sich nicht als Raumleiter identifizieren.",
    "authenticated-as-controller-notification": "{} authentifizierte sich als Raumleiter",
    "created-controlled-room-notification": "Gesteuerten Raum '{}' mit Passwort '{}' erstellt. Bitte diese Informationen für die Zukunft aufheben!",  # RoomName, operatorPassword

    "file-different-notification": "Deine Datei scheint sich von {}s zu unterscheiden",  # User
    "file-differences-notification": "Deine Datei unterscheidet sich auf folgende Art: {}",
    "room-file-differences": "Unterschiedlich in: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "Name",
    "file-difference-filesize": "Größe",
    "file-difference-duration": "Dauer",
    "alone-in-the-room": "Du bist alleine im Raum",

    "different-filesize-notification": " (ihre Dateigröße ist anders als deine!)",
    "userlist-playing-notification": "{} spielt:",  # Username
    "file-played-by-notification": "Datei: {} wird gespielt von:",  # File
    "no-file-played-notification": "{} spielt keine Datei ab",  # Username
    "notplaying-notification": "Personen im Raum, die keine Dateien spielen:",
    "userlist-room-notification":  "In Raum '{}':",  # Room
    "userlist-file-notification": "Datei",
    "controller-userlist-userflag": "Raumleiter",
    "ready-userlist-userflag": "Bereit",

    "update-check-failed-notification": "Konnte nicht automatisch prüfen, ob Syncplay {} aktuell ist. Soll https://syncplay.pl/ geöffnet werden, um manuell nach Updates zu suchen?",  # Syncplay version
    "syncplay-uptodate-notification": "Syncplay ist aktuell",
    "syncplay-updateavailable-notification": "Eine neuere Version von Syncplay ist verfügbar. Soll die Download-Seite geöffnet werden?",

    "mplayer-file-required-notification": "Syncplay für mplayer benötigt eine Dateiangabe beim Start",
    "mplayer-file-required-notification/example": "Anwendungsbeispiel: syncplay [optionen] [url|pfad/]Dateiname",
    "mplayer2-required": "Syncplay ist inkompatibel zu MPlayer 1.x, bitte nutze MPlayer2 oder mpv",

    "unrecognized-command-notification": "Unbekannter Befehl",
    "commandlist-notification": "Verfügbare Befehle:",
    "commandlist-notification/room": "\tr [Name] - Raum ändern",
    "commandlist-notification/list": "\tl - Nutzerliste anzeigen",
    "commandlist-notification/undo": "\tu - Letzter Zeitsprung rückgängig",
    "commandlist-notification/pause": "\tp - Pausieren / weiter",
    "commandlist-notification/seek": "\t[s][+-]Zeit - zu einer bestimmten Zeit spulen, ohne + oder - wird als absolute Zeit gewertet; Angabe in Sekunden oder Minuten:Sekunden",
    "commandlist-notification/help": "\th - Diese Hilfe",
    "commandlist-notification/toggle": "\tt - Bereitschaftsanzeige umschalten",
    "commandlist-notification/create": "\tc [name] - erstelle zentral gesteuerten Raum mit dem aktuellen Raumnamen",
    "commandlist-notification/auth": "\ta [password] - authentifiziere als Raumleiter mit Passwort",
    "commandlist-notification/chat": "\tch [message] - send a chat message in a room",  # TODO: Translate
    "syncplay-version-notification": "Syncplay Version: {}",  # syncplay.version
    "more-info-notification": "Weitere Informationen auf: {}",  # projectURL

    "gui-data-cleared-notification": "Syncplay hat die Pfad und Fensterdaten der Syncplay-GUI zurückgesetzt.",
    "language-changed-msgbox-label": "Die Sprache wird geändert, wenn du Syncplay neu startest.",
    "promptforupdate-label": "Soll Syncplay regelmäßig nach Updates suchen?",

    "media-player-latency-warning": "Warnung: Der Mediaplayer brauchte {} Sekunden zum Antworten. Wenn Probleme bei der Synchronisation auftreten, schließe bitte andere Anwendungen, um Ressourcen freizugeben. Sollte das nicht funktionieren, versuche es mit einem anderen Media-Player.",  # Seconds to respond
    "mpv-unresponsive-error": "MPV hat für {} Sekunden nicht geantwortet und scheint abgestürzt zu sein. Bitte starte Syncplay neu.",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "Enter drücken zum Beenden\n",

    # Client errors
    "missing-arguments-error": "Notwendige Argumente fehlen, siehe --help",
    "server-timeout-error": "Timeout: Verbindung zum Server fehlgeschlagen",
    "mpc-slave-error": "Kann MPC nicht im Slave-Modus starten!",
    "mpc-version-insufficient-error": "MPC-Version nicht ausreichend, bitte nutze `mpc-hc` >= `{}`",
    "mpc-be-version-insufficient-error": "MPC-Version nicht ausreichend, bitte nutze `mpc-be` >= `{}`",
    "mpv-version-error": "Syncplay ist nicht kompatibel mit dieser Version von mpv.  Bitte benutze eine andere Version (z.B. Git HEAD).",
    "player-file-open-error": "Fehler beim Öffnen der Datei durch den Player",
    "player-path-error": "Ungültiger Player-Pfad. Supported players are: mpv, VLC, MPC-HC, MPC-BE and mplayer2",  # To do: Translate end
    "hostname-empty-error": "Hostname darf nicht leer sein",
    "empty-error": "{} darf nicht leer sein",  # Configuration
    "media-player-error": "Player-Fehler: \"{}\"",  # Error line
    "unable-import-gui-error": "Konnte die GUI-Bibliotheken nicht importieren. PySide muss installiert sein, damit die grafische Oberfläche funktioniert.",
    "unable-import-twisted-error": "Could not import Twisted. Please install Twisted v16.4.0 or later.", #To do: translate

    "arguments-missing-error": "Notwendige Argumente fehlen, siehe --help",

    "unable-to-start-client-error": "Client kann nicht gestartet werden",

    "player-path-config-error": "Player-Pfad ist nicht ordnungsgemäß gesetzt. Supported players are: mpv, VLC, MPC-HC, MPC-BE and mplayer2.",  # To do: Translate end
    "no-file-path-config-error": "Es muss eine Datei ausgewählt werden, bevor der Player gestartet wird.",
    "no-hostname-config-error": "Hostname darf nicht leer sein",
    "invalid-port-config-error": "Port muss gültig sein",
    "empty-value-config-error": "{} darf nicht leer sein",  # Config option

    "not-json-error": "Kein JSON-String\n",
    "hello-arguments-error": "Zu wenige Hello-Argumente\n",
    "version-mismatch-error": "Verschiedene Versionen auf Client und Server\n",
    "vlc-failed-connection": "Kann nicht zu VLC verbinden. Wenn du syncplay.lua nicht installiert hast, findest du auf https://syncplay.pl/LUA/ [Englisch] eine Anleitung.",
    "vlc-failed-noscript": "Laut VLC ist das syncplay.lua Interface-Skript nicht installiert. Auf https://syncplay.pl/LUA/ [Englisch] findest du eine Anleitung.",

    "vlc-failed-versioncheck": "Diese VLC-Version wird von Syncplay nicht unterstützt. Bitte nutze VLC 2.0",
    "feature-sharedPlaylists": "shared playlists",  # used for not-supported-by-server-error # TODO: Translate
    "feature-chat": "chat",  # used for not-supported-by-server-error # TODO: Translate
    "feature-readiness": "readiness",  # used for not-supported-by-server-error # TODO: Translate
    "feature-managedRooms": "managed rooms",  # used for not-supported-by-server-error # TODO: Translate

    "not-supported-by-server-error": "Dieses Feature wird vom Server nicht unterstützt. Es wird ein Server mit Syncplay Version {}+ benötigt, aktuell verwendet wird jedoch Version {}.",  # minVersion, serverVersion
    "shared-playlists-not-supported-by-server-error": "The shared playlists feature may not be supported by the server. To ensure that it works correctly requires a server running Syncplay  {}+, but the server is running Syncplay {}.",  # minVersion, serverVersion # TODO: Translate
    "shared-playlists-disabled-by-server-error": "The shared playlist feature has been disabled in the server configuration. To use this feature you will need to connect to a different server.",  # TODO: Translate

    "invalid-seek-value": "Ungültige Zeitangabe",
    "invalid-offset-value": "Ungültiger Offset-Wert",

    "switch-file-not-found-error": "Konnte nicht zur Datei '{0}' wechseln. Syncplay looks in the specified media directories.",  # File not found, folder it was not found in # TODO: Re-translate "Syncplay sucht im Ordner der aktuellen Datei und angegebenen Medien-Verzeichnissen." to reference to checking in "current media directory"
    "folder-search-timeout-error": "The search for media in media directories was aborted as it took too long to search through '{}'. This will occur if you select a folder with too many sub-folders in your list of media folders to search through. For automatic file switching to work again please select File->Set Media Directories in the menu bar and remove this directory or replace it with an appropriate sub-folder. If the folder is actually fine then you can re-enable it by selecting File->Set Media Directories and pressing 'OK'.",  # Folder # TODO: Translate
    "folder-search-first-file-timeout-error": "The search for media in '{}' was aborted as it took too long to access the directory. This could happen if it is a network drive or if you configure your drive to spin down after a period of inactivity. For automatic file switching to work again please go to File->Set Media Directories and either remove the directory or resolve the issue (e.g. by changing power saving settings).",  # Folder # TODO: Translate
    "added-file-not-in-media-directory-error": "You loaded a file in '{}' which is not a known media directory. You can add this as a media directory by selecting File->Set Media Directories in the menu bar.",  # Folder # TODO: Translate
    "no-media-directories-error": "No media directories have been set. For shared playlist and file switching features to work properly please select File->Set Media Directories and specify where Syncplay should look to find media files.",  # TODO: Translate
    "cannot-find-directory-error": "Could not find media directory '{}'. To update your list of media directories please select File->Set Media Directories from the menu bar and specify where Syncplay should look to find media files.",  # TODO: Translate

    "failed-to-load-server-list-error": "Konnte die Liste der öffentlichen Server nicht laden. Bitte besuche https://www.syncplay.pl/ [Englisch] mit deinem Browser.",

    # Client arguments
    "argument-description": 'Syncplay ist eine Anwendung um mehrere MPlayer, MPC-HC, MPC-BE und VLC-Instanzen über das Internet zu synchronisieren.',
    "argument-epilog": 'Wenn keine Optionen angegeben sind, werden die _config-Werte verwendet',
    "nogui-argument": 'Keine GUI anzeigen',
    "host-argument": 'Server-Adresse',
    "name-argument": 'Gewünschter Nutzername',
    "debug-argument": 'Debug-Modus',
    "force-gui-prompt-argument": 'Einstellungsfenster anzeigen',
    "no-store-argument": 'keine Werte in .syncplay speichern',
    "room-argument": 'Standard-Raum',
    "password-argument": 'Server-Passwort',
    "player-path-argument": 'Pfad zum Player',
    "file-argument": 'Abzuspielende Datei',
    "args-argument": 'Player-Einstellungen; Wenn du Einstellungen, die mit - beginnen, nutzen willst, stelle ein einzelnes \'--\'-Argument davor',
    "clear-gui-data-argument": 'Setzt die Pfad- und GUI-Fenster-Daten die in den QSettings gespeichert sind zurück',
    "language-argument": 'Sprache für Syncplay-Nachrichten (de/en/ru/it/es)',

    "version-argument": 'gibt die aktuelle Version aus',
    "version-message": "Du verwendest Syncplay v. {} ({})",

    # Client labels
    "config-window-title": "Syncplay Konfiguration",

    "connection-group-title": "Verbindungseinstellungen",
    "host-label": "Server-Adresse:",
    "name-label":  "Benutzername (optional):",
    "password-label":  "Server-Passwort (falls nötig):",
    "room-label": "Standard-Raum:",

    "media-setting-title": "Media-Player Einstellungen",
    "executable-path-label": "Pfad zum Media-Player:",
    "media-path-label": "Pfad zur Datei:",  # Todo: Translate to 'Path to video (optional)'
    "player-arguments-label": "Playerparameter:",
    "browse-label": "Durchsuchen",
    "update-server-list-label": "Liste aktualisieren",

    "more-title": "Mehr Einstellungen zeigen",
    "never-rewind-value": "Niemals",
    "seconds-suffix": " sek",
    "privacy-sendraw-option": "Klartext senden",
    "privacy-sendhashed-option": "Hash senden",
    "privacy-dontsend-option": "Nicht senden",
    "filename-privacy-label": "Dateiname:",
    "filesize-privacy-label": "Dateigröße:",
    "checkforupdatesautomatically-label": "Automatisch nach Updates suchen",
    "slowondesync-label": "Verlangsamen wenn nicht synchron (nicht unterstützt mit MPC-HC/BE)",
    "dontslowdownwithme-label": "Nie verlangsamen oder andere zurückspulen (Experimentell)",
    "pausing-title": "Pausing",  # TODO: Translate
    "pauseonleave-label": "Pausieren wenn ein Benutzer austritt",
    "readiness-title": "Initial readiness state",  # TODO: Translate
    "readyatstart-label": "Standardmäßig auf \'Bereit\' stellen",
    "forceguiprompt-label": "Diesen Dialog nicht mehr anzeigen",
    "showosd-label": "OSD-Nachrichten anzeigen",

    "showosdwarnings-label": "Zeige Warnungen (z.B. wenn Dateien verschieden)",
    "showsameroomosd-label": "Zeige Ereignisse in deinem Raum",
    "shownoncontrollerosd-label": "Zeige Ereignisse von nicht geführten Räumen in geführten Räumen.",
    "showdifferentroomosd-label": "Zeige Ereignisse in anderen Räumen",
    "showslowdownosd-label": "Zeige Verlangsamungs/Zurücksetzungs-Benachrichtigung",
    "language-label": "Sprache:",
    "automatic-language": "Automatisch ({})",  # Default language
    "showdurationnotification-label": "Zeige Warnung wegen unterschiedlicher Dauer",
    "basics-label": "Grundlagen",
    "readiness-label": "Play/Pause",
    "misc-label": "Diverse",
    "core-behaviour-title": "Verhalten des Raumes",
    "syncplay-internals-title": "Syncplay intern",
    "syncplay-mediasearchdirectories-title": "In diesen Verzeichnissen nach Medien suchen",  # needs to be checked
    "syncplay-mediasearchdirectories-label": "In diesen Verzeichnissen nach Medien suchen (ein Pfad pro Zeile)",
    "sync-label": "Synchronisation",
    "sync-otherslagging-title": "Wenn andere laggen...",
    "sync-youlaggging-title": "Wenn du laggst...",
    "messages-label": "Nachrichten",
    "messages-osd-title": "OSD-(OnScreenDisplay)-Einstellungen",
    "messages-other-title": "Weitere Display-Einstellungen",
    "chat-label": "Chat",  # TODO: Translate
    "privacy-label": "Privatsphäre",
    "privacy-title": "Privatsphäreneinstellungen",
    "unpause-title": "Wenn du Play drückst, auf Bereit setzen und:",
    "unpause-ifalreadyready-option": "Wiedergeben wenn bereits als Bereit gesetzt",
    "unpause-ifothersready-option": "Wiedergeben wenn bereits als Bereit gesetzt oder alle anderen bereit sind (Standard)",
    "unpause-ifminusersready-option": "Wiedergeben wenn bereits als Bereit gesetzt oder die minimale Anzahl anderer Nutzer bereit ist",
    "unpause-always": "Immer wiedergeben",
    "syncplay-trusteddomains-title": "Trusted domains (for streaming services and hosted content)",  # TODO: Translate into German

    "chat-title": "Chat message input",  # TODO: Translate
    "chatinputenabled-label": "Enable chat input via mpv (using enter key)",  # TODO: Translate
    "chatdirectinput-label": "Allow instant chat input (bypass having to press enter key to chat)",  # TODO: Translate
    "chatinputfont-label": "Chat input font",  # TODO: Translate
    "chatfont-label": "Set font",  # TODO: Translate
    "chatcolour-label": "Set colour",  # TODO: Translate
    "chatinputposition-label": "Position of message input area in mpv",  # TODO: Translate
    "chat-top-option": "Top",  # TODO: Translate
    "chat-middle-option": "Middle",  # TODO: Translate
    "chat-bottom-option": "Bottom",  # TODO: Translate
    "chatoutputheader-label": "Chat message output",  # TODO: Translate
    "chatoutputfont-label": "Chat output font",  # TODO: Translate
    "chatoutputenabled-label": "Enable chat output in media player (mpv only for now)",  # TODO: Translate
    "chatoutputposition-label": "Output mode",  # TODO: Translate
    "chat-chatroom-option": "Chatroom style",  # TODO: Translate
    "chat-scrolling-option": "Scrolling style",  # TODO: Translate

    "mpv-key-tab-hint": "[TAB] to toggle access to alphabet row key shortcuts.",  # TODO: Translate
    "mpv-key-hint": "[ENTER] to send message. [ESC] to escape chat mode.",  # TODO: Translate
    "alphakey-mode-warning-first-line": "You can temporarily use old mpv bindings with a-z keys.",  # TODO: Translate
    "alphakey-mode-warning-second-line": "Press [TAB] to return to Syncplay chat mode.",  # TODO: Translate

    "help-label": "Hilfe",
    "reset-label": "Standardwerte zurücksetzen",
    "run-label": "Syncplay starten",
    "storeandrun-label": "Konfiguration speichern und Syncplay starten",

    "contact-label": "Du hast eine Idee, einen Bug gefunden oder möchtest Feedback geben? Sende eine E-Mail an <a href=\"mailto:dev@syncplay.pl\">dev@syncplay.pl</a>, chatte auf dem <a href=\"https://webchat.freenode.net/?channels=#syncplay\">#Syncplay IRC-Kanal</a> auf irc.freenode.net oder <a href=\"https://github.com/Uriziel/syncplay/issues\">öffne eine Fehlermeldung auf GitHub</a>. Außerdem findest du auf <a href=\"https://syncplay.pl/\">https://syncplay.pl/</a> weitere Informationen, Hilfestellungen und Updates.  OTE: Chat messages are not encrypted so do not use Syncplay to send sensitive information.",  # TODO: Translate  last sentence

    "joinroom-label": "Raum beitreten",
    "joinroom-menu-label": "Raum beitreten {}",  # TODO: Might want to fix this
    "seektime-menu-label": "Spule zu Zeit",
    "undoseek-menu-label": "Rückgängig",
    "play-menu-label": "Wiedergabe",
    "pause-menu-label": "Pause",
    "playbackbuttons-menu-label": "Wiedergabesteuerung anzeigen",
    "autoplay-menu-label": "Auto-Play-Knopf anzeigen",
    "autoplay-guipushbuttonlabel": "Automatisch abspielen wenn alle bereit sind",
    "autoplay-minimum-label": "Minimum an Nutzern:",

    "sendmessage-label": "Send",  # TODO: Translate

    "ready-guipushbuttonlabel": "Ich bin bereit den Film anzuschauen!",

    "roomuser-heading-label": "Raum / Benutzer",
    "size-heading-label": "Größe",
    "duration-heading-label": "Länge",
    "filename-heading-label": "Dateiname",
    "notifications-heading-label": "Benachrichtigungen",
    "userlist-heading-label": "Liste der gespielten Dateien",

    "browseformedia-label": "Nach Mediendateien durchsuchen",

    "file-menu-label": "&Datei",  # & precedes shortcut key
    "openmedia-menu-label": "&Mediendatei öffnen...",
    "openstreamurl-menu-label": "&Stream URL öffnen",
    "setmediadirectories-menu-label": "Set media &directories",  # TODO: Translate
    "exit-menu-label": "&Beenden",
    "advanced-menu-label": "&Erweitert",
    "window-menu-label": "&Fenster",
    "setoffset-menu-label": "&Offset einstellen",
    "createcontrolledroom-menu-label": "&Zentral gesteuerten Raum erstellen",
    "identifyascontroller-menu-label": "Als Raumleiter &identifizieren",
    "settrusteddomains-menu-label": "Set &trusted domains",  # TODO: Translate
    "addtrusteddomain-menu-label": "Add {} as trusted domain",  # Domain # TODO: Translate

    "edit-menu-label": "&Bearbeiten",
    "cut-menu-label": "Aus&schneiden",
    "copy-menu-label": "&Kopieren",
    "paste-menu-label": "&Einsetzen",
    "selectall-menu-label": "&Alles auswälhen",

    "playback-menu-label": "&Wiedergabe",

    "help-menu-label": "&Hilfe",
    "userguide-menu-label": "&Benutzerhandbuch öffnen",
    "update-menu-label": "auf &Aktualisierung prüfen",

    # startTLS messages - TODO: Translate
    "startTLS-initiated": "Attempting secure connection",
    "startTLS-secure-connection-ok": "Secure connection established ({})",
    "startTLS-server-certificate-invalid": 'Secure connection failed. The server uses an invalid security certificate. This communication could be intercepted by a third party. For further details and troubleshooting see <a href="https://syncplay.pl/trouble">here</a>.',
    "startTLS-not-supported-client": "This client does not support TLS",
    "startTLS-not-supported-server": "This server does not support TLS",

    # TLS certificate dialog - TODO: Translate
    "tls-information-title": "Certificate Details",
    "tls-dialog-status-label": "<strong>Syncplay is using an encrypted connection to {}.</strong>",
    "tls-dialog-desc-label": "Encryption with a digital certificate keeps information private as it is sent to or from the<br/>server {}.",
    "tls-dialog-connection-label": "Information encrypted using Transport Layer Security (TLS), version {} with the cipher<br/>suite: {}.",
    "tls-dialog-certificate-label": "Certificate issued by {} valid until {}.",

    # About dialog - TODO: Translate
    "about-menu-label": "&About Syncplay",
    "about-dialog-title": "About Syncplay",
    "about-dialog-release": "Version {} release {}",
    "about-dialog-license-text": "Licensed under the Apache&nbsp;License,&nbsp;Version 2.0",
    "about-dialog-license-button": "License",
    "about-dialog-dependencies": "Dependencies",

    "setoffset-msgbox-label": "Offset einstellen",
    "offsetinfo-msgbox-label": "Offset (siehe https://syncplay.pl/guide/ für eine Anleitung [Englisch]):",

    "promptforstreamurl-msgbox-label": "Stream URL öffnen",
    "promptforstreamurlinfo-msgbox-label": "Stream URL",

    "addfolder-label": "Add folder",  # TODO: Translate

    "adduris-msgbox-label": "Add URLs to playlist (one per line)",  # TODO: Translate
    "editplaylist-msgbox-label": "Set playlist (one per line)",  # TODO: Translate
    "trusteddomains-msgbox-label": "Domains it is okay to automatically switch to (one per line)",  # TODO: Translate

    "createcontrolledroom-msgbox-label": "Zentral gesteuerten Raum erstellen",
    "controlledroominfo-msgbox-label": "Namen des zentral gesteuerten Raums eingeben\r\n(siehe https://syncplay.pl/guide/ für eine Anleitung [Englisch]):",

    "identifyascontroller-msgbox-label": "Als Raumleiter identifizieren",
    "identifyinfo-msgbox-label": "Passwort des zentral gesteuerten Raums eingeben\r\n(siehe https://syncplay.pl/guide/ für eine Anleitung [Englisch]):",

    "public-server-msgbox-label": "Einen öffentlichen Server für diese Sitzung auswählen",

    "megabyte-suffix": " MB",

    # Tooltips

    "host-tooltip": "Hostname oder IP zu der verbunden werden soll. Optional mit Port (z.B.. syncplay.pl:8999). Synchronisation findet nur mit Personen auf dem selben Server und Port statt.",
    "name-tooltip": "Dein Benutzername. Keine Registrierung, kann einfach geändert werden. Bei fehlender Angabe wird ein zufälliger Name generiert.",
    "password-tooltip": "Passwörter sind nur bei Verbindung zu privaten Servern nötig.",
    "room-tooltip": "Der Raum, der betreten werden soll, kann ein x-beliebiger sein. Allerdings werden nur Clients im selben Raum synchronisiert.",

    "executable-path-tooltip": "Pfad zum ausgewählten, unterstützten Mediaplayer (MPC-HC, MPC-BE, VLC, mplayer2 or mpv).",
    "media-path-tooltip": "Pfad zum wiederzugebenden Video oder Stream. Notwendig für mplayer2.",  # TODO: Confirm translation
    "player-arguments-tooltip": "Zusätzliche Kommandozeilenparameter / -schalter für diesen Mediaplayer.",
    "mediasearcdirectories-arguments-tooltip": "Verzeichnisse, in denen Syncplay nach Mediendateien suchen soll, z.B. wenn du das Click-to-switch-Feature verwendest. Syncplay wird rekursiv Unterordner durchsuchen.",  # TODO: Translate Click-to-switch? (or use as name for feature)

    "more-tooltip": "Weitere Einstellungen anzeigen.",
    "filename-privacy-tooltip": "Privatheitsmodus beim Senden des Namens der aktuellen Datei zum Server.",
    "filesize-privacy-tooltip": "Privatheitsmodus beim Senden der Größe der aktuellen Datei zum Server.",
    "privacy-sendraw-tooltip": "Die Information im Klartext übertragen. Dies ist die Standard-Einstellung mit der besten Funktionalität.",
    "privacy-sendhashed-tooltip": "Die Informationen gehasht übertragen, um sie für andere Clients schwerer lesbar zu machen.",
    "privacy-dontsend-tooltip": "Diese Information nicht übertragen. Dies garantiert den größtmöglichen Datanschutz.",
    "checkforupdatesautomatically-tooltip": "Regelmäßig auf der Syncplay-Website nach Updates suchen.",
    "slowondesync-tooltip": "Reduziert die Abspielgeschwindigkeit zeitweise, um die Synchronität zu den anderen Clients wiederherzustellen.",
    "rewindondesync-label": "Zurückspulen bei großer Zeitdifferenz (empfohlen)",
    "fastforwardondesync-label": "Vorspulen wenn das Video laggt (empfohlen)",
    "dontslowdownwithme-tooltip": "Lässt andere nicht langsamer werden oder zurückspringen, wenn deine Wiedergabe hängt.",
    "pauseonleave-tooltip": "Wiedergabe anhalten, wenn deine Verbindung verloren geht oder jemand den Raum verlässt.",
    "readyatstart-tooltip": "Zu Beginn auf 'Bereit' setzen (sonst bist du als 'Nicht Bereit' gesetzt, bis du den Status änderst)",
    "forceguiprompt-tooltip": "Der Konfigurationsdialog wird nicht angezeigt, wenn eine Datei mit Syncplay geöffnet wird.",
    "nostore-tooltip": "Syncplay mit den angegebenen Einstellungen starten, diese aber nicht dauerhaft speichern.",
    "rewindondesync-tooltip": "Zum Wiederherstellen der Synchronität in der Zeit zurückspringen (empfohlen)",
    "fastforwardondesync-tooltip": "Nach vorne springen, wenn asynchron zum Raumleiter (oder deine vorgetäuschte Position, falls 'Niemals verlangsamen oder andere zurückspulen' aktiviert ist).",
    "showosd-tooltip": "Syncplay-Nachrichten auf dem OSD (= OnScreenDisplay, ein eingeblendetes Textfeld) des Players anzeigen.",
    "showosdwarnings-tooltip": "Warnungen bei Unterschiedlichen Dateien oder Alleinsein im Raum anzeigen.",
    "showsameroomosd-tooltip": "OSD-Meldungen über Ereignisse im selben Raum anzeigen.",
    "shownoncontrollerosd-tooltip": "OSD-Meldungen bei Ereignissen verursacht durch nicht-Raumleiter in zentral gesteuerten Räumen anzeigen.",
    "showdifferentroomosd-tooltip": "OSD-Meldungen zu anderen Räumen als dem aktuell betretenen anzeigen.",
    "showslowdownosd-tooltip": "Meldungen bei Geschwindigkeitsänderung anzeigen.",
    "showdurationnotification-tooltip": "Nützlich, wenn z.B. ein Teil eines mehrteiligen Videos fehlt, kann jedoch auch fehlerhaft anschlagen.",
    "language-tooltip": "Die verwendete Sprache von Syncplay",
    "unpause-always-tooltip": "Wiedergabe startet immer (anstatt nur den Bereitschaftsstatus zu ändern)",
    "unpause-ifalreadyready-tooltip": "Wenn du nicht bereit bist und Play drückst wirst du als bereit gesetzt - zum Starten der Wiedergabe nochmal drücken.",
    "unpause-ifothersready-tooltip": "Wenn du Play drückst und nicht bereit bist, wird nur gestartet, wenn alle anderen bereit sind.",
    "unpause-ifminusersready-tooltip": "Wenn du Play drückst und nicht bereit bist, wird nur gestartet, wenn die minimale Anzahl anderer Benutzer bereit ist.",
    "trusteddomains-arguments-tooltip": "Domains that it is okay for Syncplay to automatically switch to when shared playlists is enabled.",  # TODO: Translate into German

    "chatinputenabled-tooltip": "Enable chat input in mpv (press enter to chat, enter to send, escape to cancel)",  # TODO: Translate
    "chatdirectinput-tooltip": "Skip having to press 'enter' to go into chat input mode in mpv. Press TAB in mpv to temporarily disable this feature.",  # TODO: Translate
    "font-label-tooltip": "Font used for when entering chat messages in mpv. Client-side only, so doesn't affect what other see.",  # TODO: Translate
    "set-input-font-tooltip": "Font family used for when entering chat messages in mpv. Client-side only, so doesn't affect what other see.",  # TODO: Translate
    "set-input-colour-tooltip": "Font colour used for when entering chat messages in mpv. Client-side only, so doesn't affect what other see.",  # TODO: Translate
    "chatinputposition-tooltip": "Location in mpv where chat input text will appear when you press enter and type.",  # TODO: Translate
    "chatinputposition-top-tooltip": "Place chat input at top of mpv window.",  # TODO: Translate
    "chatinputposition-middle-tooltip": "Place chat input in dead centre of mpv window.",  # TODO: Translate
    "chatinputposition-bottom-tooltip": "Place chat input at bottom of mpv window.",  # TODO: Translate
    "chatoutputenabled-tooltip": "Show chat messages in OSD (if supported by media player).",  # TODO: Translate
    "font-output-label-tooltip": "Chat output font.",  # TODO: Translate
    "set-output-font-tooltip": "Font used for when displaying chat messages.",  # TODO: Translate
    "chatoutputmode-tooltip": "How chat messages are displayed.",  # TODO: Translate
    "chatoutputmode-chatroom-tooltip": "Display new lines of chat directly below previous line.",  # TODO: Translate
    "chatoutputmode-scrolling-tooltip": "Scroll chat text from right to left.",  # TODO: Translate

    "help-tooltip": "Öffnet Hilfe auf syncplay.pl [Englisch]",
    "reset-tooltip": "Alle Einstellungen auf Standardwerte zurücksetzen.",
    "update-server-list-tooltip": "Mit syncplay.pl verbinden um die Liste öffentlicher Server zu aktualisieren.",

    "sslconnection-tooltip": "Securely connected to server. Click for certificate details.",  # TODO: Translate

    "joinroom-tooltip": "Den aktuellen Raum verlassen und stattdessen den angegebenen betreten.",
    "seektime-msgbox-label": "Springe zur angegebenen Zeit (in Sekunden oder min:sek).  Verwende +/- zum relativen Springen.",
    "ready-tooltip": "Zeigt an, ob du bereit zum anschauen bist",
    "autoplay-tooltip": "Automatisch abspielen, wenn alle Nutzer bereit sind oder die minimale Nutzerzahl erreicht ist.",
    "switch-to-file-tooltip": "Doppelklicken um zu {} zu wechseln",  # Filename
    "sendmessage-tooltip": "Send message to room",  # TODO: Translate

    # In-userlist notes (GUI)
    "differentsize-note": "Verschiedene Größe!",
    "differentsizeandduration-note": "Verschiedene Größe und Dauer!",
    "differentduration-note": "Verschiedene Dauer!",
    "nofile-note": "(keine Datei wird abgespielt)",

    # Server messages to client
    "new-syncplay-available-motd-message": "Du nutzt Syncplay Version {}, aber es gibt eine neuere Version auf https://syncplay.pl",  # ClientVersion

    # Server notifications
    "welcome-server-notification": "Willkommen zum Syncplay-Server, v. {0}",  # version
    "client-connected-room-server-notification": "{0}({2}) hat den Raum '{1}' betreten",  # username, host, room
    "client-left-server-notification": "{0} hat den Server verlassen",  # name
    "no-salt-notification": "WICHTIGER HINWEIS: Damit von dem Server generierte Passwörter für geführte Räume auch nach einem Serverneustart funktionieren, starte den Server mit dem folgenden Parameter: --salt {}",  # Salt

    # Server arguments
    "server-argument-description": 'Anwendung, um mehrere MPlayer, MPC-HC/BE und VLC-Instanzen über das Internet zu synchronisieren. Server',
    "server-argument-epilog": 'Wenn keine Optionen angegeben sind, werden die _config-Werte verwendet',
    "server-port-argument": 'Server TCP-Port',
    "server-password-argument": 'Server Passwort',
    "server-isolate-room-argument": 'Sollen die Räume isoliert sein?',
    "server-salt-argument": "zufällige Zeichenkette, die zur Erstellung von Passwörtern verwendet wird",
    "server-disable-ready-argument": "Bereitschaftsfeature deaktivieren",
    "server-motd-argument": "Pfad zur Datei, von der die Nachricht des Tages geladen wird",
    "server-chat-argument": "Should chat be disabled?",  # TODO: Translate
    "server-chat-maxchars-argument": "Maximum number of characters in a chat message (default is {})",  # TODO: Translate
    "server-maxusernamelength-argument": "Maximum number of characters in a username (default is {})", # TODO: Translate
    "server-stats-db-file-argument": "Enable server stats using the SQLite db file provided", # TODO: Translate
    "server-startTLS-argument": "Enable TLS connections using the certificate files in the path provided", # TODO: Translate
    "server-messed-up-motd-unescaped-placeholders": "Die Nachricht des Tages hat unmaskierte Platzhalter. Alle $-Zeichen sollten verdoppelt werden ($$).",
    "server-messed-up-motd-too-long": "Die Nachricht des Tages ist zu lang - Maximal {} Zeichen, aktuell {}.",

    # Server errors
    "unknown-command-server-error": "Unbekannter Befehl {}",  # message
    "not-json-server-error": "Kein JSON-String {}",  # message
    "line-decode-server-error": "Not a utf-8 string",  # TODO: Translate
    "not-known-server-error": "Der Server muss dich kennen, bevor du diesen Befehl nutzen kannst",
    "client-drop-server-error": "Client verloren: {} -- {}",  # host, error
    "password-required-server-error": "Passwort nötig",
    "wrong-password-server-error": "Ungültiges Passwort",
    "hello-server-error": "Zu wenige Hello-Argumente",

    # Playlists TODO: Translate all this to German
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
}
