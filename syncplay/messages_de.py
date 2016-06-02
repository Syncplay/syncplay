# coding:utf8

"""Deutsch dictionary"""

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

    "media-directory-list-updated-notification" : u"Syncplay media directories have been updated.", # TODO: Translate

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

    "switch-file-not-found-error" : u"Konnte nicht zur Datei '{0}' wechseln. Syncplay looks in the specified media directories.", # File not found, folder it was not found in # TODO: Re-translate "Syncplay sucht im Ordner der aktuellen Datei und angegebenen Medien-Verzeichnissen." to reference to checking in "current media directory"
    "folder-search-timeout-error" : u"The search for media in media directories was aborted as it took too long to search through '{}'. This will occur if you select a folder with too many sub-folders in your list of media folders to search through. For automatic file switching to work again please select File->Set Media Directories in the menu bar and remove this directory or replace it with an appropriate sub-folder.", #Folder # TODO: Translate
    "folder-search-first-file-timeout-error" : u"The search for media in '{}' was aborted as it took too long to access the directory. This could happen if it is a network drive or if you configure your drive to spin down after a period of inactivity. For automatic file switching to work again please go to File->Set Media Directories and either remove the directory or resolve the issue (e.g. by changing power saving settings).", #Folder # TODO: Translate
    "added-file-not-in-media-directory-error" : u"You loaded a file in '{}' which is not a known media directory. You can add this as a media directory by selecting File->Set Media Directories in the menu bar.", #Folder # TODO: Translate
    "no-media-directories-error" : u"No media directories have been set. For shared playlist and file switching features to work properly please select File->Set Media Directories and specify where Syncplay should look to find media files.", # TODO: Translate
    "cannot-find-directory-error" : u"Could not find media directory '{}'. To update your list of media directories please select File->Set Media Directories from the menu bar and specify where Syncplay should look to find media files.", # TODO: Translate

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
    "syncplay-trusteddomains-title": u"Trusted domains (for streaming services and hosted content)", # TODO: Translate into German

    "help-label" : u"Hilfe",
    "reset-label" : u"Standardwerte zurücksetzen",
    "run-label" : u"Syncplay starten",
    "storeandrun-label" : u"Konfiguration speichern und Syncplay starten",

    "contact-label" : u"Du hast eine Idee, einen Bug gefunden oder möchtest Feedback geben? Sende eine E-Mail an <a href=\"mailto:dev@syncplay.pl\">dev@syncplay.pl</a>, chatte auf dem <a href=\"https://webchat.freenode.net/?channels=#syncplay\">#Syncplay IRC-Kanal</a> auf irc.freenode.net oder <a href=\"https://github.com/Uriziel/syncplay/issues\">öffne eine Fehlermeldung auf GitHub</a>. Außerdem findest du auf <a href=\"http://syncplay.pl/\">http://syncplay.pl/</a> weitere Informationen, Hilfestellungen und Updates.",

    "joinroom-label" : u"Raum beitreten",
    "joinroom-menu-label" : u"Raum beitreten {}", #TODO: Might want to fix this
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
    "setmediadirectories-menu-label" : u"Set media &directories", # TODO: Translate
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

    "addfolder-label" : u"Add folder", # TODO: Translate

    "adduris-msgbox-label" : u"Add URLs to playlist (one per line)", # TODO: Translate

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
    "trusteddomains-arguments-tooltip" : u"Domains that it is okay for Syncplay to automatically switch to when shared playlists is enabled.", # TODO: Translate into German

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
    "hello-server-error" : u"Zu wenige Hello-Argumente",

    # Playlists TODO: Translate all this to German
    "playlist-selection-changed-notification" :  u"{} changed the playlist selection", # Username
    "playlist-contents-changed-notification" : u"{} updated the playlist", # Username
    "cannot-find-file-for-playlist-switch-error" : u"Could not find file {} in media directories for playlist switch!", # Filename
    "cannot-add-duplicate-error" : u"Could not add second entry for '{}' to the playlist as no duplicates are allowed.", #Filename
    "cannot-add-unsafe-path-error" : u"Could not load {} because it is not known as a trusted path.", # Filename
    "sharedplaylistenabled-label" : u"Enable shared playlists",
    "removefromplaylist-menu-label" : u"Remove from playlist",
    "shuffleplaylist-menuu-label" : u"Shuffle playlist",
    "undoplaylist-menu-label" : u"Undo last change to playlist",
    "addfilestoplaylist-menu-label" : u"Add file(s) to bottom of playlist",
    "addurlstoplaylist-menu-label" : u"Add URL(s) to bottom of playlist",

    "addusersfiletoplaylist-menu-label" : u"Add {} file to playlist", # item owner indicator
    "addusersstreamstoplaylist-menu-label" : u"Add {} stream to playlist", # item owner indicator
    "openusersstream-menu-label" : u"Open {} stream", # [username]'s
    "openusersfile-menu-label" : u"Open {} file", # [username]'s
    "item-is-yours-indicator" : u"your", # Goes with addusersfiletoplaylist/addusersstreamstoplaylist
    "item-is-others-indicator" : u"{}'s", # username - goes with addusersfiletoplaylist/addusersstreamstoplaylist

    "playlist-instruction-item-message" : u"Drag file here to add it to the shared playlist.",
    "sharedplaylistenabled-tooltip" : u"Room operators can add files to a synced playlist to make it easy for everyone to watching the same thing. Configure media directories under 'Misc'.",
}
