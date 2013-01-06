try:
    import winsound
except ImportError:
    winsound = None
from syncplay import utils

def doBuzz():
    buzzPath = utils.findWorkingDir() + "\\resources\\buzzer.wav"
    print buzzPath
    if(winsound):
        winsound.PlaySound(buzzPath, winsound.SND_FILENAME|winsound.SND_ASYNC)
