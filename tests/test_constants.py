import re
import unittest


class TestKeyConstants(unittest.TestCase):
    def test_default_port(self):
        from syncplay.constants import DEFAULT_PORT
        self.assertIsInstance(DEFAULT_PORT, int)
        self.assertGreater(DEFAULT_PORT, 0)
        self.assertLess(DEFAULT_PORT, 65536)

    def test_protocol_timeout(self):
        from syncplay.constants import PROTOCOL_TIMEOUT
        self.assertIsInstance(PROTOCOL_TIMEOUT, (int, float))
        self.assertGreater(PROTOCOL_TIMEOUT, 0)

    def test_server_state_interval(self):
        from syncplay.constants import SERVER_STATE_INTERVAL
        self.assertIsInstance(SERVER_STATE_INTERVAL, (int, float))
        self.assertGreater(SERVER_STATE_INTERVAL, 0)

    def test_ping_moving_average_weight(self):
        from syncplay.constants import PING_MOVING_AVERAGE_WEIGHT
        self.assertGreater(PING_MOVING_AVERAGE_WEIGHT, 0)
        self.assertLess(PING_MOVING_AVERAGE_WEIGHT, 1)

    def test_max_lengths_positive(self):
        from syncplay.constants import (
            MAX_CHAT_MESSAGE_LENGTH, MAX_USERNAME_LENGTH,
            MAX_ROOM_NAME_LENGTH, MAX_FILENAME_LENGTH
        )
        for val in [MAX_CHAT_MESSAGE_LENGTH, MAX_USERNAME_LENGTH,
                    MAX_ROOM_NAME_LENGTH, MAX_FILENAME_LENGTH]:
            self.assertIsInstance(val, int)
            self.assertGreater(val, 0)

    def test_playlist_limits(self):
        from syncplay.constants import PLAYLIST_MAX_CHARACTERS, PLAYLIST_MAX_ITEMS
        self.assertIsInstance(PLAYLIST_MAX_CHARACTERS, int)
        self.assertIsInstance(PLAYLIST_MAX_ITEMS, int)
        self.assertGreater(PLAYLIST_MAX_CHARACTERS, 0)
        self.assertGreater(PLAYLIST_MAX_ITEMS, 0)

    def test_sync_thresholds(self):
        from syncplay.constants import (
            DEFAULT_REWIND_THRESHOLD, DEFAULT_FASTFORWARD_THRESHOLD,
            DIFFERENT_DURATION_THRESHOLD, SEEK_THRESHOLD
        )
        self.assertGreater(DEFAULT_REWIND_THRESHOLD, 0)
        self.assertGreater(DEFAULT_FASTFORWARD_THRESHOLD, 0)
        self.assertGreater(DIFFERENT_DURATION_THRESHOLD, 0)
        self.assertGreater(SEEK_THRESHOLD, 0)

    def test_version_strings_format(self):
        from syncplay.constants import (
            RECENT_CLIENT_THRESHOLD, CONTROLLED_ROOMS_MIN_VERSION,
            USER_READY_MIN_VERSION, SHARED_PLAYLIST_MIN_VERSION,
            CHAT_MIN_VERSION
        )
        for ver in [RECENT_CLIENT_THRESHOLD, CONTROLLED_ROOMS_MIN_VERSION,
                    USER_READY_MIN_VERSION, SHARED_PLAYLIST_MIN_VERSION,
                    CHAT_MIN_VERSION]:
            parts = ver.split(".")
            self.assertEqual(len(parts), 3)
            for part in parts:
                int(part)

    def test_ui_modes(self):
        from syncplay.constants import CONSOLE_UI_MODE, GRAPHICAL_UI_MODE, UNKNOWN_UI_MODE
        self.assertEqual(CONSOLE_UI_MODE, "CLI")
        self.assertEqual(GRAPHICAL_UI_MODE, "GUI")
        self.assertEqual(UNKNOWN_UI_MODE, "Unknown")

    def test_privacy_modes(self):
        from syncplay.constants import (
            PRIVACY_SENDRAW_MODE, PRIVACY_SENDHASHED_MODE,
            PRIVACY_DONTSEND_MODE, PRIVACY_HIDDENFILENAME
        )
        self.assertIsInstance(PRIVACY_SENDRAW_MODE, str)
        self.assertIsInstance(PRIVACY_SENDHASHED_MODE, str)
        self.assertIsInstance(PRIVACY_DONTSEND_MODE, str)
        self.assertIsInstance(PRIVACY_HIDDENFILENAME, str)


