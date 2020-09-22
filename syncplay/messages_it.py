# coding:utf8

"""Italian dictionary"""

it = {
    "LANGUAGE": "Italiano",

    # Client notifications
    "config-cleared-notification": "Impostazioni iniziali ripristinate. I cambiamenti saranno memorizzati quando salverai una configurazione valida.",

    "relative-config-notification": "Caricato i file di configurazione relativi: {}",

    "connection-attempt-notification": "Tentativo di connessione a {}:{}",  # Port, IP
    "reconnection-attempt-notification": "Connessione col server persa, tentativo di riconnesione in corso",
    "disconnection-notification": "Disconnesso dal server",
    "connection-failed-notification": "Connessione col server fallita",
    "connected-successful-notification": "Connessione al server effettuata con successo",
    "retrying-notification": "%s, Nuovo tentativo in %d secondi...",  # Seconds
    "reachout-successful-notification": "Collegamento stabilito con {} ({})",

    "rewind-notification": "Riavvolgo a causa della differenza temporale con {}",  # User
    "fastforward-notification": "Avanzamento rapido a causa della differenza temporale con {}",  # User
    "slowdown-notification": "Rallento a causa della differenza temporale con {}",  # User
    "revert-notification": "Ripristino la velocità di riproduzione normale",

    "pause-notification": "{} ha messo in pausa",  # User
    "unpause-notification": "{} ha ripreso la riproduzione",  # User
    "seek-notification": "{} è passato da {} a {}",  # User, from time, to time

    "current-offset-notification": "Offset corrente: {} secondi",  # Offset

    "media-directory-list-updated-notification": "Le cartelle multimediali di Syncplay sono state aggiornate.",

    "room-join-notification": "{} è entranto nella stanza: '{}'",  # User
    "left-notification": "{} ha lasciato la stanza",  # User
    "left-paused-notification": "{} ha lasciato la stanza, {} ha messo in pausa",  # User who left, User who paused
    "playing-notification": "{} sta riproducendo '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum":  " nella stanza: '{}'",  # Room

    "not-all-ready": "Non pronti: {}",  # Usernames
    "all-users-ready": "Tutti i partecipanti sono pronti ({} utenti)",  # Number of ready users
    "ready-to-unpause-notification": "Ora sei pronto - premi ancora una volta per riprendere la riproduzione",
    "set-as-ready-notification": "Ora sei pronto",
    "set-as-not-ready-notification": "Non sei pronto",
    "autoplaying-notification": "Riproduzione automatica in {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Ti sei identificato come gestore della stanza con password '{}'...",
    "failed-to-identify-as-controller-notification": "{} ha fallito l'identificazione come gestore della stanza.",
    "authenticated-as-controller-notification": "{} autenticato come gestore della stanza",
    "created-controlled-room-notification": "Stanza gestita '{}' creata con password '{}'. Per favore salva queste informazioni per una consultazione futura!\n\nIn managed rooms everyone is kept in sync with the room operator(s) who are the only ones who can pause, unpause, seek, and change the playlist.\n\nYou should ask regular viewers to join the room '{}' but the room operators can join the room '{}' to automatically authenticate themselves.", # RoomName, operatorPassword, roomName, roomName:operatorPassword # TODO: Translate

    "file-different-notification": "Il file che stai riproducendo sembra essere diverso da quello di {}",  # User
    "file-differences-notification": "Il tuo file mostra le seguenti differenze: {}",  # Differences
    "room-file-differences": "Differenze: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "nome",
    "file-difference-filesize": "dimensione",
    "file-difference-duration": "durata",
    "alone-in-the-room": "Non ci sono altri utenti nella stanza",

    "different-filesize-notification": " (la dimensione del tuo file è diversa da quella degli altri partecipanti!)",
    "userlist-playing-notification": "{} sta riproducendo:",  # Username
    "file-played-by-notification": "File: {} è in riproduzione da:",  # File
    "no-file-played-notification": "{} non sta riproducendo alcun file",  # Username
    "notplaying-notification": "Partecipanti che non stanno riproducendo alcun file:",
    "userlist-room-notification":  "Nella stanza '{}':",  # Room
    "userlist-file-notification": "File",
    "controller-userlist-userflag": "Gestore",
    "ready-userlist-userflag": "Pronto",

    "update-check-failed-notification": "Controllo automatico degli aggiornamenti di Syncplay {} fallito. Vuoi visitare https://syncplay.pl/ per verificare manualmente la presenza di aggiornamenti?",  # Syncplay version
    "syncplay-uptodate-notification": "Syncplay è aggiornato",
    "syncplay-updateavailable-notification": "Una nuova versione di Syncplay è disponibile. Vuoi visitare la pagina delle release?",

    "mplayer-file-required-notification": "Utilizzare Syncplay con mplayer di selezionare il file all'avvio",
    "mplayer-file-required-notification/example": "Esempio di utilizzo: syncplay [opzioni] [url|percorso/]nomefile",
    "mplayer2-required": "Syncplay non è compatibile con MPlayer 1.x, per favore utilizza mplayer2 or mpv",

    "unrecognized-command-notification": "Comando non riconosciuto",
    "commandlist-notification": "Comandi disponibili:",
    "commandlist-notification/room": "\tr [nome] - cambia stanza",
    "commandlist-notification/list": "\tl - mostra la lista di utenti",
    "commandlist-notification/undo": "\tu - annulla l'ultima ricerca",
    "commandlist-notification/pause": "\tp - attiva o disattiva la pausa",
    "commandlist-notification/seek": "\t[s][+-]tempo - salta all'istante di tempo dato, se + o - non è specificato si considera il tempo assoluto in secondi o min:sec",
    "commandlist-notification/help": "\th - mostra questo help",
    "commandlist-notification/toggle": "\tt - attiva o disattiva la funzionalità \"pronto\"",
    "commandlist-notification/create": "\tc [nome] - crea una stanza gestita usando il nome della stanza attuale",
    "commandlist-notification/auth": "\ta [password] - autentica come gestore della stanza, utilizzando la password del gestore",
    "commandlist-notification/chat": "\tch [message] - invia un messaggio nella chat della stanza",
    "commandList-notification/queue": "\tqa [file/url] - add file or url to bottom of playlist",  # TO DO: Translate
    "commandList-notification/playlist": "\tql - show the current playlist",  # TO DO: Translate
    "commandList-notification/select": "\tqs [index] - select given entry in the playlist",  # TO DO: Translate
    "commandList-notification/delete": "\tqd [index] - delete the given entry from the playlist",  # TO DO: Translate
    "syncplay-version-notification": "Versione di Syncplay: {}",  # syncplay.version
    "more-info-notification": "Maggiori informazioni a: {}",  # projectURL

    "gui-data-cleared-notification": "Syncplay ha ripristinato i dati dell'interfaccia relativi ai percorsi e allo stato delle finestre.",
    "language-changed-msgbox-label": "La lingua sarà cambiata quando avvierai Syncplay.",
    "promptforupdate-label": "Ti piacerebbe che, di tanto in tanto, Syncplay controllasse automaticamente la presenza di aggiornamenti?",

    "media-player-latency-warning": "Attenzione: il media player ha impiegato {} secondi per rispondere. Se stai avendo problemi di sincronizzazione, chiudi delle applicazioni per liberare le risorse di sistema e, se ciò non dovesse avere alcun effetto, prova un altro media player.",  # Seconds to respond
    "mpv-unresponsive-error": "mpv non ha risposto per {} secondi, quindi sembra non funzionare correttamente. Per favore, riavvia Syncplay.",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "Premi Invio per uscire\n",

    # Client errors
    "missing-arguments-error": "Alcuni argomenti obbligatori non sono stati trovati. Fai riferimento a --help",
    "server-timeout-error": "Connessione col server scaduta",
    "mpc-slave-error": "Non è possibile avviare MPC in modalità slave!",
    "mpc-version-insufficient-error": "La tua versione di MPC è troppo vecchia, per favore usa `mpc-hc` >= `{}`",
    "mpc-be-version-insufficient-error": "La tua versione di MPC è troppo vecchia, per favore usa `mpc-be` >= `{}`",
    "mpv-version-error": "Syncplay non è compatibile con questa versione di mpv. Per favore usa un'altra versione di mpv (es. Git HEAD).",
    "mpv-failed-advice": "The reason mpv cannot start may be due to the use of unsupported command line arguments or an unsupported version of mpv.", # TODO: Translate
    "player-file-open-error": "Il player non è riuscito ad aprire il file",
    "player-path-error": "Il path del player non è configurato correttamente. I player supportati sono: mpv, mpv.net, VLC, MPC-HC, MPC-BE e mplayer2",
    "hostname-empty-error": "Il campo hostname non può essere vuoto",
    "empty-error": "Il campo {} non può esssere vuoto",  # Configuration
    "media-player-error": "Errore media player: \"{}\"",  # Error line
    "unable-import-gui-error": "Non è possibile importare le librerie di interfaccia grafica. Hai bisogno di PySide per poter utilizzare l'interfaccia grafica.",
    "unable-import-twisted-error": "Non è possibile importare Twisted. Si prega di installare Twisted v16.4.0 o superiore.",

    "arguments-missing-error": "Alcuni argomenti obbligatori non sono stati trovati. Fai riferimento a --help",

    "unable-to-start-client-error": "Impossibile avviare il client",

    "player-path-config-error": "Il percorso del player non è configurato correttamente. I player supportati sono: mpv, mpv.net, VLC, MPC-HC, MPC-BE e mplayer2.",
    "no-file-path-config-error": "Deve essere selezionato un file prima di avviare il player",
    "no-hostname-config-error": "Il campo hostname non può essere vuoto",
    "invalid-port-config-error": "La porta deve essere valida",
    "empty-value-config-error": "Il campo {} non può essere vuoto",  # Config option

    "not-json-error": "Non è una stringa con codifica JSON\n",
    "hello-arguments-error": "Not enough Hello arguments\n",  # DO NOT TRANSLATE
    "version-mismatch-error": "La versione del client è diversa da quella del server\n",
    "vlc-failed-connection": "Impossibile collegarsi a VLC. Se non hai installato syncplay.lua e stai usando l'ultima versione di VLC, fai riferimento a https://syncplay.pl/LUA/ per istruzioni. Syncplay and VLC 4 are not currently compatible, so either use VLC 3 or an alternative such as mpv.", # TO DO: TRANSLATE
    "vlc-failed-noscript": "VLC ha segnalato che lo script di interfaccia syncplay.lua non è stato installato. Per favore, fai riferimento a https://syncplay.pl/LUA/ per istruzioni.",
    "vlc-failed-versioncheck": "Questa versione di VLC non è supportata da Syncplay.",
    "vlc-initial-warning": 'VLC does not always provide accurate position information to Syncplay, especially for .mp4 and .avi files. If you experience problems with erroneous seeking then please try an alternative media player such as <a href="https://mpv.io/">mpv</a> (or <a href="https://github.com/stax76/mpv.net/">mpv.net</a> for Windows users).', # TODO: Translate

    "feature-sharedPlaylists": "playlist condivise",  # used for not-supported-by-server-error
    "feature-chat": "chat",  # used for not-supported-by-server-error
    "feature-readiness": "pronto",  # used for not-supported-by-server-error
    "feature-managedRooms": "stanze gestite",  # used for not-supported-by-server-error

    "not-supported-by-server-error": "La feature {} non è supportata da questo server..",  # feature
    "shared-playlists-not-supported-by-server-error": "Le playlist condivise potrebbero non essere supportata dal server. È necessario un server con Syncplay {}+ per assicurarsi che funzionino correttamente, tuttavia il server sta utilizzando Syncplay {}.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "Le playlist condivise sono state disabilitate nella configurazione del server. Per utilizzarle, dovrai collegarti a un altro server.",

    "invalid-seek-value": "Valore di ricerca non valido",
    "invalid-offset-value": "Valore di offset non valido",

    "switch-file-not-found-error": "Impossibile selezionare il file '{0}'. Syncplay osserva solo le cartelle multimediali specificate.",  # File not found
    "folder-search-timeout-error": "La ricerca nelle cartelle multimediali è stata interrotta perché l'analisi di '{}' sta impiegando troppo tempo. Ciò accade se si aggiunge nella lista di ricerca una cartella con troppe sottocartelle. Per riabilitare la selezione automatica dei file seleziona File->Imposta cartelle multimediali nella barra dei menù e rimuovi questa cartella, o sostituiscila con una sottocartella appropriata. Se la cartella è idonea, è possibile riabilitarla selezionando File->Imposta cartelle multimediali e premendo 'OK'.",  # Folder
    "folder-search-first-file-timeout-error": "La ricerca dei media in '{}' è stata interrotta perché l'accesso alla cartella sta impiegando troppo tempo. Ciò accade se questa si trova in un disco di rete oppure se hai impostato il blocco della rotazione del disco rigido dopo un certo periodo di inattività. Per riabilitare la selezione automatica dei file seleziona File->Imposta cartelle multimediali, quindi rimuovi la cartella oppure risolvi il problema (es. cambiando le impostazioni di risparmio energetico).",  # Folder
    "added-file-not-in-media-directory-error": "Hai selezionato un file in '{}', che non è impostata come cartella multimediale. Puoi aggiungerla come cartella multimediale selezionando File->Imposta cartelle multimediali nella barra dei menù.",  # Folder
    "no-media-directories-error": "Nessuna cartella multimediale è stata configurata. Per permettere il corretto funzionamento delle playlist condivise e la selezione automatica dei file, naviga in File->Imposta cartelle multimediali e specifica dove Syncplay deve ricercare i file multimediali.",
    "cannot-find-directory-error": "Impossibile trovare la cartella multimediale '{}'. Per aggiornare la lista delle cartelle multimediali seleziona File->Imposta cartelle multimediali dalla barra dei menù e specifica dove Syncplay deve ricercare i file multimediali.",

    "failed-to-load-server-list-error": "Impossibile caricare la lista dei server pubblici. Per favore, visita https://www.syncplay.pl/ con il tuo browser.",

    # Client arguments
    "argument-description": 'Programma per sincronizzare la riproduzione di media player multipli attraverso la rete.',
    "argument-epilog": 'Se non è specificata alcuna opzione saranno utilizzati i valori _config',
    "nogui-argument": 'non mostrare l\'interfaccia grafica',
    "host-argument": 'indirizzo del server',
    "name-argument": 'username desiderato',
    "debug-argument": 'modalità debug',
    "force-gui-prompt-argument": 'mostra la finestra di configurazione',
    "no-store-argument": 'non salvare i valori in .syncplay',
    "room-argument": 'stanza di default',
    "password-argument": 'password del server',
    "player-path-argument": 'percorso dell\'eseguibile del tuo player',
    "file-argument": 'file da riprodurre',
    "args-argument": 'opzioni del player, se hai bisogno di utilizzare opzioni che iniziano con - anteponi un singolo \'--\'',
    "clear-gui-data-argument": 'ripristina il percorso e i dati impostati tramite interfaccia grafica e salvati come QSettings',
    "language-argument": 'lingua per i messaggi di Syncplay (de/en/ru/it/es/pt_BR/pt_PT)',

    "version-argument": 'mostra la tua versione',
    "version-message": "Stai usando la versione di Syncplay {} ({})",

    "load-playlist-from-file-argument": "loads playlist from text file (one entry per line)", # TODO: Translate

    # Client labels
    "config-window-title": "Configurazione di Syncplay",

    "connection-group-title": "Impostazioni di connessione",
    "host-label": "Indirizzo del server: ",
    "name-label": "Username (opzionale):",
    "password-label": "Password del server (se necessaria):",
    "room-label": "Stanza di default: ",
    "roomlist-msgbox-label": "Edit room list (one per line)", # TODO: Translate

    "media-setting-title": "Impostazioni del media player",
    "executable-path-label": "Percorso del media player:",
    "media-path-label": "Percorso del video (opzionale):",
    "player-arguments-label": "Opzioni del player (se necessarie):",
    "browse-label": "Sfoglia",
    "update-server-list-label": "Aggiorna lista",

    "more-title": "Mostra altre impostazioni",
    "never-rewind-value": "Mai",
    "seconds-suffix": " sec",
    "privacy-sendraw-option": "Invio semplice",
    "privacy-sendhashed-option": "Invio cifrato",
    "privacy-dontsend-option": "Non inviare",
    "filename-privacy-label": "Nome del file:",
    "filesize-privacy-label": "Dimensione del file:",
    "checkforupdatesautomatically-label": "Controlla automaticamente gli aggiornamenti di Syncplay",
    "autosavejoinstolist-label": "Add rooms you join to the room list", # TO DO: Translate
    "slowondesync-label": "Rallenta in caso di sfasamento minimo (non supportato su MPC-HC/BE)",
    "rewindondesync-label": "Riavvolgi in caso di grande sfasamento (consigliato)",
    "fastforwardondesync-label": "Avanzamento rapido in caso di ritardo (consigliato)",
    "dontslowdownwithme-label": "Non rallentare o riavvolgere gli altri utenti (sperimentale)",
    "pausing-title": "Pausa",
    "pauseonleave-label": "Metti in pausa quando gli altri utenti lasciano la stanza (es. disconnessione)",
    "readiness-title": "Stato iniziale di 'pronto'",
    "readyatstart-label": "Imposta sempre il mio stato come \"pronto\" a guardare",
    "forceguiprompt-label": "Non mostrare la finestra di configurazione di Syncplay a ogni avvio",  # (Inverted)
    "showosd-label": "Abilita i messaggi OSD",

    "showosdwarnings-label": "Mostra gli avvisi (es. file differenti, utenti non pronti)",
    "showsameroomosd-label": "Mostra gli eventi della tua stanza",
    "shownoncontrollerosd-label": "Mostra gli eventi dei non gestori nelle stanze gestite",
    "showdifferentroomosd-label": "Mostra gli eventi di altre stanze",
    "showslowdownosd-label": "Mostra le notifiche di rallentamento / riavvolgimento",
    "language-label": "Lingua:",
    "automatic-language": "Predefinita ({})",  # Default language
    "showdurationnotification-label": "Avvisa in caso di mancata corrispondenza della durata del file",
    "basics-label": "Generali",
    "readiness-label": "Play/Pausa",
    "misc-label": "Varie",
    "core-behaviour-title": "Comportamento principale della stanza",
    "syncplay-internals-title": "Funzionamento di Syncplay",
    "syncplay-mediasearchdirectories-title": "Cartelle contenenti i file multimediali",
    "syncplay-mediasearchdirectories-label": "Cartelle contenenti i file multimediali (un solo percorso per riga)",
    "sync-label": "Sincronia",  # don't have better options as the label won't fit in the panel.
    "sync-otherslagging-title": "Se gli altri partecipanti non sono sincronizzati...",
    "sync-youlaggging-title": "Se tu sei non sei sincronizzato...",
    "messages-label": "Messaggi",
    "messages-osd-title": "Impostazioni On-Screen Display",
    "messages-other-title": "Altre impostazioni dello schermo",
    "chat-label": "Chat",
    "privacy-label": "Privacy",  # Currently unused, but will be brought back if more space is needed in Misc tab
    "privacy-title": "Impostazioni privacy",
    "unpause-title": "Premendo play, imposta il tuo stato su \"pronto\" e:",
    "unpause-ifalreadyready-option": "Riprendi la riproduzione se eri già pronto",
    "unpause-ifothersready-option": "Riprendi la riproduzione se eri già pronto o se gli altri partecipanti sono pronti (default)",
    "unpause-ifminusersready-option": "Riprendi la riproduzione se eri già pronto o se un numero minimo di partecipanti è pronto",
    "unpause-always": "Riprendi sempre la riproduzione",
    "syncplay-trusteddomains-title": "Domini fidati (per streaming e i contenuti in rete)",

    "chat-title": "Inserimento messaggi di chat",
    "chatinputenabled-label": "Abilita la chat su mpv",
    "chatdirectinput-label": "Abilita la chat istantanea (evita di dover premere Invio per chattare)",
    "chatinputfont-label": "Font dell'input della chat",
    "chatfont-label": "Imposta font",
    "chatcolour-label": "Imposta colore",
    "chatinputposition-label": "Posizione dell'area di inserimento testo in mpv",
    "chat-top-option": "In alto",
    "chat-middle-option": "Al centro",
    "chat-bottom-option": "In basso",
    "chatoutputheader-label": "Output messaggi di chat",
    "chatoutputfont-label": "Font dell'output della chat",
    "chatoutputenabled-label": "Abilita l'output della chat nel media player (al momento solo mpv è supportato)",
    "chatoutputposition-label": "Modalità di output",
    "chat-chatroom-option": "Stile chatroom",
    "chat-scrolling-option": "A scorrimento",

    "mpv-key-tab-hint": "[TAB] per attivare le scorciatoie da tastiera e disattivare la chat.",
    "mpv-key-hint": "[Invio] per inviare un messaggio. [Esc] per uscire dalla modalità chat.",
    "alphakey-mode-warning-first-line": "Puoi utilizzare temporaneamente i vecchi comandi di mpv con i tasti a-z.",
    "alphakey-mode-warning-second-line": "Premi [TAB] per ritornare alla modalità chat di Syncplay.",

    "help-label": "Aiuto",
    "reset-label": "Elimina configurazione",
    "run-label": "Avvia Syncplay",
    "storeandrun-label": "Salva la configurazione e avvia Syncplay",

    "contact-label": "Sentiti libero di inviare un'e-mail a <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a>, chattare tramite il <a href=\"https://webchat.freenode.net/?channels=#syncplay\"><nobr>canale IRC #Syncplay</nobr></a> su irc.freenode.net, <a href=\"https://github.com/Uriziel/syncplay/issues\"><nobr>segnalare un problema</nobr></a> su GitHub, <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>lasciare un like sulla nostra pagina Facebook</nobr></a>, <a href=\"https://twitter.com/Syncplay/\"><nobr>seguirci su Twitter</nobr></a>, o visitare <a href=\"https://syncplay.pl/\"><nobr>https://syncplay.pl/</nobr></a>. Non usare Syncplay per inviare dati sensibili.",

    "joinroom-label": "Entra nella stanza",
    "joinroom-menu-label": "Entra nella stanza {}",
    "seektime-menu-label": "Vai a...",
    "undoseek-menu-label": "Annulla vai a...",
    "play-menu-label": "Play",
    "pause-menu-label": "Pausa",
    "playbackbuttons-menu-label": "Mostra i controlli della riproduzione",
    "autoplay-menu-label": "Mostra il tasto di riproduzione automatica",
    "autoplay-guipushbuttonlabel": "Riproduci quando tutti sono pronti",
    "autoplay-minimum-label": "Minimo utenti pronti:",

    "sendmessage-label": "Invia",

    "ready-guipushbuttonlabel": "Sono pronto a guardare!",

    "roomuser-heading-label": "Stanza / Utente",
    "size-heading-label": "Dimensione",
    "duration-heading-label": "Durata",
    "filename-heading-label": "Nome del file",
    "notifications-heading-label": "Notifiche",
    "userlist-heading-label": "Lista degli utenti nella stanza",

    "browseformedia-label": "Seleziona i file multimediali",

    "file-menu-label": "&File",  # & precedes shortcut key
    "openmedia-menu-label": "&Apri file multimediali",
    "openstreamurl-menu-label": "Apri indirizzo di &rete",
    "setmediadirectories-menu-label": "Imposta &cartelle multimediali",
    "loadplaylistfromfile-menu-label": "&Load playlist from file",  # TODO: Translate
    "saveplaylisttofile-menu-label": "&Save playlist to file",  # TODO: Translate
    "exit-menu-label": "&Esci",
    "advanced-menu-label": "&Avanzate",
    "window-menu-label": "&Finestra",
    "setoffset-menu-label": "Imposta &offset",
    "createcontrolledroom-menu-label": "&Crea stanza gestita",
    "identifyascontroller-menu-label": "&Identificati come operatore della stanza",
    "settrusteddomains-menu-label": "Imposta &domini fidati",
    "addtrusteddomain-menu-label": "Aggiungi {} come dominio fidato",  # Domain

    "edit-menu-label": "&Modifica",
    "cut-menu-label": "&Taglia",
    "copy-menu-label": "&Copia",
    "paste-menu-label": "&Incolla",
    "selectall-menu-label": "&Seleziona tutto",

    "playback-menu-label": "&Riproduzione",

    "help-menu-label": "&Aiuto",
    "userguide-menu-label": "Apri guida &utente",
    "update-menu-label": "Controlla la presenza di &aggiornamenti",

    "startTLS-initiated": "Tentativo di connessione sicura in corso",
    "startTLS-secure-connection-ok": "Connessione sicura stabilita ({})",
    "startTLS-server-certificate-invalid": 'Connessione sicura non riuscita. Il certificato di sicurezza di questo server non è valido. La comunicazione potrebbe essere intercettata da una terza parte. Per ulteriori dettagli e informazioni sulla risoluzione del problema, clicca <a href="https://syncplay.pl/trouble">qui</a>.',
    "startTLS-server-certificate-invalid-DNS-ID": "Syncplay does not trust this server because it uses a certificate that is not valid for its hostname.", # TODO: Translate
    "startTLS-not-supported-client": "Questo client non supporta TLS",
    "startTLS-not-supported-server": "Questo server non supporta TLS",

    # TLS certificate dialog
    "tls-information-title": "Informazioni sul certificato",
    "tls-dialog-status-label": "<strong>Syncplay è connesso a {} tramite una connessione codificata.</strong>",
    "tls-dialog-desc-label": "La codifica con un certificato digitale mantiene private le informazioni quando vengono<br/>inviate dal/al server {}.",
    "tls-dialog-connection-label": "Informazioni codificate usando Transport Layer Security (TLS), versione {} usando gli<br/>algoritmi di cifratura: {}.",
    "tls-dialog-certificate-label": "Certificato rilasciato da {} valido fino al {}.",

    # About dialog
    "about-menu-label": "&Informazioni su Syncplay",
    "about-dialog-title": "Informazioni su Syncplay",
    "about-dialog-release": "Versione {} release {}",
    "about-dialog-license-text": "Rilasciato sotto Apache&nbsp;License,&nbsp;Version 2.0",
    "about-dialog-license-button": "Licenza",
    "about-dialog-dependencies": "Dipendenze",

    "setoffset-msgbox-label": "Imposta offset",
    "offsetinfo-msgbox-label": "Offset (vedi https://syncplay.pl/guide/ per istruzioni):",

    "promptforstreamurl-msgbox-label": "Apri URL",
    "promptforstreamurlinfo-msgbox-label": "Indirizzo di rete",

    "addfolder-label": "Aggiungi cartella",

    "adduris-msgbox-label": "Aggiungi gli indirizzi alla playlist (uno per riga)",
    "editplaylist-msgbox-label": "Imposta playlist (una per riga)",
    "trusteddomains-msgbox-label": "Domini a cui è lecito passare automaticamente (uno per riga)",

    "createcontrolledroom-msgbox-label": "Crea stanza gestita",
    "controlledroominfo-msgbox-label": "Inserisci il nome della stanza gestita\r\n(vedi https://syncplay.pl/guide/ per istruzioni):",

    "identifyascontroller-msgbox-label": "Identificati come operatore della stanza",
    "identifyinfo-msgbox-label": "Inserisci la password dell'operatore per questa stanza\r\n(vedi https://syncplay.pl/guide/ per istruzioni):",

    "public-server-msgbox-label": "Seleziona il server pubblico per questa sessione",

    "megabyte-suffix": " MB",

    # Tooltips

    "host-tooltip": "Hostname o indirizzo IP a cui collegarsi e, se necessario, includere la porta (es. syncplay.pl:8999). La sincronizzazione avviene solo con gli utenti collegati allo stesso server/porta.",
    "name-tooltip": "Il nome utente con cui sarai riconosciuto. Nessuna registrazione necessaria, cosi potrai sempre cambiarlo. Se lasciato vuoto, viene scelto un nome casuale.",
    "password-tooltip": "La password è necessaria solo in caso di connessione a server privati.",
    "room-tooltip": "La stanza in cui entrare dopo la connessione. Può assumere qualsiasi nome, ma ricorda che sarai sincronizzato solo con gli utenti nella stessa stanza.",

    "edit-rooms-tooltip": "Edit room list.",  # TO DO: Translate

    "executable-path-tooltip": "Percorso del media player desiderato (scegliere tra mpv, mpv.net, VLC, MPC-HC/BE or mplayer2).",
    "media-path-tooltip": "Percorso del video o stream da aprire. Necessario per mplayer2.",
    "player-arguments-tooltip": "Argomenti da linea di comando aggiuntivi da passare al media player scelto.",
    "mediasearcdirectories-arguments-tooltip": "Cartelle dove Syncplay cercherà i file multimediali, es. quando usi la funzione click to switch. Syncplay cercherà anche nelle sottocartelle.",

    "more-tooltip": "Mostra le impostazioni usate meno frequentemente.",
    "filename-privacy-tooltip": "Modalità di invio al server del nome del file attualmente in riproduzione.",
    "filesize-privacy-tooltip": "Modalità di invio al server della dimensione del file attualmente in riproduzione.",
    "privacy-sendraw-tooltip": "Invia questa informazione in chiaro. Questa è l'impostazione predefinita per la maggior parte delle funzionalità.",
    "privacy-sendhashed-tooltip": "Invia una versione cifrata dell'informazione, rendendola meno visibile agli altri client.",
    "privacy-dontsend-tooltip": "Non inviare questa informazione al server. Questo garantisce massima privacy.",
    "checkforupdatesautomatically-tooltip": "Controlla regolarmente la presenza di nuove versioni di Syncplay.",
    "autosavejoinstolist-tooltip": "When you join a room in a server, automatically remember the room name in the list of rooms to join.", # TO DO: Translate
    "slowondesync-tooltip": "Riduce temporaneamente la velocità di riproduzione quando c'è bisogno di sincronizzarti con gli altri utenti. Non supportato su MPC-HC/BE.",
    "dontslowdownwithme-tooltip": "Gli altri utenti non vengono rallentati se non sei sincronizzato. Utile per i gestori della stanza.",
    "pauseonleave-tooltip": "Mette in pausa la riproduzione se vieni disconnesso o se qualcuno lascia la stanza.",
    "readyatstart-tooltip": "Imposta il tuo stato su \"pronto\" all'avvio (in caso contrario, sarai su \"non pronto\" finché non cambierai il tuo stato)",
    "forceguiprompt-tooltip": "La finestra di configurazione non viene mostrata quando apri Syncplay.",
    "nostore-tooltip": "Avvia Syncplay con la configurazione scelta, ma non salva le impostazioni.",
    "rewindondesync-tooltip": "Torna indietro quando necessario per ristabilire la sincronizzazione. Disabilitare quest'opzione può causare gravi problemi di sincronizzazione!",
    "fastforwardondesync-tooltip": "Avanza rapidamente quando non sei sincronizzato col gestore della stanza (usa una posizione fittizia se 'Non rallentare o riavvolgere gli altri utenti' è abilitato).",
    "showosd-tooltip": "Invia i messaggi di Syncplay al media player tramite OSD.",
    "showosdwarnings-tooltip": "Mostra gli avvisi in caso di riproduzione di un file differente, se sei l'unico utente nella stanza, se ci sono utenti non pronti, ecc.",
    "showsameroomosd-tooltip": "Mostra le notifiche OSD per gli eventi relativi alla stanza in cui si trova l'utente.",
    "shownoncontrollerosd-tooltip": "Mostra le notifiche OSD per gli eventi relativi ai non operatori presenti nelle stanze gestite.",
    "showdifferentroomosd-tooltip": "Mostra le notifiche OSD per gli eventi relativi alle stanze in cui l'utente non si trova.",
    "showslowdownosd-tooltip": "Mostra le notifiche di rallentamento / riavvolgimento in caso di differenza temporale.",
    "showdurationnotification-tooltip": "Utile quando manca un segmento di un file con più parti. Può causare dei falsi positivi.",
    "language-tooltip": "Lingua da utilizzare in Syncplay.",
    "unpause-always-tooltip": "Se riprendi la riproduzione, il tuo stato cambia in \"pronto\" e la riproduzione viene avviata, piuttosto che impostarti solo su pronto.",
    "unpause-ifalreadyready-tooltip": "Se riprendi la riproduzione quando non sei \"pronto\", verrai impostato su pronto - ripeti il comando ancora una volta per avviare la riproduzione.",
    "unpause-ifothersready-tooltip": "Se riprendi la riproduzione quando non sei \"pronto\" la riproduzione verrà avviata solo se gli altri sono pronti.",
    "unpause-ifminusersready-tooltip": "Se riprendi la riproduzione quando non sei \"pronto\", la riproduzione verrà avviata solo se un numero minimo di utenti è \"pronto\".",
    "trusteddomains-arguments-tooltip": "Domini verso cui è possibile collegarsi automaticamente quando le playlist condivise sono abilitate.",

    "chatinputenabled-tooltip": "Abilita l'input della chat in mpv (premi Invio per chattare, per inviare ed Esc per cancellare)",
    "chatdirectinput-tooltip": "Evita di dover premere Invio per aprire l'input della chat in mpv. Premi TAB in mpv per disabilitare temporaneamente questa funzione.",
    "font-label-tooltip": "Font usato nell'input della chat in mpv. Non influenza cosa vedono gli altri, vale solo per te.",
    "set-input-font-tooltip": "Font usato nell'input della chat in mpv. Non influenza cosa vedono gli altri, vale solo per te.",
    "set-input-colour-tooltip": "Colore del font usato nell'input della chat in mpv. Non influenza cosa vedono gli altri, vale solo per te.",
    "chatinputposition-tooltip": "Posizione dell'input della chat in mpv quando premi Invio.",
    "chatinputposition-top-tooltip": "Posiziona l'input della chat in cima alla finestra di mpv.",
    "chatinputposition-middle-tooltip": "Posizione l'input della chat al centro della finestra di mpv.",
    "chatinputposition-bottom-tooltip": "Posiziona l'input della chat in basso alla finestra di mpv.",
    "chatoutputenabled-tooltip": "Mostra i messaggi di chat nell'OSD (se supportato dal media player).",
    "font-output-label-tooltip": "Font dell'output della chat.",
    "set-output-font-tooltip": "Font usato per mostrare i messaggi di chat.",
    "chatoutputmode-tooltip": "Come sono mostrati i messaggi di chat.",
    "chatoutputmode-chatroom-tooltip": "Mostra i nuovi messaggi di chat al di sotto di quelli precedenti.",
    "chatoutputmode-scrolling-tooltip": "Scorri il testo della chat da destra a sinistra.",

    "help-tooltip": "Apri la guida utente su syncplay.pl.",
    "reset-tooltip": "Ripristina le impostazioni iniziali di Syncplay.",
    "update-server-list-tooltip": "Scarica la lista dei server pubblici da syncplay.pl.",

    "sslconnection-tooltip": "Connessione sicura al server. Clicca per informazioni sul certificato.",

    "joinroom-tooltip": "Lascia la stanza attuale e entra in quella specificata.",
    "seektime-msgbox-label": "Salta all'istante di tempo specificato (in secondi / min:sec). Usa +/- per una ricerca relativa.",
    "ready-tooltip": "Indica quando sei pronto a guardare.",
    "autoplay-tooltip": "Avvia la riproduzione automatica quando il numero minimo di utenti è pronto.",
    "switch-to-file-tooltip": "Doppio click per passare a {}",  # Filename
    "sendmessage-tooltip": "Invia il messaggio alla stanza",

    # In-userlist notes (GUI)
    "differentsize-note": "Dimensione file diversa!",
    "differentsizeandduration-note": "Durata e dimensione file diversi!",
    "differentduration-note": "Durata diversa!",
    "nofile-note": "(Nessun file in riproduzione)",

    # Server messages to client
    "new-syncplay-available-motd-message": "Stai usando Syncplay {} ma una nuova versione è disponibile presso https://syncplay.pl",  # ClientVersion

    # Server notifications
    "welcome-server-notification": "Benvenuto nel server Syncplay, ver. {0}",  # version
    "client-connected-room-server-notification": "{0}({2}) connesso alla stanza '{1}'",  # username, host, room
    "client-left-server-notification": "{0} ha lasciato il server",  # name
    "no-salt-notification": "NOTA BENE: In futuro, per consentire il corretto funzionamento delle password generate da questo server (per le stanze gestite), aggiungi da linea di comando il seguente argomento prima di avviare il server Syncplay: --salt {}",  # Salt


    # Server arguments
    "server-argument-description": 'Programma per sincronizzare la riproduzione di media player multipli attraverso la rete. Modulo server.',
    "server-argument-epilog": 'Se non è specificata alcuna opzione saranno utilizzati i valori _config',
    "server-port-argument": 'Porta TCP del server',
    "server-password-argument": 'password del server',
    "server-isolate-room-argument": 'Mantiene le stanze isolate',
    "server-salt-argument": "usare stringhe casuali per generare le password delle stanze gestite",
    "server-disable-ready-argument": "disabilita la funzionalità \"pronto\"",
    "server-motd-argument": "percorso del file da cui verrà letto il messaggio del giorno",
    "server-chat-argument": "abilita o disabilita la chat",
    "server-chat-maxchars-argument": "Numero massimo di caratteri in un messaggio di chat (default è {})", # Default number of characters
    "server-maxusernamelength-argument": "Numero massimo di caratteri in un nome utente (default è {})",
    "server-stats-db-file-argument": "Abilita la raccolta dei dati statistici nel file SQLite indicato",
    "server-startTLS-argument": "Abilita il protocollo TLS usando i certificati contenuti nel percorso indicato",
    "server-messed-up-motd-unescaped-placeholders": "Il messaggio del giorno ha dei caratteri non 'escaped'. Tutti i simboli $ devono essere doppi ($$).",
    "server-messed-up-motd-too-long": "Il messaggio del giorno è troppo lungo - numero massimo di caratteri è {}, {} trovati.",

    # Server errors
    "unknown-command-server-error": "Comando non riconosciuto {}",  # message
    "not-json-server-error": "Non è una stringa in codifica JSON {}",  # message
    "line-decode-server-error": "Non è una stringa utf-8",
    "not-known-server-error": "Devi essere autenticato dal server prima di poter inviare questo comando",
    "client-drop-server-error": "Il client è caduto: {} -- {}",  # host, error
    "password-required-server-error": "È richiesta una password",
    "wrong-password-server-error": "La password inserita è errata",
    "hello-server-error": "Not enough Hello arguments",  # DO NOT TRANSLATE

    # Playlists
    "playlist-selection-changed-notification": "{} ha cambiato il file selezionato nella playlist",  # Username
    "playlist-contents-changed-notification": "{} ha aggiornato la playlist",  # Username
    "cannot-find-file-for-playlist-switch-error": "Impossibile trovare il file {} nelle cartelle multimediali per permettere il cambio di file tramite la playlist!",  # Filename
    "cannot-add-duplicate-error": "Impossibile aggiungere una seconda voce per '{}' alla playlist. Non è possibile avere file duplicati.",  # Filename
    "cannot-add-unsafe-path-error": "Impossibile caricare automaticamente {} perché non è presente nei domini fidati. Puoi passare all'inserimento manuale facendo doppio click sull'indirizzo nella playlist, oppure aggiungerlo ai domini fidati tramite File->Avanzate->Imposta domini fidati. Cliccando col tasto destro del mouse su un indirizzo puoi impostare il suo dominio come fidato tramite il menù contestuale.",  # Filename
    "sharedplaylistenabled-label": "Abilita le playlist condivise",
    "removefromplaylist-menu-label": "Rimuovi dalla playlist",
    "shuffleremainingplaylist-menu-label": "Mescola i file non ancora riprodotti",
    "shuffleentireplaylist-menu-label": "Mescola l'intera playlist",
    "undoplaylist-menu-label": "Annulla l'ultima modifica alla playlist",
    "addfilestoplaylist-menu-label": "Aggiungi un file alla fine della playlist",
    "addurlstoplaylist-menu-label": "Aggiungi un indirizzo alla fine della playlist",
    "editplaylist-menu-label": "Modifica la playlist",

    "open-containing-folder": "Apri la cartella contenente questo file",
    "addyourfiletoplaylist-menu-label": "Aggiungi il tuo file alla playlist",
    "addotherusersfiletoplaylist-menu-label": "Aggiungi il file di {} alla playlist", # Username
    "addyourstreamstoplaylist-menu-label": "Aggiungi il tuo indirizzo alla playlist",
    "addotherusersstreamstoplaylist-menu-label": "Aggiungi l'indirizzo di {} alla playlist", # Username  # item owner indicator
    "openusersstream-menu-label": "Apri l'indirizzo di {}",  # [username]
    "openusersfile-menu-label": "Apri il file di {}",  # [username]'s

    "playlist-instruction-item-message": "Trascina qui i file per aggiungerli alla playlist condivisa.",
    "sharedplaylistenabled-tooltip": "Gli operatori della stanza possono aggiungere i file a una playlist sincronizzata per garantire che tutti i partecipanti stiano guardando la stessa cosa. Configura le cartelle multimediali alla voce 'Miscellanea'.",

    "playlist-empty-error": "Playlist is currently empty.",  # TO DO: Translate
    "playlist-invalid-index-error": "Invalid playlist index", # TO DO: Translate
}
