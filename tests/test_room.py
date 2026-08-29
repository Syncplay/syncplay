import time
import unittest
from unittest.mock import MagicMock, patch

from tests.conftest import make_room, make_controlled_room, make_watcher


class TestRoomCreation(unittest.TestCase):
    def test_defaults(self):
        """Room starts paused at position 0."""
        room = make_room("testroom")
        self.assertTrue(room.isPaused())
        self.assertFalse(room.isPlaying())
        self.assertEqual(room.getName(), "testroom")
        self.assertTrue(room.isEmpty())
        self.assertEqual(room.getPlaylist(), [])
        self.assertIsNone(room.getPlaylistIndex())
        self.assertIsNone(room.getSetBy())

    def test_str_returns_name(self):
        room = make_room("myroom")
        self.assertEqual(str(room), "myroom")


class TestRoomPersistence(unittest.TestCase):
    def test_not_persistent_without_db(self):
        room = make_room("testroom", dbhandle=None)
        self.assertFalse(room.isPersistent())
        self.assertFalse(room.roomsCanPersist())

    def test_persistent_with_db(self):
        room = make_room("testroom", dbhandle=MagicMock())
        self.assertTrue(room.isPersistent())

    def test_temp_room_not_persistent(self):
        room = make_room("testroom-temp", dbhandle=MagicMock())
        self.assertTrue(room.isMarkedAsTemporary())
        self.assertFalse(room.isPersistent())

    def test_temp_in_controlled_name(self):
        room = make_room("testroom-temp:AABBCCDDEE11", dbhandle=MagicMock())
        self.assertTrue(room.isMarkedAsTemporary())

    def test_permanent_flag(self):
        room = make_room("testroom")
        self.assertFalse(room.isPermanent())
        self.assertTrue(room.isNotPermanent())
        room.setPermanent(True)
        self.assertTrue(room.isPermanent())
        self.assertFalse(room.isNotPermanent())


class TestRoomPlayState(unittest.TestCase):
    def test_set_paused(self):
        from syncplay.server import Room
        room = make_room()
        room.setPaused(Room.STATE_PLAYING)
        self.assertTrue(room.isPlaying())
        self.assertFalse(room.isPaused())

    def test_set_paused_back(self):
        from syncplay.server import Room
        room = make_room()
        room.setPaused(Room.STATE_PLAYING)
        room.setPaused(Room.STATE_PAUSED)
        self.assertTrue(room.isPaused())

    def test_set_paused_tracks_setby(self):
        room = make_room()
        watcher = make_watcher(name="alice")
        room.setPaused(setBy=watcher)
        self.assertEqual(room.getSetBy(), watcher)


class TestRoomPosition(unittest.TestCase):
    def test_initial_position(self):
        room = make_room()
        pos = room.getPosition()
        self.assertAlmostEqual(pos, 0, delta=0.5)

    def test_set_position(self):
        room = make_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        room.setPosition(42.0)
        self.assertAlmostEqual(room._position, 42.0)

    def test_position_advances_when_playing(self):
        """When playing with no watchers, position should advance with time."""
        from syncplay.server import Room
        room = make_room()
        room._position = 10.0
        room._lastUpdate = time.time() - 2.0
        room.setPaused(Room.STATE_PLAYING)
        pos = room.getPosition()
        self.assertGreater(pos, 10.0)

    def test_position_static_when_paused(self):
        room = make_room()
        room._position = 10.0
        room._lastUpdate = time.time() - 5.0
        pos = room.getPosition()
        self.assertAlmostEqual(pos, 10.0, delta=0.5)


class TestRoomWatchers(unittest.TestCase):
    def test_add_watcher(self):
        room = make_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        self.assertFalse(room.isEmpty())
        self.assertEqual(len(room.getWatchers()), 1)
        self.assertEqual(watcher.getRoom(), room)

    def test_remove_watcher(self):
        room = make_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        room.removeWatcher(watcher)
        self.assertTrue(room.isEmpty())
        self.assertIsNone(watcher.getRoom())

    def test_remove_resets_position_when_empty_non_persistent(self):
        room = make_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        room._position = 50.0
        room.removeWatcher(watcher)
        self.assertEqual(room._position, 0)

    def test_add_watcher_syncs_position_when_others_present(self):
        room = make_room()
        w1 = make_watcher(name="alice")
        room.addWatcher(w1)
        room._position = 30.0
        w2 = make_watcher(name="bob")
        room.addWatcher(w2)
        self.assertIsNotNone(w2._position)

    def test_remove_nonexistent_watcher(self):
        """Removing a watcher not in the room should be a no-op."""
        room = make_room()
        watcher = make_watcher(name="alice")
        room.removeWatcher(watcher)


