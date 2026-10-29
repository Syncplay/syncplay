# coding: utf8
import unittest

from syncplay.utils import sanitizeVlcTitleOffset


class SanitizeVlcTitleOffsetTests(unittest.TestCase):
    def test_strips_one_title_week(self):
        # Live repro: VLC reported 610582.443 for a 5795.14s file
        self.assertAlmostEqual(
            sanitizeVlcTitleOffset(610582.443, 5795.14), 5782.443, places=3)

    def test_keeps_in_range_position(self):
        self.assertEqual(sanitizeVlcTitleOffset(100.0, 5795.14), 100.0)

    def test_no_duration_returns_original(self):
        self.assertEqual(sanitizeVlcTitleOffset(610582.443, None), 610582.443)
        self.assertEqual(sanitizeVlcTitleOffset(610582.443, 0), 610582.443)

    def test_unfixable_returns_original(self):
        self.assertEqual(sanitizeVlcTitleOffset(1000.0, 1.0), 1000.0)


if __name__ == "__main__":
    unittest.main()
