try:
    import winsound
except ImportError:
    winsound = None
try:
    import alsaaudio
    import wave
except ImportError:
    alsaaudio = None
from syncplay import utils

def doBuzz():
    if(winsound):
        buzzPath = utils.findWorkingDir() + "\\resources\\buzzer.wav"
        winsound.PlaySound(buzzPath, winsound.SND_FILENAME|winsound.SND_ASYNC)
    elif(alsaaudio):
        buzzPath = utils.findWorkingDir() + "/resources/buzzer.wav"
        print buzzPath
        try:
            buzz = wave.open(buzzPath, 'rb')
            device = alsaaudio.PCM(0)
            device.setchannels(buzz.getnchannels())
            device.setrate(buzz.getframerate())
            if buzz.getsampwidth() == 1:
                device.setformat(alsaaudio.PCM_FORMAT_U8)
            elif buzz.getsampwidth() == 2:
                device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            else:
                raise ValueError('Unsupported buzzer format')
            device.setperiodsize(640)
            data = buzz.readframes(640)
            while data:
                device.write(data)
                data = buzz.readframes(640)
            buzz.close()
        except IOError:
            pass