class TestRoomPlaylist(unittest.TestCase):
    def test_set_and_get_playlist(self):
        room = make_room()
        room.setPlaylist(["file1.mkv", "file2.mkv"])
        self.assertEqual(room.getPlaylist(), ["file1.mkv", "file2.mkv"])

    def test_set_and_get_playlist_index(self):
        room = make_room()
        room.setPlaylistIndex(2)
        self.assertEqual(room.getPlaylistIndex(), 2)

    def test_playlist_empty(self):
        room = make_room()
        self.assertTrue(room.isPlaylistEmpty())
        room.setPlaylist(["file1.mkv"])
        self.assertFalse(room.isPlaylistEmpty())


class TestRoomSanitizeFilename(unittest.TestCase):
    def test_replaces_blacklisted_chars(self):
        room = make_room()
        result = room.sanitizeFilename('file<>:name.mkv')
        self.assertNotIn("<", result)
        self.assertNotIn(">", result)
        self.assertNotIn(":", result)
        self.assertIn("_", result)

    def test_replaces_control_chars(self):
        room = make_room()
        result = room.sanitizeFilename("file\x01name.mkv")
        self.assertNotIn("\x01", result)


class TestRoomLoadRoom(unittest.TestCase):
    def test_load_room_from_tuple(self):
        room = make_room()
        room.loadRoom(("loaded_room", "file1\nfile2", 1, 42.5, 1000))
        self.assertEqual(room.getName(), "loaded_room")
        self.assertEqual(room.getPlaylist(), ["file1", "file2"])
        self.assertEqual(room.getPlaylistIndex(), 1)
        self.assertEqual(room._position, 42.5)

    def test_load_room_empty_playlist(self):
        room = make_room()
        room.loadRoom(("loaded_room", "", 0, 0, 0))
        self.assertEqual(room.getPlaylist(), [])


class TestRoomCanControl(unittest.TestCase):
    def test_regular_room_anyone_can_control(self):
        room = make_room()
        watcher = make_watcher(name="alice")
        self.assertTrue(room.canControl(watcher))

    def test_get_controllers_empty(self):
        room = make_room()
        self.assertEqual(room.getControllers(), [])


class TestControlledRoom(unittest.TestCase):
    def test_creation(self):
        room = make_controlled_room()
        self.assertTrue(room.isPaused())
        self.assertTrue(room.isEmpty())

    def test_can_control_requires_controller(self):
        room = make_controlled_room()
        watcher = make_watcher(name="alice")
        self.assertFalse(room.canControl(watcher))

    def test_add_controller(self):
        room = make_controlled_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        room.addController(watcher)
        self.assertTrue(room.canControl(watcher))

    def test_set_paused_requires_controller(self):
        from syncplay.server import Room
        room = make_controlled_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        room.setPaused(Room.STATE_PLAYING, setBy=watcher)
        self.assertTrue(room.isPaused())

    def test_set_paused_by_controller(self):
        from syncplay.server import Room
        room = make_controlled_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        room.addController(watcher)
        room.setPaused(Room.STATE_PLAYING, setBy=watcher)
        self.assertTrue(room.isPlaying())

    def test_set_position_requires_controller(self):
        room = make_controlled_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        room.setPosition(50.0, setBy=watcher)
        self.assertAlmostEqual(room._position, 0, delta=0.5)

    def test_set_position_by_controller(self):
        room = make_controlled_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        room.addController(watcher)
        room.setPosition(50.0, setBy=watcher)
        self.assertAlmostEqual(room._position, 50.0)

    def test_set_playlist_requires_controller(self):
        room = make_controlled_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        room.setPlaylist(["file.mkv"], setBy=watcher)
        self.assertEqual(room.getPlaylist(), [])

    def test_set_playlist_by_controller(self):
        room = make_controlled_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        room.addController(watcher)
        room.setPlaylist(["file.mkv"], setBy=watcher)
        self.assertEqual(room.getPlaylist(), ["file.mkv"])

    def test_set_playlist_index_requires_controller(self):
        room = make_controlled_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        room.setPlaylistIndex(3, setBy=watcher)
        self.assertIsNone(room.getPlaylistIndex())

    def test_set_playlist_index_by_controller(self):
        room = make_controlled_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        room.addController(watcher)
        room.setPlaylistIndex(3, setBy=watcher)
        self.assertEqual(room.getPlaylistIndex(), 3)

    def test_remove_watcher_removes_controller(self):
        room = make_controlled_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        room.addController(watcher)
        self.assertTrue(room.canControl(watcher))
        room.removeWatcher(watcher)
        self.assertFalse(room.canControl(watcher))

    def test_get_controllers_returns_dict(self):
        room = make_controlled_room()
        self.assertIsInstance(room.getControllers(), dict)


if __name__ == "__main__":
    unittest.main()
