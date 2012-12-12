import ConfigParser
import argparse
import os
import sys

class InvalidConfigValue(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        
class ConfigurationGetter(object):
    def __init__(self):
        self._config = None
        self._args = None
        self._syncplayClient = None
        self._configFile = None
        self._parser = None
        self._configName = ".syncplay"
        self.playerType = None

    def _findWorkingDir(self):
        frozen = getattr(sys, 'frozen', '')
        if not frozen:
            path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        elif frozen in ('dll', 'console_exe', 'windows_exe'):
            path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        else:
            path = ""
        return path

    def _checkForPortableFile(self):
        path = self._findWorkingDir()
        if(os.path.isfile(os.path.join(path, self._configName))):
            return os.path.join(path, self._configName) 
        
    def _getConfigurationFilePath(self):
        self._configFile = self._checkForPortableFile()
        if(not self._configFile):
            if(os.name <> 'nt'):
                self._configFile = os.path.join(os.getenv('HOME', '.'), self._configName)
            else:
                self._configFile = os.path.join(os.getenv('APPDATA', '.'), self._configName)

    def _prepareArgParser(self):
        self._parser = argparse.ArgumentParser(description='Solution to synchronize playback of multiple MPlayer and MPC-HC instances over the network.',
                                         epilog='If no options supplied values from .syncplay file will be used')
        self._parser.add_argument('--no-gui', action='store_true', help='show no GUI')
        self._parser.add_argument('-a', '--host', metavar='hostname', type=str, help='server\'s address')
        self._parser.add_argument('-n', '--name', metavar='username', type=str, help='desired username')
        self._parser.add_argument('-d', '--debug', action='store_true', help='debug mode')
        self._parser.add_argument('-g', '--force-gui-prompt', action='store_true', help='make configuration prompt appear')
        self._parser.add_argument('--no-store', action='store_true', help='don\'t store values in syncplay.ini')
        self._parser.add_argument('-r', '--room', metavar='room', type=str, nargs='?', help='default room')
        self._parser.add_argument('-p', '--password', metavar='password', type=str, nargs='?', help='server password')
        self._parser.add_argument('--player-path', metavar='path', type=str, help='path to your player executable')
        self._parser.add_argument('file', metavar='file', type=str, nargs='?', help='file to play')
        self._parser.add_argument('_args', metavar='options', type=str, nargs='*', help='player options, if you need to pass options starting with - prepend them with single \'--\' argument') 
  
    def _openConfigFile(self):
        if(not self._config):
            self._config = ConfigParser.RawConfigParser(allow_no_value=True)
            self._config.read(self._configFile)      
    
    def _getSectionName(self):
        return 'sync' if not self._args.debug else 'debug'

    def saveValuesIntoConfigFile(self):
        self._splitPortAndHost()
        self._openConfigFile()
        section_name = self._getSectionName()
        self._validateArguments()
        if(not self._args.no_store):
            with open(self._configFile, 'wb') as configfile:
                if(not self._config.has_section(section_name)):
                    self._config.add_section(section_name)
                self._config.set(section_name, 'host', self._args.host+":"+str(self._args.port))
                self._config.set(section_name, 'name', self._args.name)       
                self._config.set(section_name, 'room', self._args.room)
                self._config.set(section_name, 'password', self._args.password)
                self._config.set(section_name, 'player_path', self._args.player_path)
                self._config.write(configfile)
    
    def _validateArguments(self):
        if(not (self._args.host <> "" and self._args.host is not None)):
            self._args.host = None
            raise InvalidConfigValue("Hostname can't be empty")
        if(not (self._args.name <> "" and self._args.name is not None)):
            self._args.name = None
            raise InvalidConfigValue("Username can't be empty")  
        if(self._isPlayerMPCAndValid()):
            self._addSpecialMPCFlags()
            self.playerType = "mpc"
        elif(self._isMplayerPathValid()):
            self.playerType = "mplayer"
        else:
            self._args.player_path = None
            raise InvalidConfigValue('Path to player is not valid')
        
    def _readConfigValue(self, section_name, name):
        try:
            return self._config.get(section_name, name)
        except ConfigParser.NoOptionError:
            return None 
        
    def _readMissingValuesFromConfigFile(self):
        self._openConfigFile()
        section_name = self._getSectionName()
        try:
            self._valuesToReadFromConfig(section_name)
        except ConfigParser.NoSectionError:
            pass

    def _isPlayerMPCAndValid(self):
        if(os.path.isfile(self._args.player_path)):
            if(self._args.player_path[-10:] == 'mpc-hc.exe' or self._args.player_path[-12:] == 'mpc-hc64.exe'):
                return True
        if(os.path.isfile(self._args.player_path + "\\mpc-hc.exe")):
            self._args.player_path += "\\mpc-hc.exe"
            return True
        if(os.path.isfile(self._args.player_path + "\\mpc-hc64.exe")):
            self._args.player_path += "\\mpc-hc64.exe"
            return True
        return False

    def _addSpecialMPCFlags(self):
        self._args._args.extend(['/open', '/new'])

    def _isMplayerPathValid(self):
        if("mplayer" in self._args.player_path):
            if os.access(self._args.player_path, os.X_OK):
                return True
            for path in os.environ['PATH'].split(':'):
                path = os.path.join(os.path.realpath(path), self._args.player_path)
                if os.access(path, os.X_OK):
                    self._args.player_path = path
                    return True
        return False
    
    def _valuesToReadFromConfig(self, section_name):
        if (self._args.host == None):
            self._args.host = self._readConfigValue(section_name, 'host')
        if (self._args.name == None):
            self._args.name = self._readConfigValue(section_name, 'name')
        if (self._args.room == None):
            self._args.room = self._readConfigValue(section_name, 'room')
        if (self._args.password == None):
            self._args.password = self._readConfigValue(section_name, 'password')  
        if (self._args.player_path == None):
            self._args.player_path = self._readConfigValue(section_name, 'player_path')
              
    def _splitPortAndHost(self):
        if(self._args.host):
            if ':' in self._args.host:
                self._args.host, port = self._args.host.split(':', 1)
                self._args.port = int(port)
            elif("port" not in self._args):
                self._args.port = 8999
    
    def setConfiguration(self, args):
        self._args = args
        
    def getConfiguration(self):
        self._getConfigurationFilePath()
        self._prepareArgParser()
        self._args = self._parser.parse_args()
        self._readMissingValuesFromConfigFile()
        self._splitPortAndHost()
        return self._args
    
class ServerConfigurationGetter(ConfigurationGetter):
    def getConfiguration(self):
        self._prepareArgParser()
        self._args = self._parser.parse_args()
        if(self._args.port == None):
            self._args.port = 8999
        return self._args
           
    def _prepareArgParser(self):
        self._parser = argparse.ArgumentParser(description='Solution to synchronize playback of multiple MPlayer and MPC-HC instances over the network. Server instance',
                                         epilog='If no options supplied _config values will be used')
        self._parser.add_argument('--port', metavar='port', type=str, nargs='?', help='server TCP port')
        self._parser.add_argument('--password', metavar='password', type=str, nargs='?', help='server password')
        self._parser.add_argument('--isolate-rooms', action='store_true', help='should rooms be isolated?')
