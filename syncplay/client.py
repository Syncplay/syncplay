#coding:utf8

from .network_utils import argumentCount, CommandProtocol
from .utils import ArgumentParser, format_time
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
import re
import time

class SyncClientProtocol(CommandProtocol):
    def __init__(self, syncplayClient):
        self.syncplayClient = syncplayClient
        self.handler = self._MessagesHandler(syncplayClient)
        self.sender = self._MessagesSender(self)

    def connectionMade(self):
        self.sendMessage('iam', self.syncplayClient.name)
        self.syncplayClient.initProtocol(self)

    def connectionLost(self, reason):
        self.syncplayClient.destroyProtocol()
        self.syncplayClient.ui.showDebugMessage("Connection lost, reason: %s" % reason)

    def sendMessage(self, *args):
        line = ArgumentParser.joinArguments(args)
        self.sendLine(line)
        self.syncplayClient.ui.showDebugMessage('NETWORK:\t<<' + line)
    
    def dropWithError(self, error):
        self.syncplayClient.ui.showErrorMessage(error)
        CommandProtocol.dropWithError(self, error)
    
    def lineReceived(self, line):
        self.syncplayClient.ui.showDebugMessage('NETWORK:\t>>%s' % line)
        CommandProtocol.lineReceived(self, line)
    
    class _MessagesHandler(object):
        def __init__(self, syncplayClient):
            self._syncplayClient = syncplayClient
            self._lastServerTimestamp = 0
        
        @argumentCount(1)
        def hello(self, args):
            message ='Connected as ' + args[0] 
            print message
            self._syncplayClient.name = args[0]
            self._syncplayClient.protocol.sender.send_list()
            self._syncplayClient.scheduleSendStatus()
    
        @argumentCount(2, 3)
        def present(self, args):
            if len(args) == 3:
                who, where, what = args
            else:
                who, where, what = args[0], args[1], None
            if what:
                message = '%s is present and is playing \'%s\' in the room: \'%s\'' % (who, what, where)
                print message
                if(self._syncplayClient.player): self._syncplayClient.player.display_message(message)
            else:
                message = '%s is present in the room: \'%s\'' % (who, where)
                print message
                if(self._syncplayClient.player): self._syncplayClient.player.display_message(message)
    
        @argumentCount(4, 5)
        def state(self, args):
            args = self.__parseState(args)
            if not args:
                self.dropWithError('Malformed state attributes')
                return
    
            counter, ctime, paused, position, name = args
    
            self._syncplayClient.updateGlobalState(counter, ctime, paused, position, name)
    
        @argumentCount(3)
        def seek(self, args):
            ctime, position, who = args
            try:
                ctime = int(ctime)
                position = int(position)
            except ValueError:
                self.dropWithError('Invalid arguments')
    
            ctime /= 1000.0
            position /= 1000.0
    
            self._syncplayClient.seek(ctime, position, who)
    
        @argumentCount(1)
        def ping(self, args):
            self._syncplayClient.protocol.sendMessage('pong', args[0], int(time.time()*100000))
    
        @argumentCount(3)
        def playing(self, args):
            who, where, what = args
            message = '%s is playing \'%s\' in the room: \'%s\'' % (who, what, where)
            print message
            if(self._syncplayClient.player): self._syncplayClient.player.display_message(message)
    
        @argumentCount(1)
        def joined(self, args):
            message = '%s joined' % args[0]
            print message
            if(self._syncplayClient.player): self._syncplayClient.player.display_message(message)
        
        @argumentCount(2)
        def room(self, args):
            message = '%s entered the room: \'%s\'' % (args[0], args[1])
            print message
            if(self._syncplayClient.player): self._syncplayClient.player.display_message(message)
    
        @argumentCount(1)
        def left(self, args):
            message = '%s left' % args[0]
            print message
            if(self._syncplayClient.player): self._syncplayClient.player.display_message(message)

        def __parseState(self, args):
            if len(args) == 4:
                counter, ctime, state, position = args
                who_changed_state = None
            elif len(args) == 5:
                counter, ctime, state, position, who_changed_state = args
            else:
                return
        
            if not state in ('paused', 'playing'):
                return
        
            paused = state == 'paused'
        
            try:
                counter = int(counter)
                ctime = int(ctime)
                position = int(position)
            except ValueError:
                return
        
            ctime /= 1000.0
            position /= 1000.0
        
            return counter, ctime, paused, position, who_changed_state
        
    class _MessagesSender(object):
        def __init__(self, protocol):
            self._protocol = protocol
            
        def send_list(self):
            self._protocol.sendMessage('list')
    
        def send_state(self, counter, ctime, paused, position):
            self._protocol.sendMessage('state', counter, int(ctime*1000), ('paused' if paused else 'playing'), int(position*1000))
    
        def sendSeek(self, counter, ctime, position):
            self._protocol.sendMessage('seek', counter, int(ctime*1000), int(position*1000))
        
        def send_room(self, where):
            self._protocol.sendMessage('room', where)
    
        def send_playing(self, filename):
            self._protocol.sendMessage('playing', filename)

