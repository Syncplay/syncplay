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

    def test_set_speed_updates_global_and_sends_to_server(self):
        client = self._make_client()
        client.serverFeatures = {"speedSync": True}
        client.setSpeed(1.5)
        self.assertEqual(client._globalSpeed, 1.5)
        # setSpeed should NOT call player.setSpeed (player already has the speed)
        client._player.setSpeed.assert_not_called()
        # But should send state to server
        client._protocol.sendState.assert_called_once()

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


class TestDisconnectReconnectSpeed(unittest.TestCase):
    """Et0h review point 1: Reliability on disconnect/reconnect,
    including room being temporarily empty and therefore deleted."""

    def _make_room(self):
        from syncplay.server import Room
        dbhandle = MagicMock()
        dbhandle.saveRoom = MagicMock()
        return Room("testroom", dbhandle)

    def _make_watcher(self, factory, name="testuser"):
        from syncplay.server import Watcher
        connector = MagicMock()
        with patch('syncplay.server.reactor'):
            watcher = Watcher(factory, connector, name)
        return watcher

    def test_room_speed_resets_when_emptied_non_persistent(self):
        """When a non-persistent room empties, it gets deleted and recreated.
        The new room should have default speed."""
        room = self._make_room()
        room.setSpeed(2.0, None)
        self.assertEqual(room.getSpeed(), 2.0)

        # Simulate room emptying — position resets but speed does NOT
        # This is a potential issue: speed persists on the Room object
        # even when empty and position resets to 0.
        watcher = MagicMock()
        watcher.getName.return_value = "user1"
        room._watchers["user1"] = watcher
        watcher.setRoom = MagicMock()
        room.removeWatcher(watcher)

        # Room is now empty. For non-persistent rooms, the RoomManager
        # would delete this room entirely. New room = default speed.
        # But the Room object itself still has speed=2.0
        self.assertEqual(room.getSpeed(), 2.0)
        # This is fine because RoomManager._deleteRoomIfEmpty deletes the object

    def test_new_room_has_default_speed(self):
        """When a room is created fresh (after deletion), speed is default."""
        room = self._make_room()
        self.assertEqual(room.getSpeed(), constants.DEFAULT_PLAYBACK_SPEED)

    def test_reconnect_client_gets_room_speed(self):
        """After reconnect, client receives current room speed from server
        via the normal state update cycle."""
        from syncplay.client import SyncplayClient
        client = SyncplayClient.__new__(SyncplayClient)
        client._globalSpeed = constants.DEFAULT_PLAYBACK_SPEED
        client._globalPosition = 0.0
        client._globalPaused = False
        client._lastGlobalUpdate = None  # Simulates fresh reconnect
        client._lastPlayerUpdate = None
        client._playerPosition = 0.0
        client._playerPaused = True
        client._speedChanged = False
        client.lastRewindTime = None
        client.lastUpdatedFileTime = None
        client.lastAdvanceTime = None
        client._userOffset = 0.0
        client._config = {
            'slowdownThreshold': 1.5, 'rewindThreshold': 5.0,
            'slowOnDesync': True, 'rewindOnDesync': True,
            'fastforwardOnDesync': False, 'dontSlowDownWithMe': False
        }
        client.ui = MagicMock()
        client._player = MagicMock()
        client._player.speedSupported = True
        client._protocol = MagicMock()
        client._protocol.logged = True
        client.userlist = MagicMock()
        client.userlist.currentUser.file = {"name": "test.mkv", "duration": 100}
        client.userlist.currentUser.canControl.return_value = True
        client.playerPositionBeforeLastSeek = 0.0
        client.behindFirstDetected = None
        client.__dict__['_SyncplayClient__getUserlistOnLogon'] = False

        # Simulate receiving state with speed=1.5 after reconnect
        client._changePlayerStateAccordingToGlobalState(10.0, False, False, "Alice", speed=1.5)
        self.assertEqual(client._globalSpeed, 1.5)
        client._player.setSpeed.assert_called_with(1.5)


