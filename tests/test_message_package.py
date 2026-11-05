import os
import unittest

import toml

from syncplay import messages, version


class MessagePackageTests(unittest.TestCase):
    def test_spanish_spain_dictionary_is_available(self):
        self.assertIn("es_ES", messages.getLanguages())
        self.assertEqual(messages.getMessage("LANGUAGE", "es_ES"), "Español (España)")

    def test_distribution_version_matches_application_version(self):
        project_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pyproject.toml")
        with open(project_path, "r") as project_file:
            project = toml.load(project_file)
        self.assertEqual(project["project"]["version"], version)


if __name__ == "__main__":
    unittest.main()
