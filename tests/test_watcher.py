import time
import unittest
from unittest.mock import MagicMock, patch

from tests.conftest import make_watcher, make_room


class TestWatcherCreation(unittest.TestCase):
    def test_initial_state(self):
        watcher = make_watcher(name="alice")
        self.assertEqual(watcher.getName(), "alice")
        self.assertIsNone(watcher.getRoom())
        self.assertIsNone(watcher.getFile())
        self.assertIsNone(watcher._position)
        self.assertIsNone(watcher._ready)

    def test_connector_set_watcher_called(self):
        connector = MagicMock()
        connector.isLogged.return_value = True
        connector.getFeatures.return_value = {"uiMode": "GUI"}
        connector.getVersion.return_value = "1.7.4"
        with patch('syncplay.server.reactor'):
            from syncplay.server import Watcher
            watcher = Watcher(MagicMock(), connector, "alice")
        connector.setWatcher.assert_called_once_with(watcher)


class TestWatcherPosition(unittest.TestCase):
    def test_position_none_when_unset(self):
        watcher = make_watcher(name="alice")
        self.assertIsNone(watcher.getPosition())

    def test_position_set(self):
        room = make_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        watcher.setPosition(42.0)
        self.assertIsNotNone(watcher.getPosition())

    def test_position_paused_stays_still(self):
        room = make_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        watcher.setPosition(10.0)
        watcher._lastUpdatedOn = time.time() - 2.0
        pos = watcher.getPosition()
        self.assertAlmostEqual(pos, 10.0, delta=0.5)

    def test_position_playing_advances(self):
        from syncplay.server import Room
        room = make_room()
        room.setPaused(Room.STATE_PLAYING)
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        watcher.setPosition(10.0)
        watcher._lastUpdatedOn = time.time() - 2.0
        pos = watcher.getPosition()
        self.assertGreater(pos, 10.0)


class TestWatcherComparison(unittest.TestCase):
    def test_lt_by_position(self):
        room = make_room()
        w1 = make_watcher(name="alice")
        w2 = make_watcher(name="bob")
        room.addWatcher(w1)
        room.addWatcher(w2)
        w1.setPosition(10.0)
        w1._file = {"name": "file.mkv"}
        w2.setPosition(20.0)
        w2._file = {"name": "file.mkv"}
        self.assertTrue(w1 < w2)
        self.assertFalse(w2 < w1)

    def test_no_position_not_less(self):
        """Watcher with no position is never less than another."""
        room = make_room()
        w1 = make_watcher(name="alice")
        w2 = make_watcher(name="bob")
        room.addWatcher(w1)
        room.addWatcher(w2)
        w2.setPosition(10.0)
        w2._file = {"name": "file.mkv"}
        self.assertFalse(w1 < w2)

    def test_no_file_not_less(self):
        room = make_room()
        w1 = make_watcher(name="alice")
        w2 = make_watcher(name="bob")
        room.addWatcher(w1)
        room.addWatcher(w2)
        w1.setPosition(5.0)
        w2.setPosition(10.0)
        w2._file = {"name": "file.mkv"}
        self.assertFalse(w1 < w2)

    def test_other_no_position_means_self_is_less(self):
        room = make_room()
        w1 = make_watcher(name="alice")
        w2 = make_watcher(name="bob")
        room.addWatcher(w1)
        room.addWatcher(w2)
        w1.setPosition(10.0)
        w1._file = {"name": "file.mkv"}
        self.assertTrue(w1 < w2)


class TestWatcherReady(unittest.TestCase):
    def test_set_ready(self):
        watcher = make_watcher(name="alice")
        watcher.setReady(True)
        self.assertTrue(watcher.isReady())

    def test_ready_none_when_disabled(self):
        server = MagicMock()
        server.disableReady = True
        watcher = make_watcher(server=server, name="alice")
        watcher.setReady(True)
        self.assertIsNone(watcher.isReady())


class TestWatcherIsController(unittest.TestCase):
    def test_controller_in_controlled_room(self):
        from tests.conftest import make_controlled_room
        room = make_controlled_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        room.addController(watcher)
        self.assertTrue(watcher.isController())

    def test_not_controller_in_controlled_room(self):
        from tests.conftest import make_controlled_room
        room = make_controlled_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        self.assertFalse(watcher.isController())

    def test_not_controller_in_regular_room(self):
        room = make_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        self.assertFalse(watcher.isController())


class TestWatcherUpdateState(unittest.TestCase):
    def test_pause_triggers_room_pause(self):
        from syncplay.server import Room
        room = make_room()
        room.setPaused(Room.STATE_PLAYING)
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        watcher.updateState(position=10.0, paused=True, doSeek=False, messageAge=0.0)
        self.assertTrue(room.isPaused())

    def test_unpause_triggers_room_play(self):
        from syncplay.server import Room
        room = make_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        watcher.updateState(position=10.0, paused=False, doSeek=False, messageAge=0.0)
        self.assertTrue(room.isPlaying())

    def test_position_updated(self):
        room = make_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        watcher.updateState(position=25.0, paused=True, doSeek=False, messageAge=0.0)
        self.assertAlmostEqual(watcher._position, 25.0, delta=0.5)

    def test_message_age_adjusts_position(self):
        room = make_room()
        watcher = make_watcher(name="alice")
        room.addWatcher(watcher)
        watcher.updateState(position=25.0, paused=False, doSeek=False, messageAge=1.0)
        self.assertAlmostEqual(watcher._position, 26.0, delta=0.5)


class TestWatcherDelegation(unittest.TestCase):
    def test_get_version(self):
        connector = MagicMock()
        connector.getVersion.return_value = "1.7.4"
        watcher = make_watcher(connector=connector, name="alice")
        self.assertEqual(watcher.getVersion(), "1.7.4")

    def test_get_features(self):
        connector = MagicMock()
        connector.getFeatures.return_value = {"chat": True, "uiMode": "GUI"}
        watcher = make_watcher(connector=connector, name="alice")
        features = watcher.getFeatures()
        self.assertIn("chat", features)


class TestWatcherFile(unittest.TestCase):
    def test_set_file(self):
        watcher = make_watcher(name="alice")
        room = make_room()
        room.addWatcher(watcher)
        file_info = {"name": "video.mkv", "size": 1000}
        watcher.setFile(file_info)
        self.assertEqual(watcher.getFile()["name"], "video.mkv")

    def test_set_file_truncates_name(self):
        from syncplay import constants
        watcher = make_watcher(name="alice")
        room = make_room()
        room.addWatcher(watcher)
        long_name = "a" * 500 + ".mkv"
        watcher.setFile({"name": long_name})
        self.assertLessEqual(len(watcher.getFile()["name"]), constants.MAX_FILENAME_LENGTH)


if __name__ == "__main__":
    unittest.main()