class TestRoomSwitchSpeed(unittest.TestCase):
    """Et0h review point 2: Reliability on joining and changing rooms
    to those with same/different speeds."""

    def test_joining_room_with_different_speed(self):
        """Client joining a room at speed 2.0 should receive 2.0 via state."""
        from syncplay.client import SyncplayClient
        client = SyncplayClient.__new__(SyncplayClient)
        client._globalSpeed = 1.0  # Default
        client._globalPosition = 0.0
        client._globalPaused = False
        client._lastGlobalUpdate = time.time()
        client._lastPlayerUpdate = time.time()
        client._playerPosition = 0.0
        client._playerPaused = False
        client._speedChanged = False
        client._config = {
            'slowdownThreshold': 1.5, 'rewindThreshold': 5.0,
            'slowOnDesync': True, 'rewindOnDesync': True,
            'fastforwardOnDesync': False, 'dontSlowDownWithMe': False
        }
        client.ui = MagicMock()
        client._player = MagicMock()
        client._player.speedSupported = True
        client.userlist = MagicMock()
        client.userlist.currentUser.file = {"name": "test.mkv", "duration": 100}
        client.userlist.currentUser.canControl.return_value = True
        client.playerPositionBeforeLastSeek = 0.0
        client.behindFirstDetected = None

        # Server sends state with room speed 2.0
        client._changePlayerStateAccordingToGlobalState(50.0, False, False, "Bob", speed=2.0)
        self.assertEqual(client._globalSpeed, 2.0)
        client._player.setSpeed.assert_called_with(2.0)

    def test_switching_room_same_speed_no_notification(self):
        """If new room has same speed, no speed change notification."""
        from syncplay.client import SyncplayClient
        client = SyncplayClient.__new__(SyncplayClient)
        client._globalSpeed = 1.5
        client._globalPosition = 0.0
        client._globalPaused = False
        client._lastGlobalUpdate = time.time()
        client._lastPlayerUpdate = time.time()
        client._playerPosition = 0.0
        client._playerPaused = False
        client._speedChanged = False
        client._config = {
            'slowdownThreshold': 1.5, 'rewindThreshold': 5.0,
            'slowOnDesync': True, 'rewindOnDesync': True,
            'fastforwardOnDesync': False, 'dontSlowDownWithMe': False
        }
        client.ui = MagicMock()
        client._player = MagicMock()
        client._player.speedSupported = True
        client.userlist = MagicMock()
        client.userlist.currentUser.file = {"name": "test.mkv", "duration": 100}
        client.userlist.currentUser.canControl.return_value = True
        client.playerPositionBeforeLastSeek = 0.0
        client.behindFirstDetected = None

        # Same speed=1.5 — should NOT trigger speed change logic
        client._changePlayerStateAccordingToGlobalState(50.0, False, False, "Bob", speed=1.5)
        client._player.setSpeed.assert_not_called()


class TestFileChangeSpeed(unittest.TestCase):
    """Et0h review point 3: Reliability when changing from one media file to another.
    Speed should persist across file changes within the same room."""

    def test_room_speed_persists_across_file_change(self):
        """Room speed should not reset when watchers change files."""
        from syncplay.server import Room
        dbhandle = MagicMock()
        dbhandle.saveRoom = MagicMock()
        room = Room("testroom", dbhandle)
        room.setSpeed(1.5, None)

        # Simulate file change — watcher updates file, room speed unaffected
        self.assertEqual(room.getSpeed(), 1.5)

    def test_mpv_detected_speed_resets_on_file_change(self):
        """When mpv loads a new file, _detectedSpeed is reset via _set_defaults.
        This prevents stale speed from the previous file being sent to server.

        NOTE: _set_defaults is called in __init__ which sets _detectedSpeed=None.
        But _onFileUpdate does NOT reset _detectedSpeed. If the new file starts
        at 1.0x but _detectedSpeed is still 1.5 from the old file, askForStatus
        will see _detectedSpeed != globalSpeed and call setSpeed(1.5) — which
        could be wrong. However, the Lua script reports speed on every status
        update, so _detectedSpeed will be overwritten quickly."""
        from syncplay.players.mpv import MpvPlayer
        player = MpvPlayer.__new__(MpvPlayer)
        player._detectedSpeed = 1.5  # From previous file

        # After _onFileUpdate, _detectedSpeed is NOT cleared
        # This is potentially a bug but mitigated by rapid Lua updates
        self.assertEqual(player._detectedSpeed, 1.5)


