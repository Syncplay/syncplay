from syncplay.client import SyncplayClient
import sys
from syncplay.ui.ConfigurationGetter import ConfigurationGetter, InvalidConfigValue
from syncplay import ui
try:
    from syncplay.players.mpc import MPCHCAPIPlayer
except ImportError:
    MPCHCAPIPlayer = None
from syncplay.players.mplayer import MplayerPlayer
try: 
    from syncplay.ui.GuiConfiguration import GuiConfiguration
except ImportError:
    GuiConfiguration = None

class SyncplayClientManager(object):
    def __init__(self):
        self._prepareArguments()
        self.interface = ui.getUi(graphical=not self.args.no_gui)
        self._checkAndSaveConfiguration()
        syncplayClient = None
        if(self.argsGetter.playerType == "mpc"):
            syncplayClient = SyncplayClient(MPCHCAPIPlayer, self.interface, self.args)
        elif(self.argsGetter.playerType == "mplayer"):
            syncplayClient = SyncplayClient(MplayerPlayer, self.interface, self.args)
        if(syncplayClient):
            self.interface.addClient(syncplayClient)
            syncplayClient.start(self.args.host, self.args.port)
        else:
            self.interface.showErrorMessage("Unable to start client")
        
    def _checkAndSaveConfiguration(self):
        try:
            self._promptForMissingArguments()
            self.argsGetter.saveValuesIntoConfigFile()
        except InvalidConfigValue:
            self._checkAndSaveConfiguration()
        except Exception, e:
            print e.message
            sys.exit()
        
    def _prepareArguments(self):
        self.argsGetter = ConfigurationGetter()
        self.args = self.argsGetter.getConfiguration()
        
    def _guiPromptForMissingArguments(self):
        if(GuiConfiguration):
            self.args = GuiConfiguration(self.args, self.args.force_gui_prompt).getProcessedConfiguration()
        
    def _promptForMissingArguments(self):
        if(self.args.no_gui):
            if (self.args.host == None):
                self.args.host = self.interface.promptFor(prompt="Hostname: ", message="You must supply hostname on the first run, it's easier through command line arguments.")
            if (self.args.name == None):
                self.args.name = self.interface.promptFor(prompt="Username: ", message="You must supply username on the first run, it's easier through command line arguments.")
            if (self.args.player_path == None):
                self.args.player_path = self.interface.promptFor(prompt="Player executable: ", message="You must supply path to your player on the first run, it's easier through command line arguments.")
        else:
            self._guiPromptForMissingArguments()
            

        
