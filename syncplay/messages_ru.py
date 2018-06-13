# coding:utf8

"""Russian dictionary"""

ru = {
    "LANGUAGE" : u"Русский", #  (Russian)

    # Client notifications
    "config-cleared-notification" : u"Настройки сброшены. Изменения вступят в силу при сохранении корректной конфигурации.",

    "relative-config-notification" : u"Загружены файлы относительной конфигурации: {}",

    "connection-attempt-notification" : u"Подключение к {}:{}",  # Port, IP
    "reconnection-attempt-notification" : u"Соединение с сервером потеряно, переподключение",
    "disconnection-notification" : u"Отключились от сервера",
    "connection-failed-notification" : u"Не удалось подключиться к серверу",
    "connected-successful-notification" : u"Соединение с сервером установлено",
    "retrying-notification" : u"%s, следующая попытка через %d секунд(ы)...",  # Seconds

    "rewind-notification" : u"Перемотано из-за разницы во времени с {}",  # User
    "fastforward-notification" : u"Ускорено из-за разницы во времени с {}",  # User
    "slowdown-notification" : u"Воспроизведение замедлено из-за разницы во времени с {}",  # User
    "revert-notification" : u"Возвращаемся к нормальной скорости воспроизведения",

    "pause-notification" : u"{} приостановил воспроизведение",  # User
    "unpause-notification" : u"{} возобновил воспроизведение",  # User
    "seek-notification" : u"{} перемотал с {} на {}",  # User, from time, to time

    "current-offset-notification" : u"Текущее смещение: {} секунд(ы)",  # Offset

    "media-directory-list-updated-notification" : u"Папки воспроизведения обновлены.",

    "room-join-notification" : u"{} зашел в комнату: '{}'",  # User
    "left-notification" : u"{} покинул комнату",  # User
    "left-paused-notification" : u"{} покинул комнату, {} приостановил воспроизведение",  # User who left, User who paused
    "playing-notification" : u"{} включил '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum" : u" в комнате: '{}'",  # Room

    "not-all-ready" : u"Не готовы: {}", # Usernames
    "all-users-ready" : u"Все зрители готовы ({} чел.)", #Number of ready users
    "ready-to-unpause-notification" : u"Вы помечены как готовый - нажмите еще раз, чтобы продолжить воспроизведение",
    "set-as-ready-notification" : u"Вы помечены как готовый",
    "set-as-not-ready-notification" : u"Вы помечены как неготовый",
    "autoplaying-notification" : u"Автовоспроизведение через {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification" : u"Идентификация как оператора комнаты с паролем '{}'...",
    "failed-to-identify-as-controller-notification" : u"{} не прошел идентификацию в качестве оператора комнаты.",
    "authenticated-as-controller-notification" : u"{} вошел как оператор комнаты.",
    "created-controlled-room-notification" : u"Создана управляемая комната '{}' с паролем '{}'. Сохраните эти данные!", # RoomName, operatorPassword

    "file-different-notification" : u"Вероятно, файл, который Вы смотрите, отличается от того, который смотрит {}.",  # User
    "file-differences-notification" : u"Ваш файл отличается: {}", # Differences
    "room-file-differences" : u"Несовпадения файла: {}", # File differences (filename, size, and/or duration)
    "file-difference-filename" : u"имя",
    "file-difference-filesize" : u"размер",
    "file-difference-duration" : u"длительность",
    "alone-in-the-room" : u"В комнате кроме Вас никого нет.",

    "different-filesize-notification" : u" (размер Вашего файла не совпадает с размером их файла!)",
    "userlist-playing-notification" : u"{} смотрит:", #Username
    "file-played-by-notification" : u"Файл: {} просматривают:",  # File
    "no-file-played-notification" : u"{} не смотрит ничего", # Username
    "notplaying-notification" : u"Люди, которые не смотрят ничего:",
    "userlist-room-notification" : u"В комнате '{}':",  # Room
    "userlist-file-notification" : u"Файл",
    "controller-userlist-userflag" : u"Оператор",
    "ready-userlist-userflag" : u"Готов",

    "update-check-failed-notification" : u"Невозможно автоматически проверить, что версия Syncplay {} все еще актуальна. Хотите зайти на https://syncplay.pl/ и вручную проверить наличие обновлений?",
    "syncplay-uptodate-notification" : u"У вас последняя версия Syncplay",
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
    "commandlist-notification/toggle" : u"\tt - переключить статус готов/не готов к просмотру",
    "commandlist-notification/create" : u"\tc [name] - создать управляемую комнату с таким же именем, как у текущей",
    "commandlist-notification/auth" : u"\ta [password] - авторизоваться как оператор комнаты с помощью пароля",
    "commandlist-notification/chat" : "\tch [message] - send a chat message in a room", # TODO: Translate
    "syncplay-version-notification" : u"Версия Syncplay: {}",  # syncplay.version
    "more-info-notification" : u"Больше информации на {}",  # projectURL

    "gui-data-cleared-notification" : u"Syncplay очистил путь и информацию о состоянии окна, использованного GUI.",
    "language-changed-msgbox-label" : u"Язык переключится при следующем запуске Syncplay.",
    "promptforupdate-label" : u"Вы не против, если Syncplay будет автоматически изредка проверять наличие обновлений?",

    "vlc-version-mismatch": u"Syncplay не поддерживает данную версию VLC. Syncplay поддерживает VLC {}+, но не VLC 3. Используйте другой проигрыватель.", # VLC min version
    "vlc-interface-version-mismatch" : u"Вы используете модуль интерфейса Syncplay устаревшей версии {} для VLC. К сожалению, Syncplay способен работать с версией {} и выше. Пожалуйста, обратитесь к Руководству Пользователя Syncplay (https://syncplay.pl/guide/) за инструкциями о том, как установить syncplay.lua.",  # VLC interface version, VLC interface min version
    "vlc-interface-oldversion-warning" : u"Внимание: Syncplay обнаружил, что старая версия модуля интерфейса Syncplay для VLC уже установлена в директорию VLC. Пожалуйста, обратитесь к Руководству Пользователя Syncplay (https://syncplay.pl/guide/) за инструкциями о том, как установить syncplay.lua.",
    "vlc-interface-not-installed" : u"Внимание: Модуль интерфейса Syncplay для VLC не обнаружен в директории VLC. По существу, если Вы используете VLC 2.0, то VLC будет использовать модуль syncplay.lua из директории Syncplay, но в таком случае другие пользовательские скрипты и расширения интерфейса не будут работать. Пожалуйста, обратитесь к Руководству Пользователя Syncplay (https://syncplay.pl/guide/) за инструкциями о том, как установить syncplay.lua.",
    "media-player-latency-warning": u"Внимание: У Вашего проигрывателя слишком большой отклик ({} секунд). Если Вы замечаете проблемы с синхронизацией, то закройте ресурсоемкие приложения. Если это не помогло - попробуйте другой проигрыватель.", # Seconds to respond
    "mpv-unresponsive-error": u"mpv не отвечает {} секунд, по-видимому, произошел сбой. Пожалуйста, перезапустите Syncplay.", # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt" : u"Для выхода нажмите Enter\n",

    # Client errors
    "missing-arguments-error" : u"Некоторые необходимые аргументы отсутствуют, обратитесь к --help",
    "server-timeout-error" : u"Подключение к серверу превысило лимит времени",
    "mpc-slave-error" : u"Невозможно запустить MPC в slave режиме!",
    "mpc-version-insufficient-error" : u"Версия MPC слишком старая, пожалуйста, используйте `mpc-hc` >= `{}`",
    "mpc-be-version-insufficient-error" : u"Версия MPC слишком старая, пожалуйста, используйте `mpc-be` >= `{}`",
    "mpv-version-error" : u"Syncplay не совместим с данной версией mpv. Пожалуйста, используйте другую версию mpv (лучше свежайшую).",
    "player-file-open-error" : u"Проигрыватель не может открыть файл.",
    "player-path-error" : u"Путь к проигрывателю задан неверно. Supported players are: mpv, VLC, MPC-HC, MPC-BE and mplayer2.", # TODO: Translate last sentence
    "hostname-empty-error" : u"Имя пользователя не может быть пустым.",
    "empty-error" : u"{} не может быть пустым.",  # Configuration
    "media-player-error" : u"Ошибка проигрывателя: \"{}\"",  # Error line
    "unable-import-gui-error" : u"Невозможно импортировать библиотеки GUI (графического интерфейса). Необходимо установить PySide, иначе графический интерфейс не будет работать.",

    "arguments-missing-error" : u"Некоторые необходимые аргументы отсутствуют, обратитесь к --help",

    "unable-to-start-client-error" : u"Невозможно запустить клиент",

    "player-path-config-error": u"Путь к проигрывателю установлен неверно. Supported players are: mpv, VLC, MPC-HC, MPC-BE and mplayer2", # To do: Translate end
    "no-file-path-config-error" : u"Файл должен быть указан до включения проигрывателя",
    "no-hostname-config-error": u"Имя сервера не может быть пустым",
    "invalid-port-config-error" : u"Неверный номер порта",
    "empty-value-config-error" : u"Поле '{}' не может быть пустым", # Config option

    "not-json-error" : u"Не является закодированной json-строкой\n",
    "hello-arguments-error" : u"Не хватает аргументов Hello\n",
    "version-mismatch-error" : u"Конфликт версий между клиентом и сервером\n",
    "vlc-failed-connection" : u"Ошибка подключения к VLC. Если у Вас не установлен syncplay.lua, то обратитесь к https://syncplay.pl/LUA/ за инструкциями.",
    "vlc-failed-noscript" : u"VLC сообщает, что скрипт интерфейса syncplay.lua не установлен. Пожалуйста, обратитесь к https://syncplay.pl/LUA/ за инструкциями.",
    "vlc-failed-versioncheck" : u"Данная версия VLC не поддерживается Syncplay. Пожалуйста, используйте VLC версии 2 или выше.",
    "vlc-failed-other" : u"Во время загрузки скрипта интерфейса syncplay.lua в VLC произошла следующая ошибка: {}",  # Syncplay Error

    "feature-sharedPlaylists": u"shared playlists",  # used for not-supported-by-server-error # TODO: Translate
    "feature-chat": u"chat",  # used for not-supported-by-server-error # TODO: Translate
    "feature-readiness": u"readiness",  # used for not-supported-by-server-error # TODO: Translate
    "feature-managedRooms": u"managed rooms",  # used for not-supported-by-server-error # TODO: Translate

    "not-supported-by-server-error": u"The {} feature is not supported by this server..",  # feature # TODO: Translate
    #OLD TRANSLATION: "not-supported-by-server-error" : u"Эта возможность не поддерживается сервером. Требуется сервер Syncplay {}+, вы подключены к серверу Syncplay {}.", #minVersion, serverVersion
    "shared-playlists-not-supported-by-server-error" : u"Общие списки воспроизведения могут не поддерживаться сервером. Для корректной работы требуется сервер Syncplay {}+, вы подключены к серверу Syncplay {}.", #minVersion, serverVersion
    "shared-playlists-disabled-by-server-error" : "The shared playlist feature has been disabled in the server configuration. To use this feature you will need to connect to a different server.", # TODO: Translate

    "invalid-seek-value" : u"Некорректное значение для перемотки",
    "invalid-offset-value" : u"Некорректное смещение",

    "switch-file-not-found-error" : u"Невозможно найти файл '{0}'. Проверьте папки воспроизведения.", # File not found
    "folder-search-timeout-error" : u"Поиск файла был прерван в папке '{}'. Это может происходить из-за большого количества подпапок. Для корректной работы поиска файлов зайдите через выпадающее меню в Файл->Папки воспроизведения и удалите данную папку из списка, или замените её на нужную подпапку. If the folder is actually fine then you can re-enable it by selecting File->Set Media Directories and pressing 'OK'.", #Folder # TODO: Translate last sentence
    "folder-search-first-file-timeout-error" : u"Поиск файла в '{}' был прерван, так как невозможно открыть каталог. Это может происходить, если это сетевой диск или диск перешел в режим экономии энергии. Для корректной работы поиска файлов зайдите через выпадающее меню в Файл->Папки воспроизведения и удалите данную папку, или решите проблему через изменение параметров энергосбережения.", #Folder
    "added-file-not-in-media-directory-error" : u"Вы загрузили файл из '{}', который не числится в папках воспроизведения. Вы можете добавить его через выпадающее меню Файл->Папки воспроизведения.", #Folder
    "no-media-directories-error" : u"Вы не указали папки воспроизведения. Для корректной работы зайдите через выпадающее меню в Файл->Папки воспроизведения и укажите нужные каталоги.",
    "cannot-find-directory-error" : u"Не удалось найти папку воспроизведения '{}'. Для обновления списка папок, через выпадающее меню, перейдите в Файл->Папки воспроизведения и укажите нужные каталоги.",

    "failed-to-load-server-list-error" : u"Не удалось загрузить список публичных серверов. Откройте https://www.syncplay.pl/ через браузер.",

    # Client arguments
    "argument-description" : u'Решение для синхронного воспроизведения в VLC, MPlayer или MPC-HC/BE через Интернет.',
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

    "connection-group-title" : u"Подключение",
    "host-label" : u"Адрес сервера: ",
    "name-label" : u"Имя пользователя (не обязательно):",
    "password-label" : u"Пароль сервера (если требуется):",
    "room-label" : u"Комната:",

    "media-setting-title" : u"Воспроизведение",
    "executable-path-label" : u"Путь к проигрывателю:",
    "media-path-label" : u"Путь к видеофайлу:", # Todo: Translate to 'Path to video (optional)'
    "player-arguments-label" : u"Аргументы запуска проигрывателя:",
    "browse-label" : u"Выбрать",
    "update-server-list-label" : u"Обновить список",

    "more-title" : u"Больше настроек",
    "never-rewind-value" : u"Никогда",
    "seconds-suffix" : u" секунд(ы)",
    "privacy-sendraw-option" : u"отпр. как есть",
    "privacy-sendhashed-option" : u"отпр. хэш",
    "privacy-dontsend-option" : u"не отпр.",
    "filename-privacy-label" : u"Имя файла:",
    "filesize-privacy-label" : u"Размер файла:",
    "checkforupdatesautomatically-label" : u"Проверять обновления автоматически",
    "slowondesync-label" : u"Замедлять при небольших рассинхронизациях (не поддерживаетя в MPC-HC/BE)",
    "rewindondesync-label" : u"Перемотка при больших рассинхронизациях (настоятельно рекомендуется)",
    "dontslowdownwithme-label" : u"Никогда не замедлять и не перематывать видео другим (функция тестируется)",
    "pausing-title" : u"Приостановка",
    "pauseonleave-label" : u"Приостанавливать, когда кто-то уходит (например, отключился)",
    "readiness-title" : u"Готовность",
    "readyatstart-label" : u"Выставить статус 'Я готов' по умолчанию",
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
    "readiness-label" : u"Поведение",
    "misc-label" : u"Прочее",
    "core-behaviour-title" : u"Информация о файлах",
    "syncplay-internals-title" : u"Системные настройки",
    "syncplay-mediasearchdirectories-title" : u"Папки воспроизведения", #needs to be checked
    "syncplay-mediasearchdirectories-label" : u"Папки воспроизведения (один путь на строку)",
    "sync-label" : u"Синхронизация",
    "sync-otherslagging-title" : u"Опережение",
    "sync-youlaggging-title" : u"Отставание",
    "messages-label" : u"Сообщения",
    "messages-osd-title" : u"Настройки OSD",
    "messages-other-title" : u"Другие настройки отображения",
    "chat-label" : u"Chat", # TODO: Translate
    "privacy-label" : u"Приватность",
    "privacy-title" : u"Настройки приватности",
    "unpause-title" : u"Если вы стартуете, то:",
    "unpause-ifalreadyready-option" : u"Снять паузу, если уже готов",
    "unpause-ifothersready-option" : u"Снять паузу, если Вы и остальные в комнате готовы (по-умолчанию)",
    "unpause-ifminusersready-option" : u"Снять паузу, если все в комнате готовы и присутствует минимум зрителей",
    "unpause-always" : u"Всегда снимать паузу",
    "syncplay-trusteddomains-title": u"Доверенные сайты (стрим-сервисы, видеохостинги, файлы в сети)",
"addtrusteddomain-menu-label" : u"Добавить {} как доверенный сайт", # Domain

    "chat-title": u"Chat message input",  # TODO: Translate
    "chatinputenabled-label": u"Enable chat input via mpv (using enter key)",  # TODO: Translate
    "chatdirectinput-label" : u"Allow instant chat input (bypass having to press enter key to chat)", # TODO: Translate
    "chatinputfont-label": u"Chat input font",  # TODO: Translate
    "chatfont-label": u"Set font",  # TODO: Translate
    "chatcolour-label": u"Set colour",  # TODO: Translate
    "chatinputposition-label": u"Position of message input area in mpv",  # TODO: Translate
    "chat-top-option": u"Top",  # TODO: Translate
    "chat-middle-option": u"Middle",  # TODO: Translate
    "chat-bottom-option": u"Bottom",  # TODO: Translate
    "chatoutputheader-label" : u"Chat message output", # TODO: Traslate
    "chatoutputfont-label": u"Chat output font", # TODO: Translate
    "chatoutputenabled-label": u"Enable chat output in media player (mpv only for now)", # TODO: Translate
    "chatoutputposition-label": u"Output mode", # TODO: Translate
    "chat-chatroom-option": u"Chatroom style", # TODO: Translate
    "chat-scrolling-option": u"Scrolling style", # TODO: Translate

    "mpv-key-tab-hint": u"[TAB] to toggle access to alphabet row key shortcuts.", # TODO: Translate
    "mpv-key-hint": u"[ENTER] to send message. [ESC] to escape chat mode.", # TODO: Translate
    "alphakey-mode-warning-first-line": u"You can temporarily use old mpv bindings with a-z keys.", # TODO: Translate
    "alphakey-mode-warning-second-line": u"Press [TAB] to return to Syncplay chat mode.", # TODO: Translate

    "help-label" : u"Помощь",
    "reset-label" : u"Сброс настроек",
    "run-label" : u"Запустить",
    "storeandrun-label" : u"Сохранить и запустить",

    "contact-label" : u"Есть идея, нашли ошибку или хотите оставить отзыв? Пишите на <a href=\"mailto:dev@syncplay.pl\">dev@syncplay.pl</a>, в <a href=\"https://webchat.freenode.net/?channels=#syncplay\">IRC канал #Syncplay</a> на irc.freenode.net или <a href=\"https://github.com/Uriziel/syncplay/issues\">задавайте вопросы через GitHub</a>. Кроме того, заходите на <a href=\"https://syncplay.pl/\">www.syncplay.pl</a> за инорфмацией, помощью и обновлениями! NOTE: Chat messages are not encrypted so do not use Syncplay to send sensitive information.", # TODO: Translate last sentence

    "joinroom-label" : u"Зайти в комнату",
    "joinroom-menu-label" : u"Зайти в комнату {}",
    "seektime-menu-label" : u"Пере&мотать",
    "undoseek-menu-label" : u"&Отменить перемотку",
    "play-menu-label" : u"&Старт",
    "pause-menu-label" : u"&Пауза",
    "playbackbuttons-menu-label" : u"&Показывать кнопки управления",
    "autoplay-menu-label" : u"Показывать кнопку &автовоспроизведения",
    "autoplay-guipushbuttonlabel" : u"Стартовать, когда все будут готовы",
    "autoplay-minimum-label" : u"Минимум зрителей:",
    "sendmessage-label" : u"Send", # TODO: Translate

    "ready-guipushbuttonlabel" : u"Я готов",

    "roomuser-heading-label" : u"Комната / Зритель",

    "size-heading-label" : u"Размер",
    "duration-heading-label" : u"Время",
    "filename-heading-label" : u"Имя файла",
    "notifications-heading-label" : u"Уведомления",
    "userlist-heading-label" : u"Кто что смотрит",

    "browseformedia-label" : u"Выбрать файл",

    "file-menu-label" : u"&Файл", # & precedes shortcut key
    "openmedia-menu-label" : u"&Открыть файл",
    "openstreamurl-menu-label" : u"Открыть &ссылку",
    "setmediadirectories-menu-label" : u"&Папки воспроизведения",
    "exit-menu-label" : u"&Выход",
    "advanced-menu-label" : u"&Дополнительно",
    "window-menu-label" : u"&Вид",
    "setoffset-menu-label" : u"&Установить смещение",
    "createcontrolledroom-menu-label" : u"Создать управляемую &комнату",
    "identifyascontroller-menu-label" : u"&Войти как оператор комнаты",
    "settrusteddomains-menu-label" : u"Доверенные &сайты",

    "playback-menu-label" : u"&Управление",

    "help-menu-label" : u"&Помощь",
    "userguide-menu-label" : u"&Руководство пользователя",
    "update-menu-label" : u"Проверить &обновления",

    #About dialog - TODO: Translate
    "about-menu-label": u"&About Syncplay",
    "about-dialog-title": u"About Syncplay",
    "about-dialog-release": u"Version {} release {} on {}",
    "about-dialog-license-text" : u"Licensed under the Apache&nbsp;License,&nbsp;Version 2.0",
    "about-dialog-license-button": u"License",
    "about-dialog-dependencies": u"Dependencies",

    "setoffset-msgbox-label" : u"Установить смещение",
    "offsetinfo-msgbox-label" : u"Смещение (см. инструкцию на странице www.syncplay.pl/guide):",

    "promptforstreamurl-msgbox-label" : u"Открыть ссылку",
    "promptforstreamurlinfo-msgbox-label" : u"Ссылка:",

    "addfolder-label" : u"Добавить папку",

    "adduris-msgbox-label" : u"Список ссылок (одна на строку)",
    "editplaylist-msgbox-label" : u"Список воспроизведения (один на строку)",
    "trusteddomains-msgbox-label" : u"Список доверенных сайтов для автоматического воспроизведения (один на строку)",

    "createcontrolledroom-msgbox-label" : u"Создать управляемую комнату",
    "controlledroominfo-msgbox-label" : u"Введите имя управляемой комнаты\r\n(см. инструкцию на странице www.syncplay.pl/guide):",

    "identifyascontroller-msgbox-label" : u"Войти как оператор комнаты",
    "identifyinfo-msgbox-label" : u"Введите пароль оператора комнаты\r\n(см. инструкцию на странице www.syncplay.pl/guide):",

    "public-server-msgbox-label" : u"Выбите публичный сервер для данной сессии",

    "megabyte-suffix" : u" МБ", # Technically it is a mebibyte

    # Tooltips

    "host-tooltip" : u"Имя или IP-адрес, к которому будет произведено подключение, может содержать номер порта (напр., syncplay.pl:8999). Синхронизация возможна только в рамках одного сервера/порта.",
    "name-tooltip" : u"Имя, под которым Вы будете известны. Регистриция не требуется, так что имя пользователя можно легко сменить в любой момент. Будет сгенерировано случайным образом, если не указать.",
    "password-tooltip" : u"Пароли нужны для подключения к приватным серверам.",
    "room-tooltip" : u"Комната, в которую Вы попадете сразу после подключения. Синхронизация возможна только между людьми в одной и той же комнате.",

    "executable-path-tooltip" : u"Расположение Вашего видеопроигрывателя (MPC-HC, MPC-BE, VLC, mplayer2 или mpv).",
    "media-path-tooltip" : u"Расположение видеофайла или потока для просмотра. Обязательно для mplayer2.", # TODO: Confirm translation
    "player-arguments-tooltip" : u"Передавать дополнительные аргументы командной строки этому проигрывателю.",
    "mediasearcdirectories-arguments-tooltip" : u"Папки, где Syncplay будет искать медиа файлы, включая подпапки.",

    "more-tooltip" : u"Показать дополнительные настройки.",
    "filename-privacy-tooltip" : u"Режим приватности для передачи имени воспроизводимого файла на сервер.",
    "filesize-privacy-tooltip" : u"Режим приватности для передачи размера воспроизводимого файла на сервер.",
    "privacy-sendraw-tooltip" : u"Отправляет эту информацию без шифрования. Рекомендуемая опция с наибольшей функциональностью.",
    "privacy-sendhashed-tooltip" : u"Отправляет хэш-сумму этой информации, делая ее невидимой для других пользователей.",
    "privacy-dontsend-tooltip" : u"Не отправлять эту информацию на сервер. Предоставляет наибольшую приватность.",
    "checkforupdatesautomatically-tooltip" : u"Syncplay будет регулярно заходить на сайт и проверять наличие новых версий.",
    "slowondesync-tooltip" : u"Временно уменьшить скорость воспроизведения в целях синхронизации с другими зрителями. Не поддерживается в MPC-HC/BE.",
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
    "unpause-always-tooltip" : u"Когда вы стартуете, статус изменится на готов и начнется воспроизведение, а не просто смена статуса.",
    "unpause-ifalreadyready-tooltip" : u"Когда вы стартуете не готовым, это меняет статус на готов - нажмите старт еще раз для начала воспроизведения.",
    "unpause-ifothersready-tooltip" : u"Когда вы стартуете не готовым, воспроизведение начнется, если остальные готовы.",
    "unpause-ifminusersready-tooltip" : u"Когда вы стартуете не готовым, воспроизведение начнется, если остальные готовы и присутствует достаточное число зрителей.",
    "trusteddomains-arguments-tooltip" : u"Сайты, которые разрешены для автоматического воспроизведения из общего списка воспроизведения.",

    "chatinputenabled-tooltip": u"Enable chat input in mpv (press enter to chat, enter to send, escape to cancel)",# TODO: Translate
    "chatdirectinput-tooltip" : u"Skip having to press 'enter' to go into chat input mode in mpv. Press TAB in mpv to temporarily disable this feature.", # TODO: Translate
    "font-label-tooltip": u"Font used for when entering chat messages in mpv. Client-side only, so doesn't affect what other see.",# TODO: Translate
    "set-input-font-tooltip": u"Font family used for when entering chat messages in mpv. Client-side only, so doesn't affect what other see.",# TODO: Translate
    "set-input-colour-tooltip": u"Font colour used for when entering chat messages in mpv. Client-side only, so doesn't affect what other see.",# TODO: Translate
    "chatinputposition-tooltip": u"Location in mpv where chat input text will appear when you press enter and type.",# TODO: Translate
    "chatinputposition-top-tooltip": u"Place chat input at top of mpv window.",  # TODO: Translate
    "chatinputposition-middle-tooltip": u"Place chat input in dead centre of mpv window.",  # TODO: Translate
    "chatinputposition-bottom-tooltip": u"Place chat input at bottom of mpv window.",  # TODO: Translate
    "chatoutputenabled-tooltip": u"Show chat messages in OSD (if supported by media player).",  # TODO: Translate
    "font-output-label-tooltip": u"Chat output font.",  # TODO: Translate
    "set-output-font-tooltip": u"Font used for when displaying chat messages.",  # TODO: Translate
    "chatoutputmode-tooltip": u"How chat messages are displayed.",  # TODO: Translate
    "chatoutputmode-chatroom-tooltip": u"Display new lines of chat directly below previous line.",  # TODO: Translate
    "chatoutputmode-scrolling-tooltip": u"Scroll chat text from right to left.",  # TODO: Translate

    "help-tooltip" : u"Открыть Руководство Пользователя на Syncplay.pl.",
    "reset-tooltip" : u"Сбрасывает все настройки Syncplay в начальное состояние.",
    "update-server-list-tooltip" : u"Обновить список публичных серверов от syncplay.pl.",

    "joinroom-tooltip" : u"Покинуть комнату и зайти в другую, указанную комнату.",
    "seektime-msgbox-label" : u"Перемотать к определенному моменту времени (указывать в секундах или мин:сек). Используйте +/-, чтобы перемотать вперед/назад относительно настоящего момента.",
    "ready-tooltip" : u"Показывает, готовы ли Вы к просмотру или нет.",
    "autoplay-tooltip" : u"Автоматическое воспроизведение, когда все пользователи с индикаторами готовности будут готовы и присутствует достаточное число зрителей.",
    "switch-to-file-tooltip" : u"Кликните два раза для воспроизведения {}", # Filename
    "sendmessage-tooltip" : u"Send message to room", # TODO: Translate

    # In-userlist notes (GUI)
    "differentsize-note" : u"Размер файла не совпадает!",
    "differentsizeandduration-note" : u"Размер и продолжительность файла не совпадают!",
    "differentduration-note" : u"Продолжительность файла не совпадает!",
    "nofile-note" : u"(ничего)",

    # Server messages to client
    "new-syncplay-available-motd-message" : u"<NOTICE> Вы используете Syncplay версии {}. Доступна более новая версия на https://syncplay.pl/ . </NOTICE>",  # ClientVersion

    # Server notifications
    "welcome-server-notification" : u"Добро пожаловать на сервер Syncplay версии {0}",  # version
    "client-connected-room-server-notification" : u"{0}({2}) подключился к комнате '{1}'",  # username, host, room
    "client-left-server-notification" : u"{0} покинул сервер",  # name
    "no-salt-notification" : u"ВНИМАНИЕ: Чтобы сгенерированные сервером пароли операторов комнат работали после перезагрузки сервера, необходимо указать следующий аргумент командной строки при запуске сервера Syncplay: --salt {}", #Salt

    # Server arguments
    "server-argument-description" : u'Решение для синхронного воспроизведения в VLC, MPlayer или MPC-HC/BE через Интернет. Серверная часть',
    "server-argument-epilog" : u'Если параметр не будет передан, то будет использоваться значение, указанное в _config.',
    "server-port-argument" : u'номер TCP порта сервера',
    "server-password-argument" : u'пароль к серверу',
    "server-isolate-room-argument" : u'должны ли комнаты быть изолированными?',
    "server-salt-argument" : u"генерировать пароли к управляемым комнатам на основании указанной строки (соли)",
    "server-disable-ready-argument" : u"отключить статусы готов/не готов",
    "server-motd-argument" : u"путь к файлу, из которого будет извлекаться MOTD-сообщение",
    "server-chat-argument" : "Should chat be disabled?", # TODO: Translate
    "server-chat-maxchars-argument": u"Maximum number of characters in a chat message (default is {})",  # TODO: Translate
    "server-maxusernamelength-argument": u"Maximum number of charactrs in a username (default is {})", # TODO: Translate
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

    "playlist-selection-changed-notification" :  u"{} изменил выбор в списке воспроизведения", # Username
    "playlist-contents-changed-notification" : u"{} обновил список воспроизведения", # Username
    "cannot-find-file-for-playlist-switch-error" : u"Не удалось найти файл {} в папках воспроизведения!", # Filename
    "cannot-add-duplicate-error" : u"'{}' уже есть в списке воспроизведения.", #Filename
    "cannot-add-unsafe-path-error" : u"Не удалось автоматически переключиться на {}, потому что ссылка не соответствует доверенным сайтам. Её можно включить вручную, дважны кливнув по ссылке в списке воспроизведения. Добавить доверенный сайт можно в выпадающем меню 'Дополнительно' или просто кликнув по ссылке правой кнопкой мыши.", # Filename
    "sharedplaylistenabled-label" : u"Включить общий список воспроизведения",
    "removefromplaylist-menu-label" : u"Удалить",
    "shufflepremaininglaylist-menuu-label" : u"Shuffle remaining playlist", # Was: Перемешать список # TODO: Translate
    "shuffleentireplaylist-menu-label" : u"Shuffle entire playlist", # TODO: Translate
    "undoplaylist-menu-label" : u"Отменить последнее действие",
    "addfilestoplaylist-menu-label" : u"Добавить файлы в очередь",
    "addurlstoplaylist-menu-label" : u"Добавить ссылку в очередь",
    "editplaylist-menu-label": u"Редактировать список",

    "open-containing-folder": u"Open folder containing this file", # TODO: Traslate
    "addusersfiletoplaylist-menu-label" : u"Добавить файл {} в список воспроизведения", # item owner indicator
    "addusersstreamstoplaylist-menu-label" : u"Добавить поток {} в список воспроизведения", # item owner indicator
    "openusersstream-menu-label" : u"Открыть поток от {}", # [username]'s
    "openusersfile-menu-label" : u"Открыть файл от {}", # [username]'s
    "item-is-yours-indicator" : u"от вас", # Goes with addusersfiletoplaylist/addusersstreamstoplaylist
    "item-is-others-indicator" : u"{}", # username - goes with addusersfiletoplaylist/addusersstreamstoplaylist

    "playlist-instruction-item-message" : u"Перетащите сюда файлы, чтобы добавить их в общий список.",
    "sharedplaylistenabled-tooltip" : u"Оператор комнаты может добавлять файлы в список общего воспроизведения для удобного совместного просмотра. Папки воспроизведения настраиваются во вкладке 'Файл'.",
}
