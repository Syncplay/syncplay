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
    def displayMessage(self, message, duration = (constants.OSD_DURATION*1000)):
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
    @type filePath: string 
    '''
    def openFile(self, filePath, resetPosition=False):
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
        
    '''
    @type path: string
    @return: string
    '''    
    @staticmethod
    def getIconPath(path):
        raise NotImplementedError()
    
    '''
    @type path: string
    @return: string
    '''    
    @staticmethod
    def getExpandedPath(path):
        raise NotImplementedError()

    '''
    Opens a custom media browse dialog, and then changes to that media if appropriate
    '''
    @staticmethod
    def openCustomOpenDialog(self):
        raise NotImplementedError()

    '''
    @type playerPath: string
    @type filePath: string
    @return errorMessage: string

    Checks if the player has any problems with the given player/file path
    '''
    @staticmethod
    def getPlayerPathErrors(playerPath, filePath):
        raise NotImplementedError()

class DummyPlayer(BasePlayer):

    @staticmethod
    def getDefaultPlayerPathsList():
        return []
    
    @staticmethod
    def isValidPlayerPath(path):
        return False
    
    @staticmethod
    def getIconPath(path):
        return None
    
    @staticmethod
    def getExpandedPath(path):
        return path

    @staticmethod
    def getPlayerPathErrors(playerPath, filePath):
        return None