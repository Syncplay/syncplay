#coding:utf8

import ConfigParser
import argparse
import os
import re
import sys
import itertools

class ArgumentParser():
    RE_ARG = re.compile(r"('(?:[^\\']+|\\\\|\\')*'|[^\s']+)(?:\s+|\Z)")
    RE_NEED_QUOTING = re.compile(r"[\s'\\]")
    RE_QUOTABLE = re.compile(r"['\\]")
    RE_UNQUOTABLE = re.compile(r"\\(['\\])")
    
    class InvalidArgumentException(Exception):
        pass
    
    @staticmethod
    def quoteArgument(arg):
        if isinstance(arg, unicode):
            arg = arg.encode('utf8')
        elif not isinstance(arg, str):
            arg = str(arg)
    
        if not arg or ArgumentParser.RE_NEED_QUOTING.search(arg):
            return "'%s'" % ArgumentParser.RE_QUOTABLE.sub(r'\\\g<0>', arg)
        return arg
    
    @staticmethod
    def unqoteArgument(arg):
        if arg.startswith("'") and len(arg) > 1:
            arg = ArgumentParser.RE_UNQUOTABLE.sub(r'\1', arg[1:-1])
        return arg.decode('utf8', 'replace')
    
    @staticmethod
    def __splitArguments(args):
        pos = 0
        while pos < len(args):
            match = ArgumentParser.RE_ARG.match(args, pos)
            if not match:
                raise ArgumentParser.InvalidArgumentException()
            pos = match.end()
            yield ArgumentParser.unqoteArgument(match.group(1))
            
    @staticmethod
    def splitArguments(args):
        try:
            return list(ArgumentParser.__splitArguments(args))
        except ArgumentParser.InvalidArgumentException:
            return None
        
    @staticmethod
    def joinArguments(args):
        args = list(itertools.ifilterfalse(lambda x: None == x, args))
        return ' '.join(ArgumentParser.quoteArgument(arg) for arg in args)
    
def find_exec_path(name):
    if os.access(name, os.X_OK):
        return name
    for path in os.environ['PATH'].split(':'):
        path = os.path.join(os.path.realpath(path), name)
        if os.access(path, os.X_OK):
            return path

def format_time(value):
    value = int(value*100)
    seconds, mseconds = divmod(value, 100)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return '%02d:%02d:%02d.%02d' % (hours, minutes, seconds, mseconds)

def stdin_thread(manager):
    try:
        fd = sys.stdin.fileno()
        while True:
            data = os.read(fd, 1024)
            if not data:
                break   
            manager.executeCommand(data.rstrip('\n\r'))
    except:
        pass

class ConfigurationGetter(object):
    def __init__(self):
        self._config = None
        self._args = None
        self._syncplayClient = None
        self._workingDir = None
        self._parser = None
        
    def _findWorkingDirectory(self):
        frozen = getattr(sys, 'frozen', '')
        if not frozen:
            self._workingDir = os.path.dirname(os.path.dirname(__file__))
        elif frozen in ('dll', 'console_exe', 'windows_exe'):
            self._workingDir = os.path.dirname(sys.executable)
        else:
            raise Exception('Working dir not found')

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
            self._config.read(os.path.join(self._workingDir, 'syncplay.ini'))      
    
    def _getSectionName(self):
        return 'sync' if not self._args.debug else 'debug'

    def saveValuesIntoConfigFile(self):
        self._openConfigFile()
        section_name = self._getSectionName()
        if(not self._args.no_store):
            with open(os.path.join(self._workingDir, 'syncplay.ini'), 'wb') as configfile:
                if(not self._config.has_section(section_name)):
                    self._config.add_section(section_name)
                self._setUpValuesToSave(section_name)
                self._config.write(configfile)
    
    def _setUpValuesToSave(self, section_name):
        self._splitPortAndHost()
        self._config.set(section_name, 'host', self._args.host)
        self._config.set(section_name, 'name', self._args.name)
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
    
    def getConfiguration(self):
        self._findWorkingDirectory()
        self._prepareArgParser()
        self._args = self._parser.parse_args()
        self._readMissingValuesFromConfigFile()
        self.saveValuesIntoConfigFile()
        self._splitPortAndHost()
        return self._args

    
class MPCConfigurationGetter(ConfigurationGetter):
    def _prepareArgParser(self):
        ConfigurationGetter._prepareArgParser(self)
        self._parser.add_argument('--mpc-path', metavar='path', type=str, help='path to mpc-hc.exe (only for sync_mpc_api client)')

    def _setUpValuesToSave(self, section_name):
        ConfigurationGetter._setUpValuesToSave(self, section_name)
        self._config.set(section_name, 'mpc_path', self._args.mpc_path)

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
        return self._args
           
    def _prepareArgParser(self):
        self._parser = argparse.ArgumentParser(description='Solution to synchronize playback of multiple MPlayer and MPC-HC instances over the network. Server instance',
                                         epilog='If no options supplied _config values will be used')
        self._parser.add_argument('--password', metavar='password', type=str, nargs='?', help='server password')
        self._parser.add_argument('--banlist', metavar='banlist', type=str, nargs='?', help='server banlist file')
        self._parser.add_argument('--isolate-rooms', action='store_true', help='should rooms be isolated?')
        
    