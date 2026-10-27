import unittest
from unittest.mock import MagicMock, patch

from tests.conftest import make_room_manager, make_watcher


class TestFindFreeUsername(unittest.TestCase):
    def test_unique_name_unchanged(self):
        manager = make_room_manager()
        self.assertEqual(manager.findFreeUsername("alice"), "alice")

    def test_collision_appends_underscore(self):
        manager = make_room_manager()
        from syncplay.server import Room
        room = Room("testroom", None)
        w1 = make_watcher(name="alice")
        room.addWatcher(w1)
        manager._rooms["testroom"] = room
        result = manager.findFreeUsername("alice")
        self.assertEqual(result, "alice_")

    def test_multiple_collisions(self):
        manager = make_room_manager()
        from syncplay.server import Room
        room = Room("testroom", None)
        w1 = make_watcher(name="alice")
        w2 = make_watcher(name="alice_")
        room.addWatcher(w1)
        room.addWatcher(w2)
        manager._rooms["testroom"] = room
        result = manager.findFreeUsername("alice")
        self.assertEqual(result, "alice__")

    def test_trailing_underscores_stripped_before_collision(self):
        """If username ends with _ and collides, trailing underscores are stripped first."""
        manager = make_room_manager()
        from syncplay.server import Room
        room = Room("testroom", None)
        w1 = make_watcher(name="alice_")
        room.addWatcher(w1)
        manager._rooms["testroom"] = room
        result = manager.findFreeUsername("alice_")
        self.assertEqual(result, "alice")

    def test_truncation(self):
        manager = make_room_manager()
        long_name = "a" * 100
        result = manager.findFreeUsername(long_name, maxUsernameLength=16)
        self.assertLessEqual(len(result), 17)


class TestMoveWatcher(unittest.TestCase):
    def test_move_creates_room(self):
        manager = make_room_manager()
        watcher = make_watcher(name="alice")
        watcher._room = None
        manager.moveWatcher(watcher, "newroom")
        self.assertIn("newroom", manager._rooms)
        self.assertEqual(watcher.getRoom().getName(), "newroom")

    def test_move_between_rooms(self):
        manager = make_room_manager()
        watcher = make_watcher(name="alice")
        watcher._room = None
        manager.moveWatcher(watcher, "room1")
        manager.moveWatcher(watcher, "room2")
        self.assertEqual(watcher.getRoom().getName(), "room2")

    def test_creates_controlled_room(self):
        manager = make_room_manager()
        watcher = make_watcher(name="alice")
        watcher._room = None
        from syncplay.server import ControlledRoom
        manager.moveWatcher(watcher, "+myroom:AABBCCDDEE11")
        self.assertIsInstance(manager._rooms["+myroom:AABBCCDDEE11"], ControlledRoom)


class TestRemoveWatcher(unittest.TestCase):
    def test_remove_cleans_empty_room(self):
        manager = make_room_manager()
        watcher = make_watcher(name="alice")
        watcher._room = None
        manager.moveWatcher(watcher, "testroom")
        manager.removeWatcher(watcher)
        self.assertNotIn("testroom", manager._rooms)

    def test_remove_keeps_room_with_watchers(self):
        manager = make_room_manager()
        w1 = make_watcher(name="alice")
        w2 = make_watcher(name="bob")
        w1._room = None
        w2._room = None
        manager.moveWatcher(w1, "testroom")
        manager.moveWatcher(w2, "testroom")
        manager.removeWatcher(w1)
        self.assertIn("testroom", manager._rooms)
        self.assertEqual(len(manager._rooms["testroom"].getWatchers()), 1)


class TestGetRoom(unittest.TestCase):
    def test_creates_room_on_demand(self):
        manager = make_room_manager()
        from syncplay.server import Room
        room = manager._getRoom("newroom")
        self.assertIsInstance(room, Room)
        self.assertIn("newroom", manager._rooms)

    def test_returns_existing_room(self):
        manager = make_room_manager()
        room1 = manager._getRoom("myroom")
        room2 = manager._getRoom("myroom")
        self.assertIs(room1, room2)

    def test_creates_controlled_room_for_controlled_name(self):
        manager = make_room_manager()
        from syncplay.server import ControlledRoom
        room = manager._getRoom("+myroom:AABBCCDDEE11")
        self.assertIsInstance(room, ControlledRoom)


class TestBroadcast(unittest.TestCase):
    def test_broadcast_reaches_all_rooms(self):
        manager = make_room_manager()
        w1 = make_watcher(name="alice")
        w2 = make_watcher(name="bob")
        w1._room = None
        w2._room = None
        manager.moveWatcher(w1, "room1")
        manager.moveWatcher(w2, "room2")
        received = []
        manager.broadcast(w1, lambda w: received.append(w.getName()))
        self.assertIn("alice", received)
        self.assertIn("bob", received)

    def test_broadcast_room_only_reaches_same_room(self):
        manager = make_room_manager()
        w1 = make_watcher(name="alice")
        w2 = make_watcher(name="bob")
        w1._room = None
        w2._room = None
        manager.moveWatcher(w1, "room1")
        manager.moveWatcher(w2, "room2")
        received = []
        manager.broadcastRoom(w1, lambda w: received.append(w.getName()))
        self.assertIn("alice", received)
        self.assertNotIn("bob", received)


class TestPublicRoomManager(unittest.TestCase):
    def test_broadcast_isolated_to_room(self):
        from syncplay.server import PublicRoomManager
        manager = PublicRoomManager()
        w1 = make_watcher(name="alice")
        w2 = make_watcher(name="bob")
        w1._room = None
        w2._room = None
        manager.moveWatcher(w1, "room1")
        manager.moveWatcher(w2, "room2")
        received = []
        manager.broadcast(w1, lambda w: received.append(w.getName()))
        self.assertIn("alice", received)
        self.assertNotIn("bob", received)

    def test_get_all_watchers_isolated(self):
        from syncplay.server import PublicRoomManager
        manager = PublicRoomManager()
        w1 = make_watcher(name="alice")
        w2 = make_watcher(name="bob")
        w1._room = None
        w2._room = None
        manager.moveWatcher(w1, "room1")
        manager.moveWatcher(w2, "room2")
        watchers = manager.getAllWatchersForUser(w1)
        names = [w.getName() for w in watchers]
        self.assertIn("alice", names)
        self.assertNotIn("bob", names)


class TestExportRooms(unittest.TestCase):
    def test_export_returns_rooms_dict(self):
        manager = make_room_manager()
        watcher = make_watcher(name="alice")
        watcher._room = None
        manager.moveWatcher(watcher, "testroom")
        rooms = manager.exportRooms()
        self.assertIn("testroom", rooms)


if __name__ == "__main__":
    unittest.main()
