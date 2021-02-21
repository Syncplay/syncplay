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
    "reachout-successful-notification": "Подключение к {} ({}) успешно",

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
    "ready-to-unpause-notification": "Вы помечены как готовый — нажмите ещё раз, чтобы продолжить воспроизведение",
    "set-as-ready-notification": "Вы помечены как готовый",
    "set-as-not-ready-notification": "Вы помечены как неготовый",
    "autoplaying-notification": "Автовоспроизведение через {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Идентификация как оператора комнаты с паролем '{}'...",
    "failed-to-identify-as-controller-notification": "{} не прошел идентификацию в качестве оператора комнаты.",
    "authenticated-as-controller-notification": "{} вошёл как оператор комнаты.",
    "created-controlled-room-notification": "Создана управляемая комната '{}' с паролем '{}'. Сохраните эти данные!\n\nВ управляемых комнатах всех синхронизируют с оператором (-ами) комнаты, только у которых есть права ставить и снимать с паузы, перематывать и изменять список воспроизведения.\n\nПопросите обычных зрителей подключиться к комнате '{}', а операторы могут подключиться к комнате '{}', чтобы автоматически авторизироваться.", # RoomName, operatorPassword, roomName, roomName:operatorPassword
    "file-different-notification": "Вероятно, файл, который вы смотрите, отличается от того, который смотрит {}.",  # User
    "file-differences-notification": "Ваш файл отличается: {}",  # Differences
    "room-file-differences": "Несовпадения файла: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "имя",
    "file-difference-filesize": "размер",
    "file-difference-duration": "длительность",
    "alone-in-the-room": "В комнате кроме вас никого нет.",

    "different-filesize-notification": " (размер вашего файла не совпадает с размером их файла!)",
    "userlist-playing-notification": "{} смотрит:",  # Username
    "file-played-by-notification": "Файл: {} просматривают:",  # File
    "no-file-played-notification": "{} не смотрит ничего",  # Username
    "notplaying-notification": "Люди, которые не смотрят ничего:",
    "userlist-room-notification": "В комнате '{}':",  # Room
    "userlist-file-notification": "Файл",
    "controller-userlist-userflag": "Оператор",
    "ready-userlist-userflag": "Готов",

    "update-check-failed-notification": "Невозможно автоматически проверить, что версия Syncplay {} все ещё актуальна. Хотите зайти на https://syncplay.pl/ и вручную проверить наличие обновлений?",
    "syncplay-uptodate-notification": "У вас последняя версия Syncplay",
    "syncplay-updateavailable-notification": "Доступна новая версия Syncplay. Хотите открыть страницу релиза?",

    "mplayer-file-required-notification": "Для использования Syncplay с mplayer необходимо передать файл в качестве параметра",
    "mplayer-file-required-notification/example": "Пример использования: syncplay [options] [url|path/]filename",
    "mplayer2-required": "Syncplay несовместим с MPlayer 1.x, пожалуйста, используйте mplayer2 или mpv",

    "unrecognized-command-notification": "Неизвестная команда.",
    "commandlist-notification": "Доступные команды:",
    "commandlist-notification/room": "\tr [имя комнаты] - сменить комнату",
    "commandlist-notification/list": "\tl - показать список пользователей",
    "commandlist-notification/undo": "\tu - отменить последнюю перемотку",
    "commandlist-notification/pause": "\tp - вкл./выкл. паузу",
    "commandlist-notification/seek": "\t[s][+-]time - перемотать к заданному моменту времени, если не указан + или -, то время считается абсолютным (от начала файла) в секундах или мин:сек",
    "commandlist-notification/help": "\th - помощь",
    "commandlist-notification/toggle": "\tt - переключить статус готов/не готов к просмотру",
    "commandlist-notification/create": "\tc [имя комнаты] - создать управляемую комнату с таким же именем, как у текущей",
    "commandlist-notification/auth": "\ta [пароль] - авторизоваться как оператор комнаты с помощью пароля",
    "commandlist-notification/chat": "\tch [сообщение] - выслать сообщение в комнату",
    "commandList-notification/queue": "\tqa [файл/URL] - добавить файл или URL в конец списка воспроизведения",
    "commandList-notification/playlist": "\tql - показать текущий список воспроизведения",
    "commandList-notification/select": "\tqs [индекс] - выделить указанный пункт в списке воспроизведения",
    "commandList-notification/delete": "\tqd [индекс] - удалить указанный пункт из списка воспроизведения",
    "commandList-notification/load": "\tlf [path] - load file",
    "syncplay-version-notification": "Версия Syncplay: {}",  # syncplay.version
    "more-info-notification": "Больше информации на {}",  # projectURL

    "gui-data-cleared-notification": "Syncplay очистил путь и информацию о состоянии окна, использованного GUI.",
    "language-changed-msgbox-label": "Язык переключится при следующем запуске Syncplay.",
    "promptforupdate-label": "Разрешить Syncplay периодически проверять наличие обновлений?",

    "media-player-latency-warning": "Внимание: у проигрывателя слишком большой отклик ({} секунд). Если заметите проблемы с синхронизацией, закройте ресурсоёмкие приложения. Если не поможет, попробуйте другой проигрыватель.",  # Seconds to respond
    "mpv-unresponsive-error": "mpv не отвечает {} секунд, по-видимому, произошел сбой. Пожалуйста, перезапустите Syncplay.",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "Для выхода нажмите \"Ввод\"\n",

    # Client errors
    "missing-arguments-error": "Некоторые необходимые аргументы отсутствуют, обратитесь к --help",
    "server-timeout-error": "Подключение к серверу превысило лимит времени",
    "mpc-slave-error": "Невозможно запустить MPC в режиме slave!",
    "mpc-version-insufficient-error": "Версия MPC слишком старая, пожалуйста, используйте `mpc-hc` >= `{}`",
    "mpc-be-version-insufficient-error": "Версия MPC слишком старая, пожалуйста, используйте `mpc-be` >= `{}`",
    "mpv-version-error": "Syncplay несовместим с данной версией mpv. Пожалуйста, используйте другую версию mpv (лучше свежайшую).",
    "mpv-failed-advice": "Возможно, mpv не может запуститься из-за неподдерживаемых параметров командной строки или неподдерживаемой версии mpv.",
    "player-file-open-error": "Проигрыватель не может открыть файл.",
    "player-path-error": "Путь к проигрывателю задан неверно. Поддерживаемые проигрыватели: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 и IINA.",
    "hostname-empty-error": "Имя пользователя не может быть пустым.",
    "empty-error": "{} не может быть пустым.",  # Configuration
    "media-player-error": "Ошибка проигрывателя: \"{}\"",  # Error line
    "unable-import-gui-error": "Невозможно импортировать библиотеки графического интерфейса. Необходимо установить PySide, иначе графический интерфейс не будет работать.",
    "unable-import-twisted-error": "Невозможно импортировать Twisted. Установите Twisted 16.4.0 или более позднюю версию.",

    "arguments-missing-error": "Некоторые необходимые аргументы отсутствуют, обратитесь к --help",

    "unable-to-start-client-error": "Невозможно запустить клиент",

    "player-path-config-error": "Путь к проигрывателю установлен неверно. Поддерживаемые проигрыватели: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 и IINA.",
    "no-file-path-config-error": "Файл должен быть указан до включения проигрывателя",
    "no-hostname-config-error": "Адрес сервера не может быть пустым",
    "invalid-port-config-error": "Неверный номер порта",
    "empty-value-config-error": "Поле '{}' не может быть пустым",  # Config option

    "not-json-error": "Не является закодированной json-строкой\n",
    "hello-arguments-error": "Не хватает аргументов Hello\n",
    "version-mismatch-error": "Конфликт версий между клиентом и сервером\n",
    "vlc-failed-connection": "Ошибка подключения к VLC. Если у вас не установлен syncplay.lua, обратитесь к https://syncplay.pl/LUA/ за инструкциями. На данный момент Syncplay несовместим с VLC 4, поэтому используйте VLC 3 или другой проигрыватель, например, mpv.",
    "vlc-failed-noscript": "VLC сообщает, что скрипт интерфейса syncplay.lua не установлен. Пожалуйста, обратитесь к https://syncplay.pl/LUA/ за инструкциями.",
    "vlc-failed-versioncheck": "Данная версия VLC не поддерживается Syncplay. Пожалуйста, используйте VLC версии 2 или выше.",
    "vlc-initial-warning": 'VLC не всегда предоставляет точную информацию о позиции воспроизведения, особенно для файлов с расширениями mp4 и avi. Если возникли проблемы с перемоткой, попробуйте другой проигрыватель, например, <a href="https://mpv.io/">mpv</a> (или <a href="https://github.com/stax76/mpv.net/">mpv.net</a> для Windows).',

    "feature-sharedPlaylists": "общий список воспроизведения",  # used for not-supported-by-server-error
    "feature-chat": "чат",  # used for not-supported-by-server-error
    "feature-readiness": "готовность",  # used for not-supported-by-server-error
    "feature-managedRooms": "управляемые комнаты",  # used for not-supported-by-server-error

    "not-supported-by-server-error": "Возможность '{}' не поддерживается сервером.",  # feature
    "shared-playlists-not-supported-by-server-error": "Общие списки воспроизведения могут не поддерживаться сервером. Для корректной работы требуется сервер Syncplay {}+, вы подключены к серверу Syncplay {}.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "Общий список воспроизведения отключён сервером. Чтобы использовать эту возможность, подключитесь к другому серверу.",

    "invalid-seek-value": "Некорректное значение для перемотки",
    "invalid-offset-value": "Некорректное смещение",

    "switch-file-not-found-error": "Невозможно найти файл '{0}'. Проверьте папки воспроизведения.",  # File not found
    "folder-search-timeout-error": "Поиск файла был прерван в папке '{}'. Это может произойти из-за большого количества подпапок. Для корректной работы поиска файлов зайдите через выпадающее меню в Файл->Папки воспроизведения и удалите данную папку из списка или замените её на нужную подпапку. Если на самом деле с папкой всё в порядке, вы можете cнова её включить через выпадающее меню Файл->Папки воспроизведения.", # Folder
    "folder-search-first-file-timeout-error": "Поиск файла в '{}' был прерван, так как невозможно открыть каталог. Это может произойти, если это сетевой диск или диск перешёл в режим экономии энергии. Для корректной работы поиска файлов зайдите через выпадающее меню в Файл->Папки воспроизведения и удалите данную папку, или решите проблему изменив параметры энергосбережения.",  # Folder
    "added-file-not-in-media-directory-error": "Вы загрузили файл из '{}', который не числится в папках воспроизведения. Вы можете добавить его через выпадающее меню Файл->Папки воспроизведения.",  # Folder
    "no-media-directories-error": "Вы не указали папки воспроизведения. Для корректной работы зайдите через выпадающее меню в Файл->Папки воспроизведения и укажите нужные каталоги.",
    "cannot-find-directory-error": "Не удалось найти папку воспроизведения '{}'. Чтобы обновить список папок, через выпадающее меню перейдите в Файл->Папки воспроизведения и укажите нужные каталоги.",

    "failed-to-load-server-list-error": "Не удалось загрузить список публичных серверов. Откройте https://www.syncplay.pl/ через браузер.",

    # Client arguments
    "argument-description": 'Решение для синхронного воспроизведения в VLC, MPlayer или MPC-HC/BE через Интернет.',
    "argument-epilog": 'Если параметр не будет передан, то будет использоваться значение, указанное в _config.',
    "nogui-argument": 'не использовать GUI',
    "host-argument": 'адрес сервера',
    "name-argument": 'желаемое имя пользователя',
    "debug-argument": 'режим отладки',
    "force-gui-prompt-argument": 'показать окно настройки',
    "no-store-argument": 'не сохранять данные в .syncplay',
    "room-argument": 'начальная комната',
    "password-argument": 'пароль для доступа к серверу',
    "player-path-argument": 'путь к исполняемому файлу проигрывателя',
    "file-argument": 'воспроизводимый файл',
    "args-argument": 'параметры проигрывателя; если нужно передать параметры, начинающиеся с - , то сначала пишите \'--\'',
    "clear-gui-data-argument": 'сбрасывает путь и данные о состоянии окна GUI, хранимые как QSettings',
    "language-argument": 'язык сообщений Syncplay (de/en/ru/it/es/pt_BR/pt_PT/tr)',

    "version-argument": 'выводит номер версии',
    "version-message": "Вы используете Syncplay версии {} ({})",

    "load-playlist-from-file-argument": "загружает список воспроизведения из текстового файла (один пункт на строку)",

    # Client labels
    "config-window-title": "Настройка Syncplay",

    "connection-group-title": "Подключение",
    "host-label": "Адрес сервера: ",
    "name-label": "Имя пользователя (не обязательно):",
    "password-label": "Пароль сервера (если требуется):",
    "room-label": "Комната:",
    "roomlist-msgbox-label": "Редактировать список комнат (одна на строку)",

    "media-setting-title": "Воспроизведение",
    "executable-path-label": "Путь к проигрывателю:",
    "media-path-label": "Путь к видеофайлу (не обязателен):",
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
    "autosavejoinstolist-label": "Добавлять комнаты, к которым вы подключаетесь, в список комнат",
    "slowondesync-label": "Замедлять при небольших рассинхронизациях (не поддерживаетя в MPC-HC/BE)",
    "rewindondesync-label": "Перемотка при больших рассинхронизациях (настоятельно рекомендуется)",
    "dontslowdownwithme-label": "Никогда не замедлять и не перематывать видео другим (функция тестируется)",
    "pausing-title": "Приостановка",
    "pauseonleave-label": "Приостанавливать, когда кто-то уходит (например, отключается)",
    "readiness-title": "Готовность",
    "readyatstart-label": "Выставить статус 'Я готов' по умолчанию",
    "fastforwardondesync-label": "Ускорять видео при отставании (рекомендуется)",
    "forceguiprompt-label": "Не всегда показывать окно настройки Syncplay",  # (Inverted)
    "showosd-label": "Включить экранные сообщения (поверх видео)",

    "showosdwarnings-label": "Показывать предупреждения (напр., когда файлы не совпадают)",
    "showsameroomosd-label": "Показывать события вашей комнаты",
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
    "chat-label": "Чат",
    "privacy-label": "Приватность",
    "privacy-title": "Настройки приватности",
    "unpause-title": "Если вы стартуете, то:",
    "unpause-ifalreadyready-option": "Снять паузу, если уже готов",
    "unpause-ifothersready-option": "Снять паузу, если вы и остальные в комнате готовы (по умолчанию)",
    "unpause-ifminusersready-option": "Снять паузу, если все в комнате готовы и присутствует минимум зрителей",
    "unpause-always": "Всегда снимать паузу",
    "syncplay-trusteddomains-title": "Доверенные сайты (стрим-сервисы, видеохостинги, файлы в сети)",
    "addtrusteddomain-menu-label": "Добавить {} как доверенный сайт",  # Domain

    "chat-title": "Ввод сообщений чата",
    "chatinputenabled-label": "Разрешить ввод сообщений в mpv (при помощи клавиши 'ввод')",
    "chatdirectinput-label": "Разрешить мгновенный ввод сообщений (без необходимости нажимать 'ввод', чтобы выслать сообщение)",
    "chatinputfont-label": "Шрифт для поля ввода сообщений",
    "chatfont-label": "Установить шрифт",
    "chatcolour-label": "Установить цвет",
    "chatinputposition-label": "Позиция поля ввода сообщения в mpv",
    "chat-top-option": "Вверху",
    "chat-middle-option": "Посередине",
    "chat-bottom-option": "Внизу",
    "chatoutputheader-label": "Вывод сообщений чата",
    "chatoutputfont-label": "Шрифт сообщений чата",
    "chatoutputenabled-label": "Разрешить вывод сообщений в проигрывателе (пока что только в mpv)",
    "chatoutputposition-label": "Режим вывода",
    "chat-chatroom-option": "Режим чата",
    "chat-scrolling-option": "Режим прокрутки",

    "mpv-key-tab-hint": "[TAB] - включить или выключить горячие клавиши mpv.",
    "mpv-key-hint": "[ВВОД] - выслать сообщение. [ESC] - выйти из режима чата.",
    "alphakey-mode-warning-first-line": "Сейчас можно использовать горячие клавиши mpv, нажимая a-z.",
    "alphakey-mode-warning-second-line": "Нажмите [TAB], чтобы вернуться в режим чата.",

    "help-label": "Помощь",
    "reset-label": "Сброс настроек",
    "run-label": "Запустить",
    "storeandrun-label": "Сохранить и запустить",

    "contact-label": "Есть идея, нашли ошибку или хотите оставить отзыв? Пишите на <a href=\"mailto:dev@syncplay.pl\">dev@syncplay.pl</a>, в <a href=\"https://webchat.freenode.net/?channels=#syncplay\">IRC канал #Syncplay</a> на irc.freenode.net или <a href=\"https://github.com/Uriziel/syncplay/issues\">задавайте вопросы через GitHub</a>. Кроме того, заходите на <a href=\"https://syncplay.pl/\">www.syncplay.pl</a> за информацией, помощью и обновлениями! Не используйте Syncplay для передачи конфиденциальной информации.",

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
    "sendmessage-label": "Выслать",

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
    "loadplaylistfromfile-menu-label": "&Загрузить список воспроизведения из файла",
    "saveplaylisttofile-menu-label": "&Сохранить список воспроизведения в файл",
    "exit-menu-label": "&Выход",
    "advanced-menu-label": "&Дополнительно",
    "window-menu-label": "&Вид",
    "setoffset-menu-label": "&Установить смещение",
    "createcontrolledroom-menu-label": "Создать управляемую &комнату",
    "identifyascontroller-menu-label": "&Войти как оператор комнаты",
    "settrusteddomains-menu-label": "Доверенные &сайты",

    # Edit menu - TODO: check - these should match the values of macOS menubar
    "edit-menu-label": "&Правка",
    "cut-menu-label": "Bы&резать",
    "copy-menu-label": "&Скопировать",
    "paste-menu-label": "&Bставить",
    "selectall-menu-label": "Bыбра&ть все",

    "playback-menu-label": "&Управление",

    "help-menu-label": "&Помощь",
    "userguide-menu-label": "&Руководство пользователя",
    "update-menu-label": "Проверить &обновления",

    "startTLS-initiated": "Попытка установить безопасное соединение",
    "startTLS-secure-connection-ok": "Безопасное соединение установлено ({})",
    "startTLS-server-certificate-invalid": 'Не удалось установить безопасное соединение. Сервер использует некорректный сертификат безопасности. Коммуникация с сервером может быть перехвачена третьими лицами. Подробности и способы устранения проблемы <a href="https://syncplay.pl/trouble">здесь</a>.',
    "startTLS-server-certificate-invalid-DNS-ID": "Syncplay не доверяет этому серверу, потому что сервер использует сертификат безопасности, не предназначенный для данного адреса.",
    "startTLS-not-supported-client": "Клиент не поддерживает TLS",
    "startTLS-not-supported-server": "Сервер не поддерживает TLS",

    "tls-information-title": "Подробности сертификата",
    "tls-dialog-status-label": "<strong>Syncplay использует зашифрованное соединение с {}.</strong>",
    "tls-dialog-desc-label": "Шифрование при помощи цифрового сертификата позволяет не разглашать<br/>информацию во время передачи данных на сервер {} и с него.",
    "tls-dialog-connection-label": "Информация зашифрована при помощи Transport Layer Security (TLS)<br/>версии {} шифром {}.",
    "tls-dialog-certificate-label": "Сертификат выдан {}, действителен до {}.",

    "about-menu-label": "&О Syncplay",
    "about-dialog-title": "О Syncplay",
    "about-dialog-release": "Версия {}, выпуск {}",
    "about-dialog-license-text": "Лицензировано на условиях Apache&nbsp;License,&nbsp;Version 2.0",
    "about-dialog-license-button": "Лицензия",
    "about-dialog-dependencies": "Зависимости",

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

    "public-server-msgbox-label": "Выберите публичный сервер для данной сессии",

    "megabyte-suffix": " МБ",  # Technically it is a mebibyte

    # Tooltips

    "host-tooltip": "Имя или IP-адрес, к которому будет произведено подключение, может содержать номер порта (напр., syncplay.pl:8999). Синхронизация возможна только в рамках одного сервера/порта.",
    "name-tooltip": "Имя, под которым вы будете известны. Регистрация не требуется, поэтому имя можно легко сменить в любой момент. Если оставить пустым, будет сгенерировано случайное имя.",
    "password-tooltip": "Пароли нужны для подключения к приватным серверам.",
    "room-tooltip": "Комната, в которую вы попадете сразу после подключения. Синхронизация возможна только между людьми в одной и той же комнате.",

    "edit-rooms-tooltip": "Редактировать список комнат.",

    "executable-path-tooltip": "Расположение проигрывателя (mpv, mpv.net, VLC, MPC-HC/BE, mplayer2 или IINA).",
    "media-path-tooltip": "Расположение видеофайла или потока для просмотра. Обязательно для mplayer2.",
    "player-arguments-tooltip": "Передавать дополнительные аргументы командной строки этому проигрывателю.",
    "mediasearcdirectories-arguments-tooltip": "Папки, где Syncplay будет искать медиафайлы, включая подпапки.",

    "more-tooltip": "Показать дополнительные настройки.",
    "filename-privacy-tooltip": "Режим приватности для передачи имени воспроизводимого файла на сервер.",
    "filesize-privacy-tooltip": "Режим приватности для передачи размера воспроизводимого файла на сервер.",
    "privacy-sendraw-tooltip": "Отправляет эту информацию без шифрования. Рекомендуемая опция с наибольшей функциональностью.",
    "privacy-sendhashed-tooltip": "Отправляет хэш-сумму этой информации, делая ее невидимой для других пользователей.",
    "privacy-dontsend-tooltip": "Не отправлять эту информацию на сервер. Предоставляет наибольшую приватность.",
    "checkforupdatesautomatically-tooltip": "Syncplay будет регулярно заходить на сайт и проверять наличие новых версий.",
    "autosavejoinstolist-tooltip": "Автоматически запоминать название комнаты в списке при подключении к комнате.",
    "slowondesync-tooltip": "Временно уменьшить скорость воспроизведения в целях синхронизации с другими зрителями. Не поддерживается в MPC-HC/BE.",
    "dontslowdownwithme-tooltip": "Ваше отставание не будет влиять на других зрителей.",
    "pauseonleave-tooltip": "Приостановить воспроизведение, если вы покинули комнату или кто-то из зрителей отключился от сервера.",
    "readyatstart-tooltip": "Отметить вас готовым к просмотру сразу же (по умолчанию вы отмечены не готовым)",
    "forceguiprompt-tooltip": "Окно настройки не будет отображаться при открытии файла в Syncplay.",  # (Inverted)
    "nostore-tooltip": "Запустить Syncplay с данной конфигурацией, но не сохранять изменения навсегда.",
    "rewindondesync-tooltip": "Перематывать назад, когда это необходимо для синхронизации. Отключение этой опции может привести к большим рассинхронизациям!",
    "fastforwardondesync-tooltip": "Перематывать вперед при рассинхронизации с оператором комнаты (или если включена опция 'Никогда не замедлять и не перематывать видео другим').",
    "showosd-tooltip": "Отправлять сообщения Syncplay в видеопроигрыватель и отображать их поверх видео (OSD - On Screen Display).",
    "showosdwarnings-tooltip": "Показывать OSC-предупреждения, если проигрываются разные файлы или если вы в комнате больше никого нет.",
    "showsameroomosd-tooltip": "Показывать OSD-уведомления о событиях, относящихся к комнате, в которой вы находитесь.",
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

    "chatinputenabled-tooltip": "Разрешить ввод сообщений в mpv (нажмите 'Ввод', чтобы ввести сообщение, 'Ввод', чтобы отправить, 'Escape', чтобы отменить)",
    "chatdirectinput-tooltip": "Не требовать нажимать 'Ввод' для ввода сообщений в mpv. Нажмите 'Tab', чтобы временно отключить эту возможность.",
    "font-label-tooltip": "Шрифт для ввода сообщений в mpv. Настройка на стороне клиента, поэтому не влияет на то, что видят другие.",
    "set-input-font-tooltip": "Шрифт для ввода сообщений в mpv. Настройка на стороне клиента, поэтому не влияет на то, что видят другие.",
    "set-input-colour-tooltip": "Цвет шрифта для ввода сообщений в mpv. Настройка на стороне клиента, поэтому не влияет на то, что видят другие.",
    "chatinputposition-tooltip": "Расположение поля ввода сообщений, которое появляется, если нажать 'Ввод' и начать набирать сообщение.",
    "chatinputposition-top-tooltip": "Разместить ввод сообщений вверху окна mpv.",
    "chatinputposition-middle-tooltip": "Разместить ввод сообщений в центре окна mpv.",
    "chatinputposition-bottom-tooltip": "Разместить ввод сообщений внизу окна mpv.",
    "chatoutputenabled-tooltip": "Показывать сообщения в проигрывателе (если поддерживается проигрывателем).",
    "font-output-label-tooltip": "Шрифт для вывода сообщений чата.",
    "set-output-font-tooltip": "Шрифт для отображения сообщений в чате.",
    "chatoutputmode-tooltip": "Как отображаются сообщения в чате.",
    "chatoutputmode-chatroom-tooltip": "Показывать новые сообщения под предыдущим сообщением.",
    "chatoutputmode-scrolling-tooltip": "Прокручивать сообщения в чате справа налево.",

    "help-tooltip": "Открыть Руководство Пользователя на Syncplay.pl.",
    "reset-tooltip": "Сбрасывает все настройки Syncplay в начальное состояние.",
    "update-server-list-tooltip": "Обновить список публичных серверов от syncplay.pl.",

    "sslconnection-tooltip": "Установлено безопасное соединение с сервером. Нажмите, чтобы увидеть подробности сертификата.",

    "joinroom-tooltip": "Покинуть комнату и зайти в другую, указанную комнату.",
    "seektime-msgbox-label": "Перемотать к определенному моменту времени (указывать в секундах или мин:сек). Используйте +/-, чтобы перемотать вперед/назад относительно настоящего момента.",
    "ready-tooltip": "Показывает, готовы ли вы к просмотру или нет.",
    "autoplay-tooltip": "Автоматическое воспроизведение, когда все пользователи с индикаторами готовности будут готовы и присутствует достаточное число зрителей.",
    "switch-to-file-tooltip": "Кликните два раза для воспроизведения {}",  # Filename
    "sendmessage-tooltip": "Выслать сообщение в комнату",

    # In-userlist notes (GUI)
    "differentsize-note": "Размер файла не совпадает!",
    "differentsizeandduration-note": "Размер и продолжительность файла не совпадают!",
    "differentduration-note": "Продолжительность файла не совпадает!",
    "nofile-note": "(Никакой файл не проигрывается)",

    # Server messages to client
    "new-syncplay-available-motd-message": "Вы используете Syncplay версии {}. Доступна более новая версия на https://syncplay.pl/",  # ClientVersion

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
    "server-chat-argument": "Должен ли чат быть отключён?",
    "server-chat-maxchars-argument": "Максимальное число символов в сообщениях в чате (по умолчанию {})",
    "server-maxusernamelength-argument": "Максимальное число символов в именах пользователей (по умолчанию {})",
    "server-stats-db-file-argument": "Включить статистику сервера в указанном файле SQLite",
    "server-startTLS-argument": "Включить TLS-соединения используя файлы сертификатов в указанном пути",
    "server-messed-up-motd-unescaped-placeholders": "MOTD-сообщение содержит неэкранированные спецсимволы. Все знаки $ должны быть продублированы ($$).",
    "server-messed-up-motd-too-long": "MOTD-сообщение слишком длинное: максимальная длина - {} символ(ов), текущая длина - {} символ(ов).",

    # Server errors
    "unknown-command-server-error": "Неизвестная команда: {}",  # message
    "not-json-server-error": "Не является закодированной json-строкой: {}",  # message
    "line-decode-server-error": "Не строка в кодировке UTF-8",
    "not-known-server-error": "Данную команду могут выполнять только авторизованные пользователи.",
    "client-drop-server-error": "Клиент отключен с ошибкой: {} -- {}",  # host, error
    "password-required-server-error": "Необходимо указать пароль.",
    "wrong-password-server-error": "Указан неверный пароль.",
    "hello-server-error": "Не хватает аргументов Hello.",

    "playlist-selection-changed-notification":  "{} изменил выбор в списке воспроизведения",  # Username
    "playlist-contents-changed-notification": "{} обновил список воспроизведения",  # Username
    "cannot-find-file-for-playlist-switch-error": "Не удалось найти файл {} в папках воспроизведения!",  # Filename
    "cannot-add-duplicate-error": "'{}' уже есть в списке воспроизведения.",  # Filename
    "cannot-add-unsafe-path-error": "Не удалось автоматически переключиться на {}, потому что ссылка не соответствует доверенным сайтам. Её можно включить вручную, дважды кликнув по ссылке в списке воспроизведения. Добавить доверенный сайт можно в меню 'Дополнительно' или просто кликнув по ссылке правой кнопкой мыши.",  # Filename
    "sharedplaylistenabled-label": "Включить общий список воспроизведения",
    "removefromplaylist-menu-label": "Удалить",
    "shuffleremainingplaylist-menu-label": "Перемешать оставшийся список воспроизведения",
    "shuffleentireplaylist-menu-label": "Перемешать весь список воспроизведения",
    "undoplaylist-menu-label": "Отменить последнее действие",
    "addfilestoplaylist-menu-label": "Добавить файлы в очередь",
    "addurlstoplaylist-menu-label": "Добавить ссылку в очередь",
    "editplaylist-menu-label": "Редактировать список",

    "open-containing-folder": "Открыть папку, содержащую этот файл",
    "addyourfiletoplaylist-menu-label": "Добавить ваш файл в список воспроизведения",
    "addotherusersfiletoplaylist-menu-label": "Добавить файл {} в список воспроизведения",
    "addyourstreamstoplaylist-menu-label": "Добавить ваш поток в список воспроизведения",
    "addotherusersstreamstoplaylist-menu-label": "Добавить поток {} в список воспроизведения",
    "openusersstream-menu-label": "Открыть поток {}",
    "openusersfile-menu-label": "Открыть файл {}",

    "playlist-instruction-item-message": "Перетащите сюда файлы, чтобы добавить их в общий список.",
    "sharedplaylistenabled-tooltip": "Оператор комнаты может добавлять файлы в список общего воспроизведения для удобного совместного просмотра. Папки воспроизведения настраиваются в меню 'Файл'.",

    "playlist-empty-error": "Список воспроизведения пуст.",
    "playlist-invalid-index-error": "Неверный индекс в списке воспроизведения",
}
