# coding:utf8

"""Finnish dictionary"""

# Filename, dictionary name and LANGUAGE-TAG value based on ISO country code. Language tag listed at https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/a9eac961-e77d-41a6-90a5-ce1a8b0cdb9c?redirectedfrom=MSDN

fi = {
     "LANGUAGE": "Finnish",
     "LANGUAGE-TAG": "fi",

     # Strings for Windows NSIS installer
     "installer-language-file": "Finnish.nlf", # Relevant .nlf file at https://github.com/kichik/nsis/tree/master/Contrib/Language%20files
     "installer-associate": "Aseta Syncplay avaamaan multimedia-tiedostoja.",
     "installer-shortcut": "Luo pikakuvakkeet seuraaviin kohteisiin:",
     "installer-start-menu": "Käynnistä-valikko",
     "installer-desktop": "Työpöytä",
     "installer-quick-launch-bar": "Pikakäynnistyspalkki",
     "installer-automatic-updates": "Tarkista päivitykset automaattisesti",
     "installer-uninstall-configuration": "Poista asetustiedosto.",

     # Client notifications
     "config-cleared-notification": "Asetukset pyyhitty. Muutokset muistetaan tallentaessa kelvolliset asetukset.",

     "relative-config-notification": "Ladattiin hakemiston asetustiedosto(t): {}",

     "connection-attempt-notification": "Yritetään yhdistää kohteeseen {}:{}",  # Port, IP
     "reconnection-attempt-notification": "Yhteys palvelimeen menetettiin, yritetään uudelleenyhdistämistä",
     "disconnection-notification": "Yhteys palvelimeen katkaistu",
     "connection-failed-notification": "Palvelimeen yhdistäminen epäonnistui",
     "connected-successful-notification": "Yhteys muodostettu palvelimeen onnistuneesti",
     "retrying-notification": "%s, Yritetetään uudelleen %d sekunnissa...",  # Seconds
     "reachout-successful-notification": "Tavoitettu onnistuneesti {} ({})",

     "rewind-notification": "Kelattiin taaksepäin käyttäjän {} aikaeron vuoksi",  # User
     "fastforward-notification": "Pikakelattiin käyttäjän {} aikaeron vuoksi",  # User
     "slowdown-notification": "Hidastetaan toistoa käyttäjän {} aikaeron vuoksi",  # User
     "revert-notification": "Palautetaan toistonopeus normaaliksi",

     "pause-notification": "{} tauotti kohdassa {}",  # User, Time
     "unpause-notification": "{} jatkoi toistoa",  # User
     "seek-notification": "{} hyppäsi kohdasta {} kohtaan {}",  # User, from time, to time

     "current-offset-notification": "Nykyinen aikaero: {} sekuntia",  # Offset

     "media-directory-list-updated-notification": "Syncplay:n mediahakemistot on päivitetty.",

     "room-join-notification": "{} liittyi huoneeseen: '{}'",  # User
     "left-notification": "{} poistui",  # User
     "left-paused-notification": "{} poistui, {} tauotti",  # User who left, User who paused
     "playing-notification": "{} toistaa '{}' ({})",  # User, file, duration
     "playing-notification/room-addendum": " huoneessa: '{}'",  # Room

     "not-all-ready": "Ei valmiina: {}",  # Usernames
     "all-users-ready": "Kaikki ovat valmiita ({} käyttäjää)",  # Number of ready users
     "ready-to-unpause-notification": "Asetit itsesi nyt valmiiksi - paina taukoa uudelleen päättääksesi tauon",
     "set-as-ready-notification": "Asetit itsesi valmiiksi",
     "set-as-not-ready-notification": "Ilmaisit ettet ole vielä valmis",
     "autoplaying-notification": "Automaattinen toisto alkaa {}...",  # Number of seconds until playback will start

     "identifying-as-controller-notification": "Tunnistaudutaan huoneen operaattoriksi salasanalla '{}'...",
     "failed-to-identify-as-controller-notification": "{} huoneen operaattoriksi tunnistautuminen epäonnistui.",
     "authenticated-as-controller-notification": "{} tunnistautui huoneen operaattoriksi",
     "created-controlled-room-notification": "Luotiin hallittu huone '{}' salasanalla '{}'. Kirjoita tämä talteen tulevaisuudessa löydettäväksi!\n\nHallinnoiduissa huoneissa kaikkien osallistujien kohdat pidetään synkronoituneena huoneen operaattori(e)n kanssa ja vain he voivat tauottaa, jatkaa tai kelata ja muuttaa soittolistaa.\n\nSinun tulisi pyytää vakiokatsojia liittymään huoneeseen '{}' huoneen operaattorit taas voivat liittyä huoneeseen '{}' tunnistautuakseen automaattisesti.",  # RoomName, operatorPassword, roomName, roomName:operatorPassword

    "other-set-as-ready-notification": "{} was set as ready by {}", # User set as ready, user who set them as ready # TODO: Translate
    "other-set-as-not-ready-notification": "{} was set as not ready by {}", # User set as not ready, user who set them as not ready # TODO: Translate

     "file-different-notification": "Vaikutat toistavan eri tiedostoa verrattuna käyttäjään {}",  # User
     "file-differences-notification": "Tiedostosi poikkeaa seuraavasti: {}",  # Differences
     "room-file-differences": "Tiedostoerot: {}",  # File differences (filename, size, and/or duration)
     "file-difference-filename": "nimi",
     "file-difference-filesize": "koko",
     "file-difference-duration": "kesto",
     "alone-in-the-room": "Olet huoneessa yksin",

     "different-filesize-notification": " (hänen tiedostokokonsa poikkeaa omastasi!)",
     "userlist-playing-notification": "{} toistaa:",  # Username
     "file-played-by-notification": "Toistetaan tiedostoa {}",  # File
     "no-file-played-notification": "{} ei toista mitään tiedostoa",  # Username
     "notplaying-notification": "Käyttäjät, jotka eivät toista mitään:",
     "userlist-room-notification":  "Huoneessa '{}':",  # Room
     "userlist-file-notification": "Tiedosto",
     "controller-userlist-userflag": "Operaattori",
     "ready-userlist-userflag": "Valmiina",

     "update-check-failed-notification": "Syncplay {} ajantasaisuutta ei voitu tarkistaa. Haluatko vierailla osoitteessa https://syncplay.pl/ tarkistaaksesi päivitykset käsin?",  # Syncplay version
     "syncplay-uptodate-notification": "Syncplay on ajantasalla",
     "syncplay-updateavailable-notification": "Syncplayn uusi versio on saatavilla. Haluatko vierailla julkaisusivulla?",

     "mplayer-file-required-notification": "Käytettäessä Mplayer-sovellusta Syncplay vaatii tiedostonimen käynnistettäessä",
     "mplayer-file-required-notification/example": "Käyttöesimerkki: syncplay [argumentit] [osoite|polku/]tiedostonimi",
     "mplayer2-required": "Syncplay ei ole yhteensopiva MPlayer version 1.x kanssa, käytä mplayer2:ta mpv:tä",

     "unrecognized-command-notification": "Tuntematon komento",
     "commandlist-notification": "Käytettävissä olevat komennot:",
     "commandlist-notification/room": "\tr [nimi] - siirry huoneeseen",
     "commandlist-notification/list": "\tl - näytä käyttäjäluettelo",
     "commandlist-notification/undo": "\tu - peru edellinen kohtahaku",
     "commandlist-notification/pause": "\tp - tauota tai päätä tauko",
     "commandlist-notification/seek": "\t[s][+-]kohta - siirry annettuun kohtaan, mikäli + tai - ei ole määritetty, kyseessä on absoluuttinen kohta sekunneissa tai min:sek",
     "commandlist-notification/offset": "\to[+-]kesto - tee aikaero palvelimeen paikallisesti keston verran - tämä ominaisuus on deprekoitu",
     "commandlist-notification/help": "\th - tämä ohje",
     "commandlist-notification/toggle": "\tt - määrittää oletko valmis aloittamaan katselun vaiko et",
    "commandlist-notification/setready": "\tsr [name] - sets user as ready",  # TODO: Translate
    "commandlist-notification/setnotready": "\tsn [name] - sets user as not ready",  # TODO: Translate
     "commandlist-notification/create": "\tc [nimi] - tee tästä huoneesta hallittu",
     "commandlist-notification/auth": "\ta [salasana] - tunnistaudu operaattoriksi salasanalla",
     "commandlist-notification/chat": "\tch [viesti] - lähetä viesti huoneeseen",
     "commandList-notification/queue": "\tqa [tiedosto/osoite] - lisää tiedosto tai osoite soittolistan loppuun",
     "commandList-notification/queueandselect": "\tqas [tiedosto/osoite] - lisää tiedosto tai osoite soittolistan loppuun, sekä valitse se",
     "commandList-notification/playlist": "\tql - näytä nykyinen soittolista",
     "commandList-notification/select": "\tqs [sisällys] - valitse kohde soittolistassa",
     "commandList-notification/next": "\tqn - valitse toistolistalla seuraava kohde",
     "commandList-notification/delete": "\tqd [sisällys] - poista valittu kohde soittolistalta",
     "syncplay-version-notification": "Syncplayn versio: {}",  # syncplay.version
     "more-info-notification": "Lisätietoja osoitteessa: {}",  # projectURL

     "gui-data-cleared-notification": "Syncplay on tyhjentänyt käyttöliittymän polun ja ikkunan tiedot.",
     "language-changed-msgbox-label": "Kieli vaihdetaan Syncplayn uudelleenkäynnistyksen yhteydessä.",
     "promptforupdate-label": "Sallitko Syncplayn tarkistavan päivitykset automaattisesti ajoittain?",

     "media-player-latency-warning": "Varoitus: mediasoittimelta kesti {} sekuntia vastata. Mikäli kohtaat synkronointi-ongelmia, sulje muita sovelluksia vapauttaaksesi järjestelmäresursseja, ja mikäli se ei auta, kokeile toista mediasoitinta.",  # Seconds to respond
     "mpv-unresponsive-error": "mpv ei ole vastannut {} sekuntiin, joten se vaikuttaa toimineen virheellisesti. Käynnistä Syncplay uudelleen.",  # Seconds to respond

     # Client prompts
     "enter-to-exit-prompt": "Paina rivinvaihtonäppäintä (Enter) poistuaksesi\n",

     # Client errors
     "missing-arguments-error": "Joitakin vaadittuja argumentteja uupuu, katso --help",
     "server-timeout-error": "Aikakatkaisu yhdistäessä palvelimeen",
     "mpc-slave-error": "MPC:tä ei voitu käynnistää slave-tilassa!",
     "mpc-version-insufficient-error": "MPC-versio ei ole riittävä, käytä `mpc-hc` >= `{}`",
     "mpc-be-version-insufficient-error": "MPC-versio ei riittävä, käytä `mpc-be` >= `{}`",
     "mpv-version-error": "Syncplay ei ole yhteensopiva tämän mpv-soittimen version kanssa. Käytäthän mpv:n uudempaa julkaisua jotta saat toiston käyntiin(esim. Git HEAD).",
     "mpv-failed-advice": "Syy miksi mpv ei voi käynnistyä voi johtua tukemattomista komentorivin vivuista tai sitten mpv:n versiosta jota ei tueta.",
     "player-file-open-error": "Toistin ei saanut tiedostoa auki",
     "player-path-error": "Toistimen tiedostopolku ei ole oikein asetettu. Tuettuja toisto-ohjelmia ovat: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2, ja IINA",
     "hostname-empty-error": "Palvelinnimi ei voi olla tyhjä",
     "empty-error": "{} ei voi jättää tyhjäksi",  # Configuration
     "media-player-error": "Mediasoitin kohtasi virheen: \"{}\"",  # Error line
     "unable-import-gui-error": "Käyttöliittymäkirjastoja ei saatu tuotua. Mikäli sinulla ei ole PySide asennettuna, tulee sinun asentaa se jotta käyttöliittymä toimisi. If you want to run Syncplay in console mode then run it with the --no-gui command line switch. See https://syncplay.pl/guide/ for more details.", # TODO: Translate end of message and update second sentence to be a translation of "You need to have the correct version of PySide installed for the GUI to work."
     "unable-import-twisted-error": "Twisted:iä ei onnistuttu tuomaan. Asenna Twisted v16.4.0 tai myöhäisempi.",

     "arguments-missing-error": "Joitakin vipuja uupuu, katso apua --help",

     "unable-to-start-client-error": "Asiakasohjelmaa ei saatu käynnistettyä",

     "player-path-config-error": "Toistimen sijaintipolku ei ole asetettu oikein. Tuetut toisto-ohjelmat ovat: mpv, mpv.net, VLC, MPC-HC, MPC-BE, mplayer2, ja IINA.",
     "no-file-path-config-error": "Tiedosto pitää valita ennen soittimesi käynnistämistä",
     "no-hostname-config-error": "Palvellinnimi ei voi olla tyhjä",
     "invalid-port-config-error": "Portti tulee olla kelvollinen",
     "empty-value-config-error": "{} ei voi olla tyhjä",  # Config option

     "not-json-error": "Tämä ei ole json-enkoodattu lanka\n",
     "hello-arguments-error": "Not enough Hello arguments\n",  # DO NOT TRANSLATE
     "version-mismatch-error": "Yhteensopimattomuusongelma asiakasohjelman ja palvelimen välillä\n",
     "vlc-failed-connection": "VLC:hen ei saatu yhteyttä. Mikäli et ole asentanut osasta syncplay.lua ja käytät VLC:n tuoreinta julkaisua, katso lisäapua täältä https://syncplay.pl/LUA/ jotta asia ratkeaa. Syncplay ja VLC 4 eivät tällä hetkellä ole yhteensopivia, joten käytä joko VLC 3:a tai vaihtoehtoista toistinta kuten mpv.",
     "vlc-failed-noscript": "VLC ilmoitti että syncplay.lua -liitymää ei ole asennettu. Katsothan https://syncplay.pl/LUA/ saadaksesi lisätietoja.",
     "vlc-failed-versioncheck": "Tämä VLC:n julkaisu ei ole Syncplayn tukema.",
     "vlc-initial-warning": 'VLC ei aina tarjoa aivan tarkkaa toistojanan sijaintitietoa Syncplaylle, erityisesti .mp4 ja .avi tiedostojen kanssa on epätarkkuuksia. Jos kohtaat ongelmia virheellisen kohtahaun suhteen, kokeile vaihtoehtoista mediantoisto-ohjelmaa kuten <a href="https://mpv.io/">mpv</a> (or <a href="https://github.com/stax76/mpv.net/">mpv.net</a> jos olet Windows-käyttäjä).',

     "feature-sharedPlaylists": "jaetut soittoluettelot",  # used for not-supported-by-server-error
     "feature-chat": "keskustelu",  # used for not-supported-by-server-error
     "feature-readiness": "valmius",  # used for not-supported-by-server-error
     "feature-managedRooms": "hallinnoidut huoneet",  # used for not-supported-by-server-error
     "feature-setOthersReadiness": "readiness override",  # used for not-supported-by-server-error # TODO: Translate

     "not-supported-by-server-error": "Tämä {} ominaisuus ei ole tämän palvelimen tukema..",  # feature
     "shared-playlists-not-supported-by-server-error": "Jaetut toistoluettelot eivät välttämättä ole palvelimen tukemia. Varmistaaksesi että kaikki toimii oikein vaaditaan palvelin jossa ajetaan Syncplaytä  {}+, mutta palvelin ajaa Syncplayn versiota {}.",  # minVersion, serverVersion
     "shared-playlists-disabled-by-server-error": "Jaettujen toistoluettelojen ominaisuus on kytketty pois päältä palvelimen asetuksista. Käyttääksesi tätä ominaisuutta sinun tulee yhdistää eri palvelimelle.",

     "invalid-seek-value": "Epäkelp hakuarvo",
     "invalid-offset-value": "Epäkelpo poikkeama-arvo",

     "switch-file-not-found-error": "Ei onnistuttu vaihtamaan tiedostoon '{0}'. Syncplay katsoo määritettyjen mediahakemistojen läpi.",  # File not found
     "folder-search-timeout-error": "Haku median löytämiseksi mediahakemistoista keskeytettiin koska se alkoi viedä liiaksi aikaa käydä läpi '{}'. Tätä ilmenee jos valitset kansion jossa on liikaa alikansioita määritellyn hakemistopolun tiimoilla. Jotta automaattinen tiedostovaihtaminen toimisi jälleen valitse Tiedosto->Aseta mediahakemistot valikkopalkissa ja poista tämä nykyinen hakemisto tai vaihda se sopivaan alikansioon. Mikäli kansio on itseasiassa kelvollinen, täten voit uudelleenvalita sen käyttöön valiten Tiedosto->Aseta mediahakemistot ja kun napsautat 'OK'.",  # Folder
     "folder-search-first-file-timeout-error": "Haku mediaa etsien kohteessa '{}' keskeytettiin koska aikaa kului liian paljon hakemistoon pääsemiseksikään. Tätä voi ilmetä jos kyseessä on verkkoasema tai jos olet määrttänyt aseman sammuttamaan lukutoiminnan tietyn joutilasajan jälkeen. Jotta saat automaattisen tiedostovaihdon jälleen toimimaan mene Tiedosto->Aseta mediakansiotSet Media Directories ja joko poista hakemisto tai ratkaise ongelma (esim. muuttamalla virransäästön asetusta).",  # Folder
     "added-file-not-in-media-directory-error": "Lataus tapahtui ajassa '{}' mutta kyseessä ei ole tunnettu mediakansio. Voit lisätä tämän mediahakemistoksi valiten Tiedosto->Aseta mediahakemistot valikkopalkissa.",  # Folder
     "no-media-directories-error": "Mediahakemistoja ei ole asetettu. Jotta jaetut toistoluettelot ja tiedostovaihdot toimisivat valitse Tiedosto->Aseta mediahakemistot ja määritä mistä Syncplay hakee mediatiedostoja.",
     "cannot-find-directory-error": "Mediahakemistoa '{}' ei löytynyt. Päivittääksesi mediahakemistojesi luettelon valitse Tiedosto->Aseta mediahakemistot valikkopalkista ja määritä mistä Syncplay sitten hakee löytääkseen mediatiedostoja.",

     "failed-to-load-server-list-error": "Julkista palvelinluetteloa ei saatu ladattua. Käy osoitteessa https://www.syncplay.pl/ selaimellasi.",

     # Client arguments
     "argument-description": 'Ratkaisu yhdentää toisto useiden mediantoisto-ohjelmien kesken verkon yli.',
     "argument-epilog": 'Mikäli vaihtoehtoja ei määritetä käytetään _config arvoja',
     "nogui-argument": 'älä näytä käyttöliittymää',
     "host-argument": "palvelimen osoite",
     "name-argument": 'toivottu käyttäjänimi',
     "debug-argument": 'virheenmäärityksen tila',
     "force-gui-prompt-argument": 'aseta asetusilmoite näkyväksi',
     "no-store-argument": "älä säilytä arvoja tiedostossa .syncplay",
     "room-argument": 'vakiohuone',
     "password-argument": 'palvelimen salasana',
     "player-path-argument": 'tiedostopolku toistimen ajettavaan tiedostoon',
     "file-argument": 'tiedosto toistettavaksi',
     "args-argument": 'toisto-ohjelman vaihtoehdot, mikäli tarvitset käyttöön kytkentöjä alkaen - alkuun lisäämiseski yhdellä \'--\' argumentilla',
     "clear-gui-data-argument": 'nollaa tiedostopolun ja ikkunoinnin käyttöliittymätilan joka on taltiotuna kohteeseen QSettings',
     "language-argument": 'kieli Syncplayn viesteille ({})', # Languages

     "version-argument": 'näyttää versiosi',
     "version-message": "Käytät Syncplayn versiota {} ({})",

     "load-playlist-from-file-argument": "lataa toistoluettelon tekstitiedostosta (yksi syöte aina riviä kohti)",


     # Client labels
     "config-window-title": "Syncplayn asetukset",

     "connection-group-title": "Yhteysasetukset",
     "host-label": "Palvelinosoite: ",
     "name-label":  "Käyttäjänimi (valinnainen):",
     "password-label":  "Palvelimen salasana (ei välttämättä mitään):",
     "room-label": "Vakiohuone: ",
     "roomlist-msgbox-label": "Muokkaa huoneluetteloa (yksi aina riviä kohti)",

     "media-setting-title": "Mediatoisto-ohjelman asetukset",
     "executable-path-label": "Tiedostopolku toisto-ohjelmaan:",
     "media-path-label": "Tiedostopolku videoon (valinnainen):",
     "player-arguments-label": "Toistimen määritteet (ei välttämättä mitään):",
     "browse-label": "Selaa",
     "update-server-list-label": "Päivitä luettelo",

     "more-title": "Näytä lisää asetuksia",
     "never-rewind-value": "Ei koskaan",
     "seconds-suffix": " sekuntia",
     "privacy-sendraw-option": "Lähetä raaka",
     "privacy-sendhashed-option": "Lähetä hash-määreellä",
     "privacy-dontsend-option": "Älä lähetä",
     "filename-privacy-label": "Tiedostonimitiedot:",
     "filesize-privacy-label": "Tiedostokokotideot:",
     "checkforupdatesautomatically-label": "Tarkista Syncplayn päivitykset automaattisesti",
     "autosavejoinstolist-label": "Lisää huoneita joihin liityt huoneluetteloon",
     "slowondesync-label": "Hidasta pienen epäyhdennyksen sattuessa (ei tueta MPC-HC/BE:ssä)",
     "rewindondesync-label": "Kelaa taaksepäin mikäli tapahtuu isompi epäyhdennys (suositeltu)",
     "fastforwardondesync-label": "Pikakelaus eteenpäin mikäli toisto laahaa jäljessä (suositeltu)",
     "dontslowdownwithme-label": "Älä koskaan hidasta tai kelaile muita katsojia (kokeellinen)",
     "pausing-title": "Tauotetaan",
     "pauseonleave-label": "Tautota kun käyttäjä poistuu paikalta (esim. jos yhteytensä katkeaa)",
     "readiness-title": "Alustava valmiustila",
     "readyatstart-label": "Aseta minut 'valmiina katselmaan' vakiollisesti",
     "forceguiprompt-label": "Älä näytä Syncplayn asetusikkunaa aina",  # (Inverted)
     "showosd-label": "Kytke päälle OSD-viestit",

     "showosdwarnings-label": "Sisällytä varoitukset (esim. kun tiedostot ovat eroavaiset, käyttäjät eivät valmiina)",
     "showsameroomosd-label": "Sisällytä huoneeseesi tapahtumat",
     "shownoncontrollerosd-label": "Sisällytä tapahtumat ei-hallinnoijilta ylläpidetyissä huoneissa",
     "showdifferentroomosd-label": "Sisällytä tapahtumat muissa huoneissa",
     "showslowdownosd-label": "Sisällytä hidastus / palautus -huomautukset",
     "language-label": "Kieli:",
     "automatic-language": "Vakiollinen ({})",  # Default language
     "showdurationnotification-label": "Varoita median kokonaiskeston eroavaisuuksista",
     "basics-label": "Perusteet",
     "readiness-label": "Toista/tauota",
     "misc-label": "Muut",
     "core-behaviour-title": "Huoneen lähtökohtainen käyttäytymismalli",
     "syncplay-internals-title": "Syncplayn sisäiset ominaisuudet",
     "syncplay-mediasearchdirectories-title": "Hakemistot joista mediaa etsitään",
     "syncplay-mediasearchdirectories-label": "Hakemistot joista mediaa etsitään (yksi polku aina riviä kohti)",
     "sync-label": "Yhdennys",
     "sync-otherslagging-title": "Mikäli muut laahaavat jäljessä...",
     "sync-youlaggging-title": "Mikäli sinä laahaat jäljessä...",
     "messages-label": "Viestit",
     "messages-osd-title": "Näyttöasetukset",
     "messages-other-title": "Muut näyttöasetukset",
     "chat-label": "Keskustelu",
     "privacy-label": "Yksityisyys",  # Currently unused, but will be brought back if more space is needed in Misc tab
     "privacy-title": "Yksityisyysasetukset",
     "unpause-title": "Kun napsautat toista, aseta itsesi valmiiksi ja :",
     "unpause-ifalreadyready-option": "Ota tauotus pois mikäli jo valmiiksi asetettu valmiiksi",
     "unpause-ifothersready-option": "Ota tauotus pois mikäli jo valmis tai muut huoneessa ovat valmiita (vakio)",
     "unpause-ifminusersready-option": "Ota tauotus pois jos jo valmiina tai mikäli kaikki muut valmiita ja vähimmäismäärä käyttäjistä valmiina",
     "unpause-always": "Ota tauotus pois aina",
     "syncplay-trusteddomains-title": "Luotetut palvelimet- ja palvelut (suoratoistopalveluja varten sekä toisaalla isännöidylle sisällölle)",

     "chat-title": "Keskustelun viestisyöte",
     "chatinputenabled-label": "Ota käyttöön keskustelusyöte mpv:n kautta",
     "chatdirectinput-label": "Salli välitön keskustelusyöte (ei tarvetta painaa syöttöpainiketta eli enteriä viestin lähettämiseen)",
     "chatinputfont-label": "Keskustelusyötteen kirjasin",
     "chatfont-label": "Aseta kirjasin",
     "chatcolour-label": "Aseta väri",
     "chatinputposition-label": "Viestisyötteen paikka mpv:ssä",
     "chat-top-option": "Yläosa",
     "chat-middle-option": "Keskellä",
     "chat-bottom-option": "Alaosa",
     "chatoutputheader-label": "Keskusteluviestin ulostulo",
     "chatoutputfont-label": "Keskusteluviestin ulostulon kirjasin",
     "chatoutputenabled-label": "Kytke keskustelun ulostulo mediatoistimessa (vain mpv tällä hetkellä)",
     "chatoutputposition-label": "Ulostulon tyyli",
     "chat-chatroom-option": "Keskusteluhuoneen tyyli",
     "chat-scrolling-option": "Vierityksen tyyli",

     "mpv-key-tab-hint": "[TAB] kytkee pääsyn aakkosrivin avainoikopolkuihin.",
     "mpv-key-hint": "[ENTER] lähettää viestin. [ESC] pois keskustelutilasta.",
     "alphakey-mode-warning-first-line": "Voit väliaikaisesti käyttää vanhoja mpv-sidoksia näppäinhaarukassa a-z.",
     "alphakey-mode-warning-second-line": "Paina [TAB] palateksesi Syncplayn keskustelutilaan.",

     "help-label": "Apu",
     "reset-label": "Palauta vakiot",
     "run-label": "Aja Syncplay",
     "storeandrun-label": "Tallenna asetukset ja aja Syncplay",

     "contact-label": "Voit vapaasti lähettää sähköpostia osoitteeseen <a href=\"mailto:dev@syncplay.pl\"><nobr>dev@syncplay.pl</nobr></a>, <a href=\"https://github.com/Syncplay/syncplay/issues\"><nobr>luo uusi ongelmailmoitus eli issue</nobr></a> ilmoittaaksesi virheen tai muun ongelman GitHub:in kautta, <a href=\"https://github.com/Syncplay/syncplay/discussions\"><nobr>start a discussion</nobr></a> tehdäksesi ehdotuksen tai kysyäksesi kysymyksen GitHub:in kautta, <a href=\"https://www.facebook.com/SyncplaySoftware\"><nobr>tykkää meistä Facebookissa</nobr></a>, <a href=\"https://twitter.com/Syncplay/\"><nobr>seuraa Twitterissä</nobr></a>, tai käy sivullamme <a href=\"https://syncplay.pl/\"><nobr>https://syncplay.pl/</nobr></a>. Älä käytä Syncplay lähettääksesi arkaluontoisia tietoja.",

     "joinroom-label": "Liity huoneeseen",
     "joinroom-menu-label": "Liity huoneeseen {}",
     "seektime-menu-label": "Hakeudu aikajanan kohtaan",
     "undoseek-menu-label": "Peru haku",
     "play-menu-label": "Toista",
     "pause-menu-label": "Tauota",
     "playbackbuttons-menu-label": "Näytä toistopainikkeet",
     "autoplay-menu-label": "Näytä automaattitoiston painike",
     "autoplay-guipushbuttonlabel": "Toista kun kaikki ovat valmiita",
     "autoplay-minimum-label": "Vähimmäinen käyttäjämäärä:",
     "hideemptyrooms-menu-label": "Piilota tyhjät olemassaolevat huoneet",

     "sendmessage-label": "Lähetä",

     "ready-guipushbuttonlabel": "Olen valmis aloittamaan katselemisen!",

     "roomuser-heading-label": "Huone / käyttäjä",
     "size-heading-label": "Koko",
     "duration-heading-label": "Kesto",
     "filename-heading-label": "Tiedostonimi",
     "notifications-heading-label": "Ilmoitteet",
     "userlist-heading-label": "Luettelo kuka toistaa mitäkin",

     "browseformedia-label": "Selaa etsien mediatiedostoja",

     "file-menu-label": "&Tiedosto",  # & precedes shortcut key
     "openmedia-menu-label": "&Avaa mediatiedosto",
     "openstreamurl-menu-label": "Avaa &mediasuoratoiston URL-osoite",
     "setmediadirectories-menu-label": "Aseta median &hakemistot",
     "loadplaylistfromfile-menu-label": "&Lataa toistoluettelo tiedostosta",
     "saveplaylisttofile-menu-label": "&Tallenna toistoluettelo tiedostoon",
     "exit-menu-label": "P&oistu",
     "advanced-menu-label": "&Edistyneet",
     "window-menu-label": "&Ikkuna",
     "setoffset-menu-label": "Aseta &poikkeama",
     "createcontrolledroom-menu-label": "&Luo hallinoitu huone",
     "identifyascontroller-menu-label": "&Tunnistaudu huonevalvojana",
     "settrusteddomains-menu-label": "Aseta &luotetut palvelinosoitteet",
     "addtrusteddomain-menu-label": "Lisää {} luotettuna palvelinosoitteena tai palveluna",  # Domain

     "edit-menu-label": "&Muokkaa",
     "cut-menu-label": "Le&ikkaa",
     "copy-menu-label": "&Kopioi",
     "paste-menu-label": "&Liitä",
     "selectall-menu-label": "&Valitse kaikki",

     "playback-menu-label": "&Toisto",

     "help-menu-label": "&Apu",
     "userguide-menu-label": "Avaa käyttäjän &opas",
     "update-menu-label": "Tarkista &päiviykset",

     "startTLS-initiated": "Koetetaan muodostaa turvattua yhteyttä",
     "startTLS-secure-connection-ok": "Turvattu yhteys muodostettu ({})",
     "startTLS-server-certificate-invalid": 'Turvatun yhteyden muodostaminen ei onnistunut. Kyseessä oleva palvelin käyttää epäkelpoa turvavarmennetta. Tämä yhteydenpito on mahdollista kaapata kolmannen osapuolen toimesta. Lisätietoja- ja ongelmanratkaisua varten katso <a href="https://syncplay.pl/trouble">here</a>.',
     "startTLS-server-certificate-invalid-DNS-ID": "Syncplay ei luota tähän palvelimeen koska se käyttää varmennetta joka ei ole kelvollinen isäntänimeensä nähden.",
     "startTLS-not-supported-client": "Tämä asiakasohjelma ei tue TLS:ää",
     "startTLS-not-supported-server": "Tämä palvelin ei tue TLS:ää",

     # TLS certificate dialog
     "tls-information-title": "Varmenteen yksityiskohdat",
     "tls-dialog-status-label": "<strong>Syncplay käyttää salattua yhteysmallia kohteeseen {}.</strong>",
     "tls-dialog-desc-label": "salaus digitaalisella varmenteella pitää tiedot yksityisinä niitä lähetettäessä palvelimelle <br/>tai palvelimelta{}.",
     "tls-dialog-connection-label": "Tiedot salataan käyttäen Transport Layer Security (TLS), versiota {} jossa on salauksen <br/>sarja: {}.",
     "tls-dialog-certificate-label": "Varmenne julkistettu {} toimesta ajanmukainen kunnes {}.",

     # About dialog
     "about-menu-label": "&Tietoja Syncplay:stä",
     "about-dialog-title": "Tietoja Syncplay:stä",
     "about-dialog-release": "Julkaisu {} release {}",
     "about-dialog-license-text": "Luvitusmalli on Apache&nbsp;License,&nbsp;Version 2.0",
     "about-dialog-license-button": "Lupa",
     "about-dialog-dependencies": "Riippuvaisuudet",

     "setoffset-msgbox-label": "Aseta poikkeama",
     "offsetinfo-msgbox-label": "Poikkeama (katso https://syncplay.pl/guide/ käyttäohjeita varten):",

     "promptforstreamurl-msgbox-label": "Avaa mediasuoratoiston URL-osoite",
     "promptforstreamurlinfo-msgbox-label": "Suoratoiston URL-osoite",

     "addfolder-label": "Lisää kansio",

     "adduris-msgbox-label": "Lisää URL-osoitteet toistoluetteloon (yksi aina riviä kohti)",
     "editplaylist-msgbox-label": "Aseta soittoluettelo (yksi aina riviä kohti)",
     "trusteddomains-msgbox-label": "Palvelinkohteet joihin on sallittua vaihtaa automaattisesti (yksi aina riviä kohti)",

     "createcontrolledroom-msgbox-label": "Luo hallinnoitu huone",
     "controlledroominfo-msgbox-label": "Syötä hallinnoitavan huoneen nimi\r\n(katso https://syncplay.pl/guide/ käyttöohjeita varten):",

     "identifyascontroller-msgbox-label": "Tunnistaudu huonevalvojana",
     "identifyinfo-msgbox-label": "Syötä hallinnoijan salasana tätä huonetta varten\r\n(katso https://syncplay.pl/guide/ käyttöohjeita varten):",

     "public-server-msgbox-label": "Valitse julkispalvelin tätä katseluistuntoa varten",

     "megabyte-suffix": " Mt",

     # Tooltips

     "host-tooltip": "Isäntäpalvelimen nimi tai IP-osoite johon yhistetään, valinnaisesti sisältäen portin (esim. syncplay.pl:8999). Yhdennetään vain ihmisten kanssa jotka samalla palvelimella/portissa.",
     "name-tooltip": "Lempinimi jolla sinun tullaan tuntemaan. Ei rekisteröintiä, joten voit helposti vaihtaa nimen myöhemmin. Luodaan satunnaisnimi ellet syötä mitään.",
     "password-tooltip": "salasanoja tarvitaan vain yhdistäessä yksityispalvelimille.",
     "room-tooltip": "Huone johon liitytään yhdistämisen jälkeen voi olla lähes mitä tahansa, mutta sinut yhdennetään katselussa vain samassa huoneessa olevien ihmisten kanssa.",

     "edit-rooms-tooltip": "Muokkaa huoneluetteloa.",

     "executable-path-tooltip": "Kohde valitsemallesi median toisto-ohjelmalle (mpv, mpv.net, VLC, MPC-HC/BE, mplayer2 tai IINA).",
     "media-path-tooltip": "Avattavan videon sijainti. Välttämätön määrittää mplayer2:n kohdalla.",
     "player-arguments-tooltip": "Komentokehotteen lisävivut- ja käskyt / vivut jotka toimitetaan eteenpäin tälle median toisto-ohjelmalle.",
     "mediasearcdirectories-arguments-tooltip": "Hakemistot joista Syncplay tulee etsimään mediatiedostoja, esim. kun käytät ""napsautuksella vaihto"" -ominaisuutta. Syncplay etsii läpi alikansioidenkin tuon kansion kautta.",

    "more-tooltip": "Näytä harvemminkäytetyt asetukset.",
    "filename-privacy-tooltip": "Yksityisyystila lähetettäessä sillä hetkellä toistetun tiedoston nimeä palvelimelle.",
    "filesize-privacy-tooltip": "Yksityisyystila lähetettäessä sillä hetkellä toistetun tiedoston koko palvelimelle.",
    "privacy-sendraw-tooltip": "Lähetä tuo tieto ilman peittoa. Tämä on vakiollinen tapa joka suo sujuvimman toiminnallisuuden.",
    "privacy-sendhashed-tooltip": "Lähetä hash-määreellinen tietoversio, tehden sen vähemmän näkyväksi muille asiakasohjelmille.",
    "privacy-dontsend-tooltip": "Älä lähetä tätä tietoa palvelimelle. Tämä tarjoaa enimmäisen yksityisyyden.",
    "checkforupdatesautomatically-tooltip": "Tarkista säännöllisesti Syncplayn verkkosivusto josko Syncplayn uusi julkaisu olisi saatavilla.",
    "autosavejoinstolist-tooltip": "Liittyessäsi huoneeseen palvelimella, muista huoneen nimi automaattisesi liityttävien huoneiden luettelossa.",
    "slowondesync-tooltip": "Vähennä toiston astetta väliaikaisesti kun yhtenevyys tarvitsee uudelleenkohdistaa muiden katselijoiden kanssa. Ei tuettu MPC-HC/BE:ssä.",
    "dontslowdownwithme-tooltip": "Tarkoitten että muut eivät koe hidastumista tai taaksepäin kelaamista mikäli oma toistosi laahaa perässä. Kätevä huonevalvojille.",
    "pauseonleave-tooltip": "Tauota toisto mikäli yhteytesi katkeaa tai joku poistuu huoneestasi.",
    "readyatstart-tooltip": "Aseta itsesi tilaan 'valmis' käynnistyksessä (muutoin näyt 'ei valmiina' kunnes muutat valmiustilaasi)",
    "forceguiprompt-tooltip": "Asetusten ilmoitetta ei näytetä kun tiedostoa avataan Syncplayllä.",  # (Inverted)
    "nostore-tooltip": "Aja Syncplay annetulla asetuskokonaisuudella, mutta älä säilö muutoksia pysyvästi.",  # (Inverted)
    "rewindondesync-tooltip": "Hyppää takaisin mikäli näin on tarpeellinen tehdä päästäksesi takaisin ajallisesti katselussa yhdentyneeksi. Tämän valinnan poiskytkeminen voi johtaa hyvin suuriin yhdentämisen eroavaisuuksiin ja katsotte toistoa aivan eri kohdissa!",
    "fastforwardondesync-tooltip": "Hyppää eteenpäin kun yhdentäminen on katkennut huonevalvojan kanssa (tai teeskennnyskohdan suhteen jos 'älä hidasta koskaan- tai taaksepäin kelaa muita' on kytkettynä).",
    "showosd-tooltip": "Lähettää Syncplay-viestejä mediatoistimen OSD:hen.",
    "showosdwarnings-tooltip": "Näytä varoitukset mikäli toistossa on eri tiedosto, yksin huoneessa, tai käyttäjät eivät valmiina, jne.",
    "showsameroomosd-tooltip": "Näytä OSD-ilmoitteet tapahtumille liittyen huoneeseen jossa käyttäjä on.",
    "shownoncontrollerosd-tooltip": "Näytä OSD-ilmoitteet tapahtumille liittyen ei-huonevalvojiin jotka ovat hallinnoiduissa huoneissa.",
    "showdifferentroomosd-tooltip": "Näytä OSD-ilmoitteet tapahtumille liittyen huoneeseen jossa käyttäjä ei ole.",
    "showslowdownosd-tooltip": "Näytä ilmoitteet hidastamisesta / palautuksesta aikaeroavaisuuden takia.",
    "showdurationnotification-tooltip": "Hyödylinen silloin kun osio moniosaisen tiedoston suhteen uupuu, mutta voi tuottaa vääriä ilmoitusarvoja.",
    "language-tooltip": "Kieli jota käytetään Syncplayssä.",
    "unpause-always-tooltip": "Mikäli painat 'tauko pois' asettaa se toimi sinut aina valmiiksi ja tauon pois päältä, sen sijaan että näyt vain 'valmiina'.",
    "unpause-ifalreadyready-tooltip": "Mikäli painat tauon pois kun et valmis se asettaa sinut kuitenkin valmiiksi - paina tauko pois uudelleen jatkaaksesi toistoa.",
    "unpause-ifothersready-tooltip": "Mikäli painat tauon pois kun et valmis, se tauottaa ainoastaan jos muut ovat valmiina.",
    "unpause-ifminusersready-tooltip": "Mikäli painat tauon pois kun et valmiina, se ottaa tauon pois vain jos muut ovat valmiina ja vähimmäismäärä käyttäjiä on täytetty.",
    "trusteddomains-arguments-tooltip": "Palvelimet- ja palvelut jotka ovat sallittuja vaihtaa käyttöön automaattisesti Syncplayssä kun jaetut toistoluettelot on kytketty käyttöön.",

    "chatinputenabled-tooltip": "Kytke päälle keskustelusyöte mpv:ssä (paina syöttönäppäintä eli enter keskustellaksesi, tuota samaa näppäintä lähettääksesi viestin, Esc -painiketta keskeyttääksesi)",
    "chatdirectinput-tooltip": "Ohita tuon syöttänäppäimen eli 'enter' painallustarve ja siirry suoraan syöttötilaan mpv:ssä. Paina TAB mpv:ssä kytkeäksesi väliaikaisesti tämän ominaisuuden pois päältä.",
    "font-label-tooltip": "Kirjasintyyli jota käytetään lähettäessä keskusteluviestejä mpv:ssä. Vain asiakasohjelmapuoli pätee tässä, joten ei vaikuta siihen mitä muut näkevät.",
    "set-input-font-tooltip": "Kirjasinperhe jota käytetään syötettäessä viestejä mpv:ssä. Vain asiakasohjelmapuoli pätee tässä, joten ei vaikuta siihen mitä muut näkevät.",
    "set-input-colour-tooltip": "Kirjasimen väri jota käytetään syötettäessä viestejä mpv:ssä. Vain asiakasohjelmapuoli pätee tässä, joten ei vaikuta siihen mitä muut näkevät.",
    "chatinputposition-tooltip": "Sijainti mpv-toistimessa missä keskusteluviestit näkyvät kun painat syötepainiketta eli enteriä ja kirjoitat.",
    "chatinputposition-top-tooltip": "Aseta keskustelusyöte mpv-ikkunan yläosaan.",
    "chatinputposition-middle-tooltip": "Aseta keskustelusyöte mpv-ikkunan keskelle.",
    "chatinputposition-bottom-tooltip": "Aseta keksustelusyöte mpv-ikkunan alaosaan.",
    "chatoutputenabled-tooltip": "Näytä keskusteluviestit OSD:ssä (mikäli mediatoistin tätä tukee).",
    "font-output-label-tooltip": "Keksustelun ulosmeno kirjasin.",
    "set-output-font-tooltip": "Kirjasin jota käytetään tulostaessa keskusteluviestejä näytölle.",
    "chatoutputmode-tooltip": "Miten keskusteluviestit näytetään.",
    "chatoutputmode-chatroom-tooltip": "Näytä uusia keskustelun rivejä suoraan edellisen rivin alle.",
    "chatoutputmode-scrolling-tooltip": "Rullaa keskustelutekstiä oikealta vasemmalle.",

    "help-tooltip": "Avaa Syncplay.pl:n käyttöohjeen.",
    "reset-tooltip": "Nollaa kaikki asetukset niiden vakiolliseen lähtökohtaan.",
    "update-server-list-tooltip": "Yhdistä syncplay.pl:ään julkisten palvelinten luettelon päivittämiseksi.",

    "sslconnection-tooltip": "Yhteys muodostettu turvallisesti palvelimeen. Napsauta varmennetta saadaksesi yksityiskohtaista tietoa.",

    "joinroom-tooltip": "Poistuu nykyisestä huoneesta ja liittyy määriteltyyn huoneeseen.",
    "seektime-msgbox-label": "Hyppää määriteltyyn aikakohtaan (sekunneissa / min:sek). Käytä painikkeita +/- hakeaksesi edelleen tarkemmin kohtaa.",
    "ready-tooltip": "Osoittaa oletko valmiina aloittamaan katselemisen.",
    "autoplay-tooltip": "Toista automaattisesti kun kaikki käyttäjät joilla on valmiusilmaisin osoittamassa 'valmis' ja vähimmäinen käyttäjämäärä on saavutettu.",
    "switch-to-file-tooltip": "Kaksoisnapsauta vaihtaaksesi kohteeseen {}",  # Filename
    "sendmessage-tooltip": "Lähetä viesti huoneeseen",

    # In-userlist notes (GUI)
    "differentsize-note": "Eroava koko!",
    "differentsizeandduration-note": "Eroava koko ja kesto!",
    "differentduration-note": "Eroava kesto!",
    "nofile-note": "(Mitään tiedostoa ei ole toistossa)",

    # Server messages to client
    "new-syncplay-available-motd-message": "Käytät Syncplay:tä {} mutta uudempi julkaisu on tarjolla osoitteessa https://syncplay.pl",  # ClientVersion
    "persistent-rooms-notice": "HUOMIO: Tämä palvelin käyttää pysyviä huoneita, joka tarkoittaa, että toistoluettelojen tieto taltioidaan toistoistuntojen välillä. Mikäli halkuat luoda huoneen jossa tietoja ei tallenneta, laita vipu -temp huoneen nimen perään.", # NOTE: Do not translate the word -temp
    "ready-chat-message": "I have set {} as ready.",  # User # TODO: Translate
    "not-ready-chat-message": "I have set {} as not ready.",  # User # TODO: Translate

    # Server notifications
    "welcome-server-notification": "Tervetuloa Syncplay-palvelimelle, ver. {0}",  # version
    "client-connected-room-server-notification": "{0}({2}) yhteydessä huoneeseen '{1}'",  # username, host, room
    "client-left-server-notification": "{0} poistui palvelimelta",  # name
    "no-salt-notification": "HUOMAATHAN: salliaksesi huonevalvojan salasanoja muodostettavaksi tällä palvelimella ja niiden toimiakseen myös kun palvelin uudelleenkäynnistetään, lisääthän seuraavan kaksoisvivun kun ajat Syncplaytä tällä palvelimella tulevaisuudessa: --salt {}",  # Salt


    # Server arguments
    "server-argument-description": 'Ratkaisu toiston yhdentämiseen useiden mediatoistinten kanssa verkon yli. Palvelin',
    "server-argument-epilog": 'Mikäli vaihtoehtoja ei määritetä käytetään _config arvoja',
    "server-port-argument": 'palvelimen TCP-port',
    "server-password-argument": 'palvelimen salasana',
    "server-isolate-room-argument": 'eristetäänkö huoneet?',
    "server-salt-argument": "satunnaislanka jota käytetään luodakseen hallinnoitujen huoneiden salasanoja",
    "server-disable-ready-argument": "poista käytöstä valmiusominaisuus",
    "server-motd-argument": "tiedostopolku tiedostoon josta motd noudetaan",
    "server-rooms-argument": "polku tietokantatiedostoon jota käytetään tai jos pysyväishuoneen dataa varten. Kytkee päälle huoneiden pysyvyyden ilman katsojia ja säilyvyys pysyy uudelleenkäynnistysenkin jälkeen",
    "server-permanent-rooms-argument": "polku tiedostoon joka luetteloi pysyvät huoneet jotka luetteloidaan vaikka huone olisi tyhjäkin (tekstitiedostomuodossa joka luetteloi joka luetteloi yhden huoneen aina riviä kohden) - vaatii pysyvien huoneiden -toiminnon päällekytkennän",
    "server-chat-argument": "Kytketäänkö keskustelu pois päältä?",
    "server-chat-maxchars-argument": "Merkkien enimmäismäärä keskusteluviestissä (vakio on {})", # Default number of characters
    "server-maxusernamelength-argument": "Merkkien enimmäismäärä käyttäjänimessä (vakio on {})",
    "server-stats-db-file-argument": "Kytke päälle palvelintilastot käyttäen toimitettua SQLite db -tiedostoa",
    "server-startTLS-argument": "Kytke päälle TLS-yhteydet käyttäen varmennetiedostoja annetun tiedostopolkun kautta",
    "server-messed-up-motd-unescaped-placeholders": "Päivän viestissä on epäkelvot paikkamerkit. Kaikki $ merkit tulisi kaksinaistaa ($$).",
    "server-messed-up-motd-too-long": "Päivän viesti on liian pitkä - enimmäispituus on {} merkkiä, {} annettu.",

    # Server errors
    "unknown-command-server-error": "Tuntematon käsky {}",  # message
    "not-json-server-error": "Tämä ei ole json-enkoodattu käskyjono {}",  # message
    "line-decode-server-error": "Tämä ei ole utf-8 -lanka",
    "not-known-server-error": "Palvelimen tulee tuntea sinut ensinnä ennen kuin voit lähettää tämän käskyn",
    "client-drop-server-error": "Asiakasohjelman pudotus: {} -- {}",  # host, error
    "password-required-server-error": "Salasana on vaadittu",
    "wrong-password-server-error": "Toimitit väärän salasanan",
    "hello-server-error": "Not enough Hello arguments",  # DO NOT TRANSLATE

    # Playlists
    "playlist-selection-changed-notification":  "{} toistoluettelon valintoja muutettiin",  # Username
    "playlist-contents-changed-notification": "{} toistoluettelo päivitettiin",  # Username
    "cannot-find-file-for-playlist-switch-error": "Tiedostoa {} ei löytynyt mediahakemistoista toistoluettelon vaihtoa varten!",  # Filename
    "cannot-add-duplicate-error": "Toisarvoista kohdetta ei saatu lisättyä '{}' toistoluetteloon koska kaksoiskappaleita ei sallita.",  # Filename
    "cannot-add-unsafe-path-error": "Ei voitu ladata automaattisesti kohdetta {} koska se ei ole luotettu. Voit vaihtaa URL-osoitteen käsin kaksoisnapsauttamalla sitä toistoluettelossa, ja sitten vain lisäät luotetut palvelimet valikosta Tiedosto ->Edistyneet->Aseta luotetut palvelimet. Mikäli napsautat hiiren oikealla napilla URL-osoitteessa voit täten asettaa sen luotetuksi aihevalikon kautta.",  # Filename
    "sharedplaylistenabled-label": "Kytke jaetut toistoluettelot käyttöön",
    "removefromplaylist-menu-label": "Poista toistoluettelosta",
    "shuffleremainingplaylist-menu-label": "Sekoita jäljellä oleva toistoluettelosisältö",
    "shuffleentireplaylist-menu-label": "Sekoita koko toistoluettelo",
    "undoplaylist-menu-label": "Kumoa toistoluettelon viime muutos",
    "addfilestoplaylist-menu-label": "Lisää tiedosto(t) toistoluettelon alaosaan",
    "addurlstoplaylist-menu-label": "Lisää URL-osoite(tai osoitteet) toistoluettelon alaosaan",
    "editplaylist-menu-label": "Muokkaa toistoluetteloa",

    "open-containing-folder": "Avaa kansio jossa tämä tiedosto sijaitsee",
    "addyourfiletoplaylist-menu-label": "Lisää tiedostosi toistoluetteloon",
    "addotherusersfiletoplaylist-menu-label": "Lisää {}'n tiedosto toistoluetteloon",  # [Username]
    "addyourstreamstoplaylist-menu-label": "Lisää suoratoistosi toistoluetteloon",
    "addotherusersstreamstoplaylist-menu-label": "Lisää {}'n suoratoisto toistoluetteloon",  # [Username]
    "openusersstream-menu-label": "Avaa {}'n suoratoisto",  # [username]'s
    "openusersfile-menu-label": "Avaa {}'n tiedosto",  # [username]'s

    "setasready-menu-label": "Set {} as ready",  # [Username] # TODO: Translate
    "setasnotready-menu-label": "Set {} as not ready",  # [Username] # TODO: Translate

    "playlist-instruction-item-message": "Raahaa tiedosto tähän lisätäksesi sen jaettuun toistoluetteloon.",
    "sharedplaylistenabled-tooltip": "Huonevalvojat voivat lisätä tiedostoja yhdennettävään toistoluetteloon tehdäkseen kaikille helpoksi katsoa samaa asiaa. Määritä mediahakemistot kohteen 'Muut' alta.",

    "playlist-empty-error": "Toistoluettelo on tällä hetkellä tyhjä.",
    "playlist-invalid-index-error": "Epäkelpo toistoluettelohakemisto",
}