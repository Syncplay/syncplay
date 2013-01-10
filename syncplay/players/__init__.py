from syncplay.players.mplayer import MplayerPlayer
try:
    from syncplay.players.mpc import MPCHCAPIPlayer
except ImportError:
    from syncplay.players.basePlayer import DummyPlayer 
    MPCHCAPIPlayer = DummyPlayer
    
def getAvailablePlayers():
    return [MPCHCAPIPlayer, MplayerPlayer]