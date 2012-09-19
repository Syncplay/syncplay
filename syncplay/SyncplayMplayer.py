from syncplay.client import SyncplayClient
from syncplay.client import SyncplayClientManager

from syncplay.players import mplayer
from syncplay.ConfigurationGetter import ConfigurationGetter

class SyncplayMplayer(SyncplayClient):
    def __init__(self):
        SyncplayClient.__init__(self)
        run_mplayer = lambda m: mplayer.run_mplayer(m, 'mplayer', self.args._args)
        syncplayClient = SyncplayClientManager(self.args.name, run_mplayer, self.interface, self.args.debug, self.args.room, self.args.password)
        self.interface.addClient(syncplayClient)
        syncplayClient.start(self.args.host, self.args.port)
    
    def _prepareArguments(self):
        self.argsGetter = ConfigurationGetter()
        self.args = self.argsGetter.getConfiguration()
    
    def _promptForMissingArguments(self):
        SyncplayClient._promptForMissingArguments(self)
        
        self.args._args.extend(('-slave', '-msglevel', 'all=1:global=4'))
        if(self.args.file): self.args._args.extend((self.args.file,))
