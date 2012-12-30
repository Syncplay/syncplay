from ConfigParser import SafeConfigParser
import argparse
import os
import sys
from syncplay import constants
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
                        "room": constants.DEFAULT_ROOM,
                        "password": None,
                        "playerPath": None,
                        "file": None,
                        "playerArgs": [],
                        "playerType": None,
                        }
        
        #
        #Custom validation in self._validateArguments
        #
        self._required = [
                          "host",
                          "port",
                          "name",
                          "playerPath",
                          "playerType",
                         ]

        self._iniStructure = {
                        "server_data": ["host", "port", "password"],
                        "client_settings": ["name", "room", "playerPath"]
                        }

        #
        #Watch out for the method self._overrideConfigWithArgs when you're adding custom multi-word command line arguments
        #
        self._argparser = argparse.ArgumentParser(description='Solution to synchronize playback of multiple MPlayer and MPC-HC instances over the network.',
                                         epilog='If no options supplied values from configuration file will be used')
        self._argparser.add_argument('--no-gui', action='store_true', help='show no GUI')
        self._argparser.add_argument('-a', '--host', metavar='hostname', type=str, help='server\'s address')
        self._argparser.add_argument('-n', '--name', metavar='username', type=str, help='desired username')
        self._argparser.add_argument('-d', '--debug', action='store_true', help='debug mode')
        self._argparser.add_argument('-g', '--force-gui-prompt', action='store_true', help='make configuration prompt appear')
        self._argparser.add_argument('--no-store', action='store_true', help='don\'t store values in .syncplay')
        self._argparser.add_argument('-r', '--room', metavar='room', type=str, nargs='?', help='default room')
        self._argparser.add_argument('-p', '--password', metavar='password', type=str, nargs='?', help='server password')
        self._argparser.add_argument('--player-path', metavar='path', type=str, help='path to your player executable')
        self._argparser.add_argument('file', metavar='file', type=str, nargs='?', help='file to play')
        self._argparser.add_argument('_args', metavar='options', type=str, nargs='*', help='player options, if you need to pass options starting with - prepend them with single \'--\' argument') 
  
    def _validateArguments(self):
        for key in self._required:
            if(key == "playerPath"):
                if(self._isPlayerMPCAndValid(self._config["playerPath"])):
                    self._config["playerType"] = "mpc"
                    self.__addSpecialMPCFlags()
                elif(self._isMplayerPathAndValid(self._config["playerPath"])):
                    self._config["playerType"] = "mplayer"
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
            
    def _isPlayerMPCAndValid(self, path):
        if(os.path.isfile(path)):
            if(path[-10:] == 'mpc-hc.exe' or path[-12:] == 'mpc-hc64.exe'):
                return True
        if(os.path.isfile(path + "\\mpc-hc.exe")):
            path += "\\mpc-hc.exe"
            return True
        if(os.path.isfile(path + "\\mpc-hc64.exe")):
            path += "\\mpc-hc64.exe"
            return True
        return False

    def __addSpecialMPCFlags(self):
        self._config['playerArgs'].extend(['/open', '/new'])

    def _isMplayerPathAndValid(self, playerPath):
        if("mplayer" in playerPath):
            if os.access(playerPath, os.X_OK):
                return True
            for path in os.environ['PATH'].split(':'):
                path = os.path.join(os.path.realpath(path), playerPath)
                if os.access(path, os.X_OK):
                    self._config['playerPath'] = path
                    return True
        return False
    
    def _splitPortAndHost(self, host):
        port = constants.DEFAULT_PORT if not self._config["port"] else self._config["port"]
        if(host):
            if ':' in host:
                host, port = host.split(':', 1)
        return host, int(port)
        
    def _findWorkingDir(self):
        frozen = getattr(sys, 'frozen', '')
        if not frozen:
            path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        elif frozen in ('dll', 'console_exe', 'windows_exe'):
            path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        else:
            path = ""
        return path

    def _checkForPortableFile(self):
        path = self._findWorkingDir()
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
        parser.read(iniPath)
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
            print "Some necessary arguments are missing, refer to --help"
            sys.exit()
        elif(GuiConfiguration):
            return GuiConfiguration(self._config).getProcessedConfiguration()

    def _saveConfig(self, iniPath):
        if(self._config['noStore']):
            return
        parser = SafeConfigParser()
        for section, options in self._iniStructure.items():
            if(not parser.has_section(section)):
                parser.add_section(section)
            for option in options:
                parser.set(section, option, str(self._config[option]))
        parser.write(file(iniPath, "w"))
        
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
        self._argparser = argparse.ArgumentParser(description='Solution to synchronize playback of multiple MPlayer and MPC-HC instances over the network. Server instance',
                                         epilog='If no options supplied _config values will be used')
        self._argparser.add_argument('--port', metavar='port', type=str, nargs='?', help='server TCP port')
        self._argparser.add_argument('--password', metavar='password', type=str, nargs='?', help='server password')
        self._argparser.add_argument('--isolate-rooms', action='store_true', help='should rooms be isolated?')
