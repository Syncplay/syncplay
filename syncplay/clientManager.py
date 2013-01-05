from syncplay.client import SyncplayClient
from syncplay.ui.ConfigurationGetter import ConfigurationGetter
from syncplay import ui
from syncplay.messages import getMessage

try:
    from syncplay.players.mpc import MPCHCAPIPlayer
except ImportError:
    MPCHCAPIPlayer = None
from syncplay.players.mplayer import MplayerPlayer

class SyncplayClientManager(object):
    def run(self):
        config = ConfigurationGetter().getConfiguration()
        interface = ui.getUi(graphical=not config["noGui"])
        syncplayClient = None
        if(config['playerType'] == "mpc"):
            syncplayClient = SyncplayClient(MPCHCAPIPlayer, interface, config)
        elif(config['playerType'] == "mplayer"):
            syncplayClient = SyncplayClient(MplayerPlayer, interface, config)
        if(syncplayClient):
            interface.addClient(syncplayClient)
            syncplayClient.start(config['host'], config['port'])
        else:
            interface.showErrorMessage(getMessage("en", "unable-to-start-client-error"))
        