class SyncClientFactory(ClientFactory):
    def __init__(self, manager):
        self._syncplayClient = manager
        self.retry = True

    def buildProtocol(self, addr):
        return SyncClientProtocol(self._syncplayClient)

    def startedConnecting(self, connector):
        destination = connector.getDestination()
        print 'Connecting to %s:%d' % (destination.host, destination.port)

    def clientConnectionLost(self, connector, reason):
        if self.retry:
            print 'Connection lost, reconnecting'
            reactor.callLater(0.1, connector.connect)
        else:
            message = 'Disconnected'
            print message
            if(self._syncplayClient.player): self._syncplayClient.player.display_message(message)

    def clientConnectionFailed(self, connector, reason):
        message = 'Connection failed'
        print message
        if(self._syncplayClient.player): self._syncplayClient.player.display_message(message)

        self._syncplayClient.stop()

    def stop_retrying(self):
        self.retry = False

class SyncplayClientManager(object):
    def __init__(self, name, make_player, ui, debug):
        self.name = name

        self.ui = self.UiManager(ui, debug)
        self.protocol_factory = None
        self.protocol = None
        self.send_delayed = None
        self.global_paused = True
        self.global_position = 0.0
        self.global_who_paused = None
        self.global_noted_pause_change = None
        self.last_global_update = None
        self.counter = 0
        self.counter_recv = 0

        self.player = None
        self.ask_delayed = None
        self.player_paused = True
        self.player_paused_at = 0.0
        self.player_position = 0.0
        self.last_player_update = None
        self.player_speed_fix = False
        self.player_filename = None
        self.player_position_before_last_seek = 0
        
        self.seek_sent_wait = False
        self.status_ask_sent = 0
        self.status_ask_received = 0

        self.make_player = make_player
        self.running = False
    
    def start(self, host, port):
        if self.running:
            return
        self.protocol_factory = SyncClientFactory(self)
        reactor.connectTCP(host, port, self.protocol_factory)
        self.running = True
        reactor.run()

    def stop(self):
        if not self.running:
            return
        self.running = False
        if self.protocol_factory:
            self.protocol_factory.stop_retrying()
        if self.protocol:
            self.protocol.drop()
        if self.player:
            self.player.drop()
        reactor.callLater(0.1, reactor.stop)


    def getPlayerPosition(self):
        if not self.last_player_update:
            return 0.0
        position = self.player_position
        if not self.player_paused:
            position += time.time() - self.last_player_update
        return position

    def getGlobalPosition(self):
        if not self.last_global_update:
            return 0.0
        position = self.global_position
        if not self.global_paused:
            position += time.time() - self.last_global_update
        return position


    def initPlayer(self, player):
        self.player = player
        if self.last_global_update:
            self.player.set_position(self.getGlobalPosition())
            self.player.set_paused(True)
        self.scheduleAskPlayer()

    def initProtocol(self, protocol):
        self.protocol = protocol
        if self.make_player:
            self.make_player(self)
            self.make_player = None

    def destroyProtocol(self):
        if self.protocol:
            self.protocol.drop()
        self.protocol = None
        
    def scheduleAskPlayer(self, when=0.2):
        if self.ask_delayed and self.ask_delayed.active():
            self.ask_delayed.reset(when)
        else:
            self.ask_delayed = reactor.callLater(when, self.askPlayer)

    def askPlayer(self):
        if not self.running:
            return
        if self.player:
            self.status_ask_sent += 1
            self.player.ask_for_status()
        self.scheduleAskPlayer()

    def scheduleSendStatus(self, when=1):
        if self.send_delayed and self.send_delayed.active():
            self.send_delayed.reset(when)
        else:
            self.send_delayed = reactor.callLater(when, self.sendStatus)

    def sendStatus(self, force = False):
        if not (self.running and self.protocol):
            return
        self.scheduleSendStatus()
        if self.counter > self.counter_recv and not force:
            return
        self.counter += 1
        curtime = time.time()
        position = self.player_position
        if not self.player_paused:
            position += curtime - self.last_player_update
        if self.protocol:
            self.protocol.sender.send_state(self.counter, curtime, self.player_paused, self.player_position)

    def sendSeek(self):
        if not (self.running and self.protocol):
            return
        self.counter += 10
        self.protocol.sender.sendSeek(self.counter, time.time(), self.player_position)
        message = self.name +' seeked to ' + format_time(self.player_position)
        print message
        self.player.display_message(message)
        
    def sendFilename(self):
        if self.protocol and self.player_filename:
            self.protocol.sender.send_playing(self.player_filename)

    def __exectueSeekCmd(self, seek_type, minutes, seconds):
        self.player_position_before_last_seek = self.player_position
        if seek_type == 's':
            seconds = int(seconds) if seconds <> None else 0
            seconds += int(minutes) * 60 if minutes <> None else 0 
            self.player.set_position(seconds)
        else: #seek_type s+
            seconds = int(seconds) if seconds <> None else 20
            seconds += int(minutes) * 60 if minutes <> None else 60
            self.player.set_position(self.player_position+seconds)
            
    def executeCommand(self, data):
        RE_SEEK = re.compile("^(s[+s]?) ?(-?\d+)?([^0-9](\d+))?$")
        RE_ROOM = re.compile("^room( (\w+))?")
        matched_seek = RE_SEEK.match(data)
        matched_room = RE_ROOM.match(data)
        if matched_seek :
            self.__exectueSeekCmd(matched_seek.group(1), matched_seek.group(2), matched_seek.group(4))
        elif matched_room:
            room = matched_room.group(2)
            if room == None:
                room = 'default'
            self.protocol.sender.send_room(room)
        elif data == "r":
            tmp_pos = self.player_position
            self.player.set_position(self.player_position_before_last_seek)
            self.player_position_before_last_seek = tmp_pos
        elif data == "p":
            self.player.set_paused(not self.player_paused)
        elif data == 'help':
            print "Available commands:"
            print "\thelp - this help"
            print "\ts [time] - seek"
            print "\ts+ [time] - seek to: current position += time"
            print "\tr - revert last seek"
            print "\tp - toggle pause"
            print "\troom [room] - change room, if no supplied go to default"
 
    def updatePlayerStatus(self, paused, position):
        self.status_ask_received += 1
        if self.status_ask_received < self.status_ask_sent:
            return
        old_paused = self.player_paused
        self.player_paused = paused
        self.player_position = position
        self.last_player_update = time.time()
        diff = position - self.getGlobalPosition()
        if old_paused and not paused:
            self.player_paused_at = None
        if old_paused != paused and self.global_paused != paused:
            self.sendStatus(True)
            if paused:
                message = '%s paused' % self.name
                print message
                self.player.display_message(message)
                if(diff > 0):
                    self.player.set_position(self.getGlobalPosition())
                    self.askPlayer()
            else:
                message = '%s unpaused' % self.name
                print message
                self.player.display_message(message)
        if not (self.global_paused or self.seek_sent_wait):
            if (0.4 if self.player_speed_fix else 1.2) <= diff <= 4:
                #print 'client is %0.2fs ahead of server, slowing down' % diff
                if not self.player_speed_fix:
                    self.player.set_speed(0.95)
                    self.player_speed_fix = True
            else:
                if self.player_speed_fix:
                    #print 'resetting speed'
                    self.player.set_speed(1)
                    self.player_speed_fix = False
        if abs(diff) > 8:# and not self.seek_sent_wait:
            self.sendSeek()
            self.seek_sent_wait = True
        if not paused and self.player_paused_at is not None and position >= self.player_paused_at:
            #print 'Pausing %0.2fs after pause point' % (position - self.player_paused_at)
            self.player.set_paused(True)
            self.askPlayer()

    def updateFilename(self, filename):
        filename = unicode(filename, errors='replace')
        self.player_filename = filename.encode('ascii','replace')
        self.sendFilename()

    def updateGlobalState(self, counter, ctime, paused, position, name):
        self.counter_recv = max(self.counter_recv, counter)
        counter_valid = self.counter and counter >= self.counter

        curtime = time.time()
        updated_before = bool(self.last_global_update)

        if updated_before and not counter_valid:
            return

        if not paused:
            position += curtime - ctime
        self.global_paused = paused
        self.global_position = position
        self.global_who_changed = name
        self.last_global_update = curtime

        if not self.player:
            return

        changed = False
        self.seek_sent_wait = False

        if not updated_before:
            self.player.set_position(position)
            self.player.set_paused(paused)
            changed = True

        if counter_valid:
            diff = self.getPlayerPosition() - position
            if abs(diff) > 4:
                self.player.set_position(position)
                #self.player.set_paused(True)
                message = "Rewinded due to time difference"
                print message
                self.player.display_message(message)


            if self.player_paused and not paused:
                self.player_paused_at = None
                self.player.set_paused(False)
                if self.global_noted_pause_change != paused:
                    message = '%s unpaused' % name
                    print message
                    self.player.display_message(message)

            elif paused and not self.player_paused:
                self.player_paused_at = position
                if self.global_noted_pause_change != paused:
                    message = '%s paused' % name
                    print message
                    self.player.display_message(message)
                    if(diff > 0):
                        self.player.set_position(self.getGlobalPosition())
                        self.askPlayer()
                if diff < 0:
                    self.player.set_paused(True)
            self.global_noted_pause_change = paused
            changed = True
            
        if changed:
            self.askPlayer()


    def seek(self, ctime, position, who):
        curtime = time.time()
        position += curtime - ctime
        self.global_position = position
        self.last_global_update = curtime
        if self.player:
            self.player_position_before_last_seek = self.player_position
            self.player.set_position(position)
            self.askPlayer()
        message = who + ' seeked to ' + format_time(position)
        print message
        self.player.display_message(message)

    class UiManager(object):
        def __init__(self, ui, debug = False):
            self.__ui = ui
            self.debug = debug 
        
        def showMessage(self, message):
            self.__ui.showMessage(message)
        
        def showDebugMessage(self, message):
            if(self.debug):
                self.__ui.showDebugMessage(message)
            
        def showErrorMessage(self, message):
            self.__ui.showErrorMessage(message)

        def displayListOfPeople(self):
            pass


