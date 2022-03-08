from syncplay.utils import RoomPasswordProvider, NotControlledRoom, RandomStringGenerator, meetsMinVersion, playlistIsValid, truncateText
from twisted.web import server, resource
import syncplay
from syncplay import constants
import json

class WebAPI(resource.Resource):
    isLeaf = True
    def __init__(self, factory):
        self._factory = factory

    def render_GET(self, request):
        # return a simple form for browsers
        return (b"<!DOCTYPE html><html><head><meta charset='utf-8'>"
                b"<title></title></head><body>"
                b"<form method='POST'><label for='room'>Room:</label><input name='room'><br/>"
                b"<label for='url'>URL:</label><input name='url'><br/>"
                b"<input type='submit'/></form></body></html>")

    def render_POST(self, request):
        url = ""
        r = ""
        if b"url" in request.args and b"room" in request.args:
            url = request.args[b"url"][0].decode("utf-8")
            r = request.args[b"room"][0].decode("utf-8")
        else:
            obj = json.load(request.content)
            #print(obj)
            url = obj["text"]
            r = obj["channel_name"]

        room = self._factory._getRoomManager()._getRoom(r)
        pl = room.getPlaylist()
        pl += [url]
        room.setPlaylist(pl)
        #print("Room: " + r + " - adding: " + url)
        for receiver in room.getWatchers():
            receiver.setPlaylist(room.getName(), room.getPlaylist())

        return b"<html>Inserted</html>"

