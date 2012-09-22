#coding:utf8

from .network_utils import argumentCount, CommandProtocol
from .utils import ArgumentParser, format_time
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
import time
import itertools
import syncplay
import hashlib
import os

class SyncClientProtocol(CommandProtocol):
    def __init__(self, syncplayClient):
        self.syncplayClient = syncplayClient
        self.handler = self._MessagesHandler(self, syncplayClient)
        self.sender = self._MessagesSender(self)

    def connectionMade(self):
        self.sendMessage('iam', self.syncplayClient.users.currentUser.name, self.syncplayClient.users.currentUser.room, self.syncplayClient.serverPassword)
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
        self.syncplayClient.protocol_factory.stop_retrying()
        CommandProtocol.dropWithError(self, error)
    
    def lineReceived(self, line):
        self.syncplayClient.ui.showDebugMessage('NETWORK:\t>>%s' % line)
        CommandProtocol.lineReceived(self, line)
    
    class _MessagesHandler(object):
        def __init__(self, protocol, syncplayClient):
            self.__protocol = protocol
            self.__syncplayClient = syncplayClient
            self._lastServerTimestamp = 0
        
        def dropWithError(self, error):
            self.__protocol.dropWithError(error)
            
        @argumentCount(1)
        def hello(self, args):
            message ='Connected as ' + args[0] 
            self.__syncplayClient.ui.showMessage(message)
            self.__syncplayClient.users.currentUser.name = args[0]
            self.__syncplayClient.protocol.sender.send_list()
            self.__syncplayClient.scheduleSendStatus()
            if(self.__syncplayClient.users.currentUser.filename <> None):
                self.__syncplayClient.sendPlaying()
    
        @argumentCount(2, 5)
        def present(self, args):
            if len(args) == 5:
                who, where, what, duration, size = args
            else:
                who, where, what, duration, size = args[0], args[1], None, None, None
            self.__syncplayClient.users.addUser(SyncplayClientManager.SyncplayUser(who, what, where, duration, size))
            if what:
                message = '%s is present and is playing \'%s\' (%s) in the room: \'%s\'' % (who, what, format_time(int(duration)), where)
                self.__syncplayClient.ui.showMessage(message)
                self.__syncplayClient.checkIfFileMatchesOthers()
            else:
                message = '%s is present in the room: \'%s\'' % (who, where)
                self.__syncplayClient.ui.showMessage(message)
    
        @argumentCount(4, 5)
        def state(self, args):
            args = self.__parseState(args)
            if not args:
                self.dropWithError('Malformed state attributes')
                return
            counter, ctime, paused, position, name = args
            self.__syncplayClient.updateGlobalState(counter, ctime, paused, position, name)
    
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
            self.__syncplayClient.seek(ctime, position, who)
    
        @argumentCount(1)
        def ping(self, args):
            self.__syncplayClient.protocol.sendMessage('pong', args[0], int(time.time()*100000))
    
        @argumentCount(2)
        def error(self, args):
            self.__protocol.dropWithError(args[1])
            if(syncplay.version <> args[0]):
                self.__syncplayClient.ui.showMessage("Mismatch between client and server versions detected")
                self.__syncplayClient.ui.showMessage("Your version is %s against server's %s" % (syncplay.version, args[0]))
                self.__syncplayClient.ui.showMessage("Please use latest version of client and server")
        
        @argumentCount(5)
        def playing(self, args):
            who, where, what, duration, size = args
            message = '%s is playing \'%s\' (%s) in the room: \'%s\'' % (who, what, format_time(int(duration)), where)
            self.__syncplayClient.ui.showMessage(message)
            self.__syncplayClient.users.addUser(SyncplayClientManager.SyncplayUser(who, what, where, duration, size))
            self.__syncplayClient.checkIfFileMatchesOthers()
    
        @argumentCount(1)
        def joined(self, args):
            message = '%s joined' % args[0]
            self.__syncplayClient.ui.showMessage(message)
        
        @argumentCount(2)
        def room(self, args):
            message = '%s entered the room: \'%s\'' % (args[0], args[1])
            self.__syncplayClient.users.addUser(SyncplayClientManager.SyncplayUser(args[0], None, args[1]))
            self.__syncplayClient.checkIfFileMatchesOthers()
            self.__syncplayClient.ui.showMessage(message)
    
        @argumentCount(1)
        def left(self, args):
            message = '%s left' % args[0]
            self.__syncplayClient.ui.showMessage(message)
            self.__syncplayClient.users.removeUser(args[0])
            
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
    
        def send_playing(self, filename, duration, size):
            self._protocol.sendMessage('playing', filename, duration, size)

