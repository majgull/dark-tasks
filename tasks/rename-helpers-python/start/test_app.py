import unittest

import app
import utils


class AppTest(unittest.TestCase):
    def test_render(self):
        self.assertEqual(app.render(["Max Items = 3", "", "# comment", "Log Level=debug"]),
                         ["max-items=3", "log-level=debug"])

    def test_slugify(self):
        self.assertEqual(utils.slugify("Hello, World!"), "hello-world")

    def test_parse_kv_rejects_missing_equals(self):
        with self.assertRaises(ValueError):
            utils.parse_kv("no equals here")


if __name__ == "__main__":
    unittest.main()
