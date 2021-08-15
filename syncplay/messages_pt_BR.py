# coding:utf8

"""Brazilian Portuguese dictionary"""

pt_BR = {
    "LANGUAGE": "Português do Brasil",

    # Client notifications
    "config-cleared-notification": "Configurações removidas. Mudanças serão salvas quando você armazenar uma configuração válida.",

    "relative-config-notification": "Arquivo(s) de configuração relativa carregado(s): {}",

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

    "pause-notification": "{} pausou",  # User
    "unpause-notification": "{} despausou",  # User
    "seek-notification": "{} saltou de {} para {}",  # User, from time, to time

    "current-offset-notification": "Deslocamento atual: {} segundos",  # Offset

    "media-directory-list-updated-notification": "Os diretórios de mídia do Syncplay foram atualizados.",

    "room-join-notification": "{} entrou na sala: '{}'",  # User
    "left-notification": "{} saiu da sala",  # User
    "left-paused-notification": "{} saiu da sala, {} pausou",  # User who left, User who paused
    "playing-notification": "{} está tocando '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum":  " na sala: '{}'",  # Room

    "not-all-ready": "Não está pronto: {}",  # Usernames
    "all-users-ready": "Todo mundo está pronto ({} users)",  # Number of ready users
    "ready-to-unpause-notification": "Agora você está definido como pronto - despause novamente para despausar",
    "set-as-ready-notification": "Agora você está definido como pronto",
    "set-as-not-ready-notification": "Agora você está definido como não pronto",
    "autoplaying-notification": "Reprodução automática em {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Identificando-se como operador da sala com a senha '{}'...",
    "failed-to-identify-as-controller-notification": "{} falhou ao se identificar como operador da sala.",
    "authenticated-as-controller-notification": "{} autenticou-se como um operador da sala",
    "created-controlled-room-notification": "Criou a sala gerenciada '{}' com a senha '{}'. Por favor, salve essa informação para futura referência!\n\nEm uma sala gerenciada, todos são mantidos em sincronia com o(s) operador(es) de sala, que é/são o(s) único(s) que pode(m) pausar, despausar, pular, e mudar a playlist.\n\nVocê deve pedir usuários comuns para se entrarem à sala '{}', mas os operadores de sala podem se entrar à sala '{}' para autenticarem-se automaticamente.", # RoomName, operatorPassword, roomName, roomName:operatorPassword


    "file-different-notification": "O arquivo que você está tocando parece ser diferente do arquivo de {}",  # User
    "file-differences-notification": "Seus arquivos se diferem da(s) seguinte(s) forma(s): {}",  # Differences
    "room-file-differences": "Diferenças de arquivos: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "nome",
    "file-difference-filesize": "tamanho",
    "file-difference-duration": "duração",
    "alone-in-the-room": "Você está sozinho na sala",

    "different-filesize-notification": " (o tamanho do arquivo deles é diferente do seu!)",
    "userlist-playing-notification": "{} está tocando:",  # Username
    "file-played-by-notification": "Arquivo: {} está sendo tocado por:",  # File
    "no-file-played-notification": "{} não está tocando um arquivo",  # Username
    "notplaying-notification": "Pessoas que não estão tocando nenhum arquivo:",
    "userlist-room-notification":  "Na sala '{}':",  # Room
    "userlist-file-notification": "Arquivo",
    "controller-userlist-userflag": "Operador",
    "ready-userlist-userflag": "Pronto",

    "update-check-failed-notification": "Não foi possível verificar automaticamente se o Syncplay {} é a versão mais recente. Deseja visitar https://syncplay.pl/  para checar manualmente por atualizações?",  # Syncplay version
    "syncplay-uptodate-notification": "O Syncplay está atualizado",
    "syncplay-updateavailable-notification": "Uma nova versão do Syncplay está disponível. Deseja visitar a página de lançamentos?",

    "mplayer-file-required-notification": "Syncplay com mplayer requer que você forneça o arquivo ao começar",
    "mplayer-file-required-notification/example": "Exemplo de uso: syncplay [opções] [url|caminho_ate_o_arquivo/]nome_do_arquivo",
    "mplayer2-required": "O Syncplay é incompatível com o MPlayer 1.x, por favor use mplayer2 ou mpv",

    "unrecognized-command-notification": "Comando não reconhecido",
    "commandlist-notification": "Comandos disponíveis:",
    "commandlist-notification/room": "\tr [nome] - muda de sala",
    "commandlist-notification/list": "\tl - mostra lista de usuários",
    "commandlist-notification/undo": "\tu - desfaz último salto",
    "commandlist-notification/pause": "\tp - alterna pausa",
    "commandlist-notification/seek": "\t[s][+-]time - salta para o valor de tempo dado, se + ou - não forem especificados, será o tempo absoluto em segundos ou minutos:segundos",
    "commandlist-notification/help": "\th - esta mensagem de ajuda",
    "commandlist-notification/toggle": "\tt - alterna o seu status de prontidão para assistir",
    "commandlist-notification/create": "\tc [nome] - cria sala gerenciado usando o nome da sala atual",
    "commandlist-notification/auth": "\ta [senha] - autentica-se como operador da sala com a senha",
    "commandlist-notification/chat": "\tch [mensagem] - envia uma mensagem no chat da sala",
    "commandList-notification/queue": "\tqa [file/url] - adiciona arquivo ou URL para o final da playlist",
    "commandList-notification/playlist": "\tql - mostra a playlist atual",
    "commandList-notification/select": "\tqs [index] - seleciona uma dada entrada na playlist",
    "commandList-notification/delete": "\tqd [index] - deleta uma dada entrada na playlist",
    "syncplay-version-notification": "Versão do Syncplay: {}",  # syncplay.version
    "more-info-notification": "Mais informações disponíveis em: {}",  # projectURL

    "gui-data-cleared-notification": "O Syncplay limpou o caminho e o estado de dados da janela usados pela GUI.",
    "language-changed-msgbox-label": "O idioma será alterado quando você salvar as mudanças e abrir o Syncplay novamente.",
    "promptforupdate-label": "O Syncplay pode verificar automaticamente por atualizações de tempos em tempos?",

    "media-player-latency-warning": "Aviso: O reprodutor de mídia demorou {} para responder. Se você tiver problemas de sincronização, feche outros programas para liberar recursos do sistema e, se isso não funcionar, tente outro reprodutor de mídia.",  # Seconds to respond
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
    "mpv-failed-advice": "O motivo pelo qual o mpv não pode ser iniciado pode ser devido ao uso de argumentos da linha de comando não suportados ou a uma versão não suportada do mpv.",
    "player-file-open-error": "O reprodutor falhou ao abrir o arquivo",
    "player-path-error": "O caminho até o arquivo executável do reprodutor não está configurado corretamente. Os reprodutores suportados são: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 e IINA",
    "hostname-empty-error": "O endereço do servidor não pode ser vazio",
    "empty-error": "{} não pode ser vazio",  # Configuration
    "media-player-error": "Erro do reprodutor de mídia: \"{}\"",  # Error line
    "unable-import-gui-error": "Não foi possível importar bibliotecas da GUI. Se você não possuir o PySide instalado, instale-o para que a GUI funcione.",
    "unable-import-twisted-error": "Não foi possível importar o Twisted. Por favor, instale o Twisted v16.4.0 ou superior.",

    "arguments-missing-error": "Alguns argumentos necessários estão faltando, por favor reveja --help",

    "unable-to-start-client-error": "Não foi possível iniciar o client",

    "player-path-config-error": "O caminho até o arquivo executável do reprodutor não está configurado corretamente. Os reprodutores suportados são: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 e IINA.",
    "no-file-path-config-error": "O arquivo deve ser selecionado antes de iniciar seu reprodutor",
    "no-hostname-config-error": "O endereço do servidor não pode ser vazio",
    "invalid-port-config-error": "A porta deve ser válida",
    "empty-value-config-error": "{} não pode ser vazio",  # Config option

    "not-json-error": "Não é uma string codificada como JSON\n",
    "hello-arguments-error": "Not enough Hello arguments\n",  # DO NOT TRANSLATE
    "version-mismatch-error": "Discrepância entre versões do client e do servidor\n",
    "vlc-failed-connection": "Falha ao conectar ao VLC. Se você não instalou o syncplay.lua e está usando a versão mais recente do VLC, por favor veja https://syncplay.pl/LUA/ para mais instruções. Syncplay e VLC 4 são atualmente incompatíveis, portanto ou use VLC 3 ou use outro reprodutor, como o mpv.",
    "vlc-failed-noscript": "O VLC reportou que a interface de script do syncplay.lua não foi instalada. Por favor, veja https://syncplay.pl/LUA/ para mais instruções.",
    "vlc-failed-versioncheck": "Esta versão do VLC não é suportada pelo Syncplay.",
    "vlc-initial-warning": 'O VLC nem sempre fornece informações precisas de posição para o Syncplay, especialmente para arquivos .mp4 ou .avi. Se você experienciar problemas com busca (seeking) incorreta, por favor, tente um reprodutor de mídia alternativo, como o <a href="https://mpv.io/">mpv</a> (ou <a href="https://github.com/stax76/mpv.net/">mpv.net</a>, uma alternativa mais simples do mpv a usuários Windows).',

    "feature-sharedPlaylists": "playlists compartilhadas",  # used for not-supported-by-server-error
    "feature-chat": "chat",  # used for not-supported-by-server-error
    "feature-readiness": "prontidão",  # used for not-supported-by-server-error
    "feature-managedRooms": "salas gerenciadas",  # used for not-supported-by-server-error

    "not-supported-by-server-error": "O recurso {} não é suportado por este servidor.",  # feature
    "shared-playlists-not-supported-by-server-error": "O recurso de playlists compartilhadas pode não ser suportado por este servidor. Para garantir que funcione corretamente, é necessário um servidor rodando Syncplay {} ou superior, mas este está rodando Syncplay {}.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "O recurso de playlists compartilhadas foi desativado nas configurações do servidor. Para usar este recurso, você precisa se conectar a um servidor diferente.",

    "invalid-seek-value": "Valor de salto inválido",
    "invalid-offset-value": "Valor de deslocamento inválido",

    "switch-file-not-found-error": "Não foi possível mudar para o arquivo '{0}'. O Syncplay procura nos diretórios de mídia especificados.",  # File not found
    "folder-search-timeout-error": "A busca por mídias no diretório de mídias foi cancelada pois demorou muito tempo para procurar em '{}'. Isso ocorre quando você seleciona uma pasta com muitas subpastas em sua lista de pastas de mídias a serem pesquisadas.  Para que a troca automática de arquivos funcione novamente, selecione 'Arquivo -> Definir diretórios de mídias' na barra de menus e remova esse diretório ou substitua-o por uma subpasta apropriada. Se a pasta não tiver problemas, é possível reativá-la selecionando 'Arquivo -> Definir diretórios de mídias' e pressionando 'OK'.",  # Folder
    "folder-search-first-file-timeout-error": "A busca por mídias em '{}' foi interrompida, pois demorou muito para acessar o diretório. Isso pode acontecer se for uma unidade de rede ou se você configurar sua unidade para hibernar depois de um período de inatividade. Para que a troca automática de arquivos funcione novamente, vá para 'Arquivo -> Definir diretórios de mídias' e remova o diretório ou resolva o problema (por exemplo, alterando as configurações de economia de energia da unidade).",  # Folder
    "added-file-not-in-media-directory-error": "Você carregou um arquivo em '{}', que não é um diretório de mídias conhecido. Você pode adicioná-lo isso como um diretório de mídia selecionando 'Arquivo -> Definir diretórios de mídias' na barra de menus.",  # Folder
    "no-media-directories-error": "Nenhum diretório de mídias foi definido. Para que os recursos de playlists compartilhadas e troca automática de arquivos funcionem corretamente, selecione 'Arquivo -> Definir diretórios de mídias' e especifique onde o Syncplay deve procurar para encontrar arquivos de mídia.",
    "cannot-find-directory-error": "Não foi possível encontrar o diretório de mídia '{}'. Para atualizar sua lista de diretórios de mídias, selecione 'Arquivo -> Definir diretórios de mídias' na barra de menus e especifique onde o Syncplay deve procurar para encontrar arquivos de mídia.",

    "failed-to-load-server-list-error": "Não foi possível carregar a lista de servidores públicos. Por favor, visite https://www.syncplay.pl/ em seu navegador.",

    # Client arguments
    "argument-description": 'Solução para sincronizar reprodução de múltiplas instâncias de reprodutores de mídia pela rede.',
    "argument-epilog": 'Se nenhuma opção for fornecida, os valores de _config serão usados',
    "nogui-argument": 'não mostrar GUI',
    "host-argument": 'endereço do servidor',
    "name-argument": 'nome de usuário desejado',
    "debug-argument": 'modo depuração',
    "force-gui-prompt-argument": 'fazer o prompt de configuração aparecer',
    "no-store-argument": 'não guardar valores em .syncplay',
    "room-argument": 'sala padrão',
    "password-argument": 'senha do servidor',
    "player-path-argument": 'caminho até o executável do reprodutor de mídia',
    "file-argument": 'arquivo a ser tocado',
    "args-argument": 'opções do reprodutor; se você precisar passar opções começando com -, as preceda com um único argumento \'--\'',
    "clear-gui-data-argument": 'redefine o caminho e o estado de dados da janela da GUI para as de QSettings',
    "language-argument": 'idioma para mensagens do Syncplay (de/en/ru/it/es/pt_BR/pt_PT/tr/fr)',

    "version-argument": 'exibe sua versão',
    "version-message": "Você está usando o Syncplay versão {} ({})",

    "load-playlist-from-file-argument": "carrega playlist de um arquivo de texto (uma entrada por linha)",

    # Client labels
    "config-window-title": "Configuração do Syncplay",

    "connection-group-title": "Configurações de conexão",
    "host-label": "Endereço do servidor: ",
    "name-label": "Nome de usuário (opcional): ",
    "password-label": "Senha do servidor (se existir): ",
    "room-label": "Sala padrão: ",
    "roomlist-msgbox-label": "Edite a lista de salas (uma por linha)",

    "media-setting-title": "Configurações do reprodutor de mídia",
    "executable-path-label": "Executável do reprodutor:",
    "media-path-label": "Arquivo de vídeo ou URL (opcional):",
    "player-arguments-label": "Argumentos para o reprodutor (opcional):",
    "browse-label": "Navegar",
    "update-server-list-label": "Atualizar lista",

    "more-title": "Mostrar mais configurações",
    "never-rewind-value": "Nunca",
    "seconds-suffix": " s",
    "privacy-sendraw-option": "Enviar bruto",
    "privacy-sendhashed-option": "Enviar hasheado",
    "privacy-dontsend-option": "Não enviar",
    "filename-privacy-label": "Informação do nome do arquivo:",
    "filesize-privacy-label": "Informação do tamanho do arquivo:",
    "checkforupdatesautomatically-label": "Verificar atualizações do Syncplay automaticamente",
    "autosavejoinstolist-label": "Adicionar salas que você entra para a lista de salas",
    "slowondesync-label": "Diminuir velocidade em dessincronizações menores (não suportado pelo MPC-HC/BE)",
    "rewindondesync-label": "Retroceder em dessincronização maiores (recomendado)",
    "fastforwardondesync-label": "Avançar se estiver ficando para trás (recomendado)",
    "dontslowdownwithme-label": "Nunca desacelerar ou retroceder outros (experimental)",
    "pausing-title": "Pausando",
    "pauseonleave-label": "Pausar quando um usuário sair (por exemplo, se for desconectado)",
    "readiness-title": "Estado de prontidão inicial",
    "readyatstart-label": "Marque-me como 'pronto para assistir' por padrão",
    "forceguiprompt-label": "Não mostrar a janela de configuração do Syncplay",  # (Inverted)
    "showosd-label": "Ativar mensagens na tela (OSD)",

    "showosdwarnings-label": "Incluir avisos (por exemplo, quando arquivos são diferentes, usuários não estão prontos, etc)",
    "showsameroomosd-label": "Incluir eventos da sua sala",
    "shownoncontrollerosd-label": "Incluir eventos de não operadores em salas gerenciadas",
    "showdifferentroomosd-label": "Incluir eventos de outras salas",
    "showslowdownosd-label": "Incluir notificações de desaceleramento ou retrocedimento",
    "language-label": "Idioma:",
    "automatic-language": "Padrão ({})",  # Default language
    "showdurationnotification-label": "Avisar sobre discrepância nas durações dos arquivos de mídia",
    "basics-label": "Básicos",
    "readiness-label": "Play/Pause",
    "misc-label": "Miscelânea",
    "core-behaviour-title": "Comportamento da sala padrão",
    "syncplay-internals-title": "Configurações internas do Syncplay",
    "syncplay-mediasearchdirectories-title": "Diretórios a buscar por mídias",
    "syncplay-mediasearchdirectories-label": "Diretórios a buscar por mídias (um caminho por linha)",
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
    "unpause-ifminusersready-option": "Despausar se você já estiver pronto ou outros na sala estiverem prontos e o número mínimo de usuários está pronto",
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
    "alphakey-mode-warning-first-line": "Você pode usar os antigos atalhos do mpv com as teclas a-z.",
    "alphakey-mode-warning-second-line": "Aperte [TAB] para retornar ao modo de chat instantâneo do Syncplay.",

    "help-label": "Ajuda",
    "reset-label": "Restaurar padrões",
    "run-label": "Começar Syncplay",
    "storeandrun-label": "Salvar mudanças e começar Syncplay",

    "contact-label": "Sinta-se livre para mandar um e-mail para <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a>, <a href=\"https://github.com/Syncplay/syncplay/issues\"><nobr>abrir uma issue</nobr></a> pelo GitHub / <a href=\"https://github.com/Syncplay/syncplay/discussions\"><nobr>start a discussion</nobr></a> to make a suggestion or ask a question via GitHub,, <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>curtir nossa página no Facebook</nobr></a>, <a href=\"https://twitter.com/Syncplay/\"><nobr>nos seguir no Twitter</nobr></a> ou visitar <a href=\"https://syncplay.pl/\"><nobr>https://syncplay.pl/</nobr></a>. Não use o Syncplay para mandar informações sensíveis/confidenciais.", # TODO: Update translation

    "joinroom-label": "Juntar-se a uma sala",
    "joinroom-menu-label": "Juntar-se à sala {}",
    "seektime-menu-label": "Saltar para o tempo",
    "undoseek-menu-label": "Desfazer salto",
    "play-menu-label": "Play",
    "pause-menu-label": "Pause",
    "playbackbuttons-menu-label": "Mostrar botões de reprodução",
    "autoplay-menu-label": "Mostrar botão de reprodução automática",
    "autoplay-guipushbuttonlabel": "Tocar quando todos estiverem prontos",
    "autoplay-minimum-label": "Mín. de usuários:",

    "sendmessage-label": "Enviar",

    "ready-guipushbuttonlabel": "Estou pronto para assistir!",

    "roomuser-heading-label": "Sala / Usuário",
    "size-heading-label": "Tamanho",
    "duration-heading-label": "Duração",
    "filename-heading-label": "Nome do arquivo",
    "notifications-heading-label": "Notificações",
    "userlist-heading-label": "Lista de quem está tocando o quê",

    "browseformedia-label": "Navegar por arquivos de mídia",

    "file-menu-label": "&Arquivo",  # & precedes shortcut key
    "openmedia-menu-label": "A&brir arquivo de mídia",
    "openstreamurl-menu-label": "Abrir &URL de stream de mídia",
    "setmediadirectories-menu-label": "Definir &diretórios de mídias",
    "loadplaylistfromfile-menu-label": "&Carregar playlist de arquivo",
    "saveplaylisttofile-menu-label": "&Salvar playlist em arquivo",
    "exit-menu-label": "&Sair",
    "advanced-menu-label": "A&vançado",
    "window-menu-label": "&Janela",
    "setoffset-menu-label": "Definir &deslocamento",
    "createcontrolledroom-menu-label": "&Criar sala gerenciada",
    "identifyascontroller-menu-label": "&Identificar-se como operador da sala",
    "settrusteddomains-menu-label": "D&efinir domínios confiáveis",
    "addtrusteddomain-menu-label": "Adicionar {} como domínio confiável",  # Domain

    "edit-menu-label": "&Editar",
    "cut-menu-label": "Cor&tar",
    "copy-menu-label": "&Copiar",
    "paste-menu-label": "C&olar",
    "selectall-menu-label": "&Selecionar todos",

    "playback-menu-label": "&Reprodução",

    "help-menu-label": "&Ajuda",
    "userguide-menu-label": "Abrir &guia de usuário",
    "update-menu-label": "&Verificar atualizações",

    "startTLS-initiated": "Tentando estabelecer conexão segura",
    "startTLS-secure-connection-ok": "Conexão segura estabelecida ({})",
    "startTLS-server-certificate-invalid": 'Não foi possível estabelecer uma conexão segura. O servidor usa um certificado de segurança inválido. Essa comunicação pode ser interceptada por terceiros. Para mais detalhes de solução de problemas, consulte <a href="https://syncplay.pl/trouble">aqui</a>.',
    "startTLS-server-certificate-invalid-DNS-ID": "O Syncplay não confia neste servidor pois ele usa um certificado que não é válido para seu hostname.",
    "startTLS-not-supported-client": "Este client não possui suporte para TLS",
    "startTLS-not-supported-server": "Este servidor não possui suporte para TLS",

    # TLS certificate dialog
    "tls-information-title": "Detalhes do certificado",
    "tls-dialog-status-label": "<strong>Syncplay está usando uma conexão criptografada para {}.</strong>",
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

    "createcontrolledroom-msgbox-label": "Criar sala gerenciada",
    "controlledroominfo-msgbox-label": "Informe o nome da sala gerenciada\r\n(veja https://syncplay.pl/guide/ para instruções de uso):",

    "identifyascontroller-msgbox-label": "Identificar-se como operador da sala",
    "identifyinfo-msgbox-label": "Informe a senha de operador para esta sala\r\n(veja https://syncplay.pl/guide/ para instruções de uso):",

    "public-server-msgbox-label": "Selecione o servidor público para esta sessão de visualização",

    "megabyte-suffix": " MB",

    # Tooltips

    "host-tooltip": "Hostname ou IP para se conectar, opcionalmente incluindo uma porta (por exemplo, syncplay.pl:8999). Só sincroniza-se com pessoas no mesmo servidor/porta.",
    "name-tooltip": "Nome pelo qual você será conhecido. Não há cadastro, então você pode facilmente mudar mais tarde. Se não for especificado, será gerado aleatoriamente.",
    "password-tooltip": "Senhas são necessárias apenas para servidores privados.",
    "room-tooltip": "O nome da sala para se conectar pode ser praticamente qualquer coisa, mas você só irá se sincronizar com pessoas na mesma sala.",

    "edit-rooms-tooltip": "Edite a lista de salas.",

    "executable-path-tooltip": "Localização do seu reprodutor de mídia preferido (mpv, mpv.net, VLC, MPC-HC/BE, mplayer2 ou IINA).",
    "media-path-tooltip": "Localização do vídeo ou transmissão a ser aberto. Necessário com o mplayer2.",
    "player-arguments-tooltip": "Argumentos de comando de linha adicionais para serem repassados ao reprodutor de mídia.",
    "mediasearcdirectories-arguments-tooltip": "Diretório onde o Syncplay vai procurar por arquivos de mídia, por exemplo quando você estiver usando o recurso de clicar para mudar. O Syncplay irá procurar recursivamente pelas subpastas.",

    "more-tooltip": "Exibe configurações menos frequentemente utilizadas.",
    "filename-privacy-tooltip": "Modo de privacidade para mandar nome de arquivo do arquivo atual para o servidor.",
    "filesize-privacy-tooltip": "Modo de privacidade para mandar tamanho do arquivo atual para o servidor.",
    "privacy-sendraw-tooltip": "Enviar esta informação sem ofuscação. Esta é a opção padrão com mais funcionalidades.",
    "privacy-sendhashed-tooltip": "Mandar versão hasheada da informação, tornando-a menos visível aos outros clients.",
    "privacy-dontsend-tooltip": "Não enviar esta informação ao servidor. Esta opção oferece a maior privacidade.",
    "checkforupdatesautomatically-tooltip": "Checar o site do Syncplay regularmente para ver se alguma nova versão do Syncplay está disponível.",
    "autosavejoinstolist-tooltip": "Quando você se juntar a uma sala em um servidor, automaticamente lembrar do nome da sala na lista de salas para entrar.",
    "slowondesync-tooltip": "Reduzir a velocidade de reprodução temporariamente quando necessário para trazer você de volta à sincronia com os outros espectadores. Não suportado pelo MPC-HC/BE.",
    "dontslowdownwithme-tooltip": "Significa que outros não serão desacelerados ou retrocedidos se sua reprodução estiver ficando para trás. Útil para operadores de salas.",
    "pauseonleave-tooltip": "Pausar reprodução se você for desconectado ou se alguém sair da sua sala.",
    "readyatstart-tooltip": "Definir-se como 'pronto' ao começar (do contrário você será definido como 'não pronto' até mudar seu estado de prontidão)",
    "forceguiprompt-tooltip": "Diálogo de configuração não será exibido ao abrir um arquivo com o Syncplay.",  # (Inverted)
    "nostore-tooltip": "Começar Syncplay com a dada configuração, mas não guardar as mudanças permanentemente.",  # (Inverted)
    "rewindondesync-tooltip": "Retroceder automaticamente quando necessário para sincronizar. Desabilitar isto pode resultar em grandes dessincronizações!",
    "fastforwardondesync-tooltip": "Avançar automaticamente quando estiver fora de sincronia com o operador da sala (ou sua posição pretendida caso 'Nunca desacelerar ou retroceder outros' estiver habilitada).",
    "showosd-tooltip": "Envia mensagens do Syncplay à tela do reprodutor de mídia (OSD).",
    "showosdwarnings-tooltip": "Mostra avisos se: estiver tocando arquivos diferentes, sozinho na sala, usuários não prontos, etc.",
    "showsameroomosd-tooltip": "Mostra notificações na tela (OSD) sobre eventos relacionados à sala em que o usuário está.",
    "shownoncontrollerosd-tooltip": "Mostra notificações na tela (OSD) sobre eventos relacionados a não operadores que estão em salas gerenciadas.",
    "showdifferentroomosd-tooltip": "Mostra notificações na tela (OSD) sobre eventos relacionados à sala em que o usuário não está.",
    "showslowdownosd-tooltip": "Mostra notificações na tela (OSD) sobre desaceleramento/retrocedimento por conta de diferença nos tempos.",
    "showdurationnotification-tooltip": "Útil quando um segmento em um arquivo de múltiplas partes está faltando, mas pode resultar em falsos positivos.",
    "language-tooltip": "Idioma a ser utilizado pelo Syncplay.",
    "unpause-always-tooltip": "Se você pressionar para despausar, sempre te definirá como pronto e despausará em vez de simplesmente te definir com pronto.",
    "unpause-ifalreadyready-tooltip": "Se você pressionar para despausar quando não estiver pronto, irá te definir como pronto - despause novamente para despausar.",
    "unpause-ifothersready-tooltip": "Se você apertar para despausar quando não estiver pronto, só irá despausar quando outros estiverem prontos.",
    "unpause-ifminusersready-tooltip": "Se você apertar para despausar quando não estiver pronto, só irá despausar quando outros estiverem prontos e o número mínimo de usuários for atingido.",
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

    "help-tooltip": "Abre o  guia de usuário do Syncplay.pl.",
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

    # Server notifications
    "welcome-server-notification": "Seja bem-vindo ao servidor de Syncplay, versão {0}",  # version
    "client-connected-room-server-notification": "{0}({2}) conectou-se à sala '{1}'",  # username, host, room
    "client-left-server-notification": "{0} saiu do servidor",  # name
    "no-salt-notification": "POR FAVOR, NOTE: Para permitir que as senhas de operadores de sala geradas por esta instância do servidor ainda funcionem quando o servidor for reiniciado, por favor, adicione o seguinte argumento de linha de comando ao executar o servidor de Syncplay no futuro: --salt {}",  # Salt


    # Server arguments
    "server-argument-description": 'Solução para sincronizar a reprodução de múltiplas instâncias de MPlayer e MPC-HC/BE pela rede. Instância de servidor',
    "server-argument-epilog": 'Se nenhuma opção for fornecida, os valores de _config serão utilizados',
    "server-port-argument": 'porta TCP do servidor',
    "server-password-argument": 'senha do servidor',
    "server-isolate-room-argument": 'salas devem ser isoladas?',
    "server-salt-argument": "string aleatória utilizada para gerar senhas de salas gerenciadas",
    "server-disable-ready-argument": "desativar recurso de prontidão",
    "server-motd-argument": "caminho para o arquivo o qual o motd será obtido",
    "server-chat-argument": "O chat deve ser desativado?",
    "server-chat-maxchars-argument": "Número máximo de caracteres numa mensagem do chat (o padrão é {})", # Default number of characters
    "server-maxusernamelength-argument": "Número máximos de caracteres num nome de usuário (o padrão é {})",
    "server-stats-db-file-argument": "Habilita estatísticas de servidor usando o arquivo db SQLite fornecido",
    "server-startTLS-argument": "Habilita conexões TLS usando os arquivos de certificado no caminho fornecido",
    "server-messed-up-motd-unescaped-placeholders": "A Mensagem do Dia possui placeholders não escapados. Todos os sinais de $ devem ser dobrados (como em $$).",
    "server-messed-up-motd-too-long": "A Mensagem do Dia é muito longa - máximo de {} caracteres, {} foram dados.",

    # Server errors
    "unknown-command-server-error": "Comando desconhecido: {}",  # message
    "not-json-server-error": "Não é uma string codificada como json: {}",  # message
    "line-decode-server-error": "Não é uma string UTF-8",
    "not-known-server-error": "Você deve ser conhecido pelo servidor antes de mandar este comando",
    "client-drop-server-error": "Drop do client: {} -- {}",  # host, error
    "password-required-server-error": "Senha necessária",
    "wrong-password-server-error": "Senha incorreta fornecida",
    "hello-server-error": "Not enough Hello arguments",  # DO NOT TRANSLATE

    # Playlists
    "playlist-selection-changed-notification":  "{} mudou a seleção da playlist",  # Username
    "playlist-contents-changed-notification": "{} atualizou playlist",  # Username
    "cannot-find-file-for-playlist-switch-error": "Não foi possível encontrar o arquivo {} no diretórios de mídia para a troca de playlist!",  # Filename
    "cannot-add-duplicate-error": "Não foi possível adicionar uma segunda entrada para '{}' para a playlist uma vez que duplicatas não são permitidas.",  # Filename
    "cannot-add-unsafe-path-error": "Não foi possível automaticamente carregar {} porque este não é um domínio confiado. Você pode trocar para a URL manualmente dando um clique duplo nela na playlist e adicionando o domínio aos domínios confiáveis em 'Arquivo -> Avançado -> Definir domínios confiáveis'. Se você clicar com o botão direito na URL, você pode adicionar esta URL como domínio confiável pelo menu de contexto.",  # Filename
    "sharedplaylistenabled-label": "Habilitar playlists compartilhadas",
    "removefromplaylist-menu-label": "Remover da playlist",
    "shuffleremainingplaylist-menu-label": "Embaralhar resto da playlist",
    "shuffleentireplaylist-menu-label": "Embaralhar toda a playlist",
    "undoplaylist-menu-label": "Desfazer última alteração à playlist",
    "addfilestoplaylist-menu-label": "Adicionar arquivo(s) ao final da playlist",
    "addurlstoplaylist-menu-label": "Adicionar URL(s) ao final da playlist",
    "editplaylist-menu-label": "Editar playlist",

    "open-containing-folder": "Abrir pasta contendo este arquivo",
    "addyourfiletoplaylist-menu-label": "Adicionar seu arquivo à playlist",
    "addotherusersfiletoplaylist-menu-label": "Adicionar arquivos de {} à playlist",  # [Username]
    "addyourstreamstoplaylist-menu-label": "Adicionar sua transmissão à playlist",
    "addotherusersstreamstoplaylist-menu-label": "Adicionar transmissão de {} à playlist",  # [Username]
    "openusersstream-menu-label": "Abrir transmissão de {}",  # [username]'s
    "openusersfile-menu-label": "Abrir arquivo de {}",  # [username]'s

    "playlist-instruction-item-message": "Arraste um arquivo aqui para adicioná-lo à playlist compartilhada.",
    "sharedplaylistenabled-tooltip": "Operadores da sala podem adicionar arquivos para a playlist compartilhada para tornar mais fácil para todo mundo assistir a mesma coisa. Configure os diretórios de mídia em 'Miscelânea'.",

    "playlist-empty-error": "A playlist está atualemnte vazia.",
    "playlist-invalid-index-error": "Índice inválido na playlist.",
}