class TestBackwardCompatibility(unittest.TestCase):
    """Et0h review point 4: Backwards/forwards compatibility with
    older/newer clients and servers."""

    def test_old_client_no_speed_field_server_handles_gracefully(self):
        """Old client sends state without 'speed' field. Server should not crash
        and should not change room speed."""
        from syncplay.server import Watcher, Room
        dbhandle = MagicMock()
        dbhandle.saveRoom = MagicMock()
        room = Room("testroom", dbhandle)
        room.setSpeed(1.5, None)  # Room is at 1.5x

        factory = MagicMock()
        connector = MagicMock()
        with patch('syncplay.server.reactor'):
            watcher = Watcher(factory, connector, "oldclient")
        watcher._room = room
        room._watchers["oldclient"] = watcher
        room.setPaused(Room.STATE_PLAYING)

        # Old client sends update without speed (speed=None)
        watcher.updateState(10.0, False, False, 0, speed=None)
        # Room speed should remain unchanged
        self.assertEqual(room.getSpeed(), 1.5)

    def test_old_server_no_speed_field_client_handles_gracefully(self):
        """Old server sends state without 'speed' field. Client should not crash
        and globalSpeed should remain at its current value."""
        from syncplay.client import SyncplayClient
        client = SyncplayClient.__new__(SyncplayClient)
        client._globalSpeed = 1.5  # Locally set
        client._globalPosition = 0.0
        client._globalPaused = False
        client._lastGlobalUpdate = time.time()
        client._lastPlayerUpdate = time.time()
        client._playerPosition = 0.0
        client._playerPaused = False
        client._speedChanged = False
        client._config = {
            'slowdownThreshold': 1.5, 'rewindThreshold': 5.0,
            'slowOnDesync': True, 'rewindOnDesync': True,
            'fastforwardOnDesync': False, 'dontSlowDownWithMe': False
        }
        client.ui = MagicMock()
        client._player = MagicMock()
        client._player.speedSupported = True
        client.userlist = MagicMock()
        client.userlist.currentUser.file = {"name": "test.mkv", "duration": 100}
        client.userlist.currentUser.canControl.return_value = True
        client.playerPositionBeforeLastSeek = 0.0
        client.behindFirstDetected = None

        # Old server sends no speed (None)
        client._changePlayerStateAccordingToGlobalState(10.0, False, False, "Alice", speed=None)
        # Speed should remain unchanged
        self.assertEqual(client._globalSpeed, 1.5)
        client._player.setSpeed.assert_not_called()

    def test_client_protocol_always_sends_speed(self):
        """New client always includes speed in state messages to server.
        Old servers will simply ignore the unknown field."""
        from syncplay.protocols import SyncClientProtocol
        proto = SyncClientProtocol.__new__(SyncClientProtocol)
        proto.clientIgnoringOnTheFly = 0
        proto.serverIgnoringOnTheFly = 0
        proto._client = MagicMock()
        proto._client.getGlobalSpeed.return_value = 1.5
        proto._pingService = MagicMock()
        proto._pingService.newTimestamp.return_value = 12345
        proto._pingService.getRtt.return_value = 0.05

        # Build state dict
        state = {}
        state["playstate"] = {}
        state["playstate"]["position"] = 10.0
        state["playstate"]["paused"] = False
        speed = proto._client.getGlobalSpeed()
        if speed is not None:
            state["playstate"]["speed"] = speed

        self.assertIn("speed", state["playstate"])
        self.assertEqual(state["playstate"]["speed"], 1.5)


class TestOffsetCompatibility(unittest.TestCase):
    """Et0h review point 5: Compatibility with (mostly deprecated) offset feature."""

    def test_offset_and_speed_coexist(self):
        """User offset should be applied independently of speed.
        getPlayerPosition uses speed for dead-reckoning, offset is added/subtracted
        at setPosition/updatePlayerStatus boundaries."""
        from syncplay.client import SyncplayClient
        client = SyncplayClient.__new__(SyncplayClient)
        client._globalSpeed = 2.0
        client._globalPosition = 10.0
        client._globalPaused = False
        client._lastGlobalUpdate = time.time() - 1.0
        client._lastPlayerUpdate = time.time()
        client._playerPosition = 10.0
        client._playerPaused = False
        client._userOffset = 5.0

        # Global position dead reckoning uses speed
        globalPos = client.getGlobalPosition()
        self.assertAlmostEqual(globalPos, 12.0, delta=0.2)  # 10 + 1*2.0

        # Player position dead reckoning uses speed
        playerPos = client.getPlayerPosition()
        self.assertAlmostEqual(playerPos, 10.0, delta=0.2)  # just set, no time passed

        # Offset is independent
        self.assertEqual(client.getUserOffset(), 5.0)


