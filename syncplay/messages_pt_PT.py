# coding:utf8

"""Portugal Portuguese dictionary"""

# Filename, dictionary name and LANGUAGE-TAG value based on ISO country code. Language tag listed at https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/a9eac961-e77d-41a6-90a5-ce1a8b0cdb9c?redirectedfrom=MSDN

pt_PT = {
    "LANGUAGE": "Português de Portugal",
    "LANGUAGE-TAG": "pt_PT",

    # Strings for Windows NSIS installer
    "installer-language-file": "Portuguese.nlf", # Relevant .nlf file at https://github.com/kichik/nsis/tree/master/Contrib/Language%20files
    "installer-associate": "Associar Syncplay aos ficheiros multimédia.",
    "installer-shortcut": "Criar atalhos nos seguintes locais:",
    "installer-start-menu": "Menu Iniciar",
    "installer-desktop": "Área de trabalho",
    "installer-quick-launch-bar": "Barra de acesso rápido",
    "installer-automatic-updates": "Verificar atualizações automaticamente",
    "installer-uninstall-configuration": "Apagar ficheiro de configuração.",

    # Client notifications
    "config-cleared-notification": "Configurações removidas. As mudanças serão salvas quando você armazenar uma configuração válida.",

    "relative-config-notification": "Ficheiro(s) de configuração relativa carregado(s): {}",

    "connection-attempt-notification": "Tentando se conectar a {}:{}",  # Port, IP
    "reconnection-attempt-notification": "Conexão com o servidor perdida, tentando reconectar",
    "disconnection-notification": "Desconectado do servidor",
    "connection-failed-notification": "Conexão com o servidor falhou",
    "connected-successful-notification": "Conectado com sucesso ao servidor",
    "retrying-notification": "%s, tentando novamente em %d segundos...",  # Seconds
    "reachout-successful-notification": "Alcançado {} ({}) com sucesso",

    "rewind-notification": "Retrocedendo devido à diferença de tempo com {}",  # User
    "fastforward-notification": "Avançando devido à diferença de tempo com {}",  # User
    "slowdown-notification": "Diminuindo a velocidade devido à diferença de tempo com {}",  # User
    "revert-notification": "Revertendo velocidade ao normal",

    "pause-notification": "{} pausou ({})",  # User, Time - TODO: Change into format "{} paused at {}" in line with English message
    "unpause-notification": "{} despausou",  # User
    "seek-notification": "{} saltou de {} para {}",  # User, from time, to time

    "current-offset-notification": "Deslocamento atual: {} segundos",  # Offset

    "media-directory-list-updated-notification": "Os pastas de mídia do Syncplay foram atualizados.",

    "room-join-notification": "{} entrou na sala: '{}'",  # User
    "left-notification": "{} saiu da sala",  # User
    "left-paused-notification": "{} saiu da sala, {} pausou",  # User who left, User who paused
    "playing-notification": "{} está reproduzinho '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum":  " na sala: '{}'",  # Room

    "not-all-ready": "Não está pronto: {}",  # Usernames
    "all-users-ready": "Todos utilizadores estão prontos ({} users)",  # Number of ready users
    "ready-to-unpause-notification": "Agora você está definido como pronto - despause novamente para despausar",
    "set-as-ready-notification": "Agora você está definido como pronto",
    "set-as-not-ready-notification": "Agora você está definido como não pronto",
    "autoplaying-notification": "Reprodução automática em {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Identificando-se como administrador da sala com a senha '{}'...",
    "failed-to-identify-as-controller-notification": "{} falhou ao se identificar como administrador da sala.",
    "authenticated-as-controller-notification": "{} autenticou-se como um administrador da sala",
    "created-controlled-room-notification": "Criou a sala controlada '{}' com a senha '{}'. Por favor, guarda essa informação para futura referência!\n\nIn managed rooms everyone is kept in sync with the room operator(s) who are the only ones who can pause, unpause, seek, and change the playlist.\n\nYou should ask regular viewers to join the room '{}' but the room operators can join the room '{}' to automatically authenticate themselves.", # RoomName, operatorPassword, roomName, roomName:operatorPassword # TODO: Translate

    "file-different-notification": "O ficheiro que você está tocando parece ser diferente do ficheiro de {}",  # User
    "file-differences-notification": "Seus ficheiros se diferem da(s) seguinte(s) forma(s): {}",  # Differences
    "room-file-differences": "Diferenças de ficheiros: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "nome",
    "file-difference-filesize": "tamanho",
    "file-difference-duration": "duração",
    "alone-in-the-room": "Você está sozinho na sala",

    "different-filesize-notification": " (o tamanho do ficheiro deles é diferente do seu!)",
    "userlist-playing-notification": "{} está tocando:",  # Username
    "file-played-by-notification": "Ficheiro: {} está sendo reproduzido por:",  # File
    "no-file-played-notification": "{} não está reproduzinho um ficheiro",  # Username
    "notplaying-notification": "Pessoas que não estão reproduzinho nenhum ficheiro:",
    "userlist-room-notification":  "Na sala '{}':",  # Room
    "userlist-file-notification": "Ficheiro",
    "controller-userlist-userflag": "Administrador",
    "ready-userlist-userflag": "Pronto",

    "update-check-failed-notification": "Não foi possível verificar automaticamente se o Syncplay {} é a versão mais recente. Deseja visitar https://syncplay.pl/  para verificar manualmente por atualizações?",  # Syncplay version
    "syncplay-uptodate-notification": "O Syncplay está atualizado",
    "syncplay-updateavailable-notification": "Uma nova versão do Syncplay está disponível. Deseja visitar a página de lançamentos?",

    "mplayer-file-required-notification": "Syncplay com mplayer requer que você forneça o ficheiro ao começar",
    "mplayer-file-required-notification/example": "Exemplo de uso: syncplay [opções] [url|caminho_ate_o_ficheiro/]nome_do_ficheiro",
    "mplayer2-required": "O Syncplay é incompatível com o MPlayer 1.x, por favor use mplayer2 ou mpv",

    "unrecognized-command-notification": "Comando não reconhecido",
    "commandlist-notification": "Comandos disponíveis:",
    "commandlist-notification/room": "\tr [nome] - muda de sala",
    "commandlist-notification/list": "\tl - mostra lista de utilizadores",
    "commandlist-notification/undo": "\tu - desfaz último salto",
    "commandlist-notification/pause": "\tp - alterna pausa",
    "commandlist-notification/seek": "\t[s][+-]time - salta para o valor de tempo dado, se + ou - não forem especificados, será o tempo absoluto em segundos ou minutos:segundos",
    "commandlist-notification/offset": "\to[+-]duration - offset local playback by the given duration (in seconds or min:sec) from the server seek position - this is a deprecated feature", # TODO: Translate
    "commandlist-notification/help": "\th - esta mensagem de ajuda",
    "commandlist-notification/toggle": "\tt - alterna o seu status de prontidão para assistir",
    "commandlist-notification/create": "\tc [nome] - cria sala gerenciada usando o nome da sala atual",
    "commandlist-notification/auth": "\ta [senha] - autentica-se como administrador da sala com a senha",
    "commandlist-notification/chat": "\tch [mensagem] - envia uma mensagem no chat da sala",
    "commandList-notification/queue": "\tqa [file/url] - add file or url to bottom of playlist",  # TO DO: Translate
    "commandList-notification/queueandselect": "\tqas [file/url] - add file or url to bottom of playlist and select it",  # TO DO: Translate
    "commandList-notification/playlist": "\tql - show the current playlist",  # TO DO: Translate
    "commandList-notification/select": "\tqs [index] - select given entry in the playlist",  # TO DO: Translate
    "commandList-notification/next": "\tqn - select next entry in the playlist", # TODO: Translate
    "commandList-notification/delete": "\tqd [index] - delete the given entry from the playlist",  # TO DO: Translate
    "syncplay-version-notification": "Versão do Syncplay: {}",  # syncplay.version
    "more-info-notification": "Mais informações disponíveis em: {}",  # projectURL

    "gui-data-cleared-notification": "O Syncplay limpou o caminho e o estado de dados da janela usados pela GUI.",
    "language-changed-msgbox-label": "O idioma será alterado quando você salvar as alterações e reabrir o Syncplay.",
    "promptforupdate-label": "O Syncplay pode verificar automaticamente por atualizações de tempos em tempos?",

    "media-player-latency-warning": "Aviso: O reprodutor de mídia demorou {} para responder. Se você tiver problemas de sincronização, desligue outros programas para libertar recursos do sistema e, se isso não funcionar, tente outro reprodutor de mídia.",  # Seconds to respond
    "mpv-unresponsive-error": "O mpv não respondeu por {} segundos, portanto parece que não está funcionando. Por favor, reinicie o Syncplay.",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "Aperte Enter para sair\n",

    # Client errors
    "missing-arguments-error": "Alguns argumentos necessários estão faltando, por favor reveja --help",
    "server-timeout-error": "A conexão com o servidor ultrapassou o tempo limite",
    "mpc-slave-error": "Não foi possível abrir o MPC no slave mode!",
    "mpc-version-insufficient-error": "A versão do MPC é muito antiga, por favor use `mpc-hc` >= `{}`",
    "mpc-be-version-insufficient-error": "A versão do MPC-BE é muito antiga, por favor use `mpc-be` >= `{}`",
    "mpv-version-error": "O Syncplay não é compatível com esta versão do mpv. Por favor, use uma versão diferente do mpv (por exemplo, Git HEAD).",
    "mpv-failed-advice": "O motivo pelo qual o mpv não pode ser iniciado pode ser devido ao uso de argumentos da linha de comando não suportados ou a uma versão não suportada do mpv.", # TODO: Translate
    "player-file-open-error": "O reprodutor falhou ao abrir o ficheiro",
    "player-path-error": "O caminho até o ficheiro executável do reprodutor não está configurado corretamente. Os reprodutores suportados são: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 e IINA",
    "hostname-empty-error": "O endereço do servidor não pode ser vazio",
    "empty-error": "{} não pode ser vazio",  # Configuration
    "media-player-error": "Erro do reprodutor de mídia: \"{}\"",  # Error line
    "unable-import-gui-error": "Não foi possível importar bibliotecas da GUI. Se você não possuir o PySide instalado, instale-o para que a GUI funcione.",
    "unable-import-twisted-error": "Não foi possível importar o Twisted. Por favor, instale o Twisted v16.4.0 ou superior.",

    "arguments-missing-error": "Alguns argumentos necessários estão faltando, por favor reveja --help",

    "unable-to-start-client-error": "Não foi possível iniciar o client",

    "player-path-config-error": "O caminho até o ficheiro executável do reprodutor não está configurado corretamente. Os reprodutores suportados são: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 e IINA.",
    "no-file-path-config-error": "O ficheiro deve ser selecionado antes de iniciar seu reprodutor",
    "no-hostname-config-error": "O endereço do servidor não pode ser vazio",
    "invalid-port-config-error": "A porta deve ser válida",
    "empty-value-config-error": "{} não pode ser vazio",  # Config option

    "not-json-error": "Não é uma string codificada como JSON\n",
    "hello-arguments-error": "Falta de argumentos Hello\n",  # DO NOT TRANSLATE
    "version-mismatch-error": "Discrepância entre versões do cliente e do servidor\n",
    "vlc-failed-connection": "Falha ao conectar ao VLC. Se você não instalou o syncplay.lua e está usando a versão mais recente do VLC, por favor veja https://syncplay.pl/LUA/ para mais instruções.Syncplay and VLC 4 are not currently compatible, so either use VLC 3 or an alternative such as mpv.", # TO DO: TRANSLATE
    "vlc-failed-noscript": "O VLC reportou que a interface de script do syncplay.lua não foi instalada. Por favor, veja https://syncplay.pl/LUA/ para mais instruções.",
    "vlc-failed-versioncheck": "Esta versão do VLC não é suportada pelo Syncplay.",
    "vlc-initial-warning": 'VLC does not always provide accurate position information to Syncplay, especially for .mp4 and .avi files. If you experience problems with erroneous seeking then please try an alternative media player such as <a href="https://mpv.io/">mpv</a> (or <a href="https://github.com/stax76/mpv.net/">mpv.net</a> for Windows users).', # TODO: Translate

    "feature-sharedPlaylists": "playlists compartilhadas",  # used for not-supported-by-server-error
    "feature-chat": "chat",  # used for not-supported-by-server-error
    "feature-readiness": "prontidão",  # used for not-supported-by-server-error
    "feature-managedRooms": "salas administradas",  # used for not-supported-by-server-error

    "not-supported-by-server-error": "O recurso {} não é suportado por este servidor.",  # feature
    "shared-playlists-not-supported-by-server-error": "O recurso de playlists compartilhadas pode não ser suportado por este servidor. Para garantir que funcione corretamente, é necessário um servidor a correr Syncplay {} ou superior, mas este está correndoo Syncplay {}.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "O recurso de playlists compartilhadas foi desativado nas configurações do servidor. Para usar este recurso, você precisa se conectar a um servidor diferente.",

    "invalid-seek-value": "Valor de salto inválido",
    "invalid-offset-value": "Valor de deslocamento inválido",

    "switch-file-not-found-error": "Não foi possível mudar para o ficheiro '{0}'. O Syncplay procura nos pastas de mídia especificados.",  # File not found
    "folder-search-timeout-error": "A busca por mídias no pasta de mídias foi cancelada pois demorou muito tempo para procurar em '{}'. Isso ocorre quando você seleciona uma pasta com muitas subpastas em sua lista de pastas de mídias a serem pesquisadas.  Para que a troca automática de ficheiros funcione novamente, selecione 'Ficheiro -> Definir pastas de mídias' na barra de menus e remova esse pasta ou substitua-o por uma subpasta apropriada. Se a pasta não tiver problemas, é possível reativá-la selecionando 'Ficheiro -> Definir pastas de mídias' e pressionando 'OK'.",  # Folder
    "folder-search-first-file-timeout-error": "A busca por mídias em '{}' foi interrompida, pois demorou muito para acessar o pasta. Isso pode acontecer se for uma unidade de rede ou se você configurar o seu dispositivo para hibernar depois de um período de inatividade. Para que a troca automática de ficheiros funcione novamente, vá para 'Ficheiro -> Definir pastas de mídias' e remova o pasta ou resolva o problema (por exemplo, alterando as configurações de economia de energia da unidade).",  # Folder
    "added-file-not-in-media-directory-error": "Você carregou um ficheiro em '{}', que não é um pasta de mídias conhecido. Você pode adicioná-lo isso como um pasta de mídia selecionando 'Ficheiro -> Definir pastas de mídias' na barra de menus.",  # Folder
    "no-media-directories-error": "Nenhum pasta de mídias foi definido. Para que os recursos de playlists compartilhadas e troca automática de ficheiros funcionem corretamente, selecione 'Ficheiro -> Definir pastas de mídias' e especifique onde o Syncplay deve procurar para encontrar ficheiros de mídia.",
    "cannot-find-directory-error": "Não foi possível encontrar o pasta de mídia '{}'. Para atualizar sua lista de pastas de mídias, selecione 'Ficheiro -> Definir pastas de mídias' na barra de menus e especifique onde o Syncplay deve procurar para encontrar ficheiros de mídia.",

    "failed-to-load-server-list-error": "Não foi possível carregar a lista de servidores públicos. Por favor, visite https://www.syncplay.pl/ em seu navegador.",

    # Client arguments
    "argument-description": 'Solução para sincronizar reprodução de múltiplas instâncias de reprodutores de mídia pela rede.',
    "argument-epilog": 'Se nenhuma opção for fornecida, os valores de _config serão usados',
    "nogui-argument": 'não mostrar GUI',
    "host-argument": 'endereço do servidor',
    "name-argument": 'nome de utilizador desejado',
    "debug-argument": 'modo depuração',
    "force-gui-prompt-argument": 'fazer o prompt de configuração aparecer',
    "no-store-argument": 'não guardar valores em .syncplay',
    "room-argument": 'sala padrão',
    "password-argument": 'senha do servidor',
    "player-path-argument": 'caminho até o executável do reprodutor de mídia',
    "file-argument": 'ficheiro a ser tocado',
    "args-argument": 'opções do reprodutor; se você precisar passar opções começando com -, as preceda com um único argumento \'--\'',
    "clear-gui-data-argument": 'redefine o caminho e o estado de dados da janela da GUI para as de QSettings',
    "language-argument": 'idioma para mensagens do Syncplay ({})', # Languages

    "version-argument": 'exibe sua versão',
    "version-message": "Você está usando o Syncplay versão {} ({})",

    "load-playlist-from-file-argument": "carrega playlist de um ficheiro de texto (uma entrada por linha)",

    # Client labels
    "config-window-title": "Configuração do Syncplay",

    "connection-group-title": "Configurações de conexão",
    "host-label": "Endereço do servidor: ",
    "name-label": "Nome de utilizador (opcional): ",
    "password-label": "Senha do servidor (se existir): ",
    "room-label": "Sala padrão: ",
    "roomlist-msgbox-label": "Edit room list (one per line)", # TODO: Translate

    "media-setting-title": "Configurações do reprodutor de mídia",
    "executable-path-label": "Executável do reprodutor:",
    "media-path-label": "Ficheiro de vídeo ou URL (opcional):",
    "player-arguments-label": "Argumentos para o reprodutor (opcional):",
    "browse-label": "Navegar",
    "update-server-list-label": "Atualizar lista",

    "more-title": "Mostrar mais configurações",
    "never-rewind-value": "Nunca",
    "seconds-suffix": " s",
    "privacy-sendraw-option": "Enviar bruto",
    "privacy-sendhashed-option": "Enviar hasheado",
    "privacy-dontsend-option": "Não enviar",
    "filename-privacy-label": "Informação do nome do ficheiro:",
    "filesize-privacy-label": "Informação do tamanho do ficheiro:",
    "checkforupdatesautomatically-label": "Verificar atualizações do Syncplay automaticamente",
    "slowondesync-label": "Diminuir velocidade em dessincronizações menores (não suportado pelo MPC-HC/BE)",
    "rewindondesync-label": "Retroceder em dessincronização maiores (recomendado)",
    "fastforwardondesync-label": "Avançar se estiver ficando para trás (recomendado)",
    "dontslowdownwithme-label": "Nunca desacelerar ou retroceder outros (experimental)",
    "pausing-title": "Pausando",
    "pauseonleave-label": "Pausar quando um utilizador sair (por exemplo, se for desconectado)",
    "readiness-title": "Estado de prontidão inicial",
    "readyatstart-label": "Marque-me como 'pronto para assistir' por padrão",
    "forceguiprompt-label": "Não mostrar sempre a janela de configuração do Syncplay",  # (Inverted)
    "showosd-label": "Ativar mensagens na tela (OSD)",

    "showosdwarnings-label": "Incluir avisos (por exemplo, quando os ficheiros são diferentes, os utilizador não estão prontos, etc)",
    "showsameroomosd-label": "Incluir eventos da sua sala",
    "shownoncontrollerosd-label": "Incluir eventos de não administradores em salas administradas",
    "showdifferentroomosd-label": "Incluir eventos de outras salas",
    "showslowdownosd-label": "Incluir notificações de desaceleramento ou retrocedimento",
    "language-label": "Idioma:",
    "automatic-language": "Padrão ({})",  # Default language
    "showdurationnotification-label": "Avisar sobre discrepância nas durações dos arquivos de mídia",
    "basics-label": "Básicos",
    "readiness-label": "Play/Pause",
    "misc-label": "Miscelânea",
    "core-behaviour-title": "Comportamento da sala padrão",
    "syncplay-internals-title": "Syncplay internals",
    "syncplay-mediasearchdirectories-title": "pastas a buscar por mídias",
    "syncplay-mediasearchdirectories-label": "pastas a buscar por mídias (um caminho por linha)",
    "sync-label": "Sincronizar",
    "sync-otherslagging-title": "Se outros estiverem ficando pra trás...",
    "sync-youlaggging-title": "Se você estiver ficando pra trás...",
    "messages-label": "Mensagens",
    "messages-osd-title": "Configurações das mensagens na tela (OSD)",
    "messages-other-title": "Outras configurações de tela",
    "chat-label": "Chat",
    "privacy-label": "Privacidade",  # Currently unused, but will be brought back if more space is needed in Misc tab
    "privacy-title": "Configurações de privacidade",
    "unpause-title": "Se você apertar play, definir-se como pronto e:",
    "unpause-ifalreadyready-option": "Despausar se você já estiver definido como pronto",
    "unpause-ifothersready-option": "Despausar se você já estiver pronto ou outros na sala estiverem prontos (padrão)",
    "unpause-ifminusersready-option": "Despausar se você já estiver pronto ou outros na sala estiverem prontos e o número mínimo de utilizadores está pronto",
    "unpause-always": "Sempre despausar",
    "syncplay-trusteddomains-title": "Domínios confiáveis (para serviços de streaming e conteúdo hospedado)",

    "chat-title": "Entrada de mensagem do chat",
    "chatinputenabled-label": "Habilitar entrada de chat via mpv",
    "chatdirectinput-label": "Permitir entrada instantânea de chat (evita ter de apertar Enter para abrir o chat)",
    "chatinputfont-label": "Fonte da entrada de chat",
    "chatfont-label": "Definir fonte",
    "chatcolour-label": "Definir cor",
    "chatinputposition-label": "Posição da área de entrada de mensagens no mpv",
    "chat-top-option": "Topo",
    "chat-middle-option": "Meio",
    "chat-bottom-option": "Fundo",
    "chatoutputheader-label": "Saída de mensagem do chat",
    "chatoutputfont-label": "Fonte da saída de chat",
    "chatoutputenabled-label": "Habilitar saída de chat no reprodutor de mídia (apenas mpv por enquanto)",
    "chatoutputposition-label": "Modo de saída",
    "chat-chatroom-option": "Estilo sala de bate-papo",
    "chat-scrolling-option": "Estilo de rolagem",

    "mpv-key-tab-hint": "[TAB] para alternar acesso instantâneo ao chat.",
    "mpv-key-hint": "[ENTER] para enviar mensagem. [ESC] para sair do modo de chat.",
    "alphakey-mode-warning-first-line": "Você pode usar os antigos atalhos do mpv com as teclas A-Z.",
    "alphakey-mode-warning-second-line": "Aperte [TAB] para retornar ao modo de chat instantâneo do Syncplay.",

    "help-label": "Ajuda",
    "reset-label": "Restaurar padrões",
    "run-label": "Começar Syncplay",
    "storeandrun-label": "Salvar mudanças e começar Syncplay",

    "contact-label": "Sinta-se livre para enviar um e-mail para <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a>, <a href=\"https://github.com/Syncplay/syncplay/issues\"><nobr>abrir uma issue</nobr></a> pelo GitHub / <a href=\"https://github.com/Syncplay/syncplay/discussions\"><nobr>start a discussion</nobr></a> to make a suggestion or ask a question via GitHub,, <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>curtir nossa página no Facebook</nobr></a>, <a href=\"https://twitter.com/Syncplay/\"><nobr>nos seguir no Twitter</nobr></a> ou visitar <a href=\"https://syncplay.pl/\"><nobr>https://syncplay.pl/</nobr></a>. Não use o Syncplay para mandar informações sensíveis/confidenciais.", # TODO: Update translation

    "joinroom-label": "Juntar-se a uma sala",
    "joinroom-menu-label": "Juntar-se à sala {}",
    "seektime-menu-label": "Saltar para o tempo",
    "undoseek-menu-label": "Desfazer salto",
    "play-menu-label": "Play",
    "pause-menu-label": "Pause",
    "playbackbuttons-menu-label": "Mostrar botões de reprodução",
    "autoplay-menu-label": "Mostrar botão de reprodução automática",
    "autoplay-guipushbuttonlabel": "Tocar quando todos estiverem prontos",
    "autoplay-minimum-label": "Mín. de utilizadores:",
    "hideemptyrooms-menu-label": "Hide empty persistent rooms", # TODO: Translate

    "sendmessage-label": "Enviar",

    "ready-guipushbuttonlabel": "Estou pronto para assistir!",

    "roomuser-heading-label": "Sala / Utilizador",
    "size-heading-label": "Tamanho",
    "duration-heading-label": "Duração",
    "filename-heading-label": "Nome do ficheiro",
    "notifications-heading-label": "Notificações",
    "userlist-heading-label": "Lista de quem está tocando o quê",

    "browseformedia-label": "Navegar por ficheiros de mídia",

    "file-menu-label": "&Ficheiro",  # & precedes shortcut key
    "openmedia-menu-label": "A&brir ficheiro de mídia",
    "openstreamurl-menu-label": "Abrir &URL de stream de mídia",
    "setmediadirectories-menu-label": "Definir &pastas de mídias",
    "loadplaylistfromfile-menu-label": "&Carregar playlist de ficheiro",
    "saveplaylisttofile-menu-label": "&Salvar playlist em ficheiro",
    "exit-menu-label": "&Sair",
    "advanced-menu-label": "A&vançado",
    "window-menu-label": "&Janela",
    "setoffset-menu-label": "Definir &deslocamento",
    "createcontrolledroom-menu-label": "&Criar sala administrada",
    "identifyascontroller-menu-label": "&Identificar-se como administrador da sala",
    "settrusteddomains-menu-label": "D&efinir domínios confiáveis",
    "addtrusteddomain-menu-label": "Adicionar {} como domínio confiável",  # Domain

    "edit-menu-label": "&Editar",
    "cut-menu-label": "Cor&tar",
    "copy-menu-label": "&Copiar",
    "paste-menu-label": "C&olar",
    "selectall-menu-label": "&Selecionar todos",

    "playback-menu-label": "&Reprodução",

    "help-menu-label": "&Ajuda",
    "userguide-menu-label": "Abrir &guia de utilizador",
    "update-menu-label": "&Verificar atualizações",

    "startTLS-initiated": "Tentando estabelecer conexão segura",
    "startTLS-secure-connection-ok": "Conexão segura estabelecida ({})",
    "startTLS-server-certificate-invalid": 'Não foi possível estabelecer uma conexão segura. O servidor usa um certificado de segurança inválido. Essa comunicação pode ser interceptada por terceiros. Para mais detalhes de solução de problemas, consulte <a href="https://syncplay.pl/trouble">aqui</a>.',
    "startTLS-server-certificate-invalid-DNS-ID": "O Syncplay não confia neste servidor porque usa um certificado que não é válido para o nome do host.", # TODO: Translate
    "startTLS-not-supported-client": "Este client não possui suporte para TLS",
    "startTLS-not-supported-server": "Este servidor não possui suporte para TLS",

    # TLS certificate dialog
    "tls-information-title": "Detalhes do certificado",
    "tls-dialog-status-label": "<strong>Syncplay está a usar uma conexão criptografada para {}.</strong>",
    "tls-dialog-desc-label": "A criptografia com um certificado digital mantém as informações em sigilo quando são enviadas para ou do<br/>servidor {}.",
    "tls-dialog-connection-label": "Informações criptografadas usando o Transport Layer Security (TLS), versão {} com o conjunto de cifras (cipher suite)<br/>: {}.",
    "tls-dialog-certificate-label": "Certificado emitido em {} e válido até {}.",

    # About dialog
    "about-menu-label": "&Sobre o Syncplay",
    "about-dialog-title": "Sobre o Syncplay",
    "about-dialog-release": "Versão {}, lançamento {}",
    "about-dialog-license-text": "Licenciado sob a Licença&nbsp;Apache,&nbsp;Versão 2.0",
    "about-dialog-license-button": "Licença",
    "about-dialog-dependencies": "Dependências",

    "setoffset-msgbox-label": "Definir deslocamento",
    "offsetinfo-msgbox-label": "Deslocamento (veja https://syncplay.pl/guide/ para instruções de uso):",

    "promptforstreamurl-msgbox-label": "Abrir transmissão de mídia via URL",
    "promptforstreamurlinfo-msgbox-label": "Transmitir URL",

    "addfolder-label": "Adicionar pasta",

    "adduris-msgbox-label": "Adicionar URLs à playlist (uma por linha)",
    "editplaylist-msgbox-label": "Definir playlist (uma por linha)",
    "trusteddomains-msgbox-label": "Domínios para os quais é permitido trocar automaticamente (um por linha)",

    "createcontrolledroom-msgbox-label": "Criar sala administrativa",
    "controlledroominfo-msgbox-label": "Informe o nome da sala administrativa\r\n(veja https://syncplay.pl/guide/ para instruções de uso):",

    "identifyascontroller-msgbox-label": "Identificar-se como administrador da sala",
    "identifyinfo-msgbox-label": "Informe a senha de administrador para esta sala\r\n(veja https://syncplay.pl/guide/ para instruções de uso):",

    "public-server-msgbox-label": "Selecione o servidor público para esta sessão de visualização",

    "megabyte-suffix": " MB",

    # Tooltips

    "host-tooltip": "Hostname ou IP para se conectar, opcionalmente incluindo uma porta (por exemplo, syncplay.pl:8999). Só sincroniza-se com utilizadores no mesmo servidor/porta.",
    "name-tooltip": "Nome pelo qual você será conhecido. Não há cadastro, então você pode facilmente mudar mais tarde. Se não for especificado, será gerado aleatoriamente.",
    "password-tooltip": "Senhas são necessárias apenas para servidores privados.",
    "room-tooltip": "O nome da sala para se conectar pode ser praticamente qualquer coisa, mas você só irá se sincronizar com utilizadores na mesma sala.",

    "edit-rooms-tooltip": "Edit room list.",  # TO DO: Translate

    "executable-path-tooltip": "Localização do seu reprodutor de mídia preferido (mpv, mpv.net, VLC, MPC-HC/BE, mplayer2 ou IINA).",
    "media-path-tooltip": "Localização do vídeo ou transmissão a ser aberto. Necessário com o mplayer2.",
    "player-arguments-tooltip": "Argumentos de comando de linha adicionais para serem repassados ao reprodutor de mídia.",
    "mediasearcdirectories-arguments-tooltip": "Pasta onde o Syncplay vai procurar por ficheiros de mídia, por exemplo quando você estiver usando o recurso de clicar para mudar. O Syncplay irá procurar recursivamente pelas subpastas.",

    "more-tooltip": "Mostrar configurações frequentemente menos utilizadas.",
    "filename-privacy-tooltip": "Modo de privacidade para mandar nome de ficheiro do ficheiro atual para o servidor.",
    "filesize-privacy-tooltip": "Modo de privacidade para mandar tamanho do ficheiro atual para o servidor.",
    "privacy-sendraw-tooltip": "Enviar esta informação sem ofuscação. Esta é a opção padrão com mais funcionalidades.",
    "privacy-sendhashed-tooltip": "Mandar versão hasheada da informação, tornando-a menos visível aos outros clients.",
    "privacy-dontsend-tooltip": "Não enviar esta informação ao servidor. Esta opção oferece a maior privacidade.",
    "checkforupdatesautomatically-tooltip": "Verificar o site do Syncplay regularmente para ver se alguma nova versão do Syncplay está disponível.",
    "autosavejoinstolist-tooltip": "When you join a room in a server, automatically remember the room name in the list of rooms to join.", # TO DO: Translate
    "autosavejoinstolist-label": "Add rooms you join to the room list", # TO DO: Translate
    "slowondesync-tooltip": "Reduzir a velocidade de reprodução temporariamente quando necessário para trazer você de volta à sincronia com os outros espectadores. Não suportado pelo MPC-HC/BE.",
    "dontslowdownwithme-tooltip": "Significa que outros não serão desacelerados ou retrocedidos se sua reprodução estiver ficando para trás. Útil para administradores de salas.",
    "pauseonleave-tooltip": "Pausar reprodução se você for disconectado ou se alguém sair da sua sala.",
    "readyatstart-tooltip": "Definir-se como 'pronto' ao começar (do contrário você será definido como 'não pronto' até mudar seu estado de prontidão)",
    "forceguiprompt-tooltip": "Diálogo de configuração não é exibido ao abrir um ficheiro com o Syncplay.",  # (Inverted)
    "nostore-tooltip": "Começar Syncplay com a dada configuração, mas não guardar as mudanças permanentemente.",  # (Inverted)
    "rewindondesync-tooltip": "Retroceder automaticamente quando necessário para sincronizar. Desabilitar isto pode resultar em grandes dessincronizações!",
    "fastforwardondesync-tooltip": "Avançar automaticamente quando estiver fora de sincronia com o administrador da sala (ou sua posição pretendida caso 'Nunca desacelerar ou retroceder outros' estiver habilitada).",
    "showosd-tooltip": "Envia mensagens do Syncplay à tela do reprodutor de mídia (OSD).",
    "showosdwarnings-tooltip": "Mostra avisos se: estiver tocando ficheiros diferentes, sozinho na sala, utilizadores não prontos, etc.",
    "showsameroomosd-tooltip": "Mostra notificações na tela (OSD) sobre eventos relacionados à sala em que o utilizador está.",
    "shownoncontrollerosd-tooltip": "Mostra notificações na tela (OSD) sobre eventos relacionados a não administradores que estão em salas gerenciadas.",
    "showdifferentroomosd-tooltip": "Mostra notificações na tela (OSD) sobre eventos relacionados à sala em que o utilizador não está.",
    "showslowdownosd-tooltip": "Mostra notificações na tela (OSD) sobre desaceleramento/retrocedimento por conta de diferença nos tempos.",
    "showdurationnotification-tooltip": "Útil quando um segmento em um ficheiro de múltiplas partes está faltando, mas pode resultar em falsos positivos.",
    "language-tooltip": "Idioma a ser utilizado pelo Syncplay.",
    "unpause-always-tooltip": "Se você pressionar para despausar, sempre te definirá como pronto e despausará em vez de simplesmente te definir com pronto.",
    "unpause-ifalreadyready-tooltip": "Se você pressionar para despausar quando não estiver pronto, irá te definir como pronto - despause novamente para despausar.",
    "unpause-ifothersready-tooltip": "Se você apertar para despausar quando não estiver pronto, só irá despausar quando outros estiverem prontos.",
    "unpause-ifminusersready-tooltip": "Se você apertar para despausar quando não estiver pronto, só irá despausar quando outros estiverem prontos e o número mínimo de utilizadores for atingido.",
    "trusteddomains-arguments-tooltip": "Domínios para os quais é permitido trocar automaticamente quando as playlists compartilhadas estiverem habilitadas.",

    "chatinputenabled-tooltip": "Ativar entrada de chat via mpv (pressione Enter para escrever, Enter para enviar, ESC para cancelar)",
    "chatdirectinput-tooltip": "Evita ter de apertar 'Enter' para entrar no modo de entrada de chat no mpv. Pressione TAB no mpv para temporariamente desabilitar esta função.",
    "font-label-tooltip": "Fonte usada ao escrever mensagens no chat no mpv. Apenas no lado do client, portanto não afeta a cor que os outros veem.",
    "set-input-font-tooltip": "Família de fonte usada ao escrever mensagens no chat no mpv. Apenas no lado do client, portanto não afeta a cor que os outros veem.",
    "set-input-colour-tooltip": "Cor de fonte usada ao escrever mensagens no chat no mpv. Apenas no lado do client, portanto não afeta a cor que os outros veem.",
    "chatinputposition-tooltip": "Lugar no mpv onde a entrada de chat será exibida quando você apertar Enter e digitar.",
    "chatinputposition-top-tooltip": "Colocar entrada de chat no topo da janela do mpv.",
    "chatinputposition-middle-tooltip": "Colocar entrada de chat no meio da janela do mpv.",
    "chatinputposition-bottom-tooltip": "Colocar entrada de chat no fundo da janela do mpv.",
    "chatoutputenabled-tooltip": "Mostrar mensagens de chat na tela do reprodutor (OSD) (se suportado pelo reprodutor).",
    "font-output-label-tooltip": "Fonte da saída de chat.",
    "set-output-font-tooltip": "Fonte usada para exibir mensagens do chat.",
    "chatoutputmode-tooltip": "Como as mensagens do chat são exibidas.",
    "chatoutputmode-chatroom-tooltip": "Exibe novas linhas de chat diretamente abaixo da linha anterior.",
    "chatoutputmode-scrolling-tooltip": "Exibe novas linhas de chat rolando-as da direita pra esquerda.",

    "help-tooltip": "Abre o  guia de utilizadores do Syncplay.pl.",
    "reset-tooltip": "Redefine todas as configurações para seus respectivos padrões.",
    "update-server-list-tooltip": "Conecta ao syncplay.pl para atualizar a lista de servidores públicos.",

    "sslconnection-tooltip": "Conectado com segurança ao servidor. Clique para exibir detalhes do certificado.",

    "joinroom-tooltip": "Sair da sala atual e ingressar na sala especificada.",
    "seektime-msgbox-label": "Saltar para tempo especificado (em segundos ou minutos:segundos). Use + ou - para fazer um pulo relativo ao tempo atual.",
    "ready-tooltip": "Indica se você está pronto para assistir.",
    "autoplay-tooltip": "Reproduzir automaticamente quando todos os usuários que tiverem indicadores de prontidão estiverem prontos e o limiar de usuários for atingido.",
    "switch-to-file-tooltip": "Clique duas vezes para mudar para {}",  # Filename
    "sendmessage-tooltip": "Mandar mensagem para a sala",

    # In-userlist notes (GUI)
    "differentsize-note": "Tamanhos diferentes!",
    "differentsizeandduration-note": "Tamanhos e durações diferentes!",
    "differentduration-note": "Durações diferentes!",
    "nofile-note": "(Nenhum arquivo está sendo tocado)",

    # Server messages to client
    "new-syncplay-available-motd-message": "Você está usando o Syncplay {}, mas uma versão mais nova está disponível em https://syncplay.pl",  # ClientVersion
    "persistent-rooms-notice": "NOTICE: This server uses persistent rooms, which means that the playlist information is stored between playback sessions. If you want to create a room where information is not saved then put -temp at the end of the room name.", # TO DO: Translate - NOTE: Do not translate the word -temp

    # Server notifications
    "welcome-server-notification": "Seja bem-vindo ao servidor de Syncplay, versão {0}",  # version
    "client-connected-room-server-notification": "{0}({2}) conectou-se à sala '{1}'",  # username, host, room
    "client-left-server-notification": "{0} saiu do servidor",  # name
    "no-salt-notification": "POR FAVOR, NOTE: Para permitir que as senhas de administradores de sala geradas por esta instância do servidor ainda funcionem quando o servidor for reiniciado, por favor, adicione o seguinte argumento de linha de comando ao executar o servidor de Syncplay no futuro: --salt {}",  # Salt


    # Server arguments
    "server-argument-description": 'Solução para sincronizar a reprodução de múltiplas instâncias de MPlayer e MPC-HC/BE pela rede. Instância de servidor',
    "server-argument-epilog": 'Se nenhuma opção for fornecida, os valores de _config serão utilizados',
    "server-port-argument": 'porta TCP do servidor',
    "server-password-argument": 'senha do servidor',
    "server-isolate-room-argument": 'salas devem ser isoladas?',
    "server-salt-argument": "string aleatória utilizada para gerar senhas de salas gerenciadas",
    "server-disable-ready-argument": "desativar recurso de prontidão",
    "server-motd-argument": "caminho para o arquivo o qual o motd será obtido",
    "server-rooms-argument": "path to database file to use and/or create to store persistent room data. Enables rooms to persist without watchers and through restarts", # TODO: Translate
    "server-permanent-rooms-argument": "path to file which lists permenant rooms that will be listed even if the room is empty (in the form of a text file which lists one room per line) - requires persistent rooms to be enabled", # TODO: Translate
    "server-chat-argument": "O chat deve ser desativado?",
    "server-chat-maxchars-argument": "Número máximo de caracteres numa mensagem do chat (o padrão é {})", # Default number of characters
    "server-maxusernamelength-argument": "Número máximos de caracteres num nome de utilizador (o padrão é {})",
    "server-stats-db-file-argument": "Habilita estatísticas de servidor usando o arquivo db SQLite fornecido",
    "server-startTLS-argument": "Habilita conexões TLS usando os arquivos de certificado no caminho fornecido",
    "server-messed-up-motd-unescaped-placeholders": "A Mensagem do Dia possui placeholders não escapados. Todos os sinais de $ devem ser dobrados (como em $$).",
    "server-messed-up-motd-too-long": "A Mensagem do Dia é muito longa - máximo de {} caracteres, {} foram dados.",
    "server-listen-only-on-ipv4": "Listen only on IPv4 when starting the server.",
    "server-listen-only-on-ipv6": "Listen only on IPv6 when starting the server.",
    "server-interface-ipv4": "The IP address to bind to for IPv4. Leaving it empty defaults to using all.",
    "server-interface-ipv6": "The IP address to bind to for IPv6. Leaving it empty defaults to using all.",

    # Server errors
    "unknown-command-server-error": "Comando desconhecido: {}",  # message
    "not-json-server-error": "Não é uma string codificada como JSON: {}",  # message
    "line-decode-server-error": "Não é uma string UTF-8",
    "not-known-server-error": "Você deve ser conhecido pelo servidor antes de mandar este comando",
    "client-drop-server-error": "Drop do client: {} -- {}",  # host, error
    "password-required-server-error": "Senha necessária",
    "wrong-password-server-error": "Senha incorreta fornecida",
    "hello-server-error": "Not enough Hello arguments",  # DO NOT TRANSLATE

    # Playlists
    "playlist-selection-changed-notification":  "{} mudou a seleção da playlist",  # Username
    "playlist-contents-changed-notification": "{} atualizou playlist",  # Username
    "cannot-find-file-for-playlist-switch-error": "Não foi possível encontrar o ficheiro {} no pastas de mídia para a troca de playlist!",  # Filename
    "cannot-add-duplicate-error": "Não foi possível adicionar uma segunda entrada para '{}' para a playlist uma vez que duplicatas não são permitidas.",  # Filename
    "cannot-add-unsafe-path-error": "Não foi possível automaticamente carregar {} porque este não é um domínio confiado. Você pode trocar para a URL manualmente dando um clique duplo nela na playlist e adicionando o domínio aos domínios confiáveis em 'Ficheiro -> Avançado -> Definir domínios confiáveis'. Se você clicar com o botão direito na URL, você pode adicionar esta URL como domínio confiável pelo menu de contexto.",  # Filename
    "sharedplaylistenabled-label": "Habilitar playlists compartilhadas",
    "removefromplaylist-menu-label": "Remover da playlist",
    "shuffleremainingplaylist-menu-label": "Embaralhar resto da playlist",
    "shuffleentireplaylist-menu-label": "Embaralhar toda a playlist",
    "undoplaylist-menu-label": "Desfazer última alteração à playlist",
    "addfilestoplaylist-menu-label": "Adicionar ficheiro(s) ao final da playlist",
    "addurlstoplaylist-menu-label": "Adicionar URL(s) ao final da playlist",
    "editplaylist-menu-label": "Editar playlist",

    "open-containing-folder": "Abrir pasta contendo este ficheiro",
    "addyourfiletoplaylist-menu-label": "Adicionar seu ficheiro à playlist",
    "addotherusersfiletoplaylist-menu-label": "Adicionar ficheiros de {} à playlist",  # [Username]
    "addyourstreamstoplaylist-menu-label": "Adicionar sua transmissão à playlist",
    "addotherusersstreamstoplaylist-menu-label": "Adicionar transmissão de {} à playlist",  # [Username]
    "openusersstream-menu-label": "Abrir transmissão de {}",  # [username]'s
    "openusersfile-menu-label": "Abrir ficheiro de {}",  # [username]'s

    "playlist-instruction-item-message": "Arraste um ficheiro aqui para adicioná-lo à playlist compartilhada.",
    "sharedplaylistenabled-tooltip": "Operadores da sala podem adicionar ficheiros para a playlist compartilhada para tornar mais fácil para todo mundo assistir a mesma coisa. Configure os pastas de mídia em 'Miscelânea'.",

    "playlist-empty-error": "Playlist is currently empty.",  # TO DO: Translate
    "playlist-invalid-index-error": "Invalid playlist index", # TO DO: Translate
}
