from ConfigParser import SafeConfigParser
import argparse
import os
import sys
from syncplay import constants, utils
from syncplay.messages import getMessage
from syncplay.players.playerFactory import PlayerFactory
import codecs
try: 
    from syncplay.ui.GuiConfiguration import GuiConfiguration
except ImportError:
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
                        "forceGuiPrompt": False,
                        "noGui": False,
                        "noStore": False,
                        "room": "",
                        "password": None,
                        "playerPath": None,
                        "file": None,
                        "playerArgs": [],
                        "playerClass": None,
						"slowOnDesync": True
                        }
        
        #
        #Custom validation in self._validateArguments
        #
        self._required = [
                          "host",
                          "port",
                          "name",
                          "playerPath",
                          "playerClass",
                         ]

        self._iniStructure = {
                        "server_data": ["host", "port", "password"],
                        "client_settings": ["name", "room", "playerPath"]
                        }

        #
        #Watch out for the method self._overrideConfigWithArgs when you're adding custom multi-word command line arguments
        #
        self._argparser = argparse.ArgumentParser(description=getMessage("en", "argument-description"),
                                         epilog=getMessage("en", "argument-epilog"))
        self._argparser.add_argument('--no-gui', action='store_true', help=getMessage("en", "nogui-argument"))
        self._argparser.add_argument('-a', '--host', metavar='hostname', type=str, help=getMessage("en", "host-argument"))
        self._argparser.add_argument('-n', '--name', metavar='username', type=str, help=getMessage("en", "name-argument"))
        self._argparser.add_argument('-d', '--debug', action='store_true', help=getMessage("en", "debug-argument"))
        self._argparser.add_argument('-g', '--force-gui-prompt', action='store_true', help=getMessage("en", "force-gui-prompt-argument"))
        self._argparser.add_argument('--no-store', action='store_true', help=getMessage("en", "no-store-argument"))
        self._argparser.add_argument('-r', '--room', metavar='room', type=str, nargs='?', help=getMessage("en", "room-argument"))
        self._argparser.add_argument('-p', '--password', metavar='password', type=str, nargs='?', help=getMessage("en", "password-argument"))
        self._argparser.add_argument('--player-path', metavar='path', type=str, help=getMessage("en", "player-path-argument"))
        self._argparser.add_argument('file', metavar='file', type=str, nargs='?', help=getMessage("en", "file-argument"))
        self._argparser.add_argument('_args', metavar='options', type=str, nargs='*', help=getMessage("en", "args-argument"))
  
  
        self._playerFactory = PlayerFactory()
        
    def _validateArguments(self):
        for key in self._required:
            if(key == "playerPath"):
                player = self._playerFactory.getPlayerByPath(self._config["playerPath"])
                if(player):
                    self._config["playerClass"] = player
                else:
                    raise InvalidConfigValue("Player path is not set properly")
            elif(key == "host"):
                self._config["host"], self._config["port"] = self._splitPortAndHost(self._config["host"])
                hostNotValid = (self._config["host"] == "" or self._config["host"] is None)
                portNotValid = (self._config["port"] == "" or self._config["port"] is None)
                if(hostNotValid or portNotValid):
                    raise InvalidConfigValue("Hostname can't be empty")
            elif(self._config[key] == "" or self._config[key] is None):
                raise InvalidConfigValue("{} can't be empty".format(key))
    
    def _overrideConfigWithArgs(self, args):
        for key, val in vars(args).items():
            if(val):
                if(key == "force_gui_prompt"):
                    key = "forceGuiPrompt"
                if(key == "no_store"):
                    key = "noStore"
                if(key == "player_path"):
                    key = "playerPath"
                if(key == "_args"):
                    key = "playerArgs"
                if(key == "no_gui"):
                    key = "noGui"
                self._config[key] = val
            
    def _splitPortAndHost(self, host):
        port = constants.DEFAULT_PORT if not self._config["port"] else self._config["port"]
        if(host):
            if ':' in host:
                host, port = host.split(':', 1)
        return host, int(port)
        
    def _checkForPortableFile(self):
        path = utils.findWorkingDir()
        if(os.path.isfile(os.path.join(path, constants.DEFAULT_CONFIG_NAME))):
            return os.path.join(path, constants.DEFAULT_CONFIG_NAME) 
        
    def _getConfigurationFilePath(self):
        configFile = self._checkForPortableFile()
        if(not configFile):
            if(os.name <> 'nt'):
                configFile = os.path.join(os.getenv('HOME', '.'), constants.DEFAULT_CONFIG_NAME)
            else:
                configFile = os.path.join(os.getenv('APPDATA', '.'), constants.DEFAULT_CONFIG_NAME)
        return configFile

    def _parseConfigFile(self, iniPath):
        parser = SafeConfigParser()
        if(not os.path.isfile(iniPath)):
            open(iniPath, 'w').close()
        parser.readfp(codecs.open(iniPath, "r", "utf_8_sig"))
        for section, options in self._iniStructure.items():
            if(parser.has_section(section)):
                for option in options:
                    if(parser.has_option(section, option)):
                        self._config[option] = parser.get(section, option)
        
    def _checkConfig(self):
        try:
            self._validateArguments()
        except InvalidConfigValue:
            try:
                for key, value in self._promptForMissingArguments().items():
                    self._config[key] = value
                self._checkConfig()
            except:
                sys.exit()

    def _promptForMissingArguments(self):
        if(self._config['noGui']):
            print getMessage("en", "missing-arguments-error")
            sys.exit()
        elif(GuiConfiguration):
            gc = GuiConfiguration(self._config)
            gc.setAvailablePaths(self._playerFactory.getAvailablePlayerPaths())
            gc.run()
            return gc.getProcessedConfiguration()

    def __wasOptionChanged(self, parser, section, option):
        if (parser.has_option(section, option)):
            if (parser.get(section, option) != str(self._config[option])):
                return True
        else:
            return True

    def _saveConfig(self, iniPath):
        changed = False
        if(self._config['noStore']):
            return
        parser = SafeConfigParser()
        parser.readfp(codecs.open(iniPath, "r", "utf_8_sig"))
        for section, options in self._iniStructure.items():
            if(not parser.has_section(section)):
                parser.add_section(section)
                changed = True
            for option in options:
                if(self.__wasOptionChanged(parser, section, option)):
                    changed = True
                parser.set(section, option, str(self._config[option]))
        if(changed):
            parser.write(codecs.open(iniPath, "wb", "utf_8_sig"))
        
    def getConfiguration(self):
        iniPath = self._getConfigurationFilePath()
        self._parseConfigFile(iniPath)
        args = self._argparser.parse_args()
        self._overrideConfigWithArgs(args)
        if(self._config['forceGuiPrompt']):
            try:
                self._promptForMissingArguments()
            except:
                sys.exit()
        self._checkConfig()
        self._saveConfig(iniPath)
        return self._config
    
