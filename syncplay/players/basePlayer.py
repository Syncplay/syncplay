from syncplay import constants
class BasePlayer(object):
  
    '''
    This method is supposed to 
    execute updatePlayerStatus(paused, position) on client
    Given the arguments: boolean paused and float position in seconds 
    '''
    def askForStatus(self):
        raise NotImplementedError()

    '''
    Display given message on player's OSD or similar means
    '''
    def displayMessage(self, message, duration = constants.OSD_DURATION):
        raise NotImplementedError()

    '''
    Cleanup connection with player before syncplay will close down
    '''
    def drop(self):
        raise NotImplementedError()

    '''
    Start up the player, returns its instance
    '''
    @staticmethod
    def run(client, playerPath, filePath, args):
        raise NotImplementedError()

    '''
    @type value: boolean 
    '''
    def setPaused(self, value):
        raise NotImplementedError()

    '''
    @type value: float 
    '''
    def setPosition(self, value):
        raise NotImplementedError()

    '''
    @type value: float 
    '''
    def setSpeed(self, value):
        raise NotImplementedError()
    
    '''
    @return: list of strings
    '''
    @staticmethod
    def getDefaultPlayerPathsList():
        raise NotImplementedError()
    
    '''
    @type path: string
    '''
    @staticmethod
    def isValidPlayerPath(path):
        raise NotImplementedError()
    
    
class DummyPlayer(BasePlayer):

    @staticmethod
    def getDefaultPlayerPathsList():
        return []
    
    @staticmethod
    def isValidPlayerPath(path):
        return False