# coding:utf8

"""Ukrainian dictionary"""

# Filename, dictionary name and LANGUAGE-TAG value based on ISO country code. Language tag listed at https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/a9eac961-e77d-41a6-90a5-ce1a8b0cdb9c?redirectedfrom=MSDN

uk_UA = {
    "LANGUAGE": "Українська",  # (Ukrainian)
    "LANGUAGE-TAG": "uk-UA",

    # Strings for Windows NSIS installer
    "installer-language-file": "Ukrainian.nlf", # Relevant .nlf file at https://github.com/kichik/nsis/tree/master/Contrib/Language%20files
    "installer-associate": "Асоціювати Syncplay з відеофайлами",
    "installer-shortcut": "Створити ярлики:",
    "installer-start-menu": "у меню Пуск",
    "installer-desktop": "на робочому столі",
    "installer-quick-launch-bar": "у меню швидкого запуску",
    "installer-automatic-updates": "Перевіряти оновлення автоматично",
    "installer-uninstall-configuration": "Видалити файл налаштувань.",

    # Client notifications
    "config-cleared-notification": "Налаштування скинуто. Зміни набудуть чинності після збереження коректної конфігурації.",

    "relative-config-notification": "Завантажено файли відносної конфігурації: {}",

    "connection-attempt-notification": "Підключення до {}:{}",  # Port, IP
    "reconnection-attempt-notification": "З'єднання з сервером втрачено, перепідключення",
    "disconnection-notification": "Відключилися від сервера",
    "connection-failed-notification": "Не вдалося підключитися до сервера",
    "connected-successful-notification": "З'єднання з сервером встановлено",
    "retrying-notification": "%s, наступна спроба через %d секунд(и)...",  # Seconds
    "reachout-successful-notification": "Підключення до {} ({}) успішне",

    "rewind-notification": "Перемотано через різницю в часі з {}",  # User
    "fastforward-notification": "Прискорено через різницю в часі з {}",  # User
    "slowdown-notification": "Відтворення сповільнено через різницю в часі з {}",  # User
    "revert-notification": "Повертаємося до нормальної швидкості відтворення",

    "pause-notification": "{} призупинив відтворення ({})",  # User, Time
    "unpause-notification": "{} відновив відтворення",  # User
    "seek-notification": "{} перемотав з {} на {}",  # User, from time, to time

    "current-offset-notification": "Поточне зміщення: {} секунд(и)",  # Offset

    "media-directory-list-updated-notification": "Папки відтворення оновлено.",

    "room-join-notification": "{} зайшов у кімнату: '{}'",  # User
    "left-notification": "{} залишив кімнату",  # User
    "left-paused-notification": "{} залишив кімнату, {} призупинив відтворення",  # User who left, User who paused
    "playing-notification": "{} увімкнув '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum": " у кімнаті: '{}'",  # Room

    "not-all-ready": "Не готові: {}",  # Usernames
    "all-users-ready": "Усі глядачі готові ({} ос.)",  # Number of ready users
    "ready-to-unpause-notification": "Ви позначені як готовий — натисніть ще раз, щоб продовжити відтворення",
    "set-as-ready-notification": "Ви позначені як готовий",
    "set-as-not-ready-notification": "Ви позначені як неготовий",
    "autoplaying-notification": "Автовідтворення через {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Ідентифікація як оператора кімнати з паролем '{}'...",
    "failed-to-identify-as-controller-notification": "{} не пройшов ідентифікацію як оператор кімнати.",
    "authenticated-as-controller-notification": "{} увійшов як оператор кімнати.",
    "created-controlled-room-notification": "Створено керовану кімнату '{}' з паролем '{}'. Збережіть ці дані!\n\nУ керованих кімнатах усіх синхронізують з оператором(-ами) кімнати, лише у яких є права ставити та знімати з паузи, перемотувати та змінювати список відтворення.\n\nПопросіть звичайних глядачів підключитися до кімнати '{}', а оператори можуть підключитися до кімнати '{}', щоб автоматично авторизуватися.", # RoomName, operatorPassword, roomName, roomName:operatorPassword

    "other-set-as-ready-notification": "{} був позначений як готовий користувачем {}",  # User set as ready, user who set them as ready
    "other-set-as-not-ready-notification": "{} був позначений як неготовий користувачем {}", # User set as not ready, user who set them as not ready

    "file-different-notification": "Ймовірно, файл, який ви дивитесь, відрізняється від того, який дивиться {}.",  # User
    "file-differences-notification": "Ваш файл відрізняється: {}",  # Differences
    "room-file-differences": "Невідповідності файлу: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "ім'я",
    "file-difference-filesize": "розмір",
    "file-difference-duration": "тривалість",
    "alone-in-the-room": "У кімнаті, окрім вас, нікого немає.",

    "different-filesize-notification": " (розмір вашого файлу не збігається з розміром їхнього файлу!)",
    "userlist-playing-notification": "{} дивиться:",  # Username
    "file-played-by-notification": "Файл: {} переглядають:",  # File
    "no-file-played-notification": "{} не дивиться нічого",  # Username
    "notplaying-notification": "Люди, які не переглядають нічого:",
    "userlist-room-notification": "У кімнаті '{}':",  # Room
    "userlist-file-notification": "Файл",
    "controller-userlist-userflag": "Оператор",
    "ready-userlist-userflag": "Готовий",

    "update-check-failed-notification": "Неможливо автоматично перевірити, що версія Syncplay {} все ще актуальна. Хочете зайти на https://syncplay.pl/ і вручну перевірити наявність оновлень?",
    "syncplay-uptodate-notification": "У вас остання версія Syncplay",
    "syncplay-updateavailable-notification": "Доступна нова версія Syncplay. Хочете відкрити сторінку релізу?",

    "mplayer-file-required-notification": "Для використання Syncplay з mplayer необхідно передати файл як параметр",
    "mplayer-file-required-notification/example": "Приклад використання: syncplay [options] [url|path/]filename",
    "mplayer2-required": "Syncplay несумісний з MPlayer 1.x, будь ласка, використовуйте mplayer2 або mpv",

    "unrecognized-command-notification": "Невідома команда.",
    "commandlist-notification": "Доступні команди:",
    "commandlist-notification/room": "\tr [ім'я кімнати] - змінити кімнату",
    "commandlist-notification/list": "\tl - показати список користувачів",
    "commandlist-notification/undo": "\tu - скасувати останню перемотку",
    "commandlist-notification/pause": "\tp - увімк./вимк. паузу",
    "commandlist-notification/seek": "\t[s][+-]time - перемотати до заданого моменту часу, якщо не вказано + або -, то час вважається абсолютним (від початку файлу) у секундах або хв:сек",
    "commandlist-notification/offset": "\to[+-]duration - змістити локальне відтворення на задану тривалість (у секундах або хв:сек) від позиції перемотки сервера - це застаріла функція",
    "commandlist-notification/help": "\th - допомога",
    "commandlist-notification/toggle": "\tt - перемкнути статус готовий/не готовий до перегляду",
    "commandlist-notification/setready": "\tsr [ім'я] - позначити користувача як готового",
    "commandlist-notification/setnotready": "\tsn [ім'я] - позначити користувача як неготового",
    "commandlist-notification/create": "\tc [ім'я кімнати] - створити керовану кімнату з таким самим ім'ям, як у поточної",
    "commandlist-notification/auth": "\ta [пароль] - авторизуватися як оператор кімнати за допомогою пароля",
    "commandlist-notification/chat": "\tch [повідомлення] - надіслати повідомлення в кімнату",
    "commandList-notification/queue": "\tqa [файл/URL] - додати файл або URL у кінець списку відтворення",
    "commandList-notification/queueandselect": "\tqas [файл/url] - додати файл або url у кінець списку відтворення та виділити його",
    "commandList-notification/playlist": "\tql - показати поточний список відтворення",
    "commandList-notification/select": "\tqs [індекс] - виділити вказаний пункт у списку відтворення",
    "commandList-notification/next": "\tqn - виділити наступний пункт у списку відтворення",
    "commandList-notification/delete": "\tqd [індекс] - видалити вказаний пункт зі списку відтворення",
    "syncplay-version-notification": "Версія Syncplay: {}",  # syncplay.version
    "more-info-notification": "Більше інформації на {}",  # projectURL

    "gui-data-cleared-notification": "Syncplay очистив шлях та інформацію про стан вікна, використаного GUI.",
    "language-changed-msgbox-label": "Мова зміниться при наступному запуску Syncplay.",
    "promptforupdate-label": "Дозволити Syncplay періодично перевіряти наявність оновлень?",

    "media-player-latency-warning": "Увага: у програвача занадто велика затримка ({} секунд). Якщо помітите проблеми з синхронізацією, закрийте ресурсомісткі програми. Якщо не допоможе, спробуйте інший програвач.",  # Seconds to respond
    "mpv-unresponsive-error": "mpv не відповідає {} секунд, очевидно, стався збій. Будь ласка, перезапустіть Syncplay.",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "Для виходу натисніть \"Enter\"\n",

    # Client errors
    "missing-arguments-error": "Деякі необхідні аргументи відсутні, зверніться до --help",
    "server-timeout-error": "Підключення до сервера перевищило ліміт часу",
    "mpc-slave-error": "Неможливо запустити MPC у режимі slave!",
    "mpc-version-insufficient-error": "Версія MPC занадто стара, будь ласка, використовуйте `mpc-hc` >= `{}`",
    "mpc-be-version-insufficient-error": "Версія MPC занадто стара, будь ласка, використовуйте `mpc-be` >= `{}`",
    "mpv-version-error": "Syncplay несумісний з даною версією mpv. Будь ласка, використовуйте іншу версію mpv (бажано найновішу).",
    "mpv-failed-advice": "Можливо, mpv не може запуститися через непідтримувані параметри командного рядка або непідтримувану версію mpv.",
    "player-file-open-error": "Програвач не може відкрити файл.",
    "player-path-error": "Шлях до програвача встановлено неправильно. Підтримувані програвачі: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 та IINA.",
    "hostname-empty-error": "Ім'я користувача не може бути порожнім.",
    "empty-error": "{} не може бути порожнім.",  # Configuration
    "media-player-error": "Помилка програвача: \"{}\"",  # Error line
    "unable-import-gui-error": "Неможливо імпортувати бібліотеки графічного інтерфейсу. Необхідно встановити правильну версію PySide, інакше графічний інтерфейс не працюватиме. Якщо ви хочете запустити Syncplay у консольному режимі, запустіть його з параметром командного рядка --no-gui. Дивіться https://syncplay.pl/guide/ для отримання додаткової інформації.",
    "unable-import-twisted-error": "Неможливо імпортувати Twisted. Встановіть Twisted 16.4.0 або пізнішу версію.",

    "arguments-missing-error": "Деякі необхідні аргументи відсутні, зверніться до --help",

    "unable-to-start-client-error": "Неможливо запустити клієнт",

    "player-path-config-error": "Шлях до програвача встановлено неправильно. Підтримувані програвачі: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 та IINA.",
    "no-file-path-config-error": "Файл має бути вказаний до увімкнення програвача",
    "no-hostname-config-error": "Адреса сервера не може бути порожньою",
    "invalid-port-config-error": "Неправильний номер порту",
    "empty-value-config-error": "Поле '{}' не може бути порожнім",  # Config option

    "not-json-error": "Не є закодованим json-рядком\n",
    "hello-arguments-error": "Не вистачає аргументів Hello\n",
    "version-mismatch-error": "Конфлікт версій між клієнтом і сервером\n",
    "vlc-failed-connection": "Помилка підключення до VLC. Якщо у вас не встановлено syncplay.lua, зверніться до https://syncplay.pl/LUA/ за інструкціями. Наразі Syncplay несумісний з VLC 4, тому використовуйте VLC 3 або інший програвач, наприклад, mpv.",
    "vlc-failed-noscript": "VLC повідомляє, що скрипт інтерфейсу syncplay.lua не встановлено. Будь ласка, зверніться до https://syncplay.pl/LUA/ за інструкціями.",
    "vlc-failed-versioncheck": "Дана версія VLC не підтримується Syncplay. Будь ласка, використовуйте VLC версії 2 або вище.",
    "vlc-initial-warning": 'VLC не завжди надає точну інформацію про позицію відтворення, особливо для файлів з розширеннями mp4 та avi. Якщо виникли проблеми з перемоткою, спробуйте інший програвач, наприклад, <a href="https://mpv.io/">mpv</a> (або <a href="https://github.com/stax76/mpv.net/">mpv.net</a> для Windows).',

    "feature-sharedPlaylists": "спільний список відтворення",  # used for not-supported-by-server-error
    "feature-chat": "чат",  # used for not-supported-by-server-error
    "feature-readiness": "готовність",  # used for not-supported-by-server-error
    "feature-managedRooms": "керовані кімнати",  # used for not-supported-by-server-error
    "feature-setOthersReadiness": "перевизначення готовності",  # used for not-supported-by-server-error

    "not-supported-by-server-error": "Можливість '{}' не підтримується сервером.",  # feature
    "shared-playlists-not-supported-by-server-error": "Спільні списки відтворення можуть не підтримуватися сервером. Для коректної роботи потрібен сервер Syncplay {}+, ви підключені до сервера Syncplay {}.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "Спільний список відтворення вимкнено сервером. Щоб використовувати цю можливість, підключіться до іншого сервера.",

    "invalid-seek-value": "Некоректне значення для перемотки",
    "invalid-offset-value": "Некоректне зміщення",

    "switch-file-not-found-error": "Неможливо знайти файл '{0}'. Перевірте папки відтворення.",  # File not found
    "folder-search-timeout-error": "Пошук файлу було перервано в папці '{}'. Це може статися через велику кількість підпапок (після обробки перших {} файлів). Для коректної роботи пошуку файлів скористайтеся випадаючим меню Файл->Папки відтворення та видаліть дану папку зі списку або замініть її на потрібну підпапку. Якщо насправді з папкою все гаразд, ви можете знову її увімкнути через випадаюче меню Файл->Папки відтворення.", # Folder, Files processed
    "folder-search-timeout-warning": "Попередження: Сканування {:,} файлів у папці '{}' зайняло {} секунд. Це може статися, якщо ви оберете папку з надто великою кількістю підпапок у списку папок відтворення для пошуку або якщо буде занадто багато файлів для обробки.",  # Folder, Files processed. Note: {:,} is {} but with added commas separators.
    "folder-search-first-file-timeout-error": "Пошук файлу в '{}' було перервано, оскільки неможливо відкрити каталог. Це може статися, якщо це мережевий диск або диск перейшов у режим економії енергії. Для коректної роботи пошуку файлів скористайтеся випадаючим меню Файл->Папки відтворення та видаліть дану папку, або вирішіть проблему, змінивши параметри енергозбереження.",  # Folder
    "added-file-not-in-media-directory-error": "Ви відкрили файл з '{}', який не значиться в папках відтворення. Ви можете додати його через випадаюче меню Файл->Папки відтворення.",  # Folder
    "no-media-directories-error": "Ви не вказали папки відтворення. Для коректної роботи скористайтеся випадаючим меню Файл->Папки відтворення та вкажіть потрібні каталоги.",
    "cannot-find-directory-error": "Не вдалося знайти папку відтворення '{}'. Щоб оновити список папок, скористайтеся випадаючим меню Файл->Папки відтворення та вкажіть потрібні каталоги.",

    "failed-to-load-server-list-error": "Не вдалося завантажити список публічних серверів. Відкрийте https://www.syncplay.pl/ через браузер.",

    # Client arguments
    "argument-description": 'Рішення для синхронного відтворення у VLC, MPlayer або MPC-HC/BE через Інтернет.',
    "argument-epilog": 'Якщо параметр не буде передано, то буде використовуватися значення, вказане в _config.',
    "nogui-argument": 'не використовувати GUI',
    "host-argument": 'адреса сервера',
    "name-argument": 'бажане ім\'я користувача',
    "debug-argument": 'режим налагодження',
    "force-gui-prompt-argument": 'показати вікно налаштування',
    "no-store-argument": 'не зберігати дані в .syncplay',
    "room-argument": 'початкова кімната',
    "password-argument": 'пароль для доступу до сервера',
    "player-path-argument": 'шлях до виконуваного файлу програвача',
    "file-argument": 'файл для відтворення',
    "args-argument": 'параметри програвача; якщо потрібно передати параметри, що починаються з - , то спочатку пишіть \'--\'',
    "clear-gui-data-argument": 'скидає шлях та дані про стан вікна GUI, що зберігаються як QSettings',
    "language-argument": 'мова повідомлень Syncplay ({})', # Languages

    "version-argument": 'виводить номер версії',
    "version-message": "Ви використовуєте Syncplay версії {} ({})",

    "load-playlist-from-file-argument": "завантажує список відтворення з текстового файлу (один пункт на рядок)",

    # Client labels
    "config-window-title": "Налаштування Syncplay",

    "connection-group-title": "Підключення",
    "host-label": "Адреса сервера: ",
    "name-label": "Ім'я користувача (не обов'язково):",
    "password-label": "Пароль сервера (якщо потрібен):",
    "room-label": "Кімната:",
    "roomlist-msgbox-label": "Редагувати список кімнат (одна на рядок)",

    "media-setting-title": "Відтворення",
    "executable-path-label": "Шлях до програвача:",
    "media-path-label": "Шлях до відеофайлу (не обов'язковий):",
    "player-arguments-label": "Аргументи запуску програвача:",
    "browse-label": "Вибрати",
    "update-server-list-label": "Оновити список",

    "more-title": "Більше налаштувань",
    "never-rewind-value": "Ніколи",
    "seconds-suffix": " секунд(и)",
    "privacy-sendraw-option": "надс. як є",
    "privacy-sendhashed-option": "надс. хеш",
    "privacy-dontsend-option": "не надс.",
    "filename-privacy-label": "Ім'я файлу:",
    "filesize-privacy-label": "Розмір файлу:",
    "checkforupdatesautomatically-label": "Перевіряти оновлення автоматично",
    "autosavejoinstolist-label": "Додавати кімнати, до яких ви підключаєтесь, у список кімнат",
    "slowondesync-label": "Сповільнювати при невеликих розсинхронізаціях (не підтримується в MPC-HC/BE)",
    "rewindondesync-label": "Перемотка при великих розсинхронізаціях (настійно рекомендується)",
    "dontslowdownwithme-label": "Ніколи не сповільнювати та не перемотувати відео іншим (функція тестується)",
    "pausing-title": "Призупинення",
    "pauseonleave-label": "Призупиняти, коли хтось іде (наприклад, відключається)",
    "readiness-title": "Готовність",
    "readyatstart-label": "Виставити статус 'Я готовий' за замовчуванням",
    "fastforwardondesync-label": "Прискорювати відео при відставанні (рекомендується)",
    "forceguiprompt-label": "Не завжди показувати вікно налаштування Syncplay",  # (Inverted)
    "showosd-label": "Увімкнути екранні повідомлення (поверх відео)",

    "showosdwarnings-label": "Показувати попередження (напр., коли файли не збігаються)",
    "showsameroomosd-label": "Показувати події вашої кімнати",
    "shownoncontrollerosd-label": "Увімкнути події, пов'язані з не-операторами в керованій кімнаті.",
    "showdifferentroomosd-label": "Показувати події інших кімнат",
    "showslowdownosd-label": "Показувати сповіщення про сповільнення/перемотку",
    "language-label": "Мова:",
    "automatic-language": "За замовчуванням ({})",  # Automatic language
    "showdurationnotification-label": "Попереджати про невідповідність тривалості відео",
    "showplaylistskipwarnings-label": "Попереджати, якщо список відтворення може пропускати непереглянуті файли",
    "showplaylistskipwarnings-tooltip": "Показувати попередження, коли Syncplay вважає, що список відтворення пропускає файли, які ще не були переглянуті.",
    "showplaylistorderwarnings-label": "Попереджати, якщо файли в списку відтворення виглядають розташованими не за порядком",
    "showplaylistorderwarnings-tooltip": "Показувати попередження, коли Syncplay вважає, що файли в списку відтворення можуть бути в неправильному порядку.",
    "basics-label": "Основне",
    "readiness-label": "Поведінка",
    "misc-label": "Приватність/Інше",
    "core-behaviour-title": "Інформація про файли",
    "syncplay-internals-title": "Системні налаштування",
    "syncplay-mediasearchdirectories-title": "Папки відтворення",
    "syncplay-mediasearchdirectories-label": "Папки відтворення (один шлях на рядок)",
    "sync-label": "Синхронізація",
    "sync-otherslagging-title": "Випередження",
    "sync-youlaggging-title": "Відставання",
    "messages-label": "Повідомлення",
    "messages-osd-title": "Налаштування OSD",
    "messages-other-title": "Інші налаштування відображення",
    "chat-label": "Чат",
    "privacy-label": "Приватність",
    "privacy-title": "Налаштування приватності",
    "unpause-title": "Якщо ви стартуєте, то:",
    "unpause-ifalreadyready-option": "Зняти паузу, якщо вже готовий",
    "unpause-ifothersready-option": "Зняти паузу, якщо ви та решта в кімнаті готові (за замовчуванням)",
    "unpause-ifminusersready-option": "Зняти паузу, якщо всі в кімнаті готові та присутній мінімум глядачів",
    "unpause-always": "Завжди знімати паузу",
    "syncplay-trusteddomains-title": "Довірені сайти (стрім-сервіси, відеохостинги, файли в мережі)",
    "addtrusteddomain-menu-label": "Додати {} як довірений сайт",  # Domain

    "chat-title": "Введення повідомлень чату",
    "chatinputenabled-label": "Дозволити введення повідомлень у mpv (за допомогою клавіші 'Enter')",
    "chatdirectinput-label": "Дозволити миттєве введення повідомлень (без необхідності натискати 'Enter', щоб надіслати повідомлення)",
    "chatinputfont-label": "Шрифт для поля введення повідомлень",
    "chatfont-label": "Встановити шрифт",
    "chatcolour-label": "Встановити колір",
    "chatinputposition-label": "Позиція поля введення повідомлення в mpv",
    "chat-top-option": "Вгорі",
    "chat-middle-option": "Посередині",
    "chat-bottom-option": "Внизу",
    "chatoutputheader-label": "Виведення повідомлень чату",
    "chatoutputfont-label": "Шрифт повідомлень чату",
    "chatoutputenabled-label": "Дозволити виведення повідомлень у програвачі (поки що лише в mpv)",
    "chatoutputposition-label": "Режим виведення",
    "chat-chatroom-option": "Режим чату",
    "chat-scrolling-option": "Режим прокрутки",

    "mpv-key-tab-hint": "[TAB] - увімкнути або вимкнути гарячі клавіші mpv.",
    "mpv-key-hint": "[ENTER] - надіслати повідомлення. [ESC] - вийти з режиму чату.",
    "alphakey-mode-warning-first-line": "Зараз можна використовувати гарячі клавіші mpv, натискаючи a-z.",
    "alphakey-mode-warning-second-line": "Натисніть [TAB], щоб повернутися в режим чату.",

    "help-label": "Допомога",
    "reset-label": "Скидання налаштувань",
    "run-label": "Запустити",
    "storeandrun-label": "Зберегти та запустити",

    "contact-label": "Є ідея, знайшли помилку або хочете залишити відгук? Пишіть на <a href=\"mailto:dev@syncplay.pl\">dev@syncplay.pl</a> або <a href=\"https://github.com/Syncplay/syncplay/issues\">задавайте питання через GitHub</a> / <a href=\"https://github.com/Syncplay/syncplay/discussions\"><nobr>почніть обговорення</nobr></a>, щоб зробити пропозицію або поставити запитання через GitHub. Крім того, заходьте на <a href=\"https://syncplay.pl/\">www.syncplay.pl</a> за інформацією, допомогою та оновленнями! Не використовуйте Syncplay для передачі конфіденційної інформації.",

    "joinroom-label": "Зайти в кімнату",
    "joinroom-menu-label": "Зайти в кімнату {}",
    "seektime-menu-label": "Пере&мотати",
    "undoseek-menu-label": "&Скасувати перемотку",
    "play-menu-label": "&Старт",
    "pause-menu-label": "&Пауза",
    "playbackbuttons-menu-label": "&Показувати кнопки керування",
    "autoplay-menu-label": "Показувати кнопку &автовідтворення",
    "autoplay-guipushbuttonlabel": "Стартувати, коли всі будуть готові",
    "autoplay-minimum-label": "Мінімум глядачів:",
    "hideemptyrooms-menu-label": "Приховати порожні постійні кімнати",
    "sendmessage-label": "Надіслати",

    "ready-guipushbuttonlabel": "Я готовий",

    "roomuser-heading-label": "Кімната/Глядач",

    "size-heading-label": "Розмір",
    "duration-heading-label": "Час",
    "filename-heading-label": "Ім'я файлу",
    "notifications-heading-label": "Сповіщення",
    "userlist-heading-label": "Хто що дивиться",

    "browseformedia-label": "Вибрати файл",

    "file-menu-label": "&Файл",  # & precedes shortcut key
    "openmedia-menu-label": "&Відкрити файл",
    "openstreamurl-menu-label": "Відкрити &посилання",
    "setmediadirectories-menu-label": "&Папки відтворення",
    "loadplaylistfromfile-menu-label": "&Завантажити список відтворення з файлу",
    "saveplaylisttofile-menu-label": "&Зберегти список відтворення у файл",
    "exit-menu-label": "&Вихід",
    "advanced-menu-label": "&Додатково",
    "window-menu-label": "&Вигляд",
    "setoffset-menu-label": "&Встановити зміщення",
    "createcontrolledroom-menu-label": "Створити керовану &кімнату",
    "identifyascontroller-menu-label": "&Увійти як оператор кімнати",
    "settrusteddomains-menu-label": "Довірені &сайти",

    # Edit menu
    "edit-menu-label": "&Редагування",
    "cut-menu-label": "Ви&різати",
    "copy-menu-label": "&Копіювати",
    "paste-menu-label": "&Вставити",
    "selectall-menu-label": "Ви&брати все",

    "playback-menu-label": "&Керування",

    "help-menu-label": "&Допомога",
    "userguide-menu-label": "&Посібник користувача",
    "update-menu-label": "Перевірити &оновлення",

    "startTLS-initiated": "Спроба встановити безпечне з'єднання",
    "startTLS-secure-connection-ok": "Безпечне з'єднання встановлено ({})",
    "startTLS-server-certificate-invalid": 'Не вдалося встановити безпечне з\'єднання. Сервер використовує некоректний сертифікат безпеки. Комунікація з сервером може бути перехоплена третіми особами. Подробиці та способи усунення проблеми <a href="https://syncplay.pl/trouble">тут</a>.',
    "startTLS-server-certificate-invalid-DNS-ID": "Syncplay не довіряє цьому серверу, тому що сервер використовує сертифікат безпеки, не призначений для даної адреси.",
    "startTLS-not-supported-client": "Клієнт не підтримує TLS",
    "startTLS-not-supported-server": "Сервер не підтримує TLS",

    "tls-information-title": "Подробиці сертифіката",
    "tls-dialog-status-label": "<strong>Syncplay використовує зашифроване з'єднання з {}.</strong>",
    "tls-dialog-desc-label": "Шифрування за допомогою цифрового сертифіката дозволяє не розголошувати<br/>інформацію під час передачі даних на сервер {} та з нього.",
    "tls-dialog-connection-label": "Інформація зашифрована за допомогою Transport Layer Security (TLS)<br/>версії {} шифром {}.",
    "tls-dialog-certificate-label": "Сертифікат виданий {}, дійсний до {}.",

    "about-menu-label": "&Про Syncplay",
    "about-dialog-title": "Про Syncplay",
    "about-dialog-release": "Версія {}, випуск {}",
    "about-dialog-license-text": "Ліцензовано на умовах Apache&nbsp;License,&nbsp;Version 2.0",
    "about-dialog-license-button": "Ліцензія",
    "about-dialog-dependencies": "Залежності",

    "setoffset-msgbox-label": "Встановити зміщення",
    "offsetinfo-msgbox-label": "Зміщення (див. інструкцію на сторінці www.syncplay.pl/guide):",

    "promptforstreamurl-msgbox-label": "Відкрити посилання",
    "promptforstreamurlinfo-msgbox-label": "Посилання:",

    "addfolder-label": "Додати папку",

    "adduris-msgbox-label": "Список посилань (одне на рядок)",
    "editplaylist-msgbox-label": "Список відтворення (один пункт на рядок)",
    "trusteddomains-msgbox-label": "Список довірених сайтів для автоматичного відтворення (один на рядок)",

    "createcontrolledroom-msgbox-label": "Створити керовану кімнату",
    "controlledroominfo-msgbox-label": "Введіть ім'я керованої кімнати\r\n(див. інструкцію на сторінці www.syncplay.pl/guide):",

    "identifyascontroller-msgbox-label": "Увійти як оператор кімнати",
    "identifyinfo-msgbox-label": "Введіть пароль оператора кімнати\r\n(див. інструкцію на сторінці www.syncplay.pl/guide):",

    "public-server-msgbox-label": "Виберіть публічний сервер для даної сесії",

    "megabyte-suffix": " МБ",  # Technically it is a mebibyte


    # Tooltips
    "host-tooltip": "Ім'я або IP-адреса, до якої буде здійснено підключення, може містити номер порту (напр., syncplay.pl:8999). Синхронізація можлива лише в межах одного сервера/порту.",
    "name-tooltip": "Ім'я, під яким ви будете відомі. Реєстрація не потрібна, тому ім'я можна легко змінити в будь-який момент. Якщо залишити порожнім, буде згенеровано випадкове ім'я.",
    "password-tooltip": "Паролі потрібні для підключення до приватних серверів.",
    "room-tooltip": "Кімната, в яку ви потрапите одразу після підключення. Синхронізація можлива лише між людьми в одній і тій самій кімнаті.",

    "edit-rooms-tooltip": "Редагувати список кімнат.",

    "executable-path-tooltip": "Розташування програвача (mpv, mpv.net, VLC, MPC-HC/BE, mplayer2 або IINA).",
    "media-path-tooltip": "Розташування відеофайлу або потоку для перегляду. Обов'язково для mplayer2.",
    "player-arguments-tooltip": "Передавати додаткові аргументи командного рядка цьому програвачу.",
    "mediasearcdirectories-arguments-tooltip": "Папки, де Syncplay буде шукати медіафайли, включаючи підпапки.",

    "more-tooltip": "Показати додаткові налаштування.",
    "filename-privacy-tooltip": "Режим приватності для передачі імені файлу, що відтворюється, на сервер.",
    "filesize-privacy-tooltip": "Режим приватності для передачі розміру файлу, що відтворюється, на сервер.",
    "privacy-sendraw-tooltip": "Надсилає цю інформацію без шифрування. Рекомендована опція з найбільшою функціональністю.",
    "privacy-sendhashed-tooltip": "Надсилає хеш-суму цієї інформації, роблячи її невидимою для інших користувачів.",
    "privacy-dontsend-tooltip": "Не надсилати цю інформацію на сервер. Надає найбільшу приватність.",
    "checkforupdatesautomatically-tooltip": "Syncplay буде регулярно заходити на сайт і перевіряти наявність нових версій.",
    "autosavejoinstolist-tooltip": "Автоматично запам'ятовувати назву кімнати у списку при підключенні до кімнати.",
    "slowondesync-tooltip": "Тимчасово зменшити швидкість відтворення з метою синхронізації з іншими глядачами. Не підтримується в MPC-HC/BE.",
    "dontslowdownwithme-tooltip": "Ваше відставання не впливатиме на інших глядачів.",
    "pauseonleave-tooltip": "Призупинити відтворення, якщо ви залишили кімнату або хтось із глядачів відключився від сервера.",
    "readyatstart-tooltip": "Позначити вас як готового до перегляду одразу ж (за замовчуванням ви позначені не готовим)",
    "forceguiprompt-tooltip": "Вікно налаштування не буде відображатися при відкритті файлу в Syncplay.",  # (Inverted)
    "nostore-tooltip": "Запустити Syncplay з даною конфігурацією, але не зберігати зміни назавжди.",
    "rewindondesync-tooltip": "Перемотувати назад, коли це необхідно для синхронізації. Вимкнення цієї опції може призвести до великих розсинхронізацій!",
    "fastforwardondesync-tooltip": "Перемотувати вперед при розсинхронізації з оператором кімнати (або якщо увімкнено опцію 'Ніколи не сповільнювати та не перемотувати відео іншим').",
    "showosd-tooltip": "Надсилати повідомлення Syncplay у відеопрогравач і відображати їх поверх відео (OSD - On Screen Display).",
    "showosdwarnings-tooltip": "Показувати OSD-попередження, якщо відтворюються різні файли або якщо ви в кімнаті більше нікого немає.",
    "showsameroomosd-tooltip": "Показувати OSD-сповіщення про події, що стосуються кімнати, в якій ви перебуваєте.",
    "shownoncontrollerosd-tooltip": "Показувати OSD-сповіщення про події, що стосуються не-операторів у керованій кімнаті.",
    "showdifferentroomosd-tooltip": "Показувати OSD-сповіщення про події, що стосуються будь-яких інших кімнат.",
    "showslowdownosd-tooltip": "Показувати сповіщення про сповільнення або перемотку з метою синхронізації.",
    "showdurationnotification-tooltip": "Корисно, коли сегмент складеного файлу відсутній. Можливі хибні спрацювання.",
    "language-tooltip": "Мова, що використовується Syncplay.",
    "unpause-always-tooltip": "Коли ви стартуєте, статус зміниться на готовий і почнеться відтворення, а не просто зміна статусу.",
    "unpause-ifalreadyready-tooltip": "Коли ви стартуєте не готовим, це змінює статус на готовий - натисніть старт ще раз для початку відтворення.",
    "unpause-ifothersready-tooltip": "Коли ви стартуєте не готовим, відтворення почнеться, якщо решта готові.",
    "unpause-ifminusersready-tooltip": "Коли ви стартуєте не готовим, відтворення почнеться, якщо решта готові та присутня достатня кількість глядачів.",
    "trusteddomains-arguments-tooltip": "Сайти, які дозволені для автоматичного відтворення зі спільного списку відтворення.",

    "chatinputenabled-tooltip": "Дозволити введення повідомлень у mpv (натисніть 'Enter', щоб ввести повідомлення, 'Enter', щоб надіслати, 'Escape', щоб скасувати)",
    "chatdirectinput-tooltip": "Не вимагати натискати 'Enter' для введення повідомлень у mpv. Натисніть 'Tab', щоб тимчасово вимкнути цю можливість.",
    "font-label-tooltip": "Шрифт для введення повідомлень у mpv. Налаштування на стороні клієнта, тому не впливає на те, що бачать інші.",
    "set-input-font-tooltip": "Шрифт для введення повідомлень у mpv. Налаштування на стороні клієнта, тому не впливає на те, що бачать інші.",
    "set-input-colour-tooltip": "Колір шрифту для введення повідомлень у mpv. Налаштування на стороні клієнта, тому не впливає на те, що бачать інші.",
    "chatinputposition-tooltip": "Розташування поля введення повідомлень, яке з'являється, якщо натиснути 'Enter' і почати набирати повідомлення.",
    "chatinputposition-top-tooltip": "Розмістити введення повідомлень угорі вікна mpv.",
    "chatinputposition-middle-tooltip": "Розмістити введення повідомлень у центрі вікна mpv.",
    "chatinputposition-bottom-tooltip": "Розмістити введення повідомлень унизу вікна mpv.",
    "chatoutputenabled-tooltip": "Показувати повідомлення у програвачі (якщо підтримується програвачем).",
    "font-output-label-tooltip": "Шрифт для виведення повідомлень чату.",
    "set-output-font-tooltip": "Шрифт для відображення повідомлень у чаті.",
    "chatoutputmode-tooltip": "Як відображаються повідомлення в чаті.",
    "chatoutputmode-chatroom-tooltip": "Показувати нові повідомлення під попереднім повідомленням.",
    "chatoutputmode-scrolling-tooltip": "Прокручувати повідомлення в чаті справа наліво.",

    "help-tooltip": "Відкрити Посібник Користувача на Syncplay.pl.",
    "reset-tooltip": "Скидає всі налаштування Syncplay у початковий стан.",
    "update-server-list-tooltip": "Оновити список публічних серверів від syncplay.pl.",

    "sslconnection-tooltip": "Встановлено безпечне з'єднання з сервером. Натисніть, щоб побачити подробиці сертифіката.",

    "joinroom-tooltip": "Покинути кімнату та зайти в іншу, вказану кімнату.",
    "seektime-msgbox-label": "Перемотати до певного моменту часу (вказувати в секундах або хв:сек). Використовуйте +/-, щоб перемотати вперед/назад відносно теперішнього моменту.",
    "ready-tooltip": "Показує, чи готові ви до перегляду чи ні.",
    "autoplay-tooltip": "Автоматичне відтворення, коли всі користувачі з індикаторами готовності будуть готові та присутня достатня кількість глядачів.",
    "switch-to-file-tooltip": "Клікніть двічі для відтворення {}",  # Filename
    "sendmessage-tooltip": "Надіслати повідомлення в кімнату",

    # In-userlist notes (GUI)
    "differentsize-note": "Розмір файлу не збігається!",
    "differentsizeandduration-note": "Розмір і тривалість файлу не збігаються!",
    "differentduration-note": "Тривалість файлу не збігається!",
    "nofile-note": "(Жодний файл не відтворюється)",

    # Server messages to client
    "new-syncplay-available-motd-message": "Ви використовуєте Syncplay версії {}. На https://syncplay.pl/ доступна новіша версія.",  # ClientVersion
    "persistent-rooms-notice": "УВАГА: Цей сервер використовує постійні кімнати, це означає, що інформація списку відтворення зберігається між сеансами відтворення. Якщо ви хочете створити кімнату, в якій інформація не зберігається, поставте -temp у кінці назви кімнати.",
    "ready-chat-message": "Я позначив {} як готового.",  # User
    "not-ready-chat-message": "Я позначив {} як неготового.",  # User

    # Server notifications
    "welcome-server-notification": "Ласкаво просимо на сервер Syncplay версії {0}",  # version
    "client-connected-room-server-notification": "{0}({2}) підключився до кімнати '{1}'",  # username, host, room
    "client-left-server-notification": "{0} залишив сервер",  # name
    "no-salt-notification": "УВАГА: Щоб згенеровані сервером паролі операторів кімнат працювали після перезавантаження сервера, необхідно вказати наступний аргумент командного рядка при запуску сервера Syncplay: --salt {}",  # Salt

    # Server arguments
    "server-argument-description": 'Рішення для синхронного відтворення у VLC, MPlayer або MPC-HC/BE через Інтернет. Серверна частина',
    "server-argument-epilog": 'Якщо параметр не буде передано, то буде використовуватися значення, вказане в _config.',
    "server-port-argument": 'номер TCP порту сервера',
    "server-password-argument": 'пароль сервера',
    "server-isolate-room-argument": 'чи повинні кімнати бути ізольованими?',
    "server-salt-argument": "генерувати паролі до керованих кімнат на основі вказаного рядка (солі)",
    "server-disable-ready-argument": "вимкнути статуси готовності",
    "server-motd-argument": "шлях до файлу, з якого буде вилучатися MOTD-повідомлення",
    "server-rooms-argument": "шлях до файлу бази даних для використання та/або створення сховища постійних даних про кімнату. Дозволяє кімнатам зберігатися без глядачів, а також після перезапусків",
    "server-permanent-rooms-argument": "шлях до файлу зі списком постійних кімнат, які будуть перелічені, навіть якщо кімната порожня (у вигляді текстового файлу, в якому вказана одна кімната на рядок) - потрібно, щоб постійні кімнати були увімкнені",
    "server-chat-argument": "Чи повинен чат бути вимкнений?",
    "server-chat-maxchars-argument": "Максимальна кількість символів у повідомленнях у чаті (за замовчуванням {})",
    "server-maxusernamelength-argument": "Максимальна кількість символів в іменах користувачів (за замовчуванням {})",
    "server-stats-db-file-argument": "Увімкнути статистику сервера у вказаному файлі SQLite",
    "server-startTLS-argument": "Увімкнути TLS-з'єднання, використовуючи файли сертифікатів у вказаному шляху",
    "server-messed-up-motd-unescaped-placeholders": "MOTD-повідомлення містить неекрановані спецсимволи. Усі знаки $ повинні бути продубльовані ($$).",
    "server-messed-up-motd-too-long": "MOTD-повідомлення занадто довге: максимальна довжина - {} символ(ів), поточна довжина - {} символ(ів).",
    "server-listen-only-on-ipv4": "Слухати лише на IPv4 при запуску сервера.",
    "server-listen-only-on-ipv6": "Слухати лише на IPv6 при запуску сервера.",
    "server-interface-ipv4": "IP-адреса для прив'язки до IPv4. Якщо залишити порожнім, за замовчуванням використовуються всі.",
    "server-interface-ipv6": "IP-адреса для прив'язки до IPv6. Якщо залишити порожнім, за замовчуванням використовуються всі.",

    # Server errors
    "unknown-command-server-error": "Невідома команда: {}",  # message
    "not-json-server-error": "Не є закодованим json-рядком: {}",  # message
    "line-decode-server-error": "Не є рядком у кодуванні UTF-8",
    "not-known-server-error": "Дану команду можуть виконувати лише авторизовані користувачі.",
    "client-drop-server-error": "Клієнт відключено з помилкою: {} -- {}",  # host, error
    "password-required-server-error": "Необхідно вказати пароль.",
    "wrong-password-server-error": "Вказано неправильний пароль.",
    "hello-server-error": "Не вистачає аргументів Hello.",

    "playlist-selection-changed-notification": "{} змінив вибір у списку відтворення",  # Username
    "playlist-contents-changed-notification": "{} оновив список відтворення",  # Username
    "cannot-find-file-for-playlist-switch-error": "Не вдалося знайти файл {} у папках відтворення!",  # Filename
    "cannot-add-duplicate-error": "'{}' вже є у списку відтворення.",  # Filename
    "cannot-add-unsafe-path-error": "Не вдалося автоматично переключитися на {}, тому що посилання не відповідає довіреним сайтам. Його можна увімкнути вручну, двічі клікнувши по посиланню у списку відтворення. Додати довірений сайт можна в меню 'Додатково' або просто клікнувши по посиланню правою кнопкою миші.",  # Filename
    "sharedplaylistenabled-label": "Увімкнути спільний список відтворення",
    "removefromplaylist-menu-label": "Видалити",
    "shuffleremainingplaylist-menu-label": "Перемішати залишок списку відтворення",
    "shuffleentireplaylist-menu-label": "Перемішати весь список відтворення",
    "undoplaylist-menu-label": "Скасувати останню дію",
    "addfilestoplaylist-menu-label": "Додати файли в чергу",
    "addurlstoplaylist-menu-label": "Додати посилання в чергу",
    "editplaylist-menu-label": "Редагувати список",

    "open-containing-folder": "Відкрити папку, що містить цей файл",
    "addyourfiletoplaylist-menu-label": "Додати ваш файл у список відтворення",
    "addotherusersfiletoplaylist-menu-label": "Додати файл {} у список відтворення",
    "addyourstreamstoplaylist-menu-label": "Додати ваш потік у список відтворення",
    "addotherusersstreamstoplaylist-menu-label": "Додати потік {} у список відтворення",
    "openusersstream-menu-label": "Відкрити потік {}",
    "openusersfile-menu-label": "Відкрити файл {}",

    "setasready-menu-label": "Позначити {} як готового",  # [Username]
    "setasnotready-menu-label": "Позначити {} як неготового",  # [Username]

    "playlist-instruction-item-message": "Перетягніть сюди файли, щоб додати їх у спільний список.",
    "sharedplaylistenabled-tooltip": "Оператор кімнати може додавати файли у список спільного відтворення для зручного спільного перегляду. Папки відтворення налаштовуються в меню 'Файл'.",

    "playlist-empty-error": "Список відтворення порожній.",
    "playlist-invalid-index-error": "Неправильний індекс у списку відтворення",

    # Watched file functionality
    "files-label": "Файли",
    "syncplay-watchedhistory-title": "Історія переглянутих файлів",
    "syncplay-watchedhistoryenabled-label": "Увімкнути історію переглянутих файлів (JSON-індекс)",
    "syncplay-autoremovefromplaylist-label": "Автоматично видаляти переглянуті файли зі списку відтворення",
    "watchedhistoryenabled-tooltip": "Зберігає переглянуті файли поруч із файлом конфігурації Syncplay у '.syncplay-watched.json'. Статус перегляду зберігається, навіть якщо файл переміщено або видалено.",
    "autoremovewatchedfromplaylist-tooltip": "Видаляє елемент зі спільного списку відтворення, коли Syncplay позначає його як переглянутий після досягнення кінця відтворення.",
    "watched-json-read-error": "Не вдалося прочитати файл історії переглянутих файлів '{}': {}",
    "watched-json-write-error": "Не вдалося записати файл історії переглянутих файлів '{}': {}",
    "watched-json-concurrent-update-error": "Не вдалося оновити файл історії переглянутих файлів через одночасні зміни: {}",
    "watched-move-permission-error": "Не вдалося перемістити '{}' у підпапку переглянутих через помилку доступу.",
    "watched-move-failed-error": "Не вдалося перемістити '{}' у підпапку переглянутих: {}",
    "watched-move-too-many-retries-error": "Занадто багато спроб переміщення '{}' у підпапку переглянутих. Операцію скасовано.",
    "watched-mark-watched-error": "Не вдалося позначити '{}' як переглянутий: {}",
    "watched-mark-unwatched-error": "Не вдалося позначити '{}' як непереглянутий: {}",
    "watched-record-history-error": "Не вдалося записати історію перегляду для '{}': {}",
    "marked-file-as-watched-notification": "'{}' позначено як переглянутий.",
    "marked-file-as-unwatched-notification": "'{}' позначено як непереглянутий.",
    "watched-last-watched-tooltip": "Останній перегляд: {} у кімнаті '{}' ({})",  # how long, room, date and time
    "watched-datetime-format": "%d %B %Y %H:%M",
    "watched-ago-minutes": "{} хвилин тому",
    "watched-ago-hours": "{} годин тому",
    "watched-ago-days": "{} днів тому",
    "syncplay-watchedfiles-title": "Переглянуті файли",
    "syncplay-watchedautomove-label": "Автоматично переміщувати переглянуті файли у підпапку (якщо вона існує)",
    "syncplay-watchedmovesubfolder-label": "Підпапка для переглянутих файлів",
    "syncplay-watchedsubfolderautocreate-label": "Автоматично створювати підпапку для переглянутих файлів за необхідності",
    "mark-as-watched-menu-label": "Позначити як переглянутий",
    "mark-as-unwatched-menu-label": "Позначити як непереглянутий",
    "previous-file-menu-section-label": "Попередній файл: '{}'",  # filename
    "mark-previous-file-as-watched-menu-label": "Позначити як переглянутий",
    "add-previous-file-to-playlist-menu-label": "Додати до списку відтворення",
    "watchedautomove-tooltip": "Автоматично переміщує файл у підпапку переглянутих при досягненні кінця файлу. Працює лише якщо батьківська папка є папкою відтворення.",
    "watchedsubfolder-tooltip": "Підпапка, у яку переміщуються переглянуті файли відносно папки файлу (підпапка повинна існувати). Працює лише якщо батьківська папка є папкою відтворення.",
    "watchedsubfolderautocreate-tooltip": "Автоматично створює підпапку переглянутих, якщо її немає під час переміщення файлу. Працює лише якщо батьківська папка є папкою відтворення.",
    "cannot-move-file-due-to-name-conflict-error": "Не вдалося перемістити '{}' у підпапку '{}', тому що файл з таким ім'ям вже існує.",
    "cannot-move-file-due-to-parent-name-conflict-error": "Не вдалося перемістити '{}' назад у батьківську папку '{}', тому що файл з таким ім'ям вже існує.",
    "file-not-in-watched-subfolder-error": "'{}' не знаходиться у підпапці переглянутих файлів.",  # path
    "watched-file-tracking-disabled-error": "Відстеження переглянутих файлів вимкнено.",
    "watched-subfolder-unavailable-error": "Не вдалося перемістити '{}' у підпапку '{}', тому що підпапку не вдалося знайти або створити.",  # path, subfolder
    "watched-parent-folder-unavailable-error": "Не вдалося перемістити '{}' з підпапки переглянутих файлів, тому що батьківську папку не вдалося знайти.",  # path
    "moved-file-to-subfolder-notification": "'{}' переміщено у підпапку '{}'.",
    "moved-file-from-watched-subfolder-notification": "'{}' переміщено назад у '{}'.",  # path, parent folder

    "playlist-skip-warning-tooltip": "Попередження: схоже, що пропускається непереглянутий файл {}.",  # missing file number
    "playlist-out-of-order-warning-tooltip": "Попередження: файл {} розташований не за порядком після файлу {}. Замість нього очікувався файл {}."  # actual file number, previous file number, expected file number
}
