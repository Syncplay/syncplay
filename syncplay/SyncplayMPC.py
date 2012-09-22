from syncplay.client import SyncplayClient
from syncplay.client import SyncplayClientManager

from syncplay.players import mpc
from syncplay.ConfigurationGetter import MPCConfigurationGetter

      
class SyncplayMPC(SyncplayClient):
    def __init__(self):
        SyncplayClient.__init__(self)
        run_mpc = lambda m: mpc.run_mpc(m, self.args.mpc_path, self.args.file, self.args._args)
        syncplayClient = SyncplayClientManager(self.args.name, run_mpc, self.interface, self.args.debug, self.args.room, self.args.password)
        self.interface.addClient(syncplayClient)
        syncplayClient.start(self.args.host, self.args.port)
    
    def _prepareArguments(self):
        self.argsGetter = MPCConfigurationGetter()
        self.args = self.argsGetter.getConfiguration()

    def _guiPromptForMissingArguments(self):
        try:
            from syncplay.ui.GuiConfiguration import GuiConfigurationForMPC
            self.args = GuiConfigurationForMPC(self.args, self.args.force_gui_prompt).getProcessedConfiguration()
        except ImportError: 
            pass

    def _promptForMissingArguments(self):
        SyncplayClient._promptForMissingArguments(self)
        if (self.args.mpc_path == None):
            self.args.mpc_path = self.interface.promptFor(promptName = "Path to mpc-hc.exe", message = "You must supply path to mpc on the first run, it's easier through command line arguments.")
      
    