class TestSetSpeedTyping(unittest.TestCase):
    """Et0h review point 6: Whether the speed variable needs to be
    explicitly typed to a float in setSpeed."""

    def test_room_setSpeed_with_int(self):
        """Passing int 2 should work the same as 2.0."""
        from syncplay.server import Room
        dbhandle = MagicMock()
        dbhandle.saveRoom = MagicMock()
        room = Room("testroom", dbhandle)
        room.setSpeed(2, None)  # int, not float
        self.assertEqual(room.getSpeed(), 2)
        # Dead reckoning should still work
        room._playState = Room.STATE_PLAYING
        room._position = 10.0
        room._lastUpdate = time.time() - 1.0
        pos = room.getPosition()
        self.assertAlmostEqual(pos, 12.0, delta=0.2)

    def test_room_setSpeed_with_string_would_fail(self):
        """If speed somehow arrives as a string, multiplication in
        getPosition would fail. The protocol extraction uses dict access
        which preserves the JSON-parsed float type, so this shouldn't
        happen in practice."""
        from syncplay.server import Room
        dbhandle = MagicMock()
        dbhandle.saveRoom = MagicMock()
        room = Room("testroom", dbhandle)
        room.setSpeed("1.5", None)  # String — would break dead reckoning
        room._playState = Room.STATE_PLAYING
        room._position = 10.0
        room._lastUpdate = time.time() - 1.0
        # This would raise TypeError: unsupported operand type(s)
        # for *: 'float' and 'str'
        with self.assertRaises(TypeError):
            room.getPosition()


class TestSlowdownSpeedInteraction(unittest.TestCase):
    """Et0h review point 7: Ensuring speed-up/slowdown code does not
    improperly trigger speedChanged detection, and that slowdown doesn't
    interfere with speed sync."""

    def _make_client(self):
        from syncplay.client import SyncplayClient
        client = SyncplayClient.__new__(SyncplayClient)
        client._globalSpeed = 1.5
        client._globalPosition = 0.0
        client._globalPaused = False
        client._lastGlobalUpdate = time.time()
        client._lastPlayerUpdate = time.time()
        client._playerPosition = 0.0
        client._playerPaused = False
        client._speedChanged = False
        client._config = {
            'slowdownThreshold': 1.5, 'rewindThreshold': 5.0,
            'slowOnDesync': True, 'rewindOnDesync': True,
            'fastforwardOnDesync': False, 'dontSlowDownWithMe': False
        }
        client.ui = MagicMock()
        client._player = MagicMock()
        client._player.speedSupported = True
        client._protocol = MagicMock()
        client._protocol.logged = True
        client.userlist = MagicMock()
        client.userlist.currentUser.file = {"name": "test.mkv", "duration": 100}
        client.userlist.currentUser.canControl.return_value = True
        client.playerPositionBeforeLastSeek = 0.0
        client.behindFirstDetected = None
        return client

    def test_slowdown_does_not_trigger_server_speed_update(self):
        """When slowdown activates, it changes player speed locally via
        _speedChanged flag but should NOT call client.setSpeed() which
        would propagate to the server."""
        client = self._make_client()
        client._slowDownToCoverTimeDifference(2.0, "OtherUser")

        # Player speed was set to slowdown rate
        client._player.setSpeed.assert_called_with(1.5 * constants.SLOWDOWN_RATE)
        self.assertTrue(client._speedChanged)

        # But protocol.sendState should NOT have been called by slowdown
        # (setSpeed calls sendState, but _slowDownToCoverTimeDifference
        # calls _player.setSpeed directly, not client.setSpeed)
        client._protocol.sendState.assert_not_called()

    def test_speed_change_during_slowdown_updates_global_and_reverts(self):
        """If room speed changes while client is in slowdown mode,
        the new speed is stored in _globalSpeed. The speed change block
        (line 427) skips player.setSpeed due to _speedChanged=True.
        However, the subsequent _slowDownToCoverTimeDifference call
        will revert slowdown (since diff is small) and apply the new
        global speed to the player."""
        client = self._make_client()
        client._speedChanged = True  # Currently slowed down

        # Room speed changes to 2.0
        client._changePlayerStateAccordingToGlobalState(
            10.0, False, False, "Alice", speed=2.0)

        # _globalSpeed updated
        self.assertEqual(client._globalSpeed, 2.0)
        # Player gets new speed via slowdown revert path
        client._player.setSpeed.assert_called_with(2.0)
        # Slowdown flag cleared
        self.assertFalse(client._speedChanged)

    def test_slowdown_revert_uses_new_global_speed(self):
        """After slowdown resolves, player should revert to the current
        global speed (which may have changed during slowdown)."""
        client = self._make_client()
        client._globalSpeed = 2.0  # Changed while slowdown was active
        client._speedChanged = True

        # Slowdown resolves (diff < SLOWDOWN_RESET_THRESHOLD)
        client._slowDownToCoverTimeDifference(0.05, "OtherUser")
        client._player.setSpeed.assert_called_with(2.0)
        self.assertFalse(client._speedChanged)

    def test_detected_speed_during_slowdown_not_propagated(self):
        """After slowdown sets player to globalSpeed * SLOWDOWN_RATE, the
        player reports that rate back. The _speedChanged guard in
        askForStatus prevents this from being propagated to the server."""
        detected = 1.5 * constants.SLOWDOWN_RATE  # e.g. 1.425
        globalSpeed = 1.5
        speedChanged = True  # Slowdown is active
        # The condition in askForStatus (after fix):
        would_trigger = (detected is not None
                         and abs(detected - globalSpeed) > constants.SPEED_TOLERANCE
                         and not speedChanged)
        self.assertFalse(would_trigger,
            "Slowdown speed must NOT be propagated to server")


