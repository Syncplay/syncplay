#coding:utf8
from syncplay import client
from syncplay.players import mplayer
from syncplay import ui
from syncplay import utils

class SyncplayMplayer:
    def runClient(self):
        self._prepareArguments()
#        self.interface = ui.getUi(graphical = not self.args.no_gui)
        self.interface = ui.getUi(graphical = False) #TODO: add gui
        self._promptForMissingArguments()
        self.args._args.extend(('-slave', '-msglevel', 'all=1:global=4'))
        if(self.args.file): self.args._args.extend((self.args.file,))
        syncplayClient = client.SyncplayClient(self.args.name, lambda m: mplayer.run_mplayer(m, 'mplayer', self.args._args), self.interface, self.args.debug, self.args.room, self.args.password)
        self.interface.addClient(syncplayClient)
        syncplayClient.start(self.args.host, self.args.port)
    def _prepareArguments(self):
        self.argsGetter = utils.ConfigurationGetter()
        self.args = self.argsGetter.getConfiguration()
    
    def _promptForMissingArguments(self):
        if (self.args.host == None):
            self.args.host = self.interface.promptFor(promptName = "Hostname", message = "You must supply hostname on the first run, it's easier through command line arguments.")
        if (self.args.name == None):
            self.args.name = self.interface.promptFor(promptName = "Username", message = "You must supply username on the first run, it's easier through command line arguments.")
        self.argsGetter.saveValuesIntoConfigFile()   

if __name__ == '__main__':
    SyncplayMplayer().runClient()

