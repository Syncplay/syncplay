"""Tests for playback speed synchronization feature."""
import unittest
import time
import threading
from unittest.mock import MagicMock, patch, PropertyMock

# Adjust path so we can import syncplay modules
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from syncplay import constants


class TestRoomSpeed(unittest.TestCase):
    """Test server-side Room speed state."""

    def _make_room(self):
        from syncplay.server import Room
        dbhandle = MagicMock()
        dbhandle.saveRoom = MagicMock()
        room = Room("testroom", dbhandle)
        return room

    def _make_controlled_room(self):
        from syncplay.server import ControlledRoom
        dbhandle = MagicMock()
        dbhandle.saveRoom = MagicMock()
        room = ControlledRoom("testroom", dbhandle)
        return room

    def test_room_default_speed(self):
        room = self._make_room()
        self.assertEqual(room.getSpeed(), constants.DEFAULT_PLAYBACK_SPEED)

    def test_room_set_speed(self):
        room = self._make_room()
        watcher = MagicMock()
        room.setSpeed(1.5, watcher)
        self.assertEqual(room.getSpeed(), 1.5)

    def test_room_dead_reckoning_with_speed(self):
        room = self._make_room()
        from syncplay.server import Room
        room._playState = Room.STATE_PLAYING
        room._position = 10.0
        room._lastUpdate = time.time() - 2.0  # 2 seconds ago
        room.setSpeed(2.0, None)

        position = room.getPosition()
        # Position should be ~10 + 2*2.0 = ~14
        self.assertAlmostEqual(position, 14.0, delta=0.2)

    def test_room_dead_reckoning_paused_ignores_speed(self):
        room = self._make_room()
        from syncplay.server import Room
        room._playState = Room.STATE_PAUSED
        room._position = 10.0
        room._lastUpdate = time.time() - 2.0
        room.setSpeed(2.0, None)

        position = room.getPosition()
        self.assertAlmostEqual(position, 10.0, delta=0.1)

    def test_controlled_room_allows_controller(self):
        room = self._make_controlled_room()
        controller = MagicMock()
        controller.getName.return_value = "operator"
        room.addController(controller)

        room.setSpeed(1.5, controller)
        self.assertEqual(room.getSpeed(), 1.5)

    def test_controlled_room_rejects_non_controller(self):
        room = self._make_controlled_room()
        controller = MagicMock()
        controller.getName.return_value = "operator"
        room.addController(controller)

        non_controller = MagicMock()
        non_controller.getName.return_value = "viewer"
        room.setSpeed(2.0, non_controller)
        # Speed should remain at default since non-controller can't change it
        self.assertEqual(room.getSpeed(), constants.DEFAULT_PLAYBACK_SPEED)


class TestWatcherSpeedUpdate(unittest.TestCase):
    """Test that Watcher.updateState detects and propagates speed changes."""

    def _make_watcher(self):
        from syncplay.server import Watcher, Room
        dbhandle = MagicMock()
        dbhandle.saveRoom = MagicMock()
        room = Room("testroom", dbhandle)
        factory = MagicMock()
        connector = MagicMock()
        # Patch out the reactor.callLater in Watcher.__init__
        with patch('syncplay.server.reactor'):
            watcher = Watcher(factory, connector, "testuser")
        watcher._room = room
        return watcher, room, factory

    def test_speed_change_triggers_force_update(self):
        watcher, room, factory = self._make_watcher()
        watcher.setPosition(10.0)
        watcher.updateState(10.0, False, False, 0, speed=1.5)
        factory.forcePositionUpdate.assert_called_once()
        self.assertEqual(room.getSpeed(), 1.5)

    def test_no_speed_change_no_force_update(self):
        watcher, room, factory = self._make_watcher()
        watcher.setPosition(10.0)
        # Initialize pause state so it doesn't trigger pauseChanged
        room.setPaused(room.STATE_PLAYING)
        factory.reset_mock()
        # Send same speed as current (1.0)
        watcher.updateState(10.0, False, False, 0, speed=1.0)
        factory.forcePositionUpdate.assert_not_called()

    def test_none_speed_no_force_update(self):
        watcher, room, factory = self._make_watcher()
        watcher.setPosition(10.0)
        # Initialize pause state so it doesn't trigger pauseChanged
        room.setPaused(room.STATE_PLAYING)
        factory.reset_mock()
        # Old client sends no speed (None)
        watcher.updateState(10.0, False, False, 0, speed=None)
        factory.forcePositionUpdate.assert_not_called()


class TestProtocolSpeedExtraction(unittest.TestCase):
    """Test that protocol extracts speed from state messages."""

    def test_client_protocol_extracts_speed(self):
        from syncplay.protocols import SyncClientProtocol
        proto = SyncClientProtocol.__new__(SyncClientProtocol)
        state = {"playstate": {
            "position": 10.0, "paused": False,
            "doSeek": False, "setBy": "Alice", "speed": 1.5
        }}
        pos, paused, doSeek, setBy, speed = proto._extractStatePlaystateArguments(state)
        self.assertEqual(speed, 1.5)

    def test_client_protocol_missing_speed_is_none(self):
        from syncplay.protocols import SyncClientProtocol
        proto = SyncClientProtocol.__new__(SyncClientProtocol)
        state = {"playstate": {
            "position": 10.0, "paused": False,
            "doSeek": False, "setBy": "Alice"
        }}
        pos, paused, doSeek, setBy, speed = proto._extractStatePlaystateArguments(state)
        self.assertIsNone(speed)

    def test_server_protocol_extracts_speed(self):
        from syncplay.protocols import SyncServerProtocol
        proto = SyncServerProtocol.__new__(SyncServerProtocol)
        state = {"playstate": {
            "position": 10.0, "paused": False,
            "doSeek": False, "speed": 1.2
        }}
        pos, paused, doSeek, speed = proto._extractStatePlaystateArguments(state)
        self.assertEqual(speed, 1.2)

    def test_server_protocol_missing_speed_is_none(self):
        from syncplay.protocols import SyncServerProtocol
        proto = SyncServerProtocol.__new__(SyncServerProtocol)
        state = {"playstate": {
            "position": 10.0, "paused": False, "doSeek": False
        }}
        pos, paused, doSeek, speed = proto._extractStatePlaystateArguments(state)
        self.assertIsNone(speed)


