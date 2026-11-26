# coding:utf8
"""Smoke tests for the packaging contract.

These cover what the build configuration promises to ship: the entry points
import, every translation module loads, and the resources used at runtime and
by the installers are present in the installed package. Run them from a
checkout and again from a virtual environment with the built wheel installed,
so a packaging change that silently drops files fails the build.
"""

import pathlib
import unittest

import syncplay
import syncplay.messages as messages
import syncplay.resources as resources

RESOURCE_DIR = pathlib.Path(resources.__file__).parent

try:
    import syncplay.ui.gui  # noqa: F401  (importing a Qt binding must work)

    QT_AVAILABLE = True
except ImportError:
    QT_AVAILABLE = False


class VersionTests(unittest.TestCase):
    def test_version_is_a_dotted_number(self):
        parts = syncplay.version.split(".")
        self.assertGreaterEqual(len(parts), 2, syncplay.version)
        for part in parts:
            self.assertTrue(part.isdigit(), syncplay.version)


class EntryPointTests(unittest.TestCase):
    def test_client_and_server_entry_modules_import(self):
        from syncplay import ep_client, ep_server

        self.assertTrue(callable(ep_client.main))
        self.assertTrue(callable(ep_server.main))


class MessageTests(unittest.TestCase):
    def test_every_translation_module_loads(self):
        languages = sorted(language for language in messages.messages if language != "CURRENT")
        self.assertGreaterEqual(len(languages), 14)
        for language in languages:
            messages.setLanguage(language)
            for key in ("LANGUAGE", "LANGUAGE-TAG"):
                self.assertTrue(messages.getMessage(key), (language, key))


class ResourceTests(unittest.TestCase):
    def test_runtime_resources_are_shipped(self):
        for name in (
            "syncplay.png",
            "user_key.png",
            "spinner.mng",
            "syncplay.desktop",
            "syncplay-server.desktop",
            "lua/intf/syncplay.lua",
        ):
            self.assertTrue((RESOURCE_DIR / name).is_file(), name)

    def test_installer_resources_are_shipped(self):
        for name in (
            "icon.ico",
            "icon.icns",
            "hicolor/16x16/apps/syncplay.png",
            "hicolor/128x128/apps/syncplay.png",
            "hicolor/256x256/apps/syncplay.png",
        ):
            self.assertTrue((RESOURCE_DIR / name).is_file(), name)


@unittest.skipUnless(QT_AVAILABLE, "no Qt binding installed; install the gui extra")
class GuiTests(unittest.TestCase):
    def test_main_window_class_is_available(self):
        from syncplay.ui import gui

        self.assertTrue(hasattr(gui, "MainWindow"))


if __name__ == "__main__":
    unittest.main()
