#coding:utf8
from syncplay import client
from syncplay.players import mpc
from syncplay import ui
from syncplay import utils

class SyncplayMPC:
    def runClient(self):
        self._prepareArguments()
        self.interface = ui.getUi(graphical = not self.args.no_gui)
        self._promptForMissingArguments()
        syncplayClient = client.SyncplayClientManager(self.args.name, lambda m: mpc.run_mpc(m, self.args.mpc_path, self.args.file, self.args._args), self.interface, self.args.debug)
        self.interface.addClient(syncplayClient)
        syncplayClient.start(self.args.host, self.args.port)
    def _prepareArguments(self):
        self.argsGetter = utils.MPCConfigurationGetter()
        self.argsGetter.prepareClientConfiguration()
        self.args = self.argsGetter.getClientConfiguration()
    
    def _promptForMissingArguments(self):
        if (self.args.host == None):
            self.args.host = self.interface.promptFor(promptName = "Hostname", message = "You must supply hostname on the first run, it's easier trough command line arguments.")
        if (self.args.name == None):
            self.args.name = self.interface.promptFor(promptName = "Username", message = "You must supply username on the first run, it's easier trough command line arguments.")
        if (self.args.mpc_path == None):
            self.args.mpc_path = self.interface.promptFor(promptName = "Path to mpc-hc.exe", message = "You must supply path to mpc on the first run, it's easier trough command line arguments.")
        self.argsGetter.saveValuesIntoConfigFile()      

if __name__ == '__main__':
    SyncplayMPC().runClient()

