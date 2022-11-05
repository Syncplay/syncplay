
import argparse
import ast
import codecs
import re
import os
import sys
from configparser import SafeConfigParser, DEFAULTSECT

from syncplay import constants, utils, version, milestone
from syncplay.messages import getMessage, setLanguage, isValidLanguage
from syncplay.players.playerFactory import PlayerFactory
from syncplay.utils import isMacOS, isWindows


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
            "roomList": [],
            "password": None,
            "playerPath": None,
            "perPlayerArguments": None,
            "mediaSearchDirectories": None,
            "sharedPlaylistEnabled": True,
            "loopAtEndOfPlaylist": False,
            "loopSingleFiles": False,
            "onlySwitchToTrustedDomains": True,
            "autosaveJoinsToList": True,
            "trustedDomains": constants.DEFAULT_TRUSTED_DOMAINS,
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
            "readyAtStart": False,
            "unpauseAction": constants.UNPAUSE_IFOTHERSREADY_MODE,
            "autoplayInitialState": None,
            "autoplayMinUsers": -1,
            "autoplayRequireSameFilenames": True,
            "clearGUIData": False,
            "language": "",
            "checkForUpdatesAutomatically": None,
            "lastCheckedForUpdates": "",
            "resetConfig": False,
            "showOSD": True,
            "showOSDWarnings": True,
            "showSlowdownOSD": True,
            "showDifferentRoomOSD": False,
            "showSameRoomOSD": True,
            "showNonControllerOSD": False,
            "showContactInfo": True,
            "showDurationNotification": True,
            "chatInputEnabled": True,
            "chatInputFontFamily": 'sans-serif',
            "chatInputRelativeFontSize": constants.DEFAULT_CHAT_FONT_SIZE,
            "chatInputFontWeight": constants.DEFAULT_CHAT_FONT_WEIGHT,
            "chatInputFontUnderline": False,
            "chatInputFontColor": constants.DEFAULT_CHAT_INPUT_FONT_COLOR,
            "chatInputPosition": constants.INPUT_POSITION_TOP,
            "chatDirectInput": False,
            "chatOutputEnabled": True,
            "chatOutputFontFamily": 'sans-serif',
            "chatOutputRelativeFontSize": constants.DEFAULT_CHAT_FONT_SIZE,
            "chatOutputFontWeight": constants.DEFAULT_CHAT_FONT_WEIGHT,
            "chatOutputFontUnderline": False,
            "chatOutputMode": constants.CHATROOM_MODE,
            "chatMaxLines": 7,
            "chatTopMargin": 25,
            "chatLeftMargin": 20,
            "chatBottomMargin": 30,
            "chatMoveOSD": True,
            "chatOSDMargin": 110,
            "notificationTimeout": 3,
            "alertTimeout": 5,
            "chatTimeout": 7,
            "publicServers": [],
            "loadPlaylistFromFile": None
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
            "readyAtStart",
            "autoplayRequireSameFilenames",
            "clearGUIData",
            "rewindOnDesync",
            "slowOnDesync",
            "fastforwardOnDesync",
            "pauseOnLeave",
            "clearGUIData",
            "resetConfig",
            "showOSD",
            "showOSDWarnings",
            "showSlowdownOSD",
            "showDifferentRoomOSD",
            "showSameRoomOSD",
            "showNonControllerOSD",
            "showDurationNotification",
            "sharedPlaylistEnabled",
            "loopAtEndOfPlaylist",
            "loopSingleFiles",
            "onlySwitchToTrustedDomains",
            "autosaveJoinsToList",
            "chatInputEnabled",
            "chatInputFontUnderline",
            "chatDirectInput",
            "chatMoveOSD",
            "chatOutputEnabled",
            "chatOutputFontUnderline"
        ]
        self._tristate = [
            "checkForUpdatesAutomatically",
            "autoplayInitialState",
        ]

        self._serialised = [
            "roomList",
            "perPlayerArguments",
            "mediaSearchDirectories",
            "trustedDomains",
            "publicServers",
        ]

        self._numeric = [
            "slowdownThreshold",
            "rewindThreshold",
            "fastforwardThreshold",
            "autoplayMinUsers",
            "chatInputRelativeFontSize",
            "chatInputFontWeight",
            "chatOutputFontWeight",
            "chatOutputRelativeFontSize",
            "chatMaxLines",
            "chatTopMargin",
            "chatLeftMargin",
            "chatBottomMargin",
            "chatOSDMargin",
            "notificationTimeout",
            "alertTimeout",
            "chatTimeout"
        ]

        self._hexadecimal = [
            "chatInputFontColor"
        ]

        self._iniStructure = {
            "server_data": ["host", "port", "password"],
            "client_settings": [
                "name", "room", "roomList", "playerPath",
                "perPlayerArguments", "slowdownThreshold",
                "rewindThreshold", "fastforwardThreshold",
                "slowOnDesync", "rewindOnDesync",
                "fastforwardOnDesync", "dontSlowDownWithMe",
                "forceGuiPrompt", "filenamePrivacyMode",
                "filesizePrivacyMode", "unpauseAction",
                "pauseOnLeave", "readyAtStart", "autoplayMinUsers",
                "autoplayInitialState", "mediaSearchDirectories",
                "sharedPlaylistEnabled", "loopAtEndOfPlaylist",
                "loopSingleFiles",
                "autoplayRequireSameFilenames",
                "onlySwitchToTrustedDomains", "trustedDomains", "publicServers"],
            "gui": [
                "autosaveJoinsToList",
                "showOSD", "showOSDWarnings", "showSlowdownOSD",
                "showDifferentRoomOSD", "showSameRoomOSD",
                "showNonControllerOSD", "showDurationNotification",
                "chatInputEnabled", "chatInputFontUnderline",
                "chatInputFontFamily", "chatInputRelativeFontSize",
                "chatInputFontWeight", "chatInputFontColor",
                "chatInputPosition", "chatDirectInput",
                "chatOutputFontFamily", "chatOutputRelativeFontSize",
                "chatOutputFontWeight", "chatOutputFontUnderline",
                "chatOutputMode", "chatMaxLines",
                "chatTopMargin", "chatLeftMargin",
                "chatBottomMargin", "chatDirectInput",
                "chatMoveOSD", "chatOSDMargin",
                "notificationTimeout", "alertTimeout",
                "chatTimeout", "chatOutputEnabled"],
            "general": [
                "language", "checkForUpdatesAutomatically",
                "lastCheckedForUpdates"]
        }

        self._playerFactory = PlayerFactory()

    def _validateArguments(self):
        if self._config['resetConfig']:
            language = self._config['language']
            checkForUpdatesAutomatically = self._config['checkForUpdatesAutomatically']
            self._config = self._defaultConfig
            self._config['language'] = language
            self._config['checkForUpdatesAutomatically'] = checkForUpdatesAutomatically
            raise InvalidConfigValue("*" + getMessage("config-cleared-notification"))

        if not isValidLanguage(self._config['language']):
            self._config['language'] = ""

        def _isPortValid(varToTest):
            try:
                if varToTest == "" or varToTest is None:
                    return False
                if not str(varToTest).isdigit():
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

        for key in self._serialised:
            if self._config[key] is None or self._config[key] == "":
                self._config[key] = {}
            elif isinstance(self._config[key], str):
                self._config[key] = ast.literal_eval(self._config[key])

        for key in self._tristate:
            if self._config[key] == "True":
                self._config[key] = True
            elif self._config[key] == "False":
                self._config[key] = False
            elif self._config[key] == "None":
                self._config[key] = None

        for key in self._numeric:
            self._config[key] = float(self._config[key])

        for key in self._hexadecimal:
            match = re.search(r'^#(?:[0-9a-fA-F]){6}$', self._config[key])
            if not match:
                self._config[key] = "#FFFFFF"

        for key in self._required:
            if key == "playerPath":
                player = None
                if self._config["playerPath"]:
                    player = self._playerFactory.getPlayerByPath(self._config["playerPath"])
                if player:
                    self._config["playerClass"] = player
                else:
                    raise InvalidConfigValue(getMessage("player-path-config-error"))
                playerPathErrors = player.getPlayerPathErrors(
                    self._config["playerPath"], self._config['file'] if self._config['file'] else None)
                if playerPathErrors:
                    raise InvalidConfigValue(playerPathErrors)
            elif key == "host":
                self._config["host"], self._config["port"] = self._splitPortAndHost(self._config["host"])
                hostNotValid = (self._config["host"] == "" or self._config["host"] is None)
                portNotValid = (_isPortValid(self._config["port"]) == False)
                if hostNotValid:
                    raise InvalidConfigValue(getMessage("no-hostname-config-error"))
                elif portNotValid:
                    raise InvalidConfigValue(getMessage("invalid-port-config-error"))
            elif self._config[key] == "" or self._config[key] is None:
                raise InvalidConfigValue(getMessage("empty-value-config-error").format(key.capitalize()))

    def _overrideConfigWithArgs(self, args):
        for key, val in list(vars(args).items()):
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
                if key == "load_playlist_from_file":
                    key = "loadPlaylistFromFile"
                self._config[key] = val

    def _splitPortAndHost(self, host):
        port = constants.DEFAULT_PORT if not self._config["port"] else self._config["port"]
        if host:
            if ':' in host:
                if host.count(':') == 1:
                    #IPv4 address or hostname, with port
                    host, port = host.rsplit(':', 1)
                    try:
                        port = int(port)
                    except ValueError:
                        try:
                            port = port.encode('ascii', 'ignore')
                        except:
                            port = ""
                else:
                    #IPv6 address
                    if ']' in host:
                        #IPv6 address in brackets
                        endBracket = host.index(']')
                        try:
                            #port explicitely indicated
                            port = int(host[endBracket+2:])
                        except ValueError:
                            #no port after the bracket
                            pass
                        host = host[:endBracket+1]
                    else:
                        #IPv6 address with no port and no brackets
                        #add brackets to correctly store IPv6 addresses in configs
                        host = '[' + host + ']'
        return host, port

    def _checkForPortableFile(self):
        path = utils.findWorkingDir()
        for name in constants.CONFIG_NAMES:
            if os.path.isfile(os.path.join(path, name)):
                return os.path.join(path, name)

    def _getConfigurationFilePath(self):
        configFile = self._checkForPortableFile()
        if configFile:
            return configFile
        for name in constants.CONFIG_NAMES:
            configFile = self._expandConfigPath(name, xdg=False)
            if os.path.isfile(configFile):
                return configFile
        return self._expandConfigPath()

    def _expandConfigPath(self, name=None, xdg=True):
        if os.name != 'nt':
            if xdg:
                prefix = self._getXdgConfigHome()
            else:
                prefix = os.getenv('HOME', '.')
        else:
            prefix = os.getenv('APPDATA', '.')
        return os.path.join(prefix, name or constants.DEFAULT_CONFIG_NAME)

    def _getXdgConfigHome(self):
        path = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
        if not os.path.isdir(path):
            os.mkdir(path, 0o700)
        return path

    def _parseConfigFile(self, iniPath, createConfig=True):
        parser = SafeConfigParserUnicode(strict=False)
        if not os.path.isfile(iniPath):
            if createConfig:
                open(iniPath, 'w').close()
            else:
                return
        parser.readfp(codecs.open(iniPath, "r", "utf_8_sig"))
        for section, options in list(self._iniStructure.items()):
            if parser.has_section(section):
                for option in options:
                    if parser.has_option(section, option):
                        self._config[option] = parser.get(section, option)

    def _checkConfig(self):
        try:
            self._validateArguments()
        except InvalidConfigValue as e:
            try:
                for key, value in list(self._promptForMissingArguments(e).items()):
                    self._config[key] = value
                self._checkConfig()
            except:
                sys.exit()

    def _promptForMissingArguments(self, error=None):
        if self._config['noGui']:
            if error:
                print("{}!".format(error))
            print(getMessage("missing-arguments-error"))
            sys.exit()
        else:
            from syncplay.ui.GuiConfiguration import GuiConfiguration
            gc = GuiConfiguration(self._config, error=error)
            gc.setAvailablePaths(self._playerFactory.getAvailablePlayerPaths())
            gc.run()
            return gc.getProcessedConfiguration()

    def __wasOptionChanged(self, parser, section, option):
        if parser.has_option(section, option):
            if parser.get(section, option) != str(self._config[option]):
                return True
        else:
            return True

    def _saveConfig(self, iniPath):
        changed = False
        if self._config['noStore']:
            return
        parser = SafeConfigParserUnicode(strict=False)
        parser.readfp(codecs.open(iniPath, "r", "utf_8_sig"))
        for section, options in list(self._iniStructure.items()):
            if not parser.has_section(section):
                parser.add_section(section)
                changed = True
            for option in options:
                if self.__wasOptionChanged(parser, section, option):
                    changed = True
                parser.set(section, option, str(self._config[option]).replace('%', '%%'))
        if changed:
            parser.write(codecs.open(iniPath, "wb", "utf_8_sig"))

    def _forceGuiPrompt(self):
        from syncplay.ui.GuiConfiguration import GuiConfiguration
        try:
            self._validateArguments()
        except InvalidConfigValue:
            pass

        try:
            for key, value in list(self._promptForMissingArguments().items()):
                self._config[key] = value
        except GuiConfiguration.WindowClosed:
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
                if os.path.isfile(path) and (os.name == 'nt' or path != os.path.join(os.getenv('HOME', '.'), name)):
                    loadedPaths.append("'{}'".format(os.path.normpath(path)))
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
        self._argparser = argparse.ArgumentParser(
            description=getMessage("argument-description"),
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
        self._argparser.add_argument('-psn', metavar='blackhole', type=str, help=argparse.SUPPRESS)
        self._argparser.add_argument('--language', metavar='language', type=str, help=getMessage("language-argument"))
        self._argparser.add_argument('file', metavar='file', type=str, nargs='?', help=getMessage("file-argument"))
        self._argparser.add_argument('--clear-gui-data', action='store_true', help=getMessage("clear-gui-data-argument"))
        self._argparser.add_argument('-v', '--version', action='store_true', help=getMessage("version-argument"))
        self._argparser.add_argument('--load-playlist-from-file', metavar="loadPlaylistFromFile", type=str, help=getMessage("load-playlist-from-file-argument"))

        self._argparser.add_argument('_args', metavar='options', type=str, nargs='*', help=getMessage("args-argument"))
        args = self._argparser.parse_args()
        if args.version:
            print(getMessage("version-message").format(version, milestone))
            sys.exit()
        self._overrideConfigWithArgs(args)
        if not self._config['noGui']:
            try:
                from syncplay.vendor.Qt import QtWidgets, IsPySide, IsPySide2, IsPySide6, QtGui
                from syncplay.vendor.Qt.QtCore import QCoreApplication
                from syncplay.vendor import qt5reactor
                if not (IsPySide6 or IsPySide2 or IsPySide):
                    raise ImportError
                if QCoreApplication.instance() is None:
                    self.app = QtWidgets.QApplication(sys.argv)
                    if isWindows():
                        try:
                            from syncplay.vendor import darkdetect
                            isDarkMode = darkdetect.isDark()
                        except:
                            isDarkMode = False
                        if isDarkMode:
                            self.app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
                            self.app.setPalette(self.getDarkPalette(QtGui))
                qt5reactor.install()
                if isMacOS():
                    import appnope
                    appnope.nope()
            except ImportError:
                try:
                    from twisted.trial import unittest
                except Exception as e:
                    print(e)
                    print(getMessage("unable-import-twisted-error"))
                    sys.exit()
                print(getMessage("unable-import-gui-error"))
                self._config['noGui'] = True
        if self._config['file'] and self._config['file'][:2] == "--":
            self._config['playerArgs'].insert(0, self._config['file'])
            self._config['file'] = None
        # Arguments not validated yet - booleans are still text values
        if self._config['language']:
            setLanguage(self._config['language'])
        if (self._config['forceGuiPrompt'] == "True" or not self._config['file']) and not self._config['noGui']:
            self._forceGuiPrompt()
        self._checkConfig()
        self._saveConfig(iniPath)
        if self._config['file']:
            self._config['loadedRelativePaths'] = self._loadRelativeConfiguration()
        if self._config['language']:
            setLanguage(self._config['language'])
        return self._config

    def getDarkPalette(self, QtGui):
        # Based on https://gist.github.com/lschmierer/443b8e21ad93e2a2d7eb#gistcomment-3503395
        darkPalette = QtGui.QPalette()
        darkPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        darkPalette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
        darkPalette.setColor(QtGui.QPalette.Base, QtGui.QColor(35, 35, 35))
        darkPalette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        darkPalette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(25, 25, 25))
        darkPalette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(255, 255, 255))
        darkPalette.setColor(QtGui.QPalette.Text, QtGui.QColor(255, 255, 255))
        darkPalette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        darkPalette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255, 255, 255))
        darkPalette.setColor(QtGui.QPalette.BrightText, QtGui.QColor(255, 0, 0))
        darkPalette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
        darkPalette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
        darkPalette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(35, 35, 35))
        darkPalette.setColor(QtGui.QPalette.Active, QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        darkPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, QtGui.QColor(128, 128, 128))
        darkPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtGui.QColor(128, 128, 128))
        darkPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Text, QtGui.QColor(128, 128, 128))
        darkPalette.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, QtGui.QColor(53, 53, 53))
        return darkPalette

    def setConfigOption(self, option, value):
        path = self._getConfigurationFilePath()
        backup = self._config.copy()
        self._parseConfigFile(path)
        self._config[option] = value
        backup[option] = value
        self._saveConfig(path)
        self._config = backup


class SafeConfigParserUnicode(SafeConfigParser):
    def write(self, fp):
        """Write an .ini-format representation of the configuration state."""
        if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in list(self._defaults.items()):
                fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in list(self._sections[section].items()):
                if key == "__name__":
                    continue
                if (value is not None) or (self._optcre == self.OPTCRE):
                    key = " = ".join((key, str(value).replace('\n', '\n\t')))
                fp.write("%s\n" % key)
            fp.write("\n")
