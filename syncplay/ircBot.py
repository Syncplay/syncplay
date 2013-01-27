from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from syncplay import utils

class ColorCode(object):
    NORMAL = chr(15)
    BOLD = chr(2)
    RED = chr(3) + "5"
    BLUE = chr(3) + "12"

'''
@author Uriziel
@author HarHar
'''
class Bot(object):
    def __init__(self, server='irc.rizon.net', port=6667, nick='SyncBot', channel='', functions=[]):
        '''
        functions - dict of functions that can be used from the bot:
        functions = {
            "pause": lambda setBy, state: None,
            "getRooms": lambda: ["",],
            "setRoomPosition": lambda setBy, seconds 0: None,
            "getRoomPosition": lambda room: 0,
            "getRoomUsers": lambda room: [{"nick": "", "file": "", "duration": 0},],
            "isRoomPaused": lambda room: True,                            
            }
        '''
        self.factory = BotFactory(self, channel.encode("ascii", "replace"), nick.encode("ascii", "replace"))
        self.proto = None
        self.server = server
        self.port = port
        self._functions = functions
        
    def start(self):
        reactor.connectTCP(self.server, self.port, self.factory)
        
    def registerProto(self, proto):
        self.proto = proto

    def takeAction(self, action, user):
        if(action == "help" or action == "h"):
            v = (ColorCode.BOLD, ColorCode.NORMAL)
            return "{}Available commands:{} !rooms / !roominfo [room] / !playpause (or aliases: !r, !ri [room], !p).".format(*v)
        elif(action == "rooms" or action == "r"):
            return self.__listRooms()
        elif(action.startswith("roominfo") or action.startswith("ri")):
            return self.__getRoomInfo(action)
        elif(action == "playpause" or action == "p"):
            return self.__playpause(user)
        else:
            return "{}Error!{} Unknown command".format(ColorCode.RED, ColorCode.NORMAL)

    def sp_joined(self, who, room):
        msg ="{}<{}>{} has joined the room: `{}`".format(ColorCode.BOLD, who, ColorCode.NORMAL, room)
        self._sendChanMessage(msg)

    def sp_left(self, who, room):
        msg ="{}<{}>{} has left the room: `{}`".format(ColorCode.BOLD, who, ColorCode.NORMAL, room)
        self._sendChanMessage(msg)

    def sp_unpaused(self, who, room):
        msg ="{}<{}>{} has unpaused (in room `{}`)".format(ColorCode.BOLD, who, ColorCode.NORMAL, room)
        self._sendChanMessage(msg)
        
    def sp_paused(self, who, room):
        msg ="{}<{}>{} has paused (in room `{}`)".format(ColorCode.BOLD, who, ColorCode.NORMAL, room)
        self._sendChanMessage(msg)
        
    def sp_fileplaying(self, who, filename, room):
        if filename:
            msg ="{}<{}>{} is playing {} (in room `{}`)".format(ColorCode.BOLD, who, ColorCode.NORMAL, filename, room)
            self._sendChanMessage(msg)
            
    def sp_seek(self, who, fromTime, toTime, room):
        v = (ColorCode.BOLD, who, ColorCode.NORMAL, utils.formatTime(fromTime), utils.formatTime(toTime), room,)
        msg ="{}<{}>{} has jumped from {} to {} (in room `{}`)".format(*v)
        self._sendChanMessage(msg)

    def __playpause(self, user):
        rooms = self._functions["getRooms"]()
        for room in rooms:
            users = self._functions["getRoomUsers"](room)
            for u in users:
                if u['nick'] == user:
                    paused = self._functions["isRoomPaused"](room)
                    self._functions["pause"](user, not (paused))
                    return "<{}> {} the room: `{}`".format(ColorCode.BOLD, user, ColorCode.NORMAL, "paused" if paused else "unpaused", room)
        return "{}Error!{} Your nick was not found on the server.".format(ColorCode.RED, ColorCode.NORMAL)

    def __listRooms(self):
        rooms = self._functions["getRooms"]()
        if(len(rooms) >= 3):
            v = ("`, `".join(rooms[:-1]), rooms[-1])
            return "Currently the Syncplay server hosts viewing sessions as follows: `{}` and ultimately `{}`.".format(*v)
        elif(len(rooms) == 2):
            return "Currently the Syncplay server hosts viewing sessions as follows: `{}` and `{}`.".format(rooms[0], rooms[1])
        elif(len(rooms) == 1):
            return "Currently the Syncplay server hosts one viewing session called `{}`".format(rooms[0])
        else:
            return "{}Notice:{} No rooms have been found on server".format(ColorCode.BLUE, ColorCode.NORMAL)

    def __getListOfFiles(self, users):
        files = []
        for u in users:
            if [u["file"], u["duration"]] not in files:
                files.append([u["file"], u["duration"]])
        return files

    def __getUserlist(self, room):
        users = self._functions["getRoomUsers"](room)
        position = self._functions["getRoomPosition"](room)
        paused = "Paused" if self._functions["isRoomPaused"](room) else "Playing"
        files = self.__getListOfFiles(users)
        message = ""
        for f in files:
            if (f[0] == None):
                message += "No file:\n"
            else:
                v = (
                     ColorCode.BOLD, paused, ColorCode.NORMAL, 
                     utils.formatTime(position),
                     utils.formatTime(f[1]), f[0]
                     )
                message += "{}<{}>{} [{}/{}] {}\n".format(*v)
            u = [u['nick'] for u in users if f[0] == u['file'] and f[1] == u['duration']]
            if (len(u) > 1):
                message += "Played by: <{}> and <{}>.\n".format(">, <".join(u[:-1]), u[-1])
            else:
                message += "Played by {} alone.\n".format(u[0])
        return message

    def __getRoomInfo(self, action):
        if(action.startswith("rooms")):
            room = action.replace("rooms", "", 1)
        else:
            room = action.replace("ri", "", 1)
        room = room.strip()
        if('' == room):
            return  "{}Usage:{} !roominfo [room]".format(ColorCode.BLUE, ColorCode.NORMAL)
        rooms = self._functions["getRooms"]()
        if(not room in rooms):
            return "{}Error!{} Room does not exists.".format(ColorCode.RED, ColorCode.NORMAL)
        message = self.__getUserlist(room)
        return message
        
    def _sendChanMessage(self, msg):
        if(self.proto):
            self.proto.sendChanMessage(msg)
        
class BotProto(irc.IRCClient):
    def __init__(self, bot, nickname):
        self.nickname = nickname
        self.bot = bot
        self.bot.registerProto(self)
        
    def signedOn(self):
        self.join(self.factory.channel)

    def joined(self, channel):
        self.msg(channel, "Syncplay IRC Bot - I'm all fired up!")

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]
        isActionMessage = channel == self.nickname or msg.startswith(self.nickname + ":") or msg.startswith("!") or msg.startswith(".") 
        if isActionMessage:
            action = msg.replace(self.nickname + ":", "")
            action = msg.lstrip(".!")
            reply = self.bot.takeAction(action.lower(), user)
            for line in reply.splitlines():
                self.msg(channel, line)

    def sendChanMessage(self, msg):
        self.msg(self.factory.channel, msg)

class BotFactory(protocol.ClientFactory):
    def __init__(self, bot, channel, nickname):
        self.channel = channel
        self.nickname = nickname
        self.bot = bot
        
    def buildProtocol(self, addr):
        p = BotProto(self.bot, self.nickname)
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "IRC Bot connection failed, please check your configuration"