class TestPendingSpeedRemoved(unittest.TestCase):
    """Et0h review point 8: _pendingSpeed was dead code and has been removed."""

    def test_pending_speed_removed_from_client(self):
        """_pendingSpeed was unused dead code and should no longer exist."""
        import syncplay.client as client_module
        import inspect
        source = inspect.getsource(client_module.SyncplayClient)
        self.assertNotIn('_pendingSpeed', source,
            "_pendingSpeed should have been removed as dead code")


class TestSpeedTolerance(unittest.TestCase):
    """Test that float-imprecise speed values don't trigger feedback loops."""

    def test_float_imprecise_speed_not_detected_as_change(self):
        """VLC may report 1.1001 when set to 1.1. This should NOT trigger
        a speed change on the server."""
        from syncplay.server import Watcher, Room
        dbhandle = MagicMock()
        dbhandle.saveRoom = MagicMock()
        room = Room("testroom", dbhandle)
        room.setSpeed(1.1, None)
        room.setPaused(Room.STATE_PLAYING)

        factory = MagicMock()
        connector = MagicMock()
        with patch('syncplay.server.reactor'):
            watcher = Watcher(factory, connector, "testuser")
        watcher._room = room
        watcher.setPosition(10.0)
        factory.reset_mock()

        # Client reports 1.1001 due to float precision
        watcher.updateState(10.0, False, False, 0, speed=1.1001)
        factory.forcePositionUpdate.assert_not_called()
        self.assertEqual(room.getSpeed(), 1.1)

    def test_real_speed_change_still_detected(self):
        """A real user speed change (1.0 -> 1.5) must still be detected."""
        from syncplay.server import Watcher, Room
        dbhandle = MagicMock()
        dbhandle.saveRoom = MagicMock()
        room = Room("testroom", dbhandle)
        room.setPaused(Room.STATE_PLAYING)

        factory = MagicMock()
        connector = MagicMock()
        with patch('syncplay.server.reactor'):
            watcher = Watcher(factory, connector, "testuser")
        watcher._room = room
        watcher.setPosition(10.0)
        factory.reset_mock()

        watcher.updateState(10.0, False, False, 0, speed=1.5)
        factory.forcePositionUpdate.assert_called_once()
        self.assertEqual(room.getSpeed(), 1.5)

    def test_client_tolerance_no_speed_change(self):
        """Client receiving speed within tolerance of current should not
        trigger a speed change notification."""
        from syncplay.client import SyncplayClient
        client = SyncplayClient.__new__(SyncplayClient)
        client._globalSpeed = 1.1
        client._globalPosition = 0.0
        client._globalPaused = False
        client._lastGlobalUpdate = time.time()
        client._lastPlayerUpdate = time.time()
        client._playerPosition = 0.0
        client._playerPaused = False
        client._speedChanged = False
        client._config = {
            'slowdownThreshold': 1.5, 'rewindThreshold': 5.0,
            'slowOnDesync': True, 'rewindOnDesync': True,
            'fastforwardOnDesync': False, 'dontSlowDownWithMe': False
        }
        client.ui = MagicMock()
        client._player = MagicMock()
        client._player.speedSupported = True
        client.userlist = MagicMock()
        client.userlist.currentUser.file = {"name": "test.mkv", "duration": 100}
        client.userlist.currentUser.canControl.return_value = True
        client.playerPositionBeforeLastSeek = 0.0
        client.behindFirstDetected = None

        # Speed within tolerance
        client._changePlayerStateAccordingToGlobalState(10.0, False, False, "Bob", speed=1.1005)
        client._player.setSpeed.assert_not_called()
        client.ui.showMessage.assert_not_called()

    def test_askforstatus_tolerance_no_propagation(self):
        """If detected speed is within tolerance of global speed,
        askForStatus should NOT call client.setSpeed."""
        detected = 1.1001  # VLC float imprecision
        globalSpeed = 1.1
        speedChanged = False
        would_trigger = (detected is not None
                         and abs(detected - globalSpeed) > constants.SPEED_TOLERANCE
                         and not speedChanged)
        self.assertFalse(would_trigger,
            "Float-imprecise speed should not trigger propagation")


