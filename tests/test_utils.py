import re
import unittest


class TestParseTime(unittest.TestCase):
    def test_plain_seconds(self):
        from syncplay.utils import parseTime
        self.assertEqual(parseTime("90"), 90.0)

    def test_plain_float_seconds(self):
        from syncplay.utils import parseTime
        self.assertEqual(parseTime("1.5"), 1.5)

    def test_minutes_seconds(self):
        from syncplay.utils import parseTime
        self.assertEqual(parseTime("1:30"), 90.0)

    def test_hours_minutes_seconds(self):
        from syncplay.utils import parseTime
        self.assertEqual(parseTime("1:30:00"), 5400.0)

    def test_with_milliseconds(self):
        from syncplay.utils import parseTime
        result = parseTime("0:01.500")
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result, 1.5, places=1)

    def test_no_match_returns_none(self):
        from syncplay.utils import parseTime
        self.assertIsNone(parseTime(":"))


class TestFormatTime(unittest.TestCase):
    def test_zero(self):
        from syncplay.utils import formatTime
        self.assertEqual(formatTime(0), "00:00")

    def test_seconds_only(self):
        from syncplay.utils import formatTime
        self.assertEqual(formatTime(65), "01:05")

    def test_hours(self):
        from syncplay.utils import formatTime
        self.assertEqual(formatTime(3661), "01:01:01")

    def test_negative(self):
        from syncplay.utils import formatTime
        result = formatTime(-65)
        self.assertTrue(result.startswith("-"))
        self.assertIn("01:05", result)

    def test_days(self):
        from syncplay.utils import formatTime
        result = formatTime(90000)
        self.assertIn("d,", result)

    def test_weeks_as_titles(self):
        from syncplay.utils import formatTime
        result = formatTime(604800 + 60, weeksAsTitles=True)
        self.assertIn("Title 1", result)

    def test_weeks_not_as_titles(self):
        from syncplay.utils import formatTime
        result = formatTime(604800 + 60, weeksAsTitles=False)
        self.assertIn("w,", result)


class TestFormatSize(unittest.TestCase):
    def test_zero_returns_unknown(self):
        from syncplay.utils import formatSize
        self.assertEqual(formatSize(0), "???")

    def test_megabytes(self):
        from syncplay.utils import formatSize
        result = formatSize(10 * 1048576)
        self.assertIn("10", result)

    def test_precise(self):
        from syncplay.utils import formatSize
        result = formatSize(int(1.5 * 1048576), precise=True)
        self.assertIn("1.5", result)

    def test_hashed_returns_unknown(self):
        from syncplay.utils import formatSize
        self.assertEqual(formatSize("abc123abc123"), "???")


class TestIsASCII(unittest.TestCase):
    def test_ascii_string(self):
        from syncplay.utils import isASCII
        self.assertTrue(isASCII("hello world"))

    def test_non_ascii(self):
        from syncplay.utils import isASCII
        self.assertFalse(isASCII("héllo"))

    def test_empty(self):
        from syncplay.utils import isASCII
        self.assertTrue(isASCII(""))


class TestIsURL(unittest.TestCase):
    def test_http_url(self):
        from syncplay.utils import isURL
        self.assertTrue(isURL("http://example.com/video.mp4"))

    def test_https_url(self):
        from syncplay.utils import isURL
        self.assertTrue(isURL("https://example.com/video.mp4"))

    def test_none(self):
        from syncplay.utils import isURL
        self.assertFalse(isURL(None))

    def test_regular_path(self):
        from syncplay.utils import isURL
        self.assertFalse(isURL("/home/user/video.mp4"))


class TestMeetsMinVersion(unittest.TestCase):
    def test_equal_versions(self):
        from syncplay.utils import meetsMinVersion
        self.assertTrue(meetsMinVersion("1.7.3", "1.7.3"))

    def test_higher_version(self):
        from syncplay.utils import meetsMinVersion
        self.assertTrue(meetsMinVersion("1.7.4", "1.7.3"))

    def test_lower_version(self):
        from syncplay.utils import meetsMinVersion
        self.assertFalse(meetsMinVersion("1.7.2", "1.7.3"))

    def test_major_version_higher(self):
        from syncplay.utils import meetsMinVersion
        self.assertTrue(meetsMinVersion("2.0.0", "1.9.9"))

    def test_major_version_lower(self):
        from syncplay.utils import meetsMinVersion
        self.assertFalse(meetsMinVersion("1.0.0", "2.0.0"))


class TestStripFilename(unittest.TestCase):
    def test_basic_strip(self):
        from syncplay.utils import stripfilename
        result = stripfilename("my_file (2).mkv", stripURL=False)
        self.assertNotIn("_", result)
        self.assertNotIn("(", result)
        self.assertNotIn(")", result)
        self.assertNotIn(" ", result)

    def test_url_strip(self):
        from syncplay.utils import stripfilename
        result = stripfilename("http://example.com/path/video.mp4", stripURL=True)
        self.assertNotIn("http", result)

    def test_none_returns_empty(self):
        from syncplay.utils import stripfilename
        self.assertEqual(stripfilename(None, stripURL=False), "")

    def test_empty_returns_empty(self):
        from syncplay.utils import stripfilename
        self.assertEqual(stripfilename("", stripURL=False), "")


