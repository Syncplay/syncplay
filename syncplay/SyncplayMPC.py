from syncplay.client import SyncplayClient
from syncplay.client import SyncplayClientManager

from syncplay.players import mpc
from syncplay.ConfigurationGetter import MPCConfigurationGetter

class SyncplayMPC(SyncplayClient):
    def __init__(self):
        SyncplayClient.__init__(self)
        syncplayClient = SyncplayClientManager(self.args.name, lambda m: mpc.run_mpc(m, self.args.mpc_path, self.args.file, self.args._args), self.interface, self.args.debug, self.args.room, self.args.password)
        self.interface.addClient(syncplayClient)
        syncplayClient.start(self.args.host, self.args.port)
    
    def _prepareArguments(self):
        self.argsGetter = MPCConfigurationGetter()
        self.args = self.argsGetter.getConfiguration()
        self.argsGetter.saveValuesIntoConfigFile() 
    
    def _promptForMissingArguments(self):
        SyncplayClient._promptForMissingArguments(self)
        #if(self.args.no_gui)
        while (self.args.mpc_path == None):
            self.args.mpc_path = self.interface.promptFor(promptName = "Path to mpc-hc.exe", message = "You must supply path to mpc on the first run, it's easier through command line arguments.")
          
        