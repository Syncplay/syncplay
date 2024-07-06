# coding:utf8

"""Polish dictionary"""

# Filename, dictionary name and LANGUAGE-TAG value based on ISO country code. Language tag listed at https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/a9eac961-e77d-41a6-90a5-ce1a8b0cdb9c?redirectedfrom=MSDN

pl_PL = {
    "LANGUAGE": "Polski",
    "LANGUAGE-TAG": "pl_PL",

    # Strings for Windows NSIS installer
    "installer-language-file": "Polish.nlf", # Relevant .nlf file at https://github.com/kichik/nsis/tree/master/Contrib/Language%20files
    "installer-associate": "Powiąż Syncplay z plikami multimedialnymi.",
    "installer-shortcut": "Utwórz skrótki w następujących lokalizacjach:",
    "installer-start-menu": "Menu Start",
    "installer-desktop": "Desktop",
    "installer-quick-launch-bar": "Pasek Szybkiego Uruchomienia",
    "installer-automatic-updates": "Sprawdzaj automatycznie aktualizację",
    "installer-uninstall-configuration": "Usuń plik konfiguracyjny.",

    # Client notifications
    "config-cleared-notification": "Wyczyszczono ustawienia. Zmiany zostaną zapisane po wprowadzeniu prawidłowej konfiguracji.",

    "relative-config-notification": "Wczytano względne pliki konfiguracyjne: {}",

    "connection-attempt-notification": "Próba połączenia się do {}:{}",  # Port, IP
    "reconnection-attempt-notification": "Utracono połączenie z serwerem, podjęto próbę ponownego nawiązania połączenia",
    "disconnection-notification": "Rozłączono połączenie z serwerem",
    "connection-failed-notification": "Nie powiodło się połączenie z serwerem",
    "connected-successful-notification": "Pomyślne połączono się z serwerem",
    "retrying-notification": "%s, ponowna próba za %d sekund...",  # Seconds
    "reachout-successful-notification": "{} ({}) został pomyślnie zrealizowany",

    "rewind-notification": "Przewinięto z powodu różnicy czasu z {}",  # User
    "fastforward-notification": "Przewinięto naprzód ze względu na różnicę czasu z {}",  # User
    "slowdown-notification": "Spowolnienie spowodowane różnicą czasu z {}",  # User
    "revert-notification": "Przywracanie normalnej prędkości",

    "pause-notification": "{} spauzował w czasie {}",  # User, Time
    "unpause-notification": "{} odpauzował",  # User
    "seek-notification": "{} przeskoczył z czasu {} na {}",  # User, from time, to time

    "current-offset-notification": "Aktualne przesunięcie: {} sekund",  # Offset

    "media-directory-list-updated-notification": "Zaktualizowano foldery multimediów Syncplay.",

    "room-join-notification": "użytkownik {} dołączył do pokoju: „{}”",  # User
    "left-notification": "użytkownik {} wyszedł",  # User
    "left-paused-notification": "użytkownik {} wyszedł, {} spauzował",  # User who left, User who paused
    "playing-notification": "użytkownik {} odtwarza „{}” ({})",  # User, file, duration
    "playing-notification/room-addendum": " w pokoju: „{}”",  # Room

    "not-all-ready": "Nie gotowi: {}",  # Usernames
    "all-users-ready": "Każdy jest gotowy ({} użytkowników)",  # Number of ready users
    "ready-to-unpause-notification": "Jesteś teraz ustawiony jako gotowy - anuluj pauzę ponownie, aby anulować pauzę.",
    "set-as-ready-notification": "Jesteś teraz ustawiony jako gotowy",
    "set-as-not-ready-notification": "Jesteś teraz ustawiony jako niegotowy",
    "autoplaying-notification": "Auto odwarzanie za {} sekund...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Identyfikacja jako operator pokoju z hasłem „{}”...",
    "failed-to-identify-as-controller-notification": "Nie udało się zidentyfikować {} jako operatora pokoju.",
    "authenticated-as-controller-notification": "uwierzytelniono {} jako operator pokoju",

    "created-controlled-room-notification": "Utworzono pokój zarządzania „{}” z hasłem „{}”. Zachowaj te informacje na przyszłość!\n\nW pokojach zarządzanych wszyscy są zsynchronizowani z operatorem (operatorami) pokoju, którzy jako jedyni mogą wstrzymywać, cofać wstrzymanie, wyszukiwać i zmieniać playlistę.\n\nNależy poprosić zwykłych widzów o dołączenie do pokoju „{}”, ale operatorzy pokoju mogą dołączyć do pokoju „{}”, aby automatycznie się uwierzytelnić.",  # RoomName, operatorPassword, roomName, roomName:operatorPassword
    "file-different-notification": "Odtwarzany plik wydaje się być różny od pliku {}",  # User
    "file-differences-notification": "Plik różni się w następujący sposób: {}",  # Differences
    "room-file-differences": "Różnice plików:: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "nazwa",
    "file-difference-filesize": "rozmiar",
    "file-difference-duration": "długość",
    "alone-in-the-room": "Jesteś sam w pokoju",

    "different-filesize-notification": " (ich rozmiar pliku różni się od twojego!)",
    "userlist-playing-notification": "użytkownik {} odtwarza:",  # Username
    "file-played-by-notification": "Plik: {} jest odwarzany przez:",  # File
    "no-file-played-notification": "{} nie odwarza pliku",  # Username
    "notplaying-notification": "Użytkownicy, którzy nie odwarzają żaden plik:",
    "userlist-room-notification":  "W pokoju „{}”:",  # Room
    "userlist-file-notification": "Plik",
    "controller-userlist-userflag": "Operator",
    "ready-userlist-userflag": "Gotowy",

    "update-check-failed-notification": "Nie można automatycznie sprawdzić, czy Syncplay {} jest aktualny. Czy chcesz odwiedzić stronę https://syncplay.pl/, aby ręcznie sprawdzić dostępność aktualizacji?",  # Syncplay version
    "syncplay-uptodate-notification": "Syncplay jest aktualny",
    "syncplay-updateavailable-notification": "Nowa wersja Syncplay jest dostępna. Czy chcesz odwiedzić stronę wydania?",

    "mplayer-file-required-notification": "Syncplay przy użyciu mplayer wymaga podania pliku podczas uruchamiania",
    "mplayer-file-required-notification/example": "Przykład użycia: syncplay [options] [url|path]nazwa_pliku",
    "mplayer2-required": "Syncplay jest niekompatybilny z MPlayer 1.x, prosimy o użycie mplayer2 lub mpv.",

    "unrecognized-command-notification": "Nierozpoznana komenda",
    "commandlist-notification": "Dostępne komendy:",
    "commandlist-notification/room": "\tr [name] - zmień pokój",
    "commandlist-notification/list": "\tl - pokaż listę użytkowników",
    "commandlist-notification/undo": "\tu - Cofnij ostatnie wyszukiwaniek",
    "commandlist-notification/pause": "\tp - przełączanie pauzy",
    "commandlist-notification/seek": "\t[s][+-]czas - wyszukuje podaną wartość czasu, jeśli nie podano + lub -, jest to czas bezwzględny w sekundach lub min:sek.",
    "commandlist-notification/offset": "\to[+-]długość - przesunięcie lokalnego odtwarzania o podany czas trwania (w sekundach lub min:sek) od pozycji wyszukiwania na serwerze - jest to wycofana funkcja.",
    "commandlist-notification/help": "\th - Pomoc",
    "commandlist-notification/toggle": "\tt - przełączaj, gdy jesteś gotowy do oglądania, czy nie",
    "commandlist-notification/create": "\tc [name] - utworzenie pokoju zarządzanegp przy użyciu nazwy bieżącego pokoju",
    "commandlist-notification/auth": "\ta [password] - uwierzytelnienie jako operator pokoju za pomocą hasła operatora",
    "commandlist-notification/chat": "\tch [message] - wysyłanie wiadomości do czatu pokoju",
    "commandList-notification/queue": "\tqa [file/url] - dodaj plik lub adres URL do dołu playlisty",
    "commandList-notification/queueandselect": "\tqas [file/url] - dodaj plik lub adres URL do dołu playlisty i wybierz to",
    "commandList-notification/playlist": "\tql - pokaż aktualną playliste",
    "commandList-notification/select": "\tqs [index] - wybierz daną pozycję na playliście",
    "commandList-notification/next": "\tqn - wybór następnej pozycji na playliście",
    "commandList-notification/delete": "\tqd [index] - usuń podanną pozycje z listy ",
    "syncplay-version-notification": "Werjsa Syncplay: {}",  # syncplay.version
    "more-info-notification": "Więcej informacji dostępne są na: {}",  # projectURL

    "gui-data-cleared-notification": "Syncplay wyczyścił ścieżkę i dane okna używane przez GUI.",
    "language-changed-msgbox-label": "Język zostanie zmieniony po uruchomieniu Syncplay.",
    "promptforupdate-label": "Czy Syncplay może od czasu do czasu automatycznie sprawdzać dostępność aktualizacji?",

    "media-player-latency-warning": "Uwaga: Odtwarzacz multimediów potrzebował {} sekund na odpowiedź. Jeśli wystąpią problemy z synchronizacją, zamknij aplikacje, aby zwolnić zasoby systemowe, a jeśli to nie zadziała, wypróbuj inny odtwarzacz.",  # Seconds to respond
    "mpv-unresponsive-error": "mpv nie odpowiada od {} sekund, więc wygląda na to, że wystąpiła awaria. Uruchom ponownie Syncplay.",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "Wciśnij enter by wyjść\n",

    # Client errors
    "missing-arguments-error": "Brakuje niektórych niezbędnych argumentów, patrz --help",
    "server-timeout-error": "Upłynął limit czasu połączenia się z serwerem",
    "mpc-slave-error": "Nie można uruchomić MPC w trybie podrzędnym!",
    "mpc-version-insufficient-error": "Wersja MPC nie jest odpowiednia, należy użyć `mpc-hc` >= `{}`",
    "mpc-be-version-insufficient-error": "Wersja MPC nie jest odpowiednia, należy użyć `mpc-be` >= `{}`",
    "mpv-version-error": "Syncplay nie jest kompatybilny z tą wersją mpv. Użyj innej wersji mpv (np. Git HEAD).",
    "mpv-failed-advice": "Przyczyną braku możliwości uruchomienia mpv może być użycie nieobsługiwanych argumentów wiersza poleceń lub nieobsługiwana wersja mpv.",
    "player-file-open-error": "Odtwarzacz nie otworzył pliku",
    "player-path-error": "Ścieżka odtwarzacza nie jest prawidłowo ustawiona. Obsługiwane odtwarzacze to: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 i IINA.",
    "hostname-empty-error": "Nazwa hosta nie może być pusta",
    "empty-error": "{} nie może być pusta",  # Configuration
    "media-player-error": "Błąd odtwarzacza: \"{}\"",  # Error line
    "unable-import-gui-error": "Nie można zaimportować bibliotek GUI. Musisz mieć zainstalowaną poprawną wersję PySide, aby GUI działało. Jeśli chcesz uruchomić Syncplay w trybie konsoli, uruchom go z wiersza poleceń z przełącznikiem --no-gui. Więcej informacji można znaleźć na stronie https://syncplay.pl/guide/.",
    "unable-import-twisted-error": "Nie można zaimportować Twisted. Zainstaluj Twisted w wersji 16.4.0 lub nowszej.",

    "arguments-missing-error": "Brakuje niektórych niezbędnych argumentów, patrz --help",

    "unable-to-start-client-error": "Brak możliwości uruchomienia klienta",

    "player-path-config-error": "Odtwarzacz nie jest poprawnie ustawiony. Obsługiwane odtwarzacze to: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 i IINA.",
    "no-file-path-config-error": "Plik musi zostać wybrany przed uruchomieniem odtwarzacza",
    "no-hostname-config-error": "Nazwa hosta nie może być pusta",
    "invalid-port-config-error": "Port musi być prawidłowy",
    "empty-value-config-error": "{} nie może być pusty",  # Config option

    "not-json-error": "Nie jest to zakodowany ciąg json\n",
    "hello-arguments-error": "Not enough Hello arguments\n",  # DO NOT TRANSLATE
    "version-mismatch-error": "Niezgodność między wersjami klienta i serwera\n",
    "vlc-failed-connection": "Nie udało połączyć się z VLC. Jeśli nie zainstalowałeś syncplay.lua i używasz najnowszej wersji VLC, zapoznaj się z instrukcjami na stronie https://syncplay.pl/LUA/. Syncplay i VLC 4 nie są obecnie kompatybilne, więc użyj VLC 3 lub alternatywy, takiej jak mpv.",
    "vlc-failed-noscript": "VLC zgłosił, że skrypt interfejsu syncplay.lua nie został zainstalowany. Instrukcje można znaleźć na stronie https://syncplay.pl/LUA/.",
    "vlc-failed-versioncheck": "Ta wersja VLC nie jest obsługiwana przez Syncplay.",
    "vlc-initial-warning": 'VLC nie zawsze dostarcza dokładnych informacji o pozycji do Syncplay, szczególnie w przypadku plików .mp4 i .avi. Jeżeli doświadczasz problemów z błędnymi wyszukiwaniami, należy wypróbować alternatywny odtwarzacz multimedialny, taki jak <a href="https://mpv.io/">mpv</a> (lub <a href="https://github.com/stax76/mpv.net/">mpv.net</a> dla użytkowników Windows).',

    "feature-sharedPlaylists": "współdzielone playlisty",  # used for not-supported-by-server-error
    "feature-chat": "chat",  # used for not-supported-by-server-error
    "feature-readiness": "gotowość",  # used for not-supported-by-server-error
    "feature-managedRooms": "pokoje zarządzania",  # used for not-supported-by-server-error

    "not-supported-by-server-error": "Funkcja {} nie jest obsługiwana przez ten serwer.",  # feature
    "shared-playlists-not-supported-by-server-error": "Funkcja współdzielonych list odtwarzania może nie być obsługiwana przez serwer. Aby zapewnić jej prawidłowe działanie, wymagany jest serwer z uruchomionym Syncplay {}+, ale serwer z uruchomionym Syncplay {}.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "Funkcja współdzielonej playlisty została wyłączona w konfiguracji serwera. Aby skorzystać z tej funkcji, należy połączyć się z innym serwerem.",

    "invalid-seek-value": "Nieprawidłowa wartość wyszukiwania",
    "invalid-offset-value": "Nieprawidłowa wartość przesunięcia",

    "switch-file-not-found-error": "Nie można przełączyć do pliku '{0}'. Syncplay szuka w multimediów określonych folderach.",  # File not found
    "folder-search-timeout-error": "Wyszukiwanie multimediów w folderze multimediów zostało przerwane, ponieważ przeszukiwanie „{}” trwało zbyt długo. Taka sytuacja wystąpi, jeśli na liście folderów multimediów do przeszukania zostanie wybrany folder ze zbyt dużą liczbą podfolderów. Aby automatyczne przełączanie plików działało ponownie, wybierz Plik->Ustaw foldery multimediów na pasku menu i usuń ten folder lub zastąp go odpowiednim podfolderem. Jeśli folder jest w porządku, możesz go ponownie włączyć, wybierając Plik->Ustaw foldery multimediów i naciskając „OK”.",  # Folder
    "folder-search-first-file-timeout-error": "Wyszukiwanie nośnika w „{}” zostało przerwane, ponieważ uzyskanie dostępu do folderu trwało zbyt długo. Może się tak zdarzyć, jeśli jest to dysk sieciowy lub jeśli skonfigurowano dysk tak, aby wyłączał się po okresie bezczynności. Aby automatyczne przełączanie plików działało ponownie, przejdź do Plik->Ustaw foldery multimediów i usuń folder lub rozwiąż problem (np. zmieniając ustawienia oszczędzania energii).",  # Folder
    "added-file-not-in-media-directory-error": "You loaded a file in '{}' which is not a known media directory. You can add this as a media directory by selecting File->Set Media Directories in the menu bar.",  # Folder
    "no-media-directories-error": "Nie ustawiono żadnych folderów multimediów. Aby współdzielone listy odtwarzania i funkcje przełączania plików działały poprawnie, wybierz Plik->Ustaw foldery multimediów i określ, gdzie Syncplay ma szukać plików multimedialnych.",
    "cannot-find-directory-error": "Nie można znaleźć foldera multimediów „{}”. Aby zaktualizować listę folderów multimediów, wybierz Plik->Ustaw foldery multimediów z paska menu i określ, gdzie Syncplay powinien szukać plików multimedialnych.",

    "failed-to-load-server-list-error": "Nie udało się załadować listy serwerów publicznych. Odwiedź stronę https://www.syncplay.pl/ w przeglądarce.",

    # Client arguments
    "argument-description": 'Rozwiązanie do synchronizacji odtwarzania wielu instancji odtwarzaczy multimedialnych przez sieć.',
    "argument-epilog": 'Jeśli nie podano żadnych opcji, użyte zostaną wartości z _config',
    "nogui-argument": 'Nie pokazuj GUI',
    "host-argument": "adres serwera",
    "name-argument": 'wybrana nazwa użytkownika',
    "debug-argument": 'tryb debugowania',
    "force-gui-prompt-argument": 'wyświetlenie polecenia konfiguracji',
    "no-store-argument": "nie przechowuj wartości w .syncplay",
    "room-argument": 'domyślny pokój',
    "password-argument": 'hasło do serwera',
    "player-path-argument": 'ścieżka do pliku wykonywalnego odtwarzacza',
    "file-argument": 'plik do odtworzenia',
    "args-argument": 'opcje gracza, jeśli chcesz przekazać opcje zaczynające się od - poprzedzaj je pojedynczym argumentem \'--\'',
    "clear-gui-data-argument": 'resetuje ścieżkę i stan okna GUI przechowywane jako QSettings',
    "language-argument": 'język dla wiadomości Syncplay ({})', # Languages

    "version-argument": 'wyświetla swoją wersję',
    "version-message": "Używasz {} ({}) wersji Syncplay ",

    "load-playlist-from-file-argument": "wczytuje listę odtwarzania z pliku tekstowego (jeden wpis na wiersz)",


    # Client labels
    "config-window-title": "Konfiguracja Syncplay",

    "connection-group-title": "Ustawienia połączenia",
    "host-label": "Adres serwera: ",
    "name-label":  "Nazwa użytkownika (opcjonalnie):",
    "password-label":  "Hasło do serwera (jeśli jest):",
    "room-label": "Domyślny pokój: ",
    "roomlist-msgbox-label": "Edytuj listę pokoi (po jednym w wierszu)",

    "media-setting-title": "Ustawienia odtwarzacza multimedialnego",
    "executable-path-label": "Ścieżka do odtwarzacza multimedialnego:",
    "media-path-label": "Ścieżka do pliku wideo (opcjonalnie):",
    "player-arguments-label": "Argumenty odtwarzacza (jeśli jest):",
    "browse-label": "Przeglądaj",
    "update-server-list-label": "Zaktualizuj listę",

    "more-title": "Pokaż więcej opcji",
    "never-rewind-value": "Nigdy",
    "seconds-suffix": " sek.",
    "privacy-sendraw-option": "Wyślij bez szyfrowania",
    "privacy-sendhashed-option": "Wyślij z szyfrowaniem",
    "privacy-dontsend-option": "Nie wysyłaj",
    "filename-privacy-label": "Informacje o nazwie pliku:",
    "filesize-privacy-label": "Informacje o rozmiarze pliku:",
    "checkforupdatesautomatically-label": "Automatycznie sprawdzaj aktualizacje Syncplay",
    "autosavejoinstolist-label": "Dodaj pokoje, do których dołączyłeś, do listy pokoi",
    "slowondesync-label": "Spowolnienie przy niewielkiej desynchronizacji (nieobsługiwane w MPC-HC/BE)",
    "rewindondesync-label": "Przewijanie do tyłu przy dużej desynchronizacji (zalecane)",
    "fastforwardondesync-label": "Przewijanie do przodu w przypadku opóźnień (zalecane)",
    "dontslowdownwithme-label": "Nigdy nie zwalniaj ani nie przewijaj innych (eksperymentalne)",
    "pausing-title": "Pauza",
    "pauseonleave-label": "Pauzuj po wyjściu użytkownika (np. po rozłączeniu)",
    "readiness-title": "Początkowy stan gotowości",
    "readyatstart-label": "Domyślnie ustaw mnie jako „gotowego do oglądania”",
    "forceguiprompt-label": "Nie zawsze wyświetlaj okno konfiguracji Syncplay",  # (Inverted)
    "showosd-label": "Włącz komunikaty OSD",

    "showosdwarnings-label": "Dołącz ostrzeżenia (np. gdy pliki są różne, użytkownicy nie są gotowi)",
    "showsameroomosd-label": "Uwzględnij zdarzenia w swoim pokoju",
    "shownoncontrollerosd-label": "Uwzględnij zdarzenia od osób niebędących operatorami w zarządzanych pokojach",
    "showdifferentroomosd-label": "Uwzględnij wydarzenia w innych pokojach",
    "showslowdownosd-label": "Obejmuj spowolnienie / cofnięcie powiadomień",
    "language-label": "Język:",
    "automatic-language": "Domyślny język ({})",  # Default language
    "showdurationnotification-label": "Ostrzegaj o niedopasowaniu czasu trwania multimediów",
    "basics-label": "Podstawowe",
    "readiness-label": "Uruch./Pauza",
    "misc-label": "Różne",
    "core-behaviour-title": "Zachowanie w głównym pokoju",
    "syncplay-internals-title": "Elementy wewnętrzne Syncplay",
    "syncplay-mediasearchdirectories-title": "Folder do wyszukiwania multimediów",
    "syncplay-mediasearchdirectories-label": "Foldery do wyszukiwania multimediów (jedna ścieżka na linię)",
    "sync-label": "Synchronizacja",
    "sync-otherslagging-title": "Jeśli inni są z tyle przez opóżnienia...",
    "sync-youlaggging-title": "Jeśli ty jesteś w tyle przez opóżnienia...",
    "messages-label": "Wiadomości",
    "messages-osd-title": "Ustawienia wyświetlacza",
    "messages-other-title": "Inne ustawienia wyświetlacza",
    "chat-label": "Czat",
    "privacy-label": "Prywatność",  # Currently unused, but will be brought back if more space is needed in Misc tab
    "privacy-title": "Ustawienia prywatności",
    "unpause-title": "Jeśli naciśniesz przycisk odtwarzania, ustaw jako gotowy i:",
    "unpause-ifalreadyready-option": "Odpauzuj, jeśli jest już ustawiony jako gotowy",
    "unpause-ifothersready-option": "Odpauzuj, jeśli jest już gotowy lub inni w pokoju są gotowi (domyślnie)",
    "unpause-ifminusersready-option": "Odpauzuj, jeśli jest już gotowy lub jeśli wszyscy inni są gotowi i min. liczba użytkowników jest gotowa",
    "unpause-always": "Zawsze odpauzuj",
    "syncplay-trusteddomains-title": "Zaufane domeny (dla usług streamingowych i hostowanych treści)",

    "chat-title": "Wprowadzenie wiadomości do czatu",
    "chatinputenabled-label": "Włącz wprowadzanie wiadomości czatu przez mpv",
    "chatdirectinput-label": "Zezwalaj na natychmiastowe wprowadź wiadomość do czatu (omiń wciskanie klawisza Enter)",
    "chatinputfont-label": "Czcionka wprowadzania wiadomości czatu",
    "chatfont-label": "Ustaw czcionkę czatu",
    "chatcolour-label": "Ustaw kolor",
    "chatinputposition-label": "Pozycja obszaru wprowadzania komunikatu w mpv",
    "chat-top-option": "Góra",
    "chat-middle-option": "Środek",
    "chat-bottom-option": "Dół",
    "chatoutputheader-label": "Wyjście wiadomości czatu",
    "chatoutputfont-label": "Czcionka wyjścia wiadomości czatu",
    "chatoutputenabled-label": "Włącz wyjście czatu w odtwarzaczu multimedialnym (na razie dostępny tylko mpv))",
    "chatoutputposition-label": "Tryb wyjściowy",
    "chat-chatroom-option": "Styl czatu",
    "chat-scrolling-option": "Styl przewijania",

    "mpv-key-tab-hint": "[TAB], aby przełączyć dostęp do skrótów klawiszowych wiersza liter.",
    "mpv-key-hint": "[ENTER], aby wysłać wiadomość. [ESC], aby wyjść z trybu czatu.",
    "alphakey-mode-warning-first-line": "Można tymczasowo używać starych skrótów klawiaturowych mpv z klawiszami a-z.",
    "alphakey-mode-warning-second-line": "Naciśnij [TAB], aby powrócić do trybu czatu Syncplay.",

    "help-label": "Pomoc",
    "reset-label": "Przywróć ustawienia domyślne",
    "run-label": "Uruchom Syncplay",
    "storeandrun-label": "Zapisz konfigurację i uruchom Syncplay",

    "contact-label": "Śmiało pisz na email <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a>, <a href=\"https://github.com/Syncplay/syncplay/issues\"><nobr>zgłoś issue</nobr></a> w sprawie błędu/problemu poprzez GitHub, <a href=\"https://github.com/Syncplay/syncplay/discussions\"><nobr>rozpocznij dyskusje</nobr></a> by zgłosić sugestię lub zadać pytanie za pośrednictwem GitHub, <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>polub nas na Facebooku</nobr></a>, <a href=\"https://twitter.com/Syncplay/\"><nobr>obserwuj nas na X (Twitter)</nobr></a>, lub odwiedź <a href=\"https://syncplay.pl/\"><nobr>https://syncplay.pl/</nobr></a>. Nie używaj Syncplay do wysyłania poufnych informacji.",

    "joinroom-label": "Dołącz do pokoju",
    "joinroom-menu-label": "Dołącz do pokoju {}",
    "seektime-menu-label": "Wyszukaj do czasu",
    "undoseek-menu-label": "Cofnij wyszuiwanie",
    "play-menu-label": "Odtwórz",
    "pause-menu-label": "Pauzuj",
    "playbackbuttons-menu-label": "Pokaż przyciski odtwarzania",
    "autoplay-menu-label": "Pokaż przycisk automatycznego odtwarzania",
    "autoplay-guipushbuttonlabel": "Graj, gdy wszyscy będą gotowi",
    "autoplay-minimum-label": "minimalna liczba użytkowników:",
    "hideemptyrooms-menu-label": "Ukryj puste pokoje",

    "sendmessage-label": "Wyślij wiadomość",

    "ready-guipushbuttonlabel": "Jestem gotów do oglądania!",

    "roomuser-heading-label": "Pokój / Użytkownik",
    "size-heading-label": "Rozmiar",
    "duration-heading-label": "Długość",
    "filename-heading-label": "Nazwa pliku",
    "notifications-heading-label": "Powiadomienie",
    "userlist-heading-label": "Lista osób odtwarzających co",

    "browseformedia-label": "Przeglądanie plików multimedialnych",

    "file-menu-label": "&Plik",  # & precedes shortcut key
    "openmedia-menu-label": "&Otwór plik multimedialny",
    "openstreamurl-menu-label": "&Otwórz adres streamu URL",
    "setmediadirectories-menu-label": "Ustaw multimedia i &ścieżki",
    "loadplaylistfromfile-menu-label": "&Załaduj playlistę z pliku",
    "saveplaylisttofile-menu-label": "&Zapisz playlistę do pliku",
    "exit-menu-label": "W&",
    "advanced-menu-label": "&Zaawansowane",
    "window-menu-label": "&Okno",
    "setoffset-menu-label": "&Ustaw przesunięcia",
    "createcontrolledroom-menu-label": "&Utwórz pokój zarządzania",
    "identifyascontroller-menu-label": "&Zidentyfikuj się jako operator pokoju",
    "settrusteddomains-menu-label": "&Ustaw zaufane domeny",
    "addtrusteddomain-menu-label": "Dodaj {} jako zaufaną domene",  # Domain

    "edit-menu-label": "&Edycja",
    "cut-menu-label": "&Wytnij",
    "copy-menu-label": "&Kopiuj",
    "paste-menu-label": "&Wklej",
    "selectall-menu-label": "&Wybierz wszystko",

    "playback-menu-label": "&Playback",

    "help-menu-label": "&Pomoc",
    "userguide-menu-label": "&Otwór dokumentację użytkownika",
    "update-menu-label": "&Sprawdź aktualizację",

    "startTLS-initiated": "Próba nawiązania bezpiecznego połączenia",
    "startTLS-secure-connection-ok": "Nawiązano bezpieczne połączenie ({})",
    "startTLS-server-certificate-invalid": 'Bezpieczne połączenie nie powiodło się. Serwer używa nieprawidłowego certyfikatu bezpieczeństwa. Komunikacja może zostać przechwycona przez osoby trzecie. Dalsze szczegóły i rozwiązywanie problemów można znaleźć <a href="https://syncplay.pl/trouble">tutaj</a>.',
    "startTLS-server-certificate-invalid-DNS-ID": "Syncplay nie ufa temu serwerowi, ponieważ używa on certyfikatu, który nie jest ważny dla jego nazwy hosta.",
    "startTLS-not-supported-client": "Ten klient nie obsługuje protokołu TLS",
    "startTLS-not-supported-server": "Ten serwer nie obsługuje protokołu TLS",

    # TLS certificate dialog
    "tls-information-title": "Szczegóły certyfikatu",
    "tls-dialog-status-label": "<strong>Syncplay używa szyfrowanego połączenia z {}..</strong>",
    "tls-dialog-desc-label": "Szyfrowanie za pomocą certyfikatu cyfrowego zapewnia prywatność informacji przesyłanych do lub z<br/>serwera {}.",
    "tls-dialog-connection-label": "Informacje zaszyfrowane przy użyciu Transport Layer Security (TLS), wersja {} z szyfrem<br/>suite: {}.",
    "tls-dialog-certificate-label": "Certyfikat wydany przez {} ważny do {}.",

    # About dialog
    "about-menu-label": "&O Syncplay",
    "about-dialog-title": "O Syncplay",
    "about-dialog-release": "Wersja {} wydana {}",
    "about-dialog-license-text": "Licencjonowane na podstawie Apache&nbsp;License,&nbsp;Version 2.0",
    "about-dialog-license-button": "Licencja",
    "about-dialog-dependencies": "Zależności",

    "setoffset-msgbox-label": "Ustaw przesunięcie",
    "offsetinfo-msgbox-label": "Przesunięcie (instrukcje użytkowania znajdują się na stronie https://syncplay.pl/guide/):",

    "promptforstreamurl-msgbox-label": "Otwórz adres strumienia URL",
    "promptforstreamurlinfo-msgbox-label": "Strumień URL",

    "addfolder-label": "Dodaj folder",

    "adduris-msgbox-label": "Dodawanie adresów URL do listy odtwarzania (po jednym na wiersz)",
    "editplaylist-msgbox-label": "Ustaw playlistę (jedna na linię)",
    "trusteddomains-msgbox-label": "Domeny, na które można się automatycznie przełączać (jedna na wiersz)",

    "createcontrolledroom-msgbox-label": "Utwórz pokój zarządzania",
    "controlledroominfo-msgbox-label": "Wprowadź nazwę pokoju zarządzania\r\n (instrukcje użytkowania znajdują się na stronie https://syncplay.pl/guide/):",

    "identifyascontroller-msgbox-label": "Identyfikuj się jako operator pokoju",
    "identifyinfo-msgbox-label": "Wprowadź hasło operatora dla tego pokoju\r\n (instrukcje użytkowania znajdują się na stronie https://syncplay.pl/guide/):",

    "public-server-msgbox-label": "Wybierz serwer publiczny dla tej sesji przeglądania",

    "megabyte-suffix": " MB",

    # Tooltips

    "host-tooltip": "Nazwa hosta lub adres IP do połączenia, opcjonalnie wraz z portem (np. syncplay.pl:8999). Synchronizacja tylko z osobami na tym samym serwerze/porcie.",
    "name-tooltip": "Nazwa użytkownika, pod którym będziesz znany. Nie wymaga rejestracji, więc można go łatwo zmienić później. Jeśli nie zostanie podana, zostanie wygenerowana losowa nazwa.",
    "password-tooltip": "Hasła są potrzebne tylko do łączenia się z prywatnymi serwerami.",
    "room-tooltip": "Pokój, do którego można dołączyć po połączeniu, może być niemal dowolny, ale synchronizacja będzie możliwa tylko z osobami znajdującymi się w tym samym pokoju.",

    "edit-rooms-tooltip": "Edytuj listę pokoi.",

    "executable-path-tooltip": "Lokalizacja wybranego obsługiwanego odtwarzacza multimedialnego (mpv, mpv.net, VLC, MPC-HC/BE, mplayer2 lub IINA).",
    "media-path-tooltip": "Lokalizacja wideo lub strumienia do otworzenia. Niezbędne dla mplayer2.",
    "player-arguments-tooltip": "Dodatkowe polecenia / przełączniki wiersza poleceń do przekazania temu odtwarzaczowi multimedialnemu.",
    "mediasearcdirectories-arguments-tooltip": "Katalogi, w których Syncplay będzie wyszukiwać pliki multimedialne, np. podczas korzystania z funkcji kliknij, aby przełączyć. Syncplay będzie szukać rekursywnie w podfolderach.",

    "more-tooltip": "Wyświetlanie rzadziej używanych ustawień.",
    "filename-privacy-tooltip": "Tryb prywatności dla wysyłania aktualnie odtwarzanej nazwy pliku do serwera.",
    "filesize-privacy-tooltip": "Tryb prywatności dla wysyłania aktualnie rozmiaru pliku do serwera.",
    "privacy-sendraw-tooltip": "Wyślij te informacje bez maskowania. Jest to domyślna opcja dla większości funkcji.",
    "privacy-sendhashed-tooltip": "Wysyła zaszyfrowaną wersję informacji, dzięki czemu jest ona mniej widoczna dla innych klientów.",
    "privacy-dontsend-tooltip": "Nie wysyłaj tych informacji na serwer. Zapewnia to maksymalną prywatność.",
    "checkforupdatesautomatically-tooltip": "Regularnie sprawdzaj na stronie Syncplay, czy dostępna jest nowa wersja Syncplay.",
    "autosavejoinstolist-tooltip": "Po dołączeniu do pokoju na serwerze nazwa pokoju zostanie automatycznie zapamiętana na liście pokoi, do których można dołączyć.",
    "slowondesync-tooltip": "Zmniejsz tymczasowo szybkość odtwarzania w razie potrzeby, aby zsynchronizować się z innymi widzami. Funkcja nie jest obsługiwana przez MPC-HC/BE.",
    "dontslowdownwithme-tooltip": "Oznacza to, że inni nie są spowalniani lub przewijani, jeśli odtwarzanie jest opóźnione. Przydatne dla operatorów pomieszczeń.",
    "pauseonleave-tooltip": "Wstrzymaj odtwarzanie, jeśli zostaniesz rozłączony lub ktoś opuści Twój pokój.",
    "readyatstart-tooltip": "Ustaw się jako gotowy na początku (w przeciwnym razie będziesz ustawiony jako niegotowy, dopóki nie zmienisz stanu gotowości)",
    "forceguiprompt-tooltip": "Okno dialogowe konfiguracji nie jest wyświetlane podczas otwierania pliku za pomocą Syncplay.",  # (Inverted)
    "nostore-tooltip": "Uruchamia Syncplay z daną konfiguracją, ale nie przechowuje zmian na stałe.",  # (Inverted)
    "rewindondesync-tooltip": "Wskocz z powrotem, gdy jest to konieczne, aby przywrócić synchronizację. Wyłączenie tej opcji może skutkować poważnymi desynchronizacjami!",
    "fastforwardondesync-tooltip": "Przeskakuje do przodu, gdy nie jest zsynchronizowany z operatorem pokoju (lub udawaną pozycją, jeśli włączona jest opcja „Nigdy nie zwalniaj ani nie przewijaj innych”).",
    "showosd-tooltip": "Wysyła kominikaty Syncplay do OSD odtwarzacza multimedialnego.",
    "showosdwarnings-tooltip": "Wyświetlaj ostrzeżenia, jeśli odtwarzasz inny plik, jesteś sam w pokoju, użytkownicy nie są gotowi itp.",
    "showsameroomosd-tooltip": "Wyświetlanie powiadomień OSD o zdarzeniach związanych z pokojem, w którym znajduje się użytkownik.",
    "shownoncontrollerosd-tooltip": "Wyświetlanie powiadomień OSD o zdarzeniach dotyczących osób niebędących operatorami, które znajdują się w zarządzanych pokojach.",
    "showdifferentroomosd-tooltip": "Wyświetlanie powiadomień OSD o zdarzeniach związanych z pokojem, w którym nie znajduje się użytkownik.",
    "showslowdownosd-tooltip": "Wyświetlanie powiadomień o spowolnieniu / cofnięciu w zależności od różnicy czasu.",
    "showdurationnotification-tooltip": "Przydatne, gdy brakuje segmentu w wieloczęściowym pliku, ale może powodować fałszywe alarmy.",
    "language-tooltip": "Język używany przez Syncplay.",
    "unpause-always-tooltip": "Jeśli naciśniesz przycisk odpauzowania, zawsze ustawi cię jako gotowego i odpauzuje, a nie tylko jako gotowego.",
    "unpause-ifalreadyready-tooltip": "Jeśli naciśniesz odpauzowanie, gdy nie jesteś gotowy, ustawi cię jako gotowego - naciśnij odpauzowanie ponownie, aby anulować pauzę.",
    "unpause-ifothersready-tooltip": "Jeśli naciśniesz przycisk odpauzowania, gdy nie jesteś gotowy, zostanie on anulowany tylko wtedy, gdy inni będą gotowi.",
    "unpause-ifminusersready-tooltip": "Jeśli naciśniesz odpauzowanie, gdy nie jesteś gotowy, zostanie on wstrzymany tylko wtedy, gdy inni będą gotowi i zostanie osiągnięty minimalny próg użytkowników.",
    "trusteddomains-arguments-tooltip": "Domeny, na które Syncplay może się automatycznie przełączać po włączeniu współdzielonych playlist.",

    "chatinputenabled-tooltip": "Włącz czat w mpv (naciśnij enter, aby czatować, enter, aby wysłać, escape, aby anulować)",
    "chatdirectinput-tooltip": "Pomija konieczność naciśnięcia enter, aby przejść do trybu czatu w mpv. Naciśnij TAB w mpv, aby tymczasowo wyłączyć tę funkcję.",
    "font-label-tooltip": "Czcionka używana podczas pisania wiadomości na czacie w mpv. Dostępna tylko po stronie klienta, więc nie wpływa na to, co inni widzą.",
    "set-input-font-tooltip": "Rodzina czcionki używana podczas pisania wiadomości na czacie w mpv. Dostępna tylko po stronie klienta, więc nie wpływa na to, co inni widzą.",
    "set-input-colour-tooltip": "Kolor czcionki używana podczas pisania wiadomości na czacie w mpv. Dostępna tylko po stronie klienta, więc nie wpływa na to, co inni widzą.",
    "chatinputposition-tooltip": "Miejsce w mpv, w którym pojawi się tekst wprowadzania wiadomości czatu po naciśnięciu klawisza Enter i wpisaniu tekstu.",
    "chatinputposition-top-tooltip": "Ustaw okno wprowadzenia wiadomości na górze okna mpv.",
    "chatinputposition-middle-tooltip": "Ustaw okno wprowadzenia wiadomości na środku okna mpv.",
    "chatinputposition-bottom-tooltip": "Ustaw okno wprowadzenia wiadomości na dole okna mpv.",
    "chatoutputenabled-tooltip": "Wyświetlanie wiadomości czatu w OSD (jeśli jest obsługiwane przez odtwarzacz multimedialny).",
    "font-output-label-tooltip": "Czcionka wiadomości czatu.",
    "set-output-font-tooltip": "Czcionka używana podczas wyświetlania wiadomości z czatu.",
    "chatoutputmode-tooltip": "W jaki sposób wyświetlane są wiadomości czatu.",
    "chatoutputmode-chatroom-tooltip": "Wyświetla nowe wiersze czatu bezpośrednio pod poprzednim wierszem.",
    "chatoutputmode-scrolling-tooltip": "Przewijanie tekstu czatu od prawej do lewej.",

    "help-tooltip": "Otwiera podręcznik użytkowania Syncplay.pl.",
    "reset-tooltip": "Resetowanie wszystkich ustawień do konfiguracji domyślnej.",
    "update-server-list-tooltip": "Połącz się z syncplay.pl, aby zaktualizować listę serwerów publicznych.",

    "sslconnection-tooltip": "Bezpieczne połączono się z serwerem. Kliknij, aby wyświetlić szczegóły certyfikatu.",

    "joinroom-tooltip": "Opuść bieżący pokój i dołącz do określonego pokoju.",
    "seektime-msgbox-label": "Przeskok do określonego czasu (w sekundach / min:sek). Użyj +/- do względnego wyszukiwania.",
    "ready-tooltip": "Wskazuje twoją gotowość do oglądania.",
    "autoplay-tooltip": "AAutomatyczne odtwarzaj, gdy wszyscy użytkownicy posiadający znak gotowości, a minimalny próg użytkowników został osiągnięty.",
    "switch-to-file-tooltip": "Kliknij dwukrotnie, aby przełączyć się z pliku „{}”.",  # Filename
    "sendmessage-tooltip": "Wyślij wiadomość do pokoju",

    # In-userlist notes (GUI)
    "differentsize-note": "Inny rozmiar pliku!",
    "differentsizeandduration-note": "Inny rozmiar i długość pliku!",
    "differentduration-note": "Inna długość pliku!",
    "nofile-note": "(Nie jest odtwarzany żaden plik)",

    # Server messages to client
    "new-syncplay-available-motd-message": "Używasz Syncplay {}, ale jest dostępna nowsza wersja na stronie https://syncplay.pl.",  # ClientVersion
    "persistent-rooms-notice": "UWAGA: Ten serwer wykorzystuje stałe pokoje, co oznacza, że informacje o liście odtwarzania są przechowywane między sesjami odtwarzania. Jeśli chcesz utworzyć pokój, w którym informacje nie są zapisywane, umieść -temp na końcu nazwy pokoju.", # NOTE: Do not translate the word -temp

    # Server notifications
    "welcome-server-notification": "Witamy na serwerze Syncplay, ver. {0}",  # version
    "client-connected-room-server-notification": "{0}({2}) jest połączony z pokojem '{1}'",  # username, host, room
    "client-left-server-notification": "{0} wyszedł z serwera",  # name
    "no-salt-notification": "UWAGA: Aby hasła operatora pokoju wygenerowane przez tę instancję serwera nadal działały po ponownym uruchomieniu serwera, należy dodać następujący argument wiersza poleceń podczas uruchamiania serwera Syncplay w przyszłości: --salt {}",  # Salt


    # Server arguments
    "server-argument-description": 'Rozwiązanie do synchronizacji odtwarzania wielu instancji odtwarzacza multimediów przez sieć. Instancja serwera',
    "server-argument-epilog": 'Jeśli nie podano żadnych opcji, użyte zostaną wartości z _config',
    "server-port-argument": 'port TCP serwera',
    "server-password-argument": 'hasło serwera',
    "server-isolate-room-argument": 'Czy pokoje powinny być izolowane?',
    "server-salt-argument": "losowy ciąg używany do generowania haseł do pokojów zarządzanych",
    "server-disable-ready-argument": "yłączenie funkcji gotowości",
    "server-motd-argument": "ścieżka do pliku, z którego zostanie pobrany MOTD",
    "server-rooms-argument": "ścieżka do pliku bazy danych, który ma zostać użyty i/lub utworzony do przechowywania trwałych danych pokoju. Umożliwia zachowanie pokoi bez obserwatorów i po ponownym uruchomieniu.",
    "server-permanent-rooms-argument": "ścieżka do pliku z listą stałych pokoi, które będą wyświetlane nawet wtedy, gdy pokój jest pusty (w formie pliku tekstowego z listą pokoi w każdym wierszu) - wymaga włączenia opcji stałych pokoi",
    "server-chat-argument": "Czy czat powinien być wyłączony?",
    "server-chat-maxchars-argument": "Maksymalna liczba znaków w wiadomości do czatu (domyślnie {})", # Default number of characters
    "server-maxusernamelength-argument": "Maksymalna liczba znaków w nazwie użytkownika (domyślnie {})",
    "server-stats-db-file-argument": "Włącz statystyki serwera przy użyciu dostarczonego pliku bazy danych SQLite",
    "server-startTLS-argument": "Włączenie połączeń TLS przy użyciu plików certyfikatów w podanej ścieżce",
    "server-messed-up-motd-unescaped-placeholders": "Message of the Day zawiera symbole zastępcze unescaped. Wszystkie znaki $ powinny być podwojone ($$).",
    "server-messed-up-motd-too-long": "Treść Message of the Day jest zbyt długa - maksymalna długość znaków {}, wpisano {}.",
    "server-listen-only-on-ipv4": "Nasłuchuj tylko na IPv4 podczas uruchamiania serwera.",
    "server-listen-only-on-ipv6": "Nasłuchuj tylko na IPv6 podczas uruchamiania serwera.",
    "server-interface-ipv4": "Adres IP do powiązania dla IPv4. Pozostawienie pustego pola powoduje domyślne użycie opcji „all”.",
    "server-interface-ipv6": "Adres IP do powiązania dla IPv6. Pozostawienie pustego pola powoduje domyślne użycie opcji „all”.",

    # Server errors
    "unknown-command-server-error": "Nieznana komenda {}",  # message
    "not-json-server-error": "Nie jest zakodowanym ciągiem json {}",  # message
    "line-decode-server-error": "Nie jest ciągiem zgodnym ze standardem wutf-8",
    "not-known-server-error": "Musisz być znany serwerowi przed wysłaniem tej komendy",
    "client-drop-server-error": "Błąd u klienta: {} -- {}",  # host, error
    "password-required-server-error": "Wymagane hasło",
    "wrong-password-server-error": "Podano nieprawidłowe hasło",
    "hello-server-error": "Not enough Hello arguments",  # DO NOT TRANSLATE

    # Playlists
    "playlist-selection-changed-notification":  "Użytkownik {} zmienił wybór playlisty",  # Username
    "playlist-contents-changed-notification": "Użytkownik {} zaktualizował listę odtwarzania",  # Username
    "cannot-find-file-for-playlist-switch-error": "Nie można znaleźć pliku {} w folderach multimediów dla przełącznika playlisty!",  # Filename
    "cannot-add-duplicate-error": "Nie można dodać drugiego wpisu dla „{}” do playlisty, ponieważ duplikaty nie są dozwolone.",  # Filename
    "cannot-add-unsafe-path-error": "Nie można automatycznie załadować pliku „{}”, ponieważ nie znajduje się on w zaufanej domenie. Możesz ręcznie przełączyć się na adres URL, klikając go dwukrotnie na liście odtwarzania i dodać zaufane domeny za pomocą Plik->Zaawansowane->Ustaw zaufane domeny. Jeśli klikniesz adres URL prawym przyciskiem myszy, możesz dodać jego domenę jako zaufaną za pomocą menu kontekstowego.",  # Filename
    "sharedplaylistenabled-label": "Włącz udostępniane playlist",
    "removefromplaylist-menu-label": "Usuń z playlisty",
    "shuffleremainingplaylist-menu-label": "Losuj pozostałośc playlisty",
    "shuffleentireplaylist-menu-label": "Losuj całą playliste",
    "undoplaylist-menu-label": "Cofnij ostatnią zmianę w playliście",
    "addfilestoplaylist-menu-label": "Add pliki na dół playlisty",
    "addurlstoplaylist-menu-label": "Dodaj adresy URL na dole playlisty",
    "editplaylist-menu-label": "Edytuj playlistę",

    "open-containing-folder": "Otwórz folder zawierający ten plik",
    "addyourfiletoplaylist-menu-label": "Dodaj plik do playlisty",
    "addotherusersfiletoplaylist-menu-label": "Dodaj plik użytkownika {} do playlisty",  # [Username]
    "addyourstreamstoplaylist-menu-label": "Dodaj swój strumień do playlisty",
    "addotherusersstreamstoplaylist-menu-label": "Dodaj strumień użytkownika {} do playlisty",  # [Username]
    "openusersstream-menu-label": "Otwórz strumień użytkownika {}",  # [username]'s
    "openusersfile-menu-label": "Otwórz plik użytkownika {}",  # [username]'s

    "playlist-instruction-item-message": "Przeciągnij plik tutaj, aby dodać go do udostępnionej playlisty.",
    "sharedplaylistenabled-tooltip": "Operatorzy pokoi mogą dodawać pliki do zsynchronizowanej listy odtwarzania, aby ułatwić wszystkim oglądanie tego samego. Skonfiguruj foldery multimediów w sekcji „Różne”.",

    "playlist-empty-error": "Playlista jest obecnie pusta.",
    "playlist-invalid-index-error": "Nieprawidłowy indeks playlisty",
}
