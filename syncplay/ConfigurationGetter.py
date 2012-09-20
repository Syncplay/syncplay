import ConfigParser
import argparse
import os

class InvalidConfigValue(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)
        
class ConfigurationGetter(object):
    def __init__(self):
        self._config = None
        self._args = None
        self._syncplayClient = None
        self._workingDir = None
        self._parser = None
        
    def _getConfigurationFilePath(self):
        if(os.name <> 'nt'):
            self._workingDir = os.getenv('HOME', '.')
        else:
            self._workingDir = os.getenv('APPDATA', '.')

    def _prepareArgParser(self):
        self._parser = argparse.ArgumentParser(description='Solution to synchronize playback of multiple MPlayer and MPC-HC instances over the network.',
                                         epilog='If no options supplied _config values will be used')
        self._parser.add_argument('--no-gui', action='store_true', help='show no GUI')
        self._parser.add_argument('--host', metavar='hostname', type=str, help='server\'s address')
        self._parser.add_argument('--name', metavar='username', type=str, help='desired username')
        self._parser.add_argument('-d','--debug', action='store_true', help='debug mode')
        self._parser.add_argument('--no-store', action='store_true', help='don\'t store values in syncplay.ini')
        self._parser.add_argument('--room', metavar='room', type=str, nargs='?', help='default room')
        self._parser.add_argument('--password', metavar='password', type=str, nargs='?', help='server password')
        self._parser.add_argument('file', metavar='file', type=str, nargs='?', help='file to play')
        self._parser.add_argument('_args', metavar='options', type=str, nargs='*', help='player options, if you need to pass options starting with - prepend them with single \'--\' argument') 
  
    def _openConfigFile(self):
        if(not self._config):
            self._config = ConfigParser.RawConfigParser(allow_no_value=True)
            self._config.read(os.path.join(self._workingDir, '.syncplay'))      
    
    def _getSectionName(self):
        return 'sync' if not self._args.debug else 'debug'

    def saveValuesIntoConfigFile(self):
        self._splitPortAndHost()
        self._openConfigFile()
        section_name = self._getSectionName()
        if(not self._args.no_store):
            with open(os.path.join(self._workingDir, '.syncplay'), 'wb') as configfile:
                if(not self._config.has_section(section_name)):
                    self._config.add_section(section_name)
                self._setUpValuesToSave(section_name)
                self._config.write(configfile)
    
    def _setUpValuesToSave(self, section_name):
        if(self._args.host <> "" and self._args.host is not None):
            self._config.set(section_name, 'host', self._args.host)
        else:
            self._args.host = None
            raise InvalidConfigValue("Hostname can't be empty")
        if(self._args.name <> "" and self._args.name is not None):
            self._config.set(section_name, 'name', self._args.name)
        else:
            self._args.name = None
            raise InvalidConfigValue("Username can't be empty")         
        self._config.set(section_name, 'room', self._args.room)
        self._config.set(section_name, 'password', self._args.password)

        
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

    
    def _valuesToReadFromConfig(self, section_name):
        if (self._args.host == None):
            self._args.host = self._readConfigValue(section_name, 'host')
        if (self._args.name == None):
            self._args.name = self._readConfigValue(section_name, 'name')
        if (self._args.room == None):
            self._args.room = self._readConfigValue(section_name, 'room')
        if (self._args.password == None):
            self._args.password = self._readConfigValue(section_name, 'password')  
              
    def _splitPortAndHost(self):
        if(self._args.host):
            if ':' in self._args.host:
                self._args.host, port = self._args.host.split(':', 1)
                self._args.port = int(port)
            else:
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
    
class MPCConfigurationGetter(ConfigurationGetter):
    def _prepareArgParser(self):
        ConfigurationGetter._prepareArgParser(self)
        self._parser.add_argument('--mpc-path', metavar='path', type=str, help='path to mpc-hc.exe (only for sync_mpc_api client)')

    def _setUpValuesToSave(self, section_name):
        ConfigurationGetter._setUpValuesToSave(self, section_name)
        if(not self.mpc_pathValid()):
            self._args.mpc_path = None
            raise InvalidConfigValue('Path to mpc is not valid')
        self._config.set(section_name, 'mpc_path', self._args.mpc_path)
    
    def mpc_pathValid(self):
        if(os.path.isfile(self._args.mpc_path)):
            if(self._args.mpc_path[-10:] == 'mpc-hc.exe' or self._args.mpc_path[-12:] == 'mpc-hc64.exe'):
                return True
        return False

    def _valuesToReadFromConfig(self, section_name):
        ConfigurationGetter._valuesToReadFromConfig(self, section_name)
        if (self._args.mpc_path == None):
            self._args.mpc_path = self._readConfigValue(section_name, 'mpc_path')

    def __addSpecialMPCFlags(self):
        self._args._args.extend(['/open', '/new'])

    def getConfiguration(self):
        ConfigurationGetter.getConfiguration(self)
        self.__addSpecialMPCFlags()
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
