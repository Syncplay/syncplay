#coding:utf8

import re

from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from ..network_utils import (
    BodyProducer,
    handle_response,
    null_response_handler,
)

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
    def __init__(self, manager, host = None):
        self.manager = manager
        self.host = 'localhost:13579'

        self.filename = None # To be moved to Manager

        manager.player = self
        self.agent = Agent(reactor)

    def set_paused(self, value):
        self.send_post_request('wm_command=%d' % (888 if value else 887))

    def set_position(self, value):
        value = int(value*1000)
        seconds, mseconds = divmod(value, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        self.send_post_request('wm_command=-1&position=%d.%d.%d.%d' % (
            hours, minutes, seconds, mseconds
        ))

        self.send_post_request(body)

    def status_response(self, status, headers, body):
        m = RE_MPC_STATUS.match(body)
        if not m:
            return
        filename, paused, position = m.group(1), m.group(2), m.group(3)

        paused = PLAYING_STATUSES.get(paused)
        if paused is None:
            return
        if self.filename is None:
            self.filename = filename
        position = float(position)/1000
        self.manager.update_player_status(paused, position)

    def ask_for_status(self, propertyName):
        request = self.agent.request(
            'GET',
            'http://localhost:13579/status.html',
            Headers(),
            None,
        )
        request.addCallback(handle_response(self.status_response))

    def send_post_request(self, body):
        request = self.agent.request(
            'POST',
            'http://%s/command.html' % self.host,
            Headers({'Content-Type': ['application/x-www-form-urlencoded']}),
            BodyProducer(body),
        )
        request.addCallback(handle_response(null_response_handler))

