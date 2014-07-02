import syncplay.players

class PlayerFactory(object):
    def __init__(self):
        self._players = syncplay.players.getAvailablePlayers()
        
    def getAvailablePlayerPaths(self):
        l = []
        for player in self._players:
            l.extend(player.getDefaultPlayerPathsList())
        return l
    
    def getPlayerByPath(self, path):
        for player in self._players:
            if player.isValidPlayerPath(path):
                return player
                
    def getPlayerIconByPath(self, path):
        for player in self._players:
            if player.isValidPlayerPath(path):
                return player.getIconPath(path)
        return None
    
    def getExpandedPlayerPathByPath(self, path):
        for player in self._players:
            if player.isValidPlayerPath(path):
                return player.getExpandedPath(path)
        return None