class TestStripRoomName(unittest.TestCase):
    def test_controlled_room_name(self):
        from syncplay.utils import stripRoomName
        result = stripRoomName("+myroom:AABBCCDDEE11")
        self.assertEqual(result, "myroom")

    def test_regular_room_name(self):
        from syncplay.utils import stripRoomName
        result = stripRoomName("regularroom")
        self.assertEqual(result, "regularroom")

    def test_none_returns_empty(self):
        from syncplay.utils import stripRoomName
        self.assertEqual(stripRoomName(None), "")

    def test_empty_returns_empty(self):
        from syncplay.utils import stripRoomName
        self.assertEqual(stripRoomName(""), "")


class TestHashFilename(unittest.TestCase):
    def test_deterministic(self):
        from syncplay.utils import hashFilename
        h1 = hashFilename("test.mkv")
        h2 = hashFilename("test.mkv")
        self.assertEqual(h1, h2)

    def test_length(self):
        from syncplay.utils import hashFilename
        h = hashFilename("test.mkv")
        self.assertEqual(len(h), 12)

    def test_url_forces_strip(self):
        from syncplay.utils import hashFilename
        h = hashFilename("http://example.com/video.mp4")
        self.assertEqual(len(h), 12)


class TestHashFilesize(unittest.TestCase):
    def test_deterministic(self):
        from syncplay.utils import hashFilesize
        h1 = hashFilesize(12345)
        h2 = hashFilesize(12345)
        self.assertEqual(h1, h2)

    def test_length(self):
        from syncplay.utils import hashFilesize
        self.assertEqual(len(hashFilesize(12345)), 12)

    def test_different_sizes_different_hashes(self):
        from syncplay.utils import hashFilesize
        self.assertNotEqual(hashFilesize(100), hashFilesize(200))


class TestSameFilename(unittest.TestCase):
    def test_identical(self):
        from syncplay.utils import sameFilename
        self.assertTrue(sameFilename("video.mkv", "video.mkv"))

    def test_different(self):
        from syncplay.utils import sameFilename
        self.assertFalse(sameFilename("video1.mkv", "video2.mkv"))

    def test_hidden_filename_matches_anything(self):
        from syncplay.utils import sameFilename
        from syncplay.constants import PRIVACY_HIDDENFILENAME
        self.assertTrue(sameFilename(PRIVACY_HIDDENFILENAME, "anything.mkv"))
        self.assertTrue(sameFilename("anything.mkv", PRIVACY_HIDDENFILENAME))


class TestSameFilesize(unittest.TestCase):
    def test_identical(self):
        from syncplay.utils import sameFilesize
        self.assertTrue(sameFilesize(12345, 12345))

    def test_different(self):
        from syncplay.utils import sameFilesize
        self.assertFalse(sameFilesize(12345, 67890))

    def test_zero_matches_anything(self):
        from syncplay.utils import sameFilesize
        self.assertTrue(sameFilesize(0, 12345))
        self.assertTrue(sameFilesize(12345, 0))


class TestSameFileduration(unittest.TestCase):
    def test_same_duration(self):
        from syncplay.utils import sameFileduration
        self.assertTrue(sameFileduration(100.0, 100.0))

    def test_within_threshold(self):
        from syncplay.utils import sameFileduration
        self.assertTrue(sameFileduration(100.0, 102.0))

    def test_beyond_threshold(self):
        from syncplay.utils import sameFileduration
        self.assertFalse(sameFileduration(100.0, 103.0))


class TestTruncateText(unittest.TestCase):
    def test_short_text(self):
        from syncplay.utils import truncateText
        self.assertEqual(truncateText("hello", 10), "hello")

    def test_truncation(self):
        from syncplay.utils import truncateText
        self.assertEqual(truncateText("hello world", 5), "hello")

    def test_bytes_input(self):
        from syncplay.utils import truncateText
        result = truncateText(b"hello world", 5)
        self.assertEqual(result, "hello")


class TestSplitText(unittest.TestCase):
    def test_basic_split(self):
        from syncplay.utils import splitText
        result = splitText("abcdef", 3)
        self.assertEqual(result, ["abc", "def"])

    def test_no_split_needed(self):
        from syncplay.utils import splitText
        result = splitText("abc", 10)
        self.assertEqual(result, ["abc"])


class TestPlaylistIsValid(unittest.TestCase):
    def test_valid_playlist(self):
        from syncplay.utils import playlistIsValid
        self.assertTrue(playlistIsValid(["file1.mkv", "file2.mkv"]))

    def test_too_many_items(self):
        from syncplay.utils import playlistIsValid
        files = ["file{}.mkv".format(i) for i in range(251)]
        self.assertFalse(playlistIsValid(files))

    def test_too_many_characters(self):
        from syncplay.utils import playlistIsValid
        files = ["a" * 5001, "b" * 5001]
        self.assertFalse(playlistIsValid(files))


