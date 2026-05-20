# coding:utf8

"""Esperanto dictionary"""

# Filename, dictionary name and LANGUAGE-TAG value based on ISO country code. Language tag listed at https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/a9eac961-e77d-41a6-90a5-ce1a8b0cdb9c?redirectedfrom=MSDN

# Komentoj kun tradukistaj notoj komenciĝas per «FARU:».

eo = {
    "LANGUAGE": "Esperanto",
    "LANGUAGE-TAG": "eo",

    # Strings for Windows NSIS installer
    "installer-language-file": "Esperanto.nlf", # Relevant .nlf file at https://github.com/kichik/nsis/tree/master/Contrib/Language%20files
    "installer-associate": "Asocii vidaŭdaĵajn dosierojn kun Syncplay.",
    "installer-shortcut": "Krei mallongigojn en la jenaj lokoj:",
    "installer-start-menu": "Start-menuo",
    "installer-desktop": "Labortablo",
    "installer-quick-launch-bar": "Tujbreto",
    "installer-automatic-updates": "Kontroli ĝisdatigojn memage",
    "installer-uninstall-configuration": "Forigi dosieron kun agordaro.",

    # Client notifications
    "config-cleared-notification": "Agordoj vakiĝis. Ŝanĝoj konserviĝos kiam vi enmemorigos validan agordaron.",

    "relative-config-notification": "Enlegis rilatajn agordajn dosierojn: {}", # FARU: originale «relative» – ĉu «rilataj»?

    "connection-attempt-notification": "Provas konektiĝi al {}:{}",  # Port, IP
    "reconnection-attempt-notification": "Konekto al servilo perdiĝis; provas rekonektiĝi",
    "reconnect-menu-triggered-notification": "Mana rekonekto iniciatita - provos novan konekton al {}:{} post 2 sekundoj...",
    "reconnect-failed-no-host-error": "Ne eblas rekonektiĝi: neniu servila informo disponebla",
    "reconnect-failed-no-port-error": "Ne eblas rekonektiĝi: nevalida servila agordo",
    "reconnect-failed-error": "Rekonekto malsukcesis: {}",
    "disconnection-notification": "Malkonektiĝis de servilo",
    "connection-failed-notification": "Konekto al servilo malsukcesis",
    "connected-successful-notification": "Sukcese konektiĝis al servilo",
    "retrying-notification": "%s, reprovos post %d sekundoj…",  # Seconds
    "reachout-successful-notification": "Sukcese atingis al {} ({})",

    "rewind-notification": "Reiris pro tempa malakordo kun {}",  # User
    "fastforward-notification": "Pluiris pro tempa malakordo kun {}",  # User
    "slowdown-notification": "Malrapidiĝas pro tempa malakordo kun {}",  # User
    "revert-notification": "Rerapidiĝas",

    "pause-notification": "{} paŭzigis je {}",  # User, Time
    "unpause-notification": "{} malpaŭzigis",  # User
    "seek-notification": "{} saltis de {} al {}",  # User, from time, to time

    "current-offset-notification": "Nuna frueco: {} sekundoj",  # Offset

    "media-directory-list-updated-notification": "Dosierujoj kun vidaŭdaĵoj por Syncplay ĝisdatiĝis.",

    "room-join-notification": "{} aliĝis al ĉambro: «{}»",  # User
    "left-notification": "{} foriris",  # User
    "left-paused-notification": "{} foriris, {} paŭzigis",  # User who left, User who paused
    "playing-notification": "{} ludas dosieron «{}» ({})",  # User, file, duration
    "playing-notification/room-addendum": " en ĉambro: «{}»",  # Room

    "not-all-ready": "Ne pretas: {}",  # Usernames
    "all-users-ready": "Ĉiuj pretas ({} uzantoj)",  # Number of ready users
    "ready-to-unpause-notification": "Nun vi estas markita preta – malpaŭzigu ree por vere malpaŭzigi",
    "set-as-ready-notification": "Nun vi estas markita preta",
    "set-as-not-ready-notification": "Nun vi estas markita nepreta",
    "autoplaying-notification": "Memage ludos post {}…",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Identiĝas kiel ĉambrestro per la pasvorto «{}»...",
    "failed-to-identify-as-controller-notification": "{} malsukcesis identiĝi ĉambrestro.",
    "authenticated-as-controller-notification": "{} identiĝis ĉambrestro",
    "created-controlled-room-notification": "Kreis estratan ĉambron «{}» kun pasvorto «{}». Bonvolu konservi tiujn informojn osen!\n\nEn estrataj ĉambroj, ĉiu spegulas la ĉambrestrojn, kiuj estas la solaj, kiuj povas paŭzigi, malpaŭzigi, iri, kaj ŝanĝi la ludliston.\n\nVi petu ordinarajn spektantojn aliĝi la ĉambron «{}», sed ĉambrestroj povas aliĝi la ĉambron «{}» por memage aŭtentikiĝi.",  # RoomName, operatorPassword, roomName, roomName:operatorPassword

    "other-set-as-ready-notification": "{} was set as ready by {}",  # User set as ready, user who set them as ready # TODO: Translate
    "other-set-as-not-ready-notification": "{} was set as not ready by {}", # User set as not ready, user who set them as not ready # TODO: Translate

    "file-different-notification": "La dosiero, kiun vi ludas, ŝajnas malsama de tiu de {}",  # User
    "file-differences-notification": "Via dosiero malsamas per ĉi tiuj manieroj: {}",  # Differences
    "room-file-differences": "Malsamoj inter dosieroj: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "nomo",
    "file-difference-filesize": "grandeco",
    "file-difference-duration": "daŭro",
    "alone-in-the-room": "Vi estas sola en la ĉambro",

    "different-filesize-notification": " (grandeco de ĝia dosiero malsamas de tiu de la via!)",
    "userlist-playing-notification": "{} ludas:",  # Username
    "file-played-by-notification": "Dosiero: {} estas ludata de:",  # File
    "no-file-played-notification": "{} ne ludas dosieron nun",  # Username
    "notplaying-notification": "Homoj, kiuj ne ludas iun dosieron nun:",
    "userlist-room-notification":  "En ĉambro «{}»:",  # Room
    "userlist-file-notification": "Dosiero",
    "controller-userlist-userflag": "Ĉambrestro",
    "ready-userlist-userflag": "Preta",

    "update-check-failed-notification": "Ne povis memage kontroli, ĉu Syncplay {} estas ĝisdata. Ĉu vi volus viziti al https://syncplay.pl/ kaj kontroli permane?",  # Syncplay version
    "syncplay-uptodate-notification": "Syncplay estas ĝisdata",
    "syncplay-updateavailable-notification": "Nova versio de Syncplay disponeblas. Ĉu vi volus viziti la eldonan paĝon?",

    "mplayer-file-required-notification": "Syncplay kun mplayer bezonas dosieron je starto",
    "mplayer-file-required-notification/example": "Ekzempla uzo: syncplay [elektoj] [url|vojo/]dosiernomo",
    "mplayer2-required": "Syncplay ne akordas kun MPlayer 1.x, bonvolu uzi programojn mplayer2 aŭ mpv",

    "unrecognized-command-notification": "Nerekonita ordono",
    "commandlist-notification": "Doneblaj ordonoj:",
    "commandlist-notification/room": "\tr [nomo] – ŝanĝi ĉambron",
    "commandlist-notification/list": "\tl – montri liston de uzantoj",
    "commandlist-notification/undo": "\tu – maliri",
    "commandlist-notification/pause": "\tp – (mal)paŭzigi",
    "commandlist-notification/seek": "\t[s][+-]tempo - iri al donita tempo; se + aŭ - ne estas donita, ĝi estu absoluta tempo en sekundoj aŭ minutoj:sekundoj",
    "commandlist-notification/offset": "\to[+-]daŭro - fruigi lokan ludadon je la donita daŭro (en sekundoj aŭ minutoj:sekundoj), kompare al la servila pozicio – ĉi tiu kapablo ne plu estos subtenata",
    "commandlist-notification/help": "\th – tiu ĉi helpilo",
    "commandlist-notification/toggle": "\tt – ŝanĝas ĉu vi pretas spekti aŭ ne",
    "commandlist-notification/setready": "\tsr [name] - sets user as ready",  # TODO: Translate
    "commandlist-notification/setnotready": "\tsn [name] - sets user as not ready",  # TODO: Translate
    "commandlist-notification/create": "\tc [nomo] – krei estratan ĉambron kun nomo de la nuna ĉambro",
    "commandlist-notification/auth": "\ta [pasvorto] – aŭtentikiĝi ĉambrestro per ĉambrestra pasvorto",
    "commandlist-notification/chat": "\tch [mesaĝo] – sendi babilan mesaĝon al ĉambro",
    "commandList-notification/queue": "\tqa [dosiero/url] – aldoni dosieron aŭ URL-on fine de ludlisto",
    "commandList-notification/queueandselect": "\tqas [dosiero/url] – aldoni dosieron aŭ URL-on fine de ludlisto, kaj ĝin elekti",
    "commandList-notification/playlist": "\tql – montri la nunan ludliston",
    "commandList-notification/select": "\tqs [index] – elekti donitan ludlisteron",
    "commandList-notification/next": "\tqn – elekti sekvantan ludlisteron",
    "commandList-notification/delete": "\tqd [index] – forigi la donitan ludlisteron de la ludlisto",
    "syncplay-version-notification": "Versio de Syncplay: {}",  # syncplay.version
    "more-info-notification": "Pliaj informoj disponeblas per: {}",  # projectURL

    "gui-data-cleared-notification": "Syncplay vakigis la vojon kaj fenestrajn datumojn uzatajn de la fasado.",
    "language-changed-msgbox-label": "Lingvo ŝanĝiĝos kiam Syncplay ruliĝos refoje.",
    "promptforupdate-label": "Ĉu Syncplay rajtas memage kontroli fojfoje, ĉu disponeblas ĝisdatigoj?",

    "media-player-latency-warning": "Averto: La vidaŭdaĵa ludilo respondis post {} sekundoj. Se vi havos problemojn pri vidaŭdaĵa spegulado, fermu iujn aplikaĵojn por liberigi rimedojn de la sistemo, kaj se tio ne funkcios, provu alian vidaŭdaĵan ludilon.",  # Seconds to respond
    "mpv-unresponsive-error": "mpv ne respondis dum {} sekundoj, do eble ne funkcias. Bonvolu reruli on Syncplay.",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "Premu enigan klavon por ĉesigi\n",

    # Client errors
    "missing-arguments-error": "Iuj gravaj parametroj mankas, vidu je --help",
    "server-timeout-error": "Konekto al servilo eltempiĝis",
    "mpc-slave-error": "MPC ne povas nun starti en sklava reĝimo!",
    "mpc-version-insufficient-error": "Versio de MPC ne sufiĉas, bonvolu uzi `mpc-hc` ≥ `{}`",
    "mpc-be-version-insufficient-error": "Versio de MPC ne sufiĉas, bonvolu uzi `mpc-be` ≥ `{}`",
    "mpv-version-error": "Syncplay ne akordas ĉi tiun version de mpv. Bonvolu uzi alian version de mpv (ekz. Git HEAD).",
    "mpv-failed-advice": "The reason mpv cannot start may be due to the use of unsupported command line arguments or an unsupported version of mpv.",
    "mpv-failed-advice": "Eble mpv ne povas starti pro nesubtenataj konzolaj parametroj, aŭ nesubtenata versio de mpv.", # FARU: «konzolaj» – ĉu bona traduko de «command-line»?
    "player-file-open-error": "Ludilo malsukcesis malfermi dosieron",
    "player-path-error": "Vojo al ludilo ne estas ĝuste agordita. Nun subtenataj ludiloj estas: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2, kaj IINA",
    "hostname-empty-error": "Nomo de gastiga komputilo ne povas esti malplena",
    "empty-error": "{} ne povas esti malplena",  # Configuration
    "media-player-error": "Eraro de vidaŭdaĵa ludilo: \"{}\"",  # Error line
    "unable-import-gui-error": "Ne povis enporti fasadajn bibliotekojn. Se PySide ne estas instalita, vi devos instali ĝin, por ke la fasado funkciu. If you want to run Syncplay in console mode then run it with the --no-gui command line switch. See https://syncplay.pl/guide/ for more details.", # TODO: Translate end of message and update second sentence to be a translation of "You need to have the correct version of PySide installed for the GUI to work."
    "unable-import-twisted-error": "Ne povis enporti la bibliotekon Twisted. Bonvolu instali version 16.4.0 de Twisted, aŭ pli altan.",

    "arguments-missing-error": "Iuj bezonataj parametroj mankas; vidu al --help",

    "unable-to-start-client-error": "Ne povas ruli klienton",

    "player-path-config-error": "Vojo al ludilo ne estas ĝuste agordita. Nun subtenataj ludiloj estas: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2, kaj IINA",
    "no-file-path-config-error": "Dosiero devas esti elektita, antaŭ ol vi rulos vian ludilon", # FARU: eble «komencos» aŭ «ludigos»?
    "no-hostname-config-error": "Nomo de gastiga komputilo ne povas esti malplena",
    "invalid-port-config-error": "Pordo devas esti valida",
    "empty-value-config-error": "{} ne povas esti malplena",  # Config option

    "not-json-error": "Tio ne estas JSON-teksto\n",
    "hello-arguments-error": "Not enough Hello arguments\n",  # DO NOT TRANSLATE # OKAY, OKAY! Geez! No need to shout.
    "version-mismatch-error": "Malakordo inter versioj de kliento kaj servilo\n",
    "vlc-failed-connection": "Malsukcesis konektiĝi al VLC. Se vi ne instalis syncplay.lua, kaj uzas la lastan version de VLC, bonvolu vidi la instrukciojn en https://syncplay.pl/LUA/. Syncplay kaj VLC 4 ne estas interkonformaj nun, do bonvolu uzi VLC 3, aŭ alternativon kiel mpv.",
    "vlc-failed-noscript": "VLC raportis, ke la interfaca skripto syncplay.lua ne estas instalita. Bonvolu vidi instrukciojn en https://syncplay.pl/LUA/",
    "vlc-failed-versioncheck": "Ĉi tiu versio de VLC ne estas subtenata de Syncplay.",
    "vlc-initial-warning": 'VLC ne ĉiam donas precizajn informojn pri pozicio al Syncplay, precipe pri dosierformoj .mp4 kaj .avi. Se vi spertos problemon pri poziciiĝo en filmo, bonvolu provi alternativan vidaŭdaĵan ludilon, kiel ekzemple <a href="https://mpv.io/">mpv</a> (aŭ <a href="https://github.com/stax76/mpv.net/">mpv.net</a> por uzantoj de Vindozo).',

    "feature-sharedPlaylists": "komunaj ludlistoj",  # used for not-supported-by-server-error
    "feature-chat": "babilado",  # used for not-supported-by-server-error
    "feature-readiness": "preteco",  # used for not-supported-by-server-error
    "feature-managedRooms": "estrataj ĉambroj",  # used for not-supported-by-server-error
    "feature-setOthersReadiness": "readiness override",  # used for not-supported-by-server-error # TODO: Translate

    "not-supported-by-server-error": "La kapablo «{}» ne estas subtenata de ĉi tiu servilo.",  # feature
    "shared-playlists-not-supported-by-server-error": "La servilo eble ne subtenas komunajn ludlistojn. Ĝusta funkciado postulas servilon kun Syncplay {}+, sed la servilo havas nur version {}.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "Komunaj ludlistoj estas malŝaltitaj en la servila agordaro. Por uzi ĉi tiun kapablon, vi devos konektiĝi al alia servilo.",

    "invalid-seek-value": "Nevalida valoro de iro",
    "invalid-offset-value": "Nevalida valoro de frueco",

    "switch-file-not-found-error": "Ne povis ŝalti dosieron «{0}». Syncplay serĉas en donitaj dosierujoj kun vidaŭdaĵoj.",  # File not found
    "folder-search-timeout-error": "La serĉado de vidaŭdaĵoj en dosierujoj kun vidaŭdaĵoj haltis, ĉar serĉado en «{}» postulis tro da tempo (after having processed the first {:,} files). Ĉi tio okazos, se vi elektos dosierujon kun tro multaj subdosierujoj en via listo de enserĉotaj dosierujoj kun vidaŭdaĵoj. Por refunkciigi memagan ŝaltadon de dosieroj, bonvolu elekti menueron «Dosiero → Agordi dosierujojn kun vidaŭdaĵoj» en la menubreto, kaj forigi ĉi tiun dosierujon, aŭ anstataŭigi ĝin per taŭga sub-dosierujo. Se vi trovos, ke la dosierujo fakte funkcias bone, vi povos reŝalti ĝin per «Dosiero → Agordi dosierujojn kun vidaŭdaĵoj» kaj klako al «Bone».",  # Folder, Files processed - Note: {:,} is {} but with added commas seprators - TODO: Translate
    "folder-search-timeout-warning": "Warning: It has taken {} seconds to scan {:,} files in the folder '{}'. This will occur if you select a folder with too many sub-folders in your list of media folders to search through or if there are too many files to process.",  # Folder, Files processed. Note: {:,} is {} but with added commas seprators. TODO: Translate
    "folder-search-first-file-timeout-error": "La serĉo de vidaŭdaĵoj en «{}» haltis, ĉar aliro al la dosierujo postulis tro da tempo. Ĉi tio povas okazi se ĝi estas reta disko aŭ se vi agordis vian diskon malrapidiĝi post neaktivado. Por ke funkciu memaga ŝanĝado de dosieroj, bonvolu iri al «Dosiero → Agordi vidaŭdaĵajn dosierujojn», kaj forigu la dosierujon, aŭ solvu la problemon (ekz. per ŝanĝo de viaj agordoj por konservado de elektro).",  # Folder
    "added-file-not-in-media-directory-error": "Vi enlegis dosieron el «{}», kiu ne estas konata vidaŭdaĵa dosierujo. Vi povas aldoni ĝin al vidaŭdaĵaj dosierujoj per la menuero «Dosiero → Agordi vidaŭdaĵajn dosierujojn» en la menua breto.",  # Folder
    "no-media-directories-error": "Neniuj vidaŭdaĵaj dosierujoj estas agorditaj. Por ke kapabloj de komunaj ludlistoj kaj ŝanĝado de dosieroj funkciu ĝuste, bonvolu elekti menueron «Dosiero → Agordi vidaŭdaĵajn dosierujojn», kaj precizigu, kie Syncplay serĉu vidaŭdaĵojn.",
    "cannot-find-directory-error": "Ne povis trovi vidaŭdaĵan dosierujon «{}». Por ĝisdatigi vian liston de vidaŭdaĵaj dosierujoj, bonvolu elekti menueron «Dosiero → Agordi vidaŭdaĵajn dosierujojn» en la menubreto, kaj precizigi, kie Syncplay serĉu vidaŭdaĵojn.",

    "failed-to-load-server-list-error": "Malsukcesis enlegi liston de publikaj serviloj. Bonvolu viziti al https://www.syncplay.pl/ per via reta foliumilo.",

    # Client arguments
    "argument-description": 'Rimedo samtempigi plurajn vidaŭdaĵajn ludilojn per la reto.',
    "argument-epilog": 'Se neniuj elektoj estos donitaj, uziĝos valoroj de _config',
    "nogui-argument": 'ne montri fasadon',
    "host-argument": "adreso de servilo",
    "name-argument": 'dezirata uzantonomo',
    "debug-argument": 'erarserĉa reĝimo',
    "force-gui-prompt-argument": 'montru agordan fenestron',
    "no-store-argument": "ne konservu valorojn en .syncplay",
    "room-argument": 'implicita ĉambro',
    "password-argument": 'pasvorto de servilo',
    "player-path-argument": 'vojo al rulaĵo de via vidaŭdaĵa ludilo',
    "file-argument": 'ludota dosiero',
    "args-argument": 'agordoj de ludilo; se vi bezonas doni elektojn, kiuj komenciĝas per «-», antaŭmetu solan parametron «--»',
    "clear-gui-data-argument": 'restarigas vojon kaj datumojn pri stato de la fenestro, konservitajn en la formo [QSettings]',
    "language-argument": 'lingvo por mesaĝoj de Syncplay ({})', # Languages

    "version-argument": 'presas vian version',
    "version-message": "Vi uzas programon Syncplay, versio {} ({})",

    "load-playlist-from-file-argument": "legas ludliston de teksta dosiero (po unu listero linie)",


    # Client labels
    "config-window-title": "Agordaro de Syncplay",

    "connection-group-title": "Agordoj de konekto",
    "host-label": "Adreso de servilo: ",
    "name-label":  "Uzantonomo (nenecesa):",
    "password-label":  "Pasvorto de servilo (se ekzistas):",
    "room-label": "Komenca ĉambro: ",
    "roomlist-msgbox-label": "Redakti liston de ĉambroj (po unu ĉambro linie)",

    "media-setting-title": "Agordoj de vidaŭdaĵa ludilo",
    "executable-path-label": "Vojo al vidaŭdaĵa ludilo:",
    "media-path-label": "Vojo al filmo:",
    "player-arguments-label": "Parametroj de ludilo (se ekzistas):",
    "browse-label": "Foliumi",
    "update-server-list-label": "Ĝisdatigi liston",

    "more-title": "Montri pliajn agordojn",
    "never-rewind-value": "Neniam",
    "seconds-suffix": " sekundoj",
    "privacy-sendraw-option": "Sendi krude",
    "privacy-sendhashed-option": "Sendi hakete",
    "privacy-dontsend-option": "Ne sendi",
    "filename-privacy-label": "Informo pri dosiernomo:",
    "filesize-privacy-label": "Informo pri dosiergrandeco:",
    "checkforupdatesautomatically-label": "Memage kontroli ĝisdatigojn de Syncplay",
    "autosavejoinstolist-label": "Aldoni aliĝitajn ĉambrojn al la listo de ĉambroj",
    "slowondesync-label": "Malrapidiĝi pro eta malakordo (ne disponeblas por MPC-HC/BE)",
    "rewindondesync-label": "Reiri pro ega malakordo (rekomendata)",
    "fastforwardondesync-label": "Pluiri pro malfrueco (rekomendata)",
    "dontslowdownwithme-label": "Neniam malrapidigi nek reirigi aliulojn (eksperimenta)",
    "pausing-title": "Paŭzado",
    "pauseonleave-label": "Paŭzigi kiam uzanto foriras (ekz. se ĝi malkonektiĝis)",
    "readiness-title": "Komenca preteco",
    "readyatstart-label": "Marki min «preta spekti» dekomence",
    "forceguiprompt-label": "Ne montru ĉiam la agordan fenestron de Syncplay",  # (Inverted)
    "showosd-label": "Ŝalti mesaĝojn en fasado",

    "showosdwarnings-label": "Inkluzivi avertojn (ekz. kiam dosieroj malsamas, uzantoj ne pretas…)",
    "showsameroomosd-label": "Inkluzivi okazojn en via ĉambro",
    "shownoncontrollerosd-label": "Inkluzivi okazojn de neĉambrestroj en estrataj ĉambroj",
    "showdifferentroomosd-label": "Inkluzivi okazojn en aliaj ĉambroj",
    "showslowdownosd-label": "Inkluzivi sciigojn pri malrapidiĝoj / reiroj",
    "language-label": "Lingvo:",
    "automatic-language": "Implicita ({})",  # Default language
    "showdurationnotification-label": "Averti pri malakordo inter daŭroj de vidaŭdaĵoj",
    "basics-label": "Bazaj",
    "readiness-label": "Ludi/Paŭzigi",
    "misc-label": "Diversaj",
    "core-behaviour-title": "Baza konduto en ĉambroj",
    "syncplay-internals-title": "Internaĵoj de Syncplay",
    "syncplay-mediasearchdirectories-title": "Dosierujoj kun serĉotaj vidaŭdaĵoj",
    "syncplay-mediasearchdirectories-label": "Dosierujoj kun serĉotaj vidaŭdaĵoj (po unu vojo linie)",
    "sync-label": "Samtempigo",
    "sync-otherslagging-title": "Se aliuloj malfruas…",
    "sync-youlaggging-title": "Se vi malfruas…",
    "messages-label": "Mesaĝoj",
    "messages-osd-title": "Agordoj de ludila fasado",
    "messages-other-title": "Agordoj de aliaj montraĵoj",
    "chat-label": "Babilado",
    "privacy-label": "Privateco",  # Currently unused, but will be brought back if more space is needed in Misc tab
    "privacy-title": "Agordoj de privateco",
    "unpause-title": "Kiam vi premos ekludan butonon, markiĝi preta kaj:",
    "unpause-ifalreadyready-option": "Malpaŭzi se vi jam pretas",
    "unpause-ifothersready-option": "Malpaŭzi se vi aŭ aliuloj en la ĉambro jam pretas (implicita)",
    "unpause-ifminusersready-option": "Malpaŭzi se vi jam pretas, aŭ se ĉiuj aliaj pretas, kaj minimuma kvanto pretas",
    "unpause-always": "Ĉiam malpaŭzi",
    "syncplay-trusteddomains-title": "Fidataj retnomoj (por elsendfluoj kaj servado de enhavo)",

    "chat-title": "Enigo de babilaj mesaĝoj",
    "chatinputenabled-label": "Ŝalti babilan enigon per mpv",
    "chatdirectinput-label": "Permesi tujan babilan enigon (sen bezono premi la enigan klavon unue)",
    "chatinputfont-label": "Tiparo de babila enigo",
    "chatfont-label": "Agordi tiparon",
    "chatcolour-label": "Agordi koloron",
    "chatinputposition-label": "Pozicio de mesaĝa enigujo en mpv",
    "chat-top-option": "Supre",
    "chat-middle-option": "Meze",
    "chat-bottom-option": "Sube",
    "chatoutputheader-label": "Eligo de babilaj mesaĝoj",
    "chatoutputfont-label": "Tiparo de babila eligo",
    "chatoutputenabled-label": "Ŝalti babilan enigon en vidaŭdaĵa ludilo (ankoraŭ nur mpv)",
    "chatoutputposition-label": "Eliga reĝimo",
    "chat-chatroom-option": "Babilĉambro stilo",
    "chat-scrolling-option": "Ruluma stilo",

    "mpv-key-tab-hint": "[TAB] por aktivigi ŝparklavojn en alfabeta vico.",
    "mpv-key-hint": "[ENIG] por sendi mesaĝon. [ESKAP] por ĉesigi babilan reĝimon.",
    "alphakey-mode-warning-first-line": "Vi povas provizore uzi malnovajn ŝparklavojn de mpv per la klavoj a–z.",
    "alphakey-mode-warning-second-line": "Premu klavon [TAB] por reiri al babila reĝimo de Syncplay.",

    "help-label": "Helpo",
    "reset-label": "Reagordi implicitajn",
    "run-label": "Ruli programon Syncplay",
    "storeandrun-label": "Konservi agordaron kaj ruli programon Syncplay",

    "contact-label": "Laŭplaĉe sendu retleteron al <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a>, <a href=\"https://github.com/Syncplay/syncplay/issues\"><nobr>registru problemon</nobr></a> por raporti la eraron per GitHub, <a href=\"https://github.com/Syncplay/syncplay/discussions\"><nobr>komencu diskuton</nobr></a> por fari proponon aŭ meti demandon per GitHub, <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>ŝatu nin ĉe Fejsbuko</nobr></a>, <a href=\"https://twitter.com/Syncplay/\"><nobr>abonu nin ĉe Tvitro</nobr></a>, aŭ vizitu al <a href=\"https://syncplay.pl/\"><nobr>https://syncplay.pl/</nobr></a>. Syncplay ne taŭgas por sendado de privataj aŭ sentigemaj informoj.",

    "joinroom-label": "Aliĝi al ĉambro",
    "joinroom-menu-label": "Aliĝi al ĉambro {}",
    "seektime-menu-label": "Iri al tempo",
    "undoseek-menu-label": "Reiri",
    "play-menu-label": "Ludi",
    "pause-menu-label": "Paŭzigi",
    "playbackbuttons-menu-label": "Montri ludbutonojn",
    "autoplay-menu-label": "Montri butonon por memaga ludado",
    "autoplay-guipushbuttonlabel": "Ludi kiam ĉiuj pretas",
    "autoplay-minimum-label": "Minimumo da uzantoj:",
    "hideemptyrooms-menu-label": "Kaŝi malplenajn persistajn ĉambrojn",

    "sendmessage-label": "Sendi",

    "ready-guipushbuttonlabel": "Mi pretas spekti!",

    "roomuser-heading-label": "Ĉambro / Uzanto",
    "size-heading-label": "Grandeco",
    "duration-heading-label": "Longeco",
    "filename-heading-label": "Dosiernomo",
    "notifications-heading-label": "Sciigoj",
    "userlist-heading-label": "Listo de nuna ludado",

    "browseformedia-label": "Foliumi vidaŭdaĵojn",

    "file-menu-label": "&Dosiero",  # & precedes shortcut key
    "openmedia-menu-label": "&Malfermi vidaŭdaĵon",
    "openstreamurl-menu-label": "Malfermi &vidaŭdfluan URL-on",
    "setmediadirectories-menu-label": "Agordi vidaŭdajn dosier&ujojn",
    "loadplaylistfromfile-menu-label": "&Enlegi ludliston de dosiero",
    "saveplaylisttofile-menu-label": "&Konservi ludliston al dosiero",
    "reconnect-menu-label": "&Rekonektiĝi al servilo",
    "exit-menu-label": "Ĉesi&gi la programon",
    "advanced-menu-label": "&Altnivelaj",
    "window-menu-label": "&Fenestro",
    "setoffset-menu-label": "Agordi frue&con",
    "createcontrolledroom-menu-label": "&Krei estratan ĉambron",
    "identifyascontroller-menu-label": "&Identiĝi ĉambrestro",
    "settrusteddomains-menu-label": "Agordi fidatajn &retnomojn",
    "addtrusteddomain-menu-label": "Aldoni retnomon {} kiel fidatan",  # Domain

    "edit-menu-label": "&Redakti",
    "cut-menu-label": "El&tondi",
    "copy-menu-label": "&Kopii",
    "paste-menu-label": "&Alglui",
    "selectall-menu-label": "Ĉion &elekti",

    "playback-menu-label": "&Ludado",

    "help-menu-label": "&Helpo",
    "userguide-menu-label": "Malfermi &gvidilon por uzantoj",
    "update-menu-label": "Kontroli ĝisdati&gon",

    "startTLS-initiated": "Provas konektiĝi sekure",
    "startTLS-secure-connection-ok": "Konektiĝis sekure ({})",
    "startTLS-server-certificate-invalid": 'Malsukcesis konektiĝi sekure. La servilo uzas nevalidan atestilon pri sekureco. Iu povus subaŭskluti ĉi tiun komunikadon. Por pliaj detaloj kaj eblaj solvoj, vizitu <a href="https://syncplay.pl/trouble">ĉi tien</a>.',
    "startTLS-server-certificate-invalid-DNS-ID": "Syncplay ne fidas ĉi tiun servilon, ĉar ĝi uzas atestilon, kiu ne validas por la nomo de gastiga komputilo.",
    "startTLS-not-supported-client": "TLS ne estas subtenata de la kliento",
    "startTLS-not-supported-server": "TLS ne estas subtenata de la servilo",

    # TLS certificate dialog
    "tls-information-title": "Detaloj pri atestilo",
    "tls-dialog-status-label": "<strong>Syncplay uzas ĉifratan konekton al {}.</strong>",
    "tls-dialog-desc-label": "Ĉifrado kun cifereca atestilo lasas informojn privataj dum ili sendiĝas de aŭ al<br/>la servilo {}.",
    "tls-dialog-connection-label": "Informoj ĉifritaj per [Transport Layer Security] (TLS), versio {} kun la<br/>ĉifra ilaro: {}.",
    "tls-dialog-certificate-label": "Atestilo eldonita de {} kaj valida ĝis {}.",

    # About dialog
    "about-menu-label": "&Pri Syncplay",
    "about-dialog-title": "Pri Syncplay",
    "about-dialog-release": "Versio {}, eldono {}",
    "about-dialog-license-text": "Eldonita sub al permesilo «Apache&nbsp;License,&nbsp;Version 2.0»",
    "about-dialog-license-button": "Permesilo",
    "about-dialog-dependencies": "Dependoj",

    "setoffset-msgbox-label": "Agordi fruecon",
    "offsetinfo-msgbox-label": "Frueco (vidu instrukciojn ĉe https://syncplay.pl/guide/):",

    "promptforstreamurl-msgbox-label": "Malfermi URL-on al vidaŭdaĵa elsendfluo",
    "promptforstreamurlinfo-msgbox-label": "URL de elsendfluo",

    "addfolder-label": "Aldoni dosierujon",

    "adduris-msgbox-label": "Aldoni URL-ojn al ludlisto (po unu linie)",
    "editplaylist-msgbox-label": "Meti ludliston (po unu linie)",
    "trusteddomains-msgbox-label": "Retnomoj, kiujn oni rajtas memage viziti (po unu linie)",

    "createcontrolledroom-msgbox-label": "Krei estratan ĉambron",
    "controlledroominfo-msgbox-label": "Enigu nomon de estrata ĉambro\r\n(vidu al https://syncplay.pl/guide/ por instrukcioj pri uzado):",

    "identifyascontroller-msgbox-label": "Identiĝi ĉambrestro",
    "identifyinfo-msgbox-label": "Enigu ĉambrestran pasvorton por ĉi tiu ĉambro\r\n(vidu al https://syncplay.pl/guide/ por instrukcioj pri uzado):",

    "public-server-msgbox-label": "Elektu publikan servilon por ĉi tiu kunspekto",

    "megabyte-suffix": " MB",

    # Tooltips

    "host-tooltip": "Retnomo aŭ IP-adreso, al kiu vi konektiĝos, laŭplaĉe kun pordo (ekz. syncplay.pl:8999). Vi samtempiĝos nur kun personoj ĉe la sama servilo/pordo.",
    "name-tooltip": "Via prezenta kaŝnomo. Oni ne registriĝas, kaj vi povos facile ŝanĝi ĝin poste. Se vi elektos neniun, vi ricevos hazardan.",
    "password-tooltip": "Pasvortoj nur necesas por konektoj al privataj serviloj.",
    "room-tooltip": "Ĉambro, kiun vi eniros je konektiĝo, povas esti preskaŭ ĉio ajn, sed vi nur samtempiĝos kun personoj en la sama ĉambro.",

    "edit-rooms-tooltip": "Redakti liston de ĉambroj.",

    "executable-path-tooltip": "Loko de via elektita subtenata vidaŭdaĵa ludilo (mpv, mpv.net, VLC, MPC-HC/BE, mplayer2 aŭ IINA).",
    "media-path-tooltip": "Loko de filmo aŭ elsendfluo malfermota. Necesas por mplayer2.",
    "player-arguments-tooltip": "Aldonaj konzolaj parametroj / elektoj ricevotaj de ĉi tiu ludilo.",
    "mediasearcdirectories-arguments-tooltip": "Dosierujoj, en kiuj Syncplay serĉos vidaŭdaĵojn, ekz. kiam vi uzas la kapablon «klaki por ŝanĝi». Syncplay serĉos profunde en sub-dosierujoj.",

    "more-tooltip": "Montri malpli oftajn agordojn.",
    "filename-privacy-tooltip": "Privateca reĝimo por sendi nomon de nun ludata dosiero al la servilo.",
    "filesize-privacy-tooltip": "Privateca reĝimo por sendi grandecon de nun ludata dosiero al la servilo.",
    "privacy-sendraw-tooltip": "Sendi ĉi tiun informon senkaŝe. Ĉi tio estas la implicita agordo kun plej bona funkciado.",
    "privacy-sendhashed-tooltip": "Sendi haketitan version de la informo, kiu malpli evidentos por aliaj klientoj.",
    "privacy-dontsend-tooltip": "Ne sendi ĉi tiun informon al la servilo. Ĉi tio donas maksimuman privatecon.",
    "checkforupdatesautomatically-tooltip": "Kontroladi per la retejo de Syncplay, ĉu nova versio de Syncplay disponeblas.",
    "autosavejoinstolist-tooltip": "Kiam vi aliĝas al ĉambro en servilo, memage memoru la ĉambronomon en listo de aliĝotaj ĉambroj.",
    "slowondesync-tooltip": "malpliigi ludrapidecon kelkatempe, kiam vi bezonas resamtempiĝi kun aliaj spektantoj. Nesubtenata per MPC-HC/BE.",
    "dontslowdownwithme-tooltip": "Signifas, ke aliuloj ne malrapidiĝos nek reiros se via ludado prokrastiĝas. Utile por ĉambrestroj.",
    "pauseonleave-tooltip": "Paŭzigi kiam vi malkonektiĝas aŭ iu foriras de la ĉamrbo.",
    "readyatstart-tooltip": "Markiĝi «preta» je la komenco (alie vi estos «nepreta» ĝis vi mem ŝanĝos vian pretecon)",
    "forceguiprompt-tooltip": "Agorda fenestro ne montriĝas kiam vi malfermas dosieron per Syncplay.",  # (Inverted)
    "nostore-tooltip": "Syncplay ruliĝu kun la donita agordaro, sed ne memoru la ŝanĝojn poste.",  # (Inverted)
    "rewindondesync-tooltip": "Reiru kiam vi devas resamtempiĝi. Malŝalto de ĉi tiu elekto povas venigi gravajn diferencojn!",
    "fastforwardondesync-tooltip": "Saltu pluen pro misspegulado de ĉambrestro (aŭ ŝajnigu malveran pozicion, se «Neniam malrapidigi aŭ reirigi aliulojn» estas ŝaltita).",
    "showosd-tooltip": "Sendi mesaĝojn de Syncplay al fasado de la ludilo.",
    "showosdwarnings-tooltip": "Montri avertojn se ludiĝas alia dosiero, vi solas en ĉambro, uzantoj ne pretas, ktp.",
    "showsameroomosd-tooltip": "Montri fasade sciigojn pri okazoj rilataj al la ĉambro de la uzanto.",
    "shownoncontrollerosd-tooltip": "Montri fasade sciigojn pri okazoj rilataj al neĉambrestroj en estrataj ĉambroj.",
    "showdifferentroomosd-tooltip": "Montri fasade sciigojn pri okazoj rilata al ĉambro, en kiu la uzanto ne estas.",
    "showslowdownosd-tooltip": "Montri sciigojn pri malrapidiĝo / reiro pro tempa malakordo.",
    "showdurationnotification-tooltip": "Utilas kiam parto de plurparta dosiero mankas, sed fojfoje povas raporti problemojn erare.",
    "language-tooltip": "Lingvo uzota de Syncplay.",
    "unpause-always-tooltip": "Se vi malpaŭzos, vi ne nur pretiĝos, sed ĉiam ankaŭ malpaŭzos.",
    "unpause-ifalreadyready-tooltip": "Se vi malpaŭzigos nepreta, vi pretiĝos – malpaŭzigu refoje por vere malpaŭzigi.",
    "unpause-ifothersready-tooltip": "Se vi malpaŭzigos nepreta, vi nur malpaŭzigos se aliaj jam pretas.",
    "unpause-ifminusersready-tooltip": "Se vi malpaŭzigos nepreta, vi nur malpaŭzigos se aliaj jam pretas kaj minimuma limo de uzantoj atingiĝis.",
    "trusteddomains-arguments-tooltip": "Retnomoj, al kiuj Syncplay povas memage konektiĝi kiam komunaj ludlistoj estas ŝaltitaj.",

    "chatinputenabled-tooltip": "Ŝalti enigon de babilaj mesaĝoj en mpv (premu enigan klavon por enigi kaj sendi mesaĝojn, kaj eskapan klavon por nuligi)",
    "chatdirectinput-tooltip": "Ne atendi enigan klavon por babilado en mpv. Premu la tab-klavon por malŝalti provizore ĉi tiun kapablon.",
    "font-label-tooltip": "Tiparo uzata por enigo de babilaj mesaĝoj en mpv. Nur klient-flanke; ne influas aspekton por aliaj uzantoj.",
    "set-input-font-tooltip": "Familio de tiparo uzata por enigo de babilaj mesaĝoj en mpv. Nur klient-flanke; ne influas aspekton por aliaj uzantoj.",
    "set-input-colour-tooltip": "Koloro de tiparo uzata por enigo de babilaj mesaĝoj en mpv. Nur klient-flanke; ne influas aspekton por aliaj uzantoj.",
    "chatinputposition-tooltip": "Loko en mpv, kie eniga teksto aperos, kiam vi premos enigan klavon kaj tajpos.",
    "chatinputposition-top-tooltip": "Metu babilan enigon supre en la fenestro de mpv.",
    "chatinputposition-middle-tooltip": "Metu babilan enigon centre en la fenestro de mpv.",
    "chatinputposition-bottom-tooltip": "Metu babilan enigon sube en la fenestro de mpv.",
    "chatoutputenabled-tooltip": "Montru babilajn mesaĝojn en fasado (se vidaŭdaĵa ludilo tion subtenas).",
    "font-output-label-tooltip": "Tiparo por eligo de babilaj mesaĝoj.",
    "set-output-font-tooltip": "Tiparo uzota por montrado de babilaj mesaĝoj.",
    "chatoutputmode-tooltip": "Kiel babilaj mesaĝoj montriĝas.",
    "chatoutputmode-chatroom-tooltip": "Montri novajn liniojn de babilo rekte sub la lasta linio.",
    "chatoutputmode-scrolling-tooltip": "Rulumi babilan tekston maldekstren.",

    "help-tooltip": "Malfermas la gvidilon por uzantoj en Syncplay.pl.",
    "reset-tooltip": "Reagordas ĉion al komencaj valoroj.",
    "update-server-list-tooltip": "Konektiĝi al syncplay.pl por ĝisdatigi la liston de publikaj serviloj.",

    "sslconnection-tooltip": "Sekure konektiĝis al servilo. Klaku por detaloj pri atestilo.",

    "joinroom-tooltip": "Foriri de nuna ĉambro kaj aliĝi al donita ĉambro.",
    "seektime-msgbox-label": "Salti al donita tempo (en sekundoj / min:sek). Uzu la antaŭsignojn +/- por desalti.",
    "ready-tooltip": "Indikas, ĉu vi pretas spekti.",
    "autoplay-tooltip": "Memage ludi kiam ĉiuj uzantoj kun indikilo de preteco pretas, kaj minimuma kvanto de uzantoj ĉeestas.",
    "switch-to-file-tooltip": "Duoble klaku por ŝanĝi al {}",  # Filename
    "sendmessage-tooltip": "Sendi mesaĝon al ĉambro",

    # In-userlist notes (GUI)
    "differentsize-note": "Malsama grandeco!",
    "differentsizeandduration-note": "Malsamaj grandeco kaj daŭro!",
    "differentduration-note": "Malsama daŭro!",
    "nofile-note": "(Neniu dosiero ludiĝas)",

    # Server messages to client
    "new-syncplay-available-motd-message": "Vi uzas version {} de Syncplay, sed pli nova versio estas disponebla per https://syncplay.pl",  # ClientVersion
    "persistent-rooms-notice": "AVIZO: Ĉi tiu servilo uzas persistajn ĉámbrojn, kio signifas, ke la informoj pri ludlistoj konserviĝas por venontaj kunspektoj. Se vi volas krei ĉambron kie la informoj ne konserviĝas, finu la nomon de la ĉambro per «-temp».", # NOTE: Do not translate the word -temp
    "ready-chat-message": "I have set {} as ready.",  # User # TODO: Translate
    "not-ready-chat-message": "I have set {} as not ready.",  # User # TODO: Translate

    # Server notifications
    "welcome-server-notification": "Bonvenu al servilo de Syncplay, versio {0}",  # version
    "client-connected-room-server-notification": "{0}({2}) konektiĝis al ĉambro '{1}'",  # username, host, room
    "client-left-server-notification": "{0} foriris de la servilo",  # name
    "no-salt-notification": "BONVOLU SCII: Por ke pasvortoj de ĉambrestroj, estigitaj de ĉi tiu servilo, ankoraŭ funkciu post restarto de la servilo, bonvolu aldoni ĉi tiun konzolan parametron, kiam vi rerulos la servilon de Syncplay: --salt {}",  # Salt


    # Server arguments
    "server-argument-description": 'Solution to synchronize playback of multiple media player instances over the network. Server instance',
    "server-argument-epilog": 'Se neniuj elektoj estas donitaj, valoroj el _config uziĝos',
    "server-port-argument": 'TCP-pordo de la servilo',
    "server-password-argument": 'pasvorto de la servilo',
    "server-isolate-room-argument": 'ĉu ĉambroj estu izolitaj?',
    "server-salt-argument": "hazarda ĉeno uzata por estigi pasvortojn de estrataj ĉambroj",
    "server-disable-ready-argument": "malŝalti pretecon",
    "server-motd-argument": "vojo al dosiero, el kiu oni prenos mesaĝon de tago",
    "server-rooms-argument": "vojo al datumbaza dosiero por datumoj pri persistaj ĉambroj. Povigas ĉambrojn persisti sen spektantoj kaj inter restartigoj",
    "server-permanent-rooms-argument": "vojo al dosiero, kiu listigas persistajn ĉambrojn, kiuj listiĝos eĉ se ili malplenas (en la formo de teksta dosiero, kiu listigas po unu ĉambro linie) – postulas persistajn ĉambrojn ŝaltitajn",
    "server-chat-argument": "Ĉu babilado estu malŝaltita?",
    "server-chat-maxchars-argument": "Maksimuma kvanto de signoj en babila mesaĝo (implicita valoro estas {})", # Default number of characters
    "server-maxusernamelength-argument": "Maksimuma kvanto de signoj en uzantonomo (implicita valoro estas {})",
    "server-stats-db-file-argument": "Ŝalti servilajn statistikojn per la donita datumbaza dosiero de SQLite",
    "server-startTLS-argument": "Ŝalti TLS-konektojn per la atestilaj dosieroj en la donita vojo",
    "server-messed-up-motd-unescaped-placeholders": "Mesaĝo de tago havas neŝirmitajn anstataŭiĝojn. Ĉiuj dolarsignoj devus aperi duoble ($$).",
    "server-messed-up-motd-too-long": "Mesaĝo de tago estas tro longa – maksimuma kvanto estas {} signoj, sed {} estas donitaj.",
    "server-listen-only-on-ipv4": "Listen only on IPv4 when starting the server.",
    "server-listen-only-on-ipv6": "Listen only on IPv6 when starting the server.",
    "server-interface-ipv4": "The IP address to bind to for IPv4. Leaving it empty defaults to using all.",
    "server-interface-ipv6": "The IP address to bind to for IPv6. Leaving it empty defaults to using all.",

    # Server errors
    "unknown-command-server-error": "Nekonata ordono {}",  # message
    "not-json-server-error": "{} ne estas teksto kodita por JSON",  # message
    "line-decode-server-error": "{} ne estas teksto kodita per UTF-8",
    "not-known-server-error": "La servilo devas koni vin, antaŭ ol vi sendos ĉi tiun ordonon",
    "client-drop-server-error": "Client drop: {} -- {}",  # host, error # FARU: Mi ne komprenas.
    "password-required-server-error": "Necesas pasvorto",
    "wrong-password-server-error": "Malĝusta pasvorto estas donita",
    "hello-server-error": "Not enough Hello arguments",  # DO NOT TRANSLATE # Okay, geez, no need to shout!

    # Playlists
    "playlist-selection-changed-notification":  "{} ŝanĝis la elekton de ludlisto",  # Username
    "playlist-contents-changed-notification": "{} ĝisdatigis la ludliston",  # Username
    "cannot-find-file-for-playlist-switch-error": "Ne trovis la dosieron {} en vidaŭdaĵaj dosierujoj por ludlista ŝanĝo!",  # Filename
    "cannot-add-duplicate-error": "Ne povis aldoni duan listeron «{}» al la ludlisto ĉar duoblaĵoj ne estas permesitaj.",  # Filename
    "cannot-add-unsafe-path-error": "Ne povis memage enlegi el {}, ĉar ĝi ne estas fidata retnomo. Vi povas iri al la URL permane, se vi duoble klakos ĝin en la ludlisto, kaj aldoni fidatajn retnomojn per la menuero «Dosiero → Altnivelaj → Agordi fidatajn retnomojn». Se vi dekstre klakos al URL, vi povos fidi ĝian retnomon per la kunteksta menuo",  # Filename
    "sharedplaylistenabled-label": "Ŝalti komunajn ludlistojn",
    "removefromplaylist-menu-label": "Forigi de ludlisto",
    "shuffleremainingplaylist-menu-label": "Miksi ceteron de ludlisto",
    "shuffleentireplaylist-menu-label": "Miksi tutan ludliston",
    "undoplaylist-menu-label": "Malfari lastan ŝanĝon al ludlisto",
    "addfilestoplaylist-menu-label": "Aldoni dosiero(j)n al fino de ludlisto",
    "addurlstoplaylist-menu-label": "Aldoni URL-o(j)n al fino de ludlisto",
    "editplaylist-menu-label": "Redakti ludliston",

    "open-containing-folder": "Malfermi dosierujon kun ĉi tiu dosiero",
    "addyourfiletoplaylist-menu-label": "Aldoni vian dosieron al la ludlisto",
    "addotherusersfiletoplaylist-menu-label": "Aldoni dosieron de {} al la ludlisto",  # [Username]
    "addyourstreamstoplaylist-menu-label": "Aldoni vian elsendon al la ludlisto",
    "addotherusersstreamstoplaylist-menu-label": "Aldoni elsendon de {} al la ludlisto",  # [Username]
    "openusersstream-menu-label": "Malfermi elsendon de {}",  # [username]'s
    "openusersfile-menu-label": "Malfermi dosieron de {}",  # [username]'s

    "setasready-menu-label": "Set {} as ready",  # [Username] # TODO: Translate
    "setasnotready-menu-label": "Set {} as not ready",  # [Username] # TODO: Translate

    "playlist-instruction-item-message": "Metu dosieron ĉi tien por aldoni ĝin al la komuna ludlisto.",
    "sharedplaylistenabled-tooltip": "Ĉambrestroj povas aldoni dosierojn al spegulata ludlisto, por ke ĉiuj povu facile spekti la saman filmon. Agordu vidaŭdaĵajn dosierojn sub «Diversaj».",

    "playlist-empty-error": "Ludlisto nun estas malplena.",
    "playlist-invalid-index-error": "Nevalida indico de ludlisto",
}
