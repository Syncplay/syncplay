# coding:utf8

"""Russian dictionary"""

ru = {
    "LANGUAGE" : u"Русский", #  (Russian)

    # Client notifications
    "config-cleared-notification" : u"Настройки сброшены. Изменения вступят в силу при сохранении корректной конфигурации.",

    "relative-config-notification" : u"Загружен(ы) файл(ы) относительной конфигурации: {}",

    "connection-attempt-notification" : u"Подключение к {}:{}",  # Port, IP
    "reconnection-attempt-notification" : u"Соединение с сервером потеряно, переподключение",
    "disconnection-notification" : u"Отключились от сервера",
    "connection-failed-notification" : u"Не удалось подключиться к серверу",
    "connected-successful-notification" : u"Соединение с сервером установлено",
    "retrying-notification" : u"%s, следующая попытка через %d секунд(ы)...",  # Seconds

    "rewind-notification" : u"Перемотано из-за разницы во времени с <{}>",  # User
    "fastforward-notification" : u"Ускорено из-за разницы во времени с <{}>",  # User
    "slowdown-notification" : u"Воспроизведение замедлено из-за разницы во времени с <{}>",  # User
    "revert-notification" : u"Возвращаемся к нормальной скорости воспроизведения",

    "pause-notification" : u"<{}> приостановил(а) воспроизведение",  # User
    "unpause-notification" : u"<{}> возобновил(а) воспроизведение",  # User
    "seek-notification" : u"<{}> перемотал с {} на {}",  # User, from time, to time

    "current-offset-notification" : u"Текущее смещение: {} секунд(ы)",  # Offset

    "media-directory-list-updated-notification" : u"Syncplay media directories have been updated.", # TODO: Translate

    "room-join-notification" : u"<{}> зашел(зашла) в комнату: '{}'",  # User
    "left-notification" : u"<{}> покинул(а) комнату",  # User
    "left-paused-notification" : u"<{}> покинул(а) комнату, <{}> приостановил(а) воспроизведение",  # User who left, User who paused
    "playing-notification" : u"<{}> включил '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum" : u" в комнате: '{}'",  # Room

    "not-all-ready" : u"Не готовы: {}", # Usernames
    "all-users-ready" : u"Все пользователи готовы ({} чел.)", #Number of ready users
    "ready-to-unpause-notification" : u"Вы помечены как готовый - нажмите еще раз, чтобы продолжить воспроизведение",
    "set-as-ready-notification" : u"Вы помечены как готовый",
    "set-as-not-ready-notification" : u"Вы помечены как неготовый",
    "autoplaying-notification" : u"Автовоспроизведение через {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification" : u"Идентификация как оператора комнаты с паролем '{}'...",
    "failed-to-identify-as-controller-notification" : u"<{}> не прошел идентификацию в качестве оператора комнаты.",
    "authenticated-as-controller-notification" : u"<{}> вошел как оператор комнаты.",
    "created-controlled-room-notification" : u"Создана управляемая комната '{}' с паролем '{}'. Сохраните эти данные!", # RoomName, operatorPassword

    "file-different-notification" : u"Вероятно, файл, который Вы смотрите, отличается от того, который смотрит <{}>.",  # User
    "file-differences-notification" : u"Ваш файл отличается: {}", # Differences
    "room-file-differences" : u"Несовпадения файла: {}", # File differences (filename, size, and/or duration)
    "file-difference-filename" : u"имя",
    "file-difference-filesize" : u"размер",
    "file-difference-duration" : u"длительность",
    "alone-in-the-room" : u"В этой комнате кроме Вас никого нет.",

    "different-filesize-notification" : u" (размер Вашего файла не совпадает с размером их файла!)",
    "userlist-playing-notification" : u"{} смотрит:", #Username
    "file-played-by-notification" : u"Файл: {} просматривают:",  # File
    "no-file-played-notification" : u"{} не смотрит ничего", # Username
    "notplaying-notification" : u"Люди, которые не смотрят ничего:",
    "userlist-room-notification" : u"В комнате '{}':",  # Room
    "userlist-file-notification" : u"Файл",
    "controller-userlist-userflag" : u"Оператор",
    "ready-userlist-userflag" : u"Готов",

    "update-check-failed-notification" : u"Невозможно автоматически проверить, что версия Syncplay {} все еще актуальна. Хотите зайти на http://syncplay.pl/ и вручную проверить наличие обновлений?",
    "syncplay-uptodate-notification" : u"Syncplay обновлен",
    "syncplay-updateavailable-notification" : u"Доступна новая версия Syncplay. Хотите открыть страницу релиза?",

    "mplayer-file-required-notification" : u"Для использования Syncplay с mplayer необходимо передать файл в качестве параметра",
    "mplayer-file-required-notification/example" : u"Пример использования: syncplay [options] [url|path/]filename",
    "mplayer2-required" : u"Syncplay не совместим с MPlayer 1.x, пожалуйста, используйте mplayer2 или mpv",

    "unrecognized-command-notification" : u"Неизвестная команда.",
    "commandlist-notification" : u"Доступные команды:",
    "commandlist-notification/room" : u"\tr [name] - сменить комнату",
    "commandlist-notification/list" : u"\tl - показать список пользователей",
    "commandlist-notification/undo" : u"\tu - отменить последнюю перемотку",
    "commandlist-notification/pause" : u"\tp - вкл./выкл. паузу",
    "commandlist-notification/seek" : u"\t[s][+-]time - перемотать к заданному моменту времени, если не указан + или -, то время считается абсолютным (от начала файла) в секундах или мин:сек",
    "commandlist-notification/help" : u"\th - помощь",
    "commandlist-notification/toggle" : u"\tt - переключить статус готов/неготов к просмотру",
    "commandlist-notification/create" : u"\tc [name] - создать управляемую комнату с таким же именем, как у текущей",
    "commandlist-notification/auth" : u"\ta [password] - авторизоваться как оператор комнаты с помощью пароля",
    "syncplay-version-notification" : u"Версия Syncplay: {}",  # syncplay.version
    "more-info-notification" : u"Больше информации на {}",  # projectURL

    "gui-data-cleared-notification" : u"Syncplay очистил путь и информацию о состоянии окна, использованного GUI.",
    "language-changed-msgbox-label" : u"Язык переключится при следующем запуске SYncplay.",
    "promptforupdate-label" : u"Вы не против, если Syncplay будет автоматически изредка проверять наличие обновлений?",

    "vlc-version-mismatch": u"This version of VLC does not support Syncplay. VLC {}+ supports Syncplay but VLC 3 does not. Please use an alternative media player.", # VLC min version # TODO: Translate
    "vlc-interface-version-mismatch" : u"В используете модуль интерфейса Syncplay устаревшей версии {} для VLC. К сожалению, Syncplay способен работать с версией {} и выше. Пожалуйста, обратитесь к Руководству Пользователя Syncplay (http://syncplay.pl/guide/) за инструкциями о том, как установить syncplay.lua.",  # VLC interface version, VLC interface min version
    "vlc-interface-oldversion-warning" : u"Внимание: Syncplay обнаружил, что старая версия модуля интерфейса Syncplay для VLC уже установлена в директорию VLC. Пожалуйста, обратитесь к Руководству Пользователя Syncplay (http://syncplay.pl/guide/) за инструкциями о том, как установить syncplay.lua.",
    "vlc-interface-not-installed" : u"Внимание: Модуль интерфейса Syncplay для VLC не обнаружен в директории VLC. По существу, если Вы используете VLC 2.0, то VLC будет использовать модуль syncplay.lua из директории Syncplay, но в таком случае другие пользовательские скрипты и расширения интерфейса не будут работать. Пожалуйста, обратитесь к Руководству Пользователя Syncplay (http://syncplay.pl/guide/) за инструкциями о том, как установить syncplay.lua.",
    "media-player-latency-warning": u"Внимание: У Вашего проигрывателя слишком большой отклик ({} секунд). Если Вы замечаете проблемы с синхронизацией, то закройте ресурсоемкие приложения, а если это не помогло - попробуйте другой проигрыватель.", # Seconds to respond
    "mpv-unresponsive-error": u"mpv has not responded for {} seconds so appears to have malfunctioned. Please restart Syncplay.", # Seconds to respond # TODO: Translate to Russian

    # Client prompts
    "enter-to-exit-prompt" : u"Для выхода нажмите Enter\n",

    # Client errors
    "missing-arguments-error" : u"Некоторые необходимые аргументы отсутствуют, обратитесь к --help",
    "server-timeout-error" : u"Подключение к серверу превысило лимит времени",
    "mpc-slave-error" : u"Невозможно запустить MPC в slave режиме!",
    "mpc-version-insufficient-error" : u"Версия MPC слишком старая, пожалуйста, используйте `mpc-hc` >= `{}`",
    "mpv-version-error" : u"Syncplay не совместим с данной версией mpv. Пожалуйста, используйте другую версию mpv (лучше свежайшую).",
    "player-file-open-error" : u"Проигрыватель не может открыть файл.",
    "player-path-error" : u"Путь к проигрывателю задан неверно.",
    "hostname-empty-error" : u"Имя пользователя не может быть пустым.",
    "empty-error" : u"{} не может быть пустым.",  # Configuration
    "media-player-error" : u"Ошибка проигрывателя: \"{}\"",  # Error line
    "unable-import-gui-error" : u"Невозможно импортировать библиотеки GUI (графического интерфейса). Необходимо установить PySide, иначе графический интерфейс не будет работать.",

    "arguments-missing-error" : u"Некоторые необходимые аргументы отсутствуют, обратитесь к --help",

    "unable-to-start-client-error" : u"Невозможно запустить клиент",

    "player-path-config-error": u"Путь к проигрывателю установлен неверно",
    "no-file-path-config-error" : u"Файл должен быть указан до включения проигрывателя",
    "no-hostname-config-error": u"Имя сервера не может быть пустым",
    "invalid-port-config-error" : u"Неверный номер порта",
    "empty-value-config-error" : u"Поле '{}' не может быть пустым", # Config option

    "not-json-error" : u"Не является закодированной json-строкой\n",
    "hello-arguments-error" : u"Не хватает аргументов Hello\n",
    "version-mismatch-error" : u"Конфликт версий между клиентом и сервером\n",
    "vlc-failed-connection" : u"Ошибка подключения к VLC. Если у Вас не установлен syncplay.lua, то обратитесь к http://syncplay.pl/LUA/ за инструкциями.",
    "vlc-failed-noscript" : u"VLC сообщает, что скрипт интерфейса syncplay.lua не установлен. Пожалуйста, обратитесь к http://syncplay.pl/LUA/ за инструкциями.",
    "vlc-failed-versioncheck" : u"Данная версия VLC не поддерживается Syncplay. Пожалуйста, используйте VLC версии 2 или выше.",
    "vlc-failed-other" : u"Во время загрузки скрипта интерфейса syncplay.lua в VLC произошла следующая ошибка: {}",  # Syncplay Error

    "not-supported-by-server-error" : u"Эта возможность не поддерживается сервером. The feature requires a server running Syncplay {}+, but the server is running Syncplay {}.", #minVersion, serverVersion #TODO: Translate into Russian
    "shared-playlists-not-supported-by-server-error" : "The shared playlists feature may not be supported by the server. To ensure that it works correctly requires a server running Syncplay  {}+, but the server is running Syncplay {}.", #minVersion, serverVersion # TODO: Translate

    "invalid-seek-value" : u"Некорректное значение для перемотки",
    "invalid-offset-value" : u"Некорректное смещение",

    "switch-file-not-found-error" : u"Невозможно переключиться на файл '{0}'. Syncplay looks in the folder specified media directories.", # File not found # TODO: Translate last part into Russian
    "folder-search-timeout-error" : u"The search for media in media directories was aborted as it took too long to search through '{}'. This will occur if you select a folder with too many sub-folders in your list of media folders to search through. For automatic file switching to work again please select File->Set Media Directories in the menu bar and remove this directory or replace it with an appropriate sub-folder.", #Folder # TODO: Translate
    "folder-search-first-file-timeout-error" : u"The search for media in '{}' was aborted as it took too long to access the directory. This could happen if it is a network drive or if you configure your drive to spin down after a period of inactivity. For automatic file switching to work again please go to File->Set Media Directories and either remove the directory or resolve the issue (e.g. by changing power saving settings).", #Folder # TODO: Translate
    "added-file-not-in-media-directory-error" : u"You loaded a file in '{}' which is not a known media directory. You can add this as a media directory by selecting File->Set Media Directories in the menu bar.", #Folder #TODO: Translate
    "no-media-directories-error" : u"No media directories have been set. For shared playlist and file switching features to work properly please select File->Set Media Directories and specify where Syncplay should look to find media files.", # TODO: Translate
    "cannot-find-directory-error" : u"Could not find media directory '{}'. To update your list of media directories please select File->Set Media Directories from the menu bar and specify where Syncplay should look to find media files.", # TODO: Translate

    "failed-to-load-server-list-error" : u"Failed to load public server list. Please visit http://www.syncplay.pl/ in your browser.", # TODO: Translate into Russian

    # Client arguments
    "argument-description" : u'Решение для синхронного воспроизведения в VLC, MPlayer или MPC-HC через Интернет.',
    "argument-epilog" : u'Если параметр не будет передан, то будет использоваться значение, указанное в _config.',
    "nogui-argument" : u'не использовать GUI',
    "host-argument" : u'адрес сервера',
    "name-argument" : u'желательное имя пользователя',
    "debug-argument" : u'режим отладки',
    "force-gui-prompt-argument" : u'показать окно настройки',
    "no-store-argument" : u'не сохранять данные в .syncplay',
    "room-argument" : u'начальная комната',
    "password-argument" : u'пароль для доступа к серверу',
    "player-path-argument" : u'путь к исполняемому файлу Вашего проигрывателя',
    "file-argument" : u'воспроизводимый файл',
    "args-argument" : u'параметры проигрывателя; если нужно передать параметры, начинающиеся с - , то сначала пишите \'--\'',
    "clear-gui-data-argument" : u'сбрасывает путь и данные о состоянии окна GUI, хранимые как QSettings',
    "language-argument" : u'язык сообщений Syncplay (de/en/ru)',

    "version-argument" : u'выводит номер версии',
    "version-message" : u"Вы используете Syncplay версии {} ({})",

    # Client labels
    "config-window-title" : u"Настройка Syncplay",

    "connection-group-title" : u"Параметры подключения",
    "host-label" : u"Адрес сервера: ",
    "name-label" : u"Имя пользователя (не обязательно):",
    "password-label" : u"Пароль к серверу (если требуется):",
    "room-label" : u"Начальная комната: ",

    "media-setting-title" : u"Параметры проигрывателя",
    "executable-path-label" : u"Путь к проигрывателю:",
    "media-path-label" : u"Путь к видеофайлу:",
    "player-arguments-label" : u"Аргументы для запуска проигрывателя:",
    "browse-label" : u"Выбрать",
    "update-server-list-label" : u"Update list", # TODO: Translate into Russian

    "more-title" : u"Больше настроек",
    "never-rewind-value" : u"Никогда",
    "seconds-suffix" : u" секунд(ы)",
    "privacy-sendraw-option" : u"отпр. как есть",
    "privacy-sendhashed-option" : u"отпр. хэш",
    "privacy-dontsend-option" : u"не отпр.",
    "filename-privacy-label" : u"Имя файла:",
    "filesize-privacy-label" : u"Размер файла:",
    "checkforupdatesautomatically-label" : u"Проверять обновления автоматически",
    "slowondesync-label" : u"Замедлять при небольших рассинхронизациях (не поддерживаетя в MPC-HC)",
    "rewindondesync-label" : u"Перемотка при больших рассинхронизациях (настоятельно рекомендуется)",
    "dontslowdownwithme-label" : u"Никогда не замедлять и не перематывать видео другим (функция тестируется)",
    "pauseonleave-label" : u"Приостанавливать, когда кто-то уходит (например, отключился)",
    "readyatstart-label" : u"Выставить статус 'готово к просмотру' по умолчанию",
    "fastforwardondesync-label" : u"Ускорять видео при отставании (рекомендуется)",
    "forceguiprompt-label" : u"Не показывать больше этот диалог", # (Inverted)
    "showosd-label" : u"Включить экранные сообщения (поверх видео)",

    "showosdwarnings-label" : u"Показывать предупреждения (напр., когда файлы не совпадают)",
    "showsameroomosd-label" : u"Показывать события Вашей комнаты",
    "shownoncontrollerosd-label" : u"Включить события, связанные с не-операторами в управляемой комнате.",
    "showdifferentroomosd-label" : u"Показывать события других комнат",
    "showslowdownosd-label" : u"Показывать уведомления о замедлении/перемотке",
    "language-label" : u"Язык:",
    "automatic-language" : u"По умолчанию ({})", # Automatic language
    "showdurationnotification-label" : u"Предупреждать о несовпадении продолжительности видео",
    "basics-label" : u"Основное",
    "readiness-label" : u"Воспроизведение/Пауза", # TODO: Confirm translation of play/pause
    "misc-label" : u"Прочее",
    "core-behaviour-title" : u"Core room behaviour", # TODO: Translate into Russian
    "syncplay-internals-title" : u"Syncplay internals", # TODO: Translate into Russian
    "syncplay-mediasearchdirectories-title" : u"Directories to search for media (one path per line)", # TODO: Translate into Russian
    "sync-label" : u"Синхронизация",
    "sync-otherslagging-title" : u"При отставании других зрителей...",
    "sync-youlaggging-title" : u"Когда я отстаю ...",
    "messages-label" : u"Сообщения",
    "messages-osd-title" : u"Настройки OSD",
    "messages-other-title" : u"Другие настройки отображения",
    "privacy-label" : u"Приватность",
    "privacy-title" : u"Настройки приватности",
    "unpause-title" : u"If you press play, set as ready and:", # TODO: Translate into Russian
    "unpause-ifalreadyready-option" : u"Unpause if already set as ready", # TODO: Translate into Russian
    "unpause-ifothersready-option" : u"Unpause if already ready or others in room are ready (default)", # TODO: Translate into Russian
    "unpause-ifminusersready-option" : u"Unpause if already ready or if all others ready and min users ready", # TODO: Translate into Russian
    "unpause-always" : u"Always unpause", # TODO: Translate into Russian
    "syncplay-trusteddomains-title": u"Trusted domains (for streaming services and hosted content)", # TODO: Translate into Russian
"addtrusteddomain-menu-label" : u"Add {} as trusted domain", # Domain # TODO: Translate

    "help-label" : u"Помощь",
    "reset-label" : u"Сброс настроек",
    "run-label" : u"Запустить Syncplay",
    "storeandrun-label" : u"Сохранить настройки и зап. Syncplay",

    "contact-label" : u"Есть идея, нашли ошибку или хотите оставить отзыв? Пишите на <a href=\"mailto:dev@syncplay.pl\">dev@syncplay.pl</a>, в <a href=\"https://webchat.freenode.net/?channels=#syncplay\">IRC канал #Syncplay</a> на irc.freenode.net или <a href=\"https://github.com/Uriziel/syncplay/issues\">задавайте вопросы через GitHub</a>. Кроме того, заходите на <a href=\"http://syncplay.pl/\">http://syncplay.pl/</a> за инорфмацией, помощью и обновлениями!",

    "joinroom-label" : u"Зайти в комнату",
    "joinroom-menu-label" : u"Зайти в комнату {}", #TODO: Might want to fix this
    "seektime-menu-label" : u"Перемотать",
    "undoseek-menu-label" : u"Отменить перемотку",
    "play-menu-label" : u"Play",
    "pause-menu-label" : u"Пауза",
    "playbackbuttons-menu-label" : u"Показывать кнопки воспроизведения",
    "autoplay-menu-label" : u"Показывать кнопку автовоспроизведения",
    "autoplay-guipushbuttonlabel" : u"Воспроизвести автоматически, когда все будут готовы",
    "autoplay-minimum-label" : u"Минимум пользователей:",

    "ready-guipushbuttonlabel" : u"Я готов к просмотру!",

    "roomuser-heading-label" : u"Комната / Пользователь",
    "size-heading-label" : u"Размер",
    "duration-heading-label" : u"Длительность",
    "filename-heading-label" : u"Имя файла",
    "notifications-heading-label" : u"Уведомления",
    "userlist-heading-label" : u"Кто что смотрит",

    "browseformedia-label" : u"Выбрать видеофайл",

    "file-menu-label" : u"&Файл", # & precedes shortcut key
    "openmedia-menu-label" : u"&Открыть видеофайл",
    "openstreamurl-menu-label" : u"Открыть URL &потокового вещания",
    "setmediadirectories-menu-label" : u"Set media &directories", # TODO: Translate
    "exit-menu-label" : u"&Выход",
    "advanced-menu-label" : u"&Дополнительно",
    "window-menu-label" : u"&Окна",
    "setoffset-menu-label" : u"Установить &смещение",
    "createcontrolledroom-menu-label" : u"&Создать управляемую комнату",
    "identifyascontroller-menu-label" : u"&Войти как оператор комнаты",
    "settrusteddomains-menu-label" : u"Set &trusted domains", # TODO: Translate

    "playback-menu-label" : u"&Воспроизведение",

    "help-menu-label" : u"&Помощь",
    "userguide-menu-label" : u"&Руководство Пользователя",
    "update-menu-label" : u"Проверить &обновления",

    "setoffset-msgbox-label" : u"Установить смещение",
    "offsetinfo-msgbox-label" : u"Смещение (см. инструкцию на странице http://syncplay.pl/guide/):",

    "promptforstreamurl-msgbox-label" : u"Открыть URL потокового вещания",
    "promptforstreamurlinfo-msgbox-label" : u"URL потока",

    "addfolder-label" : u"Add folder", # TODO: Translate

    "adduris-msgbox-label" : u"Add URLs to playlist (one per line)", # TODO: Translate
    "editplaylist-msgbox-label" : u"Set playlist (one per line)", # TODO: Translate
    "trusteddomains-msgbox-label" : u"Domains it is okay to automatically switch to (one per line)", # TODO: Translate

    "createcontrolledroom-msgbox-label" : u"Создать управляемую комнату",
    "controlledroominfo-msgbox-label" : u"Введите имя управляемой комнаты\r\n(см. инструкцию на странице http://syncplay.pl/guide/):",

    "identifyascontroller-msgbox-label" : u"Войти как оператор комнаты",
    "identifyinfo-msgbox-label" : u"Введите пароль оператора комнаты\r\n(см. инструкцию на странице http://syncplay.pl/guide/):",

    "public-server-msgbox-label" : u"Select the public server for this viewing session", # TODO: Translate into Russian

    "megabyte-suffix" : u" МБ", # Technically it is a mebibyte

    # Tooltips

    "host-tooltip" : u"Имя или IP-адрес, к которому будет произведено подключение, может содержать номер порта (напр., syncplay.pl:8999). Синхронизация возможна только в рамках одного сервера/порта.",
    "name-tooltip" : u"Имя, под которым Вы будете известны. Регистриция не требуется, так что имя пользователя можно легко сменить в любой момент. Будет сгенерировано случайным образом, если не указать.",
    "password-tooltip" : u"Пароли нужны для подключения к приватным серверам.",
    "room-tooltip" : u"Комната, в которую Вы попадете сразу после подключения. Можно не указывать. Синхронизация возможна только между людьми в одной и той же комнате.",

    "executable-path-tooltip" : u"Расположение Вашего видеопроигрывателя (MPC-HC, VLC, mplayer2 или mpv).",
    "media-path-tooltip" : u"Расположение видеофайла или потока для просмотра. Обязательно для mpv и mplayer2.",
    "player-arguments-tooltip" : u"Передавать дополнительные аргументы командной строки этому проигрывателю.",
    "mediasearcdirectories-arguments-tooltip" : u"Directories where Syncplay will search for media files, e.g. when you are using the click to switch feature. Syncplay will look recursively through sub-folders.", # TODO: Translate into Russian

    "more-tooltip" : u"Показать дополнительные настройки.",
    "filename-privacy-tooltip" : u"Режим приватности для передачи имени воспроизводимого файла на сервер.",
    "filesize-privacy-tooltip" : u"Режим приватности для передачи размера воспроизводимого файла на сервер.",
    "privacy-sendraw-tooltip" : u"Отправляет эту информацию без шифрования. Рекомендуемая опция с наибольшей функциональностью.",
    "privacy-sendhashed-tooltip" : u"Отправляет хэш-сумму этой информации, делая ее невидимой для других пользователей.",
    "privacy-dontsend-tooltip" : u"Не отправлять эту информацию на сервер. Предоставляет наибольшую приватность.",
    "checkforupdatesautomatically-tooltip" : u"Syncplay будет регулярно заходить на сайт и проверять наличие новых версий.",
    "slowondesync-tooltip" : u"Временно уменьшить скорость воспроизведения в целях синхронизации с другими зрителями. Не поддерживается в MPC-HC.",
    "dontslowdownwithme-tooltip" : u"Ваши лаги не будут влиять на других зрителей.",
    "pauseonleave-tooltip" : u"Приостановить воспроизведение, если Вы покинули комнату или кто-то из зрителей отключился от сервера.",
    "readyatstart-tooltip" : u"Отметить Вас готовым к просмотру сразу же (по умолчанию Вы отмечены не готовым)",
    "forceguiprompt-tooltip" : u"Окно настройки не будет отображаться при открытии файла в Syncplay.", # (Inverted)
    "nostore-tooltip" : u"Запустить Syncplay с данной конфигурацией, но не сохранять изменения навсегда.",
    "rewindondesync-tooltip" : u"Перематывать назад, когда это необходимо для синхронизации. Отключение этой опции может привести к большим рассинхронизациям!",
    "fastforwardondesync-tooltip" : u"Перематывать вперед при рассинхронизации с оператором комнаты (или если включена опция 'Никогда не замедлять и не перематывать видео другим').",
    "showosd-tooltip" : u"Отправлять сообщения Syncplay в видеопроигрыватель и отображать их поверх видео (OSD - On Screen Display).",
    "showosdwarnings-tooltip" : u"Показывать OSC-предупреждения, если проигрываются разные файлы или если Вы в комнате больше никого нет.",
    "showsameroomosd-tooltip" : u"Показывать OSD-уведомления о событиях, относящихся к комнате, в которой Вы находитесь.",
    "shownoncontrollerosd-tooltip" : u"Показывать OSD-уведомления о событиях, относящихся к не-операторам в управляемой комнате.",
    "showdifferentroomosd-tooltip" : u"Показывать OSD-уведомления о событиях, относящихся к любым другим комнатам.",
    "showslowdownosd-tooltip" : u"Показывать уведомления о замедлении или перемотке в целях синхронизации.",
    "showdurationnotification-tooltip" : u"Полезно, когда сегмент составного файла отсутствует. Возможны ложные срабатывания.",
    "language-tooltip" : u"Язык, используемый Syncplay.",
    "unpause-always-tooltip" : u"If you press unpause it always sets you as ready and unpause, rather than just setting you as ready.", # TODO: Translate into Russian
    "unpause-ifalreadyready-tooltip" : u"If you press unpause when not ready it will set you as ready - press unpause again to unpause.", # TODO: Translate into Russian
    "unpause-ifothersready-tooltip" : u"If you press unpause when not ready, it will only upause if others are ready.", # TODO: Translate into Russian
    "unpause-ifminusersready-tooltip" : u"If you press unpause when not ready, it will only upause if others are ready and minimum users threshold is met.", # TODO: Translate into Russian
    "trusteddomains-arguments-tooltip" : u"Domains that it is okay for Syncplay to automatically switch to when shared playlists is enabled.", # TODO: Translate into Russian

    "help-tooltip" : u"Открыть Руководство Пользователя на Syncplay.pl.",
    "reset-tooltip" : u"Сбрасывает все настройки Syncplay в начальное состояние.",
    "update-server-list-tooltip" : u"Connect to syncplay.pl to update list of public servers.", # TODO: Translate to Russian

    "joinroom-tooltip" : u"Покинуть комнату и зайти в другую, указанную комнату.",
    "seektime-msgbox-label" : u"Перемотать к определенному моменту времени (указывать в секундах или мин:сек). Используйте +/-, чтобы перемотать вперед/назад относительно настоящего момента.",
    "ready-tooltip" : u"Показывает, готовы ли Вы к просмотру или нет.",
    "autoplay-tooltip" : u"Автоматическое воспроизведение, когда все пользователи с индикаторами готовности будут готовы и присутствует достаточное число пользователей.",
    "switch-to-file-tooltip" : u"Double click to switch to {}", # Filename # TODO: Translate to Russian

    # In-userlist notes (GUI)
    "differentsize-note" : u"Размер файла не совпадает!",
    "differentsizeandduration-note" : u"Размер и продолжительность файла не совпадают!",
    "differentduration-note" : u"Продолжительность файла не совпадает!",
    "nofile-note" : u"(Ничего не воспроизводим)",

    # Server messages to client
    "new-syncplay-available-motd-message" : u"<NOTICE> Вы используете Syncplay версии {}. Доступна более новая версия на http://syncplay.pl/ . </NOTICE>",  # ClientVersion

    # Server notifications
    "welcome-server-notification" : u"Добро пожаловать на сервер Syncplay версии {0}",  # version
    "client-connected-room-server-notification" : u"{0}({2}) подключился(-лась) к комнате '{1}'",  # username, host, room
    "client-left-server-notification" : u"{0} покинул(а) сервер",  # name
    "no-salt-notification" : u"ВНИМАНИЕ: Чтобы сгенерированные сервером пароли операторов комнат работали после перезагрузки сервера, необходимо указать следующий аргумент командной строки при запуске сервера Syncplay: --salt {}", #Salt

    # Server arguments
    "server-argument-description" : u'Решение для синхронного воспроизведения в VLC, MPlayer или MPC-HC через Интернет. Серверная часть',
    "server-argument-epilog" : u'Если параметр не будет передан, то будет использоваться значение, указанное в _config.',
    "server-port-argument" : u'номер TCP порта сервера',
    "server-password-argument" : u'пароль к серверу',
    "server-isolate-room-argument" : u'должны ли комнаты быть изолированными?',
    "server-salt-argument" : u"генерировать пароли к управляемым комнатам на основании указанной строки (соли)",
    "server-disable-ready-argument" : u"отключить статусы готов/не готов",
    "server-motd-argument" : u"путь к файлу, из которого будет извлекаться MOTD-сообщение",
    "server-messed-up-motd-unescaped-placeholders" : u"MOTD-сообщение содержит неэкранированные спец.символы. Все знаки $ должны быть продублированы ($$).",
    "server-messed-up-motd-too-long" : u"MOTD-сообщение слишком длинное: максимальная длина - {} символ(ов), текущая длина - {} символ(ов).",

    # Server errors
    "unknown-command-server-error" : u"Неизвестная команда: {}",  # message
    "not-json-server-error" : u"Не является закодированной json-строкой: {}",  # message
    "not-known-server-error" : u"Данную команду могут выполнять только авторизованные пользователи.",
    "client-drop-server-error" : u"Клиент отключен с ошибкой: {} -- {}",  # host, error
    "password-required-server-error" : u"Необходимо указать пароль.",
    "wrong-password-server-error" : u"Указан неверный пароль.",
    "hello-server-error" : u"Не хватает аргументов Hello.",

    # Playlists TODO: Translate all this to Russian
    "playlist-selection-changed-notification" :  u"{} changed the playlist selection", # Username
    "playlist-contents-changed-notification" : u"{} updated the playlist", # Username
    "cannot-find-file-for-playlist-switch-error" : u"Could not find file {} in media directories for playlist switch!", # Filename
    "cannot-add-duplicate-error" : u"Could not add second entry for '{}' to the playlist as no duplicates are allowed.", #Filename
    "cannot-add-unsafe-path-error" : u"Could not automatically load {} because it is not on a trusted domain. You can switch to the URL manually by double clicking it in the playlist, and add trusted domains via File->Advanced->Set Trusted Domains.", # Filename # TODO: Translate
    "sharedplaylistenabled-label" : u"Enable shared playlists",
    "removefromplaylist-menu-label" : u"Remove from playlist",
    "shuffleplaylist-menuu-label" : u"Shuffle playlist",
    "undoplaylist-menu-label" : u"Undo last change to playlist",
    "addfilestoplaylist-menu-label" : u"Add file(s) to bottom of playlist",
    "addurlstoplaylist-menu-label" : u"Add URL(s) to bottom of playlist",
    "editplaylist-menu-label": u"Edit playlist",

    "addusersfiletoplaylist-menu-label" : u"Add {} file to playlist", # item owner indicator
    "addusersstreamstoplaylist-menu-label" : u"Add {} stream to playlist", # item owner indicator
    "openusersstream-menu-label" : u"Open {} stream", # [username]'s
    "openusersfile-menu-label" : u"Open {} file", # [username]'s
    "item-is-yours-indicator" : u"your", # Goes with addusersfiletoplaylist/addusersstreamstoplaylist
    "item-is-others-indicator" : u"{}'s", # username - goes with addusersfiletoplaylist/addusersstreamstoplaylist

    "playlist-instruction-item-message" : u"Drag file here to add it to the shared playlist.",
    "sharedplaylistenabled-tooltip" : u"Room operators can add files to a synced playlist to make it easy for everyone to watching the same thing. Configure media directories under 'Misc'.",
}