class SyncClientFactory(ClientFactory):
    def __init__(self, manager, retry = 10):
        self.__syncplayClient = manager
        self.retry = retry #add incremental wait

    def buildProtocol(self, addr):
        return SyncClientProtocol(self.__syncplayClient)

    def startedConnecting(self, connector):
        destination = connector.getDestination()
        self.__syncplayClient.ui.showMessage('Connecting to %s:%d' % (destination.host, destination.port))

    def clientConnectionLost(self, connector, reason):
        if self.retry:
            self.retry -= 1
            message = 'Connection lost, reconnecting'
            self.__syncplayClient.ui.showMessage(message)
            self.__syncplayClient.counter = 0
            reactor.callLater(0.1, connector.connect)
        else:
            message = 'Disconnected'
            self.__syncplayClient.ui.showMessage(message)

    def clientConnectionFailed(self, connector, reason):
        message = 'Connection failed'
        self.__syncplayClient.ui.showMessage(message)
        self.__syncplayClient.stop()

    def stop_retrying(self):
        self.retry = 0

class SyncplayClientManager(object):
    def __init__(self, name, make_player, ui, debug, room, password = None):
        self.users = self.UserList()
        self.users.currentUser.name = name
        if(room == None or room == ''):
            room = 'default'
        self.users.currentUser.room = room
        if(password):
            password = hashlib.md5(password).hexdigest()
        self.serverPassword = password
        self.ui = self.UiManager(self, ui, debug)
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
        self.player_position_before_last_seek = 0
        
        self.seek_sent_wait = False
        self.status_ask_sent = 0
        self.status_ask_received = 0

        self.make_player = make_player
        self.running = False
    
    def start(self, host, port):
        if self.running:
            return
        if self.make_player:
            self.make_player(self)
            self.make_player = None
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

    def checkIfFileMatchesOthers(self):
        notMatchingList = self.users.getUsersWithNotMatchingFilenames()
        if (notMatchingList <> []):
            for u in notMatchingList:
                message = "File you're playing is different from %s's" % u.name
                self.ui.showMessage(message)

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
        self.scheduleAskPlayer()

    def initProtocol(self, protocol):
        self.protocol = protocol

    def destroyProtocol(self):
        if self.protocol:
            self.protocol.drop()
        self.protocol = None
        
    def scheduleAskPlayer(self, when=0.3):
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
        self.player_position_before_last_seek = self.getGlobalPosition()
        self.protocol.sender.sendSeek(self.counter, time.time(), self.player_position)
        message = self.users.currentUser.name +' jumped to ' + format_time(self.player_position)
        self.ui.showMessage(message)
        
    def sendPlaying(self):
        if self.protocol and self.users.currentUser.filename:
            self.protocol.sender.send_playing(self.users.currentUser.filename, self.users.currentUser.fileduration, self.users.currentUser.filesize)

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
                message = '%s paused' % self.users.currentUser.name
                self.ui.showMessage(message)
                if(diff > 0):
                    self.player.set_position(self.getGlobalPosition())
                    self.askPlayer()
            else:
                message = '%s unpaused' % self.users.currentUser.name
                self.ui.showMessage(message)
        if not (self.global_paused or self.seek_sent_wait):
            if (0.4 if self.player_speed_fix else 1.2) <= diff <= 4:
                if not self.player_speed_fix:
                    self.player.set_speed(0.95)
                    self.player_speed_fix = True
            else:
                if self.player_speed_fix:
                    self.player.set_speed(1)
                    self.player_speed_fix = False
        if abs(diff) > 8 and not self.seek_sent_wait:
            self.sendSeek()
            self.seek_sent_wait = True
        if not paused and self.player_paused_at is not None and position >= self.player_paused_at:
            self.player.set_paused(True)
            self.askPlayer()

    def updateFile(self, filename, duration, path):
        filename = unicode(filename, errors='replace')
        self.users.currentUser.filename = filename.encode('ascii','replace')
        self.users.currentUser.fileduration = unicode(duration)
        self.users.currentUser.filesize = unicode(os.path.getsize(path))
        self.sendPlaying()

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
                self.ui.showMessage(message)

            if self.player_paused and not paused:
                self.player_paused_at = None
                self.player.set_paused(False)
                if self.global_noted_pause_change != paused:
                    message = '%s unpaused' % name
                    self.ui.showMessage(message)

            elif paused and not self.player_paused:
                self.player_paused_at = position
                if self.global_noted_pause_change != paused:
                    message = '%s paused' % name
                    self.ui.showMessage(message)
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
        message = who + ' jumped to ' + format_time(position)
        self.ui.showMessage(message)

    class UiManager(object):
        def __init__(self, client, ui, debug = False):
            self.__syncplayClient = client
            self.__ui = ui
            self.debug = debug 
        
        def showMessage(self, message):
            if(self.__syncplayClient.player): self.__syncplayClient.player.display_message(message)
            self.__ui.showMessage(message)
        
        def showDebugMessage(self, message):
            if(self.debug):
                self.__ui.showDebugMessage(message)
            
        def showErrorMessage(self, message):
            self.__ui.showErrorMessage(message)
    
    class SyncplayUser(object):
        def __init__(self, name = None, filename = None, room = None, fileduration = None, filesize = None):
            self.name = name
            self.room = room
            self.filename = filename
            self.filesize = filesize
            self.fileduration = fileduration
            
    class UserList(object):
        def __init__(self):
            self.users = dict()
            self.currentUser = SyncplayClientManager.SyncplayUser()
            
        def addUser(self, user):
            if(not isinstance(user,SyncplayClientManager.SyncplayUser)):
                user = SyncplayClientManager.SyncplayUser(user)
            if(not user.name == self.currentUser.name):
                if(self.users.has_key(user.name)):
                    self.users[user.name].room = user.room if user.room <> None else self.users[user.name].room
                    self.users[user.name].filename = user.filename if user.filename <> None else self.users[user.name].filename
                    self.users[user.name].filesize = user.filesize if user.filesize <> None else self.users[user.name].filesize
                    self.users[user.name].fileduration = user.fileduration if user.fileduration <> None else self.users[user.name].fileduration
                else:   
                    self.users[user.name] = user
            
        def removeUser(self, user):
            if(not isinstance(user,SyncplayClientManager.SyncplayUser)):
                user = SyncplayClientManager.SyncplayUser(user) 
            if(self.users.has_key(user.name)):
                self.users.pop(user.name)
    
        def getUsersWithNotMatchingFilenames(self):
            if(self.currentUser.filename == None):
                return []
            matchingFilename = lambda x: self._areUsersFilesSame(x)
            return list(itertools.ifilterfalse(matchingFilename, self.users.itervalues()))
            
        def _areUsersFilesSame(self, user):
            filenameCheck = (user.filename == None or user.filename == self.currentUser.filename)
            sizeCheck = (user.filesize == None or user.filesize == self.currentUser.filesize)
            durationCheck = (user.fileduration == None or user.fileduration == self.currentUser.fileduration)
            roomCheck = user.room <> self.currentUser.room
            return (filenameCheck and sizeCheck and durationCheck) or roomCheck


