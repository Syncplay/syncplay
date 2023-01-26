# coding:utf8

"""Simplified Chinese dictionary"""

# Filename, dictionary name and LANGUAGE-TAG value based on ISO country code. Language tag listed at https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/a9eac961-e77d-41a6-90a5-ce1a8b0cdb9c?redirectedfrom=MSDN

zh_CN = {
    "LANGUAGE": "简体中文",
    "LANGUAGE-TAG": "zh_CN",

    # Strings for Windows NSIS installer
    "installer-language-file": "SimpChinese.nlf", # Relevant .nlf file at https://github.com/kichik/nsis/tree/master/Contrib/Language%20files
    "installer-associate": "将Syncplay与多媒体文件关联。",
    "installer-shortcut": "在以下位置创建快捷方式:",
    "installer-start-menu": "开始菜单",
    "installer-desktop": "桌面",
    "installer-quick-launch-bar": "快速启动栏",
    "installer-automatic-updates": "自动检查更新",
    "installer-uninstall-configuration": "删除配置文件",

    # Client notifications
    "config-cleared-notification": "设置已清除。 当你存储一个有效的配置时，更改将被保存。",

    "relative-config-notification": "已加载的相对配置文件:{}",

    "connection-attempt-notification": "正在尝试连接{}:{}",  # Port, IP
    "reconnection-attempt-notification": "服务器连接中断，正在尝试重连",
    "disconnection-notification": "与服务器连接中断",
    "connection-failed-notification": "服务器连接失败",
    "connected-successful-notification": "服务器连接成功",
    "retrying-notification": "%s，%d秒内将重试...",  # Seconds
    "reachout-successful-notification": "成功连入{}（{}）",

    "rewind-notification": "与{}不同步，已回放",  # User
    "fastforward-notification": "与{}不同步，已快进",  # User
    "slowdown-notification": "与{}不同步，正在慢速播放",  # User
    "revert-notification": "播放速度恢复一倍速",

    "pause-notification": "{}暂停了 ({})",  # User, Time - TODO: Change into format "{} paused at {}" in line with English message
    "unpause-notification": "{}重新开始播放",  # User
    "seek-notification": "{}从{}跳转到{}",  # User, from time, to time

    "current-offset-notification": "当前偏移量：{}秒",  # Offset

    "media-directory-list-updated-notification": "Syncplay的媒体文件目录已更新。",

    "room-join-notification": "{}加入了'{}'房间",  # User
    "left-notification": "{}离开了房间",  # User
    "left-paused-notification": "{}离开了房间，{}暂停了",  # User who left, User who paused
    "playing-notification": "{}正在播放'{}' (时长{})",  # User, file, duration
    "playing-notification/room-addendum": "正在'{}'房间",  # Room

    "not-all-ready": "{}还未准备",  # Usernames
    "all-users-ready": "所有人已准备（共{}人）",  # Number of ready users
    "ready-to-unpause-notification": "您已准备，按下播放键可继续播放",
    "set-as-ready-notification": "您已准备",
    "set-as-not-ready-notification": "您已取消准备",
    "autoplaying-notification": "{}秒后将自动开始...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "用密码'{}'认证为管理员...",
    "failed-to-identify-as-controller-notification": "{}未能成为管理员",
    "authenticated-as-controller-notification": "{}成为了管理员",
    "created-controlled-room-notification": "已创建房间：'{}' ，密码是'{}'。请保存好以上信息以备用！\n\n只有房主或管理员可以暂停，继续播放，跳转播放，改变播放列表。每个人都与房主或管理员的播放进度同步。\n\n最近观看过的人都可加入'{}'房间，但只有房主或管理员在加入'{}'房间时才会自动认证为管理员。",  # RoomName, operatorPassword, roomName, roomName:operatorPassword

    "file-different-notification": "您正在播放的视频与{}不一致",  # User
    "file-differences-notification": "你们播放的视频文件{}不一致",  # Differences
    "room-file-differences": "播放文件不同点：{}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "名称",
    "file-difference-filesize": "大小",
    "file-difference-duration": "时长",
    "alone-in-the-room": "您正在一人观看",

    "different-filesize-notification": "（其他人的视频文件大小和您的不一致！）",
    "userlist-playing-notification": "{}正在播放：",  # Username
    "file-played-by-notification": "{}由以下用户播放：",  # File
    "no-file-played-notification": "{}无视频供开始播放",  # Username
    "notplaying-notification": "以下用户没有视频供开始播放：",
    "userlist-room-notification":  "房间'{}'里面有：",  # Room
    "userlist-file-notification": "视频文件",
    "controller-userlist-userflag": "管理员",
    "ready-userlist-userflag": "已准备",

    "update-check-failed-notification": "无法自动检测Syncplay{}版本是否最新。是否前往https://syncplay.pl/手动更新？",  # Syncplay version
    "syncplay-uptodate-notification": "Syncplay版本已最新",
    "syncplay-updateavailable-notification": "Syncplay已有更新版本。是否前往最新版本页面？",

    "mplayer-file-required-notification": "如使用mplayer播放器，您需要在开始前手动加入视频文件。",
    "mplayer-file-required-notification/example": "使用示例：syncplay [options] [url|path/]filename",
    "mplayer2-required": "Syncplay与MPlayer 1.x版本不兼容，请使用mplayer2或mpv（推荐）播放器",

    "unrecognized-command-notification": "未知命令",
    "commandlist-notification": "您可使用如下命令：",
    "commandlist-notification/room": "\tr [name] - 切换房间",
    "commandlist-notification/list": "\tl - 显示房间所有用户",
    "commandlist-notification/undo": "\tu - 撤销上次跳转",
    "commandlist-notification/pause": "\tp - 暂停/继续播放",
    "commandlist-notification/seek": "\t[s][+-]time - 跳转指定时长，如果未输入 + 或 - ，将会跳转到输入的时间节点（时间节点输入格式可为秒或分：秒）",
    "commandlist-notification/offset": "\to[+-]duration - 将本地的播放偏移量设置为给定时长（输入格式可为秒或分：秒），您的本地播放进度将与服务器不一致，因此极不推荐使用该设置",
    "commandlist-notification/help": "\th - 帮助菜单",
    "commandlist-notification/toggle": "\tt - 准备/取消准备",
    "commandlist-notification/create": "\tc [name] - 以给定房间名创建一个由您管理的房间",
    "commandlist-notification/auth": "\ta [password] - 用给定密码来认证为管理员",
    "commandlist-notification/chat": "\tch [message] - 发送聊天信息",
    "commandList-notification/queue": "\tqa [file/url] - 在播放列表最后添加文件或URL",
    "commandList-notification/queueandselect": "\tqas [file/url] - 在播放列表最后添加文件或URL并选中",
    "commandList-notification/playlist": "\tql - 显示当前播放列表",
    "commandList-notification/select": "\tqs [index] - 选中播放列表中指定序号的视频",
    "commandList-notification/next": "\tqn - select next entry in the playlist", # TODO: Translate
    "commandList-notification/delete": "\tqd [index] - 删除播放列表中指定序号的视频",
    "syncplay-version-notification": "当前Syncplay版本为{}",  # syncplay.version
    "more-info-notification": "更多信息请参照{}",  # projectURL

    "gui-data-cleared-notification": "Syncplay已经清除了GUI使用的路径和窗口状态数据。",
    "language-changed-msgbox-label": "当您运行Syncplay时，界面将切换为中文",
    "promptforupdate-label": "是否让Syncplay自动检查更新？",

    "media-player-latency-warning": "警告：播放器用了{}秒响应。如果您遇到播放不同步问题，请关闭其他应用以清理内存。如果仍无法解决问题，建议您更换其他播放器。",  # Seconds to respond
    "mpv-unresponsive-error": "mpv播放器在{}秒之内无反应，可能出现故障。请尝试重启Syncplay。",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "Press enter to exit\n",

    # Client errors
    "missing-arguments-error": "缺少一些必要的参数，使用--help命令查看详细信息",
    "server-timeout-error": "与服务器的连接超时",
    "mpc-slave-error": "无法在从属模式下启动MPC！",
    "mpc-version-insufficient-error": "MPC版本过低，请使用mpc-hc{}以上版本",
    "mpc-be-version-insufficient-error": "MPC版本过低，请使用mpc-be{}以上版本",
    "mpv-version-error": "Syncplay与此版本的mpv不兼容。请使用其他版本的mpv（例如：Git HEAD）。",
    "mpv-failed-advice": "mpv不能启动的原因可能是由于使用了不支持的命令行参数或不支持的mpv版本。",
    "player-file-open-error": "播放器打开文件失败",
    "player-path-error": "播放器路径设置不正确。支持的播放器有：mpv、mpv.net、VLC、MPC-HC、MPC-BE、mplayer2和IINA。",
    "hostname-empty-error": "主机名不能是空的",
    "empty-error": "{}不能是空的",  # Configuration
    "media-player-error": "媒体播放器错误：\"{}\"",  # Error line
    "unable-import-gui-error": "无法导入GUI库。如果你没有安装PySide，GUI则无法工作，请安装PySide。",
    "unable-import-twisted-error": "无法导入Twisted。请安装Twisted v16.4.0或更高版本。",

    "arguments-missing-error": "缺少一些必要的参数，使用--help命令查看详细信息",

    "unable-to-start-client-error": "无法启动客户端",

    "player-path-config-error": "播放器路径设置不正确。支持的播放器有：mpv、mpv.net、VLC、MPC-HC、MPC-BE、mplayer2和IINA。",
    "no-file-path-config-error": "在启动播放器之前，必须选择要播放的文件",
    "no-hostname-config-error": "主机名不能是空的",
    "invalid-port-config-error": "端口无效",
    "empty-value-config-error": "{}不能是空的",  # Config option

    "not-json-error": "不是一个json编码的字符串\n",
    "hello-arguments-error": "Not enough Hello arguments\n",  # DO NOT TRANSLATE
    "version-mismatch-error": "客户端和服务器的版本不匹配\n",
    "vlc-failed-connection": "连接VLC失败。如果你没有安装syncplay.lua并且使用最新版本的VLC，那么请参考https://syncplay.pl/LUA/。Syncplay和VLC 4目前并不兼容，所以请使用VLC 3或mpv等替代软件。",
    "vlc-failed-noscript": "VLC报告没有安装syncplay.lua接口脚本。请参考https://syncplay.pl/LUA/获得指导。",
    "vlc-failed-versioncheck": "Syncplay不支持这个版本的VLC。",
    "vlc-initial-warning": 'VLC无法给Syncplay提供准确进度信息，尤其是在播放.mp4和.avi文件时。如果您遇到了跳转错误的问题，请使用其他播放器例如<a href="https://mpv.io/">mpv</a>（或者为Windows用户提供的<a href="https://github.com/stax76/mpv.net/">mpv.net</a>）。',

    "feature-sharedPlaylists": "共享播放列表",  # used for not-supported-by-server-error
    "feature-chat": "聊天",  # used for not-supported-by-server-error
    "feature-readiness": "准备状态",  # used for not-supported-by-server-error
    "feature-managedRooms": "房间管理",  # used for not-supported-by-server-error

    "not-supported-by-server-error": "该服务器不支持{}功能",  # feature
    "shared-playlists-not-supported-by-server-error": "服务器可能不支持共享播放列表的功能。为确保其正常运行，需要一个运行Syncplay {}以上版本的服务器，但服务器是运行Syncplay {}的。",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "在服务器配置中，共享播放列表功能已被禁用。要使用这一功能，你需要连接到其他服务器。",

    "invalid-seek-value": "无效的跳转值",
    "invalid-offset-value": "无效的偏移值",

    "switch-file-not-found-error": "无法切换到视频文件'{0}'。Syncplay只在指定的媒体目录中查找文件。",  # File not found
    "folder-search-timeout-error": "在媒体目录中搜索媒体文件时，由于在'{}'中搜索时间过长而中止。如果你在要搜索的媒体文件夹列表中选择了一个子文件夹过多的文件夹，就会出现这种情况。为了使自动文件切换再次工作，请在菜单栏中选择\"文件->设置媒体目录\"，并删除这个目录或用一个适当的子文件夹替换它。如果这个文件夹实际上是适当的，那么你可以通过选择\"文件->设置媒体目录\"并按\"确定\"来重新启用它。",  # Folder
    "folder-search-first-file-timeout-error": "搜索'{}'中的媒体文件时，由于访问该目录的时间太长而被中止。如果该目录位于网络驱动器，或者如果你配置了你的驱动器在一段时间不活动后停止工作，就会发生这种情况。为了能够自动切换播放文件，请进入\"文件->设置媒体目录\"，并删除该目录或解决这个问题（还可尝试其他解决方式，例如，改变省电设置）。",  # Folder
    "added-file-not-in-media-directory-error": "你在'{}'中加载了一个文件，该媒体目录尚未保存。你可以通过选择菜单栏中的\"文件->设置媒体目录\"将其保存为指定媒体目录。",  # Folder
    "no-media-directories-error": "没有设置媒体目录。为了使共享播放列表和文件切换功能正常工作，请选择\"文件->设置媒体目录\"，并指定Syncplay应该在哪里寻找媒体文件。",
    "cannot-find-directory-error": "无法找到媒体目录'{}'。要更新您的媒体目录列表，请从菜单栏中选择\"文件->设置媒体目录\"，并指定Syncplay应该在哪里寻找媒体文件。",

    "failed-to-load-server-list-error": "载入公共服务器列表失败。请在您的浏览器中访问https://www.syncplay.pl/以获得更多信息。",

    # Client arguments
    "argument-description": '通过网络来同步多个媒体播放器的解决方案',
    "argument-epilog": '如果没有提供可选值，将使用配置文件中的值',
    "nogui-argument": '不显示GUI',
    "host-argument": "服务器地址",
    "name-argument": '用户名',
    "debug-argument": '调试模式',
    "force-gui-prompt-argument": '显示配置提示信息',
    "no-store-argument": "不要将值保存在.syncplay",
    "room-argument": '默认房间',
    "password-argument": '服务器密码',
    "player-path-argument": '播放器路径',
    "file-argument": '待播放文件',
    "args-argument": '播放器选项，如果你需要传递以-开头的选项，请在它们前面加上一个\'--\'开头',
    "clear-gui-data-argument": '重置存储为QSettings的路径和窗口状态GUI数据。',
    "language-argument": 'Syncplay消息的语言 (de/en/ru/it/es/pt_BR/pt_PT/tr/fr/zh_CN)',

    "version-argument": '显示版本信息',
    "version-message": "您正在使用Syncplay version {} ({})",

    "load-playlist-from-file-argument": "从文本文件中加载播放列表（每一行代表一个文件）",


    # Client labels
    "config-window-title": "Syncplay设置",

    "connection-group-title": "连接设置",
    "host-label": "服务器地址: ",
    "name-label":  "用户名（可选）:",
    "password-label":  "服务器密码（若需要）:",
    "room-label": "默认房间: ",
    "roomlist-msgbox-label": "编辑房间列表（每行一个房间）",

    "media-setting-title": "播放器设置",
    "executable-path-label": "播放器路径:",
    "media-path-label": "视频文件路径（可选）:",
    "player-arguments-label": "播放器参数（若需要）:",
    "browse-label": "选择...",
    "update-server-list-label": "更新列表",

    "more-title": "高级设置",
    "never-rewind-value": "从不",
    "seconds-suffix": " 秒",
    "privacy-sendraw-option": "原始数据",
    "privacy-sendhashed-option": "哈希加密",
    "privacy-dontsend-option": "不共享",
    "filename-privacy-label": "是否共享文件名:",
    "filesize-privacy-label": "是否共享文件大小:",
    "checkforupdatesautomatically-label": "自动为我检查Syncplay更新信息",
    "autosavejoinstolist-label": "将加入的房间添加到房间列表中",
    "slowondesync-label": "进度过快时慢速播放（MPC-HC/BE播放器不支持）",
    "rewindondesync-label": "进度过快时直接跳转（推荐）",
    "fastforwardondesync-label": "进度过慢时直接跳转（推荐）",
    "dontslowdownwithme-label": "进度过慢时不用让其他人与我同步（试验功能）",
    "pausing-title": "暂停设置",
    "pauseonleave-label": "当其他人离开时暂停（例如其他人掉线）",
    "readiness-title": "初始准备状态",
    "readyatstart-label": "自动将我设置为\"已准备\"状态",
    "forceguiprompt-label": "不要总是打开Syncplay设置窗口",  # (Inverted)
    "showosd-label": "启用OSD信息",

    "showosdwarnings-label": "包括警告信息（例如，当文件不同时，用户没有准备好）",
    "showsameroomosd-label": "包括在你的房间中的活动",
    "shownoncontrollerosd-label": "包括在管理的房间中的非管理员的活动",
    "showdifferentroomosd-label": "包括其他房间的活动",
    "showslowdownosd-label": "包括慢速播放/恢复一倍速的通知",
    "language-label": "语言设置",
    "automatic-language": "默认（{}）",  # Default language
    "showdurationnotification-label": "时长不匹配时警告",
    "basics-label": "基本设置",
    "readiness-label": "播放/暂停设置",
    "misc-label": "其他设置",
    "core-behaviour-title": "主房间行为设置",
    "syncplay-internals-title": "Syncplay内部设置",
    "syncplay-mediasearchdirectories-title": "检索媒体文件的目录",
    "syncplay-mediasearchdirectories-label": "检索媒体文件的目录（每行一个目录）",
    "sync-label": "同步设置",
    "sync-otherslagging-title": "如果您播放进度过快...",
    "sync-youlaggging-title": "如果您播放进度过慢...",
    "messages-label": "消息设置",
    "messages-osd-title": "屏幕显示消息设置",
    "messages-other-title": "其他显示消息设置",
    "chat-label": "聊天设置",
    "privacy-label": "隐私设置",  # Currently unused, but will be brought back if more space is needed in Misc tab
    "privacy-title": "隐私设定",
    "unpause-title": "如果您点击播放按钮，将切换为已准备状态并且：",
    "unpause-ifalreadyready-option": "继续播放，如果已准备",
    "unpause-ifothersready-option": "继续播放，如果已准备或者房间中其他人已准备（默认）",
    "unpause-ifminusersready-option": "继续播放，如果已准备或房间中其他人都已准备且准备人数达到最小开始人数",
    "unpause-always": "总是继续播放",
    "syncplay-trusteddomains-title": "受信任的网站（用于流媒体服务和托管内容）",

    "chat-title": "聊天信息输入设置",
    "chatinputenabled-label": "允许通过mpv播放器进行聊天",
    "chatdirectinput-label": "允许即时聊天输入（不需要按Enter键发送）",
    "chatinputfont-label": "聊天输入字体设置",
    "chatfont-label": "聊天输入字体",
    "chatcolour-label": "设置字体颜色",
    "chatinputposition-label": "mpv播放器中聊天输入窗口位置",
    "chat-top-option": "顶部",
    "chat-middle-option": "中间",
    "chat-bottom-option": "底部",
    "chatoutputheader-label": "聊天显示设置",
    "chatoutputfont-label": "聊天显示字体",
    "chatoutputenabled-label": "启用媒体播放器中的聊天显示（目前仅支持mpv播放器）",
    "chatoutputposition-label": "现实模式",
    "chat-chatroom-option": "聊天室模式",
    "chat-scrolling-option": "弹幕模式",

    "mpv-key-tab-hint": "按下[TAB]来切换为字母快捷键模式。",
    "mpv-key-hint": "按下[ENTER]来发送聊天信息。按下[ESC]来退出聊天模式。",
    "alphakey-mode-warning-first-line": "你可以暂时使用旧版本mpv绑定的a-z键。",
    "alphakey-mode-warning-second-line": "按[TAB]返回到Syncplay聊天模式。",

    "help-label": "帮助",
    "reset-label": "恢复默认设置",
    "run-label": "运行Syncplay",
    "storeandrun-label": "保存设置并运行Syncplay",

    "contact-label": "欢迎发送邮件至 <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a>, 在GitHub上<a href=\"https://github.com/Syncplay/syncplay/issues\"><nobr>创建issue</nobr></a>来反馈漏洞或问题，在GitHub上<a href=\"https://github.com/Syncplay/syncplay/discussions\"><nobr>创建discussion</nobr></a>来提出建议或问题， <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>在Facebook上喜欢我们</nobr></a>, <a href=\"https://twitter.com/Syncplay/\"><nobr>在Twitter上关注我们</nobr></a>，或者访问<a href=\"https://syncplay.pl/\"><nobr>https://syncplay.pl/</nobr></a>。请勿使用Syncplay发送敏感信息。",

    "joinroom-label": "加入房间",
    "joinroom-menu-label": "加入房间 {}",
    "seektime-menu-label": "跳转到",
    "undoseek-menu-label": "撤销跳转",
    "play-menu-label": "播放",
    "pause-menu-label": "暂停",
    "playbackbuttons-menu-label": "显示播放控制按钮",
    "autoplay-menu-label": "显示自动播放按钮",
    "autoplay-guipushbuttonlabel": "当所有人准备好时开始播放",
    "autoplay-minimum-label": "最小开始人数:",
    "hideemptyrooms-menu-label": "隐藏空房间",

    "sendmessage-label": "发送",

    "ready-guipushbuttonlabel": "我已经准备好了！",

    "roomuser-heading-label": "房间 / 用户",
    "size-heading-label": "大小",
    "duration-heading-label": "时长",
    "filename-heading-label": "名称",
    "notifications-heading-label": "消息通知",
    "userlist-heading-label": "正在播放列表",

    "browseformedia-label": "浏览媒体文件",

    "file-menu-label": "&文件",  # & precedes shortcut key
    "openmedia-menu-label": "&打开媒体文件",
    "openstreamurl-menu-label": "打开 &媒体流URL",
    "setmediadirectories-menu-label": "设置媒体 &目录",
    "loadplaylistfromfile-menu-label": "&从文件加载播放列表",
    "saveplaylisttofile-menu-label": "&保存播放列表到文件",
    "exit-menu-label": "退&出",
    "advanced-menu-label": "&高级",
    "window-menu-label": "&窗口",
    "setoffset-menu-label": "设置&偏移量",
    "createcontrolledroom-menu-label": "&创建管理的房间",
    "identifyascontroller-menu-label": "&认证为管理员",
    "settrusteddomains-menu-label": "设置&受信任的网站",
    "addtrusteddomain-menu-label": "添加{}为受信任的网站",  # Domain

    "edit-menu-label": "&编辑",
    "cut-menu-label": "剪&切",
    "copy-menu-label": "&复制",
    "paste-menu-label": "&粘贴",
    "selectall-menu-label": "&全选",

    "playback-menu-label": "&播放控制",

    "help-menu-label": "&帮助",
    "userguide-menu-label": "打开用户&指南",
    "update-menu-label": "检查&更新",

    "startTLS-initiated": "尝试安全连接",
    "startTLS-secure-connection-ok": "安全连接已建立（{}）",
    "startTLS-server-certificate-invalid": '安全连接建立失败。该服务器使用了无效的证书。这次通信可能被第三方截获。更多详情和故障排除请参见<a href="https://syncplay.pl/trouble">这里</a>。',
    "startTLS-server-certificate-invalid-DNS-ID": "Syncplay不信任这个服务器，因为它使用的是对其主机名无效的证书。",
    "startTLS-not-supported-client": "客户端不支持TLS加密安全连接",
    "startTLS-not-supported-server": "服务器不支持TLS加密安全连接",

    # TLS certificate dialog
    "tls-information-title": "证书详情",
    "tls-dialog-status-label": "<strong>Syncplay正使用加密的连接到{}.</strong>",
    "tls-dialog-desc-label": "用数字证书进行加密，使信息在发送到或来自<br/>服务器{}时保持隐私。",
    "tls-dialog-connection-label": "使用Transport Layer Security (TLS)对信息进行加密。版本为{}，<br/>加密套件{}。",
    "tls-dialog-certificate-label": "由{}颁发的证书有效期至{}。",

    # About dialog
    "about-menu-label": "&关于Syncplay",
    "about-dialog-title": "关于Syncplay",
    "about-dialog-release": "Version {} release {}",
    "about-dialog-license-text": "Licensed under the Apache&nbsp;License,&nbsp;Version 2.0",
    "about-dialog-license-button": "License",
    "about-dialog-dependencies": "Dependencies",

    "setoffset-msgbox-label": "设置偏移量",
    "offsetinfo-msgbox-label": "偏移量（使用指南参见https://syncplay.pl/guide/）:",

    "promptforstreamurl-msgbox-label": "打开媒体流URL",
    "promptforstreamurlinfo-msgbox-label": "媒体流URL",

    "addfolder-label": "添加文件夹",

    "adduris-msgbox-label": "添加URL到播放列表（每行一个）",
    "editplaylist-msgbox-label": "设置播放列表（每行一个）",
    "trusteddomains-msgbox-label": "可以自动切换到的网站（每行一个）",

    "createcontrolledroom-msgbox-label": "创建管理的房间",
    "controlledroominfo-msgbox-label": "输入房间名称\r\n（使用指南参见https://syncplay.pl/guide/）:",

    "identifyascontroller-msgbox-label": "认证为房间管理员",
    "identifyinfo-msgbox-label": "输入房间密码\r\n（使用指南参见https://syncplay.pl/guide/）:",

    "public-server-msgbox-label": "为当前会话选择公共服务器",

    "megabyte-suffix": " MB",

    # Tooltips

    "host-tooltip": "要连接的主机名或IP，可包括端口（例如：syncplay.pl:8999）。只能与同一服务器/端口上的人进行同步播放。",
    "name-tooltip": "您的昵称。无需注册，之后可以任意改变。如果没有指定，则生成随机昵称。",
    "password-tooltip": "只有在连接到私人服务器时才需要密码。",
    "room-tooltip": "连接后加入的房间，可以是任意名称，但你只能与同一房间的人进行同步播放。",

    "edit-rooms-tooltip": "编辑房间列表。",

    "executable-path-tooltip": "您选择的播放器的位置（目前仅支持mpv、mpv.net、VLC、MPC-HC/BE、mplayer2或IINA）。",
    "media-path-tooltip": "要打开的视频或媒体流的位置。如果您使用mplayer2，该项为必填项。",
    "player-arguments-tooltip": "额外的命令行参数/开关，以传递给该媒体播放器。",
    "mediasearcdirectories-arguments-tooltip": "Syncplay将搜索媒体文件的目录，例如，当你使用点击切换功能时。Syncplay将通过子文件夹进行递归搜索。",

    "more-tooltip": "显示不常用的设置。",
    "filename-privacy-tooltip": "向服务器发送当前播放文件名的隐私模式。",
    "filesize-privacy-tooltip": "向服务器发送当前播放文件的大小的隐私模式。",
    "privacy-sendraw-tooltip": "发送该信息而不进行混淆处理。这是大多数功能的默认选项。",
    "privacy-sendhashed-tooltip": "发送信息的哈希版本，使其对其他客户不太可见。",
    "privacy-dontsend-tooltip": "不要向服务器发送这些信息。这提供了最大的隐私保护。",
    "checkforupdatesautomatically-tooltip": "定期到Syncplay网站查看是否有新版本的Syncplay。",
    "autosavejoinstolist-tooltip": "当你加入一个服务器中的房间时，在要加入的房间列表中自动记住房间名称。",
    "slowondesync-tooltip": "在需要时暂时降低播放速率，使您与其他观众同步。在MPC-HC/BE上不支持。",
    "dontslowdownwithme-tooltip": "意味着如果你的播放滞后，其他人不会被减慢或倒退。这对房间管理员很有用。",
    "pauseonleave-tooltip": "如果你被断开连接或有人从你的房间离开，则暂停播放。",
    "readyatstart-tooltip": "在开始时将自己设定为\"准备好了\"（否则你将被设定为\"没有准备好\"，直到你改变你的准备状态。）",
    "forceguiprompt-tooltip": "当用Syncplay打开一个文件时，不显示设置窗口。",  # (Inverted)
    "nostore-tooltip": "用给定的配置运行Syncplay，但不永久存储这些变化。",  # (Inverted)
    "rewindondesync-tooltip": "为了达到同步在需要时跳转当前播放进度。禁用这个选项可能会导致严重的不同步现象!",
    "fastforwardondesync-tooltip": "当与房间管理员不同步时，会向前跳转播放进度（如果 \"进度过慢时不用让其他人与我同步\"被启用，则是跳转到你应当的进度）。",
    "showosd-tooltip": "向媒体播放器OSD发送Syncplay信息。",
    "showosdwarnings-tooltip": "如果出现播放不同的文件，独自在房间里，用户没有准备好等情况，则显示警告。",
    "showsameroomosd-tooltip": "显示与用户所在房间有关的活动的OSD通知。",
    "shownoncontrollerosd-tooltip": "显示OSD对与在管理的房间的非管理员有关的活动的通知。",
    "showdifferentroomosd-tooltip": "显示与用户不在的房间有关的活动的OSD通知。",
    "showslowdownosd-tooltip": "显示因进度不同步而进行慢速播放/恢复一倍速的通知。",
    "showdurationnotification-tooltip": "当一个多部分文件中的一个片段丢失时，这很有用，但可能会导致误报。",
    "language-tooltip": "Syncplay中使用的语言。",
    "unpause-always-tooltip": "如果你按下继续播放，会总是将你设置为已准备并继续播放，而不是只将你设置为已准备。",
    "unpause-ifalreadyready-tooltip": "如果你在没有准备好的情况下按下继续播放，它将把你设定为已准备的状态--再按下继续播放就可以继续播放。",
    "unpause-ifothersready-tooltip": "如果你在没有准备好时按下继续播放，只有在其他人准备好时才会继续播放。",
    "unpause-ifminusersready-tooltip": "如果你在没有准备好时按下继续播放，那么只有在其他人准备好并且达到最小开始人数时，它才会取消暂停。",
    "trusteddomains-arguments-tooltip": "启用共享播放列表时，可以让Syncplay自动切换到的网站。",

    "chatinputenabled-tooltip": "在mpv中启用聊天输入（按回车键聊天，按回车键发送，按Esc键取消）。",
    "chatdirectinput-tooltip": "在mpv中无需按回车键即可进入聊天输入模式。在mpv中按TAB键可以暂时禁用这个功能。",
    "font-label-tooltip": "在mpv中输入聊天信息时使用的字体。只在客户端使用，所以不影响其他人看到的内容。",
    "set-input-font-tooltip": "在mpv中输入聊天信息时使用的字体。只在客户端使用，所以不影响其他人看到的内容。",
    "set-input-colour-tooltip": "在mpv中输入聊天信息时使用的字体颜色。只在客户端使用，所以不影响其他人看到的内容。",
    "chatinputposition-tooltip": "聊天输入文本在mpv中的位置，当你按下回车键进行打字输入时，会出现在mpv中。",
    "chatinputposition-top-tooltip": "将聊天输入放在mpv窗口的顶部。",
    "chatinputposition-middle-tooltip": "将聊天输入放在mpv窗口的中间。",
    "chatinputposition-bottom-tooltip": "将聊天输入放在mpv窗口的底部。",
    "chatoutputenabled-tooltip": "在OSD中显示聊天信息（如果媒体播放器支持）。",
    "font-output-label-tooltip": "聊天显示字体。",
    "set-output-font-tooltip": "显示聊天信息时使用的字体。",
    "chatoutputmode-tooltip": "聊天信息的显示方式。",
    "chatoutputmode-chatroom-tooltip": "在前一行的正下方显示新的聊天行。",
    "chatoutputmode-scrolling-tooltip": "像弹幕一样从左到右滚动显示聊天信息。",

    "help-tooltip": "打开Syncplay.pl网站上的用户指南。",
    "reset-tooltip": "将所有设置重置为默认配置。",
    "update-server-list-tooltip": "连接到syncplay.pl来更新公共服务器的列表。",

    "sslconnection-tooltip": "安全地连接到服务器。点击查看证书详情。",

    "joinroom-tooltip": "离开当前房间，加入指定房间。",
    "seektime-msgbox-label": "跳到指定的时间（格式：秒/分：秒）。使用+/-进行相对跳转。",
    "ready-tooltip": "表示你是否准备好观看。",
    "autoplay-tooltip": "当所有拥有准备就绪指示器的用户都准备好了，并且满足最小开始人数时，自动播放。",
    "switch-to-file-tooltip": "双击即可切换到{}",  # Filename
    "sendmessage-tooltip": "发送消息到房间中。",

    # In-userlist notes (GUI)
    "differentsize-note": "大小不同！",
    "differentsizeandduration-note": "大小和时长不同！",
    "differentduration-note": "时长不同！",
    "nofile-note": "（没有正在播放的视频）",

    # Server messages to client
    "new-syncplay-available-motd-message": "您正在使用Syncplay {}版本，但已有较新的版本可从https://syncplay.pl下载。",  # ClientVersion
    "persistent-rooms-notice": "NOTICE: This server uses persistent rooms, which means that the playlist information is stored between playback sessions. If you want to create a room where information is not saved then put -temp at the end of the room name.", # NOTE: Do not translate the word -temp

    # Server notifications
    "welcome-server-notification": "欢迎使用Syncplay服务端，当前版本{0}",  # version
    "client-connected-room-server-notification": "{0}({2})连接到了房间'{1}'",  # username, host, room
    "client-left-server-notification": "{0}断开了服务器",  # name
    "no-salt-notification": "请注意：为了使该服务器实例生成的房间管理员密码在服务器重新启动时仍然有效，请在今后运行Syncplay服务器时添加以下命令行参数：--salt {}",  # Salt


    # Server arguments
    "server-argument-description": '在网络上同步播放多个媒体播放器实例的解决方案。服务器实例',
    "server-argument-epilog": '如果没有提供选项，将使用_config的值',
    "server-port-argument": '服务器TCP端口',
    "server-password-argument": '服务器密码',
    "server-isolate-room-argument": '房间是否相互隔离？',
    "server-salt-argument": "用于生成管理的房间密码的随机字符串",
    "server-disable-ready-argument": "停用准备就绪功能",
    "server-motd-argument": "取出Motd的文件的路径",
    "server-rooms-argument": "使用和/或创建数据库文件的路径，以存储持久的房间数据。使房间能够在没有观察者的情况下持续存在，并通过重新启动来实现。",
    "server-permanent-rooms-argument": "列出永久房间的文件的路径，即使房间是空的也会被列出（以文本文件的形式，每行列出一个房间）--要求启用永久房间。",
    "server-chat-argument": "是否禁用聊天功能？",
    "server-chat-maxchars-argument": "聊天信息中的最大字符数（默认为{}）", # Default number of characters
    "server-maxusernamelength-argument": "用户名中的最大字符数（默认为{}）。",
    "server-stats-db-file-argument": "使用提供的SQLite db文件启用服务器统计功能",
    "server-startTLS-argument": "使用提供的路径中的证书文件启用TLS连接",
    "server-messed-up-motd-unescaped-placeholders": "每日信息中有未转义的占位符。所有 $ 字符应当重复两遍 ($$).",
    "server-messed-up-motd-too-long": "每日信息过长 - 最大{}个chars, 给出的长度{}",
    "server-listen-only-on-ipv4": "Listen only on IPv4 when starting the server.",
    "server-listen-only-on-ipv6": "Listen only on IPv6 when starting the server.",
    "server-interface-ipv4": "The IP address to bind to for IPv4. Leaving it empty defaults to using all.",
    "server-interface-ipv6": "The IP address to bind to for IPv6. Leaving it empty defaults to using all.",

    # Server errors
    "unknown-command-server-error": "未知命令 {}",  # message
    "not-json-server-error": "非json格式字符串 {}",  # message
    "line-decode-server-error": "非utf-8编码字符串",
    "not-known-server-error": "在发送这条命令之前，你必须被服务器认证",
    "client-drop-server-error": "客户端错误消息： {} -- {}",  # host, error
    "password-required-server-error": "请输入密码",
    "wrong-password-server-error": "密码不正确",
    "hello-server-error": "Not enough Hello arguments",  # DO NOT TRANSLATE

    # Playlists
    "playlist-selection-changed-notification":  "{}换碟了",  # Username
    "playlist-contents-changed-notification": "{}更新了播放列表",  # Username
    "cannot-find-file-for-playlist-switch-error": "切换播放内容时，在媒体目录中找不到{}！",  # Filename
    "cannot-add-duplicate-error": "无法将'{}'第二次添加到播放列表中，因为不允许重复。",  # Filename
    "cannot-add-unsafe-path-error": "不能自动加载{}，因为它不在受信任的网站上。你可以在播放列表中双击该URL，手动切换到该URL，并通过文件->高级->设置受信任网站添加受信任网站。如果你鼠标右键一个URL，那么你可以通过右键菜单将其网站添加为受信任网站。",  # Filename
    "sharedplaylistenabled-label": "启用共享播放列表",
    "removefromplaylist-menu-label": "从播放列表中删除",
    "shuffleremainingplaylist-menu-label": "随机排列未完成的播放列表",
    "shuffleentireplaylist-menu-label": "随机排列整个播放列表",
    "undoplaylist-menu-label": "撤销对播放列表的上一次修改",
    "addfilestoplaylist-menu-label": "将文件添加到播放列表的底部",
    "addurlstoplaylist-menu-label": "将URL添加到播放列表的底部",
    "editplaylist-menu-label": "编辑播放列表",

    "open-containing-folder": "打开包含该文件的文件夹",
    "addyourfiletoplaylist-menu-label": "将文件添加到播放列表",
    "addotherusersfiletoplaylist-menu-label": "添加{}的文件到播放列表",  # [Username]
    "addyourstreamstoplaylist-menu-label": "将媒体流添加到播放列表",
    "addotherusersstreamstoplaylist-menu-label": "添加{}的媒体流流到播放列表",  # [Username]
    "openusersstream-menu-label": "打开{}的媒体流",  # [username]'s
    "openusersfile-menu-label": "打开{}的文件",  # [username]'s

    "playlist-instruction-item-message": "把文件拖到这里，就可以把它添加到共享播放列表中。",
    "sharedplaylistenabled-tooltip": "房间管理员可以将文件添加到共享播放列表中，以方便大家观看同样的东西。可以在其他设置中配置媒体目录。",

    "playlist-empty-error": "播放列表目前是空的。",
    "playlist-invalid-index-error": "无效的播放列表索引",
}
