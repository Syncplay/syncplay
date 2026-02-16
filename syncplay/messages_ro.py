# coding:utf8

"""Romanian dictionary"""

# Filename, dictionary name and LANGUAGE-TAG value based on ISO country code. Language tag listed at https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/a9eac961-e77d-41a6-90a5-ce1a8b0cdb9c?redirectedfrom=MSDN

ro = {
    "LANGUAGE": "Română",
    "LANGUAGE-TAG": "ro",

    # Strings for Windows NSIS installer
    "installer-language-file": "Romanian.nlf",  # Relevant .nlf file at https://github.com/kichik/nsis/tree/master/Contrib/Language%20files
    "installer-associate": "Asociază Syncplay cu fișierele multimedia.",
    "installer-shortcut": "Creează scurtături în următoarele locații:",
    "installer-start-menu": "Meniul Start",
    "installer-desktop": "Desktop",
    "installer-quick-launch-bar": "Bara de lansare rapidă",
    "installer-automatic-updates": "Verifică automat dacă există actualizări",
    "installer-uninstall-configuration": "Șterge fișierul de configurare.",

    # Client notifications
    "config-cleared-notification": "Setările au fost șterse. Modificările vor fi salvate când stocați o configurație validă.",

    "relative-config-notification": "Fișier(e) de configurare relativă încărcat(e): {}",

    "connection-attempt-notification": "Se încearcă conectarea la {}:{}",  # Port, IP
    "reconnection-attempt-notification": "Conexiunea cu serverul a fost pierdută, se încearcă reconectarea",
    "reconnect-menu-triggered-notification": "Reconectare manuală inițiată - se va încerca o conexiune nouă la {}:{} în 2 secunde...",
    "reconnect-failed-no-host-error": "Nu se poate reconecta: nu sunt disponibile informații despre server",
    "reconnect-failed-no-port-error": "Nu se poate reconecta: configurație invalidă a serverului",
    "reconnect-failed-error": "Reconectarea a eșuat: {}",
    "disconnection-notification": "Deconectat de la server",
    "connection-failed-notification": "Conexiunea cu serverul a eșuat",
    "connected-successful-notification": "Conectat cu succes la server",
    "retrying-notification": "%s, Se reîncearcă în %d secunde...",  # Seconds
    "reachout-successful-notification": "S-a contactat cu succes {} ({})",

    "rewind-notification": "S-a derulat înapoi din cauza diferenței de timp cu {}",  # User
    "fastforward-notification": "S-a derulat rapid înainte din cauza diferenței de timp cu {}",  # User
    "slowdown-notification": "Se încetinește din cauza diferenței de timp cu {}",  # User
    "revert-notification": "Se revine la viteza normală",

    "pause-notification": "{} a pus pe pauză la {}",  # User, Time
    "unpause-notification": "{} a reluat redarea",  # User
    "seek-notification": "{} a sărit de la {} la {}",  # User, from time, to time

    "current-offset-notification": "Decalaj curent: {} secunde",  # Offset

    "media-directory-list-updated-notification": "Directoarele media Syncplay au fost actualizate.",

    "room-join-notification": "{} s-a alăturat camerei: '{}'",  # User
    "left-notification": "{} a plecat",  # User
    "left-paused-notification": "{} a plecat, {} a pus pe pauză",  # User who left, User who paused
    "playing-notification": "{} redă '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum": " în camera: '{}'",  # Room

    "not-all-ready": "Nu sunt pregătiți: {}",  # Usernames
    "all-users-ready": "Toți sunt pregătiți ({} utilizatori)",  # Number of ready users
    "ready-to-unpause-notification": "Acum ești setat ca pregătit - reia din nou pentru a relua redarea",
    "set-as-ready-notification": "Acum ești setat ca pregătit",
    "set-as-not-ready-notification": "Acum ești setat ca nepregătit",
    "autoplaying-notification": "Redare automată în {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Se identifică ca operator al camerei cu parola '{}'...",
    "failed-to-identify-as-controller-notification": "{} nu a reușit să se identifice ca operator al camerei.",
    "authenticated-as-controller-notification": "{} s-a autentificat ca operator al camerei",
    "created-controlled-room-notification": "S-a creat camera gestionată '{}' cu parola '{}'. Vă rugăm să salvați aceste informații pentru referință viitoare!\n\nÎn camerele gestionate, toți sunt sincronizați cu operatorul/operatorii camerei, care sunt singurii care pot pune pe pauză, relua, sări și modifica lista de redare.\n\nAr trebui să cereți vizitatorilor obișnuiți să se alăture camerei '{}', dar operatorii camerei pot intra în camera '{}' pentru a se autentifica automat.",  # RoomName, operatorPassword, roomName, roomName:operatorPassword

    "other-set-as-ready-notification": "{} a fost setat ca pregătit de {}", # User set as ready, user who set them as ready
    "other-set-as-not-ready-notification": "{} a fost setat ca nepregătit de {}", # User set as not ready, user who set them as not ready

    "file-different-notification": "Fișierul pe care îl redați pare să fie diferit de cel al lui {}",  # User
    "file-differences-notification": "Fișierul dumneavoastră diferă în următoarele moduri: {}",  # Differences
    "room-file-differences": "Diferențe de fișier: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "nume",
    "file-difference-filesize": "dimensiune",
    "file-difference-duration": "durată",
    "alone-in-the-room": "Sunteți singur în cameră",

    "different-filesize-notification": " (dimensiunea fișierului lor este diferită de a dumneavoastră!)",
    "userlist-playing-notification": "{} redă:",  # Username
    "file-played-by-notification": "Fișier: {} este redat de:",  # File
    "no-file-played-notification": "{} nu redă niciun fișier",  # Username
    "notplaying-notification": "Persoane care nu redau niciun fișier:",
    "userlist-room-notification":  "În camera '{}':",  # Room
    "userlist-file-notification": "Fișier",
    "controller-userlist-userflag": "Operator",
    "ready-userlist-userflag": "Pregătit",

    "update-check-failed-notification": "Nu s-a putut verifica automat dacă Syncplay {} este actualizat. Doriți să vizitați https://syncplay.pl/ pentru a verifica manual?",  # Syncplay version
    "syncplay-uptodate-notification": "Syncplay este actualizat",
    "syncplay-updateavailable-notification": "O nouă versiune de Syncplay este disponibilă. Doriți să vizitați pagina de lansare?",

    "mplayer-file-required-notification": "Syncplay cu mplayer necesită furnizarea unui fișier la pornire",
    "mplayer-file-required-notification/example": "Exemplu de utilizare: syncplay [opțiuni] [url|cale/]nume_fișier",
    "mplayer2-required": "Syncplay este incompatibil cu MPlayer 1.x, vă rugăm să utilizați mplayer2 sau mpv",

    "unrecognized-command-notification": "Comandă nerecunoscută",
    "commandlist-notification": "Comenzi disponibile:",
    "commandlist-notification/room": "\tr [nume] - schimbă camera",
    "commandlist-notification/list": "\tl - arată lista de utilizatori",
    "commandlist-notification/undo": "\tu - anulează ultima săritură",
    "commandlist-notification/pause": "\tp - comută pauza",
    "commandlist-notification/seek": "\t[s][+-]timp - sare la valoarea dată de timp, dacă + sau - nu este specificat, este timp absolut în secunde sau min:sec",
    "commandlist-notification/offset": "\to[+-]durată - decalează redarea locală cu durata dată (în secunde sau min:sec) față de poziția serverului - această funcție este depreciată",
    "commandlist-notification/help": "\th - acest ajutor",
    "commandlist-notification/toggle": "\tt - comută dacă sunteți pregătit să vizionați sau nu",
    "commandlist-notification/setready": "\tsr [nume] - setează utilizatorul ca pregătit",
    "commandlist-notification/setnotready": "\tsn [nume] - setează utilizatorul ca nepregătit",
    "commandlist-notification/create": "\tc [nume] - creează o cameră gestionată folosind numele camerei curente",
    "commandlist-notification/auth": "\ta [parolă] - autentifică ca operator al camerei cu parola operatorului",
    "commandlist-notification/chat": "\tch [mesaj] - trimite un mesaj de chat în cameră",
    "commandList-notification/queue": "\tqa [fișier/url] - adaugă fișierul sau url-ul la sfârșitul listei de redare",
    "commandList-notification/queueandselect": "\tqas [fișier/url] - adaugă fișierul sau url-ul la sfârșitul listei de redare și îl selectează",
    "commandList-notification/playlist": "\tql - arată lista de redare curentă",
    "commandList-notification/select": "\tqs [index] - selectează intrarea dată din lista de redare",
    "commandList-notification/next": "\tqn - selectează următoarea intrare din lista de redare",
    "commandList-notification/delete": "\tqd [index] - șterge intrarea dată din lista de redare",
    "syncplay-version-notification": "Versiune Syncplay: {}",  # syncplay.version
    "more-info-notification": "Mai multe informații disponibile la: {}",  # projectURL

    "gui-data-cleared-notification": "Syncplay a șters datele de cale și stare ale ferestrei folosite de interfață.",
    "language-changed-msgbox-label": "Limba va fi schimbată când reporniți Syncplay.",
    "promptforupdate-label": "Este în regulă ca Syncplay să verifice automat dacă există actualizări din când în când?",

    "media-player-latency-warning": "Atenție: Playerul media a răspuns în {} secunde. Dacă întâmpinați probleme de sincronizare, închideți aplicații pentru a elibera resurse, iar dacă nu funcționează, încercați un alt player media.",  # Seconds to respond
    "mpv-unresponsive-error": "mpv nu a răspuns de {} secunde, deci pare să aibă o defecțiune. Vă rugăm să reporniți Syncplay.",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "Apăsați Enter pentru a ieși\n",

    # Client errors
    "missing-arguments-error": "Lipsesc unele argumente necesare, consultați --help",
    "server-timeout-error": "Conexiunea cu serverul a expirat",
    "mpc-slave-error": "Nu se poate porni MPC în modul slave!",
    "mpc-version-insufficient-error": "Versiunea MPC nu este suficientă, vă rugăm să utilizați `mpc-hc` >= `{}`",
    "mpc-be-version-insufficient-error": "Versiunea MPC nu este suficientă, vă rugăm să utilizați `mpc-be` >= `{}`",
    "mpv-version-error": "Syncplay nu este compatibil cu această versiune de mpv. Vă rugăm să utilizați o altă versiune de mpv (de ex. Git HEAD).",
    "mpv-failed-advice": "Motivul pentru care mpv nu poate porni ar putea fi din cauza utilizării unor argumente de linie de comandă nesuportate sau a unei versiuni nesuportate de mpv.",
    "player-file-open-error": "Playerul nu a putut deschide fișierul",
    "player-path-error": "Calea playerului nu este setată corect. Playerele suportate sunt: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 și IINA",
    "hostname-empty-error": "Numele gazdei nu poate fi gol",
    "empty-error": "{} nu poate fi gol",  # Configuration
    "media-player-error": "Eroare player media: \"{}\"",  # Error line
    "unable-import-gui-error": "Nu s-au putut importa bibliotecile pentru interfața grafică. Trebuie să aveți versiunea corectă de PySide instalată pentru ca interfața grafică să funcționeze. Dacă doriți să rulați Syncplay în modul consolă, folosiți opțiunea --no-gui. Consultați https://syncplay.pl/guide/ pentru mai multe detalii.",
    "unable-import-twisted-error": "Nu s-a putut importa Twisted. Vă rugăm să instalați Twisted v16.4.0 sau mai recent.",

    "arguments-missing-error": "Lipsesc unele argumente necesare, consultați --help",

    "unable-to-start-client-error": "Nu se poate porni clientul",

    "player-path-config-error": "Calea playerului nu este setată corect. Playerele suportate sunt: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 și IINA.",
    "no-file-path-config-error": "Fișierul trebuie selectat înainte de a porni playerul",
    "no-hostname-config-error": "Numele gazdei nu poate fi gol",
    "invalid-port-config-error": "Portul trebuie să fie valid",
    "empty-value-config-error": "{} nu poate fi gol",  # Config option

    "not-json-error": "Nu este un șir codificat JSON\n",
    "hello-arguments-error": "Not enough Hello arguments\n",  # DO NOT TRANSLATE
    "version-mismatch-error": "Nepotrivire între versiunile clientului și serverului\n",
    "vlc-failed-connection": "Conectarea la VLC a eșuat. Dacă nu ați instalat syncplay.lua și folosiți cea mai recentă versiune de VLC, consultați https://syncplay.pl/LUA/ pentru instrucțiuni. Syncplay și VLC 4 nu sunt compatibile momentan, deci utilizați fie VLC 3, fie o alternativă cum ar fi mpv.",
    "vlc-failed-noscript": "VLC a raportat că scriptul de interfață syncplay.lua nu a fost instalat. Consultați https://syncplay.pl/LUA/ pentru instrucțiuni.",
    "vlc-failed-versioncheck": "Această versiune de VLC nu este suportată de Syncplay.",
    "vlc-initial-warning": 'VLC nu furnizează întotdeauna informații precise despre poziție către Syncplay, în special pentru fișierele .mp4 și .avi. Dacă întâmpinați probleme cu salturi eronate, încercați un alt player media precum <a href="https://mpv.io/">mpv</a> (sau <a href="https://github.com/stax76/mpv.net/">mpv.net</a> pentru utilizatorii Windows).',

    "feature-sharedPlaylists": "liste de redare partajate",  # used for not-supported-by-server-error
    "feature-chat": "chat",  # used for not-supported-by-server-error
    "feature-readiness": "pregătire",  # used for not-supported-by-server-error
    "feature-managedRooms": "camere gestionate",  # used for not-supported-by-server-error
    "feature-setOthersReadiness": "suprascriere stare pregătire",  # used for not-supported-by-server-error

    "not-supported-by-server-error": "Funcția {} nu este suportată de acest server.",  # feature
    "shared-playlists-not-supported-by-server-error": "Funcția de liste de redare partajate ar putea să nu fie suportată de server. Pentru a funcționa corect, este nevoie de un server care rulează Syncplay {}+, dar serverul rulează Syncplay {}.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "Funcția de listă de redare partajată a fost dezactivată în configurația serverului. Pentru a utiliza această funcție, trebuie să vă conectați la un alt server.",

    "invalid-seek-value": "Valoare de salt invalidă",
    "invalid-offset-value": "Valoare de decalaj invalidă",

    "switch-file-not-found-error": "Nu s-a putut comuta la fișierul '{0}'. Syncplay caută în directoarele media specificate.",  # File not found
    "folder-search-timeout-error": "Căutarea fișierelor media în directoare a fost anulată deoarece a durat prea mult să se caute în '{}' după procesarea primelor {:,} fișiere. Acest lucru se întâmplă dacă selectați un director cu prea multe subdirectoare în lista de directoare media sau dacă sunt prea multe fișiere de procesat. Pentru ca comutarea automată să funcționeze din nou, selectați Fișier->Setare directoare media din bara de meniu și eliminați acest director sau înlocuiți-l cu un subdirector corespunzător. Dacă directorul este de fapt în regulă, îl puteți reactiva selectând Fișier->Setare directoare media și apăsând 'OK'.",  # Folder, Files processed
    "folder-search-timeout-warning": "Atenție: A durat {} secunde să se scaneze {:,} fișiere în directorul '{}'. Acest lucru se întâmplă dacă selectați un director cu prea multe subdirectoare în lista de directoare media sau dacă sunt prea multe fișiere de procesat.",  # Folder, Files processed
    "folder-search-first-file-timeout-error": "Căutarea fișierelor media în '{}' a fost anulată deoarece a durat prea mult accesarea directorului. Acest lucru se poate întâmpla dacă este un disc de rețea sau dacă ați configurat discul să se oprească după o perioadă de inactivitate. Pentru ca comutarea automată să funcționeze din nou, mergeți la Fișier->Setare directoare media și eliminați directorul sau rezolvați problema (de ex. prin schimbarea setărilor de economisire a energiei).",  # Folder
    "added-file-not-in-media-directory-error": "Ați încărcat un fișier din '{}' care nu este un director media cunoscut. Puteți adăuga acest director selectând Fișier->Setare directoare media din bara de meniu.",  # Folder
    "no-media-directories-error": "Nu au fost setate directoare media. Pentru ca funcțiile de listă de redare partajată și comutare automată să funcționeze corect, selectați Fișier->Setare directoare media și specificați unde ar trebui Syncplay să caute fișiere media.",
    "cannot-find-directory-error": "Nu s-a putut găsi directorul media '{}'. Pentru a actualiza lista de directoare media, selectați Fișier->Setare directoare media din bara de meniu și specificați unde ar trebui Syncplay să caute fișiere media.",

    "failed-to-load-server-list-error": "Nu s-a putut încărca lista de servere publice. Vă rugăm să vizitați https://www.syncplay.pl/ în browser.",

    # Client arguments
    "argument-description": 'Soluție pentru sincronizarea redării mai multor instanțe de player media prin rețea.',
    "argument-epilog": 'Dacă nu sunt furnizate opțiuni, se vor folosi valorile din _config',
    "nogui-argument": 'nu afișa interfața grafică',
    "host-argument": "adresa serverului",
    "name-argument": 'numele de utilizator dorit',
    "debug-argument": 'modul depanare',
    "force-gui-prompt-argument": 'afișează fereastra de configurare',
    "no-store-argument": "nu stoca valorile în .syncplay",
    "room-argument": 'camera implicită',
    "password-argument": 'parola serverului',
    "player-path-argument": 'calea către executabilul playerului',
    "file-argument": 'fișier de redat',
    "args-argument": 'opțiuni player, dacă trebuie să transmiteți opțiuni care încep cu - prefixați-le cu argumentul \'--\'',
    "clear-gui-data-argument": 'resetează datele de cale și stare ale ferestrei stocate ca QSettings',
    "language-argument": 'limba pentru mesajele Syncplay ({})', # Languages

    "version-argument": 'afișează versiunea',
    "version-message": "Utilizați Syncplay versiunea {} ({})",

    "load-playlist-from-file-argument": "încarcă lista de redare din fișier text (o intrare pe linie)",


    # Client labels
    "config-window-title": "Configurare Syncplay",

    "connection-group-title": "Setări de conexiune",
    "host-label": "Adresa serverului: ",
    "name-label":  "Nume de utilizator (opțional):",
    "password-label":  "Parola serverului (dacă există):",
    "room-label": "Camera implicită: ",
    "roomlist-msgbox-label": "Editare listă camere (una pe linie)",

    "media-setting-title": "Setări player media",
    "executable-path-label": "Calea către playerul media:",
    "media-path-label": "Calea către video (opțional):",
    "player-arguments-label": "Argumente player (dacă există):",
    "browse-label": "Răsfoiește",
    "update-server-list-label": "Actualizează lista",

    "more-title": "Arată mai multe setări",
    "never-rewind-value": "Niciodată",
    "seconds-suffix": " sec",
    "privacy-sendraw-option": "Trimite brut",
    "privacy-sendhashed-option": "Trimite cu hash",
    "privacy-dontsend-option": "Nu trimite",
    "filename-privacy-label": "Informații despre numele fișierului:",
    "filesize-privacy-label": "Informații despre dimensiunea fișierului:",
    "checkforupdatesautomatically-label": "Verifică automat actualizările Syncplay",
    "autosavejoinstolist-label": "Adaugă camerele la care te alături în lista de camere",
    "slowondesync-label": "Încetinește la desincronizare minoră (nu este suportat pe MPC-HC/BE)",
    "rewindondesync-label": "Derulează înapoi la desincronizare majoră (recomandat)",
    "fastforwardondesync-label": "Derulează rapid înainte dacă rămâi în urmă (recomandat)",
    "dontslowdownwithme-label": "Nu încetini sau derula înapoi niciodată pe alții (experimental)",
    "pausing-title": "Pauză",
    "pauseonleave-label": "Pune pe pauză când un utilizator pleacă (de ex. dacă se deconectează)",
    "readiness-title": "Starea inițială de pregătire",
    "readyatstart-label": "Setează-mă ca 'pregătit' implicit",
    "forceguiprompt-label": "Nu afișa întotdeauna fereastra de configurare Syncplay",  # (Inverted)
    "showosd-label": "Activează mesajele OSD",

    "showosdwarnings-label": "Include avertismente (de ex. când fișierele sunt diferite, utilizatori nepregătiți)",
    "showsameroomosd-label": "Include evenimente din camera ta",
    "shownoncontrollerosd-label": "Include evenimente de la non-operatori în camerele gestionate",
    "showdifferentroomosd-label": "Include evenimente din alte camere",
    "showslowdownosd-label": "Include notificări de încetinire / revenire",
    "language-label": "Limbă:",
    "automatic-language": "Implicit ({})",  # Default language
    "showdurationnotification-label": "Avertizează despre nepotrivirile de durată media",
    "basics-label": "Elemente de bază",
    "readiness-label": "Redare/Pauză",
    "misc-label": "Diverse",
    "core-behaviour-title": "Comportamentul de bază al camerei",
    "syncplay-internals-title": "Componente interne Syncplay",
    "syncplay-mediasearchdirectories-title": "Directoare de căutare media",
    "syncplay-mediasearchdirectories-label": "Directoare de căutare media (o cale pe linie)",
    "sync-label": "Sincronizare",
    "sync-otherslagging-title": "Dacă alții rămân în urmă...",
    "sync-youlaggging-title": "Dacă tu rămâi în urmă...",
    "messages-label": "Mesaje",
    "messages-osd-title": "Setări afișare pe ecran",
    "messages-other-title": "Alte setări de afișare",
    "chat-label": "Chat",
    "privacy-label": "Confidențialitate",  # Currently unused
    "privacy-title": "Setări de confidențialitate",
    "unpause-title": "Dacă apăsați redare, setează ca pregătit și:",
    "unpause-ifalreadyready-option": "Reia dacă ești deja setat ca pregătit",
    "unpause-ifothersready-option": "Reia dacă ești deja pregătit sau alții din cameră sunt pregătiți (implicit)",
    "unpause-ifminusersready-option": "Reia dacă ești deja pregătit sau toți ceilalți sunt pregătiți și nr. min. de utilizatori este atins",
    "unpause-always": "Reia întotdeauna",
    "syncplay-trusteddomains-title": "Domenii de încredere (pentru servicii de streaming și conținut găzduit)",

    "chat-title": "Introducere mesaje chat",
    "chatinputenabled-label": "Activează introducerea de chat prin mpv",
    "chatdirectinput-label": "Permite introducerea instantă de chat (fără a apăsa Enter)",
    "chatinputfont-label": "Font introducere chat",
    "chatfont-label": "Setează font",
    "chatcolour-label": "Setează culoare",
    "chatinputposition-label": "Poziția zonei de introducere a mesajelor în mpv",
    "chat-top-option": "Sus",
    "chat-middle-option": "Mijloc",
    "chat-bottom-option": "Jos",
    "chatoutputheader-label": "Afișare mesaje chat",
    "chatoutputfont-label": "Font afișare chat",
    "chatoutputenabled-label": "Activează afișarea chat-ului în playerul media (doar mpv deocamdată)",
    "chatoutputposition-label": "Mod de afișare",
    "chat-chatroom-option": "Stil cameră de chat",
    "chat-scrolling-option": "Stil rulare",

    "mpv-key-tab-hint": "[TAB] pentru a comuta accesul la scurtăturile cu taste alfanumerice.",
    "mpv-key-hint": "[ENTER] pentru a trimite mesajul. [ESC] pentru a ieși din modul chat.",
    "alphakey-mode-warning-first-line": "Puteți folosi temporar scurtăturile mpv vechi cu tastele a-z.",
    "alphakey-mode-warning-second-line": "Apăsați [TAB] pentru a reveni la modul chat Syncplay.",

    "help-label": "Ajutor",
    "reset-label": "Restaurare setări implicite",
    "run-label": "Pornește Syncplay",
    "storeandrun-label": "Salvează configurația și pornește Syncplay",

    "contact-label": "Nu ezitați să trimiteți un e-mail la <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a>, <a href=\"https://github.com/Syncplay/syncplay/issues\"><nobr>creați un issue</nobr></a> pentru a raporta un bug pe GitHub, <a href=\"https://github.com/Syncplay/syncplay/discussions\"><nobr>începeți o discuție</nobr></a> pentru sugestii sau întrebări pe GitHub, <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>dați-ne like pe Facebook</nobr></a>, <a href=\"https://twitter.com/Syncplay/\"><nobr>urmăriți-ne pe Twitter</nobr></a>, sau vizitați <a href=\"https://syncplay.pl/\"><nobr>https://syncplay.pl/</nobr></a>. Nu utilizați Syncplay pentru a trimite informații sensibile.",

    "joinroom-label": "Intră în cameră",
    "joinroom-menu-label": "Intră în camera {}",
    "seektime-menu-label": "Sari la timp",
    "undoseek-menu-label": "Anulează saltul",
    "play-menu-label": "Redare",
    "pause-menu-label": "Pauză",
    "playbackbuttons-menu-label": "Afișează butoanele de redare",
    "autoplay-menu-label": "Afișează butonul de redare automată",
    "autoplay-guipushbuttonlabel": "Redă când toți sunt pregătiți",
    "autoplay-minimum-label": "Nr. min. utilizatori:",
    "hideemptyrooms-menu-label": "Ascunde camerele permanente goale",

    "sendmessage-label": "Trimite",

    "ready-guipushbuttonlabel": "Sunt pregătit să vizionez!",

    "roomuser-heading-label": "Cameră / Utilizator",
    "size-heading-label": "Dimensiune",
    "duration-heading-label": "Durată",
    "filename-heading-label": "Nume fișier",
    "notifications-heading-label": "Notificări",
    "userlist-heading-label": "Lista cine redă ce",

    "browseformedia-label": "Răsfoiește fișiere media",

    "file-menu-label": "&Fișier",  # & precedes shortcut key
    "openmedia-menu-label": "&Deschide fișier media",
    "openstreamurl-menu-label": "Deschide URL &stream media",
    "setmediadirectories-menu-label": "Setare &directoare media",
    "loadplaylistfromfile-menu-label": "Încarcă &lista de redare din fișier",
    "saveplaylisttofile-menu-label": "&Salvează lista de redare în fișier",
    "reconnect-menu-label": "&Reconectare la server",
    "exit-menu-label": "&Ieșire",
    "advanced-menu-label": "&Avansat",
    "window-menu-label": "&Fereastră",
    "setoffset-menu-label": "Setare &decalaj",
    "createcontrolledroom-menu-label": "&Creează cameră gestionată",
    "identifyascontroller-menu-label": "&Identifică-te ca operator",
    "settrusteddomains-menu-label": "Setare domenii de î&ncredere",
    "addtrusteddomain-menu-label": "Adaugă {} ca domeniu de încredere",  # Domain

    "edit-menu-label": "&Editare",
    "cut-menu-label": "De&cupare",
    "copy-menu-label": "&Copiere",
    "paste-menu-label": "&Lipire",
    "selectall-menu-label": "Selectează &tot",

    "playback-menu-label": "&Redare",

    "help-menu-label": "&Ajutor",
    "userguide-menu-label": "Deschide &ghidul utilizatorului",
    "update-menu-label": "Verifică &actualizări",

    "startTLS-initiated": "Se inițiază conexiunea securizată",
    "startTLS-secure-connection-ok": "Conexiune securizată stabilită ({})",
    "startTLS-server-certificate-invalid": 'Conexiunea securizată a eșuat. Serverul folosește un certificat de securitate invalid. Această comunicare ar putea fi interceptată de terți. Pentru mai multe detalii și depanare, consultați <a href="https://syncplay.pl/trouble">aici</a>.',
    "startTLS-server-certificate-invalid-DNS-ID": "Syncplay nu are încredere în acest server deoarece folosește un certificat care nu este valid pentru numele său de gazdă.",
    "startTLS-not-supported-client": "Acest client nu suportă TLS",
    "startTLS-not-supported-server": "Acest server nu suportă TLS",

    # TLS certificate dialog
    "tls-information-title": "Detalii certificat",
    "tls-dialog-status-label": "<strong>Syncplay folosește o conexiune criptată către {}.</strong>",
    "tls-dialog-desc-label": "Criptarea cu un certificat digital păstrează informațiile private în timp ce sunt trimise către sau de la<br/>serverul {}.",
    "tls-dialog-connection-label": "Informații criptate folosind Transport Layer Security (TLS), versiunea {} cu suita<br/>de cifrare: {}.",
    "tls-dialog-certificate-label": "Certificat emis de {} valid până la {}.",

    # About dialog
    "about-menu-label": "&Despre Syncplay",
    "about-dialog-title": "Despre Syncplay",
    "about-dialog-release": "Versiunea {} lansarea {}",
    "about-dialog-license-text": "Licențiat sub Apache&nbsp;License,&nbsp;Versiunea 2.0",
    "about-dialog-license-button": "Licență",
    "about-dialog-dependencies": "Dependențe",

    "setoffset-msgbox-label": "Setare decalaj",
    "offsetinfo-msgbox-label": "Decalaj (consultați https://syncplay.pl/guide/ pentru instrucțiuni de utilizare):",

    "promptforstreamurl-msgbox-label": "Deschide URL stream media",
    "promptforstreamurlinfo-msgbox-label": "URL stream",

    "addfolder-label": "Adaugă director",

    "adduris-msgbox-label": "Adaugă URL-uri la lista de redare (unul pe linie)",
    "editplaylist-msgbox-label": "Setare listă de redare (una pe linie)",
    "trusteddomains-msgbox-label": "Domenii la care este permisă comutarea automată (unul pe linie)",

    "createcontrolledroom-msgbox-label": "Creează cameră gestionată",
    "controlledroominfo-msgbox-label": "Introduceți numele camerei gestionate\r\n(consultați https://syncplay.pl/guide/ pentru instrucțiuni de utilizare):",

    "identifyascontroller-msgbox-label": "Identificare ca operator al camerei",
    "identifyinfo-msgbox-label": "Introduceți parola de operator pentru această cameră\r\n(consultați https://syncplay.pl/guide/ pentru instrucțiuni de utilizare):",

    "public-server-msgbox-label": "Selectați serverul public pentru această sesiune de vizionare",

    "megabyte-suffix": " MB",

    # Tooltips

    "host-tooltip": "Numele gazdei sau IP-ul la care să vă conectați, opțional cu port (de ex. syncplay.pl:8999). Sunteți sincronizat doar cu persoanele de pe același server/port.",
    "name-tooltip": "Porecla sub care veți fi cunoscut. Fără înregistrare, deci se poate schimba ușor ulterior. Un nume aleatoriu este generat dacă nu este specificat niciunul.",
    "password-tooltip": "Parolele sunt necesare doar pentru conectarea la servere private.",
    "room-tooltip": "Camera la care să vă alăturați la conectare poate fi aproape orice, dar veți fi sincronizat doar cu persoanele din aceeași cameră.",

    "edit-rooms-tooltip": "Editare listă camere.",

    "executable-path-tooltip": "Locația playerului media suportat ales (mpv, mpv.net, VLC, MPC-HC/BE, mplayer2 sau IINA).",
    "media-path-tooltip": "Locația video-ului sau stream-ului de deschis. Necesar pentru mplayer2.",
    "player-arguments-tooltip": "Argumente / comutatoare adiționale de linie de comandă de transmis acestui player media.",
    "mediasearcdirectories-arguments-tooltip": "Directoare unde Syncplay va căuta fișiere media, de ex. când folosiți funcția de clic pentru comutare. Syncplay va căuta recursiv în subdirectoare.",

    "more-tooltip": "Afișează setările mai rar utilizate.",
    "filename-privacy-tooltip": "Modul de confidențialitate pentru trimiterea numelui fișierului redat curent către server.",
    "filesize-privacy-tooltip": "Modul de confidențialitate pentru trimiterea dimensiunii fișierului redat curent către server.",
    "privacy-sendraw-tooltip": "Trimite această informație fără ofuscare. Aceasta este opțiunea implicită cu cele mai multe funcționalități.",
    "privacy-sendhashed-tooltip": "Trimite o versiune hash a informației, făcând-o mai puțin vizibilă pentru alți clienți.",
    "privacy-dontsend-tooltip": "Nu trimite această informație către server. Aceasta oferă confidențialitate maximă.",
    "checkforupdatesautomatically-tooltip": "Verifică periodic pe site-ul Syncplay dacă o nouă versiune este disponibilă.",
    "autosavejoinstolist-tooltip": "Când intrați într-o cameră pe un server, rețineți automat numele camerei în lista de camere.",
    "slowondesync-tooltip": "Reduce temporar viteza de redare când este necesar pentru a vă readuce în sincronizare cu ceilalți spectatori. Nu este suportat pe MPC-HC/BE.",
    "dontslowdownwithme-tooltip": "Înseamnă că alții nu sunt încetiniți sau derulați înapoi dacă redarea dumneavoastră rămâne în urmă. Util pentru operatorii de cameră.",
    "pauseonleave-tooltip": "Pune pe pauză redarea dacă sunteți deconectat sau cineva pleacă din camera dumneavoastră.",
    "readyatstart-tooltip": "Setați-vă ca 'pregătit' la pornire (altfel sunteți setat ca 'nepregătit' până când schimbați starea)",
    "forceguiprompt-tooltip": "Fereastra de configurare nu este afișată când se deschide un fișier cu Syncplay.",  # (Inverted)
    "nostore-tooltip": "Rulează Syncplay cu configurația dată, dar nu stochează permanent modificările.",  # (Inverted)
    "rewindondesync-tooltip": "Sare înapoi când este necesar pentru a reveni în sincronizare. Dezactivarea acestei opțiuni poate duce la desincronizări majore!",
    "fastforwardondesync-tooltip": "Sare înainte când nu sunteți sincronizat cu operatorul camerei (sau cu poziția pretinsă dacă 'Nu încetini sau derula înapoi niciodată pe alții' este activat).",
    "showosd-tooltip": "Trimite mesajele Syncplay către OSD-ul playerului media.",
    "showosdwarnings-tooltip": "Afișează avertismente dacă se redau fișiere diferite, ești singur în cameră, utilizatorii nu sunt pregătiți, etc.",
    "showsameroomosd-tooltip": "Afișează notificări OSD pentru evenimente din camera în care se află utilizatorul.",
    "shownoncontrollerosd-tooltip": "Afișează notificări OSD pentru evenimente legate de non-operatori care se află în camere gestionate.",
    "showdifferentroomosd-tooltip": "Afișează notificări OSD pentru evenimente din camerele în care nu se află utilizatorul.",
    "showslowdownosd-tooltip": "Afișează notificări de încetinire / revenire la diferență de timp.",
    "showdurationnotification-tooltip": "Util când lipsește un segment dintr-un fișier cu mai multe părți, dar poate genera alerte false.",
    "language-tooltip": "Limba utilizată de Syncplay.",
    "unpause-always-tooltip": "Dacă apăsați redare, vă setează întotdeauna ca pregătit și reia redarea, în loc să vă seteze doar ca pregătit.",
    "unpause-ifalreadyready-tooltip": "Dacă apăsați redare când nu sunteți pregătit, vă setează ca pregătit - apăsați redare din nou pentru a relua.",
    "unpause-ifothersready-tooltip": "Dacă apăsați redare când nu sunteți pregătit, va relua doar dacă alții sunt pregătiți.",
    "unpause-ifminusersready-tooltip": "Dacă apăsați redare când nu sunteți pregătit, va relua doar dacă alții sunt pregătiți și pragul minim de utilizatori este atins.",
    "trusteddomains-arguments-tooltip": "Domenii la care Syncplay are permisiunea de a comuta automat când listele de redare partajate sunt activate.",

    "chatinputenabled-tooltip": "Activează introducerea de chat în mpv (apăsați Enter pentru a scrie, Enter pentru a trimite, Escape pentru a anula)",
    "chatdirectinput-tooltip": "Nu mai este nevoie să apăsați 'Enter' pentru a intra în modul de introducere chat în mpv. Apăsați TAB în mpv pentru a dezactiva temporar această funcție.",
    "font-label-tooltip": "Font folosit la introducerea mesajelor de chat în mpv. Doar pe partea clientului, nu afectează ce văd alții.",
    "set-input-font-tooltip": "Familia de fonturi folosită la introducerea mesajelor de chat în mpv. Doar pe partea clientului, nu afectează ce văd alții.",
    "set-input-colour-tooltip": "Culoarea fontului folosită la introducerea mesajelor de chat în mpv. Doar pe partea clientului, nu afectează ce văd alții.",
    "chatinputposition-tooltip": "Locul în mpv unde va apărea textul de introducere chat când apăsați Enter și scrieți.",
    "chatinputposition-top-tooltip": "Plasează introducerea chat în partea de sus a ferestrei mpv.",
    "chatinputposition-middle-tooltip": "Plasează introducerea chat în centrul ferestrei mpv.",
    "chatinputposition-bottom-tooltip": "Plasează introducerea chat în partea de jos a ferestrei mpv.",
    "chatoutputenabled-tooltip": "Afișează mesajele de chat în OSD (dacă este suportat de playerul media).",
    "font-output-label-tooltip": "Font afișare chat.",
    "set-output-font-tooltip": "Font folosit la afișarea mesajelor de chat.",
    "chatoutputmode-tooltip": "Cum sunt afișate mesajele de chat.",
    "chatoutputmode-chatroom-tooltip": "Afișează linii noi de chat direct sub linia anterioară.",
    "chatoutputmode-scrolling-tooltip": "Rulează textul chat-ului de la dreapta la stânga.",

    "help-tooltip": "Deschide ghidul utilizatorului Syncplay.pl.",
    "reset-tooltip": "Resetează toate setările la configurația implicită.",
    "update-server-list-tooltip": "Se conectează la syncplay.pl pentru a actualiza lista de servere publice.",

    "sslconnection-tooltip": "Conectat securizat la server. Clic pentru detalii certificat.",

    "joinroom-tooltip": "Părăsește camera curentă și intră în camera specificată.",
    "seektime-msgbox-label": "Sari la timpul specificat (în secunde / min:sec). Folosiți +/- pentru salt relativ.",
    "ready-tooltip": "Indică dacă sunteți pregătit să vizionați.",
    "autoplay-tooltip": "Redare automată când toți utilizatorii cu indicator de pregătire sunt pregătiți și pragul minim de utilizatori este atins.",
    "switch-to-file-tooltip": "Dublu clic pentru a comuta la {}",  # Filename
    "sendmessage-tooltip": "Trimite mesaj în cameră",

    # In-userlist notes (GUI)
    "differentsize-note": "Dimensiune diferită!",
    "differentsizeandduration-note": "Dimensiune și durată diferite!",
    "differentduration-note": "Durată diferită!",
    "nofile-note": "(Niciun fișier în redare)",

    # Server messages to client
    "new-syncplay-available-motd-message": "Utilizați Syncplay {} dar o versiune mai nouă este disponibilă la https://syncplay.pl",  # ClientVersion
    "persistent-rooms-notice": "NOTĂ: Acest server folosește camere permanente, ceea ce înseamnă că informațiile listei de redare sunt stocate între sesiuni. Dacă doriți să creați o cameră unde informațiile nu sunt salvate, adăugați -temp la sfârșitul numelui camerei.", # NOTE: Do not translate the word -temp
    "ready-chat-message": "Am setat pe {} ca pregătit.", # User
    "not-ready-chat-message": "Am setat pe {} ca nepregătit.", # User

    # Server notifications
    "welcome-server-notification": "Bine ați venit pe serverul Syncplay, ver. {0}",  # version
    "client-connected-room-server-notification": "{0}({2}) s-a conectat la camera '{1}'",  # username, host, room
    "client-left-server-notification": "{0} a părăsit serverul",  # name
    "no-salt-notification": "VĂ RUGĂM SĂ NOTAȚI: Pentru ca parolele operatorilor de cameră generate de această instanță de server să funcționeze când serverul este repornit, adăugați următorul argument de linie de comandă când rulați serverul Syncplay în viitor: --salt {}",  # Salt


    # Server arguments
    "server-argument-description": 'Soluție pentru sincronizarea redării mai multor instanțe de player media prin rețea. Instanța server',
    "server-argument-epilog": 'Dacă nu sunt furnizate opțiuni, se vor folosi valorile din _config',
    "server-port-argument": 'port TCP al serverului',
    "server-password-argument": 'parola serverului',
    "server-isolate-room-argument": 'camerele ar trebui să fie izolate?',
    "server-salt-argument": "șir aleatoriu folosit pentru generarea parolelor camerelor gestionate",
    "server-disable-ready-argument": "dezactivează funcția de pregătire",
    "server-motd-argument": "calea către fișierul din care se va prelua mesajul zilei",
    "server-rooms-argument": "calea către fișierul bazei de date pentru stocarea/crearea datelor camerelor permanente. Permite camerelor să persiste fără spectatori și între reporniri",
    "server-permanent-rooms-argument": "calea către fișierul care listează camerele permanente care vor fi afișate chiar dacă sunt goale (sub formă de fișier text cu o cameră pe linie) - necesită activarea camerelor permanente",
    "server-chat-argument": "Ar trebui dezactivat chat-ul?",
    "server-chat-maxchars-argument": "Numărul maxim de caractere într-un mesaj de chat (implicit {})", # Default number of characters
    "server-maxusernamelength-argument": "Numărul maxim de caractere într-un nume de utilizator (implicit {})",
    "server-stats-db-file-argument": "Activează statisticile serverului folosind fișierul bazei de date SQLite furnizat",
    "server-startTLS-argument": "Activează conexiunile TLS folosind fișierele de certificat din calea furnizată",
    "server-messed-up-motd-unescaped-placeholders": "Mesajul zilei conține substituenți neescapați. Toate semnele $ ar trebui dublate ($$).",
    "server-messed-up-motd-too-long": "Mesajul zilei este prea lung - maximum {} caractere, {} furnizate.",
    "server-listen-only-on-ipv4": "Ascultă doar pe IPv4 la pornirea serverului.",
    "server-listen-only-on-ipv6": "Ascultă doar pe IPv6 la pornirea serverului.",
    "server-interface-ipv4": "Adresa IP de legare pentru IPv4. Lăsarea goală folosește toate.",
    "server-interface-ipv6": "Adresa IP de legare pentru IPv6. Lăsarea goală folosește toate.",

    # Server errors
    "unknown-command-server-error": "Comandă necunoscută {}",  # message
    "not-json-server-error": "Nu este un șir codificat JSON {}",  # message
    "line-decode-server-error": "Nu este un șir utf-8",
    "not-known-server-error": "Trebuie să fiți cunoscut de server înainte de a trimite această comandă",
    "client-drop-server-error": "Client deconectat: {} -- {}",  # host, error
    "password-required-server-error": "Parola este necesară",
    "wrong-password-server-error": "Parolă incorectă furnizată",
    "hello-server-error": "Not enough Hello arguments",  # DO NOT TRANSLATE

    # Playlists
    "playlist-selection-changed-notification":  "{} a schimbat selecția din lista de redare",  # Username
    "playlist-contents-changed-notification": "{} a actualizat lista de redare",  # Username
    "cannot-find-file-for-playlist-switch-error": "Nu s-a putut găsi fișierul {} în directoarele media pentru comutarea listei de redare!",  # Filename
    "cannot-add-duplicate-error": "Nu s-a putut adăuga a doua intrare pentru '{}' în lista de redare deoarece duplicatele nu sunt permise.",  # Filename
    "cannot-add-unsafe-path-error": "Nu s-a putut încărca automat {} deoarece nu este pe un domeniu de încredere. Puteți comuta manual la URL dând dublu clic pe el în lista de redare și adăugați domenii de încredere prin Fișier->Avansat->Setare domenii de încredere. Dacă dați clic dreapta pe un URL, puteți adăuga domeniul său ca domeniu de încredere din meniul contextual.",  # Filename
    "sharedplaylistenabled-label": "Activează listele de redare partajate",
    "removefromplaylist-menu-label": "Elimină din lista de redare",
    "shuffleremainingplaylist-menu-label": "Amestecă restul listei de redare",
    "shuffleentireplaylist-menu-label": "Amestecă întreaga listă de redare",
    "undoplaylist-menu-label": "Anulează ultima modificare a listei de redare",
    "addfilestoplaylist-menu-label": "Adaugă fișier(e) la sfârșitul listei de redare",
    "addurlstoplaylist-menu-label": "Adaugă URL(-uri) la sfârșitul listei de redare",
    "editplaylist-menu-label": "Editează lista de redare",

    "open-containing-folder": "Deschide directorul care conține acest fișier",
    "addyourfiletoplaylist-menu-label": "Adaugă fișierul tău la lista de redare",
    "addotherusersfiletoplaylist-menu-label": "Adaugă fișierul lui {} la lista de redare",  # [Username]
    "addyourstreamstoplaylist-menu-label": "Adaugă stream-ul tău la lista de redare",
    "addotherusersstreamstoplaylist-menu-label": "Adaugă stream-ul lui {} la lista de redare",  # [Username]
    "openusersstream-menu-label": "Deschide stream-ul lui {}",  # [username]'s
    "openusersfile-menu-label": "Deschide fișierul lui {}",  # [username]'s

    "setasready-menu-label": "Setează pe {} ca pregătit", # [Username]
    "setasnotready-menu-label": "Setează pe {} ca nepregătit", # [Username]

    "playlist-instruction-item-message": "Trageți un fișier aici pentru a-l adăuga la lista de redare partajată.",
    "sharedplaylistenabled-tooltip": "Operatorii de cameră pot adăuga fișiere la o listă de redare sincronizată pentru a facilita vizionarea aceluiași conținut. Configurați directoarele media în 'Diverse'.",

    "playlist-empty-error": "Lista de redare este momentan goală.",
    "playlist-invalid-index-error": "Index invalid în lista de redare",
}
