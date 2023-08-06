import os
import unittest

from p360_export.config.LocalFileConfigGetter import LocalFileConfigGetter


class LocalFileConfigGetterTest(unittest.TestCase):
    def test_file_content_matches(self):
        config_getter = LocalFileConfigGetter(base_path=".")

        with open("./test_config_id.json", "w", encoding="utf8") as file_handler:
            file_handler.write('{"test": "content"}')

        config = config_getter.get(config_id="test_config_id")

        self.assertEqual(config, {"test": "content"})

        os.remove("./test_config_id.json")


if __name__ == "__main__":
    unittest.main()