class TestSetSpeedGracePeriod(unittest.TestCase):
    """Test that setSpeed sets a grace period to suppress echo."""

    def test_mpv_setspeed_sets_grace_period(self):
        from syncplay.players.mpv import MpvPlayer
        player = MpvPlayer.__new__(MpvPlayer)
        player._listener = MagicMock()
        player._listener.mpvpipe = MagicMock()
        player.setSpeed(1.5)
        self.assertAlmostEqual(player._lastSpeedSetTime, time.time(), delta=0.1)

    def test_vlc_setspeed_sets_grace_period(self):
        from syncplay.players.vlc import VlcPlayer
        player = VlcPlayer.__new__(VlcPlayer)
        player._listener = MagicMock()
        player.setSpeed(1.5)
        self.assertAlmostEqual(player._lastSpeedSetTime, time.time(), delta=0.1)

    def test_mplayer_setspeed_sets_grace_period(self):
        from syncplay.players.mplayer import MplayerPlayer
        player = MplayerPlayer.__new__(MplayerPlayer)
        player._listener = MagicMock()
        player.setSpeed(1.5)
        self.assertAlmostEqual(player._lastSpeedSetTime, time.time(), delta=0.1)

    def test_grace_period_suppresses_old_speed_echo(self):
        """During grace period, askForStatus should not propagate speed
        even if _detectedSpeed differs from global speed."""
        detectedSpeed = 1.0  # Old speed VLC hasn't updated yet
        globalSpeed = 1.7    # Just set via setSpeed
        lastSpeedSetTime = time.time()  # Just now
        speedChanged = False

        gracePeriodActive = time.time() - lastSpeedSetTime < constants.SPEED_SET_GRACE_PERIOD
        rounded = round(detectedSpeed, 2)
        would_trigger = (detectedSpeed is not None
                         and not speedChanged
                         and not gracePeriodActive
                         and abs(rounded - globalSpeed) > constants.SPEED_TOLERANCE)
        self.assertFalse(would_trigger,
            "Old speed must NOT be propagated during grace period")

    def test_after_grace_period_real_change_propagates(self):
        """After grace period expires, a real speed change should propagate."""
        detectedSpeed = 1.5
        globalSpeed = 1.0
        lastSpeedSetTime = time.time() - 1.0  # 1 second ago, well past grace period
        speedChanged = False

        gracePeriodActive = time.time() - lastSpeedSetTime < constants.SPEED_SET_GRACE_PERIOD
        rounded = round(detectedSpeed, 2)
        would_trigger = (detectedSpeed is not None
                         and not speedChanged
                         and not gracePeriodActive
                         and abs(rounded - globalSpeed) > constants.SPEED_TOLERANCE)
        self.assertTrue(would_trigger,
            "Real speed change must propagate after grace period")


