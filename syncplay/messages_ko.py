# coding:utf8

"""Korean dictionary"""

# Filename, dictionary name and LANGUAGE-TAG value based on ISO country code. Language tag listed at https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/a9eac961-e77d-41a6-90a5-ce1a8b0cdb9c?redirectedfrom=MSDN

ko = {
    "LANGUAGE": "한국어",
    "LANGUAGE-TAG": "ko",

    # Strings for Windows NSIS installer
    "installer-language-file": "Korean.nlf", # Relevant .nlf file at https://github.com/kichik/nsis/tree/master/Contrib/Language%20files
    "installer-associate": "Syncplay를 멀티미디어 파일과 연결합니다.",
    "installer-shortcut": "다음 위치에 바로 가기 만들기:",
    "installer-start-menu": "시작 메뉴",
    "installer-desktop": "바탕화면",
    "installer-quick-launch-bar": "빠른 실행 표시줄",
    "installer-automatic-updates": "자동으로 업데이트 확인하기",
    "installer-uninstall-configuration": "구성 파일을 삭제합니다.",

    # Client notifications
    "config-cleared-notification": "설정이 지워졌습니다. 유효한 구성을 저장하면 변경사항이 저장됩니다.",

    "relative-config-notification": "불러온 관련 구성 파일: {}",

    "connection-attempt-notification": "{}:{}에 연결을 시도 중입니다",  # Port, IP
    "reconnection-attempt-notification": "서버와의 연결이 끊어져 다시 연결을 시도 중입니다.",
    "disconnection-notification": "서버에서 연결이 끊어졌습니다",
    "connection-failed-notification": "서버 연결에 실패했습니다.",
    "connected-successful-notification": "서버에 성공적으로 연결했습니다",
    "retrying-notification": "%s, %d초 후에 재시도 중...",  # Seconds
    "reachout-successful-notification": "성공적으로 {}에 연결되었습니다 ({})",

    "rewind-notification": "{}님과의 시간 차이로 인해 되감기되었습니다",  # User
    "fastforward-notification": "{}님과의 시간 차이로 인해 빨리감기되었습니다",  # User
    "slowdown-notification": "{}님과의 시간 차이로 인해 속도가 느려졌습니다",  # User
    "revert-notification": "속도를 정상으로 되돌리기",

    "pause-notification": "{}님이 {}에서 일시 중지되었습니다",  # User, Time
    "unpause-notification": "{}님이 일시중지 해제되었습니다",  # User
    "seek-notification": "{}님이 {}에서 {}로 점프했습니다",  # User, from time, to time

    "current-offset-notification": "현재 오프셋: {}초",  # Offset

    "media-directory-list-updated-notification": "Syncplay 미디어 디렉터리가 업데이트되었습니다.",

    "room-join-notification": "{}님이 방에 참여했습니다: '{}'",  # User
    "left-notification": "{}님이 떠났습니다",  # User
    "left-paused-notification": "{}님 떠남, {}님 일시중지됨",  # User who left, User who paused
    "playing-notification": "{}님의 재생중인 파일: '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum": " in room: '{}'",  # Room

    "not-all-ready": "준비되지 않음: {}님",  # Usernames
    "all-users-ready": "모두 준비됨 (사용자 {}명)",  # Number of ready users
    "ready-to-unpause-notification": "이제 준비됨으로 설정되었습니다. 일시중지를 해제하려면 일시중지를 다시 해제하세요",
    "set-as-ready-notification": "이제 준비됨으로 설정되었습니다",
    "set-as-not-ready-notification": "이제 준비되지 않음으로 설정되었습니다",
    "autoplaying-notification": "{}초 후 자동 재생...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "'{}' 비밀번호를 사용하여 방 운영자로 식별하는 중...",
    "failed-to-identify-as-controller-notification": "{}님이 방 운영자로 식별되지 않았습니다",
    "authenticated-as-controller-notification": "{}님이 방 운영자로 인증되었습니다",
    "created-controlled-room-notification": "'{}' 방을 '{}' 비밀번호로 관리되게 만들었습니다. 나중에 참조할 수 있도록 이 정보를 저장하세요!\n\n관리되는 방에서는 모든 사람이 재생목록을 일시 중지, 일시 중지 해제, 검색 및 변경할 수 있는 유일한 사람인 방 운영자와 동기화 상태를 유지합니다.\n\n일반 시청자에게 '{}' 방에 참여하도록 요청해야 하지만, 방 운영자는 '{}' 방에 참여하여 자동으로 자신을 인증할 수 있습니다.",  # RoomName, operatorPassword, roomName, roomName:operatorPassword

    "file-different-notification": "재생 중인 파일이 {}님의 파일과 다른 것 같습니다",  # User
    "file-differences-notification": "다음과 같은 방식으로 당신의 파일이 다릅니다: {}",  # Differences
    "room-file-differences": "파일 차이점: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "이름",
    "file-difference-filesize": "크기",
    "file-difference-duration": "재생시간",
    "alone-in-the-room": "당신은 방에 혼자입니다",

    "different-filesize-notification": " (그들의 파일 크기가 당신의 것과 다릅니다!)",
    "userlist-playing-notification": "{}님 재생 중:",  # Username
    "file-played-by-notification": "파일: {} 재생 중:",  # File
    "no-file-played-notification": "{}님은 파일을 재생하고 있지 않습니다",  # Username
    "notplaying-notification": "파일을 재생하지 않는 사용자:",
    "userlist-room-notification":  "In room '{}':",  # Room
    "userlist-file-notification": "파일",
    "controller-userlist-userflag": "운영자",
    "ready-userlist-userflag": "준비됨",

    "update-check-failed-notification": "Syncplay {}가 최신인지 자동으로 확인할 수 없습니다. 업데이트를 수동으로 확인하려면 https://syncplay.pl/을 방문하시겠습니까?",  # Syncplay version
    "syncplay-uptodate-notification": "Syncplay는 최신 버전입니다",
    "syncplay-updateavailable-notification": "Syncplay의 새 버전을 사용할 수 있습니다. 릴리스 페이지를 방문하시겠습니까?",

    "mplayer-file-required-notification": "mplayer를 사용하는 Syncplay는 시작할 때 파일을 제공해야 합니다",
    "mplayer-file-required-notification/example": "사용 예시: syncplay [옵션] [url|경로/]파일명",
    "mplayer2-required": "Syncplay는 MPlayer 1.x와 호환되지 않습니다. mplayer2 또는 mpv를 사용하세요",

    "unrecognized-command-notification": "인식할 수 없는 명령",
    "commandlist-notification": "사용 가능한 명령:",
    "commandlist-notification/room": "\tr [name] - 방 변경하기",
    "commandlist-notification/list": "\tl - 사용자 목록 표시하기",
    "commandlist-notification/undo": "\tu - 마지막 검색 실행취소",
    "commandlist-notification/pause": "\tp - 일시중지 전환하기",
    "commandlist-notification/seek": "\t[s][+-]time - 지정된 시간 값까지 탐색합니다(+ 또는 -가 지정되지 않은 경우 절대 시간(초) 또는 분:초)",
    "commandlist-notification/offset": "\to[+-]duration - 서버 탐색 위치에서 지정된 시간(초 또는 분:초)만큼 로컬 재생을 오프셋합니다 - 이 기능은 사용되지 않습니다",
    "commandlist-notification/help": "\th - 이 도움말",
    "commandlist-notification/toggle": "\tt - 시청 준비 여부를 전환합니다",
    "commandlist-notification/create": "\tc [name] - 현재 방의 이름을 사용하여 관리되는 방을 만듭니다",
    "commandlist-notification/auth": "\ta [password] - 운영자 비밀번호를 사용해 방 운영자로 인증합니다",
    "commandlist-notification/chat": "\tch [message] - 방에서 채팅 메시지를 전송합니다",
    "commandList-notification/queue": "\tqa [file/url] - 재생목록 하단에 파일 또는 URL을 추가합니다",
    "commandList-notification/queueandselect": "\tqas [file/url] - 재생목록 하단에 파일 또는 URL을 추가하고 선택합니다",
    "commandList-notification/playlist": "\tql - 현재 재생목록을 표시합니다",
    "commandList-notification/select": "\tqs [index] - 재생목록에서 지정된 항목을 선택합니다",
    "commandList-notification/next": "\tqn - 재생목록에서 다음 항목을 선택합니다",
    "commandList-notification/delete": "\tqd [index] - 재생목록에서 지정된 항목을 삭제합니다",
    "syncplay-version-notification": "Syncplay 버전: {}",  # syncplay.version
    "more-info-notification": "자세한 정보는 다음에서 확인하세요: {}",  # projectURL

    "gui-data-cleared-notification": "Syncplay가 GUI에서 사용하는 경로 및 창 상태 데이터를 지웠습니다.",
    "language-changed-msgbox-label": "Syncplay를 실행하면 언어가 변경됩니다.",
    "promptforupdate-label": "Syncplay가 수시로 업데이트를 자동으로 확인해도 괜찮습니까?",

    "media-player-latency-warning": "경고: 미디어 플레이어가 응답하는 데 {}초가 걸렸습니다. 동기화 이슈가 발생하면 응용 프로그램을 닫아 시스템 리소스를 확보하고 그래도 작동하지 않으면 다른 미디어 플레이어를 사용해 보세요.",  # Seconds to respond
    "mpv-unresponsive-error": "mpv가 {}초 동안 응답하지 않았으므로 오작동한 것 같습니다. Syncplay를 다시 시작하세요.",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "종료하려면 Enter 키를 누르세요.\n",

    # Client errors
    "missing-arguments-error": "일부 필요한 인수가 누락되었습니다. --help를 참조하세요.",
    "server-timeout-error": "서버와의 연결 시간이 초과되었습니다",
    "mpc-slave-error": "슬레이브 모드에서 MPC를 시작할 수 없습니다!",
    "mpc-version-insufficient-error": "MPC 버전이 충분하지 않은 경우, `mpc-hc` >= `{}`를 사용하세요",
    "mpc-be-version-insufficient-error": "MPC 버전이 충분하지 않은 경우, `mpc-be` >= `{}`를 사용하세요",
    "mpv-version-error": "Syncplay는 이 버전의 mpv와 호환되지 않습니다. 다른 버전의 mpv를 사용하세요 (e.g. Git HEAD).",
    "mpv-failed-advice": "mpv를 시작할 수 없는 이유는 지원되지 않는 명령줄 인수를 사용하거나 지원되지 않는 mpv 버전 때문일 수 있습니다.",
    "player-file-open-error": "플레이어가 파일을 열지 못했습니다",
    "player-path-error": "플레이어 경로가 제대로 설정되지 않았습니다. 지원되는 플레이어는 mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 및 IINA입니다.",
    "hostname-empty-error": "호스트이름은 비워둘 수 없습니다",
    "empty-error": "{}은(는) 비워 둘 수 없습니다",  # Configuration
    "media-player-error": "미디어 플레이어 오류: \"{}\"",  # Error line
    "unable-import-gui-error": "GUI 라이브러리를 가져올 수 없습니다. PySide가 설치되어 있지 않은 경우 GUI가 작동하려면 설치해야 합니다.",
    "unable-import-twisted-error": "Twisted를 가져올 수 없습니다. Twisted v16.4.0 이상을 설치하세요.",

    "arguments-missing-error": "일부 필요한 인수가 누락되었습니다. --help를 참조하세요.",

    "unable-to-start-client-error": "클라이언트를 시작할 수 없습니다",

    "player-path-config-error": "플레이어 경로가 제대로 설정되지 않았습니다. 지원되는 플레이어는 mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 및 IINA입니다.",
    "no-file-path-config-error": "플레이어를 시작하기 전에 파일을 선택해야 합니다",
    "no-hostname-config-error": "호스트이름은 비워둘 수 없습니다",
    "invalid-port-config-error": "포트가 유효해야 합니다",
    "empty-value-config-error": "{}은(는) 비워 둘 수 없습니다",  # Config option

    "not-json-error": "json으로 인코딩된 문자열이 아닙니다\n",
    "hello-arguments-error": "Not enough Hello arguments\n",  # DO NOT TRANSLATE
    "version-mismatch-error": "클라이언트와 서버의 버전이 일치하지 않습니다\n",
    "vlc-failed-connection": "VLC에 연결하지 못했습니다. syncplay.lua를 설치하지 않았고 최신 버전의 VLC를 사용 중인 경우 https://syncplay.pl/LUA/ 에서 지침을 참조하세요. Syncplay와 VLC 4는 현재 호환되지 않으므로 VLC 3 또는 mpv와 같은 대체 프로그램을 사용하세요.",
    "vlc-failed-noscript": "VLC에서 syncplay.lua 인터페이스 스크립트가 설치되지 않았다고 보고했습니다. 자세한 내용은 https://syncplay.pl/LUA/ 을 참조하세요.",
    "vlc-failed-versioncheck": "이 버전의 VLC는 Syncplay에서 지원되지 않습니다.",
    "vlc-initial-warning": 'VLC는 특히 .mp4 및 .avi 파일의 경우 Syncplay에 정확한 위치 정보를 항상 제공하지는 않습니다. 잘못된 검색에 문제가 있는 경우 <a href="https://mpv.io/">mpv</a>와 같은 대체 미디어 플레이어를 사용해 보세요. (또는 Windows 사용자의 경우 <a href="https://github.com/stax76/mpv.net/">mpv.net</a>)',

    "feature-sharedPlaylists": "공유 재생목록",  # used for not-supported-by-server-error
    "feature-chat": "채팅",  # used for not-supported-by-server-error
    "feature-readiness": "준비",  # used for not-supported-by-server-error
    "feature-managedRooms": "관리되는 방",  # used for not-supported-by-server-error

    "not-supported-by-server-error": "{} 기능은 이 서버에서 지원되지 않습니다..",  # feature
    "shared-playlists-not-supported-by-server-error": "공유 재생목록 기능은 서버에서 지원하지 않을 수 있습니다. 올바르게 작동하려면 Syncplay {}+를 실행하는 서버가 필요하지만 서버는 Syncplay {}를 실행하고 있습니다.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "서버 구성에서 공유 재생목록 기능이 비활성화되었습니다. 이 기능을 사용하려면 다른 서버에 연결해야 합니다.",

    "invalid-seek-value": "잘못된 탐색 값",
    "invalid-offset-value": "잘못된 오프셋 값",

    "switch-file-not-found-error": "'{0}' 파일로 전환할 수 없습니다. Syncplay는 지정된 미디어 디렉터리를 찾습니다.",  # File not found
    "folder-search-timeout-error": "'{}'을(를) 검색하는 데 너무 오래 걸리기 때문에 미디어 디렉터리에서 미디어 검색이 중단되었습니다. 미디어 폴더 목록에서 검색할 하위 폴더가 너무 많은 폴더를 선택하면 이 문제가 발생합니다. 자동 파일 전환이 다시 작동하도록 하려면 메뉴 표시줄에서 파일->미디어 디렉터리 설정을 선택하고 이 디렉터리를 제거하거나 적절한 하위 폴더로 바꾸세요. 폴더가 실제로 괜찮다면 파일->미디어 디렉터리 설정을 선택하고 '확인'을 눌러 폴더를 다시 활성화할 수 있습니다.",  # Folder
    "folder-search-first-file-timeout-error": "디렉터리에 액세스하는 데 시간이 너무 오래 걸려 '{}'의 미디어 검색이 중단되었습니다. 이는 네트워크 드라이브이거나 일정 시간 동안 사용하지 않으면 스핀다운하도록 드라이브를 구성한 경우에 발생할 수 있습니다. 자동 파일 전환이 다시 작동하려면 파일->미디어 디렉터리 설정으로 이동하여 디렉터리를 제거하거나 이슈를 해결하세요(예: 절전 설정 변경).",  # Folder
    "added-file-not-in-media-directory-error": "알려진 미디어 디렉터리가 아닌 '{}'에 파일을 로드했습니다. 메뉴 표시줄에서 파일->미디어 디렉터리 설정을 선택하여 이 파일을 미디어 디렉터리로 추가할 수 있습니다.",  # Folder
    "no-media-directories-error": "미디어 디렉터리가 설정되지 않았습니다. 공유 재생목록 및 파일 전환 기능이 제대로 작동하려면 파일->미디어 디렉터리 설정을 선택하고 Syncplay가 미디어 파일을 찾을 위치를 지정하세요.",
    "cannot-find-directory-error": "미디어 디렉터리 '{}'을 찾을 수 없습니다. 미디어 디렉터리 목록을 업데이트하려면 메뉴 표시줄에서 파일->미디어 디렉터리 설정을 선택하고 Syncplay가 미디어 파일을 찾을 위치를 지정하세요.",

    "failed-to-load-server-list-error": "공개 서버 목록을 로드하지 못했습니다. 브라우저에서 https://www.syncplay.pl/을 방문하세요.",

    # Client arguments
    "argument-description": '네트워크를 통해 여러 미디어 플레이어 인스턴스의 재생을 동기화하는 솔루션입니다.',
    "argument-epilog": '제공된 옵션이 없으면 _config 값이 사용됩니다',
    "nogui-argument": 'GUI 표시 안함',
    "host-argument": "서버의 주소",
    "name-argument": '원하는 사용자 이름',
    "debug-argument": '디버그 모드',
    "force-gui-prompt-argument": '구성 프롬프트가 나타나도록 합니다',
    "no-store-argument": ".syncplay에 값을 저장하지 않습니다",
    "room-argument": '기본 방',
    "password-argument": '서버 비밀번호',
    "player-path-argument": '플레이어 실행 파일의 경로',
    "file-argument": '재생할 파일',
    "args-argument": '플레이어 옵션, -로 시작하는 옵션을 전달해야 할 경우 단일 \'--\' 인수로 추가합니다',
    "clear-gui-data-argument": 'QSettings로 저장된 경로 및 창 상태 GUI 데이터를 재설정합니다',
    "language-argument": 'Syncplay 메시지의 언어 ({})', # Languages

    "version-argument": '사용자 버전 출력',
    "version-message": "Syncplay 버전 {} ({})을 사용하고 있습니다",

    "load-playlist-from-file-argument": "텍스트 파일에서 재생목록 불러오기 (한 줄에 하나의 항목)",


    # Client labels
    "config-window-title": "Syncplay 구성",

    "connection-group-title": "연결 설정",
    "host-label": "서버 주소: ",
    "name-label":  "사용자 이름 (선택 사항):",
    "password-label":  "서버 비밀번호(있는 경우):",
    "room-label": "기본 방: ",
    "roomlist-msgbox-label": "룸 목록 편집 (한 줄에 하나씩)",

    "media-setting-title": "미디어 플레이어 설정",
    "executable-path-label": "미디어 플레이어 경로:",
    "media-path-label": "비디오 경로 (선택 사항):",
    "player-arguments-label": "플레이어 인수 (있는 경우):",
    "browse-label": "찾아보기",
    "update-server-list-label": "목록 업데이트",

    "more-title": "더 많은 설정 표시하기",
    "never-rewind-value": "안함",
    "seconds-suffix": "초",
    "privacy-sendraw-option": "Raw 전송하기",
    "privacy-sendhashed-option": "Hashed 전송하기",
    "privacy-dontsend-option": "전송 안함",
    "filename-privacy-label": "파일 이름 정보:",
    "filesize-privacy-label": "파일 크기 정보:",
    "checkforupdatesautomatically-label": "자동으로 Syncplay 업데이트 확인",
    "autosavejoinstolist-label": "참여하는 방을 방 목록에 추가하기",
    "slowondesync-label": "마이너 동기화 해제 시 속도 저하 (MPC-HC/BE에서는 지원되지 않음)",
    "rewindondesync-label": "메이저 동기화 해제 시 되감기 (권장됨)",
    "fastforwardondesync-label": "뒤처지는 경우 빨리 감기 (권장됨)",
    "dontslowdownwithme-label": "다른 사람의 속도를 늦추거나 되감지 않음 (실험적)",
    "pausing-title": "일시 중지하는 중",
    "pauseonleave-label": "사용자가 떠날 때 일시 중지 (예: 연결이 끊긴 경우)",
    "readiness-title": "초기 준비 상태",
    "readyatstart-label": "기본적으로 '시청 준비됨'으로 설정",
    "forceguiprompt-label": "항상 Syncplay 구성 창을 표시하지 않음",  # (Inverted)
    "showosd-label": "OSD 메시지 활성화",
OSD 메시지 활성화
    "showosdwarnings-label": "경고 포함 (예: 파일이 다른 경우, 사용자가 준비되지 않음)",
    "showsameroomosd-label": "사용자의 방에 이벤트 포함하기",
    "shownoncontrollerosd-label": "관리되는 방에 비운영자의 이벤트 포함하기",
    "showdifferentroomosd-label": "다른 방에 이벤트 포함하기",
    "showslowdownosd-label": "알림 속도 늦추기 / 되돌리기 포함하기",
    "language-label": "언어:",
    "automatic-language": "기본값 ({})",  # Default language
    "showdurationnotification-label": "미디어 재생 시간 불일치에 대해 경고하기",
    "basics-label": "기본사항",
    "readiness-label": "재생/일시정지",
    "misc-label": "기타",
    "core-behaviour-title": "핵심 방 행동",
    "syncplay-internals-title": "Syncplay 내부",
    "syncplay-mediasearchdirectories-title": "미디어 검색을 위한 디렉터리",
    "syncplay-mediasearchdirectories-label": "미디어를 검색할 디렉터리 (한 줄에 하나의 경로)",
    "sync-label": "동기화",
    "sync-otherslagging-title": "다른 사람들이 뒤처져 있다면...",
    "sync-youlaggging-title": "사용자가 뒤처져 있다면...",
    "messages-label": "메시지",
    "messages-osd-title": "화면 디스플레이 설정",
    "messages-other-title": "기타 디스플레이 설정",
    "chat-label": "채팅",
    "privacy-label": "비공개",  # Currently unused, but will be brought back if more space is needed in Misc tab
    "privacy-title": "비공개 설정",
    "unpause-title": "재생을 누르면 준비 상태로 설정하고 다음을 수행합니다:",
    "unpause-ifalreadyready-option": "이미 준비 상태로 설정된 경우 일시중지 해제",
    "unpause-ifothersready-option": "이미 준비되었거나 방에 있는 다른 사람이 준비되면 일시중지 해제 (기본값)",
    "unpause-ifminusersready-option": "이미 준비되었거나 다른 모든 사용자가 준비되고 최소 사용자가 준비되었으면 일시중지 해제",
    "unpause-always": "항상 일시중지 해제",
    "syncplay-trusteddomains-title": "신뢰할 수 있는 도메인 (스트리밍 서비스 및 호스팅 콘텐츠용)",

    "chat-title": "채팅 메시지 입력",
    "chatinputenabled-label": "mpv를 통한 채팅 입력 활성화",
    "chatdirectinput-label": "인스턴트 채팅 입력 허용 (채팅에 엔터 키를 누르지 않아도 됨)",
    "chatinputfont-label": "채팅 입력 글꼴",
    "chatfont-label": "글꼴 설정",
    "chatcolour-label": "색상 설정",
    "chatinputposition-label": "mpv에서 메시지 입력 영역의 위치",
    "chat-top-option": "상단",
    "chat-middle-option": "중간",
    "chat-bottom-option": "하단",
    "chatoutputheader-label": "채팅 메시지 출력",
    "chatoutputfont-label": "채팅 출력 글꼴",
    "chatoutputenabled-label": "미디어 플레이어에서 채팅 출력 활성화 (지금은 mpv만 가능)",
    "chatoutputposition-label": "출력 모드",
    "chat-chatroom-option": "채팅방 스타일",
    "chat-scrolling-option": "스크롤 스타일",

    "mpv-key-tab-hint": "[Tab]을 눌러 알파벳 행 키 단축키에 대한 액세스를 전환합니다.",
    "mpv-key-hint": "[엔터]를 눌러 메시지를 보냅니다. [ESC]를 눌러 채팅 모드를 종료합니다.",
    "alphakey-mode-warning-first-line": "임시로 a-z 키가 포함된 이전 mpv 바인딩을 사용할 수 있습니다.",
    "alphakey-mode-warning-second-line": "Syncplay 채팅 모드로 돌아가려면 [TAB]을 누르세요.",

    "help-label": "도움말",
    "reset-label": "기본값 복원",
    "run-label": "Syncplay 실행하기",
    "storeandrun-label": "구성을 저장하고 Syncplay 실행하기",

    "contact-label": "언제든지 <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a>로 이메일을 보내주세요, GitHub를 통해 버그/문제를 보고하려면 <a href=\"https://github.com/Syncplay/syncplay/issues\"><nobr>이슈 만들기</nobr></a>, GitHub를 통해 제안하거나 질문을 하려면 <a href=\"https://github.com/Syncplay/syncplay/discussions\"><nobr>토론 시작</nobr></a>, <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>Facebook에서 좋아요</nobr></a>, <a href=\"https://twitter.com/Syncplay/\"><nobr>Twitter에서 팔로우</nobr></a >하거나, <a href=\"https://syncplay.pl/\"><nobr>https://syncplay.pl/</nobr></a>을 방문하세요. Syncplay를 사용하여 민감한 정보를 전송하지 마세요.",

    "joinroom-label": "방 참여하기",
    "joinroom-menu-label": "{} 방 참여하기",
    "seektime-menu-label": "시간으로 탐색",
    "undoseek-menu-label": "탐색 실행취소",
    "play-menu-label": "재생하기",
    "pause-menu-label": "일시중지",
    "playbackbuttons-menu-label": "재생 버튼 표시하기",
    "autoplay-menu-label": "자동 재생 버튼 표시하기",
    "autoplay-guipushbuttonlabel": "모든 준비가 완료되면 재생",
    "autoplay-minimum-label": "최소 사용자 수:",
    "hideemptyrooms-menu-label": "남아있는 빈 방 숨기기",

    "sendmessage-label": "전송하기",

    "ready-guipushbuttonlabel": "시청할 준비가 되었습니다!",

    "roomuser-heading-label": "방 / 사용자",
    "size-heading-label": "크기",
    "duration-heading-label": "길이",
    "filename-heading-label": "파일 이름",
    "notifications-heading-label": "알림",
    "userlist-heading-label": "누가 무엇을 재생하는지에 대한 목록",

    "browseformedia-label": "미디어 파일 찾아보기",

    "file-menu-label": "파일(&F)",  # & precedes shortcut key
    "openmedia-menu-label": "미디어 파일 열기(&O)",
    "openstreamurl-menu-label": "미디어 스트림 URL 열기(&M)",
    "setmediadirectories-menu-label": "미디어 디렉터리 설정(&D)",
    "loadplaylistfromfile-menu-label": "파일에서 재생목록 불러오기(&L)",
    "saveplaylisttofile-menu-label": "재생목록을 파일로 저장(&S)",
    "exit-menu-label": "종료(&X)",
    "advanced-menu-label": "고급(&A)",
    "window-menu-label": "창(&W)",
    "setoffset-menu-label": "오프셋 설정(&O)",
    "createcontrolledroom-menu-label": "관리되는 방 만들기(&C)",
    "identifyascontroller-menu-label": "방 운영자로 식별하기(&I)",
    "settrusteddomains-menu-label": "신뢰할 수 있는 도메인 설정(&T)",
    "addtrusteddomain-menu-label": "신뢰할 수 있는 도메인으로 {} 추가하기",  # Domain

    "edit-menu-label": "편집하기(&E)",
    "cut-menu-label": "잘라내기(&T)",
    "copy-menu-label": "복사하기(&C)",
    "paste-menu-label": "붙여넣기(&P)",
    "selectall-menu-label": "모두 선택(&S)",

    "playback-menu-label": "재생(&P)",

    "help-menu-label": "도움말(&H)",
    "userguide-menu-label": "사용자 가이드 열기(&G)",
    "update-menu-label": "업데이트 확인(&U)",

    "startTLS-initiated": "보안 연결 시도 중",
    "startTLS-secure-connection-ok": "보안 연결 설정됨 ({})",
    "startTLS-server-certificate-invalid": '보안 연결 실패. 서버가 유효하지 않은 보안 인증서를 사용합니다. 이 통신은 제3자가 가로챌 수 있습니다. 자세한 내용과 문제 해결은 <a href="https://syncplay.pl/trouble">여기</a>를 참조하세요.',
    "startTLS-server-certificate-invalid-DNS-ID": "Syncplay는 호스트 이름에 유효하지 않은 인증서를 사용하기 때문에 이 서버를 신뢰하지 않습니다.",
    "startTLS-not-supported-client": "이 클라이언트는 TLS를 지원하지 않습니다",
    "startTLS-not-supported-server": "이 서버는 TLS를 지원하지 않습니다",

    # TLS certificate dialog
    "tls-information-title": "인증서 세부정보",
    "tls-dialog-status-label": "<strong>Syncplay는 {}에 대해 암호화된 연결을 사용하고 있습니다.</strong>",
    "tls-dialog-desc-label": "디지털 인증서를 사용한 암호화는 정보가 서버 {}로 전송되거나 서버에서 전송될 때 비공개로 유지합니다.",
    "tls-dialog-connection-label": "암호화 스위트가 있는 TLS, {} 버전을 사용하여 암호화된 정보: {}.",
    "tls-dialog-certificate-label": "{}에서 발급한 인증서는 {}까지 유효합니다.",

    # About dialog
    "about-menu-label": "Syncplay 정보(&A)",
    "about-dialog-title": "Syncplay 정보",
    "about-dialog-release": "버전 {} 릴리스 {}",
    "about-dialog-license-text": "Apache&nbsp;라이선스,&nbsp;버전 2.0에 따라 라이센스가 부여되었습니다.",
    "about-dialog-license-button": "라이선스",
    "about-dialog-dependencies": "종속성",

    "setoffset-msgbox-label": "오프셋 설정",
    "offsetinfo-msgbox-label": "오프셋 (사용 지침은 https://syncplay.pl/guide/ 참조):",

    "promptforstreamurl-msgbox-label": "미디어 스트림 URL 열기",
    "promptforstreamurlinfo-msgbox-label": "스트림 URL",

    "addfolder-label": "폴더 추가하기",

    "adduris-msgbox-label": "재생목록에 URL 추가 (한 줄에 하나씩)",
    "editplaylist-msgbox-label": "재생목록 설정 (한 줄에 하나씩)",
    "trusteddomains-msgbox-label": "자동으로 전환해도 되는 도메인 (한 줄에 하나씩)",

    "createcontrolledroom-msgbox-label": "관리되는 방 만들기",
    "controlledroominfo-msgbox-label": "관리되는 방 이름 입력\r\n(사용 지침은 https://syncplay.pl/guide/ 참조):",

    "identifyascontroller-msgbox-label": "방 운영자로 식별하기",
    "identifyinfo-msgbox-label": "이 방의 운영자 비밀번호 입력하기\r\n(사용 지침은 https://syncplay.pl/guide/ 참조):",

    "public-server-msgbox-label": "이 보기 세션에 대한 공개 서버 선택",

    "megabyte-suffix": " MB",

    # Tooltips

    "host-tooltip": "연결할 호스트 이름 또는 IP, 선택적으로 포트 포함(예: syncplay.pl:8999). 동일한 서버/포트에 있는 사람들과만 동기화됩니다.",
    "name-tooltip": "나를 알릴 닉네임입니다. 등록할 필요가 없으므로 나중에 쉽게 변경할 수 있습니다. 지정하지 않으면 임의의 이름이 생성됩니다.",
    "password-tooltip": "비밀번호는 비공개 서버에 연결할 때만 필요합니다.",
    "room-tooltip": "연결 시 참여할 수 있는 방은 거의 모든 것이 가능하지만, 같은 방에 있는 사람들과만 동기화됩니다.",

    "edit-rooms-tooltip": "방 목록을 편집합니다.",

    "executable-path-tooltip": "선택한 지원 미디어 플레이어(mpv, mpv.net, VLC, MPC-HC/BE, mplayer2 또는 IINA)의 위치입니다.",
    "media-path-tooltip": "열려는 비디오 또는 스트림의 위치입니다. mplayer2에 필요합니다.",
    "player-arguments-tooltip": "이 미디어 플레이어에 전달할 추가 명령줄 인수/스위치입니다.",
    "mediasearcdirectories-arguments-tooltip": "Syncplay가 미디어 파일을 검색할 디렉터리, 예: 클릭하여 전환 기능을 사용할 때. Syncplay는 하위 폴더를 재귀적으로 살펴봅니다.",

    "more-tooltip": "자주 사용하지 않는 설정을 표시합니다.",
    "filename-privacy-tooltip": "현재 재생 중인 파일명을 서버로 전송하기 위한 비공개 모드입니다.",
    "filesize-privacy-tooltip": "현재 재생 중인 파일의 크기를 서버로 전송하는 비공개 모드입니다.",
    "privacy-sendraw-tooltip": "이 정보를 난독화하지 않고 전송합니다. 대부분의 기능에서 이 옵션이 기본값으로 설정되어 있습니다.",
    "privacy-sendhashed-tooltip": "해시된 버전의 정보를 전송하여 다른 클라이언트가 볼 수 없도록 합니다.",
    "privacy-dontsend-tooltip": "이 정보를 서버로 보내지 마세요. 이렇게 하면 개인정보가 최대한 보호됩니다.",
    "checkforupdatesautomatically-tooltip": "Syncplay 웹사이트를 정기적으로 확인하여 새 버전의 Syncplay를 사용할 수 있는지 확인하세요.",
    "autosavejoinstolist-tooltip": "서버의 방에 참여할 때 참여할 방 목록에서 자동으로 방 이름을 기억합니다.",
    "slowondesync-tooltip": "필요한 경우 재생 속도를 일시적으로 줄여 다른 시청자와 동기화할 수 있습니다. MPC-HC/BE에서는 지원되지 않습니다.",
    "dontslowdownwithme-tooltip": "재생이 느려지거나 되감기는 경우에도 다른 사람들이 느려지거나 되감기지 않도록 합니다. 방 운영자에게 유용합니다.",
    "pauseonleave-tooltip": "연결이 끊기거나 누군가 방에서 나가면 재생을 일시 중지합니다.",
    "readyatstart-tooltip": "시작 시 자신을 '준비됨'으로 설정합니다(그렇지 않으면 준비 상태를 변경할 때까지 '준비되지 않음'으로 설정됨).",
    "forceguiprompt-tooltip": "동기화 재생으로 파일을 열 때 구성 대화 상자가 표시되지 않습니다.",  # (Inverted)
    "nostore-tooltip": "주어진 구성으로 Syncplay를 실행하지만 변경 사항을 영구적으로 저장하지 마세요.",  # (Inverted)
    "rewindondesync-tooltip": "다시 동기화하기 위해 필요할 때 뒤로 이동합니다. 이 옵션을 비활성화하면 심각한 비동기화가 발생할 수 있습니다!",
    "fastforwardondesync-tooltip": "룸 오퍼레이터와 동기화되지 않은 경우 앞으로 이동합니다(또는 '다른 사람의 속도를 늦추거나 되감지 않음'이 활성화된 경우 가장한 위치).",
    "showosd-tooltip": "미디어 플레이어 OSD에 Syncplay 메시지를 보냅니다.",
    "showosdwarnings-tooltip": "다른 파일을 재생하는 경우, 방에 혼자 있는 경우, 사용자가 준비되지 않은 경우 등의 경고를 표시합니다.",
    "showsameroomosd-tooltip": "방 사용자와 관련된 이벤트에 대한 OSD 알림을 표시합니다.",
    "shownoncontrollerosd-tooltip": "관리되는 방에 있는 비운영자와 관련된 이벤트에 대한 OSD 알림을 표시합니다.",
    "showdifferentroomosd-tooltip": "방 사용자가 참석하지 않은 것과 관련된 이벤트에 대한 OSD 알림을 표시합니다.",
    "showslowdownosd-tooltip": "시차에 따라 느려지거나 되돌리는 알림을 표시합니다.",
    "showdurationnotification-tooltip": "여러 부분으로 구성된 파일의 세그먼트가 누락되었지만 잘못된 긍정이 발생할 수 있는 경우에 유용합니다.",
    "language-tooltip": "Syncplay에서 사용할 언어입니다.",
    "unpause-always-tooltip": "일시 중지 해제를 누르면 그냥 준비 상태로 설정하는 것이 아니라 항상 준비 상태로 설정하고 일시 중지를 해제합니다.",
    "unpause-ifalreadyready-tooltip": "준비되지 않았을 때 일시정지 해제를 누르면 준비 상태로 설정됩니다. 다시 일시정지를 해제하려면 일시정지 해제를 누르세요.",
    "unpause-ifothersready-tooltip": "준비되지 않았을 때 일시정지 해제를 누르면 다른 사람이 준비되었을 때만 일시정지가 해제됩니다.",
    "unpause-ifminusersready-tooltip": "준비되지 않았을 때 일시중지 해제를 누르면 다른 사용자가 준비되고 최소 사용자 임계값을 충족하는 경우에만 일시중지가 해제됩니다.",
    "trusteddomains-arguments-tooltip": "공유 재생목록이 활성화되면 Syncplay가 자동으로 전환해도 되는 도메인입니다.",

    "chatinputenabled-tooltip": "mpv에서 채팅 입력 활성화(채팅하려면 Enter 키를 누르고, 보내려면 Enter 키를 누르고, 취소하려면 Esc 키를 누르세요)",
    "chatdirectinput-tooltip": "Skip는 mpv에서 채팅 입력 모드로 들어가려면 'Enter'를 눌러야 합니다. 이 기능을 일시적으로 비활성화하려면 mpv에서 TAB을 누르세요.",
    "font-label-tooltip": "mpv에서 채팅 메시지를 입력할 때 사용하는 글꼴입니다. 클라이언트 측 전용이므로 다른 사람이 보는 것에 영향을 미치지 않습니다.",
    "set-input-font-tooltip": "mpv에서 채팅 메시지를 입력할 때 사용되는 글꼴 모음입니다. 클라이언트 측 전용이므로 다른 사람이 보는 것에 영향을 미치지 않습니다.",
    "set-input-colour-tooltip": "mpv에서 채팅 메시지를 입력할 때 사용되는 글꼴 색상입니다. 클라이언트 측 전용이므로 다른 사람이 보는 것에 영향을 미치지 않습니다.",
    "chatinputposition-tooltip": "Enter 키를 누르고 입력할 때 채팅 입력 텍스트가 나타나는 mpv의 위치입니다.",
    "chatinputposition-top-tooltip": "mpv 창 상단에 채팅 입력을 배치합니다.",
    "chatinputposition-middle-tooltip": "mpv 창의 정중앙에 채팅 입력을 배치합니다.",
    "chatinputposition-bottom-tooltip": "mpv 창 하단에 채팅 입력을 배치합니다.",
    "chatoutputenabled-tooltip": "OSD에서 채팅 메시지를 표시합니다(미디어 플레이어에서 지원하는 경우).",
    "font-output-label-tooltip": "채팅 출력 글꼴입니다.",
    "set-output-font-tooltip": "채팅 메시지를 표시할 때 사용하는 글꼴입니다.",
    "chatoutputmode-tooltip": "채팅 메시지가 표시되는 방식입니다.",
    "chatoutputmode-chatroom-tooltip": "이전 줄 바로 아래에 새 채팅 줄을 표시합니다.",
    "chatoutputmode-scrolling-tooltip": "채팅 텍스트를 오른쪽에서 왼쪽으로 스크롤합니다.",

    "help-tooltip": "Syncplay.pl 사용자 가이드를 엽니다.",
    "reset-tooltip": "모든 설정을 기본 구성으로 재설정합니다.",
    "update-server-list-tooltip": "syncplay.pl에 연결하여 공개 서버 목록을 업데이트합니다.",

    "sslconnection-tooltip": "서버에 안전하게 연결되었습니다. 인증서 세부 정보를 보려면 클릭합니다.",

    "joinroom-tooltip": "현재 방에서 나와 지정된 방에 참여합니다.",
    "seektime-msgbox-label": "지정된 시간으로 이동합니다(초/분:초 단위). 상대적 검색에는 +/-를 사용합니다.",
    "ready-tooltip": "시청할 준비가 되었는지 여부를 표시합니다.",
    "autoplay-tooltip": "준비 상태 표시기가 있는 모든 사용자가 준비되고 최소 사용자 임계값이 충족되면 자동 재생됩니다.",
    "switch-to-file-tooltip": "두 번 클릭하여 {}로 전환",  # Filename
    "sendmessage-tooltip": "방에 메시지 전송하기",

    # In-userlist notes (GUI)
    "differentsize-note": "크기가 다릅니다!",
    "differentsizeandduration-note": "크기와 재생시간이 다릅니다!",
    "differentduration-note": "재생시간이 다릅니다!",
    "nofile-note": "(재생 중인 파일 없음)",

    # Server messages to client
    "new-syncplay-available-motd-message": "Syncplay {}를 사용 중이지만 https://syncplay.pl에서 최신 버전을 사용할 수 있습니다",  # ClientVersion
    "persistent-rooms-notice": "NOTICE: This server uses persistent rooms, which means that the playlist information is stored between playback sessions. If you want to create a room where information is not saved then put -temp at the end of the room name.", # NOTE: Do not translate the word -temp

    # Server notifications
    "welcome-server-notification": "Syncplay 서버에 오신 것을 환영합니다. 버전 {0}",  # version
    "client-connected-room-server-notification": "{0}({2})님이 '{1}' 방에 연결되었습니다",  # username, host, room
    "client-left-server-notification": "{0}님이 서버에서 나갔습니다",  # name
    "no-salt-notification": "참고: 서버가 다시 시작될 때 이 서버 인스턴스에서 생성된 방 운영자 비밀번호가 계속 작동하도록 하려면 나중에 Syncplay 서버를 실행할 때 다음 명령줄 인수를 추가하세요. --salt {}",  # Salt


    # Server arguments
    "server-argument-description": '네트워크를 통해 여러 미디어 플레이어 인스턴스의 재생을 동기화하는 솔루션입니다. 서버 인스턴스',
    "server-argument-epilog": '제공된 옵션이 없으면 _config 값이 사용됩니다.',
    "server-port-argument": '서버 TCP 포트',
    "server-password-argument": '서버 비밀번호',
    "server-isolate-room-argument": '방을 격리하시겠습니까?',
    "server-salt-argument": "관리되는 방 비밀번호를 생성하는 데 사용되는 임의의 문자열",
    "server-disable-ready-argument": "준비 기능 비활성화",
    "server-motd-argument": "motd를 가져올 파일 경로",
    "server-rooms-argument": "남아있는 방 데이터를 저장하는 데 사용하거나 생성할 데이터베이스 파일의 경로입니다. 감시자 없이 재시작을 통해 방을 지속할 수 있도록 합니다.",
    "server-permanent-rooms-argument": "방이 비어 있어도 나열되는 남아있는 방을 나열하는 파일 경로 (한 줄에 하나의 방이 나열되는 텍스트 파일 형식) - 영구 방을 활성화해야 합니다.",
    "server-chat-argument": "채팅을 비활성화하시겠습니까?",
    "server-chat-maxchars-argument": "채팅 메시지의 최대 문자 수 (기본값은 {})", # Default number of characters
    "server-maxusernamelength-argument": "사용자 이름의 최대 문자 수 (기본값은 {})",
    "server-stats-db-file-argument": "제공된 SQLite db 파일을 사용하여 서버 통계 활성화",
    "server-startTLS-argument": "제공된 경로의 인증서 파일을 사용하여 TLS 연결 활성화",
    "server-messed-up-motd-unescaped-placeholders": "오늘의 메시지에는 이스케이프 처리되지 않은 자리 표시자가 있습니다. 모든 $ 기호는 이중($$)이어야 합니다.",
    "server-messed-up-motd-too-long": "오늘의 메시지가 너무 깁니다 - 최대 {}자, {}개까지만 허용됩니다.",

    # Server errors
    "unknown-command-server-error": "알 수 없는 명령 {}",  # message
    "not-json-server-error": "json으로 인코딩된 문자열 {}이 아닙니다",  # message
    "line-decode-server-error": "utf-8 문자열이 아닙니다",
    "not-known-server-error": "이 명령을 보내기 전에 서버에 알려야 합니다",
    "client-drop-server-error": "클라이언트 드롭: {} -- {}",  # host, error
    "password-required-server-error": "비밀번호 필요함",
    "wrong-password-server-error": "잘못된 비밀번호 입력됨",
    "hello-server-error": "Not enough Hello arguments",  # DO NOT TRANSLATE

    # Playlists
    "playlist-selection-changed-notification":  "{}님이 재생목록 선택을 변경했습니다",  # Username
    "playlist-contents-changed-notification": "{}님이 재생목록을 업데이트했습니다",  # Username
    "cannot-find-file-for-playlist-switch-error": "재생목록 전환을 위한 미디어 디렉터리에서 {} 파일을 찾을 수 없습니다!",  # Filename
    "cannot-add-duplicate-error": "중복이 허용되지 않으므로 '{}'에 대한 두 번째 항목을 재생목록에 추가할 수 없습니다.",  # Filename
    "cannot-add-unsafe-path-error": "신뢰할 수 있는 도메인에 없기 때문에 {}를 자동으로 로드할 수 없습니다. 재생목록에서 URL을 두 번 클릭하여 수동으로 URL로 전환하고 파일->고급->신뢰할 수 있는 도메인 설정을 통해 신뢰할 수 있는 도메인을 추가할 수 있습니다. URL을 마우스 오른쪽 버튼으로 클릭하면 컨텍스트 메뉴를 통해 해당 도메인을 신뢰할 수 있는 도메인으로 추가할 수 있습니다.",  # Filename
    "sharedplaylistenabled-label": "공유 재생목록 활성화",
    "removefromplaylist-menu-label": "재생목록에서 제거",
    "shuffleremainingplaylist-menu-label": "남은 재생목록 순서섞기",
    "shuffleentireplaylist-menu-label": "전체 재생목록 순서섞기",
    "undoplaylist-menu-label": "재생목록의 마지막 변경 사항 실행취소",
    "addfilestoplaylist-menu-label": "재생목록 하단에 파일 추가하기",
    "addurlstoplaylist-menu-label": "재생목록 하단에 URL 추가하기",
    "editplaylist-menu-label": "재생목록 편집",

    "open-containing-folder": "이 파일이 포함된 폴더 열기",
    "addyourfiletoplaylist-menu-label": "사용자의 재생목록에 파일 추가하기",
    "addotherusersfiletoplaylist-menu-label": "{}님의 파일을 재생목록에 추가하기",  # [Username]
    "addyourstreamstoplaylist-menu-label": "사용자의 재생목록에 스트림 추가하기",
    "addotherusersstreamstoplaylist-menu-label": "재생목록에 {}' 스트림 추가하기",  # [Username]
    "openusersstream-menu-label": "{}의 스트림 열기",  # [username]'s
    "openusersfile-menu-label": "{}의 파일 열기",  # [username]'s

    "playlist-instruction-item-message": "파일을 여기로 드래그하여 공유 재생목록에 추가하세요.",
    "sharedplaylistenabled-tooltip": "방 운영자는 동기화된 재생목록에 파일을 추가하여 모든 사람이 쉽게 같은 내용을 볼 수 있도록 할 수 있습니다. '기타'에서 미디어 디렉터리를 구성합니다.",

    "playlist-empty-error": "현재 재생목록이 비어 있습니다.",
    "playlist-invalid-index-error": "잘못된 재생목록 색인",
}
