# coding:utf8

"""Italian dictionary"""

it = {
    "LANGUAGE" : u"Italiano",

    # Client notifications
    "config-cleared-notification" : u"Impostazioni resettate. I cambiamenti saranno memorizzati quando salverai una configurazione valida.",

    "relative-config-notification" : u"Caricato i file di configurazione relativi: {}",

    "connection-attempt-notification" : u"Tentativo di connessione a {}:{}",  # Port, IP
    "reconnection-attempt-notification" : u"Connessione col server persa, tentativo di riconnesione in corso",
    "disconnection-notification" : u"Disconnesso dal server",
    "connection-failed-notification" : u"Connessione col server fallita",
    "connected-successful-notification" : u"Connessione al server effettuata con successo",
    "retrying-notification" : u"%s, Nuovo tentativo in %d secondi...",  # Seconds

    "rewind-notification" : u"Riavvolgo a causa della differenza temporale con {}",  # User
    "fastforward-notification" : u"Avanzamento rapido a causa della differenza temporale con {}",  # User
    "slowdown-notification" : u"Rallento a causa della differenza temporale con {}",  # User
    "revert-notification" : u"Velocità di riproduzione normale ripristinata",

    "pause-notification" : u"{} ha messo in pausa",  # User
    "unpause-notification" : u"{} ha ripreso la riproduzione",  # User
    "seek-notification" : u"{} è passato da {} a {}",  # User, from time, to time

    "current-offset-notification" : u"Offset corrente: {} secondi",  # Offset

    "media-directory-list-updated-notification" : u"Le cartelle multimediali di Syncplay sono state aggiornate.",

    "room-join-notification" : u"{} è entranto nella stanza: '{}'",  # User
    "left-notification" : u"{} ha abbandonato",  # User
    "left-paused-notification" : u"{} ha abbandonato, {} ha messo in pausa",  # User who left, User who paused
    "playing-notification" : u"{} sta riproducendo '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum" :  u" nella stanza: '{}'",  # Room

    "not-all-ready" : u"Non pronti: {}", # Usernames
    "all-users-ready" : u"Tutti i partecipanti sono pronti ({} utenti)", #Number of ready users
    "ready-to-unpause-notification" : u"Ora sei pronto - premi ancora una volta il tasto pausa per riprendere la riproduzione",
    "set-as-ready-notification" : u"Ora sei pronto",
    "set-as-not-ready-notification" : u"Non sei pronto",
    "autoplaying-notification" : u"Riproduzione automatica in {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification" : u"Identificato come gestore della stanza con password '{}'...",
    "failed-to-identify-as-controller-notification" : u"{} ha fallito l'identificazione come gestore della stanza.",
    "authenticated-as-controller-notification" : u"{} autenticato come gestore della stanza",
    "created-controlled-room-notification" : u"Stanza gestita '{}' creata con password '{}'. Per favore salva queste informazioni per una consultazione futura!", # RoomName, operatorPassword

    "file-different-notification" : u"Il file che stai riproducendo sembra essere diverso da quello di {}",  # User
    "file-differences-notification" : u"Il tuo file mostra le seguenti differenze: {}", # Differences
    "room-file-differences" : u"Differenze nel tuo file: {}", # File differences (filename, size, and/or duration)
    "file-difference-filename" : u"nome",
    "file-difference-filesize" : u"dimensione",
    "file-difference-duration" : u"durata",
    "alone-in-the-room": u"Non ci sono altri utenti nella stanza",

    "different-filesize-notification" : u" (la dimensione del tuo file è diversa da quella degli altri partecipanti!)",
    "userlist-playing-notification" : u"{} sta riproducendo:", #Username
    "file-played-by-notification" : u"File: {} è in riproduzione da:",  # File
    "no-file-played-notification" : u"{} non sta riproducendo alcun file", # Username
    "notplaying-notification" : u"Partecipanti che non stanno riproducendo alcun file:",
    "userlist-room-notification" :  u"Nella stanza '{}':",  # Room
    "userlist-file-notification" : u"File",
    "controller-userlist-userflag" : u"Gestore",
    "ready-userlist-userflag" : u"Pronto",

    "update-check-failed-notification" : u"Controllo automatico degli aggiornamenti di Syncplay {} fallito. Vuoi visitare http://syncplay.pl/ per verificare manualmente la presenza di aggiornamenti?", #Syncplay version
    "syncplay-uptodate-notification" : u"Syncplay è aggiornato",
    "syncplay-updateavailable-notification" : u"Una nuova versione di Syncplay è disponibile. Vuoi visitare la pagina delle release?",

    "mplayer-file-required-notification" : u"Utilizzare Syncplay con mplayer di selezionare il file all'avvio",
    "mplayer-file-required-notification/example" : u"Esempio di utilizzo: syncplay [opzioni] [url|percorso/]nomefile",
    "mplayer2-required" : u"Syncplay non è compatibile con MPlayer 1.x, per favore utilizza mplayer2 or mpv",

    "unrecognized-command-notification" : u"Comando non riconosciuto",
    "commandlist-notification" : u"Comandi disponibili:",
    "commandlist-notification/room" : u"\tr [nome] - cambia stanza",
    "commandlist-notification/list" : u"\tl - mostra la lista di utenti",
    "commandlist-notification/undo" : u"\tu - annulla l'ultima ricerca",
    "commandlist-notification/pause" : u"\tp - attiva o disattiva la pausa",
    "commandlist-notification/seek" : u"\t[s][+-]tempo - salta all'istante di tempo dato, se + o - non è specificato si considera il tempo assoluto in secondi o min:sec",
    "commandlist-notification/help" : u"\th - mostra questo help",
    "commandlist-notification/toggle" : u"\tt - attiva o disattiva lo stato 'Pronto'",
    "commandlist-notification/create" : u"\tc [nome] - crea una stanza gestita usando il nome della stanza attuale",
    "commandlist-notification/auth" : u"\ta [password] - autentica come gestore della stanza, utilizzando la password del gestore",
    "commandlist-notification/chat" : u"\tch [message] - invia un messaggio nella chat della stanza",
    "syncplay-version-notification" : u"Versione di Syncplay: {}",  # syncplay.version
    "more-info-notification" : u"Maggiori informazioni a: {}",  # projectURL

    "gui-data-cleared-notification" : u"Syncplay ha resettato i dati dell'interfaccia relativi ai percorsi e allo stato delle finestre.",
    "language-changed-msgbox-label" : u"La lingua sarà cambiata quando avvierai Syncplay.",
    "promptforupdate-label" : u"Ti piacerebbe che, di tanto in tanto, Syncplay controllasse automaticamente la presenza di aggiornamenti?",

    "vlc-interface-version-mismatch": u"Stai eseguendo la versione {} del modulo di interfaccia per VLC di Syncplay, ma Syncplay è progettato per essere utilizzato con la versione {} o superiore. Per favore, fai riferimento alla User Guide di Syncplay presso http://syncplay.pl/guide/ per istruzioni su come installare syncplay.lua.",  # VLC interface version, VLC interface min version
    "vlc-interface-oldversion-warning": u"Attenzione: Syncplay ha rilevato una vecchia versione del modulo di interfaccia per VLC di Syncplay installata nella cartella di VLC. Per favore, fai riferimento alla User Guide di Syncplay presso http://syncplay.pl/guide/ per istruzioni su come installare syncplay.lua.",
    "media-player-latency-warning": u"Attenzione: il media player ha impiegato {} secondi per rispondere. Se stai avendo problemi di sincronizzazione, chiudi delle applicazioni per liberare le risorse di sistema e, se ciò non dovesse avere alcun effetto, prova un altro media player.", # Seconds to respond
    "vlc-interface-not-installed": u"Attenzione: il modulo di interfaccia per VLC di Syncplay non è stato trovato nella cartella di VLC. Se stai utilizzando VLC 2.0, VLC userà il modulo syncplay.lua contenuto nella cartella di Syncplay, ma ciò significa che altri custom script di interfaccia ed estensioni non funzioneranno. Per favore, fai riferimento alla User Guide di Syncplay presso http://syncplay.pl/guide/ per istruzioni su come installare syncplay.lua.",
    "mpv-unresponsive-error": u"mpv non ha risposto per {} secondi, quindi sembra non funzionare correttamente. Per favore, riavvia Syncplay.", # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt" : u"Premi Invio per uscire\n",

    # Client errors
    "missing-arguments-error" : u"Alcuni argomenti obbligatori non sono stati trovati. Fai riferimento a --help",
    "server-timeout-error" : u"Connessione col server scaduta",
    "mpc-slave-error" : u"Non è possibile avviare MPC in modalità slave!",
    "mpc-version-insufficient-error" : u"La tua versione di MPC è troppo vecchia, per favore usa `mpc-hc` >= `{}`",
    "mpc-be-version-insufficient-error" : u"La tua versione di MPC è troppo vecchia, per favore usa `mpc-be` >= `{}`",
    "mpv-version-error" : u"Syncplay non è compatibile con questa versione di mpv. Per favore usa un'altra versione di mpv (es. Git HEAD).",
    "player-file-open-error" : u"Il player non è riuscito ad aprire il file",
    "player-path-error" : u"Il path del player non è configurato correttamente. I player supportati sono: mpv, VLC, MPC-HC, MPC-BE e mplayer2",
    "hostname-empty-error" : u"Il campo hostname non può essere vuoto",
    "empty-error" : u"Il campo {} non può esssere vuoto",  # Configuration
    "media-player-error": u"Errore media player: \"{}\"",  # Error line
    "unable-import-gui-error": u"Non è possibile importare le librerie di interfaccia grafica. Hai bisogno di PySide per poter utilizzare l'interfaccia grafica.",

    "arguments-missing-error" : u"Alcuni argomenti obbligatori non sono stati trovati. Fai riferimento a --help",

    "unable-to-start-client-error" : u"Impossibile avviare il client",

    "player-path-config-error": u"Il percorso del player non è configurato correttamente. I player supportati sono: mpv, VLC, MPC-HC, MPC-BE e mplayer2.",
    "no-file-path-config-error" :u"Deve essere selezionato un file prima di avviare il player",
    "no-hostname-config-error": u"Il campo hostname non può essere vuoto",
    "invalid-port-config-error" : u"La porta deve essere valida",
    "empty-value-config-error" : u"Il campo {} non può essere vuoto", # Config option

    "not-json-error" : u"Non è una stringa con codifica JSON\n",
    "hello-arguments-error" : u"Argomenti Hello non sufficienti\n",
    "version-mismatch-error" : u"La versione del client è diversa da quella del server\n",
    "vlc-failed-connection": u"Impossibile collegarsi a VLC. Se non hai installato syncplay.lua e stai usando l'ultima versione di VLC, fai riferimento a http://syncplay.pl/LUA/ per istruzioni.",
    "vlc-failed-noscript": u"VLC ha segnalato che lo script di interfaccia syncplay.lua non è stato installato. Per favore, fai riferimento a http://syncplay.pl/LUA/ per istruzioni.",
    "vlc-failed-versioncheck": u"Questa versione di VLC non è supportata da Syncplay.",

    "feature-sharedPlaylists" : u"playlist condivise", # used for not-supported-by-server-error
    "feature-chat" : u"chat", # used for not-supported-by-server-error
    "feature-readiness" : u"pronto", # used for not-supported-by-server-error
    "feature-readiness" : u"pronto", # used for not-supported-by-server-error
    "feature-managedRooms" : u"stanze gestite", # used for not-supported-by-server-error

    "not-supported-by-server-error" : u"La feature {} non è supportata da questo server..", #feature
    "shared-playlists-not-supported-by-server-error" : u"Le playlist condivise potrebbero non essere supportata dal server. È necessario un server con Syncplay {}+ per assicurarsi che funzionino correttamente, tuttavia il server sta utilizzando Syncplay {}.", #minVersion, serverVersion
    "shared-playlists-disabled-by-server-error" : u"Le playlist condivise sono state disabilitate nella configurazione del server. Per utilizzarle, dovrai collegarti a un altro server.",

    "invalid-seek-value" : u"Valore di ricerca non valido",
    "invalid-offset-value" : u"Valore di offset non valido",

    "switch-file-not-found-error" : u"Impossibile selezionare il file '{0}'. Syncplay osserva solo le cartelle multimediali specificate.", # File not found
    "folder-search-timeout-error" : u"La ricerca nelle cartelle multimediali è stata interrotta perché l'analisi di '{}' sta impiegando troppo tempo. Ciò accade se si aggiunge nella lista di ricerca una cartella con troppe sottocartelle. Per riabilitare la selezione automatica dei file seleziona File->Imposta cartelle multimediali nella barra dei menù e rimuovi questa cartella, o sostituiscila con una sottocartella appropriata. Se la cartella è idonea, è possibile riabilitarla selezionando File->Imposta cartelle multimediali e premendo 'OK'.", #Folder
    "folder-search-first-file-timeout-error" : u"La ricerca dei media in '{}' è stata interrotta perché l'accesso alla cartella sta impiegando troppo tempo. Ciò accade se questa si trova in un disco di rete oppure se hai impostato il blocco della rotazione del disco rigido dopo un certo periodo di inattività. Per riabilitare la selezione automatica dei file seleziona File->Imposta cartelle multimediali, quindi rimuovi la cartella oppure risolvi il problema (es. cambiando le impostazioni di risparmio energetico).", #Folder
    "added-file-not-in-media-directory-error" : u"Hai selezionato un file in '{}', che non è impostata come cartella multimediale. Puoi aggiungerla come cartella multimediale selezionando File->Imposta cartelle multimediali nella barra dei menù.", #Folder
    "no-media-directories-error" : u"Nessuna cartella multimediale è stata configurata. Per permettere il corretto funzionamento delle playlist condivise e la selezione automatica dei file, naviga in File->Imposta cartelle multimediali e specifica dove Syncplay deve ricercare i file multimediali.",
    "cannot-find-directory-error" : u"Impossibile trovare la cartella multimediale '{}'. Per aggiornare la lista delle cartelle multimediali seleziona File->Imposta cartelle multimediali dalla barra dei menù e specifica dove Syncplay deve ricercare i file multimediali.",

    "failed-to-load-server-list-error" : u"Impossibile caricare la lista dei server pubblici. Per favore, visita http://www.syncplay.pl/ con il tuo browser.",

    # Client arguments
    "argument-description" : u'Programma per sincronizzare la riproduzione di media player multipli attraverso la rete.',
    "argument-epilog" : u'Se non è specificata alcuna opzione saranno utilizzati i valori _config',
    "nogui-argument" : u'non mostrare l\'interfaccia grafica',
    "host-argument" : u'indirizzo del server',
    "name-argument" : u'username desiderato',
    "debug-argument" : u'modalità debug',
    "force-gui-prompt-argument" : u'mostra la finestra di configurazione',
    "no-store-argument" : u'non salvare i valori in .syncplay',
    "room-argument" : u'stanza di default',
    "password-argument" : u'password del server',
    "player-path-argument" : u'percorso dell\'eseguibile del tuo player',
    "file-argument" : u'file da riprodurre',
    "args-argument" : u'opzioni del player, se hai bisogno di utilizzare opzioni che iniziano con - anteponi un singolo \'--\'',
    "clear-gui-data-argument" : u'resetta il percorso e i dati impostati tramite interfaccia grafica e salvati come QSettings',
    "language-argument" : u'lingua per i messaggi di Syncplay (de/en/ru/it)',

    "version-argument" : u'mostra la tua versione',
    "version-message" : u"Stai usando la versione di Syncplay {} ({})",

    # Client labels
    "config-window-title" : u"Configurazione di Syncplay",

    "connection-group-title" : u"Impostazioni di connessione",
    "host-label" : u"Indirizzo del server: ",
    "name-label" : u"Username (opzionale):",
    "password-label" : u"Password del server (se necessaria):",
    "room-label" : u"Stanza di default: ",

    "media-setting-title" : u"Impostazioni del media player",
    "executable-path-label" : u"Percorso del media player:",
    "media-path-label" : u"Percorso del video (opzionale):",
    "player-arguments-label" : u"Opzioni del player (se necessarie):",
    "browse-label" : u"Sfoglia",
    "update-server-list-label" : u"Aggiorna lista",

    "more-title" : u"Mostra altre impostazioni",
    "never-rewind-value" : u"Mai",
    "seconds-suffix" : u" sec",
    "privacy-sendraw-option" : u"Invio semplice",
    "privacy-sendhashed-option" : u"Invio cifrato",
    "privacy-dontsend-option" : u"Non inviare",
    "filename-privacy-label" : u"Nome del file:",
    "filesize-privacy-label" : u"Dimensione del file:",
    "checkforupdatesautomatically-label" : u"Controlla automaticamente gli aggiornamenti di Syncplay",
    "slowondesync-label" : u"Rallenta in caso di sfasamento minimo (non supportato su MPC-HC/BE)",
    "rewindondesync-label" : u"Riavvolgi in caso di grande sfasamento (consigliato)",
    "fastforwardondesync-label" : u"Avanzamento rapido in caso di ritardo (consigliato)",
    "dontslowdownwithme-label" : u"Non rallentare o riavvolgere gli altri utenti (sperimentale)",
    "pausing-title" : u"Pausa",
    "pauseonleave-label" : u"Metti in pausa quando gli altri utenti abbandonano (es. disconnessione)",
    "readiness-title" : u"Stato iniziale di 'pronto'",
    "readyatstart-label" : u"Impostami sempre su 'pronto a guardare'",
    "forceguiprompt-label" : u"Non mostrare la finestra di configurazione di Syncplay a ogni apertura", # (Inverted)
    "showosd-label" : u"Abilita i messaggi OSD",

    "showosdwarnings-label" : u"Mostra gli avvisi (es. file differenti, utenti non pronti)",
    "showsameroomosd-label" : u"Mostra gli eventi della tua stanza",
    "shownoncontrollerosd-label" : u"Mostra gli eventi dei non gestori nelle stanze gestite",
    "showdifferentroomosd-label" : u"Mostra gli eventi di altre stanze",
    "showslowdownosd-label" : u"Mostra le notifiche di rallentamento / riavvolgimento",
    "language-label" : u"Lingua:",
    "automatic-language" : u"Predefinita ({})", # Default language
    "showdurationnotification-label" : u"Avvisa in caso di mancata corrispondenza della durata del file",
    "basics-label" : u"Generali",
    "readiness-label" : u"Play/Pausa",
    "misc-label" : u"Varie",
    "core-behaviour-title" : u"Comportamento principale della stanza",
    "syncplay-internals-title" : u"Funzionamento di Syncplay",
    "syncplay-mediasearchdirectories-title" : u"Cartelle contenenti i file multimediali",
    "syncplay-mediasearchdirectories-label" : u"Cartelle contenenti i file multimediali (un solo percorso per riga)",    
    "sync-label" : u"Sincronia", # don't have better options as the label won't fit in the panel.
    "sync-otherslagging-title" : u"Se gli altri partecipanti non sono sincronizzati...",
    "sync-youlaggging-title" : u"Se tu sei non sei sincronizzato...",
    "messages-label" : u"Messaggi",
    "messages-osd-title" : u"Impostazioni On-screen Display",
    "messages-other-title" : u"Altre impostazioni dello schermo",
    "chat-label" : u"Chat",
    "privacy-label" : u"Privacy", # Currently unused, but will be brought back if more space is needed in Misc tab
    "privacy-title" : u"Impostazioni privacy",
    "unpause-title" : u"Premendo play, imposta il tuo stato su pronto e:",
    "unpause-ifalreadyready-option" : u"Riprendi la riproduzione se eri già pronto",
    "unpause-ifothersready-option" : u"Riprendi la riproduzione se eri già pronto o se gli altri partecipanti sono pronti (default)",
    "unpause-ifminusersready-option" : u"Riprendi la riproduzione se eri già pronto o se un numero minimo di partecipanti è pronto",
    "unpause-always" : u"Riprendi sempre la riproduzione",
    "syncplay-trusteddomains-title": u"Domini fidati (per streaming e i contenuti in rete)",

    "chat-title" : u"Inserimento messaggi di chat",
    "chatinputenabled-label" : u"Abilita la chat su mpv",
    "chatdirectinput-label" : u"Abilita la chat istantanea (evita di dover premere Invio per chattare)",
    "chatinputfont-label" : u"Font dell'input della chat",
    "chatfont-label" : u"Imposta font",
    "chatcolour-label" : u"Imposta colore",
    "chatinputposition-label" : u"Posizione dell'area di inserimento testo in mpv",
    "chat-top-option" : u"In alto",
    "chat-middle-option" : u"Al centro",
    "chat-bottom-option" : u"In basso",
    "chatoutputheader-label" : u"Output messaggi di chat",
    "chatoutputfont-label": u"Font dell'output della chat",
    "chatoutputenabled-label": u"Abilita l'output della chat nel media player (al momento solo mpv è supportato)",
    "chatoutputposition-label": u"Modalità di output",
    "chat-chatroom-option": u"Stile chatroom",
    "chat-scrolling-option": u"A scorrimento",

    "mpv-key-tab-hint": u"[TAB] to toggle access to alphabet row key shortcuts.", # TODO needs to clarify this
    "mpv-key-hint": u"[Invio] per inviare un messaggio. [Esc] per uscire dalla modalità chat.",
    "alphakey-mode-warning-first-line": u"Puoi utilizzare temporaneamente i vecchi comandi di mpv con i tasti a-z.",
    "alphakey-mode-warning-second-line": u"Premi [TAB] per ritornare alla modalità chat di Syncplay.",

    "help-label" : u"Aiuto",
    "reset-label" : u"Impostazioni iniziali",
    "run-label" : u"Avvia Syncplay",
    "storeandrun-label" : u"Salva la configurazione e avvia Syncplay",

    "contact-label" : u"Sentiti libero di inviare un'e-mail a <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a>, chattare tramite il <a href=\"https://webchat.freenode.net/?channels=#syncplay\"><nobr>canale IRC #Syncplay</nobr></a> su irc.freenode.net, <a href=\"https://github.com/Uriziel/syncplay/issues\"><nobr>segnalare un problema</nobr></a> su GitHub, <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>lasciare un like sulla nostra pagina Facebook</nobr></a>, <a href=\"https://twitter.com/Syncplay/\"><nobr>seguirci su Twitter</nobr></a>, o visitare <a href=\"http://syncplay.pl/\"><nobr>http://syncplay.pl/</nobr></a>. NOTA: i messaggi di chat non sono cifrati, quindi non usare Syncplay per inviare dati sensibili.",

    "joinroom-label" : u"Entra nella stanza",
    "joinroom-menu-label" : u"Entra nella stanza {}",
    "seektime-menu-label" : u"Vai a...",
    "undoseek-menu-label" : u"Annulla vai a...",
    "play-menu-label" : u"Play",
    "pause-menu-label" : u"Pausa",
    "playbackbuttons-menu-label" : u"Mostra i controlli della riproduzione",
    "autoplay-menu-label" : u"Mostra il tasto di riproduzione automatica",
    "autoplay-guipushbuttonlabel" : u"Riproduci quando tutti sono pronti",
    "autoplay-minimum-label" : u"Minimo utenti pronti:",

    "sendmessage-label" : u"Invia",

    "ready-guipushbuttonlabel" : u"Sono pronto a guardare!",

    "roomuser-heading-label" : u"Stanza / Utente",
    "size-heading-label" : u"Dimensione",
    "duration-heading-label" : u"Durata",
    "filename-heading-label" : u"Nome del file",
    "notifications-heading-label" : u"Notifiche",
    "userlist-heading-label" : u"Lista degli utenti nella stanza",

    "browseformedia-label" : u"Seleziona i file multimediali",

    "file-menu-label" : u"&File", # & precedes shortcut key
    "openmedia-menu-label" : u"&Apri file multimediali",
    "openstreamurl-menu-label" : u"Apri indirizzo di &rete",
    "setmediadirectories-menu-label" : u"Imposta &cartelle multimediali",
    "exit-menu-label" : u"&Esci",
    "advanced-menu-label" : u"&Avanzate",
    "window-menu-label" : u"&Finestra",
    "setoffset-menu-label" : u"Imposta &offset",
    "createcontrolledroom-menu-label" : u"&Crea stanza gestita",
    "identifyascontroller-menu-label" : u"&Identificati come operatore della stanza",
    "settrusteddomains-menu-label" : u"Imposta &domini fidati",
    "addtrusteddomain-menu-label" : u"Aggiungi {} come dominio fidato", # Domain

    "playback-menu-label" : u"&Riproduzione",

    "help-menu-label" : u"&Aiuto",
    "userguide-menu-label" : u"Apri guida &utente",
    "update-menu-label" : u"Controlla la presenza di &aggiornamenti",

    #About dialog
    "about-menu-label": u"&Informazioni su Syncplay",
    "about-dialog-title": u"Informazioni su Syncplay",
    "about-dialog-release": u"Versione {} release {} con {}",
    "about-dialog-license-text" : u"Rilasciato sotto Apache&nbsp;License,&nbsp;Version 2.0",
    "about-dialog-license-button": u"Licenza",
    "about-dialog-dependencies": u"Dipendenze",

    "setoffset-msgbox-label" : u"Imposta offset",
    "offsetinfo-msgbox-label" : u"Offset (vedi http://syncplay.pl/guide/ per istruzioni):",

    "promptforstreamurl-msgbox-label" : u"Apri URL",
    "promptforstreamurlinfo-msgbox-label" : u"Indirizzo di rete",

    "addfolder-label" : u"Aggiungi cartella",

    "adduris-msgbox-label" : u"Aggiungi gli indirizzi alla playlist (uno per riga)",
    "editplaylist-msgbox-label" : u"Imposta playlist (una per riga)",
    "trusteddomains-msgbox-label" : u"Domini a cui è lecito passare automaticamente (uno per riga)",

    "createcontrolledroom-msgbox-label" : u"Crea stanza gestita",
    "controlledroominfo-msgbox-label" : u"Inserisci il nome della stanza gestita\r\n(vedi http://syncplay.pl/guide/ per istruzioni):",

    "identifyascontroller-msgbox-label" : u"Identificati come operatore della stanza",
    "identifyinfo-msgbox-label" : u"Inserisci la password dell'operatore per questa stanza\r\n(vedi http://syncplay.pl/guide/ per istruzioni):",

    "public-server-msgbox-label" : u"Seleziona il server pubblico per questa sessione",

    "megabyte-suffix" : u" MB",

    # Tooltips

    "host-tooltip" : u"Hostname o indirizzo IP a cui collegarsi e, se necessario, includere la porta (es. syncplay.pl:8999). La sincronizzazione avviene solo con gli utenti collegati allo stesso server/porta.",
    "name-tooltip" : u"Il nome utente con cui sarai riconosciuto. Nessuna registrazione necessaria, cosi potrai sempre cambiarlo. Se lasciato vuoto, viene scelto un nome casuale.",
    "password-tooltip" : u"La password è necessaria solo in caso di connessione a server privati.",
    "room-tooltip" : u"La stanza in cui entrare dopo la connessione. Può assumere qualsiasi nome, ma ricorda che sarai sincronizzato solo con gli utenti nella stessa stanza.",

    "executable-path-tooltip" : u"Percorso del media player desiderato (scegliere tra mpv, VLC, MPC-HC/BE or mplayer2).",
    "media-path-tooltip" : u"Percorso del video o stream da aprire. Necessario per mplayer2.",
    "player-arguments-tooltip" : u"Argomenti da linea di comando aggiuntivi da passare al media player scelto.",
    "mediasearcdirectories-arguments-tooltip" : u"Cartelle dove Syncplay cercherà i file multimediali, es. quando usi la funzione click to switch. Syncplay cercherà anche nelle sottocartelle.",

    "more-tooltip" : u"Mostra le impostazioni usate meno frequentemente.",
    "filename-privacy-tooltip" : u"Modalità di invio al server del nome del file attualmente in riproduzione.",
    "filesize-privacy-tooltip" : u"Modalità di invio al server della dimensione del file attualmente in riproduzione.",
    "privacy-sendraw-tooltip" : u"Invia questa informazione in chiaro. Questa è l'impostazione predefinita per la maggior parte delle funzionalità.",
    "privacy-sendhashed-tooltip" : u"Invia una versione cifrata dell'informazione, rendendola meno visibile agli altri client.",
    "privacy-dontsend-tooltip" : u"Non inviare questa informazione al server. Questo garantisce massima privacy.",
    "checkforupdatesautomatically-tooltip" : u"Controlla regolarmente la presenza di nuove versioni di Syncplay.",
    "slowondesync-tooltip" : u"Riduce temporaneamente la velocità di riproduzione quando c'è bisogno di sincronizzarti con gli altri utenti. Non supportato su MPC-HC/BE.",
    "dontslowdownwithme-tooltip" : u"Gli altri utenti non vengono rallentati se non sei sincronizzato. Utile per i gestori della stanza.",
    "pauseonleave-tooltip" : u"Mette in pausa la riproduzione se vieni disconnesso o se qualcuno lascia la stanza.",
    "readyatstart-tooltip" : u"Imposta il tuo stato su 'pronto' all'avvio (in caso contrario, sarai su 'non pronto' finché non cambierai il tuo stato)",
    "forceguiprompt-tooltip" : u"La finestra di configurazione non viene mostrata quando apri Syncplay.",
    "nostore-tooltip" : u"Avvia Syncplay con la configurazione scelta, ma non salva le impostazioni.",
    "rewindondesync-tooltip" : u"Torna indietro quando necessario per ristabilire la sincronizzazione. Disabilitare quest'opzione può causare gravi problemi di sincronizzazione!",
    "fastforwardondesync-tooltip" : u"Avanza rapidamente quando non sei sincronizzato col gestore della stanza (o la tua posizione supposta se 'Non rallentare o riavvolgere gli altri utenti' è abilitato).",
    "showosd-tooltip" : u"Invia i messaggi di Syncplay all'OSD del media player.",
    "showosdwarnings-tooltip" : u"Mostra gli avvisi in caso di riproduzione di un file differente, se sei l'unico utente nella stanza, se ci sono utenti non pronti, ecc.",
    "showsameroomosd-tooltip" : u"Mostra le notifiche OSD per gli eventi relativi alla stanza in cui si trova l'utente.",
    "shownoncontrollerosd-tooltip" : u"Mostra le notifiche OSD per gli eventi relativi ai non operatori presenti nelle stanze gestite.",
    "showdifferentroomosd-tooltip" : u"Mostra le notifiche OSD per gli eventi relativi alle stanze in cui l'utente non si trova.",
    "showslowdownosd-tooltip" : u"Mostra le notifiche di rallentamento / riavvolgimento in caso di differenza temporale.",
    "showdurationnotification-tooltip" : u"Utile quando manca un segmento di un file multiparte. Può causare dei falsi positivi.",
    "language-tooltip" : u"Lingua da utilizzare in Syncplay.",
    "unpause-always-tooltip" : u"Se riprendi la riproduzione, il tuo stato cambia in 'pronto' e la riproduzione viene avviata, piuttosto che impostarti solo su pronto.",
    "unpause-ifalreadyready-tooltip" : u"Se riprendi la riproduzione quando non sei 'pronto', verrai impostato su pronto - ripeti il comando ancora una volta per avviare la riproduzione.",
    "unpause-ifothersready-tooltip" : u"Se riprendi la riproduzione quando non sei 'pronto' la riproduzione verrà avviata solo se gli altri sono pronti.",
    "unpause-ifminusersready-tooltip" : u"Se riprendi la riproduzione quando non sei 'pronto', la riproduzione verrà avviata solo se un numero minimo di utenti è 'pronto'.",
    "trusteddomains-arguments-tooltip" : u"Domini verso cui è possibile collegarsi automaticamente quando le playlist condivise sono abilitate.",

    "chatinputenabled-tooltip" : u"Abilita l'input della chat in mpv (premi Invio per chattare, per inviare ed Esc per cancellare)",
    "chatdirectinput-tooltip" : u"Evita di dover premere Invio per aprire l'input della chat in mpv. Premi TAB in mpv per disabilitare temporaneamente questa funzione.",
    "font-label-tooltip" : u"Font usato nell'input della chat in mpv. Non influenza cosa vedono gli altri, vale solo per te.",
    "set-input-font-tooltip" : u"Font usato nell'input della chat in mpv. Non influenza cosa vedono gli altri, vale solo per te.",
    "set-input-colour-tooltip" : u"Colore del font usato nell'input della chat in mpv. Non influenza cosa vedono gli altri, vale solo per te.",
    "chatinputposition-tooltip" : u"Posizione dell'input della chat in mpv quando premi Invio.",
    "chatinputposition-top-tooltip" : u"Posiziona l'input della chat in cima alla finestra di mpv.",
    "chatinputposition-middle-tooltip" : u"Posizione l'input della chat al centro della finestra di mpv.",
    "chatinputposition-bottom-tooltip" : u"Posiziona l'input della chat in basso alla finestra di mpv.",
    "chatoutputenabled-tooltip": u"Mostra i messaggi di chat nell'OSD (se supportato dal media player).",
    "font-output-label-tooltip": u"Font dell'output della chat.",
    "set-output-font-tooltip": u"Font usato per mostrare i messaggi di chat.",
    "chatoutputmode-tooltip": u"Come sono mostrati i messaggi di chat.",
    "chatoutputmode-chatroom-tooltip": u"Mostra i nuovi messaggi di chat al di sotto di quelli precedenti.",
    "chatoutputmode-scrolling-tooltip": u"Scorri il testo della chat da destra a sinistra.",

    "help-tooltip" : u"Apri la guida utente su Syncplay.pl.",
    "reset-tooltip" : u"Ripristina tutte le impostazioni.",
    "update-server-list-tooltip" : u"Scarica la lista dei server pubblici da syncplay.pl.",

    "joinroom-tooltip" : u"Abbandona la stanza attuale e entra in quella specificata.",
    "seektime-msgbox-label" : u"Salta all'istante di tempo specificato (in secondi / min:sec). Usa +/- per una ricerca relativa.",
    "ready-tooltip" : u"Indica quando sei pronto a guardare.",
    "autoplay-tooltip" : u"Riproduzione automatica quando il numero minimo di utenti è 'pronto'.",
    "switch-to-file-tooltip" : u"Doppio click per passare a {}", # Filename
    "sendmessage-tooltip" : u"Invia il messaggio alla stanza",

    # In-userlist notes (GUI)
    "differentsize-note" : u"Dimensione file diversa!",
    "differentsizeandduration-note" : u"Durata e dimensione file diversi!",
    "differentduration-note" : u"Durata diversa!",
    "nofile-note" : u"(Nessun file in riproduzione)",

    # Server messages to client
    "new-syncplay-available-motd-message" : u"<NOTICE> Stai usando Syncplay {} ma una nuova versione è disponibile presso http://syncplay.pl </NOTICE>",  # ClientVersion

    # Server notifications
    "welcome-server-notification" : u"Benvenuto nel server Syncplay, ver. {0}",  # version
    "client-connected-room-server-notification" : u"{0}({2}) connesso alla stanza '{1}'",  # username, host, room
    "client-left-server-notification" : u"{0} ha abbandonato il server",  # name
    "no-salt-notification" : u"NOTA BENE: In futuro, per consentire il corretto funzionamento delle password generate da questo server (per le stanze gestite), aggiungi da linea di comando il seguente argomento prima di avviare il server Syncplay: --salt {}", #Salt


    # Server arguments
    "server-argument-description" : u'Programma per sincronizzare la riproduzione di media player multipli attraverso la rete. Modulo server.',
    "server-argument-epilog" : u'Se non è specificata alcuna opzione saranno utilizzati i valori _config',
    "server-port-argument" : u'Porta TCP del server',
    "server-password-argument" : u'password del server',
    "server-isolate-room-argument" : u'Mantiene le stanze isolate',
    "server-salt-argument" : u"usare stringhe casuali per generare le password delle stanze gestite",
    "server-disable-ready-argument" : u"disabilita la funzionalità 'pronto'",
    "server-motd-argument": u"percorso del file da cui verrà letto il messaggio del giorno",
    "server-chat-argument" : u"abilita o disabilita la chat",
    "server-chat-maxchars-argument" : u"Numero massimo di caratteri in un messaggio di chat (default è {})", # Default number of characters
    "server-messed-up-motd-unescaped-placeholders": u"Il messaggio del giorno ha dei caratteri non 'escaped'. Tutti i simboli $ devono essere doppi ($$).",
    "server-messed-up-motd-too-long": u"Il messaggio del giorno è troppo lungo - numero massimo di caratteri è {}, {} trovati.",

    # Server errors
    "unknown-command-server-error" : u"Comando non riconosciuto {}",  # message
    "not-json-server-error" : u"Non è una stringa in codifica JSON {}",  # message
    "not-known-server-error" : u"Devi essere riconosciuto dal server prima di poter inviare questo comando",
    "client-drop-server-error" : u"Il client è caduto: {} -- {}",  # host, error
    "password-required-server-error" : u"È richiesta una password",
    "wrong-password-server-error" : u"La password inserita è errata",
    "hello-server-error" : u"Non ci sono abbastanza argomenti Hello",

    # Playlists
    "playlist-selection-changed-notification" : u"{} ha cambiato il file selezionato nella playlist", # Username
    "playlist-contents-changed-notification" : u"{} ha aggiornato la playlist", # Username
    "cannot-find-file-for-playlist-switch-error" : u"Impossibile trovare il file {} nelle cartelle multimediali per permettere il cambio di file tramite la playlist!", # Filename
    "cannot-add-duplicate-error" : u"Impossibile aggiungere una seconda voce per '{}' alla playlist. Non è possibile avere file duplicati.", #Filename
    "cannot-add-unsafe-path-error" : u"Impossibile caricare automaticamente {} perché non è presente nei domini fidati. Puoi passare all'inserimento manuale facendo doppio click sull'indirizzo nella playlist, oppure aggiungerlo ai domini fidati tramite File->Avanzate->Imposta domini fidati. Cliccando col tasto destro del mouse su un indirizzo puoi impostare il suo dominio come fidato tramite il menù contestuale.", # Filename
    "sharedplaylistenabled-label" : u"Abilita le playlist condivise",
    "removefromplaylist-menu-label" : u"Rimuovi dalla playlist",
    "shuffleremainingplaylist-menu-label" : u"Mescola i file non ancora riprodotti",
    "shuffleentireplaylist-menuu-label" : u"Mescola l'intera playlist",
    "undoplaylist-menu-label" : u"Annulla l'ultima modifica alla playlist",
    "addfilestoplaylist-menu-label" : u"Aggiungi un file alla fine della playlist",
    "addurlstoplaylist-menu-label" : u"Aggiungi un indirizzo alla fine della playlist",
    "editplaylist-menu-label": u"Modifica la playlist",

    "open-containing-folder": u"Apri la cartella contenente questo file",
    "addusersfiletoplaylist-menu-label" : u"Aggiungi il file {} alla playlist", # item owner indicator # TODO needs testing
    "addusersstreamstoplaylist-menu-label" : u"Aggiungi l'indirizzo {} alla playlist", # item owner indicator # TODO needs testing
    "openusersstream-menu-label" : u"Apri l'indirizzo di {}", # [username]'s
    "openusersfile-menu-label" : u"Apri il file di {}", # [username]'s
    "item-is-yours-indicator" : u"tuo", # Goes with addusersfiletoplaylist/addusersstreamstoplaylist # TODO needs testing
    "item-is-others-indicator" : u"di {}", # username - goes with addusersfiletoplaylist/addusersstreamstoplaylist # TODO needs testing

    "playlist-instruction-item-message" : u"Trascina qui i file per aggiungerli alla playlist condivisa.",
    "sharedplaylistenabled-tooltip" : u"Gli operatori della stanza possono aggiungere i file a una playlist sincronizzata per garantire che tutti i partecipanti stiano guardando la stessa cosa. Configura le cartelle multimediali alla voce 'Miscellanea'.",
}
