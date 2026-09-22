import unittest

from slugify import slugify


class SlugifyTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_punctuation_and_padding(self):
        self.assertEqual(slugify("  Hello,  World!  "), "hello-world")

    def test_ampersand(self):
        self.assertEqual(slugify("Rock & Roll"), "rock-roll")

    def test_empty(self):
        self.assertEqual(slugify(""), "")


if __name__ == "__main__":
    unittest.main()