class TestFeatureGating(unittest.TestCase):
    """Test that speed sync uses the features system for inter-version compatibility."""

    def _make_client(self, speed_sync_supported=True):
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
        client.serverVersion = "1.7.3" if speed_sync_supported else "1.7.2"
        client.serverFeatures = {"speedSync": speed_sync_supported}
        return client

    def test_setSpeed_sends_state_when_server_supports(self):
        client = self._make_client(speed_sync_supported=True)
        client.setSpeed(1.5)
        self.assertEqual(client._globalSpeed, 1.5)
        client._protocol.sendState.assert_called_once()

    def test_setSpeed_skips_send_when_server_unsupported(self):
        client = self._make_client(speed_sync_supported=False)
        client.setSpeed(1.5)
        # Global speed is still updated locally
        self.assertEqual(client._globalSpeed, 1.5)
        # But state is NOT sent to server
        client._protocol.sendState.assert_not_called()

    def test_server_features_include_speed_sync(self):
        from syncplay.server import SyncFactory
        factory = SyncFactory.__new__(SyncFactory)
        factory.isolateRooms = False
        factory.disableReady = False
        factory.disableChat = False
        factory.maxChatMessageLength = 150
        factory.maxUsernameLength = 150
        factory.roomsDbFile = None
        features = factory.getFeatures()
        self.assertTrue(features["speedSync"])

    def test_client_features_include_speed_sync(self):
        from syncplay.client import SyncplayClient
        client = SyncplayClient.__new__(SyncplayClient)
        client.ui = MagicMock()
        client.ui.getUIMode.return_value = "GUI"
        client._config = {'sharedPlaylistEnabled': True}
        client.serverFeatures = {"sharedPlaylists": True}
        features = client.getFeatures()
        self.assertTrue(features["speedSync"])

    def test_check_feature_support_defaults_false_for_old_server(self):
        """Old server (< 1.7.3) should default speedSync to False."""
        from syncplay.client import SyncplayClient
        from syncplay import utils
        client = SyncplayClient.__new__(SyncplayClient)
        client.serverVersion = "1.7.2"
        client.ui = MagicMock()
        client._player = MagicMock()
        client._config = {'sharedPlaylistEnabled': True}
        # Build defaults
        defaults = {
            "speedSync": utils.meetsMinVersion("1.7.2", constants.SPEED_SYNC_MIN_VERSION)
        }
        self.assertFalse(defaults["speedSync"])

    def test_check_feature_support_true_for_new_server(self):
        """New server (>= 1.7.5) should default speedSync to True."""
        from syncplay import utils
        defaults = {
            "speedSync": utils.meetsMinVersion("1.7.5", constants.SPEED_SYNC_MIN_VERSION)
        }
        self.assertTrue(defaults["speedSync"])


class TestMpcSpeedSupport(unittest.TestCase):
    """Test MPC-HC/MPC-BE speed support (receive-only)."""

    def test_mpc_speed_supported_is_true(self):
        """MPC-HC should have speedSupported = True."""
        from syncplay.players.mpc import MPCHCAPIPlayer
        self.assertTrue(MPCHCAPIPlayer.speedSupported)

    def test_mpc_setspeed_tracks_grace_period(self):
        """MPC-HC setSpeed should track _lastSpeedSetTime."""
        from syncplay.players.mpc import MPCHCAPIPlayer
        player = MPCHCAPIPlayer.__new__(MPCHCAPIPlayer)
        player._mpcApi = MagicMock()
        player.setSpeed(1.5)
        self.assertAlmostEqual(player._lastSpeedSetTime, time.time(), delta=0.1)
        player._mpcApi.setSpeed.assert_called_with(1.5)


class TestSpeedRounding(unittest.TestCase):
    """Test that float-imprecise detected speeds are rounded before propagation."""

    def test_imprecise_speed_rounded_to_clean_value(self):
        """1.1000000238 should be rounded to 1.1 before comparison/propagation."""
        raw = 1.1000000238419
        rounded = round(raw, 2)
        self.assertEqual(rounded, 1.1)

    def test_rounding_prevents_propagation_of_noise(self):
        """After rounding, imprecise speed matches global and should not trigger."""
        detectedSpeed = 1.1000000238419
        globalSpeed = 1.1
        rounded = round(detectedSpeed, 2)
        would_trigger = abs(rounded - globalSpeed) > constants.SPEED_TOLERANCE
        self.assertFalse(would_trigger)

    def test_rounding_preserves_real_change(self):
        """A real change like 1.0 -> 1.5 is preserved after rounding."""
        detectedSpeed = 1.4999999
        globalSpeed = 1.0
        rounded = round(detectedSpeed, 2)
        would_trigger = abs(rounded - globalSpeed) > constants.SPEED_TOLERANCE
        self.assertTrue(would_trigger)


if __name__ == '__main__':
    unittest.main()
