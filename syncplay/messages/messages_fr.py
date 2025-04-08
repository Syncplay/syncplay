# coding:utf8

"""French dictionary"""

# Filename, dictionary name and LANGUAGE-TAG value based on ISO country code. Language tag listed at https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/a9eac961-e77d-41a6-90a5-ce1a8b0cdb9c?redirectedfrom=MSDN

fr = {
    "LANGUAGE": "Français",
    "LANGUAGE-TAG": "fr",

    # Strings for Windows NSIS installer
    "installer-language-file": "French.nlf", # Relevant .nlf file at https://github.com/kichik/nsis/tree/master/Contrib/Language%20files
    "installer-associate": "Associer Syncplay avec les fichiers multimedias.",
    "installer-shortcut": "Créer Racourcis pour les chemins suivants:",
    "installer-start-menu": "Menu Démarrer",
    "installer-desktop": "Bureau",
    "installer-quick-launch-bar": "Barre de Lancement Rapide",
    "installer-automatic-updates": "Vérifier automatiquement les mises à jour",
    "installer-uninstall-configuration": "Supprimer le fichier de configuration.",

    # Client notifications
    "config-cleared-notification": "Paramètres effacés. Les modifications seront enregistrées lorsque vous enregistrez une configuration valide.",

    "relative-config-notification": "Fichiers de configuration relatifs chargés: {}",

    "connection-attempt-notification": "Tentative de connexion à {}:{}",  # Port, IP
    "reconnection-attempt-notification": "Connexion avec le serveur perdue, tentative de reconnexion",
    "disconnection-notification": "Déconnecté du serveur",
    "connection-failed-notification": "Échec de la connexion avec le serveur",
    "connected-successful-notification": "Connexion réussie au serveur",
    "retrying-notification": "%s, nouvelle tentative dans %d secondes...",  # Seconds
    "reachout-successful-notification": "Vous avez atteint {} ({})",

    "rewind-notification": "Retour en arrière en raison du décalage de temps avec {}",  # User
    "fastforward-notification": "Avance rapide en raison du décalage de temps avec {}",  # User
    "slowdown-notification": "Ralentissement dû au décalage de temps avec {}",  # User
    "revert-notification": "Retour à la vitesse normale",

    "pause-notification": "{} en pause ({})",  # User, Time - TODO: Change into format "{} paused at {}" in line with English message
    "unpause-notification": "{} non suspendu",  # User
    "seek-notification": "{} est passé de {} à {}",  # User, from time, to time

    "current-offset-notification": "Décalage actuel: {}secondes",  # Offset

    "media-directory-list-updated-notification": "Les répertoires multimédias Syncplay ont été mis à jour.",

    "room-join-notification": "{} a rejoint la salle: '{}'",  # User
    "left-notification": "{} est parti",  # User
    "left-paused-notification": "{} restants, {} en pause",  # User who left, User who paused
    "playing-notification": "{} est en train de jouer '{}' ({})",  # User, file, duration
    "playing-notification/room-addendum": "dans le salon: '{}'",  # Room

    "not-all-ready": "Pas prêt: {}",  # Usernames
    "all-users-ready": "Tout le monde est prêt ({} utilisateurs)",  # Number of ready users
    "ready-to-unpause-notification": "Vous êtes maintenant défini comme prêt - réactivez la pause pour réactiver",
    "set-as-ready-notification": "Vous êtes maintenant défini comme prêt",
    "set-as-not-ready-notification": "Vous êtes maintenant défini comme non prêt",
    "autoplaying-notification": "Lecture automatique dans {}...",  # Number of seconds until playback will start

    "identifying-as-controller-notification": "Identification en tant qu'opérateur de salle avec le mot de passe '{}'...",
    "failed-to-identify-as-controller-notification": "{} n'a pas réussi à s'identifier en tant qu'opérateur de salle.",
    "authenticated-as-controller-notification": "{} authentifié en tant qu'opérateur de salle",
    "created-controlled-room-notification": "Salle gérée créée «{}» avec le mot de passe «{}». Veuillez conserver ces informations pour référence future !\n\nDans les salons gérés, tout le monde est synchronisé avec le ou les opérateurs de salon qui sont les seuls à pouvoir mettre en pause, reprendre, se déplacer dans la lecture et modifier la liste de lecture.\n\nVous devez demander aux spectateurs réguliers de rejoindre le salon '{}' mais les opérateurs de salon peuvent rejoindre le salon '{}' pour s'authentifier automatiquement.",  # RoomName, operatorPassword, roomName, roomName:operatorPassword

    "other-set-as-ready-notification": "{} was set as ready by {}", # User set as ready, user who set them as ready # TODO: Translate
    "other-set-as-not-ready-notification": "{} was set as not ready by {}", # User set as not ready, user who set them as not ready # TODO: Translate

    "file-different-notification": "Le fichier que vous lisez semble être différent de celui de {}",  # User
    "file-differences-notification": "Votre fichier diffère de la (des) manière(s) suivante(s): {}",  # Differences
    "room-file-differences": "Différences de fichiers: {}",  # File differences (filename, size, and/or duration)
    "file-difference-filename": "Nom",
    "file-difference-filesize": "Taille",
    "file-difference-duration": "durée",
    "alone-in-the-room": "Vous êtes seul dans le salon",

    "different-filesize-notification": "(leur taille de fichier est différente de la vôtre!)",
    "userlist-playing-notification": "{} est en train de jouer:",  # Username
    "file-played-by-notification": "Fichier: {} est lu par:",  # File
    "no-file-played-notification": "{} ne lit pas de fichier",  # Username
    "notplaying-notification": "Les personnes qui ne lisent aucun fichier:",
    "userlist-room-notification": "Dans la chambre '{}':",  # Room
    "userlist-file-notification": "Fichier",
    "controller-userlist-userflag": "Opérateur",
    "ready-userlist-userflag": "Prêt",

    "update-check-failed-notification": "Impossible de vérifier automatiquement si Syncplay {} est à jour. Vous voulez visiter https://syncplay.pl/ pour vérifier manuellement les mises à jour?",  # Syncplay version
    "syncplay-uptodate-notification": "Syncplay est à jour",
    "syncplay-updateavailable-notification": "Une nouvelle version de Syncplay est disponible. Voulez-vous visiter la page de publication?",

    "mplayer-file-required-notification": "Syncplay à l'aide de mplayer nécessite que vous fournissiez un fichier au démarrage",
    "mplayer-file-required-notification/example": "Exemple d'utilisation: syncplay [options] [url|chemin/]nom de fichier",
    "mplayer2-required": "Syncplay est incompatible avec MPlayer 1.x, veuillez utiliser mplayer2 ou mpv",

    "unrecognized-command-notification": "commande non reconnue",
    "commandlist-notification": "Commandes disponibles:",
    "commandlist-notification/room": "\tr [nom] - changer de chambre",
    "commandlist-notification/list": "\tl - afficher la liste des utilisateurs",
    "commandlist-notification/undo": "\tu - annuler la dernière recherche",
    "commandlist-notification/pause": "\tp - basculer sur pause",
    "commandlist-notification/seek": "\t[s][+-]temps - recherche la valeur de temps donnée, si + ou - n'est pas spécifié c'est le temps absolu en secondes ou min:sec",
    "commandlist-notification/offset": "\to[+-]duration - offset local playback by the given duration (in seconds or min:sec) from the server seek position - this is a deprecated feature", # TODO: Translate
    "commandlist-notification/help": "\th - cette aide",
    "commandlist-notification/toggle": "\tt - bascule si vous êtes prêt à regarder ou non",
    "commandlist-notification/setready": "\tsr [name] - sets user as ready",  # TODO: Translate
    "commandlist-notification/setnotready": "\tsn [name] - sets user as not ready",  # TODO: Translate
    "commandlist-notification/create": "\tc [nom] - crée une salle gérée en utilisant le nom de la salle actuelle",
    "commandlist-notification/auth": "\tun [mot de passe] - s'authentifier en tant qu'opérateur de salle avec le mot de passe opérateur",
    "commandlist-notification/chat": "\tch [message] - envoyer un message de chat dans une pièce",
    "commandList-notification/queue": "\tqa [fichier/url] - ajoute un fichier ou une URL au bas de la liste de lecture",
    "commandList-notification/queueandselect": "\tqas [file/url] - add file or url to bottom of playlist and select it", # TODO: Translate
    "commandList-notification/playlist": "\tql - afficher la liste de lecture actuelle",
    "commandList-notification/select": "\tqs [index] - sélectionnez l'entrée donnée dans la liste de lecture",
    "commandList-notification/next": "\tqn - select next entry in the playlist", # TODO: Translate
    "commandList-notification/delete": "\tqd [index] - supprime l'entrée donnée de la liste de lecture",
    "syncplay-version-notification": "Version de Syncplay: {}",  # syncplay.version
    "more-info-notification": "Plus d'informations disponibles sur: {}",  # projectURL

    "gui-data-cleared-notification": "Syncplay a effacé les données d'état de chemin et de fenêtre utilisées par l'interface graphique.",
    "language-changed-msgbox-label": "La langue sera modifiée lorsque vous exécuterez Syncplay.",
    "promptforupdate-label": "Est-ce que Syncplay peut vérifier automatiquement les mises à jour de temps en temps?",

    "media-player-latency-warning": "Avertissement: Le lecteur multimédia a mis {}secondes à répondre. Si vous rencontrez des problèmes de synchronisation, fermez les applications pour libérer des ressources système, et si cela ne fonctionne pas, essayez un autre lecteur multimédia.",  # Seconds to respond
    "mpv-unresponsive-error": "mpv n'a pas répondu pendant {} secondes et semble donc avoir mal fonctionné. Veuillez redémarrer Syncplay.",  # Seconds to respond

    # Client prompts
    "enter-to-exit-prompt": "Appuyez sur entrée pour quitter",

    # Client errors
    "missing-arguments-error": "Certains arguments nécessaires sont manquants, reportez-vous à --help",
    "server-timeout-error": "La connexion avec le serveur a expiré",
    "mpc-slave-error": "Impossible de démarrer MPC en mode esclave!",
    "mpc-version-insufficient-error": "La version MPC n'est pas suffisante, veuillez utiliser `mpc-hc` >= `{}`",
    "mpc-be-version-insufficient-error": "La version MPC n'est pas suffisante, veuillez utiliser `mpc-be` >= `{}`",
    "mpv-version-error": "Syncplay n'est pas compatible avec cette version de mpv. Veuillez utiliser une version différente de mpv (par exemple Git HEAD).",
    "mpv-failed-advice": "La raison pour laquelle mpv ne peut pas démarrer peut être due à l'utilisation d'arguments de ligne de commande non pris en charge ou à une version non prise en charge de mpv.",
    "player-file-open-error": "Le lecteur n'a pas réussi à ouvrir le fichier",
    "player-path-error": "Le chemin du lecteur n'est pas défini correctement. Les lecteurs pris en charge sont : mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 et IINA",
    "hostname-empty-error": "Le nom d'hôte ne peut pas être vide",
    "empty-error": "{} ne peut pas être vide",  # Configuration
    "media-player-error": "Media player error: \"{}\"",  # Error line
    "unable-import-gui-error": "Impossible d'importer les bibliothèques GUI. Si vous n'avez pas installé PySide, vous devrez l'installer pour que l'interface graphique fonctionne. If you want to run Syncplay in console mode then run it with the --no-gui command line switch. See https://syncplay.pl/guide/ for more details.", # TODO: Translate end of message and update second sentence to be a translation of "You need to have the correct version of PySide installed for the GUI to work."
    "unable-import-twisted-error": "Impossible d'importer Twisted. Veuillez installer Twisted v16.4.0 ou une version ultérieure.",

    "arguments-missing-error": "Certains arguments nécessaires sont manquants, reportez-vous à --help",

    "unable-to-start-client-error": "Impossible de démarrer le client",

    "player-path-config-error": "Le chemin du lecteur n'est pas défini correctement. Les lecteurs pris en charge sont : mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2 et IINA.",
    "no-file-path-config-error": "Le fichier doit être sélectionné avant de démarrer votre lecteur",
    "no-hostname-config-error": "Le nom d'hôte ne peut pas être vide",
    "invalid-port-config-error": "Le port doit être valide",
    "empty-value-config-error": "{} ne peut pas être vide",  # Config option

    "not-json-error": "Pas une chaîne encodée en json",
    "hello-arguments-error": "Pas assez d'arguments pour Hello",  # DO NOT TRANSLATE
    "version-mismatch-error": "Non-concordance entre les versions du client et du serveur",
    "vlc-failed-connection": "Échec de la connexion à VLC. Si vous n'avez pas installé syncplay.lua et utilisez la dernière version de VLC, veuillez vous référer à https://syncplay.pl/LUA/ pour obtenir des instructions. Syncplay et VLC 4 ne sont actuellement pas compatibles, utilisez donc VLC 3 ou une alternative telle que mpv.",
    "vlc-failed-noscript": "VLC a signalé que le script d'interface syncplay.lua n'a pas été installé. Veuillez vous référer à https://syncplay.pl/LUA/ pour obtenir des instructions.",
    "vlc-failed-versioncheck": "Cette version de VLC n'est pas prise en charge par Syncplay.",
    "vlc-initial-warning": "VLC ne fournit pas toujours des informations de position précises à Syncplay, en particulier pour les fichiers .mp4 et .avi. Si vous rencontrez des problèmes de recherche erronée, essayez un autre lecteur multimédia tel que <a href=\"https://mpv.io/\">mpv</a> (ou <a href=\"https://github.com/stax76/mpv.net/\">mpv.net</a> pour les utilisateurs de Windows).",

    "feature-sharedPlaylists": "listes de lecture partagées",  # used for not-supported-by-server-error
    "feature-chat": "chat",  # used for not-supported-by-server-error
    "feature-readiness": "préparation",  # used for not-supported-by-server-error
    "feature-managedRooms": "salons gérés",  # used for not-supported-by-server-error
    "feature-setOthersReadiness": "readiness override",  # used for not-supported-by-server-error # TODO: Translate

    "not-supported-by-server-error": "La fonctionnalité {} n'est pas prise en charge par ce serveur.",  # feature
    "shared-playlists-not-supported-by-server-error": "La fonctionnalité de listes de lecture partagées peut ne pas être prise en charge par le serveur. Pour s'assurer qu'il fonctionne correctement, il faut un serveur exécutant Syncplay {}+, mais le serveur exécute Syncplay {}.",  # minVersion, serverVersion
    "shared-playlists-disabled-by-server-error": "La fonctionnalité de liste de lecture partagée a été désactivée dans la configuration du serveur. Pour utiliser cette fonctionnalité, vous devrez vous connecter à un autre serveur.",

    "invalid-seek-value": "Valeur de recherche non valide",
    "invalid-offset-value": "Valeur de décalage non valide",

    "switch-file-not-found-error": "Impossible de passer au fichier ''. Syncplay recherche dans les répertoires multimédias spécifiés.",  # File not found
    "folder-search-timeout-error": "La recherche de médias dans les répertoires de médias a été abandonnée car la recherche dans '{}' a pris trop de temps (after having processed the first {:,} files). Cela se produira si vous sélectionnez un dossier avec trop de sous-dossiers dans votre liste de dossiers multimédias à parcourir. Pour que le basculement automatique des fichiers fonctionne à nouveau, veuillez sélectionner Fichier->Définir les répertoires multimédias dans la barre de menu et supprimez ce répertoire ou remplacez-le par un sous-dossier approprié. Si le dossier est correct, vous pouvez le réactiver en sélectionnant Fichier->Définir les répertoires multimédias et en appuyant sur «OK».", # Folder, Files processed - Note: {:,} is {} but with added commas seprators - TODO: Translate
    "folder-search-timeout-warning": "Warning: It has taken {} seconds to scan {:,} files in the folder '{}'. This will occur if you select a folder with too many sub-folders in your list of media folders to search through or if there are too many files to process.",  # Folder, Files processed. Note: {:,} is {} but with added commas seprators. TODO: Translate
    "folder-search-first-file-timeout-error": "La recherche de média dans '{}' a été abandonnée car elle a pris trop de temps pour accéder au répertoire. Cela peut arriver s'il s'agit d'un lecteur réseau ou si vous configurez votre lecteur pour qu'il ralentisse après une période d'inactivité. Pour que le basculement automatique des fichiers fonctionne à nouveau, accédez à Fichier-> Définir les répertoires multimédias et supprimez le répertoire ou résolvez le problème (par exemple en modifiant les paramètres d'économie d'énergie).",  # Folder
    "added-file-not-in-media-directory-error": "Vous avez chargé un fichier dans '{}' qui n'est pas un répertoire média connu. Vous pouvez l'ajouter en tant que répertoire multimédia en sélectionnant Fichier->Définir les répertoires multimédias dans la barre de menus.",  # Folder
    "no-media-directories-error": "Aucun répertoire multimédia n'a été défini. Pour que les fonctionnalités de liste de lecture partagée et de changement de fichier fonctionnent correctement, sélectionnez Fichier-> Définir les répertoires multimédias et spécifiez où Syncplay doit rechercher les fichiers multimédias.",
    "cannot-find-directory-error": "Impossible de trouver le répertoire multimédia '{}'. Pour mettre à jour votre liste de répertoires multimédias, veuillez sélectionner Fichier->Définir les répertoires multimédias dans la barre de menu et spécifiez où Syncplay doit chercher pour trouver les fichiers multimédias.",

    "failed-to-load-server-list-error": "Échec du chargement de la liste des serveurs publics. Veuillez visiter https://www.syncplay.pl/ dans votre navigateur.",

    # Client arguments
    "argument-description": "Solution pour synchroniser la lecture de plusieurs instances de lecteur multimédia sur le réseau.",
    "argument-epilog": "Si aucune option n'est fournie, les valeurs _config seront utilisées",
    "nogui-argument": "masquer l'interface graphique",
    "host-argument": "adresse du serveur",
    "name-argument": "nom d'utilisateur souhaité",
    "debug-argument": "Mode débogage",
    "force-gui-prompt-argument": "faire apparaître l'invite de configuration",
    "no-store-argument": "ne pas stocker de valeurs dans .syncplay",
    "room-argument": "salon par défaut",
    "password-argument": "Mot de passe du serveur",
    "player-path-argument": "chemin d'accès à l'exécutable de votre lecteur",
    "file-argument": "fichier à lire",
    "args-argument": 'player options, if you need to pass options starting with - prepend them with single \'--\' argument',
    "clear-gui-data-argument": "réinitialise les données GUI du chemin et de l'état de la fenêtre stockées en tant que QSettings",
    "language-argument": "langue pour les messages Syncplay ({})", # Languages

    "version-argument": "imprime votre version",
    "version-message": "Vous utilisez Syncplay version {} ({})",

    "load-playlist-from-file-argument": "charge la liste de lecture à partir d'un fichier texte (une entrée par ligne)",


    # Client labels
    "config-window-title": "configuration Syncplay",

    "connection-group-title": "Paramètres de connexion",
    "host-label": "Adresse du serveur:",
    "name-label": "Nom d'utilisateur (facultatif):",
    "password-label": "Mot de passe du serveur (le cas échéant):",
    "room-label": "Salon par défaut:",
    "roomlist-msgbox-label": "Modifier la liste des salons (une par ligne)",

    "media-setting-title": "Paramètres du lecteur multimédia",
    "executable-path-label": "Chemin d'accès au lecteur multimédia:",
    "media-path-label": "Chemin d'accès à la vidéo (facultatif):",
    "player-arguments-label": "Arguments du joueur (le cas échéant):",
    "browse-label": "Parcourir",
    "update-server-list-label": "Mettre à jour la liste",

    "more-title": "Afficher plus de paramètres",
    "never-rewind-value": "Jamais",
    "seconds-suffix": "secs",
    "privacy-sendraw-option": "Envoyer brut",
    "privacy-sendhashed-option": "Envoyer haché",
    "privacy-dontsend-option": "Ne pas envoyer",
    "filename-privacy-label": "Informations sur le nom de fichier:",
    "filesize-privacy-label": "Informations sur la taille du fichier:",
    "checkforupdatesautomatically-label": "Rechercher automatiquement les mises à jour de Syncplay",
    "autosavejoinstolist-label": "Ajouter les salons que vous rejoignez à la liste des salons",
    "slowondesync-label": "Ralentissement en cas de désynchronisation mineure (non pris en charge sur MPC-HC/BE)",
    "rewindondesync-label": "Retour en arrière en cas de désynchronisation majeure (recommandé)",
    "fastforwardondesync-label": "Avance rapide en cas de retard (recommandé)",
    "dontslowdownwithme-label": "Ne jamais ralentir ou rembobiner les autres (expérimental)",
    "pausing-title": "Pause",
    "pauseonleave-label": "Pause lorsque l'utilisateur quitte (par exemple s'il est déconnecté)",
    "readiness-title": "État de préparation initial",
    "readyatstart-label": "Définissez-moi comme «prêt à regarder» par défaut",
    "forceguiprompt-label": "Ne pas toujours afficher la fenêtre de configuration Syncplay",  # (Inverted)
    "showosd-label": "Activer les Messages OSD",

    "showosdwarnings-label": "Inclure des avertissements (par exemple, lorsque les fichiers sont différents, les utilisateurs ne sont pas prêts)",
    "showsameroomosd-label": "Inclure des événements dans votre salon",
    "shownoncontrollerosd-label": "Inclure les événements des non-opérateurs dans les salons gérés",
    "showdifferentroomosd-label": "Inclure des événements dans d'autres salons",
    "showslowdownosd-label": "Inclure les notifications de ralentissement/annulation",
    "language-label": "Langue:",
    "automatic-language": "Défaut ({})",  # Default language
    "showdurationnotification-label": "Avertir des incohérences de durée de média",
    "basics-label": "Réglages de base",
    "readiness-label": "Jouer pause",
    "misc-label": "Divers",
    "core-behaviour-title": "Comportement du salon principal",
    "syncplay-internals-title": "procédures internes",
    "syncplay-mediasearchdirectories-title": "Répertoires pour rechercher des médias",
    "syncplay-mediasearchdirectories-label": "Répertoires pour rechercher des médias (un chemin par ligne)",
    "sync-label": "Synchroniser",
    "sync-otherslagging-title": "Si d'autres sont à la traîne...",
    "sync-youlaggging-title": "Si vous êtes à la traîne...",
    "messages-label": "Messages",
    "messages-osd-title": "Paramètres d'affichage à l'écran",
    "messages-other-title": "Autres paramètres d'affichage",
    "chat-label": "Chat",
    "privacy-label": "Sécurité données",  # Currently unused, but will be brought back if more space is needed in Misc tab
    "privacy-title": "Paramètres de confidentialité",
    "unpause-title": "Si vous appuyez sur play, définissez comme prêt et:",
    "unpause-ifalreadyready-option": "Annuler la pause si déjà défini comme prêt",
    "unpause-ifothersready-option": "Reprendre la pause si déjà prêt ou si d'autres personnes dans la pièce sont prêtes (par défaut)",
    "unpause-ifminusersready-option": "Annuler la pause si déjà prêt ou si tous les autres sont prêts et utilisateurs minimum prêts",
    "unpause-always": "Toujours reprendre",
    "syncplay-trusteddomains-title": "Domaines de confiance (pour les services de streaming et le contenu hébergé)",

    "chat-title": "Saisie du message de discussion",
    "chatinputenabled-label": "Activer la saisie de discussion via mpv",
    "chatdirectinput-label": "Autoriser la saisie de discussion instantanée (éviter d'avoir à appuyer sur la touche Entrée pour discuter)",
    "chatinputfont-label": "Police de caractères pour la saisie sur le Chat ",
    "chatfont-label": "Définir la fonte",
    "chatcolour-label": "Définir la couleur",
    "chatinputposition-label": "Position de la zone de saisie des messages dans mpv",
    "chat-top-option": "Haut",
    "chat-middle-option": "Milieu",
    "chat-bottom-option": "Bas",
    "chatoutputheader-label": "Sortie du message de discussion",
    "chatoutputfont-label": "Police de sortie du chat",
    "chatoutputenabled-label": "Activer la sortie du chat dans le lecteur multimédia (mpv uniquement pour l'instant)",
    "chatoutputposition-label": "Mode de sortie",
    "chat-chatroom-option": "Style de salon de discussion",
    "chat-scrolling-option": "Style de défilement",

    "mpv-key-tab-hint": "[TAB] pour basculer l'accès aux raccourcis des touches de la ligne alphabétique.",
    "mpv-key-hint": "[ENTER] pour envoyer un message. [ESC] pour quitter le mode chat.",
    "alphakey-mode-warning-first-line": "Vous pouvez temporairement utiliser les anciennes liaisons mpv avec les touches az.",
    "alphakey-mode-warning-second-line": "Appuyez sur [TAB] pour revenir au mode de discussion Syncplay.",

    "help-label": "Aider",
    "reset-label": "Réinitialiser",
    "run-label": "Exécuter Syncplay",
    "storeandrun-label": "Stocker la configuration et exécuter Syncplay",

    "contact-label": "Feel free to e-mail <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a>, <a href=\"https://github.com/Syncplay/syncplay/issues\"><nobr>create an issue</nobr></a> to report a bug/problem via GitHub, <a href=\"https://github.com/Syncplay/syncplay/discussions\"><nobr>start a discussion</nobr></a> to make a suggestion or ask a question via GitHub, <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>like us on Facebook</nobr></a>, <a href=\"https://twitter.com/Syncplay/\"><nobr>follow us on Twitter</nobr></a>, or visit <a href=\"https://syncplay.pl/\"><nobr>https://syncplay.pl/</nobr></a>. Do not use Syncplay to send sensitive information.",

    "joinroom-label": "Rejoindre la salle",
    "joinroom-menu-label": "Rejoindre la salle {}",
    "seektime-menu-label": "Chercher le temps",
    "undoseek-menu-label": "Annuler la recherche",
    "play-menu-label": "Jouer",
    "pause-menu-label": "Pause",
    "playbackbuttons-menu-label": "Afficher les boutons de lecture",
    "autoplay-menu-label": "Afficher le bouton de lecture automatique",
    "autoplay-guipushbuttonlabel": "Jouer quand tout est prêt",
    "autoplay-minimum-label": "Utilisateurs minimum:",
    "hideemptyrooms-menu-label": "Hide empty persistent rooms", # TODO: Translate

    "sendmessage-label": "Envoyer",

    "ready-guipushbuttonlabel": "Je suis prêt à regarder !",

    "roomuser-heading-label": "Salon / Utilisateur",
    "size-heading-label": "Taille",
    "duration-heading-label": "Durée",
    "filename-heading-label": "Nom de fichier",
    "notifications-heading-label": "Notifications",
    "userlist-heading-label": "Liste de qui joue quoi",

    "browseformedia-label": "Parcourir les fichiers multimédias",

    "file-menu-label": "&Fichier",  # & precedes shortcut key
    "openmedia-menu-label": "&Ouvrir le fichier multimédia",
    "openstreamurl-menu-label": "Ouvrir l'URL du &flux multimédia",
    "setmediadirectories-menu-label": "Définir les &répertoires multimédias",
    "loadplaylistfromfile-menu-label": "&Charger la liste de lecture à partir du fichier",
    "saveplaylisttofile-menu-label": "&Enregistrer la liste de lecture dans un fichier",
    "exit-menu-label": "Sortir",
    "advanced-menu-label": "&Avancée",
    "window-menu-label": "&Fenêtre",
    "setoffset-menu-label": "Définir &décalage",
    "createcontrolledroom-menu-label": "&Créer une salon à gérer",
    "identifyascontroller-menu-label": "&Identifier en tant qu'opérateur de salon",
    "settrusteddomains-menu-label": "Définir des &domaines de confiance",
    "addtrusteddomain-menu-label": "Ajouter {} comme domaine de confiance",  # Domain

    "edit-menu-label": "&Éditer",
    "cut-menu-label": "Couper",
    "copy-menu-label": "&Copier",
    "paste-menu-label": "&Coller",
    "selectall-menu-label": "&Tout sélectionner",

    "playback-menu-label": "&Relecture",

    "help-menu-label": "&Aide",
    "userguide-menu-label": "Ouvrir le &guide de l'utilisateur",
    "update-menu-label": "Rechercher et mettre à jour",

    "startTLS-initiated": "Tentative de connexion sécurisée",
    "startTLS-secure-connection-ok": "Connexion sécurisée établie ({})",
    "startTLS-server-certificate-invalid": "Échec de la Connexion Sécurisée. Le serveur utilise un certificat de sécurité non valide. Cette communication pourrait être interceptée par un tiers. Pour plus de détails et de dépannage, voir <a href=\"https://syncplay.pl/trouble\">ici</a> .",
    "startTLS-server-certificate-invalid-DNS-ID": "Syncplay ne fait pas confiance à ce serveur car il utilise un certificat qui n'est pas valide pour son nom d'hôte.",
    "startTLS-not-supported-client": "Ce client ne prend pas en charge TLS",
    "startTLS-not-supported-server": "Ce serveur ne prend pas en charge TLS",

    # TLS certificate dialog
    "tls-information-title": "Détails du certificat",
    "tls-dialog-status-label": "<strong>Syncplay utilise une connexion cryptée à {}.</strong>",
    "tls-dialog-desc-label": "Le cryptage avec un certificat numérique préserve la confidentialité des informations lorsqu'elles sont envoyées vers ou depuis le serveur {}.",
    "tls-dialog-connection-label": "Informations chiffrées à l'aide de Transport Layer Security (TLS), version {} avec la suite de chiffrement: {}.",
    "tls-dialog-certificate-label": "Certificat délivré par {} valable jusqu'au {}.",

    # About dialog
    "about-menu-label": "&À propos de la lecture synchronisée",
    "about-dialog-title": "À propos de Syncplay",
    "about-dialog-release": "Version {} release {}",
    "about-dialog-license-text": "Sous licence Apache, version 2.0",
    "about-dialog-license-button": "Licence",
    "about-dialog-dependencies": "Dépendances",

    "setoffset-msgbox-label": "Définir le décalage",
    "offsetinfo-msgbox-label": "Offset (voir https://syncplay.pl/guide/ pour les instructions d'utilisation):",

    "promptforstreamurl-msgbox-label": "Ouvrir l'URL du flux multimédia",
    "promptforstreamurlinfo-msgbox-label": "URL de diffusion",

    "addfolder-label": "Ajouter le dossier",

    "adduris-msgbox-label": "Ajouter des URL à la liste de lecture (une par ligne)",
    "editplaylist-msgbox-label": "Définir la liste de lecture (une par ligne)",
    "trusteddomains-msgbox-label": "Domaines vers lesquels vous pouvez basculer automatiquement (un par ligne)",

    "createcontrolledroom-msgbox-label": "Créer un salon à  gérer",
    "controlledroominfo-msgbox-label": "Enter name of managed room\r\n(see https://syncplay.pl/guide/ for usage instructions):",

    "identifyascontroller-msgbox-label": "S'identifier en tant qu'opérateur de salon",
    "identifyinfo-msgbox-label": "Enter operator password for this room\r\n(see https://syncplay.pl/guide/ for usage instructions):",

    "public-server-msgbox-label": "Sélectionnez le serveur public pour cette session de visualisation",

    "megabyte-suffix": "Mo",

    # Tooltips

    "host-tooltip": "Nom d'hôte ou IP auquel se connecter, incluant éventuellement le port (par exemple syncplay.pl:8999). Uniquement synchronisé avec des personnes sur le même serveur/port.",
    "name-tooltip": "Surnom sous lequel vous serez connu. Pas d'inscription, donc peut facilement changer plus tard. Nom aléatoire généré si aucun n'est spécifié.",
    "password-tooltip": "Les mots de passe ne sont nécessaires que pour se connecter à des serveurs privés.",
    "room-tooltip": "Le salon à rejoindre lors de la connexion peut être presque n'importe quoi, mais vous ne serez synchronisé qu'avec des personnes dans le même salon.",

    "edit-rooms-tooltip": "Modifier la liste des salons.",

    "executable-path-tooltip": "Emplacement du lecteur multimédia pris en charge que vous avez choisi (mpv, mpv.net, VLC, MPC-HC/BE, mplayer2 ou IINA).",
    "media-path-tooltip": "Emplacement de la vidéo ou du flux à ouvrir. Nécessaire pour mplayer2.",
    "player-arguments-tooltip": "Arguments/commutateurs de ligne de commande supplémentaires à transmettre à ce lecteur multimédia.",
    "mediasearcdirectories-arguments-tooltip": "Répertoires dans lesquels Syncplay recherchera les fichiers multimédias, par exemple lorsque vous utilisez la fonctionalité cliquer pour basculer. Syncplay recherchera récursivement dans les sous-dossiers.",

    "more-tooltip": "Afficher les paramètres moins fréquemment utilisés.",
    "filename-privacy-tooltip": "Mode de confidentialité pour l'envoi du nom de fichier en cours de lecture au serveur.",
    "filesize-privacy-tooltip": "Mode de confidentialité pour l'envoi de la taille du fichier en cours de lecture au serveur.",
    "privacy-sendraw-tooltip": "Envoyez ces informations sans brouillage. Il s'agit de l'option par défaut avec la plupart des fonctionnalités.",
    "privacy-sendhashed-tooltip": "Envoyez une version hachée des informations, les rendant moins visibles pour les autres clients.",
    "privacy-dontsend-tooltip": "N'envoyez pas ces informations au serveur. Cela garantit une confidentialité maximale.",
    "checkforupdatesautomatically-tooltip": "Vérifiez régulièrement sur le site Web de Syncplay si une nouvelle version de Syncplay est disponible.",
    "autosavejoinstolist-tooltip": "Lorsque vous rejoignez un salon sur un serveur, mémorisez automatiquement le nom de la salle dans la liste des salons à rejoindre.",
    "slowondesync-tooltip": "Réduisez temporairement le taux de lecture si nécessaire pour vous synchroniser avec les autres téléspectateurs. Non pris en charge sur MPC-HC/BE.",
    "dontslowdownwithme-tooltip": "Cela signifie que les autres ne sont pas ralentis ou rembobinés si votre lecture est en retard. Utile pour les opérateurs de salon.",
    "pauseonleave-tooltip": "Mettez la lecture en pause si vous êtes déconnecté ou si quelqu'un quitte votre salon.",
    "readyatstart-tooltip": "Définissez-vous comme «prêt» au début (sinon, vous êtes défini comme «pas prêt» jusqu'à ce que vous changiez votre état de préparation)",
    "forceguiprompt-tooltip": "La boîte de dialogue de configuration ne s'affiche pas lors de l'ouverture d'un fichier avec Syncplay.",  # (Inverted)
    "nostore-tooltip": "Exécutez Syncplay avec la configuration donnée, mais ne stockez pas les modifications de manière permanente.",  # (Inverted)
    "rewindondesync-tooltip": "Revenez en arrière au besoin pour vous synchroniser. La désactivation de cette option peut entraîner des désynchronisations majeures!",
    "fastforwardondesync-tooltip": "Avancez en cas de désynchronisation avec l'opérateur de la salle (ou votre position factice si l'option «Ne jamais ralentir ou rembobiner les autres» est activée).",
    "showosd-tooltip": "Envoie des messages Syncplay à l'OSD du lecteur multimédia.",
    "showosdwarnings-tooltip": "Afficher des avertissements en cas de lecture d'un fichier différent, seul dans la pièce, utilisateurs non prêts, etc.",
    "showsameroomosd-tooltip": "Afficher les notifications OSD pour les événements liés à l'utilisateur du salon.",
    "shownoncontrollerosd-tooltip": "Afficher les notifications OSD pour les événements relatifs aux non-opérateurs qui se trouvent dans les salles gérées.",
    "showdifferentroomosd-tooltip": "Afficher les notifications OSD pour les événements liés à l'absence de l'utilisateur du salon.",
    "showslowdownosd-tooltip": "Afficher les notifications de ralentissement / de retour au décalage temps.",
    "showdurationnotification-tooltip": "Utile lorsqu'un segment dans un fichier en plusieurs parties est manquant, mais peut entraîner des faux positifs.",
    "language-tooltip": "Langue à utiliser par Syncplay.",
    "unpause-always-tooltip": "Si vous appuyez sur unpause, cela vous définit toujours comme prêt et non-pause, plutôt que de simplement vous définir comme prêt.",
    "unpause-ifalreadyready-tooltip": "Si vous appuyez sur unpause lorsque vous n'êtes pas prêt, cela vous mettra comme prêt - appuyez à nouveau sur unpause pour reprendre la pause.",
    "unpause-ifothersready-tooltip": "Si vous appuyez sur unpause lorsque vous n'êtes pas prêt, il ne reprendra la pause que si d'autres sont prêts.",
    "unpause-ifminusersready-tooltip": "Si vous appuyez sur annuler la pause lorsqu'il n'est pas prêt, il ne s'arrêtera que si d'autres personnes sont prêtes et que le seuil minimal d'utilisateurs est atteint.",
    "trusteddomains-arguments-tooltip": "Domaines vers lesquels Syncplay peut basculer automatiquement lorsque les listes de lecture partagées sont activées.",

    "chatinputenabled-tooltip": "Activer la saisie du chat dans mpv (appuyez sur Entrée pour discuter, Entrée pour envoyer, Échap pour annuler)",
    "chatdirectinput-tooltip": "Évitez d'avoir à appuyer sur «enter» pour passer en mode de saisie de discussion dans mpv. Appuyez sur TAB dans mpv pour désactiver temporairement cette fonctionnalité.",
    "font-label-tooltip": "Police utilisée lors de la saisie de messages de discussion dans mpv. Côté client uniquement, n'affecte donc pas ce que les autres voient.",
    "set-input-font-tooltip": "Famille de polices utilisée lors de la saisie de messages de discussion dans mpv. Côté client uniquement, n'affecte donc pas ce que les autres voient.",
    "set-input-colour-tooltip": "Couleur de police utilisée lors de la saisie de messages de discussion dans mpv. Côté client uniquement, n'affecte donc pas ce que les autres voient.",
    "chatinputposition-tooltip": "Emplacement dans mpv où le texte d'entrée de discussion apparaîtra lorsque vous appuyez sur Entrée et tapez.",
    "chatinputposition-top-tooltip": "Placez l'entrée de discussion en haut de la fenêtre mpv.",
    "chatinputposition-middle-tooltip": "Placez l'entrée de discussion au point mort de la fenêtre mpv.",
    "chatinputposition-bottom-tooltip": "Placez l'entrée de discussion en bas de la fenêtre mpv.",
    "chatoutputenabled-tooltip": "Afficher les messages de discussion dans l'OSD (si pris en charge par le lecteur multimédia).",
    "font-output-label-tooltip": "Police de sortie du chat.",
    "set-output-font-tooltip": "Police utilisée pour l'affichage des messages de discussion.",
    "chatoutputmode-tooltip": "Comment les messages de chat sont affichés.",
    "chatoutputmode-chatroom-tooltip": "Affichez les nouvelles lignes de discussion directement sous la ligne précédente.",
    "chatoutputmode-scrolling-tooltip": "Faites défiler le texte du chat de droite à gauche.",

    "help-tooltip": "Ouvre le guide de l'utilisateur de Syncplay.pl.",
    "reset-tooltip": "Réinitialisez tous les paramètres à la configuration par défaut.",
    "update-server-list-tooltip": "Connectez-vous à syncplay.pl pour mettre à jour la liste des serveurs publics.",

    "sslconnection-tooltip": "Connecté en toute sécurité au serveur. Cliquez pour obtenir les détails du certificat.",

    "joinroom-tooltip": "Quitter la salle actuelle et rejoindre le salon spécifié.",
    "seektime-msgbox-label": "Aller au temps spécifié (en secondes / min:sec). Utilisez +/- pour la recherche relative.",
    "ready-tooltip": "Indique si vous êtes prêt à regarder.",
    "autoplay-tooltip": "Lecture automatique lorsque tous les utilisateurs qui ont un indicateur de disponibilité sont prêts et que le seuil d'utilisateur minimum est atteint.",
    "switch-to-file-tooltip": "Double-cliquez pour passer à {}",  # Filename
    "sendmessage-tooltip": "Envoyer un message au salon",

    # In-userlist notes (GUI)
    "differentsize-note": "Différentes tailles!",
    "differentsizeandduration-note": "Taille et durée différentes !",
    "differentduration-note": "Durée différente !",
    "nofile-note": "(Aucun fichier en cours de lecture)",

    # Server messages to client
    "new-syncplay-available-motd-message": "Vous utilisez Syncplay {} mais une version plus récente est disponible sur https://syncplay.pl",  # ClientVersion
    "persistent-rooms-notice": "NOTICE: This server uses persistent rooms, which means that the playlist information is stored between playback sessions. If you want to create a room where information is not saved then put -temp at the end of the room name.", # NOTE: Do not translate the word -temp # TODO: Translate
    "ready-chat-message": "I have set {} as ready.",  # User # TODO: Translate
    "not-ready-chat-message": "I have set {} as not ready.",  # User # TODO: Translate

    # Server notifications
    "welcome-server-notification": "Bienvenue sur le serveur Syncplay, ver.",  # version
    "client-connected-room-server-notification": "({2}) connecté à la salle '{1}'",  # username, host, room
    "client-left-server-notification": "a quitté le serveur",  # name
    "no-salt-notification": "VEUILLEZ NOTER: Pour permettre aux mots de passe d'opérateur de salle générés par cette instance de serveur de fonctionner lorsque le serveur est redémarré, veuillez ajouter l'argument de ligne de commande suivant lors de l'exécution du serveur Syncplay à l'avenir: --salt {}",  # Salt


    # Server arguments
    "server-argument-description": "Solution pour synchroniser la lecture de plusieurs instances de lecteur multimédia sur le réseau. Instance de serveur",
    "server-argument-epilog": "Si aucune option n'est fournie, les valeurs _config seront utilisées",
    "server-port-argument": "port TCP du serveur",
    "server-password-argument": "Mot de passe du serveur",
    "server-isolate-room-argument": "faut-il isoler les salons ?",
    "server-salt-argument": "chaîne aléatoire utilisée pour générer les mots de passe des salons gérés",
    "server-disable-ready-argument": "désactiver la fonction de préparation",
    "server-motd-argument": "chemin vers le fichier à partir duquel motd sera récupéré",
    "server-rooms-argument": "path to database file to use and/or create to store persistent room data. Enables rooms to persist without watchers and through restarts", # TODO: Translate
    "server-permanent-rooms-argument": "path to file which lists permenant rooms that will be listed even if the room is empty (in the form of a text file which lists one room per line) - requires persistent rooms to be enabled", # TODO: Translate
    "server-chat-argument": "Le chat doit-il être désactivé?",
    "server-chat-maxchars-argument": "Nombre maximum de caractères dans un message de discussion (la valeur par défaut est {})", # Default number of characters
    "server-maxusernamelength-argument": "Nombre maximum de caractères dans un nom d'utilisateur (la valeur par défaut est {})",
    "server-stats-db-file-argument": "Activer les statistiques du serveur à l'aide du fichier db SQLite fourni",
    "server-startTLS-argument": "Activer les connexions TLS à l'aide des fichiers de certificat dans le chemin fourni",
    "server-messed-up-motd-unescaped-placeholders": "Le message du jour a des espaces réservés non échappés. Tous les signes $ doivent être doublés ($$).",
    "server-messed-up-motd-too-long": "Le message du jour est trop long: {}caractères maximum, {} donnés.",
    "server-listen-only-on-ipv4": "Listen only on IPv4 when starting the server.",
    "server-listen-only-on-ipv6": "Listen only on IPv6 when starting the server.",
    "server-interface-ipv4": "The IP address to bind to for IPv4. Leaving it empty defaults to using all.",
    "server-interface-ipv6": "The IP address to bind to for IPv6. Leaving it empty defaults to using all.",

    # Server errors
    "unknown-command-server-error": "Commande inconnue {}",  # message
    "not-json-server-error": "Pas une chaîne encodée json {}",  # message
    "line-decode-server-error": "Pas une chaîne utf-8",
    "not-known-server-error": "Vous devez être connu du serveur avant d'envoyer cette commande",
    "client-drop-server-error": "Client drop: {} -- {}",  # host, error
    "password-required-server-error": "Mot de passe requis",
    "wrong-password-server-error": "Mauvais mot de passe fourni",
    "hello-server-error": "Pas assez d'arguments pour Hello",  # DO NOT TRANSLATE

    # Playlists
    "playlist-selection-changed-notification": "{} a modifié la sélection de la liste de lecture",  # Username
    "playlist-contents-changed-notification": "{} a mis à jour la liste de lecture",  # Username
    "cannot-find-file-for-playlist-switch-error": "Impossible de trouver le fichier {} dans les répertoires multimédias pour le changement de liste de lecture!",  # Filename
    "cannot-add-duplicate-error": "Impossible d'ajouter la deuxième entrée pour '{}' à la liste de lecture car aucun doublon n'est autorisé.",  # Filename
    "cannot-add-unsafe-path-error": "Impossible de charger automatiquement {}, car il ne se trouve pas sur un domaine approuvé. Vous pouvez basculer manuellement vers l'URL en double-cliquant dessus dans la liste de lecture et ajouter des domaines de confiance via Fichier->Avancé->Définir les domaines de confiance. Si vous faites un clic droit sur une URL, vous pouvez ajouter son domaine en tant que domaine de confiance via le menu contextuel.",  # Filename
    "sharedplaylistenabled-label": "Activer les listes de lecture partagées",
    "removefromplaylist-menu-label": "Supprimer de la liste de lecture",
    "shuffleremainingplaylist-menu-label": "Mélanger la liste de lecture restante",
    "shuffleentireplaylist-menu-label": "Mélanger toute la liste de lecture",
    "undoplaylist-menu-label": "Annuler la dernière modification de la liste de lecture",
    "addfilestoplaylist-menu-label": "Ajouter des fichiers au bas de la liste de lecture",
    "addurlstoplaylist-menu-label": "Ajouter des URL au bas de la liste de lecture",
    "editplaylist-menu-label": "Modifier la liste de lecture",

    "open-containing-folder": "Ouvrir le dossier contenant ce fichier",
    "addyourfiletoplaylist-menu-label": "Ajoutez votre fichier à la liste de lecture",
    "addotherusersfiletoplaylist-menu-label": "Ajouter le fichier de {} à la liste de lecture",  # [Username]
    "addyourstreamstoplaylist-menu-label": "Ajoutez votre flux à la liste de lecture",
    "addotherusersstreamstoplaylist-menu-label": "Ajouter {}' stream à la playlist",  # [Username]
    "openusersstream-menu-label": "Ouvrir le flux de {}",  # [username]'s
    "openusersfile-menu-label": "Ouvrir le fichier de {}",  # [username]'s

    "setasready-menu-label": "Set {} as ready",  # [Username] # TODO: Translate
    "setasnotready-menu-label": "Set {} as not ready",  # [Username] # TODO: Translate

    "playlist-instruction-item-message": "Faites glisser le fichier ici pour l'ajouter à la liste de lecture partagée.",
    "sharedplaylistenabled-tooltip": "Les opérateurs de salle peuvent ajouter des fichiers à une liste de lecture synchronisée pour permettre à tout le monde de regarder facilement la même chose. Configurez les répertoires multimédias sous «Divers».",

    "playlist-empty-error": "La liste de lecture est actuellement vide.",
    "playlist-invalid-index-error": "Index de liste de lecture non valide",
}
