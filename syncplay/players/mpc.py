#coding:utf8
 
import re
 
from twisted.internet import reactor
from twisted.internet.defer import Deferred, succeed
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
 
from zope.interface import implements
from twisted.web.iweb import IBodyProducer

from ..network_utils import handle_response

#RE_MPC_STATUS = re.compile("^OnStatus\('(.+)', '(Paused|Playing)', (\d+), '\d{2}:\d{2}:\d{2}', \d+, '\d{2}:\d{2}:\d{2}', \d+, \d+, '.+'\)$")
RE_MPC_STATUS = re.compile(r"^OnStatus\('((?:[^']*(?:\\\\)*\\')*[^']*)', '(.+?)', (\d+),")

PLAYING_STATUSES = {
    'Playing': False,
    'Reproduzindo': False,
    'Прайграванне': False,
    'Reproduint': False,
    'Přehrávání': False,
    'Spiele ab': False,
    'Reproduciendo': False,
    'Lecture': False,
    'מנגן': False,
    'Lejátszás': False,
    'Վերարատադրվում է': False,
    'Riproduzione': False,
    '再生中': False,
    '재생중': False,
    'Afspelen': False,
    'Odtwarzanie...': False,
    'Воспроизведение': False,
    '正在播放': False,
    'Prehráva sa': False,
    'Spelar': False,
    '播放中': False,
    'Oynatılıyor': False,
    'Відтворення': False,

    'Paused': True,
    'Pausado': True,
    'Паўза': True,
    'Pausat': True,
    'Pozastaveno': True,
    'Angehalten': True,
    'Pausado': True,
    'En pause': True,
    'מושהה': True,
    'Szünet': True,
    'Դադար': True,
    'In pausa': True,
    '一時停止': True,
    '일시정지': True,
    'Gepauzeerd': True,
    'Wstrzymano': True,
    'Пауза': True,
    '已暂停': True,
    'Pozastavené': True,
    'Pausad': True,
    '已暫停': True,
    'Duraklatıldı': True,
    'Пауза': True,
}
 
class MPCHCPlayer(object):
    def __init__(self, manager):
        self.manager = manager
        manager.player = self
    
    def send_set_paused(self, value):
        self.set_property('Paused', value)

    def send_get_paused(self):
        self.get_property('Paused')
        
    def send_set_position(self, value):
        self.set_property('Position', '%d'%(value*1000))

    def send_get_position(self):
        self.get_property('Position')

    def send_set_speed(self, value):
        pass

    def send_get_speed(self):
        pass
    
    def set_property(self, name, value):
        requestData = {
        'Paused': lambda value: 'wm_command=888&null=0' if value else 'wm_command=887&null=0',
        'Position': lambda value: "wm_command=-1&position="+  '%d.%d.%d.%d' % ((int(value)/3600000), (int(value)/60000)%60, (int(value)/1000)%60, int(value)%1000)
        }[name](value)

        body = StringBodyProducer(requestData)
        self.sendPostRequest(body)
    
    def get_property(self, propertyName):
        agent = Agent(reactor)
        request = agent.request(
            'GET',
            'http://localhost:13579/status.html',
            Headers(),
            None)
            
        def cbRequest(status, headers, body):
            m = RE_MPC_STATUS.match(body)
            if not m:
                return
            fileName, playerStatus, currentTime = m.group(1), m.group(2), m.group(3)
            playerStatus = PLAYING_STATUSES.get(playerStatus)
            if playerStatus is None:
                return
            if(propertyName == "Paused"):
                self.manager.update_player_paused(playerStatus)
            if(propertyName == "Position"):
                self.manager.update_player_position(float(currentTime)/1000.0)
				
        request.addCallback(handle_response(cbRequest))

    def sendPostRequest(self, body):
        agent = Agent(reactor)
        request = agent.request(
            'POST',
            'http://localhost:13579/command.html',
            Headers({'Content-Type': ['application/x-www-form-urlencoded']}),
            body)

        def cbRequest(ignored):
            return
        request.addCallback(cbRequest)

class StringBodyProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass

