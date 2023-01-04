# coding:utf8
from syncplay import ui
from syncplay.messages import getMessage
from syncplay.ui.ConfigurationGetter import ConfigurationGetter


class SyncplayClientManager(object):
    def run(self):
        config = ConfigurationGetter().getConfiguration()
        from syncplay.client import SyncplayClient  # Imported later, so the proper reactor is installed
        menuBar = config['menuBar'] if 'menuBar' in config else None
        interface = ui.getUi(graphical=not config["noGui"], passedBar=menuBar)
        syncplayClient = SyncplayClient(config["playerClass"], interface, config)
        if syncplayClient:
            interface.addClient(syncplayClient)
            syncplayClient.start(config['host'], config['port'])
        else:
            interface.showErrorMessage(getMessage("unable-to-start-client-error"), True)
