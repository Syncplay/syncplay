import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def make_room(name="testroom", dbhandle=None):
    from syncplay.server import Room
    return Room(name, dbhandle)


def make_controlled_room(name="+testroom:AABBCCDDEE11", dbhandle=None):
    from syncplay.server import ControlledRoom
    return ControlledRoom(name, dbhandle)


def make_watcher(server=None, connector=None, name="testuser"):
    from syncplay.server import Watcher
    if server is None:
        server = MagicMock()
        server.disableReady = False
    if connector is None:
        connector = MagicMock()
        connector.isLogged.return_value = True
        connector.getFeatures.return_value = {"uiMode": "GUI"}
        connector.getVersion.return_value = "1.7.4"
        connector.meetsMinVersion.return_value = True
    with patch('syncplay.server.reactor'):
        watcher = Watcher(server, connector, name)
    return watcher


def make_room_manager(roomsdbfile=None, permanentRooms=None):
    from syncplay.server import RoomManager
    if permanentRooms is None:
        permanentRooms = []
    with patch('syncplay.server.RoomDBManager'):
        manager = RoomManager(roomsdbfile=roomsdbfile, permanentRooms=permanentRooms)
    return manager