from syncplay import ui
from syncplay.ConfigurationGetter import ConfigurationGetter   
from syncplay.ConfigurationGetter import InvalidConfigValue 
from syncplay.ui.GuiConfiguration import GuiConfiguration
import sys

class SyncplayClient(object):
    def __init__(self):
        self._prepareArguments()
        self.interface = ui.getUi(graphical = not self.args.no_gui)
        self._checkAndSaveConfiguration()

    def _checkAndSaveConfiguration(self):
        try:
            self._promptForMissingArguments()
            self.argsGetter.saveValuesIntoConfigFile()
        except InvalidConfigValue:
            self._checkAndSaveConfiguration()
        except GuiConfiguration.WindowClosed:
            sys.exit()
        
    def _prepareArguments(self):
        self.argsGetter = ConfigurationGetter()
        self.args = self.argsGetter.getConfiguration()
        
    def _guiPromptForMissingArguments(self):
        self.args = GuiConfiguration(self.args, self.args.force_gui_prompt).getProcessedConfiguration()
        
    def _promptForMissingArguments(self):
        if(self.args.no_gui):
            if (self.args.host == None):
                self.args.host = self.interface.promptFor(promptName = "Hostname", message = "You must supply hostname on the first run, it's easier through command line arguments.")
            if (self.args.name == None):
                self.args.name = self.interface.promptFor(promptName = "Username", message = "You must supply username on the first run, it's easier through command line arguments.")
        else:
            self._guiPromptForMissingArguments()