class TestGetValueForOS(unittest.TestCase):
    def test_returns_value(self):
        from syncplay.constants import getValueForOS
        result = getValueForOS({"win": "a", "linux": "b", "darwin": "c", "default": "d"})
        self.assertIsNotNone(result)

    def test_default_fallback(self):
        from syncplay.constants import getValueForOS
        result = getValueForOS({"default": "fallback"})
        self.assertIsNotNone(result)

    def test_monospace_font(self):
        from syncplay.constants import MONOSPACE_FONT
        self.assertIsInstance(MONOSPACE_FONT, str)
        self.assertGreater(len(MONOSPACE_FONT), 0)


class TestRegexPatterns(unittest.TestCase):
    def test_parse_time_regex_compiles(self):
        from syncplay.constants import PARSE_TIME_REGEX
        compiled = re.compile(PARSE_TIME_REGEX)
        self.assertIsNotNone(compiled)

    def test_filename_strip_regex_compiles(self):
        from syncplay.constants import FILENAME_STRIP_REGEX
        compiled = re.compile(FILENAME_STRIP_REGEX)
        self.assertIsNotNone(compiled)

    def test_room_name_strip_regex_compiles(self):
        from syncplay.constants import ROOM_NAME_STRIP_REGEX
        compiled = re.compile(ROOM_NAME_STRIP_REGEX)
        self.assertIsNotNone(compiled)

    def test_argument_split_regex_compiles(self):
        from syncplay.constants import ARGUMENT_SPLIT_REGEX
        compiled = re.compile(ARGUMENT_SPLIT_REGEX)
        self.assertIsNotNone(compiled)

    def test_ui_command_regex_compiles(self):
        from syncplay.constants import UI_COMMAND_REGEX
        compiled = re.compile(UI_COMMAND_REGEX)
        self.assertIsNotNone(compiled)

    def test_ui_offset_regex_compiles(self):
        from syncplay.constants import UI_OFFSET_REGEX
        compiled = re.compile(UI_OFFSET_REGEX)
        self.assertIsNotNone(compiled)

    def test_ui_seek_regex_compiles(self):
        from syncplay.constants import UI_SEEK_REGEX
        compiled = re.compile(UI_SEEK_REGEX)
        self.assertIsNotNone(compiled)

    def test_mplayer_answer_regex_compiles(self):
        from syncplay.constants import MPLAYER_ANSWER_REGEX
        compiled = re.compile(MPLAYER_ANSWER_REGEX)
        self.assertIsNotNone(compiled)

    def test_vlc_answer_regex_compiles(self):
        from syncplay.constants import VLC_ANSWER_REGEX
        compiled = re.compile(VLC_ANSWER_REGEX)
        self.assertIsNotNone(compiled)

    def test_message_with_username_regex_compiles(self):
        from syncplay.constants import MESSAGE_WITH_USERNAME_REGEX
        compiled = re.compile(MESSAGE_WITH_USERNAME_REGEX)
        self.assertIsNotNone(compiled)

    def test_parse_time_regex_matches_basic(self):
        from syncplay.constants import PARSE_TIME_REGEX
        compiled = re.compile(PARSE_TIME_REGEX)
        m = compiled.match("1:30:00")
        self.assertIsNotNone(m)

    def test_room_name_strip_regex_matches(self):
        from syncplay.constants import ROOM_NAME_STRIP_REGEX
        compiled = re.compile(ROOM_NAME_STRIP_REGEX)
        m = compiled.match("+myroom:AABBCCDDEE11")
        self.assertIsNotNone(m)
        self.assertEqual(m.group("roomnamebase"), "myroom")


class TestTLSConstants(unittest.TestCase):
    def test_tls_cert_rotation_retries(self):
        from syncplay.constants import TLS_CERT_ROTATION_MAX_RETRIES
        self.assertIsInstance(TLS_CERT_ROTATION_MAX_RETRIES, int)
        self.assertGreater(TLS_CERT_ROTATION_MAX_RETRIES, 0)


if __name__ == "__main__":
    unittest.main()
