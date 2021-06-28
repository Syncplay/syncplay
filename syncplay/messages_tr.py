# coding:utf8

"""Turkish dictionary"""

tr = {
    "LANGUAGE": "Türkçe", # Turkish

    # Client notifications
    "config-cleared-notification": "Ayarlar temizlendi. Geçerli bir konfigürasyon kaydettiğinizde değişiklikler kaydedilecektir.",

    "relative-config-notification": "Göreli yapılandırma dosya(ları) yüklendi: {}",

    "connection-attempt-notification": "{} İle bağlantı kurulmaya çalışılıyor: {}",  # Port, IP
    "reconnection-attempt-notification": "Sunucuyla bağlantı kesildi, yeniden bağlanılmaya çalışılıyor",
    "disconnection-notification": "Sunucuyla bağlantısı kesildi",
    "connection-failed-notification": "Sunucuyla bağlantı başarısız oldu",
    "connected-successful-notification": "Sunucuya başarıyla bağlandı",
    "retrying-notification": "% s,% d saniye içinde yeniden deneniyor ...",  # Seconds
    "reachout-successful-notification": "Başarıyla ulaşıldı {} ({})",

    "rewind-notification": "{} ile zaman farkı nedeniyle geri alındı",  # User
    "fastforward-notification": "{} ile zaman farkı nedeniyle ileri sarıldı",  # User
    "slowdown-notification": "{} ile zaman farkı nedeniyele nedeniyle yavaşlıyor",  # User
    "revert-notification": "Hızı normale döndürülüyor",

    "pause-notification": "{} duraklattı",  # User
    "unpause-notification": "{} devam ettirdi",  # User
    "seek-notification": "{}, {} konumundan {} konumuna atladı",  # User, from time, to time

    "current-offset-notification": "Mevcut fark: {} saniye",  # Offset

    "media-directory-list-updated-notification": "Syncplay ortam dizinleri güncellendi.",

    "room-join-notification": "{} odaya katıldı: '{}'",  # User
    "left-notification": "{} ayrıldı",  # User
    "left-paused-notification": "{} ayrıldı, {} duraklattı",  # User who left, User who paused
    "playing-notification": "{} oynatıyor '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum":  " odada: '{}'",  # Room

    "not-all-ready": "Hazır değil: {}",  # Usernames
    "all-users-ready": "Herkes hazır ({} kullanıcı)",  # Number of ready users
    "ready-to-unpause-notification": "Artık hazır olarak ayarlandınız - devam ettirmek için yeniden duraklatmayı kaldırın",
    "set-as-ready-notification": "Artık hazırsınız",
    "set-as-not-ready-notification": "Artık hazır değilsiniz",
    "autoplaying-notification": "{} içinde otomatik oynatılıyor ...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Oda operatörü '{}' parolası ile tanımlanıyor ...",
    "failed-to-identify-as-controller-notification": "{}, operatörü olarak tanımlanamadı.",
    "authenticated-as-controller-notification": "{}, oda operatörü olarak doğrulandı",
    "created-controlled-room-notification": "Yönetilen oda '{}' '{}' şifresiyle oluşturuldu. Lütfen bu bilgileri ileride başvurmak üzere kaydedin!\n\nYönetilen odalarda, oynatma listesini duraklatabilen, devam ettirebilen, arayabilen ve değiştirebilen tek kişi olan oda operatörleri ile herkes senkronize edilir.\n\nNormal izleyicilerden '{}' odasına katılmalarını istemelisiniz, ancak oda operatörleri kendilerini otomatik olarak doğrulamak için '{}' odasına katılabilir.",  # RoomName, operatorPassword, roomName, roomName:operatorPassword

    "file-different-notification": "Oynadığınız dosya, {} dosyasından farklı görünüyor",  # User
    "file-differences-notification": "Dosyanız aşağıdaki şekil(ler)de farklılık gösterir: {}",  # Differences
    "room-file-differences": "Dosya farklılıkları: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "adı",
    "file-difference-filesize": "boyutu",
    "file-difference-duration": "süresi",
    "alone-in-the-room": "Odada yalnızsın",

    "different-filesize-notification": " (dosya boyutları sizinkinden farklı!)",
    "userlist-playing-notification": "{} oynuyor:",  # Username
    "file-played-by-notification": "Dosya: {} şu kullanıcı tarafından oynatılıyor:",  # File
    "no-file-played-notification": "{} dosya oynatmıyor",  # Username
    "notplaying-notification": "Herhangi bir dosya oynatmayan kişiler:",
    "userlist-room-notification":  "Odada '{}':",  # Room
    "userlist-file-notification": "Dosya",
    "controller-userlist-userflag": "Operatör",
    "ready-userlist-userflag": "Hazır",

    "update-check-failed-notification": "Syncplay {} 'in güncel olup olmadığı otomatik olarak kontrol edilemedi. Güncellemeleri manuel olarak kontrol etmek için https://syncplay.pl/ adresini ziyaret etmek ister misiniz?",  # Syncplay version
    "syncplay-uptodate-notification": "Syncplay güncel",
    "syncplay-updateavailable-notification": "Syncplay'in yeni bir sürümü mevcut. Sürüm sayfasını ziyaret etmek istiyor musunuz?",

    "mplayer-file-required-notification": "MPlayer kullanarak Syncplay, başlatırken dosya sağlamanızı gerektirir",
    "mplayer-file-required-notification/example": "Kullanım örneği: syncplay [options] [url|path/]filename",
    "mplayer2-required": "Syncplay, MPlayer 1.x ile uyumlu değil, lütfen mplayer2 veya mpv kullanın",

    "unrecognized-command-notification": "Tanımsız komut",
    "commandlist-notification": "Kullanılabilir komutlar:",
    "commandlist-notification/room": "\tr [name] - odayı değiştirir",
    "commandlist-notification/list": "\tl - kullanıcı listesini gösterir",
    "commandlist-notification/undo": "\tu - son isteği geri alır",
    "commandlist-notification/pause": "\tp - duraklatmayı değiştirir",
    "commandlist-notification/seek": "\t[s][+-]time - verilen zaman değerine atlar, eğer + veya - belirtilmezse, saniye:dakika cinsinden mutlak zamandır.",
    "commandlist-notification/help": "\th - yardım",
    "commandlist-notification/toggle": "\tt - izlemeye hazır olup olmadığınızı değiştirir",
    "commandlist-notification/create": "\tc [name] - mevcut odanın adını kullanarak yönetilen oda oluştur",
    "commandlist-notification/auth": "\ta [password] - operatör şifresi ile oda operatörü olarak kimlik doğrular",
    "commandlist-notification/chat": "\tch [message] - bir odaya sohbet mesajı gönderir",
    "commandList-notification/queue": "\tqa [file/url] - oynatma listesinin altına dosya veya bağlantı ekler",
    "commandList-notification/playlist": "\tql - mevcut oynatma listesini gösterir",
    "commandList-notification/select": "\tqs [index] - oynatma listesinde verilen girişi seçer",
    "commandList-notification/delete": "\tqd [index] - verilen girişi oynatma listesinden siler",
    "syncplay-version-notification": "Syncplay sürümü: {}",  # syncplay.version
    "more-info-notification": "Daha fazla bilgiye şu adresten ulaşabilirsiniz: {}",  # projectURL

    "gui-data-cleared-notification": "Syncplay, GUI tarafından kullanılan yolu ve pencere durumu verilerini temizledi.",
    "language-changed-msgbox-label": "Syncplay'i çalıştırdığınızda dil değiştirilecek.",
    "promptforupdate-label": "Syncplay'in zaman zaman güncellemeleri otomatik olarak kontrol etmesi uygun mudur?",

    "media-player-latency-warning": "Uyarı: Medya yürütücünün yanıt vermesi {} saniye sürdü. Senkronizasyon sorunları yaşıyorsanız, sistem kaynaklarını boşaltmak için uygulamaları kapatın ve bu işe yaramazsa, farklı bir medya oynatıcı deneyin.",  # Seconds to respond
    "mpv-unresponsive-error": "mpv {} saniye boyunca yanıt vermedi, bu nedenle arızalı görünüyor. Lütfen Syncplay'i yeniden başlatın.",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "Çıkmak için enter tuşuna basın\n",

    # Client errors
    "missing-arguments-error": "Bazı gerekli argümanlar eksik, bakınız --help",
    "server-timeout-error": "Sunucuyla bağlantı zaman aşımına uğradı",
    "mpc-slave-error": "Bağımlı modda MPC başlatılamıyor!",
    "mpc-version-insufficient-error": "MPC sürümü yeterli değil, lütfen `mpc-hc`> =` {} `kullanın",
    "mpc-be-version-insufficient-error": "MPC sürümü yeterli değil, lütfen `mpc-hc`> =` {} `kullanın",
    "mpv-version-error": "Syncplay, mpv'nin bu sürümüyle uyumlu değil. Lütfen farklı bir mpv sürümü kullanın (ör. Git HEAD).",
    "mpv-failed-advice": "Mpv'nin başlatılamamasının nedeni, desteklenmeyen komut satırı bağımsız değişkenlerinin veya mpv'nin desteklenmeyen bir sürümünün kullanılması olabilir.",
    "player-file-open-error": "Oynatıcı dosyayı açamadı",
    "player-path-error": "Oynatıcı yolu doğru ayarlanmadı. Desteklenen oynatıcılar şunlardır: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 ve IINA",
    "hostname-empty-error": "Ana bilgisayar adı boş olamaz",
    "empty-error": "{} boş olamaz",  # Configuration
    "media-player-error": "Medaya oynatıcısı hatası: \"{}\"",  # Error line
    "unable-import-gui-error": "GUI kitaplıkları içe aktarılamadı. PySide kurulu değilse, GUI'nin çalışması için kurmanız gerekecektir.",
    "unable-import-twisted-error": "Twisted içe aktarılamadı. Lütfen Twisted v16.4.0 veya sonraki sürümünü yükleyin.",

    "arguments-missing-error": "Bazı gerekli argümanlar eksik, bakınız --help",

    "unable-to-start-client-error": "İstemci başlatılamıyor",

    "player-path-config-error": "Oynatıcı yolu doğru ayarlanmadı. Desteklenen oyuncular şunlardır: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 ve IINA.",
    "no-file-path-config-error": "Oynatıcınız başlatılmadan önce dosya seçilmelidir",
    "no-hostname-config-error": "Ana bilgisayar adı boş olamaz",
    "invalid-port-config-error": "Bağlantı noktası geçerli olmalıdır",
    "empty-value-config-error": "{} boş olamaz",  # Config option

    "not-json-error": "JSON ile kodlanmış bir dize değil\n",
    "hello-arguments-error": "Not enough Hello arguments\n",  # DO NOT TRANSLATE
    "version-mismatch-error": "İstemci ve sunucu sürümleri arasında uyumsuzluk\n",
    "vlc-failed-connection": "VLC'ye bağlanılamadı. Syncplay.lua'yı yüklemediyseniz ve VLC'nin en son sürümünü kullanıyorsanız talimatlar için lütfen https://syncplay.pl/LUA/ adresine bakın. Syncplay ve VLC 4 şu anda uyumlu değildir, bu nedenle VLC 3'ü veya mpv gibi bir alternatifi kullanın.",
    "vlc-failed-noscript": "VLC, syncplay.lua arabirim komut dosyasının yüklenmediğini bildirdi. Talimatlar için lütfen https://syncplay.pl/LUA/ adresine bakın.",
    "vlc-failed-versioncheck": "VLC'nin bu sürümü Syncplay tarafından desteklenmemektedir.",
    "vlc-initial-warning": 'VLC, özellikle .mp4 ve .avi dosyaları için Syncplay\'e her zaman doğru konum bilgisi sağlamaz. Hatalı arama ile ilgili sorunlar yaşarsanız, lütfen <a href="https://mpv.io/"> mpv</a> gibi alternatif bir medya oynatıcı deneyin. (veya Windows kullanıcıları için <a href="https://github.com/stax76/mpv.net/">mpv.net</a>).',

    "feature-sharedPlaylists": "paylaşılan oynatma listeleri",  # used for not-supported-by-server-error
    "feature-chat": "sohbet",  # used for not-supported-by-server-error
    "feature-readiness": "hazırlık",  # used for not-supported-by-server-error
    "feature-managedRooms": "yönetilen odalar",  # used for not-supported-by-server-error

    "not-supported-by-server-error": "{} özelliği bu sunucu tarafından desteklenmiyor ..",  # feature
    "shared-playlists-not-supported-by-server-error": "Paylaşılan çalma listeleri özelliği sunucu tarafından desteklenmeyebilir. Doğru çalıştığından emin olmak için Syncplay  {}+ çalıştıran bir sunucu gerektirir, ancak sunucu Syncplay {} çalıştırmaktadır.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "Paylaşılan çalma listesi özelliği, sunucu yapılandırmasında devre dışı bırakıldı. Bu özelliği kullanmak için farklı bir sunucuya bağlanmanız gerekecektir.",

    "invalid-seek-value": "Geçersiz atlama değerie",
    "invalid-offset-value": "Geçersiz zaman konumu değeri",

    "switch-file-not-found-error": "'{0}' dosyasına geçilemedi. Syncplay, belirtilen medya dizinlerine bakar.",  # File not found
    "folder-search-timeout-error": "'{}' üzerinden arama yapmak çok uzun sürdüğü için medya dizinlerinde medya araması durduruldu. Ortam klasörleri listenizde arama yapmak için çok fazla alt klasörün bulunduğu bir klasör seçerseniz bu meydana gelir. Otomatik dosya değiştirmenin tekrar çalışması için lütfen menü çubuğunda Dosya-> Medya Dizinlerini Ayarla'yı seçin ve bu dizini kaldırın veya uygun bir alt klasörle değiştirin. Klasör gerçekten iyi durumdaysa, Dosya-> Medya Dizinlerini Ayarla'yı seçip 'Tamam'a basarak yeniden etkinleştirebilirsiniz.",  # Folder
    "folder-search-first-file-timeout-error": "Dizine erişim çok uzun sürdüğü için '{}' içindeki medya araması durduruldu. Bu, bir ağ sürücüsü ise veya sürücünüzü bir süre kullanılmadığında dönecek şekilde yapılandırırsanız olabilir. Otomatik dosya değiştirmenin tekrar çalışması için lütfen Dosya-> Medya Dizinlerini Ayarla'ya gidin ve dizini kaldırın veya sorunu çözün (örn. Güç tasarrufu ayarlarını değiştirerek).",  # Folder
    "added-file-not-in-media-directory-error": "Bilinen bir medya dizini olmayan '{}' içine bir dosya yüklediniz. Menü çubuğunda Dosya-> Medya Dizinlerini Ayarla'yı seçerek bunu bir medya dizini olarak ekleyebilirsiniz.",  # Folder
    "no-media-directories-error": "Hiçbir medya dizini ayarlanmadı. Paylaşılan çalma listesi ve dosya değiştirme özelliklerinin düzgün çalışması için lütfen Dosya-> Ortam Dizinlerini Ayarla'yı seçin ve Syncplay'in medya dosyalarını bulmak için nereye bakması gerektiğini belirtin.",
    "cannot-find-directory-error": "'{}' medya dizini bulunamadı. Medya dizinleri listenizi güncellemek için lütfen menü çubuğundan Dosya-> Medya Dizinlerini Ayarla'yı seçin ve Syncplay'in medya dosyalarını bulmak için nereye bakması gerektiğini belirtin.",

    "failed-to-load-server-list-error": "Genel sunucu listesi yüklenemedi. Lütfen tarayıcınızda https://www.syncplay.pl/ adresini ziyaret edin.",

    # Client arguments
    "argument-description": 'Ağ üzerinden birden çok medya oynatıcı örneğinin oynatılmasını senkronize etme çözümü.',
    "argument-epilog": 'Sağlanan seçenek yoksa _config değerleri kullanılacaktır',
    "nogui-argument": 'GUI olmadan göster',
    "host-argument": 'sunucunun adresi',
    "name-argument": 'istenilen kullanıcı adı',
    "debug-argument": 'debug modu',
    "force-gui-prompt-argument": 'yapılandırma isteminin görünmesini sağlayın',
    "no-store-argument": 'değerleri .syncplay içinde saklamayın',
    "room-argument": 'varsayılan oda',
    "password-argument": 'sunucu parolası',
    "player-path-argument": 'oynatıcınızın çalıştırılabilir yolu',
    "file-argument": 'oynatmak için dosya',
    "args-argument": 'oynatıcı seçenekleri, ile başlayan seçenekleri iletmeniz gerekiyorsa - bunların başına tek \'--\' argümanı ekleyin',
    "clear-gui-data-argument": 'QSettings olarak depolanan yol ve pencere durumu GUI verilerini sıfırlar',
    "language-argument": 'Syncplay mesajları için dil (de/en/ru/it/es/pt_BR/pt_PT/tr)',

    "version-argument": 'versiyonunuzu yazdırır',
    "version-message": "Syncplay sürümünü kullanıyorsunuz {} ({})",

    "load-playlist-from-file-argument": "metin dosyasından oynatma listesi yükler (her satıra bir giriş)",


    # Client labels
    "config-window-title": "Syncplay yapılandırması",

    "connection-group-title": "Bağlantı ayarları",
    "host-label": "Sunucu adresi: ",
    "name-label":  "Kullanıcı adı (isteğe bağlı):",
    "password-label":  "Sunucu şifresi (varsa):",
    "room-label": "Varsayılan oda: ",
    "roomlist-msgbox-label": "Oda listesini düzenleyin (her satıra bir tane)",

    "media-setting-title": "Medya oynatıcı ayarları",
    "executable-path-label": "Medya oynatıcı dosya yolu:",
    "media-path-label": "Video dosya yolu (isteğe bağlı):",
    "player-arguments-label": "Oynatıcı argümanları (varsa):",
    "browse-label": "Araştır",
    "update-server-list-label": "Listeyi güncelle",

    "more-title": "Daha fazla ayar göster",
    "never-rewind-value": "Asla",
    "seconds-suffix": " secs",
    "privacy-sendraw-option": "raw gönder",
    "privacy-sendhashed-option": "hashed gönder",
    "privacy-dontsend-option": "Gönderme",
    "filename-privacy-label": "Dosya yolu bilgisi:",
    "filesize-privacy-label": "Dosya boyutu bilgisi:",
    "checkforupdatesautomatically-label": "Syncplay güncellemelerini otomatik olarak kontrol edin",
    "autosavejoinstolist-label": "Katıldığınız odaları oda listesine ekleyin",
    "slowondesync-label": "Küçük desenkronizasyonda yavaşlama (MPC-HC / BE'de desteklenmez)",
    "rewindondesync-label": "Ana desenkronizasyonda geri sar (önerilir)",
    "fastforwardondesync-label": "Geride kalırsa hızlı ileri sar (önerilir)",
    "dontslowdownwithme-label": "Başkalarını asla yavaşlatma veya geri sarma (deneysel)",
    "pausing-title": "Duraklatılıyor",
    "pauseonleave-label": "Kullanıcı ayrıldığında duraklayın (ör. Bağlantısı kesilirse)",
    "readiness-title": "İlk hazırlık durumu",
    "readyatstart-label": "Beni varsayılan olarak 'izlemeye hazır' olarak ayarla",
    "forceguiprompt-label": "Syncplay yapılandırma penceresini her zaman gösterme",  # (Inverted)
    "showosd-label": "OSD Mesajlarını Etkinleştir",

    "showosdwarnings-label": "Uyarıları dahil edin (ör. Dosyalar farklı olduğunda, kullanıcılar hazır olmadığında)",
    "showsameroomosd-label": "Odanızdaki etkinlikleri dahil edin",
    "shownoncontrollerosd-label": "Operatör olmayanlardan gelen olayları yönetilen odalara dahil et",
    "showdifferentroomosd-label": "Diğer odalardaki etkinlikleri dahil et",
    "showslowdownosd-label": "Yavaşlatma / geri alma bildirimlerini dahil et",
    "language-label": "Dil:",
    "automatic-language": "Varsayılan ({})",  # Default language
    "showdurationnotification-label": "Medya süresi uyuşmazlıkları konusunda uyarın",
    "basics-label": "Temeller",
    "readiness-label": "Oynat/Duraklat",
    "misc-label": "Misc",
    "core-behaviour-title": "Çekirdek oda davranışı",
    "syncplay-internals-title": "Syncplay dahili bileşenleri",
    "syncplay-mediasearchdirectories-title": "Medya aramak için dizinler",
    "syncplay-mediasearchdirectories-label": "Medya aramak için dizinler (satır başına bir yol)",
    "sync-label": "Sync",
    "sync-otherslagging-title": "Başkaları geride kalıyorsa ...",
    "sync-youlaggging-title": "Geride kalıyorsan ...",
    "messages-label": "mesajlar",
    "messages-osd-title": "Ekran üstü görüntü ayarları",
    "messages-other-title": "Diğer ekran ayarları",
    "chat-label": "Sohbet",
    "privacy-label": "Gizlilik",  # Currently unused, but will be brought back if more space is needed in Misc tab
    "privacy-title": "Gizlilik ayarları",
    "unpause-title": "Oynat'a basarsanız, hazır olarak ayarlayın ve:",
    "unpause-ifalreadyready-option": "Zaten hazır olarak ayarlanmışsa duraklatmayı bırakın",
    "unpause-ifothersready-option": "Zaten hazırsa veya odadaki diğerleri hazırsa duraklatmayı bırakın (varsayılan)",
    "unpause-ifminusersready-option": "Zaten hazırsa veya diğerleri hazırsa ve min kullanıcılar hazırsa duraklatmayı kaldırın",
    "unpause-always": "Her zaman devam ettir",
    "syncplay-trusteddomains-title": "Güvenilir alanlar (akış hizmetleri ve barındırılan içerik için)",

    "chat-title": "Sohbet mesajı girişi",
    "chatinputenabled-label": "Mpv aracılığıyla sohbet girişini etkinleştir",
    "chatdirectinput-label": "Anında sohbet girişine izin ver (sohbet etmek için enter tuşuna basma zorunluluğunu atlayın)",
    "chatinputfont-label": "Sohbet yazı tipi",
    "chatfont-label": "Yazı tipini ayarla",
    "chatcolour-label": "Rengi ayarla",
    "chatinputposition-label": "Mesaj giriş alanının mpv'deki konumu",
    "chat-top-option": "Üst",
    "chat-middle-option": "Orta",
    "chat-bottom-option": "Alt",
    "chatoutputheader-label": "Sohbet mesajı çıkışı",
    "chatoutputfont-label": "Sohbet çıktı yazı tipi",
    "chatoutputenabled-label": "Medya oynatıcıda sohbet çıkışını etkinleştirin (şimdilik yalnızca mpv)",
    "chatoutputposition-label": "Çıkış modu",
    "chat-chatroom-option": "Sohbet odası stili",
    "chat-scrolling-option": "Kaydırma stili",

    "mpv-key-tab-hint": "Alfabe satırı tuşu kısayollarına erişimi değiştirmek için [TAB].",
    "mpv-key-hint": "Mesaj göndermek için [ENTER]. Sohbet modundan çıkmak için [ESC].",
    "alphakey-mode-warning-first-line": "Geçici olarak eski mpv bağlamalarını a-z tuşlarıyla kullanabilirsiniz.",
    "alphakey-mode-warning-second-line": "Syncplay sohbet moduna dönmek için [TAB] tuşuna basın.",

    "help-label": "Yardım",
    "reset-label": "Varsayılanları geri yükle",
    "run-label": "Syncplay'i çalıştırın",
    "storeandrun-label": "Yapılandırmayı depolayın ve Syncplay'i çalıştırın",

    "contact-label": "E-posta <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a> göndermekten çekinmeyin. irc.freenode.net'te <a href=\"https://webchat.freenode.net/?channels=#syncplay\"><nobr>#Syncplay IRC channel</nobr></a> kanalı üzerinden yazabilir, GitHub üzerinden <a href=\"https://github.com/Uriziel/syncplay/issues\"><nobr>sorun bildirebilir</nobr></a>, Facebook üzerinden <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>bizi beğenebilir</nobr></a>, Twitter üzerinden <a href=\"https://twitter.com/Syncplay/\"><nobr>bizi takip edebilir</nobr></a>, veya <a href=\"https://syncplay.pl/\"><nobr>https://syncplay.pl/</nobr></a> adresinden sayfamızı ziyaret edebilirsiniz. Hassas bilgileri göndermek için Syncplay kullanmayın.",

    "joinroom-label": "Odaya katıl",
    "joinroom-menu-label": "{} odasına katıl",
    "seektime-menu-label": "Zamana atla",
    "undoseek-menu-label": "Atlamayı geri al",
    "play-menu-label": "Oynat",
    "pause-menu-label": "Duraklat",
    "playbackbuttons-menu-label": "Oynatma düğmelerini göster",
    "autoplay-menu-label": "Otomatik oynat düğmesini göster",
    "autoplay-guipushbuttonlabel": "Her şey hazır olduğunda oynat",
    "autoplay-minimum-label": "Asgari kullanıcı:",

    "sendmessage-label": "Gönder",

    "ready-guipushbuttonlabel": "İzlemeye hazırım!",

    "roomuser-heading-label": "Oda / Kullanıcı",
    "size-heading-label": "Boyut",
    "duration-heading-label": "Uzunluk",
    "filename-heading-label": "Dosya Adı",
    "notifications-heading-label": "Bildirimler",
    "userlist-heading-label": "Kimin ne oynadığını listesi",

    "browseformedia-label": "Medya dosyalarına göz atın",

    "file-menu-label": "&Dosya",  # & precedes shortcut key
    "openmedia-menu-label": "Medya d&osyasını aç",
    "openstreamurl-menu-label": "Medya akışı &URL'sini aç",
    "setmediadirectories-menu-label": "Medya di&zinlerini ayarlayın",
    "loadplaylistfromfile-menu-label": "Dosyadan oynatma &listesi yükle",
    "saveplaylisttofile-menu-label": "Oynatma listesini dosyaya kay&dedin",
    "exit-menu-label": "Çı&kış",
    "advanced-menu-label": "&Gelişmiş",
    "window-menu-label": "&Pencere",
    "setoffset-menu-label": "Zaman &konumunu ayarla",
    "createcontrolledroom-menu-label": "&Yönetilen oda oluştur",
    "identifyascontroller-menu-label": "&Oda operatörü olarak tanımlayın",
    "settrusteddomains-menu-label": "Güvenilir &domain ayarlayın",
    "addtrusteddomain-menu-label": "{} Alanını güvenilen alan olarak ekleyin",  # Domain

    "edit-menu-label": "Düzenl&e",
    "cut-menu-label": "Ke&s",
    "copy-menu-label": "&Kopyala",
    "paste-menu-label": "&Yapıştır",
    "selectall-menu-label": "&Tümünü Seç",

    "playback-menu-label": "&Oynatma",

    "help-menu-label": "&Yardım",
    "userguide-menu-label": "&Kullanım kılavuzunu aç",
    "update-menu-label": "&Güncellemeleri kontrol ediniz",

    "startTLS-initiated": "Güvenli bağlantı kurulmaya çalışılıyor",
    "startTLS-secure-connection-ok": "Güvenli bağlantı kuruldu ({})",
    "startTLS-server-certificate-invalid": 'Güvenli bağlantı kurulamadı. Sunucu geçersiz bir güvenlik sertifikası kullanıyor. Bu iletişim üçüncü bir şahıs tarafından engellenebilir. Daha fazla ayrıntı ve sorun giderme için <a href="https://syncplay.pl/trouble"> buraya </a> bakın.',
    "startTLS-server-certificate-invalid-DNS-ID": "Syncplay, ana bilgisayar adı için geçerli olmayan bir sertifika kullandığından bu sunucuya güvenmiyor.",
    "startTLS-not-supported-client": "Bu istemci TLS'yi desteklemiyor",
    "startTLS-not-supported-server": "Bu sunucu TLS'yi desteklemiyor",

    # TLS certificate dialog
    "tls-information-title": "Sertifika Ayrıntıları",
    "tls-dialog-status-label": "<strong> Syncplay, {} ile şifrelenmiş bir bağlantı kullanıyor. </strong>",
    "tls-dialog-desc-label": "Dijital sertifika yapılam şifreleme, <br>bu sunucuya {} veri gönderirken ve alırken bilgileri gizli tutar.",
    "tls-dialog-connection-label": "Transport Layer Security (TLS), sürüm {} ile şifrelenen şifre<br/>paketi: {}.",
    "tls-dialog-certificate-label": "{} Tarafından verilen sertifika {} tarihine kadar geçerlidir.",

    # About dialog
    "about-menu-label": "&Syncplay hakkında",
    "about-dialog-title": "Syncplay hakkında",
    "about-dialog-release": "Sürüm {} yayın {}",
    "about-dialog-license-text": "Apache Lisansı altında&nbsp;Lisanslanmıştır,&nbsp;Sürüm 2.0",
    "about-dialog-license-button": "Lisans",
    "about-dialog-dependencies": "Bağımlılıklar",

    "setoffset-msgbox-label": "Zaman konumunu ayarla",
    "offsetinfo-msgbox-label": "Zaman Konumu (Kullanım talimatları için https://syncplay.pl/guide/ adresine bakın):",

    "promptforstreamurl-msgbox-label": "Medya akışı URL'sini aç",
    "promptforstreamurlinfo-msgbox-label": "Akış URL'si",

    "addfolder-label": "Klasör ekle",

    "adduris-msgbox-label": "Oynatma listesine URL ekleyin (her satıra bir tane)",
    "editplaylist-msgbox-label": "Oynatma listesi ayarlayın (satır başına bir)",
    "trusteddomains-msgbox-label": "Etki alanları otomatik olarak geçiş yapmakta sorun yoktur (her satırda bir)",

    "createcontrolledroom-msgbox-label": "Yönetilen oda oluştur",
    "controlledroominfo-msgbox-label": "Yönetilen odanın adını girin\r\n(kullanım talimatları için https://syncplay.pl/guide/ adresine bakın):",

    "identifyascontroller-msgbox-label": "Oda operatörü olarak tanımlayın",
    "identifyinfo-msgbox-label": "Bu oda için operatör şifresini girin\r\n(kullanım talimatları için https://syncplay.pl/guide/ adresine bakın):",

    "public-server-msgbox-label": "Bu görüntüleme oturumu için genel sunucuyu seçin",

    "megabyte-suffix": " MB",

    # Tooltips

    "host-tooltip": "Bağlanılacak ana bilgisayar adı veya IP, isteğe bağlı olarak bağlantı noktası dahil (ör. Syncplay.pl:8999). Yalnızca aynı sunucu/bağlantı noktasındaki kişilerle senkronize edilir.",
    "name-tooltip": "Takma adınız tarafından tanınacaksınız. Kayıt yok, bu nedenle daha sonra kolayca değiştirebilirsiniz. Hiçbiri belirtilmediyse rastgele ad oluşturuldu.",
    "password-tooltip": "Parolalar yalnızca özel sunuculara bağlanmak için gereklidir.",
    "room-tooltip": "Bağlantı kurulduğunda katılabileceğiniz oda neredeyse her şey olabilir, ancak yalnızca aynı odadaki kişilerle senkronize olacaksınız.",

    "edit-rooms-tooltip": "Oda listesini düzenleyin.",

    "executable-path-tooltip": "Seçtiğiniz desteklenen medya oynatıcının konumu (mpv, mpv.net, VLC, MPC-HC / BE, mplayer2 veya IINA).",
    "media-path-tooltip": "Açılacak videonun veya akışın konumu. Mplayer2 için gerekli.",
    "player-arguments-tooltip": "Bu medya oynatıcıya iletilecek ek komut satırı argümanları / anahtarları.",
    "mediasearcdirectories-arguments-tooltip": "Syncplay'in medya dosyalarını arayacağı dizinler, ör. geçmek için tıklama özelliğini kullandığınızda. Syncplay, alt klasörler arasında yinelemeli olarak bakacaktır.",

    "more-tooltip": "Daha az kullanılan ayarları görüntüleyin.",
    "filename-privacy-tooltip": "Oynatılmakta olan dosya adını sunucuya göndermek için gizlilik modu.",
    "filesize-privacy-tooltip": "Oynatılmakta olan dosyanın boyutunu sunucuya göndermek için gizlilik modu.",
    "privacy-sendraw-tooltip": "Bu bilgileri şaşırtmadan gönderin. Bu, çoğu işlevselliğe sahip varsayılan seçenektir.",
    "privacy-sendhashed-tooltip": "Bilginin karma bir versiyonunu göndererek diğer istemciler tarafından daha az görünür hale getirin.",
    "privacy-dontsend-tooltip": "Bu bilgiyi sunucuya göndermeyin. Bu, maksimum gizlilik sağlar.",
    "checkforupdatesautomatically-tooltip": "Syncplay'in yeni bir sürümünün mevcut olup olmadığını görmek için Syncplay web sitesine düzenli olarak danışın.",
    "autosavejoinstolist-tooltip": "Sunucudaki bir odaya katıldığınızda, katılacağınız odalar listesindeki oda adını otomatik olarak hatırlayın.",
    "slowondesync-tooltip": "Sizi diğer izleyicilerle senkronize hale getirmek için gerektiğinde oynatma oranını geçici olarak azaltın. MPC-HC/BE'de desteklenmez.",
    "dontslowdownwithme-tooltip": "Oynatma işleminiz geciktiğinde başkalarının yavaşlamaması veya geri sarılmaması anlamına gelir. Oda operatörleri için kullanışlıdır.",
    "pauseonleave-tooltip": "Bağlantınız kesilirse veya biri odanızdan ayrılırsa oynatmayı duraklatın.",
    "readyatstart-tooltip": "Başlangıçta kendinizi 'hazır' olarak ayarlayın (aksi takdirde hazır olma durumunuzu değiştirene kadar 'hazır değil' olarak ayarlanırsınız)",
    "forceguiprompt-tooltip": "Syncplay ile bir dosya açarken yapılandırma diyaloğu gösterilmiyor.",  # (Inverted)
    "nostore-tooltip": "Syncplay'i verilen yapılandırmayla çalıştırın, ancak değişiklikleri kalıcı olarak saklamayın.",  # (Inverted)
    "rewindondesync-tooltip": "Tekrar senkronize olmak için gerektiğinde geri gidin. Bu seçeneğin devre dışı bırakılması büyük desenkronizasyonlara neden olabilir!",
    "fastforwardondesync-tooltip": "Oda operatörüyle senkronizasyon dışındayken ileri atlayın (veya 'Başkalarını asla yavaşlatma veya geri sarma' etkinse taklit konumunuz).",
    "showosd-tooltip": "Syncplay mesajlarını medya oynatıcı OSD'sine gönderir.",
    "showosdwarnings-tooltip": "Farklı bir dosya oynatılıyorsa, odada tek başına, kullanıcılar hazır değilse vb. Uyarıları gösterin.",
    "showsameroomosd-tooltip": "Oda kullanıcısının bulunduğu yerle ilgili olaylar için OSD bildirimlerini göster.",
    "shownoncontrollerosd-tooltip": "Yönetilen odalarda bulunan operatör olmayanlarla ilgili olaylar için OSD bildirimlerini gösterin.",
    "showdifferentroomosd-tooltip": "Oda kullanıcısının içinde olmadığı ile ilgili olaylar için OSD bildirimlerini göster.",
    "showslowdownosd-tooltip": "Zaman farkında yavaşlama / geri dönme bildirimlerini gösterin.",
    "showdurationnotification-tooltip": "Çok parçalı bir dosyadaki bir segment eksik olduğunda kullanışlıdır, ancak yanlış pozitiflere neden olabilir.",
    "language-tooltip": "Syncplay tarafından kullanılacak dil.",
    "unpause-always-tooltip": "Yeniden duraklatmaya basarsanız, yalnızca sizi hazır olarak ayarlamak yerine, her zaman hazır ve duraklatmaya devam etmenizi sağlar.",
    "unpause-ifalreadyready-tooltip": "Hazır olmadığınızda yeniden duraklatmaya basarsanız, sizi hazır olarak ayarlar - devam ettirmek için yeniden duraklatmaya basın.",
    "unpause-ifothersready-tooltip": "Hazır olmadığınızda duraklatmayı kaldır'a basarsanız, yalnızca başkaları hazırsa duraklatmaya devam eder.",
    "unpause-ifminusersready-tooltip": "Hazır değilken duraklatmayı kaldır'a basarsanız, yalnızca başkaları hazırsa ve minimum kullanıcı eşiğine ulaşılırsa duraklatmaya devam edilir.",
    "trusteddomains-arguments-tooltip": "Syncplay'in, paylaşılan oynatma listeleri etkinleştirildiğinde otomatik olarak geçiş yapmasının uygun olduğu alanlar.",

    "chatinputenabled-tooltip": "MPv'de sohbet girişini etkinleştirin (sohbet için enter'a basın, göndermek için enter'a basın, iptal etmek için çıkış yapın)",
    "chatdirectinput-tooltip": "Mpv'de sohbet giriş moduna geçmek için 'enter' tuşuna basma zorunluluğunu atlayın. Bu özelliği geçici olarak devre dışı bırakmak için mpv'de TAB tuşuna basın.",
    "font-label-tooltip": "Mpv'de sohbet mesajlarını girerken kullanılan yazı tipi. Yalnızca istemci tarafındadır, bu nedenle diğerlerinin gördüklerini etkilemez.",
    "set-input-font-tooltip": "Mpv'de sohbet mesajlarını girerken kullanılan yazı tipi ailesi. Yalnızca istemci tarafındadır, bu nedenle diğerlerinin gördüklerini etkilemez.",
    "set-input-colour-tooltip": "Mpv'de sohbet mesajlarını girerken kullanılan yazı tipi rengi. Yalnızca istemci tarafındadır, bu nedenle diğerlerinin gördüklerini etkilemez.",
    "chatinputposition-tooltip": "Enter tuşuna basıp yazdığınızda sohbet giriş metninin görüneceği mpv'deki konum.",
    "chatinputposition-top-tooltip": "Sohbet girişini mpv penceresinin üstüne yerleştirin.",
    "chatinputposition-middle-tooltip": "Sohbet girişini mpv penceresinin tam ortasına yerleştirin.",
    "chatinputposition-bottom-tooltip": "Sohbet girişini mpv penceresinin altına yerleştirin.",
    "chatoutputenabled-tooltip": "OSD'de sohbet mesajlarını gösterin (medya oynatıcı tarafından destekleniyorsa).",
    "font-output-label-tooltip": "Sohbet yazı tipi.",
    "set-output-font-tooltip": "Sohbet mesajlarını görüntülerken kullanılan yazı tipi.",
    "chatoutputmode-tooltip": "Sohbet mesajları nasıl görüntülenir.",
    "chatoutputmode-chatroom-tooltip": "Yeni sohbet satırlarını doğrudan önceki satırın altında görüntüleyin.",
    "chatoutputmode-scrolling-tooltip": "Sohbet metnini sağdan sola kaydırın.",

    "help-tooltip": "Syncplay.pl kullanım kılavuzunu açar.",
    "reset-tooltip": "Tüm ayarları varsayılan yapılandırmaya sıfırlayın.",
    "update-server-list-tooltip": "Genel sunucuların listesini güncellemek için syncplay.pl'ye bağlanın.",

    "sslconnection-tooltip": "Sunucuya güvenli bir şekilde bağlı. Sertifika detayları için tıklayınız.",

    "joinroom-tooltip": "Mevcut odadan çıkın ve belirtilen odaya katılır.",
    "seektime-msgbox-label": "Belirtilen zamana atlayın (saniye / dakika:saniye). Göreceli atlama için +/- kullanın.",
    "ready-tooltip": "İzlemeye hazır olup olmadığınızı gösterir.",
    "autoplay-tooltip": "Hazır olma göstergesine sahip tüm kullanıcılar hazır olduğunda ve minimum kullanıcı eşiğine ulaşıldığında otomatik oynatın.",
    "switch-to-file-tooltip": "Çift tıklama ile şuna geç {}",  # Filename
    "sendmessage-tooltip": "Odaya mesaj gönder",

    # In-userlist notes (GUI)
    "differentsize-note": "Farklı boyut!",
    "differentsizeandduration-note": "Farklı boyut ve süre!",
    "differentduration-note": "Farklı süre!",
    "nofile-note": "(Oynatılan dosya yok)",

    # Server messages to client
    "new-syncplay-available-motd-message": "Syncplay {} kullanıyorsunuz ancak daha yeni bir sürüm https://syncplay.pl adresinde mevcut",  # ClientVersion

    # Server notifications
    "welcome-server-notification": "Syncplay sunucusuna hoş geldiniz, ver. {0}",  # version
    "client-connected-room-server-notification": "{0}({2}) odaya bağlandı '{1}'",  # username, host, room
    "client-left-server-notification": "{0} sunucudan ayrıldı",  # name
    "no-salt-notification": "LÜTFEN DİKKAT: Bu sunucu örneği tarafından oluşturulan oda operatörü şifrelerinin sunucu yeniden başlatıldığında da çalışmasına izin vermek için, lütfen gelecekte Syncplay sunucusunu çalıştırırken aşağıdaki komut satırı bağımsız değişkenini ekleyin: --salt {}",  # Salt


    # Server arguments
    "server-argument-description": 'Ağ üzerinden birden çok medya oynatıcı örneğinin oynatılmasını senkronize etme çözümü. Sunucu örneği',
    "server-argument-epilog": 'Sağlanan seçenek yoksa _config değerleri kullanılacaktır',
    "server-port-argument": 'sunucu TCP bağlantı noktası',
    "server-password-argument": 'sunucu parolası',
    "server-isolate-room-argument": 'odalar izole edilmeli mi?',
    "server-salt-argument": "yönetilen oda şifreleri oluşturmak için kullanılan rastgele dize",
    "server-disable-ready-argument": "hazır olma özelliğini devre dışı bırak",
    "server-motd-argument": "motd alınacak dosyanın yolu",
    "server-rooms-argument": "path to directory to store/fetch room data. Enables rooms to persist without watchers and through restarts", # TODO: Translate
    "server-timer-argument": "time in seconds before a persistent room with no watchers is pruned. 0 disables pruning", # TODO: Translate
    "server-chat-argument": "Sohbet devre dışı bırakılmalı mı?",
    "server-chat-maxchars-argument": "Bir sohbet mesajındaki maksimum karakter sayısı (varsayılan: {})", # Default number of characters
    "server-maxusernamelength-argument": "Bir kullanıcı adındaki maksimum karakter sayısı (varsayılan {})",
    "server-stats-db-file-argument": "SQLite db dosyasını kullanarak sunucu istatistiklerini etkinleştirin",
    "server-startTLS-argument": "Dosya yolundaki sertifika dosyalarını kullanarak TLS bağlantılarını etkinleştirin",
    "server-messed-up-motd-unescaped-placeholders": "Günün Mesajında çıkış karaktersiz yer tutucular var. Tüm $ işaretleri iki katına çıkarılmalıdır ($$).",
    "server-messed-up-motd-too-long": "Günün Mesajı çok uzun - maksimum {} karakter olmalı, {} verildi.",

    # Server errors
    "unknown-command-server-error": "Bilinmeyen komut {}",  # message
    "not-json-server-error": "JSON ile kodlanmış bir dize değil {}",  # message
    "line-decode-server-error": "Utf-8 dizesi değil",
    "not-known-server-error": "Bu komutu göndermeden önce sunucu tarafından bilinmelisiniz",
    "client-drop-server-error": "İstemci bırakma: {} -- {}",  # host, error
    "password-required-server-error": "Parola gerekli",
    "wrong-password-server-error": "Yanlış parola sağlandı",
    "hello-server-error": "Not enough Hello arguments",  # DO NOT TRANSLATE

    # Playlists
    "playlist-selection-changed-notification":  "{} oynatma listesi seçimini değiştirdi",  # Username
    "playlist-contents-changed-notification": "{} oynatma listesini güncelledi",  # Username
    "cannot-find-file-for-playlist-switch-error": "Çalma listesi anahtarı için medya dizinlerinde {} dosyası bulunamadı!",  # Filename
    "cannot-add-duplicate-error": "Yinelemelere izin verilmediğinden oynatma listesine '{}' için ikinci giriş eklenemedi.",  # Filename
    "cannot-add-unsafe-path-error": "Güvenilir bir alanda olmadığı için {} otomatik olarak yüklenemedi. Oynatma listesinde çift tıklayarak URL'ye manuel olarak geçebilir ve Dosya-> Gelişmiş-> Güvenilir Etki Alanlarını Ayarla aracılığıyla güvenilir etki alanları ekleyebilirsiniz. Bir URL'yi sağ tıklarsanız, o URL'nin etki alanını bağlam menüsü aracılığıyla güvenilen etki alanı olarak ekleyebilirsiniz.",  # Filename
    "sharedplaylistenabled-label": "Oynatma listesi paylaşımını etkinleştir",
    "removefromplaylist-menu-label": "Oynatma listesinden kaldır",
    "shuffleremainingplaylist-menu-label": "Kalan oynatma listesini karıştır",
    "shuffleentireplaylist-menu-label": "Tüm oynatma listesini karıştır",
    "undoplaylist-menu-label": "Oynatma listesindeki son değişikliği geri al",
    "addfilestoplaylist-menu-label": "Oynatma listesinin altına dosya(lar) ekle",
    "addurlstoplaylist-menu-label": "Oynatma listesinin altına URL('ler) ekle",
    "editplaylist-menu-label": "Oynatma listesini düzenle",

    "open-containing-folder": "Bu dosyayı içeren klasörü aç",
    "addyourfiletoplaylist-menu-label": "Dosyanızı oynatma listesine ekleyin",
    "addotherusersfiletoplaylist-menu-label": "{} kişisinin dosyasını oynatma listesine ekle",  # [Username]
    "addyourstreamstoplaylist-menu-label": "Akışınızı oynatma listesine ekleyin",
    "addotherusersstreamstoplaylist-menu-label": "Oynatma listesine {} kişisinin akışını ekleyin",  # [Username]
    "openusersstream-menu-label": "{} kişisinin akışını açın",  # [username]'s
    "openusersfile-menu-label": "{} kişisinin dosyasını açın",  # [username]'s

    "playlist-instruction-item-message": "Dosyayı paylaşılan çalma listesine eklemek için buraya sürükleyin.",
    "sharedplaylistenabled-tooltip": "Oda operatörleri, herkesin aynı şeyi izlemesini kolaylaştırmak için senkronize edilmiş bir çalma listesine dosya ekleyebilir. 'Misc' altında ortam dizinlerini yapılandırın.",

    "playlist-empty-error": "Oynatma listesi şu anda boş.",
    "playlist-invalid-index-error": "Geçersiz oynatma listesi dizini",
}
