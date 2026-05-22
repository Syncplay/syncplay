import time
import unittest
from unittest.mock import MagicMock, patch, PropertyMock


class TestJSONCommandProtocolHandleMessages(unittest.TestCase):
    def _make_protocol(self):
        from syncplay.protocols import JSONCommandProtocol
        proto = JSONCommandProtocol()
        proto.handleHello = MagicMock()
        proto.handleSet = MagicMock()
        proto.handleState = MagicMock()
        proto.handleList = MagicMock()
        proto.handleChat = MagicMock()
        proto.handleError = MagicMock()
        proto.handleTLS = MagicMock()
        proto.dropWithError = MagicMock()
        proto.showDebugMessage = MagicMock()
        return proto

    def test_hello_dispatch(self):
        proto = self._make_protocol()
        proto.handleMessages({"Hello": {"username": "alice"}})
        proto.handleHello.assert_called_once_with({"username": "alice"})

    def test_set_dispatch(self):
        proto = self._make_protocol()
        proto.handleMessages({"Set": {"room": {"name": "test"}}})
        proto.handleSet.assert_called_once()

    def test_state_dispatch(self):
        proto = self._make_protocol()
        proto.handleMessages({"State": {"playstate": {}}})
        proto.handleState.assert_called_once()

    def test_list_dispatch(self):
        proto = self._make_protocol()
        proto.handleMessages({"List": None})
        proto.handleList.assert_called_once()

    def test_chat_dispatch(self):
        proto = self._make_protocol()
        proto.handleMessages({"Chat": {"message": "hi"}})
        proto.handleChat.assert_called_once()

    def test_error_dispatch(self):
        proto = self._make_protocol()
        proto.handleMessages({"Error": {"message": "oops"}})
        proto.handleError.assert_called_once()

    def test_tls_dispatch(self):
        proto = self._make_protocol()
        proto.handleMessages({"TLS": {"startTLS": "send"}})
        proto.handleTLS.assert_called_once()

    def test_unknown_command_drops(self):
        proto = self._make_protocol()
        proto.handleMessages({"UnknownCmd": {}})
        proto.dropWithError.assert_called_once()


class TestSyncClientProtocolExtractHello(unittest.TestCase):
    def _make_client_protocol(self):
        from syncplay.protocols import SyncClientProtocol
        client = MagicMock()
        client.ui = MagicMock()
        proto = SyncClientProtocol(client)
        return proto

    def test_full_extraction(self):
        proto = self._make_client_protocol()
        hello = {
            "username": "alice",
            "room": {"name": "testroom"},
            "version": "1.2.255",
            "realversion": "1.7.4",
            "motd": "Welcome",
            "features": {"chat": True}
        }
        username, roomName, version, motd, features = proto._extractHelloArguments(hello)
        self.assertEqual(username, "alice")
        self.assertEqual(roomName, "testroom")
        self.assertEqual(version, "1.7.4")
        self.assertEqual(motd, "Welcome")
        self.assertEqual(features, {"chat": True})

    def test_missing_fields(self):
        proto = self._make_client_protocol()
        hello = {}
        username, roomName, version, motd, features = proto._extractHelloArguments(hello)
        self.assertIsNone(username)
        self.assertIsNone(roomName)
        self.assertIsNone(version)
        self.assertIsNone(motd)
        self.assertIsNone(features)

    def test_realversion_overrides_version(self):
        proto = self._make_client_protocol()
        hello = {"version": "1.2.255", "realversion": "1.7.4"}
        _, _, version, _, _ = proto._extractHelloArguments(hello)
        self.assertEqual(version, "1.7.4")


class TestSyncClientProtocolExtractStatePlaystate(unittest.TestCase):
    def _make_client_protocol(self):
        from syncplay.protocols import SyncClientProtocol
        proto = SyncClientProtocol(MagicMock())
        return proto

    def test_full_extraction(self):
        proto = self._make_client_protocol()
        state = {
            "playstate": {
                "position": 42.5,
                "paused": True,
                "doSeek": False,
                "setBy": "alice"
            }
        }
        position, paused, doSeek, setBy = proto._extractStatePlaystateArguments(state)
        self.assertEqual(position, 42.5)
        self.assertTrue(paused)
        self.assertFalse(doSeek)
        self.assertEqual(setBy, "alice")

    def test_missing_fields_have_defaults(self):
        proto = self._make_client_protocol()
        state = {"playstate": {}}
        position, paused, doSeek, setBy = proto._extractStatePlaystateArguments(state)
        self.assertEqual(position, 0)
        self.assertIsNone(paused)
        self.assertIsNone(doSeek)
        self.assertIsNone(setBy)


class TestSyncClientProtocolSendHello(unittest.TestCase):
    def test_sends_hello_structure(self):
        from syncplay.protocols import SyncClientProtocol
        client = MagicMock()
        client.getUsername.return_value = "alice"
        client.getPassword.return_value = None
        client.getRoom.return_value = "testroom"
        client.getFeatures.return_value = {"chat": True}
        proto = SyncClientProtocol(client)
        proto.sendMessage = MagicMock()
        proto.sendHello()
        call_args = proto.sendMessage.call_args[0][0]
        self.assertIn("Hello", call_args)
        hello = call_args["Hello"]
        self.assertEqual(hello["username"], "alice")
        self.assertEqual(hello["room"], {"name": "testroom"})
        self.assertEqual(hello["version"], "1.2.255")
        self.assertIn("realversion", hello)
        self.assertIn("features", hello)

    def test_includes_password_when_set(self):
        from syncplay.protocols import SyncClientProtocol
        client = MagicMock()
        client.getUsername.return_value = "alice"
        client.getPassword.return_value = "secret"
        client.getRoom.return_value = "testroom"
        client.getFeatures.return_value = {}
        proto = SyncClientProtocol(client)
        proto.sendMessage = MagicMock()
        proto.sendHello()
        hello = proto.sendMessage.call_args[0][0]["Hello"]
        self.assertEqual(hello["password"], "secret")


