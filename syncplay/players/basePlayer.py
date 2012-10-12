class BasePlayer(object):
    def askForStatus(self):
        raise NotImplementedError()

    def displayMessage(self):
        raise NotImplementedError()

    def drop(self):
        raise NotImplementedError()

    @staticmethod
    def run(client, playerPath, filePath, args):
        raise NotImplementedError()

    def setPaused(self):
        raise NotImplementedError()

    def setPosition(self):
        raise NotImplementedError()

    def setSpeed(self):
        raise NotImplementedError()