class TestGetDomainFromURL(unittest.TestCase):
    def test_basic_url(self):
        from syncplay.utils import getDomainFromURL
        self.assertEqual(getDomainFromURL("https://example.com/page"), "example.com")

    def test_www_prefix_stripped(self):
        from syncplay.utils import getDomainFromURL
        self.assertEqual(getDomainFromURL("https://www.example.com/page"), "example.com")

    def test_no_domain(self):
        from syncplay.utils import getDomainFromURL
        self.assertIsNone(getDomainFromURL("not-a-url"))

    def test_none_like(self):
        from syncplay.utils import getDomainFromURL
        self.assertIsNone(getDomainFromURL(""))


class TestRoomPasswordProvider(unittest.TestCase):
    def test_is_controlled_room_true(self):
        from syncplay.utils import RoomPasswordProvider
        self.assertTrue(RoomPasswordProvider.isControlledRoom("+myroom:AABBCCDDEE11"))

    def test_is_controlled_room_false(self):
        from syncplay.utils import RoomPasswordProvider
        self.assertFalse(RoomPasswordProvider.isControlledRoom("regularroom"))
        self.assertFalse(RoomPasswordProvider.isControlledRoom("+nopasshash"))

    def test_get_controlled_room_name_format(self):
        from syncplay.utils import RoomPasswordProvider
        name = RoomPasswordProvider.getControlledRoomName("myroom", "AB-123-456", "SALTSALTSALT")
        self.assertTrue(name.startswith("+myroom:"))
        self.assertEqual(len(name), len("+myroom:") + 12)

    def test_check_valid_password(self):
        from syncplay.utils import RoomPasswordProvider
        salt = "SALTSALTSALT"
        password = "AB-123-456"
        roomName = RoomPasswordProvider.getControlledRoomName("myroom", password, salt)
        self.assertTrue(RoomPasswordProvider.check(roomName, password, salt))

    def test_check_wrong_password(self):
        from syncplay.utils import RoomPasswordProvider
        salt = "SALTSALTSALT"
        password = "AB-123-456"
        roomName = RoomPasswordProvider.getControlledRoomName("myroom", password, salt)
        self.assertFalse(RoomPasswordProvider.check(roomName, "CD-789-012", salt))

    def test_check_invalid_password_format(self):
        from syncplay.utils import RoomPasswordProvider
        with self.assertRaises(ValueError):
            RoomPasswordProvider.check("+room:AABBCCDDEE11", "badformat", "SALT")

    def test_check_not_controlled_room(self):
        from syncplay.utils import RoomPasswordProvider, NotControlledRoom
        with self.assertRaises(NotControlledRoom):
            RoomPasswordProvider.check("regularroom", "AB-123-456", "SALT")

    def test_check_empty_password(self):
        from syncplay.utils import RoomPasswordProvider
        with self.assertRaises(ValueError):
            RoomPasswordProvider.check("+room:AABBCCDDEE11", "", "SALT")


class TestRandomStringGenerator(unittest.TestCase):
    def test_password_format(self):
        from syncplay.utils import RandomStringGenerator
        password = RandomStringGenerator.generate_room_password()
        self.assertRegex(password, r"^[A-Z]{2}-\d{3}-\d{3}$")

    def test_salt_format(self):
        from syncplay.utils import RandomStringGenerator
        salt = RandomStringGenerator.generate_server_salt()
        self.assertEqual(len(salt), 10)
        self.assertTrue(salt.isalpha())
        self.assertTrue(salt.isupper())

    def test_password_uniqueness(self):
        from syncplay.utils import RandomStringGenerator
        passwords = {RandomStringGenerator.generate_room_password() for _ in range(20)}
        self.assertGreater(len(passwords), 1)


class TestListConversions(unittest.TestCase):
    def test_list_to_multiline(self):
        from syncplay.utils import getListAsMultilineString
        result = getListAsMultilineString(["a", "b", "c"])
        self.assertEqual(result, "a\nb\nc")

    def test_empty_list(self):
        from syncplay.utils import getListAsMultilineString
        self.assertEqual(getListAsMultilineString([]), "")

    def test_none_list(self):
        from syncplay.utils import getListAsMultilineString
        self.assertEqual(getListAsMultilineString(None), "")

    def test_multiline_to_list(self):
        from syncplay.utils import convertMultilineStringToList
        result = convertMultilineStringToList("a\nb\nc")
        self.assertEqual(result, ["a", "b", "c"])

    def test_empty_multiline(self):
        from syncplay.utils import convertMultilineStringToList
        self.assertEqual(convertMultilineStringToList(""), [])

    def test_none_multiline(self):
        from syncplay.utils import convertMultilineStringToList
        self.assertEqual(convertMultilineStringToList(None), [])


if __name__ == "__main__":
    unittest.main()
