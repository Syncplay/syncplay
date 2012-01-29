#coding:utf8
 
import re
 
from twisted.internet import reactor
from twisted.internet.defer import Deferred, succeed
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
 
from zope.interface import implements
from twisted.web.iweb import IBodyProducer

from ..network_utils import handle_response

RE_MPC_STATUS = re.compile("^OnStatus\('(.+)', '(Paused|Playing)', (\d+), '\d{2}:\d{2}:\d{2}', \d+, '\d{2}:\d{2}:\d{2}', \d+, \d+, '.+'\)$")
 
class MPCHCProtocol(object):
    def __init__(self, manager):
        self.manager = manager
    
    def send_set_paused(self, value):
        self.set_property('pause', value)

    def send_get_paused(self):
        self.get_property('pause')
        
    def send_set_position(self, value):
        self.set_property('time_pos', '%d'%(value*1000))

    def send_get_position(self):
        self.get_property('time_pos')

    def send_set_speed(self, value):
        pass

    def send_get_speed(self):
        pass
    
    def set_property(self, name, value):
        requestData = {
        'paused': lambda value: 'wm_command=888&null=0' if value else 'wm_command=887&null=0',
        'time_pos': lambda value: "wm_command=-1&position="+  '%d.%d.%d.%d' % ((int(value)/3600000), (int(value)/60000)%60, (int(value)/1000)%60, int(value)%1000)
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
            fileName, playerStatus, currentTime = m.group(1), m.group(2), m.group(3)
            if(propertyName == "paused"):
                self.manager.update_player_paused(True if playerStatus=="Paused" else False)
            if(propertyName == "time_pos"):
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

