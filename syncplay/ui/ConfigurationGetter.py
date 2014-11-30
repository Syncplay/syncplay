from ConfigParser import SafeConfigParser, DEFAULTSECT
import argparse
import os
import sys
from syncplay import constants, utils, version, milestone
from syncplay.messages import getMessage, setLanguage
from syncplay.players.playerFactory import PlayerFactory
import codecs
try:
    from syncplay.ui.GuiConfiguration import GuiConfiguration
    from PySide import QtGui  # @UnresolvedImport
    from PySide.QtCore import QCoreApplication
except ImportError:
    print getMessage("unable-import-gui-error")
    GuiConfiguration = None

class InvalidConfigValue(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)

class ConfigurationGetter(object):
    def __init__(self):
        self._config = {
                        "host": None,
                        "port": constants.DEFAULT_PORT,
                        "name": None,
                        "debug": False,
                        "forceGuiPrompt": True,
                        "noGui": False,
                        "noStore": False,
                        "room": "",
                        "password": None,
                        "playerPath": None,
                        "file": None,
                        "playerArgs": [],
                        "playerClass": None,
                        "slowdownThreshold": constants.DEFAULT_SLOWDOWN_KICKIN_THRESHOLD,
                        "rewindThreshold": constants.DEFAULT_REWIND_THRESHOLD,
                        "fastforwardThreshold": constants.DEFAULT_FASTFORWARD_THRESHOLD,
                        "rewindOnDesync": True,
                        "slowOnDesync": True,
                        "fastforwardOnDesync": True,
                        "dontSlowDownWithMe": False,
                        "filenamePrivacyMode": constants.PRIVACY_SENDRAW_MODE,
                        "filesizePrivacyMode": constants.PRIVACY_SENDRAW_MODE,
                        "pauseOnLeave": False,
                        "clearGUIData": False,
                        "language" : "",
                        "resetConfig" : False,
                        "showOSD" : True,
                        "showOSDWarnings" : True,
                        "showSlowdownOSD" : True,
                        "showDifferentRoomOSD" : False,
                        "showSameRoomOSD" : True,
                        "showNonControllerOSD" : False,
                        "showContactInfo" : True,
                        "showDurationNotification" : True
                        }

        self._defaultConfig = self._config.copy()

        #
        # Custom validation in self._validateArguments
        #
        self._required = [
                          "host",
                          "port",
                          "room",
                          "playerPath",
                          "playerClass",
                         ]

        self._boolean = [
                         "debug",
                         "forceGuiPrompt",
                         "noGui",
                         "noStore",
                         "dontSlowDownWithMe",
                         "pauseOnLeave",
                         "clearGUIData",
                         "rewindOnDesync",
                         "slowOnDesync",
                         "pauseOnLeave",
                         "clearGUIData",
                         "resetConfig",
                         "showOSD",
                         "showOSDWarnings",
                         "showSlowdownOSD",
                         "showDifferentRoomOSD",
                         "showSameRoomOSD",
                         "showNonControllerOSD",
                         "showContactInfo" ,
                         "showDurationNotification"
                        ]

        self._numeric = [
            "slowdownThreshold",
            "rewindThreshold",
            "fastforwardThreshold",
        ]

        self._iniStructure = {
                        "server_data": ["host", "port", "password"],
                        "client_settings": ["name", "room", "playerPath", "slowdownThreshold", "rewindThreshold", "fastforwardThreshold", "slowOnDesync", "rewindOnDesync", "fastforwardOnDesync", "dontSlowDownWithMe", "forceGuiPrompt", "filenamePrivacyMode", "filesizePrivacyMode", "pauseOnLeave"],
                        "gui": ["showOSD", "showOSDWarnings", "showSlowdownOSD", "showDifferentRoomOSD", "showSameRoomOSD", "showNonControllerOSD", "showContactInfo" , "showDurationNotification"],
                        "general": ["language"]
                        }

        self._playerFactory = PlayerFactory()

    def _validateArguments(self):
        if self._config['resetConfig']:
            language = self._config['language']
            self._config = self._defaultConfig
            self._config['language'] = language
            raise InvalidConfigValue("*"+getMessage("config-cleared-notification"))

        def _isPortValid(varToTest):
            try:
                if varToTest == "" or varToTest is None:
                    return False
                if str(varToTest).isdigit() == False:
                    return False
                varToTest = int(varToTest)
                if varToTest > 65535 or varToTest < 1:
                    return False
                return True
            except:
                return False
        for key in self._boolean:
            if self._config[key] == "True":
                self._config[key] = True
            elif self._config[key] == "False":
                self._config[key] = False

        for key in self._numeric:
            self._config[key] = float(self._config[key])

        for key in self._required:
            if key == "playerPath":
                player = None
                if self._config["playerPath"]:
                    player = self._playerFactory.getPlayerByPath(self._config["playerPath"])
                if player:
                    self._config["playerClass"] = player
                else:
                    raise InvalidConfigValue("Player path is not set properly")
                if player.__name__ in ['MpvPlayer', 'MplayerPlayer']:
                    if not self._config['file']:
                        raise InvalidConfigValue("File must be selected before starting your player")
            elif key == "host":
                self._config["host"], self._config["port"] = self._splitPortAndHost(self._config["host"])
                hostNotValid = (self._config["host"] == "" or self._config["host"] is None)
                portNotValid = (_isPortValid(self._config["port"]) == False)
                if hostNotValid:
                    raise InvalidConfigValue("Hostname can't be empty")
                elif portNotValid:
                    raise InvalidConfigValue("Port must be valid")
            elif self._config[key] == "" or self._config[key] is None:
                raise InvalidConfigValue("{} can't be empty".format(key.capitalize()))

    def _overrideConfigWithArgs(self, args):
        for key, val in vars(args).items():
            if val:
                if key == "force_gui_prompt":
                    key = "forceGuiPrompt"
                if key == "no_store":
                    key = "noStore"
                if key == "player_path":
                    key = "playerPath"
                if key == "_args":
                    key = "playerArgs"
                if key == "no_gui":
                    key = "noGui"
                if key == "clear_gui_data":
                    key = "clearGUIData"
                self._config[key] = val

    def _splitPortAndHost(self, host):
        port = constants.DEFAULT_PORT if not self._config["port"] else self._config["port"]
        if host:
            if ':' in host:
                host, port = host.split(':', 1)
                try:
                    port = int(port)
                except ValueError:
                    try:
                        port = port.encode('ascii', 'ignore')
                    except:
                        port = ""
        return host, port

    def _checkForPortableFile(self):
        path = utils.findWorkingDir()
        for name in constants.CONFIG_NAMES:
            if os.path.isfile(os.path.join(path, name)):
                return os.path.join(path, name)

    def _getConfigurationFilePath(self):
        configFile = self._checkForPortableFile()
        if not configFile:
            for name in constants.CONFIG_NAMES:
                if configFile and os.path.isfile(configFile):
                    break
                if os.name <> 'nt':
                    configFile = os.path.join(os.getenv('HOME', '.'), name)
                else:
                    configFile = os.path.join(os.getenv('APPDATA', '.'), name)
            if configFile and not os.path.isfile(configFile):
                if os.name <> 'nt':
                    configFile = os.path.join(os.getenv('HOME', '.'), constants.DEFAULT_CONFIG_NAME_LINUX)
                else:
                    configFile = os.path.join(os.getenv('APPDATA', '.'), constants.DEFAULT_CONFIG_NAME_WINDOWS)

        return configFile

    def _parseConfigFile(self, iniPath, createConfig=True):
        parser = SafeConfigParserUnicode()
        if not os.path.isfile(iniPath):
            if createConfig:
                open(iniPath, 'w').close()
            else:
                return
        parser.readfp(codecs.open(iniPath, "r", "utf_8_sig"))
        for section, options in self._iniStructure.items():
            if parser.has_section(section):
                for option in options:
                    if parser.has_option(section, option):
                        self._config[option] = parser.get(section, option)

    def _checkConfig(self):
        try:
            self._validateArguments()
        except InvalidConfigValue as e:
            try:
                for key, value in self._promptForMissingArguments(e.message).items():
                    self._config[key] = value
                self._checkConfig()
            except:
                sys.exit()

    def _promptForMissingArguments(self, error=None):
        if self._config['noGui'] or not GuiConfiguration:
            if error:
                print "{}!".format(error)
            print getMessage("missing-arguments-error")
            sys.exit()
        elif GuiConfiguration:
            gc = GuiConfiguration(self._config, error=error)
            gc.setAvailablePaths(self._playerFactory.getAvailablePlayerPaths())
            gc.run()
            return gc.getProcessedConfiguration()

    def __wasOptionChanged(self, parser, section, option):
        if parser.has_option(section, option):
            if parser.get(section, option) != unicode(self._config[option]):
                return True
        else:
            return True

    def _saveConfig(self, iniPath):
        changed = False
        if self._config['noStore']:
            return
        parser = SafeConfigParserUnicode()
        parser.readfp(codecs.open(iniPath, "r", "utf_8_sig"))
        for section, options in self._iniStructure.items():
            if not parser.has_section(section):
                parser.add_section(section)
                changed = True
            for option in options:
                if self.__wasOptionChanged(parser, section, option):
                    changed = True
                parser.set(section, option, unicode(self._config[option]).replace('%', '%%'))
        if changed:
            parser.write(codecs.open(iniPath, "wb", "utf_8_sig"))


    def _forceGuiPrompt(self):
        if GuiConfiguration:
            try:
                self._validateArguments()
            except InvalidConfigValue:
                pass

            try:
                if self._config['noGui'] == False:
                    for key, value in self._promptForMissingArguments().items():
                        self._config[key] = value
            except GuiConfiguration.WindowClosed:
                sys.exit()
        else:
            try:
                self._validateArguments()
            except InvalidConfigValue:
                self._promptForMissingArguments()
                sys.exit()

    def __getRelativeConfigLocations(self):
        locations = []
        path = os.path.dirname(os.path.realpath(self._config['file']))
        locations.append(path)
        while path != os.path.dirname(path):
            path = os.path.dirname(path)
            locations.append(path)
        locations.reverse()
        return locations

    def _loadRelativeConfiguration(self):
        locations = self.__getRelativeConfigLocations()
        loadedPaths = []
        for location in locations:
            for name in constants.CONFIG_NAMES:
                path = location + os.path.sep + name
                if os.path.isfile(path) and (os.name == 'nt' or path != os.path.join(os.getenv('HOME', '.'), constants.DEFAULT_CONFIG_NAME_LINUX)):
                    loadedPaths.append("'" + os.path.normpath(path) + "'")
                    self._parseConfigFile(path, createConfig=False)
                    self._checkConfig()
        return loadedPaths

    def getConfiguration(self):
        iniPath = self._getConfigurationFilePath()
        self._parseConfigFile(iniPath)
        #
        # Watch out for the method self._overrideConfigWithArgs when you're adding custom multi-word command line arguments
        #
        if self._config['language']:
            setLanguage(self._config['language'])
        self._argparser = argparse.ArgumentParser(description=getMessage("argument-description"),
                                         epilog=getMessage("argument-epilog"))
        self._argparser.add_argument('--no-gui', action='store_true', help=getMessage("nogui-argument"))
        self._argparser.add_argument('-a', '--host', metavar='hostname', type=str, help=getMessage("host-argument"))
        self._argparser.add_argument('-n', '--name', metavar='username', type=str, help=getMessage("name-argument"))
        self._argparser.add_argument('-d', '--debug', action='store_true', help=getMessage("debug-argument"))
        self._argparser.add_argument('-g', '--force-gui-prompt', action='store_true', help=getMessage("force-gui-prompt-argument"))
        self._argparser.add_argument('--no-store', action='store_true', help=getMessage("no-store-argument"))
        self._argparser.add_argument('-r', '--room', metavar='room', type=str, nargs='?', help=getMessage("room-argument"))
        self._argparser.add_argument('-p', '--password', metavar='password', type=str, nargs='?', help=getMessage("password-argument"))
        self._argparser.add_argument('--player-path', metavar='path', type=str, help=getMessage("player-path-argument"))
        self._argparser.add_argument('--language', metavar='language', type=str, help=getMessage("language-argument"))
        self._argparser.add_argument('file', metavar='file', type=str, nargs='?', help=getMessage("file-argument"))
        self._argparser.add_argument('--clear-gui-data', action='store_true', help=getMessage("clear-gui-data-argument"))
        self._argparser.add_argument('-v', '--version', action='store_true', help=getMessage("version-argument"))
        self._argparser.add_argument('_args', metavar='options', type=str, nargs='*', help=getMessage("args-argument"))
        args = self._argparser.parse_args()
        if args.version:
            print getMessage("version-message").format(version, milestone)
            sys.exit()
        self._overrideConfigWithArgs(args)
        if self._config['file'] and self._config['file'][:2] == "--":
            self._config['playerArgs'].insert(0, self._config['file'])
            self._config['file'] = None
        # Arguments not validated yet - booleans are still text values
        if self._config['language']:
            setLanguage(self._config['language'])
        if (self._config['forceGuiPrompt'] == "True" or not self._config['file']) and GuiConfiguration and not self._config['noGui']:
            self._forceGuiPrompt()
        self._checkConfig()
        self._saveConfig(iniPath)
        if self._config['file']:
            self._config['loadedRelativePaths'] = self._loadRelativeConfiguration()
        if self._config['language']:
            setLanguage(self._config['language'])
        if not GuiConfiguration:
            self._config['noGui'] = True
        if not self._config['noGui']:
            from syncplay.vendor import qt4reactor
            if QCoreApplication.instance() is None:
                self.app = QtGui.QApplication(sys.argv)
            qt4reactor.install()
        return self._config

class SafeConfigParserUnicode(SafeConfigParser):
    def write(self, fp):
        """Write an .ini-format representation of the configuration state."""
        if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key == "__name__":
                    continue
                if (value is not None) or (self._optcre == self.OPTCRE):
                    key = " = ".join((key, unicode(value).replace('\n', '\n\t')))
                fp.write("%s\n" % key)
            fp.write("\n")
