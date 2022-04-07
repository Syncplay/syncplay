# coding:utf8

"""Spanish dictionary"""

es = {
    "LANGUAGE": "Español",

    # Client notifications
    "config-cleared-notification": "Ajustes limpiados. Los cambios serán guardados cuando almacenes una configuración válida.",

    "relative-config-notification": "Cargados los archivo(s) de configuración relativa: {}",

    "connection-attempt-notification": "Intentando conectarse a {}:{}",  # Port, IP
    "reconnection-attempt-notification": "Se perdió la conexión con el servidor, intentando reconectar",
    "disconnection-notification": "Desconectado del servidor",
    "connection-failed-notification": "La conexión con el servidor falló",
    "connected-successful-notification": "Conectado al servidor exitosamente",
    "retrying-notification": "%s, Reintentando en %d segundos...",  # Seconds
    "reachout-successful-notification": "Se alcanzó {} ({}) satisfactoriamente",

    "rewind-notification": "Rebobinado debido a diferencia de tiempo con {}",  # User
    "fastforward-notification": "Adelantado debido a diferencia de tiempo con {}",  # User
    "slowdown-notification": "Ralentizando debido a diferencia de tiempo con {}",  # User
    "revert-notification": "Revirtiendo a la velocidad normal",

    "pause-notification": "{} pausado ({})",  # User
    "unpause-notification": "{} resumido",  # User
    "seek-notification": "{} saltó desde {} hasta {}",  # User, from time, to time

    "current-offset-notification": "Compensación actual: {} segundos",  # Offset

    "media-directory-list-updated-notification": "Se han actualizado los directorios multimedia de Syncplay.",

    "room-join-notification": "{} se unió al canal: '{}'",  # User
    "left-notification": "{} se fue",  # User
    "left-paused-notification": "{} se fue, {} pausó",  # User who left, User who paused
    "playing-notification": "{} está reproduciendo '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum":  " en la sala: '{}'",  # Room

    "not-all-ready": "No están listos: {}",  # Usernames
    "all-users-ready": "Todos están listos ({} users)",  # Number of ready users
    "ready-to-unpause-notification": "Se te ha establecido como listo - despausa nuevamente para resumir",
    "set-as-ready-notification": "Se te ha establecido como listo",
    "set-as-not-ready-notification": "Se te ha establecido como no-listo",
    "autoplaying-notification": "Reproduciendo automáticamente en {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Autentificando como el operador de la sala, con contraseña '{}'...",
    "failed-to-identify-as-controller-notification": "{} falló la autentificación como operador de la sala.",
    "authenticated-as-controller-notification": "{} autentificado como operador de la sala",
    "created-controlled-room-notification": "Sala administrada '{}' creada con contraseña '{}'. Por favor guarda esta información para referencias futuras!\n\nIn managed rooms everyone is kept in sync with the room operator(s) who are the only ones who can pause, unpause, seek, and change the playlist.\n\nYou should ask regular viewers to join the room '{}' but the room operators can join the room '{}' to automatically authenticate themselves.", # RoomName, operatorPassword, roomName, roomName:operatorPassword # TODO: Translate

    "file-different-notification": "El archivo que reproduces parece ser diferente al archivo de {}",  # User
    "file-differences-notification": "Tu archivo difiere de la(s) siguiente(s) forma(s): {}",  # Differences
    "room-file-differences": "Diferencias de archivo: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "nombre",
    "file-difference-filesize": "tamaño",
    "file-difference-duration": "duración",
    "alone-in-the-room": "Estás solo en la sala",

    "different-filesize-notification": " (el tamaño de su archivo difiere con el tuyo!)",
    "userlist-playing-notification": "{} está reproduciendo:",  # Username
    "file-played-by-notification": "Archivo: {} está siendo reproducido por:",  # File
    "no-file-played-notification": "{} está ahora reproduciendo un archivo",  # Username
    "notplaying-notification": "Personas que no reproducen algún archivo:",
    "userlist-room-notification":  "En sala '{}':",  # Room
    "userlist-file-notification": "Archivo",
    "controller-userlist-userflag": "Operador",
    "ready-userlist-userflag": "Listo",

    "update-check-failed-notification": "No se pudo determinar automáticamente que Syncplay {} esté actualizado. ¿Te gustaría visitar https://syncplay.pl/ para buscar actualizaciones manualmente?",  # Syncplay version
    "syncplay-uptodate-notification": "Syncplay está actualizado",
    "syncplay-updateavailable-notification": "Una nueva versión de Syncplay está disponible. ¿Te gustaría visitar la página del lanzamiento?",

    "mplayer-file-required-notification": "Al utilizar Syncplay con mplayer se debe proveer un archivo al inicio.",
    "mplayer-file-required-notification/example": "Ejemplo de uso: syncplay [opciones] [url|ubicación/]nombreDelArchivo",
    "mplayer2-required": "Syncplay no es compatible con MPlayer 1.x, por favor utiliza mplayer2 o mpv",

    "unrecognized-command-notification": "Comando no reconocido",
    "commandlist-notification": "Comandos disponibles:",
    "commandlist-notification/room": "\tr [nombre] - cambiar de sala",
    "commandlist-notification/list": "\tl - mostrar lista de usuarios",
    "commandlist-notification/undo": "\tu - deshacer última búsqueda",
    "commandlist-notification/pause": "\tp - activar pausa",
    "commandlist-notification/seek": "\t[s][+-]tiempo - ir al tiempo definido, si no se especifica + o -, será el tiempo absoluto en segundos o min:sec",
    "commandlist-notification/offset": "\to[+-]duration - offset local playback by the given duration (in seconds or min:sec) from the server seek position - this is a deprecated feature", # TODO: Translate
    "commandlist-notification/help": "\th - esta ayuda",
    "commandlist-notification/toggle": "\tt - activa/inactiva señal que estás listo para ver",
    "commandlist-notification/create": "\tc [nombre] - crear sala administrada usando el nombre de la sala actual",
    "commandlist-notification/auth": "\ta [contraseña] - autentificar como operador de la sala con la contraseña de operador",
    "commandlist-notification/chat": "\tch [mensaje] - enviar un mensaje en la sala",
    "commandList-notification/queue": "\tqa [file/url] - add file or url to bottom of playlist",  # TO DO: Translate
    "commandList-notification/queueandselect": "\tqas [file/url] - add file or url to bottom of playlist and select it",  # TO DO: Translate
    "commandList-notification/playlist": "\tql - show the current playlist",  # TO DO: Translate
    "commandList-notification/select": "\tqs [index] - select given entry in the playlist",  # TO DO: Translate
    "commandList-notification/delete": "\tqd [index] - delete the given entry from the playlist",  # TO DO: Translate
    "syncplay-version-notification": "Versión de Syncplay: {}",  # syncplay.version
    "more-info-notification": "Más información disponible en: {}",  # projectURL

    "gui-data-cleared-notification": "Syncplay limpió la ruta y el estado de la ventana utilizado por la GUI.",
    "language-changed-msgbox-label": "El lenguaje se modificará cuando ejecutes Syncplay.",
    "promptforupdate-label": "¿Está bien si Syncplay comprueba por actualizaciones automáticamente y de vez en cuando?",

    "media-player-latency-warning": "Advertencia: El reproductor multimedia tardó {} segundos en responder. Si experimentas problemas de sincronización, cierra otros programas para liberar recursos del sistema; si esto no funciona, intenta con otro reproductor multimedia.",  # Seconds to respond
    "mpv-unresponsive-error": "mpv no ha respondido por {} segundos. Al aparecer no está funcionando correctamente. Por favor reinicia Syncplay.",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "Presiona intro para salir\n",

    # Client errors
    "missing-arguments-error": "Están faltando algunos argumentos necesarios. Por favor revisa --help",
    "server-timeout-error": "La conexión con el servidor ha caducado",
    "mpc-slave-error": "No se logró iniciar MPC en modo esclavo!",
    "mpc-version-insufficient-error": "La versión de MPC no es suficiente, por favor utiliza `mpc-hc` >= `{}`",
    "mpc-be-version-insufficient-error": "La versión de MPC no es suficiente, por favor utiliza `mpc-be` >= `{}`",
    "mpv-version-error": "Syncplay no es compatible con esta versión de mpv. Por favor utiliza una versión diferente de mpv (p.ej. Git HEAD).",
    "mpv-failed-advice": "The reason mpv cannot start may be due to the use of unsupported command line arguments or an unsupported version of mpv.", # TODO: Translate
    "player-file-open-error": "El reproductor falló al abrir el archivo",
    "player-path-error": "La ruta del reproductor no está definida correctamente. Los reproductores soportados son: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2, y IINA",
    "hostname-empty-error": "El nombre del host no puede ser vacío",
    "empty-error": "{} no puede ser vacío",  # Configuration
    "media-player-error": "Error del reproductor multimedia: \"{}\"",  # Error line
    "unable-import-gui-error": "No se lograron importar las librerías GUI. Si no tienes instalado PySide, entonces tendrás que instalarlo para que funcione el GUI.",
    "unable-import-twisted-error": "No se logró importar Twisted. Por favor instala Twisted v16.4.0 o posterior.",

    "arguments-missing-error": "Están faltando algunos argumentos necesarios. Por favor revisa --help",

    "unable-to-start-client-error": "No se logró iniciar el cliente",

    "player-path-config-error": "La ruta del reproductor no está definida correctamente. Los reproductores soportados son: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 y IINA.",
    "no-file-path-config-error": "El archivo debe ser seleccionado antes de iniciar el reproductor",
    "no-hostname-config-error": "El nombre del host no puede ser vacío",
    "invalid-port-config-error": "El puerto debe ser válido",
    "empty-value-config-error": "{} no puede ser vacío",  # Config option

    "not-json-error": "No es una cadena de caracteres JSON válida\n",
    "hello-arguments-error": "Not enough Hello arguments\n",  # DO NOT TRANSLATE
    "version-mismatch-error": "No coinciden las versiones del cliente y servidor\n",
    "vlc-failed-connection": "Falló la conexión con VLC. Si no has instalado syncplay.lua y estás usando la última versión de VLC, por favor revisa https://syncplay.pl/LUA/ para obtener instrucciones. Syncplay and VLC 4 are not currently compatible, so either use VLC 3 or an alternative such as mpv.", # TO DO: TRANSLATE
    "vlc-failed-noscript": "VLC ha reportado que la interfaz syncplay.lua no se ha instalado. Por favor revisa https://syncplay.pl/LUA/ para obtener instrucciones.",
    "vlc-failed-versioncheck": "Esta versión de VLC no está soportada por Syncplay.",
    "vlc-initial-warning": 'VLC does not always provide accurate position information to Syncplay, especially for .mp4 and .avi files. If you experience problems with erroneous seeking then please try an alternative media player such as <a href="https://mpv.io/">mpv</a> (or <a href="https://github.com/stax76/mpv.net/">mpv.net</a> for Windows users).', # TODO: Translatef

    "feature-sharedPlaylists": "listas de reproducción compartidas",  # used for not-supported-by-server-error
    "feature-chat": "chat",  # used for not-supported-by-server-error
    "feature-readiness": "preparación",  # used for not-supported-by-server-error
    "feature-managedRooms": "salas administradas",  # used for not-supported-by-server-error

    "not-supported-by-server-error": "La característica {} no está soportada por este servidor..",  # feature
    "shared-playlists-not-supported-by-server-error": "El servidor no admite la función de listas de reproducción compartidas. Para asegurarse de que funciona correctamente, se requiere un servidor que ejecute Syncplay {}+, pero el servidor está ejecutando Syncplay {}.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "La función de lista de reproducción compartida no está habilitada en la configuración del servidor. Para utilizar esta función, debes conectarte a un servidor distinto.",

    "invalid-seek-value": "Valor de búsqueda inválido",
    "invalid-offset-value": "Valor de desplazamiento inválido",

    "switch-file-not-found-error": "No se pudo cambiar el archivo '{0}'. Syncplay busca en los directorios de medios especificados.",  # File not found
    "folder-search-timeout-error": "Se anuló la búsqueda de medios en el directorio de medios, ya que tardó demasiado buscando en '{}'. Esto ocurrirá si seleccionas una carpeta con demasiadas subcarpetas en tu lista de carpetas de medios para buscar. Para que el cambio automático de archivos vuelva a funcionar, selecciona Archivo->Establecer directorios de medios en la barra de menú y elimina este directorio o reemplázalo con una subcarpeta apropiada. Si la carpeta está bien, puedes volver a reactivarlo seleccionando Archivo->Establecer directorios de medios y presionando 'OK'.",  # Folder
    "folder-search-first-file-timeout-error": "Se anuló la búsqueda de medios en '{}', ya que tardó demasiado buscando en acceder al directorio. Esto podría ocurrir si se trata de una unidad de red, o si tienes configurada la unidad para centrifugar luego de cierto período de inactividad. Para que el cambio automático de archivos vuelva a funcionar, por favor dirígete a Archivo->Establecer directorios de medios y elimina el directorio o resuelve el problema (p.ej. cambiando la configuración de ahorro de energía).",  # Folder
    "added-file-not-in-media-directory-error": "Has cargado un archivo en '{}' el cual no es un directorio de medios conocido. Puedes agregarlo como un directorio de medios seleccionado Archivo->Establecer directorios de medios en la barra de menú.",  # Folder
    "no-media-directories-error": "No se han establecido directorios de medios. Para que las funciones de lista de reproducción compartida y cambio de archivos funcionen correctamente, selecciona Archivo->Establecer directorios de medios y especifica dónde debe buscar Syncplay para encontrar archivos multimedia.",
    "cannot-find-directory-error": "No se encontró el directorio de medios '{}'.Para actualizar tu lista de directorios de medios, seleccciona Archivo->Establecer directorios de medios desde la barra de menú y especifica dónde debe buscar Syncplay para encontrar archivos multimedia.",

    "failed-to-load-server-list-error": "Error al cargar la lista de servidor públicos. Por favor visita https://www.syncplay.pl/ en tu navegador.",

    # Client arguments
    "argument-description": 'Solución para sincronizar la reproducción de múltiples instancias de reproductores de medios, a través de la red.',
    "argument-epilog": 'Si no se especifican opciones, se utilizarán los valores de _config',
    "nogui-argument": 'no mostrar GUI',
    "host-argument": 'dirección del servidor',
    "name-argument": 'nombre de usuario deseado',
    "debug-argument": 'modo debug',
    "force-gui-prompt-argument": 'hacer que aparezca el aviso de configuración',
    "no-store-argument": 'no guardar valores en .syncplay',
    "room-argument": 'sala por defecto',
    "password-argument": 'contraseña del servidor',
    "player-path-argument": 'ruta al ejecutable de tu reproductor',
    "file-argument": 'archivo a reproducir',
    "args-argument": 'opciones del reproductor, si necesitas pasar opciones que empiezan con -, pásalas utilizando \'--\'',
    "clear-gui-data-argument": 'restablece ruta y los datos del estado de la ventana GUI almacenados como QSettings',
    "language-argument": 'lenguaje para los mensajes de Syncplay (de/en/ru/it/es/pt_BR/pt_PT/tr/fr/zh_CN)',

    "version-argument": 'imprime tu versión',
    "version-message": "Estás usando la versión de Syncplay {} ({})",

    "load-playlist-from-file-argument": "loads playlist from text file (one entry per line)", # TODO: Translate

    # Client labels
    "config-window-title": "Configuración de Syncplay",

    "connection-group-title": "Configuración de conexión",
    "host-label": "Dirección del servidor: ",
    "name-label":  "Nombre de usuario (opcional):",
    "password-label":  "Contraseña del servidor (si corresponde):",
    "room-label": "Sala por defecto: ",
    "roomlist-msgbox-label": "Edit room list (one per line)", # TODO: Translate

    "media-setting-title": "Configuración del reproductor multimedia",
    "executable-path-label": "Ruta al reproductor multimedia:",
    "media-path-label": "Ruta al video (opcional):",
    "player-arguments-label": "Argumentos del reproductor (si corresponde):",
    "browse-label": "Visualizar",
    "update-server-list-label": "Actualizar lista",

    "more-title": "Mostrar más configuraciones",
    "never-rewind-value": "Nunca",
    "seconds-suffix": " segs",
    "privacy-sendraw-option": "Enviar crudo",
    "privacy-sendhashed-option": "Enviar \"hasheado\"",
    "privacy-dontsend-option": "No enviar",
    "filename-privacy-label": "Información del nombre de archivo:",
    "filesize-privacy-label": "Información del tamaño de archivo:",
    "checkforupdatesautomatically-label": "Buscar actualizaciones de Syncplay automáticamente",
    "autosavejoinstolist-label": "Add rooms you join to the room list", # TO DO: Translate
    "slowondesync-label": "Ralentizar si hay una desincronización menor (no soportado en MPC-HC/BE)",
    "rewindondesync-label": "Rebobinar si hay una desincronización mayor (recomendado)",
    "fastforwardondesync-label": "Avanzar rápidamente si hay un retraso (recomendado)",
    "dontslowdownwithme-label": "Nunca ralentizar ni rebobinar a otros (experimental)",
    "pausing-title": "Pausando",
    "pauseonleave-label": "Pausar cuando un usuario se va (p.ej. si se desconectan)",
    "readiness-title": "Estado de preparación inicial",
    "readyatstart-label": "Establecerme como \"listo-para-ver\" por defecto",
    "forceguiprompt-label": "No mostrar siempre la ventana de configuración de Syncplay",  # (Inverted)
    "showosd-label": "Activar mensajes OSD",

    "showosdwarnings-label": "Incluir advertencias (p.ej. cuando los archivos son distintos, los usuarios no están listos)",
    "showsameroomosd-label": "Incluir eventos en tu sala",
    "shownoncontrollerosd-label": "Incluir eventos de no-operadores en salas administradas",
    "showdifferentroomosd-label": "Incluir eventos en otras salas",
    "showslowdownosd-label": "Incluir notificaciones de ralentización/reversión",
    "language-label": "Lenguaje:",
    "automatic-language": "Predeterminado ({})",  # Default language
    "showdurationnotification-label": "Advertir sobre discrepancias en la duración de los medios",
    "basics-label": "Básicos",
    "readiness-label": "Reproducir/Pausar",
    "misc-label": "Misc.",
    "core-behaviour-title": "Comportamiento de la sala central",
    "syncplay-internals-title": "Internos de Syncplay",
    "syncplay-mediasearchdirectories-title": "Directorios para buscar medios",
    "syncplay-mediasearchdirectories-label": "Directorios para buscar medios (una ruta por línea)",
    "sync-label": "Sincronizar",
    "sync-otherslagging-title": "Si otros se están quedando atrás...",
    "sync-youlaggging-title": "Si tú te estás quedando atrás...",
    "messages-label": "Mensajes",
    "messages-osd-title": "Configuraciones de visualización en pantalla",
    "messages-other-title": "Otras configuraciones de visualización",
    "chat-label": "Chat",
    "privacy-label": "Privacidad",  # Currently unused, but will be brought back if more space is needed in Misc tab
    "privacy-title": "Configuración de privacidad",
    "unpause-title": "Si presionas reproducir, definir como listo y:",
    "unpause-ifalreadyready-option": "Despausar si ya está definido como listo",
    "unpause-ifothersready-option": "Despausar si ya está listo u otros en la sala están listos (predeterminado)",
    "unpause-ifminusersready-option": "Despausar si ya está listo, o si todos los demás están listos y el mín. de usuarios están listos",
    "unpause-always": "Siempre despausar",
    "syncplay-trusteddomains-title": "Dominios de confianza (para servicios de transmisión y contenido alojado)",

    "chat-title": "Entrada de mensaje de chat",
    "chatinputenabled-label": "Habilitar entrada de chat a través de mpv",
    "chatdirectinput-label": "Permitir entrada de chat instantánea (omitir tener que presionar Intro para chatear)",
    "chatinputfont-label": "Fuente de entrada de chat",
    "chatfont-label": "Establecer fuente",
    "chatcolour-label": "Establecer color",
    "chatinputposition-label": "Posición del área de entrada del mensaje en mpv",
    "chat-top-option": "Arriba",
    "chat-middle-option": "Medio",
    "chat-bottom-option": "Fondo",
    "chatoutputheader-label": "Salida de mensaje de chat",
    "chatoutputfont-label": "Fuente de salida de chat",
    "chatoutputenabled-label": "Habilitar salida de chat en el reproductor (solo mpv por ahora)",
    "chatoutputposition-label": "Modo de salida",
    "chat-chatroom-option": "Estilo de sala de chat",
    "chat-scrolling-option": "Estilo de desplazamiento",

    "mpv-key-tab-hint": "[TAB] para alternar acceso a los accesos directos de las teclas de la fila del alfabeto",
    "mpv-key-hint": "[INTRO] para enviar mensaje. [ESC] para salir del modo de chat.",
    "alphakey-mode-warning-first-line": "Puedes usar temporalmente los enlaces de mpv con las teclas a-z.",
    "alphakey-mode-warning-second-line": "Presiona [TAB] para retornar al modo de chat de Syncplay.",

    "help-label": "Ayuda",
    "reset-label": "Restaurar valores predeterminados",
    "run-label": "Ejecutar Syncplay",
    "storeandrun-label": "Almacenar la configuración y ejecutar Syncplay",

    "contact-label": "No dudes en enviar un correo electrónico a <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a>, <a href=\"https://github.com/Syncplay/syncplay/issues\"><nobr>reportar un problema</nobr></a> vía GitHub / <a href=\"https://github.com/Syncplay/syncplay/discussions\"><nobr>start a discussion</nobr></a> to make a suggestion or ask a question via GitHub, <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>danos \"me gusta\" en Facebook</nobr></a>, <a href=\"https://twitter.com/Syncplay/\"><nobr>síguenos en Twitter</nobr></a>, o visita <a href=\"https://syncplay.pl/\"><nobr>https://syncplay.pl/</nobr></a>. No utilices Syncplay para enviar información sensible.", # TODO: Update translation

    "joinroom-label": "Unirse a la sala",
    "joinroom-menu-label": "Unirse a la sala {}",
    "seektime-menu-label": "Buscar tiempo",
    "undoseek-menu-label": "Deshacer búsqueda",
    "play-menu-label": "Reproducir",
    "pause-menu-label": "Pausar",
    "playbackbuttons-menu-label": "Mostrar botones de reproducción",
    "autoplay-menu-label": "Mostrar botón de auto-reproducción",
    "autoplay-guipushbuttonlabel": "Reproducir cuando todos estén listos",
    "autoplay-minimum-label": "Mín. de usuarios:",
    "hideemptyrooms-menu-label": "Hide empty persistent rooms", # TODO: Translate

    "sendmessage-label": "Enviar",

    "ready-guipushbuttonlabel": "¡Estoy listo para ver!",

    "roomuser-heading-label": "Sala / Usuario",
    "size-heading-label": "Tamaño",
    "duration-heading-label": "Duración",
    "filename-heading-label": "Nombre de archivo",
    "notifications-heading-label": "Notificaciones",
    "userlist-heading-label": "Lista de quién reproduce qué",

    "browseformedia-label": "Buscar archivos multimedia",

    "file-menu-label": "&Archivo",  # & precedes shortcut key
    "openmedia-menu-label": "A&brir archivo multimedia",
    "openstreamurl-menu-label": "Abrir URL de &flujo de medios",
    "setmediadirectories-menu-label": "&Establecer directorios de medios",
    "loadplaylistfromfile-menu-label": "&Load playlist from file",  # TODO: Translate
    "saveplaylisttofile-menu-label": "&Save playlist to file",  # TODO: Translate
    "exit-menu-label": "&Salir",
    "advanced-menu-label": "A&vanzado",
    "window-menu-label": "&Ventana",
    "setoffset-menu-label": "Establecer &compensación",
    "createcontrolledroom-menu-label": "C&rear sala administrada",
    "identifyascontroller-menu-label": "&Identificar como operador de sala",
    "settrusteddomains-menu-label": "Es&tablecer dominios de confianza",
    "addtrusteddomain-menu-label": "Agregar {} como dominio de confianza",  # Domain

    "edit-menu-label": "&Edición",
    "cut-menu-label": "Cor&tar",
    "copy-menu-label": "&Copiar",
    "paste-menu-label": "&Pegar",
    "selectall-menu-label": "&Seleccionar todo",

    "playback-menu-label": "Re&producción",

    "help-menu-label": "A&yuda",
    "userguide-menu-label": "Abrir &guía de usuario",
    "update-menu-label": "Buscar actuali&zaciones",

    "startTLS-initiated": "Intentando conexión segura",
    "startTLS-secure-connection-ok": "Conexión segura establecida ({})",
    "startTLS-server-certificate-invalid": 'Falló la conexión segura. El servidor utiliza un certificado inválido. Esta comunicación podría ser interceptada por un tercero. Para más detalles y solución de problemas, consulta <a href="https://syncplay.pl/trouble">aquí</a>.',
    "startTLS-server-certificate-invalid-DNS-ID": "Syncplay does not trust this server because it uses a certificate that is not valid for its hostname.", # TODO: Translate
    "startTLS-not-supported-client": "Este cliente no soporta TLS",
    "startTLS-not-supported-server": "Este servidor no soporta TLS",

    # TLS certificate dialog
    "tls-information-title": "Detalles del certificado",
    "tls-dialog-status-label": "<strong>Syncplay está utilizando una conexión cifrada con {}.</strong>",
    "tls-dialog-desc-label": "El cifrado con un certificado digital, mantiene la información privada cuando se envía hacia o desde<br/>el servidor {}.",
    "tls-dialog-connection-label": "Información cifrada utilizando \"Transport Layer Security\" (TLS), versión {} con la<br/>suite de cifrado: {}.",
    "tls-dialog-certificate-label": "Certificado emitido por {} válido hasta {}.",

    # About dialog
    "about-menu-label": "Acerca de Sy&ncplay",
    "about-dialog-title": "Acerca de Syncplay",
    "about-dialog-release": "Versión {} lanzamiento {}",
    "about-dialog-license-text": "Licenciado bajo la Licencia Apache Versión 2.0",
    "about-dialog-license-button": "Licencia",
    "about-dialog-dependencies": "Dependencias",

    "setoffset-msgbox-label": "Establecer compensación",
    "offsetinfo-msgbox-label": "Compensación (consulta https://syncplay.pl/guide/ para obtener instrucciones de uso):",

    "promptforstreamurl-msgbox-label": "Abrir URL de flujo de medios",
    "promptforstreamurlinfo-msgbox-label": "Publicar URL",

    "addfolder-label": "Agregar carpeta",

    "adduris-msgbox-label": "Agregar URLs a la lista de reproducción (una por línea)",
    "editplaylist-msgbox-label": "Establecer lista de reproducción (una por línea)",
    "trusteddomains-msgbox-label": "Dominios con los cuales está bien intercambiar automáticamente (uno por línea)",

    "createcontrolledroom-msgbox-label": "Crear sala administrada",
    "controlledroominfo-msgbox-label": "Ingresa el nombre de la sala administrada\r\n(consulta https://syncplay.pl/guide/ para obtener instrucciones de uso):",

    "identifyascontroller-msgbox-label": "Identificar como operador de la sala",
    "identifyinfo-msgbox-label": "Ingresa la contraseña de operador para esta sala\r\n(consulta https://syncplay.pl/guide/ para obtener instrucciones de uso):",

    "public-server-msgbox-label": "Selecciona el servidor público para esta sesión de visualización",

    "megabyte-suffix": " MB",

    # Tooltips

    "host-tooltip": "Nombre de host o IP para conectarse, opcionalmente incluyendo puerto (p.ej. syncplay.pl:8999). Sólo sincronizado con personas en el mismo servidor/puerto.",
    "name-tooltip": "Apodo por el que se te conocerá. No hay registro, por lo que puedes cambiarlo fácilmente más tarde. Si no se especifica, se genera un nombre aleatorio.",
    "password-tooltip": "Las contraseñas son sólo necesarias para conectarse a servidores privados.",
    "room-tooltip": "La sala para unirse en la conexión puede ser casi cualquier cosa, pero sólo se sincronizará con las personas en la misma sala.",

    "edit-rooms-tooltip": "Edit room list.", # TO DO: Translate

    "executable-path-tooltip": "Ubicación de tu reproductor multimedia compatible elegido (mpv, mpv.net, VLC, MPC-HC/BE, mplayer2 o IINA).",
    "media-path-tooltip": "Ubicación del video o flujo que se abrirá. Necesario para mplayer2.",
    "player-arguments-tooltip": "Arguementos de línea de comandos adicionales / parámetros para pasar a este reproductor multimedia.",
    "mediasearcdirectories-arguments-tooltip": "Directorios donde Syncplay buscará archivos de medios, p.ej. cuando estás usando la función \"clic para cambiar\". Syncplay buscará recursivamente a través de las subcarpetas.",

    "more-tooltip": "Mostrar configuraciones usadas con menos frecuencia.",
    "filename-privacy-tooltip": "Modo de privacidad para enviar el nombre del archivo que se está reproduciendo actualmente al servidor.",
    "filesize-privacy-tooltip": "Modo de privacidad para enviar el tamaño del archivo que se está reproduciendo actualmente al servidor.",
    "privacy-sendraw-tooltip": "Enviar esta información sin ofuscación. Ésta es la opción predeterminada en la mayoría de las funciones.",
    "privacy-sendhashed-tooltip": "Enviar una versión \"hasheada\" de la información, para que sea menos visible para otros clientes.",
    "privacy-dontsend-tooltip": "No enviar esta información al servidor. Esto proporciona la máxima privacidad.",
    "checkforupdatesautomatically-tooltip": "Regularmente verificar con el sitio Web de Syncplay para ver si hay una nueva versión de Syncplay disponible.",
    "autosavejoinstolist-tooltip": "When you join a room in a server, automatically remember the room name in the list of rooms to join.", # TO DO: Translate
    "slowondesync-tooltip": "Reducir la velocidad de reproducción temporalmente cuando sea necesario, para volver a sincronizar con otros espectadores. No soportado en MPC-HC/BE.",
    "dontslowdownwithme-tooltip": "Significa que otros no se ralentizan ni rebobinan si la reproducción se retrasa. Útil para operadores de la sala.",
    "pauseonleave-tooltip": "Pausa la reproducción si te desconectas o alguien sale de tu sala.",
    "readyatstart-tooltip": "Establecerte como 'listo' al inicio (de lo contrario, se te establecerá como 'no-listo' hasta que cambies tu estado de preparación)",
    "forceguiprompt-tooltip": "El diálogo de configuración no es mostrado cuando se abre un archivo con Syncplay.",  # (Inverted)
    "nostore-tooltip": "Ejecutar Syncplay con la configuración dada, pero no guardar los cambios permanentemente.",  # (Inverted)
    "rewindondesync-tooltip": "Retroceder cuando sea necesario para volver a sincronizar. ¡Deshabilitar esta opción puede resultar en desincronizaciones importantes!",
    "fastforwardondesync-tooltip": "Saltar hacia adelante cuando no está sincronizado con el operador de la sala (o tu posición ficticia 'Nunca ralentizar o rebobinar a otros' está activada).",
    "showosd-tooltip": "Envía mensajes de Syncplay al reproductor multimedia OSD.",
    "showosdwarnings-tooltip": "Mostrar advertencias si se está reproduciendo un archivo diferente, solo en la sala, usuarios no están listos, etc.",
    "showsameroomosd-tooltip": "Mostrar notificaciones de OSD para eventos relacionados con la sala en la que está el usuario.",
    "shownoncontrollerosd-tooltip": "Mostrar notificaciones de OSD para eventos relacionados con no-operadores que están en salas administradas.",
    "showdifferentroomosd-tooltip": "Mostrar notificaciones de OSD para eventos relacionados la sala en la que no está el usuario.",
    "showslowdownosd-tooltip": "Mostrar notificaciones de desaceleración / diferencia de la reversión.",
    "showdurationnotification-tooltip": "Útil cuando falta un segmento de un archivo de varias partes, pero puede dar lugar a falsos positivos.",
    "language-tooltip": "Idioma a ser utilizado por Syncplay.",
    "unpause-always-tooltip": "Si presionas despausar siempre te pone como listo y despausa, en lugar de simplemente ponerte como listo.",
    "unpause-ifalreadyready-tooltip": "Si presionas despausar cuando no estás listo, te pondrá como listo - presiona despausar nuevamente para despausar.",
    "unpause-ifothersready-tooltip": "Si presionas despausar cuando no estás listo, sólo se despausará si los otros están listos.",
    "unpause-ifminusersready-tooltip": "Si presionas despausar cuando no estás listo, sólo se despausará si los otros están listos y se cumple con el mínimo requerido de usuarios.",
    "trusteddomains-arguments-tooltip": "Dominios con los cuales está bien intercambiar automáticamente, cuando las listas de reproducción compartidas están activas.",

    "chatinputenabled-tooltip": "Activa la entrada de chat en mpv (presiona intro para chatear, intro para enviar, escape para cancelar)",
    "chatdirectinput-tooltip": "Omitir tener que presionar 'intro' para ir al modo de entrada de chat en mpv. Presiona TAB en mpv para desactivar temporalmente esta función.",
    "font-label-tooltip": "Fuente utilizada cuando se ingresan mensajes de chat en mpv. Sólo del lado del cliente, por lo que no afecta lo que otros ven.",
    "set-input-font-tooltip": "Familia de fuentes utilizada cuando se ingresan mensajes de chat en mpv. Sólo del lado del cliente, por lo que no afecta lo que otros ven.",
    "set-input-colour-tooltip": "Color de fuente utilizado cuando se ingresan mensajes de chat en mpv. Sólo del lado del cliente, por lo que no afecta lo que otros ven.",
    "chatinputposition-tooltip": "Ubicación en mpv donde aparecerán los mensajes de chat cuando se presione intro y se escriba.",
    "chatinputposition-top-tooltip": "Colocar la entrada del chat en la parte superior de la ventana de mpv.",
    "chatinputposition-middle-tooltip": "Colocar la entrada del chat en el centro muerto de la ventana de mpv.",
    "chatinputposition-bottom-tooltip": "Colocar la entrada del chat en la parte inferior de la ventana de mpv.",
    "chatoutputenabled-tooltip": "Mostrar mensajes de chat en OSD (si está soportado por el reproductor multimedia).",
    "font-output-label-tooltip": "Fuente de salida del chat.",
    "set-output-font-tooltip": "Fuente utilizada para mostrar mensajes de chat.",
    "chatoutputmode-tooltip": "Cómo se muestran los mensajes de chat.",
    "chatoutputmode-chatroom-tooltip": "Mostrar nuevas líneas de chat directamente debajo de la línea anterior.",
    "chatoutputmode-scrolling-tooltip": "Desplazar el texto del chat de derecha a izquierda.",

    "help-tooltip": "Abrir la guía de usuario de Syncplay.pl.",
    "reset-tooltip": "Restablecer todas las configuraciones a la configuración predeterminada.",
    "update-server-list-tooltip": "Conectar a syncplay.pl para actualizar la lista de servidores públicos.",

    "sslconnection-tooltip": "Conectado de forma segura al servidor. Haga clic para obtener los detalles del certificado.",

    "joinroom-tooltip": "Abandonar la sala actual y unirse a la sala especificada.",
    "seektime-msgbox-label": "Saltar al tiempo especificado (en segundos / min:seg). Usar +/- para una búsqueda relativa.",
    "ready-tooltip": "Indica si estás listo para ver.",
    "autoplay-tooltip": "Reproducir automáticamente cuando todos los usuarios que tienen indicador de preparación están listos, y se ha alcanzado el mínimo requerido de usuarios.",
    "switch-to-file-tooltip": "Hacer doble clic para cambiar a {}",  # Filename
    "sendmessage-tooltip": "Enviar mensaje a la sala",

    # In-userlist notes (GUI)
    "differentsize-note": "¡Tamaño diferente!",
    "differentsizeandduration-note": "¡Tamaño y duración diferentes!",
    "differentduration-note": "¡Duración diferente!",
    "nofile-note": "(No se está reproduciendo ningún archivo)",

    # Server messages to client
    "new-syncplay-available-motd-message": "Estás usando Syncplay {} pero hay una versión más nueva disponible en https://syncplay.pl",  # ClientVersion
    "persistent-rooms-notice": "NOTICE: This server uses persistent rooms, which means that the playlist information is stored between playback sessions. If you want to create a room where information is not saved then put -temp at the end of the room name.", # TO DO: Translate - NOTE: Do not translate the word -temp

    # Server notifications
    "welcome-server-notification": "Bienvenido al servidor de Syncplay, ver. {0}",  # version
    "client-connected-room-server-notification": "{0}({2}) conectado a la sala '{1}'",  # username, host, room
    "client-left-server-notification": "{0} abandonó el servidor",  # name
    "no-salt-notification": "IMPORTANTE: Para permitir que las contraseñas del operador de la sala, generadas por esta instancia del servidor, sigan funcionando cuando se reinicie el servidor, por favor en el futuro agregar el siguiente argumento de línea de comandos al ejecutar el servidor de Syncplay: --salt {}",  # Salt


    # Server arguments
    "server-argument-description": 'Solución para sincronizar la reproducción de múltiples instancias de MPlayer y MPC-HC/BE a través de la red. Instancia del servidor',
    "server-argument-epilog": 'Si no se especifican opciones, serán utilizados los valores de _config',
    "server-port-argument": 'puerto TCP del servidor',
    "server-password-argument": 'contraseña del servidor',
    "server-isolate-room-argument": '¿las salas deberían estar aisladas?',
    "server-salt-argument": "cadena aleatoria utilizada para generar contraseñas de salas administradas",
    "server-disable-ready-argument": "deshabilitar la función de preparación",
    "server-motd-argument": "ruta al archivo del cual se obtendrá el texto motd",
    "server-rooms-argument": "path to database file to use and/or create to store persistent room data. Enables rooms to persist without watchers and through restarts", # TODO: Translate
    "server-permanent-rooms-argument": "path to file which lists permenant rooms that will be listed even if the room is empty (in the form of a text file which lists one room per line) - requires persistent rooms to be enabled", # TODO: Translate
    "server-chat-argument": "¿Debería deshabilitarse el chat?",
    "server-chat-maxchars-argument": "Número máximo de caracteres en un mensaje de chat (el valor predeterminado es {})", # Default number of characters
    "server-maxusernamelength-argument": "Número máximo de caracteres para el nombre de usuario (el valor predeterminado es {})",
    "server-stats-db-file-argument": "Habilitar estadísticas del servidor utilizando el archivo db SQLite proporcionado",
    "server-startTLS-argument": "Habilitar conexiones TLS usando los archivos de certificado en la ruta provista",
    "server-messed-up-motd-unescaped-placeholders": "El mensaje del dia contiene marcadores de posición sin escapar. Todos los signos $ deberían ser dobles ($$).",
    "server-messed-up-motd-too-long": "El mensaje del día es muy largo - máximo de {} caracteres, se recibieron {}.",

    # Server errors
    "unknown-command-server-error": "Comando desconocido {}",  # message
    "not-json-server-error": "No es una cadena JSON válida {}",  # message
    "line-decode-server-error": "No es una cadena utf-8",
    "not-known-server-error": "Debes ser reconocido por el servidor antes de enviar este comando",
    "client-drop-server-error": "Caída del cliente: {} -- {}",  # host, error
    "password-required-server-error": "Contraseña requerida",
    "wrong-password-server-error": "Contraseña ingresada incorrecta",
    "hello-server-error": "Not enough Hello arguments",  # DO NOT TRANSLATE

    # Playlists
    "playlist-selection-changed-notification":  "{} cambió la selección de la lista de reproducción",  # Username
    "playlist-contents-changed-notification": "{} actualizó la lista de reproducción",  # Username
    "cannot-find-file-for-playlist-switch-error": "¡No se encontró el archivo {} en el directorio de medios para intercambiar en la lista de reproducción!",  # Filename
    "cannot-add-duplicate-error": "No se pudo agregar una segunda entrada para '{}' a la lista de reproducción ya que no se admiten duplicados.",  # Filename
    "cannot-add-unsafe-path-error": "No se pudo cargar automáticamente {} porque no es un dominio de confianza. Puedes intercambiar la URL manualmente dándole doble clic en la lista de reproducción, y agregar dominios de confianza vía Archivo->Avanzado->Establecer dominios de confianza. Si haces doble clic en una URL entonces puedes agregar su dominio como un dominio de confianza, desde el menú de contexto.",  # Filename
    "sharedplaylistenabled-label": "Activar listas de reproducción compartidas",
    "removefromplaylist-menu-label": "Remover de la lista de reproducción",
    "shuffleremainingplaylist-menu-label": "Mezclar el resto de la lista de reproducción",
    "shuffleentireplaylist-menu-label": "Mezclar toda la lista de reproducción",
    "undoplaylist-menu-label": "Deshacer el último cambio a la lista de reproducción",
    "addfilestoplaylist-menu-label": "Agregar archivo(s) al final de la lista de reproducción",
    "addurlstoplaylist-menu-label": "Agregar URL(s) al final de la lista de reproducción",
    "editplaylist-menu-label": "Editar lista de reproducción",

    "open-containing-folder": "Abrir directorio que contiene este archivo",
    "addyourfiletoplaylist-menu-label": "Agregar tu archivo a la lista de reproducción",
    "addotherusersfiletoplaylist-menu-label": "Agregar el archivo de {} a la lista de reproducción",  # [Username]
    "addyourstreamstoplaylist-menu-label": "Agregar tu flujo a la lista de reproducción",
    "addotherusersstreamstoplaylist-menu-label": "Agregar el flujo de {} a la lista de reproducción",  # [Username]
    "openusersstream-menu-label": "Abrir el flujo de {}",  # [username]'s
    "openusersfile-menu-label": "Abrir el archivo de {}",  # [username]'s

    "playlist-instruction-item-message": "Desplazar aquí el archivo para agregarlo a la lista de reproducción compartida.",
    "sharedplaylistenabled-tooltip": "Los operadores de la sala pueden agregar archivos a una lista de reproducción sincronizada, para que visualizar la misma cosa sea más sencillo para todos. Configurar directorios multimedia en 'Misc'.",

    "playlist-empty-error": "Playlist is currently empty.", # TO DO: Translate
    "playlist-invalid-index-error": "Invalid playlist index", # TO DO: Translate
}