class ServerConfigurationGetter(object):
    def getConfiguration(self):
        self._prepareArgParser()
        self._args = self._argparser.parse_args()
        if(self._args.port == None):
            self._args.port = constants.DEFAULT_PORT
        return self._args
           
    def _prepareArgParser(self):
        self._argparser = argparse.ArgumentParser(description=getMessage("en", "server-argument-description"),
                                         epilog=getMessage("en", "server-argument-epilog"))
        self._argparser.add_argument('--port', metavar='port', type=str, nargs='?', help=getMessage("en", "server-port-argument"))
        self._argparser.add_argument('--password', metavar='password', type=str, nargs='?', help=getMessage("en", "server-password-argument"))
        self._argparser.add_argument('--isolate-rooms', action='store_true', help=getMessage("en", "server-isolate-room-argument"))
        self._argparser.add_argument('--motd-file', metavar='file', type=str, nargs='?', help=getMessage("en", "server-motd-argument"))
        self._argparser.add_argument('--http-reply-file', metavar='file', type=str, nargs='?', help=getMessage("en", "server-http-reply-argument"))
        self._argparser.add_argument('--irc-verbose', action='store_true', help=getMessage("en", "server-irc-verbose"))
        self._argparser.add_argument('--irc-config-file', metavar='file', type=str, nargs='?', help=getMessage("en", "server-irc-config"))