class TestSyncClientProtocolSetUser(unittest.TestCase):
    def test_joined_event(self):
        from syncplay.protocols import SyncClientProtocol
        client = MagicMock()
        proto = SyncClientProtocol(client)
        users = {"alice": {"room": {"name": "testroom"}, "event": {"joined": True}}}
        proto._SetUser(users)
        client.userlist.addUser.assert_called_once_with("alice", "testroom", None)

    def test_left_event(self):
        from syncplay.protocols import SyncClientProtocol
        client = MagicMock()
        proto = SyncClientProtocol(client)
        users = {"alice": {"room": {"name": "testroom"}, "event": {"left": True}}}
        proto._SetUser(users)
        client.removeUser.assert_called_once_with("alice")

    def test_mod_event(self):
        from syncplay.protocols import SyncClientProtocol
        client = MagicMock()
        proto = SyncClientProtocol(client)
        users = {"alice": {"room": {"name": "testroom"}, "file": {"name": "video.mkv"}}}
        proto._SetUser(users)
        client.userlist.modUser.assert_called_once()


class TestSyncServerProtocolExtractHello(unittest.TestCase):
    def _make_server_protocol(self):
        from syncplay.protocols import SyncServerProtocol
        factory = MagicMock()
        proto = SyncServerProtocol(factory)
        proto.transport = MagicMock()
        proto.transport.getPeer.return_value = MagicMock(host="127.0.0.1")
        return proto

    def test_full_extraction(self):
        proto = self._make_server_protocol()
        hello = {
            "username": "alice",
            "password": "secret",
            "room": {"name": "testroom"},
            "version": "1.2.255",
            "realversion": "1.7.4",
            "features": {"chat": True}
        }
        username, password, roomName, version, features = proto._extractHelloArguments(hello)
        self.assertEqual(username, "alice")
        self.assertEqual(password, "secret")
        self.assertEqual(roomName, "testroom")
        self.assertEqual(version, "1.7.4")
        self.assertEqual(features, {"chat": True})

    def test_missing_fields(self):
        proto = self._make_server_protocol()
        hello = {}
        username, password, roomName, version, features = proto._extractHelloArguments(hello)
        self.assertIsNone(username)
        self.assertIsNone(password)
        self.assertIsNone(roomName)
        self.assertIsNone(version)
        self.assertIsNone(features)

    def test_username_stripped(self):
        proto = self._make_server_protocol()
        hello = {"username": "  alice  ", "room": {"name": "testroom"}, "version": "1.7.4"}
        username, _, _, _, _ = proto._extractHelloArguments(hello)
        self.assertEqual(username, "alice")


class TestSyncServerProtocolGetFeatures(unittest.TestCase):
    def _make_server_protocol(self):
        from syncplay.protocols import SyncServerProtocol
        factory = MagicMock()
        proto = SyncServerProtocol(factory)
        proto.transport = MagicMock()
        return proto

    def test_features_for_modern_client(self):
        proto = self._make_server_protocol()
        proto._version = "1.7.4"
        features = proto.getFeatures()
        self.assertTrue(features["sharedPlaylists"])
        self.assertTrue(features["chat"])
        self.assertTrue(features["readiness"])
        self.assertTrue(features["managedRooms"])

    def test_features_for_old_client(self):
        proto = self._make_server_protocol()
        proto._version = "1.2.0"
        features = proto.getFeatures()
        self.assertFalse(features["sharedPlaylists"])
        self.assertFalse(features["chat"])
        self.assertFalse(features["readiness"])
        self.assertFalse(features["managedRooms"])


class TestPingService(unittest.TestCase):
    def test_initial_state(self):
        from syncplay.protocols import PingService
        ps = PingService()
        self.assertEqual(ps.getRtt(), 0)
        self.assertEqual(ps.getLastForwardDelay(), 0)

    def test_new_timestamp(self):
        from syncplay.protocols import PingService
        ps = PingService()
        ts = ps.newTimestamp()
        self.assertAlmostEqual(ts, time.time(), delta=1.0)

    def test_receive_message_updates_rtt(self):
        from syncplay.protocols import PingService
        ps = PingService()
        ts = time.time() - 0.1
        ps.receiveMessage(ts, 0.05)
        self.assertGreater(ps.getRtt(), 0)
        self.assertGreater(ps.getLastForwardDelay(), 0)

    def test_receive_message_no_timestamp(self):
        from syncplay.protocols import PingService
        ps = PingService()
        ps.receiveMessage(None, 0.05)
        self.assertEqual(ps.getRtt(), 0)

    def test_negative_rtt_ignored(self):
        from syncplay.protocols import PingService
        ps = PingService()
        ps.receiveMessage(time.time() + 100, 0.05)
        self.assertLessEqual(ps.getRtt(), 0)
        self.assertEqual(ps.getLastForwardDelay(), 0)

    def test_moving_average(self):
        from syncplay.protocols import PingService
        ps = PingService()
        for _ in range(5):
            ts = time.time() - 0.1
            ps.receiveMessage(ts, 0.05)
        self.assertGreater(ps._avrRtt, 0)

    def test_forward_delay_when_sender_behind(self):
        """When senderRtt < self._rtt, fd includes the difference."""
        from syncplay.protocols import PingService
        ps = PingService()
        ts = time.time() - 0.2
        ps.receiveMessage(ts, 0.05)
        fd = ps.getLastForwardDelay()
        self.assertGreater(fd, ps._avrRtt / 2)


if __name__ == "__main__":
    unittest.main()