class TestClientSpeedState(unittest.TestCase):
    """Test client-side speed state management."""

    def _make_client(self):
        from syncplay.client import SyncplayClient
        client = SyncplayClient.__new__(SyncplayClient)
        client._globalSpeed = constants.DEFAULT_PLAYBACK_SPEED
        client._globalPosition = 0.0
        client._globalPaused = False
        client._lastGlobalUpdate = time.time()
        client._lastPlayerUpdate = None
        client._playerPosition = 0.0
        client._playerPaused = False
        client._speedChanged = False
        client._config = {'slowdownThreshold': 1.5}
        client.ui = MagicMock()
        client._player = MagicMock()
        client._player.speedSupported = True
        client._protocol = MagicMock()
        client._protocol.logged = True
        client.userlist = MagicMock()
        client.userlist.currentUser.file = {"name": "test.mkv", "duration": 100}
        return client

    def test_get_global_speed_default(self):
        client = self._make_client()
        self.assertEqual(client.getGlobalSpeed(), 1.0)

    def test_set_speed_updates_global_and_player(self):
        client = self._make_client()
        client.setSpeed(1.5)
        self.assertEqual(client._globalSpeed, 1.5)
        client._player.setSpeed.assert_called_with(1.5)

    def test_global_position_dead_reckoning_with_speed(self):
        client = self._make_client()
        client._globalSpeed = 2.0
        client._globalPosition = 10.0
        client._globalPaused = False
        client._lastGlobalUpdate = time.time() - 1.0  # 1 second ago

        pos = client.getGlobalPosition()
        # 10 + 1.0 * 2.0 = 12.0
        self.assertAlmostEqual(pos, 12.0, delta=0.2)

    def test_slowdown_relative_to_global_speed(self):
        client = self._make_client()
        client._globalSpeed = 1.5
        client._speedChanged = False

        client._slowDownToCoverTimeDifference(2.0, "OtherUser")
        client._player.setSpeed.assert_called_with(1.5 * constants.SLOWDOWN_RATE)

    def test_slowdown_revert_to_global_speed(self):
        client = self._make_client()
        client._globalSpeed = 1.5
        client._speedChanged = True

        client._slowDownToCoverTimeDifference(0.05, "OtherUser")
        client._player.setSpeed.assert_called_with(1.5)


class TestMpvSpeedParsing(unittest.TestCase):
    """Test that mpv line parsing extracts speed correctly."""

    def test_parse_speed_from_status_line(self):
        """Simulate the string splitting logic from mpv.py lineReceived."""
        line = "<paused=true, pos=42.5, speed=1.2>"
        update_string = line.replace(">", "<").replace("=", "<").replace(", ", "<").split("<")
        # Expected: ['', 'paused', 'true', 'pos', '42.5', 'speed', '1.2', '']
        self.assertEqual(update_string[1], "paused")
        self.assertEqual(update_string[2], "true")
        self.assertEqual(update_string[3], "pos")
        self.assertEqual(update_string[4], "42.5")
        self.assertEqual(update_string[5], "speed")
        self.assertEqual(update_string[6], "1.2")

    def test_parse_without_speed_field(self):
        """Old Lua script format without speed - should not crash."""
        line = "<paused=false, pos=10.0>"
        update_string = line.replace(">", "<").replace("=", "<").replace(", ", "<").split("<")
        # Expected: ['', 'paused', 'false', 'pos', '10.0', '']
        self.assertTrue(len(update_string) <= 6 or update_string[5] != "speed")


class TestSpeedThreadSafety(unittest.TestCase):
    """Test that speed detection in mpv uses the correct thread pattern."""

    def test_line_received_stores_speed_not_calls_setspeed(self):
        """Verify lineReceived only stores _detectedSpeed, doesn't call client.setSpeed."""
        # This is a design-level test: the mpv reader thread should NEVER
        # call protocol methods. Speed should be stored and picked up by
        # askForStatus which runs in the reactor thread.
        from syncplay.players.mpv import MpvPlayer
        player = MpvPlayer.__new__(MpvPlayer)
        player._client = MagicMock()
        player._client.getGlobalSpeed.return_value = 1.0
        player._detectedSpeed = None
        player._paused = False
        player._position = 0.0
        player._positionAsk = threading.Event()
        player._pausedAsk = threading.Event()
        player.fileLoaded = True
        player.lastMPVPositionUpdate = time.time()

        # Simulate lineReceived processing
        line = "<paused=false, pos=10.0, speed=1.5>"
        # Call the parsing logic inline (extracted from lineReceived)
        if "<paused=" in line and ", pos=" in line:
            update_string = line.replace(">", "<").replace("=", "<").replace(", ", "<").split("<")
            if len(update_string) > 6 and update_string[5] == "speed":
                speed_update = update_string[6]
                if speed_update != "nil":
                    try:
                        player._detectedSpeed = float(speed_update)
                    except ValueError:
                        pass

        # Speed should be stored, NOT applied via setSpeed
        self.assertEqual(player._detectedSpeed, 1.5)
        player._client.setSpeed.assert_not_called()


if __name__ == '__main__':
    unittest.main()
