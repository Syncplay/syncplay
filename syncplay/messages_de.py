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
    "reachout-successful-notification": "{} ({}) erfolgreich erreicht",

    "rewind-notification": "Zurückgespult wegen Zeitdifferenz mit {}",  # User
    "fastforward-notification": "Vorgespult wegen Zeitdifferenz mit {}",  # User
    "slowdown-notification": "Verlangsamt wegen Zeitdifferenz mit {}",  # User
    "revert-notification": "Normalgeschwindigkeit",

    "pause-notification": "{} pausierte",  # User
    "unpause-notification": "{} startete",  # User
    "seek-notification": "{} sprang von {} nach {}",  # User, from time, to time

    "current-offset-notification": "Aktueller Offset: {} Sekunden",  # Offset

    "media-directory-list-updated-notification": "Syncplay-Medienverzeichnisse wurden aktualisiert.",

    "room-join-notification": "{} hat den Raum „{}“ betreten",  # User
    "left-notification": "{} ist gegangen",  # User
    "left-paused-notification": "{} ist gegangen, {} pausierte",  # User who left, User who paused
    "playing-notification": "{} spielt „{}“ ({})",  # User, file, duration
    "playing-notification/room-addendum":  " in Raum: „{}“",  # Room

    "not-all-ready": "Noch nicht bereit: {}",  # Usernames
    "all-users-ready": "Alle sind bereit ({} Nutzer)",  # Number of ready users
    "ready-to-unpause-notification": "Du bist bereit - noch einmal fortsetzen klicken zum abspielen",
    "set-as-ready-notification": "Du bist bereit",
    "set-as-not-ready-notification": "Du bist nicht bereit",
    "autoplaying-notification": "Starte in {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Identifiziere als Raumleiter mit Passwort „{}“...",  # TODO: find a better translation to "room operator"
    "failed-to-identify-as-controller-notification": "{} konnte sich nicht als Raumleiter identifizieren.",
    "authenticated-as-controller-notification": "{} authentifizierte sich als Raumleiter",
    "created-controlled-room-notification": "Gesteuerten Raum „{}“ mit Passwort „{}“ erstellt. Bitte diese Informationen für die Zukunft aufheben! \n\nIn managed rooms everyone is kept in sync with the room operator(s) who are the only ones who can pause, unpause, seek, and change the playlist.\n\nYou should ask regular viewers to join the room '{}' but the room operators can join the room '{}' to automatically authenticate themselves.", # RoomName, operatorPassword, roomName, roomName:operatorPassword # TODO: Translate

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
    "userlist-room-notification":  "In Raum „{}“:",  # Room
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
    "commandlist-notification/chat": "\tch [message] - Chatnachricht an einem Raum senden",
    "commandList-notification/queue": "\tqa [file/url] - add file or url to bottom of playlist", # TO DO: Translate
    "commandList-notification/playlist": "\tql - show the current playlist", # TO DO: Translate
    "commandList-notification/select": "\tqs [index] - select given entry in the playlist", # TO DO: Translate
    "commandList-notification/delete": "\tqd [index] - delete the given entry from the playlist", # TO DO: Translate
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
    "mpv-failed-advice": "The reason mpv cannot start may be due to the use of unsupported command line arguments or an unsupported version of mpv.", # TODO: Translate
    "player-file-open-error": "Fehler beim Öffnen der Datei durch den Player",
    "player-path-error": "Ungültiger Player-Pfad. Unterstützte Player sind: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 und IINA",
    "hostname-empty-error": "Hostname darf nicht leer sein",
    "empty-error": "{} darf nicht leer sein",  # Configuration
    "media-player-error": "Player-Fehler: \"{}\"",  # Error line
    "unable-import-gui-error": "Konnte die GUI-Bibliotheken nicht importieren. PySide muss installiert sein, damit die grafische Oberfläche funktioniert.",
    "unable-import-twisted-error": "Twisted konnte nicht importiert werden. Bitte installiere Twisted v16.4.0 oder höher",

    "arguments-missing-error": "Notwendige Argumente fehlen, siehe --help",

    "unable-to-start-client-error": "Client kann nicht gestartet werden",

    "player-path-config-error": "Player-Pfad ist nicht ordnungsgemäß gesetzt. Unterstützte Player sind: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 und IINA",
    "no-file-path-config-error": "Es muss eine Datei ausgewählt werden, bevor der Player gestartet wird.",
    "no-hostname-config-error": "Hostname darf nicht leer sein",
    "invalid-port-config-error": "Port muss gültig sein",
    "empty-value-config-error": "{} darf nicht leer sein",  # Config option

    "not-json-error": "Kein JSON-String\n",
    "hello-arguments-error": "Zu wenige Hello-Argumente\n",
    "version-mismatch-error": "Verschiedene Versionen auf Client und Server\n",
    "vlc-failed-connection": "Kann nicht zu VLC verbinden. Wenn du syncplay.lua nicht installiert hast, findest du auf https://syncplay.pl/LUA/ [Englisch] eine Anleitung. Syncplay and VLC 4 are not currently compatible, so either use VLC 3 or an alternative such as mpv.", # TO DO: TRANSLATE
    "vlc-failed-noscript": "Laut VLC ist das syncplay.lua Interface-Skript nicht installiert. Auf https://syncplay.pl/LUA/ [Englisch] findest du eine Anleitung.",
    "vlc-failed-versioncheck": "Diese VLC-Version wird von Syncplay nicht unterstützt. Bitte nutze VLC 2.0",
    "vlc-initial-warning": 'VLC does not always provide accurate position information to Syncplay, especially for .mp4 and .avi files. If you experience problems with erroneous seeking then please try an alternative media player such as <a href="https://mpv.io/">mpv</a> (or <a href="https://github.com/stax76/mpv.net/">mpv.net</a> for Windows users).', # TODO: Translate

    "feature-sharedPlaylists": "Geteilte Playlists",  # used for not-supported-by-server-error
    "feature-chat": "Chat",  # used for not-supported-by-server-error
    "feature-readiness": "Bereitschaftsstatus",  # used for not-supported-by-server-error
    "feature-managedRooms": "Zentral gesteuerte Räume",  # used for not-supported-by-server-error

    "not-supported-by-server-error": "Diese Funktion wird vom Server nicht unterstützt. Es wird ein Server mit Syncplay Version {}+ benötigt, aktuell verwendet wird jedoch Version {}.",  # minVersion, serverVersion
    "shared-playlists-not-supported-by-server-error": "Die Geteilte-Playlists-Funktion wird von diesem Server eventuell nicht unterstützt. Um ein korrektes Funktionieren sicherzustellen wird ein Server mit Syncplay Version {}+ benötigt, aktuell verwendet wird jedoch Version {}.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "Die Geteilte-Playlists-Funktion wurde in der Serverkonfiguration deaktiviert. Um diese Funktion zu verwenden, musst du dich mit einem anderen Server verbinden.",

    "invalid-seek-value": "Ungültige Zeitangabe",
    "invalid-offset-value": "Ungültiger Offset-Wert",

    "switch-file-not-found-error": "Konnte nicht zur Datei „{0}“ wechseln. Syncplay sucht im Verzeichnis der aktuellen Datei und angegebenen Medienverzeichnissen.",  # File not found, folder it was not found in
    "folder-search-timeout-error": "Die Suche nach Medien in den Medienverzeichnissen wurde abgebrochen, weil es zu lange gedauert hat, „{}“ zu durchsuchen. Das kann passieren, wenn du in deiner Liste der Medienverzeichnisse ein Verzeichnis mit zu vielen Unterverzeichnissen auswhälst. Damit der automatische Dateiwechsel wieder funktioniert, wähle Datei->Medienverzeichnisse auswählen in der Menüleiste und entferne dieses Verzeichnis oder ersetze es mit einem geeigneten Unterverzeichnis. Wenn das Verzeichnis in Ordnung ist, kannst du es reaktivieren, indem du Datei->Medienverzeichnisse auswählen wählst und „OK“ drückst.",  # Folder
    "folder-search-first-file-timeout-error": "Die Suche nach Medien in den Medienverzeichnissen wurde abgebrochen, weil es zu lange gedauert hat, auf „{}“ zuzugreifen. Das kann passieren, wenn es sich dabei um ein Netzwerkgerät handelt und du eingestellt hast, dass es sich nach Inaktivität ausschaltet. Damit der automatische Dateiwechsel wieder funktioniert, wähle Datei->Medienverzeichnisse auswählen in der Menüleiste und entferne dieses Verzeichnis oder löse das Problem (z.B. indem du die Energiespareinstellungen anpasst).",  # Folder
    "added-file-not-in-media-directory-error": "Du hast eine Datei in im Verzeichnis „{}“ geladeden, welches kein bekanntes Medienverzeichnis ist. Du kannst es als Medienverzeichnis hinzufügen, indem du  Datei->Medienverzeichnisse auswählen in der Menüleiste wählst.",  # Folder
    "no-media-directories-error": "Es wurden keine Medienverzeichnisse ausgewählt. Damit geteilte Playlists und Dateiwechsel korrekt funktionieren, wähle Datei->Medienverzeichnisse auswählen in der Menüleiste und gib an, wo Syncplay nach Mediendateien suchen soll.",
    "cannot-find-directory-error": "Das Medienverzeichnis „{}“ konnte nicht gefunden werden. Um deine Liste an Medienverzeichnissen anzupassen, wähle Datei->Medienverzeichnisse auswählen in der Menüleiste und gib an, wo Syncplay nach Mediendateien suchen soll.",

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
    "language-argument": 'Sprache für Syncplay-Nachrichten (de/en/ru/it/es/pt_BR/pt_PT/tr)',

    "version-argument": 'gibt die aktuelle Version aus',
    "version-message": "Du verwendest Syncplay v. {} ({})",

    "load-playlist-from-file-argument": "lädt eine Playlist aus einer Textdatei (ein Eintrag pro Zeile)",

    # Client labels
    "config-window-title": "Syncplay-Konfiguration",

    "connection-group-title": "Verbindungseinstellungen",
    "host-label": "Server-Adresse:",
    "name-label":  "Benutzername (optional):",
    "password-label":  "Server-Passwort (falls nötig):",
    "room-label": "Standard-Raum:",
    "roomlist-msgbox-label": "Edit room list (one per line)", # TODO: Translate

    "media-setting-title": "Media-Player Einstellungen",
    "executable-path-label": "Pfad zum Media-Player:",
    "media-path-label": "Pfad zum Video (optional):",
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
    "pausing-title": "Pausiere",
    "pauseonleave-label": "Pausieren wenn ein Benutzer austritt",
    "readiness-title": "Anfänglicher Bereitschaftsstatus",
    "readyatstart-label": "Standardmäßig auf „Bereit“ stellen",
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
    "chat-label": "Chat",
    "privacy-label": "Privatsphäre",
    "privacy-title": "Privatsphäreneinstellungen",
    "unpause-title": "Wenn du Play drückst, auf Bereit setzen und:",
    "unpause-ifalreadyready-option": "Wiedergeben wenn bereits als Bereit gesetzt",
    "unpause-ifothersready-option": "Wiedergeben wenn bereits als Bereit gesetzt oder alle anderen bereit sind (Standard)",
    "unpause-ifminusersready-option": "Wiedergeben wenn bereits als Bereit gesetzt oder die minimale Anzahl anderer Nutzer bereit ist",
    "unpause-always": "Immer wiedergeben",
    "syncplay-trusteddomains-title": "Vertrauenswürdige Domains (für Streamingdienste und gehostete Inhalte)",

    "chat-title": "Chatnachrichten-Eingabe",
    "chatinputenabled-label": "Chateingabe via mpv erlauben (mit der Entertaste)",
    "chatdirectinput-label": "Sofotige Chateingabe erlauben (ohne die Entertaste zu drücken)",
    "chatinputfont-label": "Chateingabe-Schriftart",
    "chatfont-label": "Schriftart wählen",
    "chatcolour-label": "Farbe wählen",
    "chatinputposition-label": "Position des Nachrichteneingabe-Felds in mpv",
    "chat-top-option": "Oben",
    "chat-middle-option": "Mitte",
    "chat-bottom-option": "Unten",
    "chatoutputheader-label": "Chatnachrichten-Eingabe",
    "chatoutputfont-label": "Chateingabe-Schriftart",
    "chatoutputenabled-label": "Chatausgabe im Medienplayer aktivieren (bisher nur mpv)",
    "chatoutputposition-label": "Ausgabemodus",
    "chat-chatroom-option": "Chatroom-Stil",
    "chat-scrolling-option": "Scrolling-Stil",

    "mpv-key-tab-hint": "[TAB] um Zugriff auf die Buchstabentastenkürzel ein-/auszuschalten.",
    "mpv-key-hint": "[ENTER] um eine Nachricht zu senden. [ESC] um den Chatmodus zu verlassen.",
    "alphakey-mode-warning-first-line": "Du kannst vorübergehend die alten mpv-Tastaturkürzel mit den a–z-Tasten verwenden.",
    "alphakey-mode-warning-second-line": "Drücke [TAB], um in den Syncplay-Chatmodus zurückzukehren.",

    "help-label": "Hilfe",
    "reset-label": "Auf Standardwerte zurücksetzen",
    "run-label": "Syncplay starten",
    "storeandrun-label": "Konfiguration speichern und Syncplay starten",

    "contact-label": "Du hast eine Idee, einen Bug gefunden oder möchtest Feedback geben? Sende eine E-Mail an <a href=\"mailto:dev@syncplay.pl\">dev@syncplay.pl</a>, chatte auf dem <a href=\"https://webchat.freenode.net/?channels=#syncplay\">#Syncplay IRC-Kanal</a> auf irc.freenode.net oder <a href=\"https://github.com/Uriziel/syncplay/issues\">öffne eine Fehlermeldung auf GitHub</a>. Außerdem findest du auf <a href=\"https://syncplay.pl/\">https://syncplay.pl/</a> weitere Informationen, Hilfestellungen und Updates. Chatnachrichten sind nicht verschlüsselt, also verwende Syncplay nicht, um sensible Daten zu verschicken.",

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

    "sendmessage-label": "Senden",

    "ready-guipushbuttonlabel": "Ich bin bereit zum Gucken!",

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
    "setmediadirectories-menu-label": "Medienverzeichnisse &auswählen",
    "loadplaylistfromfile-menu-label": "&Lade Playlist aus Datei",
    "saveplaylisttofile-menu-label": "&Speichere Playlist in Datei",
    "exit-menu-label": "&Beenden",
    "advanced-menu-label": "&Erweitert",
    "window-menu-label": "&Fenster",
    "setoffset-menu-label": "&Offset einstellen",
    "createcontrolledroom-menu-label": "&Zentral gesteuerten Raum erstellen",
    "identifyascontroller-menu-label": "Als Raumleiter &identifizieren",
    "settrusteddomains-menu-label": "&Vertrauenswürdige Domains auswählen",
    "addtrusteddomain-menu-label": "{} als vertrauenswürdige Domain hinzufügen",  # Domain

    "edit-menu-label": "&Bearbeiten",
    "cut-menu-label": "Aus&schneiden",
    "copy-menu-label": "&Kopieren",
    "paste-menu-label": "&Einsetzen",
    "selectall-menu-label": "&Alles auswälhen",

    "playback-menu-label": "&Wiedergabe",

    "help-menu-label": "&Hilfe",
    "userguide-menu-label": "&Benutzerhandbuch öffnen",
    "update-menu-label": "auf &Aktualisierung prüfen",

    # startTLS messages
    "startTLS-initiated": "Sichere Verbindung wird versucht",
    "startTLS-secure-connection-ok": "Sichere Verbindung hergestellt ({})",
    "startTLS-server-certificate-invalid": 'Sichere Verbindung fehlgeschlagen. Der Server benutzt ein ungültiges Sicherheitszertifikat. Der Kanal könnte von Dritten abgehört werden. Für weitere Details und Problemlösung siehe <a href="https://syncplay.pl/trouble">hier</a> [Englisch].',
    "startTLS-server-certificate-invalid-DNS-ID": "Syncplay does not trust this server because it uses a certificate that is not valid for its hostname.", # TODO: Translate
    "startTLS-not-supported-client": "Dieser Server unterstützt kein TLS",
    "startTLS-not-supported-server": "Dieser Server unterstützt kein TLS",

    # TLS certificate dialog
    "tls-information-title": "Zertifikatdetails",
    "tls-dialog-status-label": "<strong>Syncplay nutzt eine verschlüsselte Verbindung zu {}.</strong>",
    "tls-dialog-desc-label": "Verschlüsselung mit einem digitalen Zertifikat hält Informationen geheim, die vom Server {} gesendet oder empfangen werden.",
    "tls-dialog-connection-label": "Daten werden verschlüsselt mit Transport Layer Security (TLS) Version {} und <br/>folgender Chiffre: {}.",
    "tls-dialog-certificate-label": "Zertifikat ausgestellt durch {} gültig bis {}.",

    # About dialog
    "about-menu-label": "&Über Syncplay",
    "about-dialog-title": "Über Syncplay",
    "about-dialog-release": "Version {} Release {}",
    "about-dialog-license-text": "Lizensiert unter der Apache-Lizenz&nbsp;Version 2.0",
    "about-dialog-license-button": "Lizenz",
    "about-dialog-dependencies": "Abhängigkeiten",

    "setoffset-msgbox-label": "Offset einstellen",
    "offsetinfo-msgbox-label": "Offset (siehe https://syncplay.pl/guide/ für eine Anleitung [Englisch]):",

    "promptforstreamurl-msgbox-label": "Stream-URL öffnen",
    "promptforstreamurlinfo-msgbox-label": "Stream-URL",

    "addfolder-label": "Verzeichnis hinzufügen",

    "adduris-msgbox-label": "URLs zur Playlist hinzufügen (ein Eintrag pro Zeile)",
    "editplaylist-msgbox-label": "Playlist auswählen (ein Eintrag pro Zeile)",
    "trusteddomains-msgbox-label": "Domains, zu denen automatisch gewechselt werden darf (ein Eintrag pro Zeile)",

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

    "edit-rooms-tooltip": "Edit room list.", # TO DO: Translate

    "executable-path-tooltip": "Pfad zum ausgewählten, unterstützten Mediaplayer (mpv, mpv.net, VLC, MPC-HC/BE, mplayer2, oder IINA).",
    "media-path-tooltip": "Pfad zum wiederzugebenden Video oder Stream. Notwendig für mplayer2.",
    "player-arguments-tooltip": "Zusätzliche Kommandozeilenparameter/-schalter für diesen Mediaplayer.",
    "mediasearcdirectories-arguments-tooltip": "Verzeichnisse, in denen Syncplay nach Mediendateien suchen soll, z.B. wenn du die Click-to-switch-Funktion verwendest. Syncplay wird Unterverzeichnisse rekursiv durchsuchen.",  # TODO: Translate Click-to-switch? (or use as name for feature)

    "more-tooltip": "Weitere Einstellungen anzeigen.",
    "filename-privacy-tooltip": "Privatheitsmodus beim Senden des Namens der aktuellen Datei zum Server.",
    "filesize-privacy-tooltip": "Privatheitsmodus beim Senden der Größe der aktuellen Datei zum Server.",
    "privacy-sendraw-tooltip": "Die Information im Klartext übertragen. Dies ist die Standard-Einstellung mit der besten Funktionalität.",
    "privacy-sendhashed-tooltip": "Die Informationen gehasht übertragen, um sie für andere Clients schwerer lesbar zu machen.",
    "privacy-dontsend-tooltip": "Diese Information nicht übertragen. Dies garantiert den größtmöglichen Datanschutz.",
    "checkforupdatesautomatically-tooltip": "Regelmäßig auf der Syncplay-Website nach Updates suchen.",
    "autosavejoinstolist-tooltip": "When you join a room in a server, automatically remember the room name in the list of rooms to join.", # TO DO: Translate
    "autosavejoinstolist-label": "Add rooms you join to the room list e", # TO DO: Translate
    "slowondesync-tooltip": "Reduziert die Abspielgeschwindigkeit zeitweise, um die Synchronität zu den anderen Clients wiederherzustellen.",
    "rewindondesync-label": "Zurückspulen bei großer Zeitdifferenz (empfohlen)",
    "fastforwardondesync-label": "Vorspulen wenn das Video laggt (empfohlen)",
    "dontslowdownwithme-tooltip": "Lässt andere nicht langsamer werden oder zurückspringen, wenn deine Wiedergabe hängt.",
    "pauseonleave-tooltip": "Wiedergabe anhalten, wenn deine Verbindung verloren geht oder jemand den Raum verlässt.",
    "readyatstart-tooltip": "Zu Beginn auf „Bereit“ setzen (sonst bist du als „Nicht Bereit“ gesetzt, bis du den Status änderst)",
    "forceguiprompt-tooltip": "Der Konfigurationsdialog wird nicht angezeigt, wenn eine Datei mit Syncplay geöffnet wird.",
    "nostore-tooltip": "Syncplay mit den angegebenen Einstellungen starten, diese aber nicht dauerhaft speichern.",
    "rewindondesync-tooltip": "Zum Wiederherstellen der Synchronität in der Zeit zurückspringen (empfohlen)",
    "fastforwardondesync-tooltip": "Nach vorne springen, wenn asynchron zum Raumleiter (oder deine vorgetäuschte Position, falls „Niemals verlangsamen oder andere zurückspulen“ aktiviert ist).",
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
    "trusteddomains-arguments-tooltip": "Domains, zu denen Syncplay automatisch wechself darf, wenn geteilte Playlists aktiviert sind.",

    "chatinputenabled-tooltip": "Chateingabe in mpv aktivieren (Drücke Enter zum Chatten, Enter zum Senden, Esc um abzubrechen)",
    "chatdirectinput-tooltip": "Überspringe, Enter drücken zu müssen, um in mpv in den Chatmodus zu gelangen. Drücke TAB, um diese Funktion vorübergehend zu deaktivieren.",
    "font-label-tooltip": "Schriftart für die Darstellung der Chateingabe in mpv. Nur clientseitig, beeinflusst also nicht, was andere sehen.",
    "set-input-font-tooltip": "Schriftfamilie für die Darstellung der Chateingabe in mpv. Nur clientseitig, beeinflusst also nicht, was andere sehen.",
    "set-input-colour-tooltip": "Schriftfarbe für die Darstellung der Chateingabe in mpv. Nur clientseitig, beeinflusst also nicht, was andere sehen.",
    "chatinputposition-tooltip": "Position in mpv, an der Text der Chateingabe erscheint, wenn du Enter drückst und tippst.",
    "chatinputposition-top-tooltip": "Chateingabe oben im mpv-Fenster platzieren.",
    "chatinputposition-middle-tooltip": "Chateingabe mittig im mpv-Fenster platzieren.",
    "chatinputposition-bottom-tooltip": "Chateingabe unten im mpv-Fenster platzieren.",
    "chatoutputenabled-tooltip": "Chatnachrichten im OSD anzeigen (sofern vom Medienplayer unterstützt).",
    "font-output-label-tooltip": "Chatausgabe-Schriftart.",
    "set-output-font-tooltip": "Schriftart für die Darstellung von Chatnachrichten.",
    "chatoutputmode-tooltip": "Wie Chatnachrichten dargestellt werden.",
    "chatoutputmode-chatroom-tooltip": "Neue Chatzeilen unmittelbar unterder vorangehenden Zeile anzeigen.",
    "chatoutputmode-scrolling-tooltip": "Chat-Text von rechts nach links scrollen lassen",

    "help-tooltip": "Öffnet Hilfe auf syncplay.pl [Englisch]",
    "reset-tooltip": "Alle Einstellungen auf Standardwerte zurücksetzen.",
    "update-server-list-tooltip": "Mit syncplay.pl verbinden um die Liste öffentlicher Server zu aktualisieren.",

    "sslconnection-tooltip": "Sicher mit Server verbunden. Klicken, um Zertifikatdetails anzuzeigen.",

    "joinroom-tooltip": "Den aktuellen Raum verlassen und stattdessen den angegebenen betreten.",
    "seektime-msgbox-label": "Springe zur angegebenen Zeit (in Sekunden oder min:sek).  Verwende +/- zum relativen Springen.",
    "ready-tooltip": "Zeigt an, ob du bereit zum anschauen bist",
    "autoplay-tooltip": "Automatisch abspielen, wenn alle Nutzer bereit sind oder die minimale Nutzerzahl erreicht ist.",
    "switch-to-file-tooltip": "Doppelklicken um zu {} zu wechseln",  # Filename
    "sendmessage-tooltip": "Nachricht an Raum senden",

    # In-userlist notes (GUI)
    "differentsize-note": "Verschiedene Größe!",
    "differentsizeandduration-note": "Verschiedene Größe und Dauer!",
    "differentduration-note": "Verschiedene Dauer!",
    "nofile-note": "(keine Datei wird abgespielt)",

    # Server messages to client
    "new-syncplay-available-motd-message": "Du nutzt Syncplay Version {}, aber es gibt eine neuere Version auf https://syncplay.pl",  # ClientVersion

    # Server notifications
    "welcome-server-notification": "Willkommen zum Syncplay-Server, v. {0}",  # version
    "client-connected-room-server-notification": "{0}({2}) hat den Raum „{1}“ betreten",  # username, host, room
    "client-left-server-notification": "{0} hat den Server verlassen",  # name
    "no-salt-notification": "WICHTIGER HINWEIS: Damit von dem Server generierte Passwörter für geführte Räume auch nach einem Serverneustart funktionieren, starte den Server mit dem folgenden Parameter: --salt {}",  # Salt

    # Server arguments
    "server-argument-description": 'Anwendung, um mehrere MPlayer, MPC-HC/BE und VLC-Instanzen über das Internet zu synchronisieren. Server',
    "server-argument-epilog": 'Wenn keine Optionen angegeben sind, werden die _config-Werte verwendet',
    "server-port-argument": 'Server TCP-Port',
    "server-password-argument": 'Server-Passwort',
    "server-isolate-room-argument": 'Sollen die Räume isoliert sein?',
    "server-salt-argument": "zufällige Zeichenkette, die zur Erstellung von Passwörtern verwendet wird",
    "server-disable-ready-argument": "Bereitschaftsfeature deaktivieren",
    "server-motd-argument": "Pfad zur Datei, von der die Nachricht des Tages geladen wird",
    "server-chat-argument": "Soll Chat deaktiviert werden?",
    "server-chat-maxchars-argument": "Maximale Zeichenzahl in einer Chatnachricht (Standard ist {})",
    "server-maxusernamelength-argument": "Maximale Zeichenzahl in einem Benutzernamen (Standard ist {})",
    "server-stats-db-file-argument": "Aktiviere Server-Statistiken mithilfe der bereitgestellten SQLite-db-Datei",
    "server-startTLS-argument": "Erlaube TLS-Verbindungen mit den Zertifikatdateien im Angegebenen Pfad",
    "server-messed-up-motd-unescaped-placeholders": "Die Nachricht des Tages hat unmaskierte Platzhalter. Alle $-Zeichen sollten verdoppelt werden ($$).",
    "server-messed-up-motd-too-long": "Die Nachricht des Tages ist zu lang - Maximal {} Zeichen, aktuell {}.",

    # Server errors
    "unknown-command-server-error": "Unbekannter Befehl {}",  # message
    "not-json-server-error": "Kein JSON-String {}",  # message
    "line-decode-server-error": "Keine utf-8-Zeichenkette",
    "not-known-server-error": "Der Server muss dich kennen, bevor du diesen Befehl nutzen kannst",
    "client-drop-server-error": "Client verloren: {} -- {}",  # host, error
    "password-required-server-error": "Passwort nötig",
    "wrong-password-server-error": "Ungültiges Passwort",
    "hello-server-error": "Zu wenige Hello-Argumente",

    # Playlists
    "playlist-selection-changed-notification":  "{} hat die Playlist-Auswahl geändert",  # Username
    "playlist-contents-changed-notification": "{} hat die Playlist aktualisiert",  # Username
    "cannot-find-file-for-playlist-switch-error": "Die Datei {} konnte zum Dateiwechsel nicht in den Medienverzeichnissen gefunden werden!",  # Filename
    "cannot-add-duplicate-error": "Konnte zweiten Eintrag für „{}“ nicht zur Playlist hinzufügen, weil Dubletten nicht erlaubt sind.",  # Filename
    "cannot-add-unsafe-path-error": "{} konnte nicht automatisch geladen werden, weil es sich nicht um eine vertrauenswürdige Domain handelt. Du kannst manuell zu der URL wechseln, indem du sie in der Playlist doppelklickst oder vertrauenswürdige Domains unter Datei->Erweitert->Vertrauenswürdige Domains auswählen hinzufügst. Wenn du einen Rechtsklick auf eine URL ausführst, kannst du ihre Domain im Kontextmenü als vertrauenswürdig hinzufügen.",  # Filename
    "sharedplaylistenabled-label": "Geteilte Playlists aktivieren",
    "removefromplaylist-menu-label": "Von Playlist entfernen",
    "shuffleremainingplaylist-menu-label": "Verbleibende Playlist shuffeln",
    "shuffleentireplaylist-menu-label": "Gesamte Playlist shuffeln",
    "undoplaylist-menu-label": "Letze Playlist-Änderung rückgängig machen",
    "addfilestoplaylist-menu-label": "Datei(en) zum Ende der Playlist hinzufügen",
    "addurlstoplaylist-menu-label": "URL(s) zum Ende der Playlist hinzufügen",
    "editplaylist-menu-label": "Playlist bearbeiten",

    "open-containing-folder": "Übergeordnetes Verzeichnis der Datei öffnen",
    "addyourfiletoplaylist-menu-label": "Deine Datei zur Playlist hinzufügen",
    "addotherusersfiletoplaylist-menu-label": "{}s Datei zur Playlist hinzufügen",  # [Username]
    "addyourstreamstoplaylist-menu-label": "Deinen Stream zur Playlist hinzufügen",
    "addotherusersstreamstoplaylist-menu-label": "{}s Stream zur Playlist hinzufügen",  # [Username]
    "openusersstream-menu-label": "{}s Stream öffnen",  # [username]'s
    "openusersfile-menu-label": "{}s Datei öffnen",  # [username]'s

    "playlist-instruction-item-message": "Zieh eine Datei hierher, um sie zur geteilten Playlist hinzuzufügen.",
    "sharedplaylistenabled-tooltip": "Raumleiter können Dateien zu einer geteilten Playlist hinzufügen und es so erleichtern, gemeinsam das Gleiche zu gucken. Konfiguriere Medienverzeichnisse unter „Diverse“",

    "playlist-empty-error": "Playlist is currently empty.", # TO DO: Translate
    "playlist-invalid-index-error": "Invalid playlist index", # TO DO: Translate
}
