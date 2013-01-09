from syncplay import constants
class BasePlayer(object):
    def askForStatus(self):
        raise NotImplementedError()

    def displayMessage(self, message, duration = constants.OSD_DURATION):
        raise NotImplementedError()

    def drop(self):
        raise NotImplementedError()

    @staticmethod
    def run(client, playerPath, filePath, args):
        raise NotImplementedError()

    def setPaused(self, value):
        raise NotImplementedError()

    def setPosition(self, value):
        raise NotImplementedError()

    def setSpeed(self, value):
        raise NotImplementedError()
