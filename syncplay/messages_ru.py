# coding:utf8

"""Russian dictionary"""

ru = {
    "LANGUAGE": "Русский",  # (Russian)

    # Client notifications
    "config-cleared-notification": "Настройки сброшены. Изменения вступят в силу при сохранении корректной конфигурации.",

    "relative-config-notification": "Загружены файлы относительной конфигурации: {}",

    "connection-attempt-notification": "Подключение к {}:{}",  # Port, IP
    "reconnection-attempt-notification": "Соединение с сервером потеряно, переподключение",
    "disconnection-notification": "Отключились от сервера",
    "connection-failed-notification": "Не удалось подключиться к серверу",
    "connected-successful-notification": "Соединение с сервером установлено",
    "retrying-notification": "%s, следующая попытка через %d секунд(ы)...",  # Seconds

    "rewind-notification": "Перемотано из-за разницы во времени с {}",  # User
    "fastforward-notification": "Ускорено из-за разницы во времени с {}",  # User
    "slowdown-notification": "Воспроизведение замедлено из-за разницы во времени с {}",  # User
    "revert-notification": "Возвращаемся к нормальной скорости воспроизведения",

    "pause-notification": "{} приостановил воспроизведение",  # User
    "unpause-notification": "{} возобновил воспроизведение",  # User
    "seek-notification": "{} перемотал с {} на {}",  # User, from time, to time

    "current-offset-notification": "Текущее смещение: {} секунд(ы)",  # Offset

    "media-directory-list-updated-notification": "Папки воспроизведения обновлены.",

    "room-join-notification": "{} зашел в комнату: '{}'",  # User
    "left-notification": "{} покинул комнату",  # User
    "left-paused-notification": "{} покинул комнату, {} приостановил воспроизведение",  # User who left, User who paused
    "playing-notification": "{} включил '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum": " в комнате: '{}'",  # Room

    "not-all-ready": "Не готовы: {}",  # Usernames
    "all-users-ready": "Все зрители готовы ({} чел.)",  # Number of ready users
    "ready-to-unpause-notification": "Вы помечены как готовый - нажмите еще раз, чтобы продолжить воспроизведение",
    "set-as-ready-notification": "Вы помечены как готовый",
    "set-as-not-ready-notification": "Вы помечены как неготовый",
    "autoplaying-notification": "Автовоспроизведение через {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Идентификация как оператора комнаты с паролем '{}'...",
    "failed-to-identify-as-controller-notification": "{} не прошел идентификацию в качестве оператора комнаты.",
    "authenticated-as-controller-notification": "{} вошел как оператор комнаты.",
    "created-controlled-room-notification": "Создана управляемая комната '{}' с паролем '{}'. Сохраните эти данные!",  # RoomName, operatorPassword

    "file-different-notification": "Вероятно, файл, который Вы смотрите, отличается от того, который смотрит {}.",  # User
    "file-differences-notification": "Ваш файл отличается: {}",  # Differences
    "room-file-differences": "Несовпадения файла: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "имя",
    "file-difference-filesize": "размер",
    "file-difference-duration": "длительность",
    "alone-in-the-room": "В комнате кроме Вас никого нет.",

    "different-filesize-notification": " (размер Вашего файла не совпадает с размером их файла!)",
    "userlist-playing-notification": "{} смотрит:",  # Username
    "file-played-by-notification": "Файл: {} просматривают:",  # File
    "no-file-played-notification": "{} не смотрит ничего",  # Username
    "notplaying-notification": "Люди, которые не смотрят ничего:",
    "userlist-room-notification": "В комнате '{}':",  # Room
    "userlist-file-notification": "Файл",
    "controller-userlist-userflag": "Оператор",
    "ready-userlist-userflag": "Готов",

    "update-check-failed-notification": "Невозможно автоматически проверить, что версия Syncplay {} все еще актуальна. Хотите зайти на https://syncplay.pl/ и вручную проверить наличие обновлений?",
    "syncplay-uptodate-notification": "У вас последняя версия Syncplay",
    "syncplay-updateavailable-notification": "Доступна новая версия Syncplay. Хотите открыть страницу релиза?",

    "mplayer-file-required-notification": "Для использования Syncplay с mplayer необходимо передать файл в качестве параметра",
    "mplayer-file-required-notification/example": "Пример использования: syncplay [options] [url|path/]filename",
    "mplayer2-required": "Syncplay не совместим с MPlayer 1.x, пожалуйста, используйте mplayer2 или mpv",

    "unrecognized-command-notification": "Неизвестная команда.",
    "commandlist-notification": "Доступные команды:",
    "commandlist-notification/room": "\tr [name] - сменить комнату",
    "commandlist-notification/list": "\tl - показать список пользователей",
    "commandlist-notification/undo": "\tu - отменить последнюю перемотку",
    "commandlist-notification/pause": "\tp - вкл./выкл. паузу",
    "commandlist-notification/seek": "\t[s][+-]time - перемотать к заданному моменту времени, если не указан + или -, то время считается абсолютным (от начала файла) в секундах или мин:сек",
    "commandlist-notification/help": "\th - помощь",
    "commandlist-notification/toggle": "\tt - переключить статус готов/не готов к просмотру",
    "commandlist-notification/create": "\tc [name] - создать управляемую комнату с таким же именем, как у текущей",
    "commandlist-notification/auth": "\ta [password] - авторизоваться как оператор комнаты с помощью пароля",
    "commandlist-notification/chat": "\tch [message] - send a chat message in a room",  # TODO: Translate
    "syncplay-version-notification": "Версия Syncplay: {}",  # syncplay.version
    "more-info-notification": "Больше информации на {}",  # projectURL

    "gui-data-cleared-notification": "Syncplay очистил путь и информацию о состоянии окна, использованного GUI.",
    "language-changed-msgbox-label": "Язык переключится при следующем запуске Syncplay.",
    "promptforupdate-label": "Вы не против, если Syncplay будет автоматически изредка проверять наличие обновлений?",

    "vlc-version-mismatch": "Syncplay не поддерживает данную версию VLC. Syncplay поддерживает VLC {}+, но не VLC 3. Используйте другой проигрыватель.",  # VLC min version
    "vlc-interface-version-mismatch": "Вы используете модуль интерфейса Syncplay устаревшей версии {} для VLC. К сожалению, Syncplay способен работать с версией {} и выше. Пожалуйста, обратитесь к Руководству Пользователя Syncplay (https://syncplay.pl/guide/) за инструкциями о том, как установить syncplay.lua.",  # VLC interface version, VLC interface min version
    "vlc-interface-oldversion-warning": "Внимание: Syncplay обнаружил, что старая версия модуля интерфейса Syncplay для VLC уже установлена в директорию VLC. Пожалуйста, обратитесь к Руководству Пользователя Syncplay (https://syncplay.pl/guide/) за инструкциями о том, как установить syncplay.lua.",
    "vlc-interface-not-installed": "Внимание: Модуль интерфейса Syncplay для VLC не обнаружен в директории VLC. По существу, если Вы используете VLC 2.0, то VLC будет использовать модуль syncplay.lua из директории Syncplay, но в таком случае другие пользовательские скрипты и расширения интерфейса не будут работать. Пожалуйста, обратитесь к Руководству Пользователя Syncplay (https://syncplay.pl/guide/) за инструкциями о том, как установить syncplay.lua.",
    "media-player-latency-warning": "Внимание: У Вашего проигрывателя слишком большой отклик ({} секунд). Если Вы замечаете проблемы с синхронизацией, то закройте ресурсоемкие приложения. Если это не помогло - попробуйте другой проигрыватель.",  # Seconds to respond
    "mpv-unresponsive-error": "mpv не отвечает {} секунд, по-видимому, произошел сбой. Пожалуйста, перезапустите Syncplay.",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "Для выхода нажмите Enter\n",

    # Client errors
    "missing-arguments-error": "Некоторые необходимые аргументы отсутствуют, обратитесь к --help",
    "server-timeout-error": "Подключение к серверу превысило лимит времени",
    "mpc-slave-error": "Невозможно запустить MPC в slave режиме!",
    "mpc-version-insufficient-error": "Версия MPC слишком старая, пожалуйста, используйте `mpc-hc` >= `{}`",
    "mpc-be-version-insufficient-error": "Версия MPC слишком старая, пожалуйста, используйте `mpc-be` >= `{}`",
    "mpv-version-error": "Syncplay не совместим с данной версией mpv. Пожалуйста, используйте другую версию mpv (лучше свежайшую).",
    "player-file-open-error": "Проигрыватель не может открыть файл.",
    "player-path-error": "Путь к проигрывателю задан неверно. Supported players are: mpv, VLC, MPC-HC, MPC-BE and mplayer2.",  # TODO: Translate last sentence
    "hostname-empty-error": "Имя пользователя не может быть пустым.",
    "empty-error": "{} не может быть пустым.",  # Configuration
    "media-player-error": "Ошибка проигрывателя: \"{}\"",  # Error line
    "unable-import-gui-error": "Невозможно импортировать библиотеки GUI (графического интерфейса). Необходимо установить PySide, иначе графический интерфейс не будет работать.",
    "unable-import-twisted-error": "Could not import Twisted. Please install Twisted v12.1.0 or later.", #To do: translate

    "arguments-missing-error": "Некоторые необходимые аргументы отсутствуют, обратитесь к --help",

    "unable-to-start-client-error": "Невозможно запустить клиент",

    "player-path-config-error": "Путь к проигрывателю установлен неверно. Supported players are: mpv, VLC, MPC-HC, MPC-BE and mplayer2",  # To do: Translate end
    "no-file-path-config-error": "Файл должен быть указан до включения проигрывателя",
    "no-hostname-config-error": "Имя сервера не может быть пустым",
    "invalid-port-config-error": "Неверный номер порта",
    "empty-value-config-error": "Поле '{}' не может быть пустым",  # Config option

    "not-json-error": "Не является закодированной json-строкой\n",
    "hello-arguments-error": "Не хватает аргументов Hello\n",
    "version-mismatch-error": "Конфликт версий между клиентом и сервером\n",
    "vlc-failed-connection": "Ошибка подключения к VLC. Если у Вас не установлен syncplay.lua, то обратитесь к https://syncplay.pl/LUA/ за инструкциями.",
    "vlc-failed-noscript": "VLC сообщает, что скрипт интерфейса syncplay.lua не установлен. Пожалуйста, обратитесь к https://syncplay.pl/LUA/ за инструкциями.",
    "vlc-failed-versioncheck": "Данная версия VLC не поддерживается Syncplay. Пожалуйста, используйте VLC версии 2 или выше.",
    "vlc-failed-other": "Во время загрузки скрипта интерфейса syncplay.lua в VLC произошла следующая ошибка: {}",  # Syncplay Error

    "feature-sharedPlaylists": "shared playlists",  # used for not-supported-by-server-error # TODO: Translate
    "feature-chat": "chat",  # used for not-supported-by-server-error # TODO: Translate
    "feature-readiness": "readiness",  # used for not-supported-by-server-error # TODO: Translate
    "feature-managedRooms": "managed rooms",  # used for not-supported-by-server-error # TODO: Translate

    "not-supported-by-server-error": "The {} feature is not supported by this server..",  # feature # TODO: Translate
    # OLD TRANSLATION: "not-supported-by-server-error": u"Эта возможность не поддерживается сервером. Требуется сервер Syncplay {}+, вы подключены к серверу Syncplay {}.",  # minVersion, serverVersion
    "shared-playlists-not-supported-by-server-error": "Общие списки воспроизведения могут не поддерживаться сервером. Для корректной работы требуется сервер Syncplay {}+, вы подключены к серверу Syncplay {}.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "The shared playlist feature has been disabled in the server configuration. To use this feature you will need to connect to a different server.",  # TODO: Translate

    "invalid-seek-value": "Некорректное значение для перемотки",
    "invalid-offset-value": "Некорректное смещение",

    "switch-file-not-found-error": "Невозможно найти файл '{0}'. Проверьте папки воспроизведения.",  # File not found
    "folder-search-timeout-error": "Поиск файла был прерван в папке '{}'. Это может происходить из-за большого количества подпапок. Для корректной работы поиска файлов зайдите через выпадающее меню в Файл->Папки воспроизведения и удалите данную папку из списка, или замените её на нужную подпапку. If the folder is actually fine then you can re-enable it by selecting File->Set Media Directories and pressing 'OK'.",  # Folder # TODO: Translate last sentence
    "folder-search-first-file-timeout-error": "Поиск файла в '{}' был прерван, так как невозможно открыть каталог. Это может происходить, если это сетевой диск или диск перешел в режим экономии энергии. Для корректной работы поиска файлов зайдите через выпадающее меню в Файл->Папки воспроизведения и удалите данную папку, или решите проблему через изменение параметров энергосбережения.",  # Folder
    "added-file-not-in-media-directory-error": "Вы загрузили файл из '{}', который не числится в папках воспроизведения. Вы можете добавить его через выпадающее меню Файл->Папки воспроизведения.",  # Folder
    "no-media-directories-error": "Вы не указали папки воспроизведения. Для корректной работы зайдите через выпадающее меню в Файл->Папки воспроизведения и укажите нужные каталоги.",
    "cannot-find-directory-error": "Не удалось найти папку воспроизведения '{}'. Для обновления списка папок, через выпадающее меню, перейдите в Файл->Папки воспроизведения и укажите нужные каталоги.",

    "failed-to-load-server-list-error": "Не удалось загрузить список публичных серверов. Откройте https://www.syncplay.pl/ через браузер.",

    # Client arguments
    "argument-description": 'Решение для синхронного воспроизведения в VLC, MPlayer или MPC-HC/BE через Интернет.',
    "argument-epilog": 'Если параметр не будет передан, то будет использоваться значение, указанное в _config.',
    "nogui-argument": 'не использовать GUI',
    "host-argument": 'адрес сервера',
    "name-argument": 'желательное имя пользователя',
    "debug-argument": 'режим отладки',
    "force-gui-prompt-argument": 'показать окно настройки',
    "no-store-argument": 'не сохранять данные в .syncplay',
    "room-argument": 'начальная комната',
    "password-argument": 'пароль для доступа к серверу',
    "player-path-argument": 'путь к исполняемому файлу Вашего проигрывателя',
    "file-argument": 'воспроизводимый файл',
    "args-argument": 'параметры проигрывателя; если нужно передать параметры, начинающиеся с - , то сначала пишите \'--\'',
    "clear-gui-data-argument": 'сбрасывает путь и данные о состоянии окна GUI, хранимые как QSettings',
    "language-argument": 'язык сообщений Syncplay (de/en/ru)',

    "version-argument": 'выводит номер версии',
    "version-message": "Вы используете Syncplay версии {} ({})",

    # Client labels
    "config-window-title": "Настройка Syncplay",

    "connection-group-title": "Подключение",
    "host-label": "Адрес сервера: ",
    "name-label": "Имя пользователя (не обязательно):",
    "password-label": "Пароль сервера (если требуется):",
    "room-label": "Комната:",

    "media-setting-title": "Воспроизведение",
    "executable-path-label": "Путь к проигрывателю:",
    "media-path-label": "Путь к видеофайлу:",  # Todo: Translate to 'Path to video (optional)'
    "player-arguments-label": "Аргументы запуска проигрывателя:",
    "browse-label": "Выбрать",
    "update-server-list-label": "Обновить список",

    "more-title": "Больше настроек",
    "never-rewind-value": "Никогда",
    "seconds-suffix": " секунд(ы)",
    "privacy-sendraw-option": "отпр. как есть",
    "privacy-sendhashed-option": "отпр. хэш",
    "privacy-dontsend-option": "не отпр.",
    "filename-privacy-label": "Имя файла:",
    "filesize-privacy-label": "Размер файла:",
    "checkforupdatesautomatically-label": "Проверять обновления автоматически",
    "slowondesync-label": "Замедлять при небольших рассинхронизациях (не поддерживаетя в MPC-HC/BE)",
    "rewindondesync-label": "Перемотка при больших рассинхронизациях (настоятельно рекомендуется)",
    "dontslowdownwithme-label": "Никогда не замедлять и не перематывать видео другим (функция тестируется)",
    "pausing-title": "Приостановка",
    "pauseonleave-label": "Приостанавливать, когда кто-то уходит (например, отключился)",
    "readiness-title": "Готовность",
    "readyatstart-label": "Выставить статус 'Я готов' по умолчанию",
    "fastforwardondesync-label": "Ускорять видео при отставании (рекомендуется)",
    "forceguiprompt-label": "Не показывать больше этот диалог",  # (Inverted)
    "showosd-label": "Включить экранные сообщения (поверх видео)",

    "showosdwarnings-label": "Показывать предупреждения (напр., когда файлы не совпадают)",
    "showsameroomosd-label": "Показывать события Вашей комнаты",
    "shownoncontrollerosd-label": "Включить события, связанные с не-операторами в управляемой комнате.",
    "showdifferentroomosd-label": "Показывать события других комнат",
    "showslowdownosd-label": "Показывать уведомления о замедлении/перемотке",
    "language-label": "Язык:",
    "automatic-language": "По умолчанию ({})",  # Automatic language
    "showdurationnotification-label": "Предупреждать о несовпадении продолжительности видео",
    "basics-label": "Основное",
    "readiness-label": "Поведение",
    "misc-label": "Прочее",
    "core-behaviour-title": "Информация о файлах",
    "syncplay-internals-title": "Системные настройки",
    "syncplay-mediasearchdirectories-title": "Папки воспроизведения",  # needs to be checked
    "syncplay-mediasearchdirectories-label": "Папки воспроизведения (один путь на строку)",
    "sync-label": "Синхронизация",
    "sync-otherslagging-title": "Опережение",
    "sync-youlaggging-title": "Отставание",
    "messages-label": "Сообщения",
    "messages-osd-title": "Настройки OSD",
    "messages-other-title": "Другие настройки отображения",
    "chat-label": "Chat",  # TODO: Translate
    "privacy-label": "Приватность",
    "privacy-title": "Настройки приватности",
    "unpause-title": "Если вы стартуете, то:",
    "unpause-ifalreadyready-option": "Снять паузу, если уже готов",
    "unpause-ifothersready-option": "Снять паузу, если Вы и остальные в комнате готовы (по-умолчанию)",
    "unpause-ifminusersready-option": "Снять паузу, если все в комнате готовы и присутствует минимум зрителей",
    "unpause-always": "Всегда снимать паузу",
    "syncplay-trusteddomains-title": "Доверенные сайты (стрим-сервисы, видеохостинги, файлы в сети)",
    "addtrusteddomain-menu-label": "Добавить {} как доверенный сайт",  # Domain

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
    "chatoutputheader-label": "Chat message output",  # TODO: Traslate
    "chatoutputfont-label": "Chat output font",  # TODO: Translate
    "chatoutputenabled-label": "Enable chat output in media player (mpv only for now)",  # TODO: Translate
    "chatoutputposition-label": "Output mode",  # TODO: Translate
    "chat-chatroom-option": "Chatroom style",  # TODO: Translate
    "chat-scrolling-option": "Scrolling style",  # TODO: Translate

    "mpv-key-tab-hint": "[TAB] to toggle access to alphabet row key shortcuts.",  # TODO: Translate
    "mpv-key-hint": "[ENTER] to send message. [ESC] to escape chat mode.",  # TODO: Translate
    "alphakey-mode-warning-first-line": "You can temporarily use old mpv bindings with a-z keys.",  # TODO: Translate
    "alphakey-mode-warning-second-line": "Press [TAB] to return to Syncplay chat mode.",  # TODO: Translate

    "help-label": "Помощь",
    "reset-label": "Сброс настроек",
    "run-label": "Запустить",
    "storeandrun-label": "Сохранить и запустить",

    "contact-label": "Есть идея, нашли ошибку или хотите оставить отзыв? Пишите на <a href=\"mailto:dev@syncplay.pl\">dev@syncplay.pl</a>, в <a href=\"https://webchat.freenode.net/?channels=#syncplay\">IRC канал #Syncplay</a> на irc.freenode.net или <a href=\"https://github.com/Uriziel/syncplay/issues\">задавайте вопросы через GitHub</a>. Кроме того, заходите на <a href=\"https://syncplay.pl/\">www.syncplay.pl</a> за инорфмацией, помощью и обновлениями! NOTE: Chat messages are not encrypted so do not use Syncplay to send sensitive information.",  # TODO: Translate last sentence

    "joinroom-label": "Зайти в комнату",
    "joinroom-menu-label": "Зайти в комнату {}",
    "seektime-menu-label": "Пере&мотать",
    "undoseek-menu-label": "&Отменить перемотку",
    "play-menu-label": "&Старт",
    "pause-menu-label": "&Пауза",
    "playbackbuttons-menu-label": "&Показывать кнопки управления",
    "autoplay-menu-label": "Показывать кнопку &автовоспроизведения",
    "autoplay-guipushbuttonlabel": "Стартовать, когда все будут готовы",
    "autoplay-minimum-label": "Минимум зрителей:",
    "sendmessage-label": "Send",  # TODO: Translate

    "ready-guipushbuttonlabel": "Я готов",

    "roomuser-heading-label": "Комната / Зритель",

    "size-heading-label": "Размер",
    "duration-heading-label": "Время",
    "filename-heading-label": "Имя файла",
    "notifications-heading-label": "Уведомления",
    "userlist-heading-label": "Кто что смотрит",

    "browseformedia-label": "Выбрать файл",

    "file-menu-label": "&Файл",  # & precedes shortcut key
    "openmedia-menu-label": "&Открыть файл",
    "openstreamurl-menu-label": "Открыть &ссылку",
    "setmediadirectories-menu-label": "&Папки воспроизведения",
    "exit-menu-label": "&Выход",
    "advanced-menu-label": "&Дополнительно",
    "window-menu-label": "&Вид",
    "setoffset-menu-label": "&Установить смещение",
    "createcontrolledroom-menu-label": "Создать управляемую &комнату",
    "identifyascontroller-menu-label": "&Войти как оператор комнаты",
    "settrusteddomains-menu-label": "Доверенные &сайты",

    "playback-menu-label": "&Управление",

    "help-menu-label": "&Помощь",
    "userguide-menu-label": "&Руководство пользователя",
    "update-menu-label": "Проверить &обновления",

    # About dialog - TODO: Translate
    "about-menu-label": "&About Syncplay",
    "about-dialog-title": "About Syncplay",
    "about-dialog-release": "Version {} release {}",
    "about-dialog-license-text": "Licensed under the Apache&nbsp;License,&nbsp;Version 2.0",
    "about-dialog-license-button": "License",
    "about-dialog-dependencies": "Dependencies",

    "setoffset-msgbox-label": "Установить смещение",
    "offsetinfo-msgbox-label": "Смещение (см. инструкцию на странице www.syncplay.pl/guide):",

    "promptforstreamurl-msgbox-label": "Открыть ссылку",
    "promptforstreamurlinfo-msgbox-label": "Ссылка:",

    "addfolder-label": "Добавить папку",

    "adduris-msgbox-label": "Список ссылок (одна на строку)",
    "editplaylist-msgbox-label": "Список воспроизведения (один на строку)",
    "trusteddomains-msgbox-label": "Список доверенных сайтов для автоматического воспроизведения (один на строку)",

    "createcontrolledroom-msgbox-label": "Создать управляемую комнату",
    "controlledroominfo-msgbox-label": "Введите имя управляемой комнаты\r\n(см. инструкцию на странице www.syncplay.pl/guide):",

    "identifyascontroller-msgbox-label": "Войти как оператор комнаты",
    "identifyinfo-msgbox-label": "Введите пароль оператора комнаты\r\n(см. инструкцию на странице www.syncplay.pl/guide):",

    "public-server-msgbox-label": "Выбите публичный сервер для данной сессии",

    "megabyte-suffix": " МБ",  # Technically it is a mebibyte

    # Tooltips

    "host-tooltip": "Имя или IP-адрес, к которому будет произведено подключение, может содержать номер порта (напр., syncplay.pl:8999). Синхронизация возможна только в рамках одного сервера/порта.",
    "name-tooltip": "Имя, под которым Вы будете известны. Регистриция не требуется, так что имя пользователя можно легко сменить в любой момент. Будет сгенерировано случайным образом, если не указать.",
    "password-tooltip": "Пароли нужны для подключения к приватным серверам.",
    "room-tooltip": "Комната, в которую Вы попадете сразу после подключения. Синхронизация возможна только между людьми в одной и той же комнате.",

    "executable-path-tooltip": "Расположение Вашего видеопроигрывателя (MPC-HC, MPC-BE, VLC, mplayer2 или mpv).",
    "media-path-tooltip": "Расположение видеофайла или потока для просмотра. Обязательно для mplayer2.",  # TODO: Confirm translation
    "player-arguments-tooltip": "Передавать дополнительные аргументы командной строки этому проигрывателю.",
    "mediasearcdirectories-arguments-tooltip": "Папки, где Syncplay будет искать медиа файлы, включая подпапки.",

    "more-tooltip": "Показать дополнительные настройки.",
    "filename-privacy-tooltip": "Режим приватности для передачи имени воспроизводимого файла на сервер.",
    "filesize-privacy-tooltip": "Режим приватности для передачи размера воспроизводимого файла на сервер.",
    "privacy-sendraw-tooltip": "Отправляет эту информацию без шифрования. Рекомендуемая опция с наибольшей функциональностью.",
    "privacy-sendhashed-tooltip": "Отправляет хэш-сумму этой информации, делая ее невидимой для других пользователей.",
    "privacy-dontsend-tooltip": "Не отправлять эту информацию на сервер. Предоставляет наибольшую приватность.",
    "checkforupdatesautomatically-tooltip": "Syncplay будет регулярно заходить на сайт и проверять наличие новых версий.",
    "slowondesync-tooltip": "Временно уменьшить скорость воспроизведения в целях синхронизации с другими зрителями. Не поддерживается в MPC-HC/BE.",
    "dontslowdownwithme-tooltip": "Ваши лаги не будут влиять на других зрителей.",
    "pauseonleave-tooltip": "Приостановить воспроизведение, если Вы покинули комнату или кто-то из зрителей отключился от сервера.",
    "readyatstart-tooltip": "Отметить Вас готовым к просмотру сразу же (по умолчанию Вы отмечены не готовым)",
    "forceguiprompt-tooltip": "Окно настройки не будет отображаться при открытии файла в Syncplay.",  # (Inverted)
    "nostore-tooltip": "Запустить Syncplay с данной конфигурацией, но не сохранять изменения навсегда.",
    "rewindondesync-tooltip": "Перематывать назад, когда это необходимо для синхронизации. Отключение этой опции может привести к большим рассинхронизациям!",
    "fastforwardondesync-tooltip": "Перематывать вперед при рассинхронизации с оператором комнаты (или если включена опция 'Никогда не замедлять и не перематывать видео другим').",
    "showosd-tooltip": "Отправлять сообщения Syncplay в видеопроигрыватель и отображать их поверх видео (OSD - On Screen Display).",
    "showosdwarnings-tooltip": "Показывать OSC-предупреждения, если проигрываются разные файлы или если Вы в комнате больше никого нет.",
    "showsameroomosd-tooltip": "Показывать OSD-уведомления о событиях, относящихся к комнате, в которой Вы находитесь.",
    "shownoncontrollerosd-tooltip": "Показывать OSD-уведомления о событиях, относящихся к не-операторам в управляемой комнате.",
    "showdifferentroomosd-tooltip": "Показывать OSD-уведомления о событиях, относящихся к любым другим комнатам.",
    "showslowdownosd-tooltip": "Показывать уведомления о замедлении или перемотке в целях синхронизации.",
    "showdurationnotification-tooltip": "Полезно, когда сегмент составного файла отсутствует. Возможны ложные срабатывания.",
    "language-tooltip": "Язык, используемый Syncplay.",
    "unpause-always-tooltip": "Когда вы стартуете, статус изменится на готов и начнется воспроизведение, а не просто смена статуса.",
    "unpause-ifalreadyready-tooltip": "Когда вы стартуете не готовым, это меняет статус на готов - нажмите старт еще раз для начала воспроизведения.",
    "unpause-ifothersready-tooltip": "Когда вы стартуете не готовым, воспроизведение начнется, если остальные готовы.",
    "unpause-ifminusersready-tooltip": "Когда вы стартуете не готовым, воспроизведение начнется, если остальные готовы и присутствует достаточное число зрителей.",
    "trusteddomains-arguments-tooltip": "Сайты, которые разрешены для автоматического воспроизведения из общего списка воспроизведения.",

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

    "help-tooltip": "Открыть Руководство Пользователя на Syncplay.pl.",
    "reset-tooltip": "Сбрасывает все настройки Syncplay в начальное состояние.",
    "update-server-list-tooltip": "Обновить список публичных серверов от syncplay.pl.",

    "joinroom-tooltip": "Покинуть комнату и зайти в другую, указанную комнату.",
    "seektime-msgbox-label": "Перемотать к определенному моменту времени (указывать в секундах или мин:сек). Используйте +/-, чтобы перемотать вперед/назад относительно настоящего момента.",
    "ready-tooltip": "Показывает, готовы ли Вы к просмотру или нет.",
    "autoplay-tooltip": "Автоматическое воспроизведение, когда все пользователи с индикаторами готовности будут готовы и присутствует достаточное число зрителей.",
    "switch-to-file-tooltip": "Кликните два раза для воспроизведения {}",  # Filename
    "sendmessage-tooltip": "Send message to room",  # TODO: Translate

    # In-userlist notes (GUI)
    "differentsize-note": "Размер файла не совпадает!",
    "differentsizeandduration-note": "Размер и продолжительность файла не совпадают!",
    "differentduration-note": "Продолжительность файла не совпадает!",
    "nofile-note": "(ничего)",

    # Server messages to client
    "new-syncplay-available-motd-message": "<NOTICE> Вы используете Syncplay версии {}. Доступна более новая версия на https://syncplay.pl/ . </NOTICE>",  # ClientVersion

    # Server notifications
    "welcome-server-notification": "Добро пожаловать на сервер Syncplay версии {0}",  # version
    "client-connected-room-server-notification": "{0}({2}) подключился к комнате '{1}'",  # username, host, room
    "client-left-server-notification": "{0} покинул сервер",  # name
    "no-salt-notification": "ВНИМАНИЕ: Чтобы сгенерированные сервером пароли операторов комнат работали после перезагрузки сервера, необходимо указать следующий аргумент командной строки при запуске сервера Syncplay: --salt {}",  # Salt

    # Server arguments
    "server-argument-description": 'Решение для синхронного воспроизведения в VLC, MPlayer или MPC-HC/BE через Интернет. Серверная часть',
    "server-argument-epilog": 'Если параметр не будет передан, то будет использоваться значение, указанное в _config.',
    "server-port-argument": 'номер TCP порта сервера',
    "server-password-argument": 'пароль к серверу',
    "server-isolate-room-argument": 'должны ли комнаты быть изолированными?',
    "server-salt-argument": "генерировать пароли к управляемым комнатам на основании указанной строки (соли)",
    "server-disable-ready-argument": "отключить статусы готов/не готов",
    "server-motd-argument": "путь к файлу, из которого будет извлекаться MOTD-сообщение",
    "server-chat-argument": "Should chat be disabled?",  # TODO: Translate
    "server-chat-maxchars-argument": "Maximum number of characters in a chat message (default is {})",  # TODO: Translate
    "server-maxusernamelength-argument": "Maximum number of characters in a username (default is {})", # TODO: Translate
    "server-stats-db-file-argument": "Enable server stats using the SQLite db file provided", # TODO: Translate
    "server-messed-up-motd-unescaped-placeholders" : "MOTD-сообщение содержит неэкранированные спец.символы. Все знаки $ должны быть продублированы ($$).",
    "server-messed-up-motd-too-long" : "MOTD-сообщение слишком длинное: максимальная длина - {} символ(ов), текущая длина - {} символ(ов).",

    # Server errors
    "unknown-command-server-error": "Неизвестная команда: {}",  # message
    "not-json-server-error": "Не является закодированной json-строкой: {}",  # message
    "not-known-server-error": "Данную команду могут выполнять только авторизованные пользователи.",
    "client-drop-server-error": "Клиент отключен с ошибкой: {} -- {}",  # host, error
    "password-required-server-error": "Необходимо указать пароль.",
    "wrong-password-server-error": "Указан неверный пароль.",
    "hello-server-error": "Не хватает аргументов Hello.",

    "playlist-selection-changed-notification":  "{} изменил выбор в списке воспроизведения",  # Username
    "playlist-contents-changed-notification": "{} обновил список воспроизведения",  # Username
    "cannot-find-file-for-playlist-switch-error": "Не удалось найти файл {} в папках воспроизведения!",  # Filename
    "cannot-add-duplicate-error": "'{}' уже есть в списке воспроизведения.",  # Filename
    "cannot-add-unsafe-path-error": "Не удалось автоматически переключиться на {}, потому что ссылка не соответствует доверенным сайтам. Её можно включить вручную, дважны кливнув по ссылке в списке воспроизведения. Добавить доверенный сайт можно в выпадающем меню 'Дополнительно' или просто кликнув по ссылке правой кнопкой мыши.",  # Filename
    "sharedplaylistenabled-label": "Включить общий список воспроизведения",
    "removefromplaylist-menu-label": "Удалить",
    "shufflepremaininglaylist-menu-label": "Shuffle remaining playlist",  # Was: Перемешать список # TODO: Translate
    "shuffleentireplaylist-menu-label": "Shuffle entire playlist",  # TODO: Translate
    "undoplaylist-menu-label": "Отменить последнее действие",
    "addfilestoplaylist-menu-label": "Добавить файлы в очередь",
    "addurlstoplaylist-menu-label": "Добавить ссылку в очередь",
    "editplaylist-menu-label": "Редактировать список",

    "open-containing-folder": "Open folder containing this file",  # TODO: Traslate
    "addusersfiletoplaylist-menu-label": "Добавить файл {} в список воспроизведения",  # item owner indicator
    "addusersstreamstoplaylist-menu-label": "Добавить поток {} в список воспроизведения",  # item owner indicator
    "openusersstream-menu-label": "Открыть поток от {}",  # [username]'s
    "openusersfile-menu-label": "Открыть файл от {}",  # [username]'s
    "item-is-yours-indicator": "от вас",  # Goes with addusersfiletoplaylist/addusersstreamstoplaylist
    "item-is-others-indicator": "{}",  # username - goes with addusersfiletoplaylist/addusersstreamstoplaylist

    "playlist-instruction-item-message": "Перетащите сюда файлы, чтобы добавить их в общий список.",
    "sharedplaylistenabled-tooltip": "Оператор комнаты может добавлять файлы в список общего воспроизведения для удобного совместного просмотра. Папки воспроизведения настраиваются во вкладке 'Файл'.",
}
