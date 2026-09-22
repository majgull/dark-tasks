import unittest

from textutil import clamp, mean, percent, slug, title_words, truncate


class Strings(unittest.TestCase):
    def test_slug(self):
        self.assertEqual(slug("Dark Runner: Phase 2!"), "dark-runner-phase-2")

    def test_title_words(self):
        self.assertEqual(title_words("the  quick brown"), "The Quick Brown")

    def test_truncate(self):
        self.assertEqual(truncate("abcdef", 4), "abc…")
        self.assertEqual(truncate("abc", 4), "abc")


class Numbers(unittest.TestCase):
    def test_clamp(self):
        self.assertEqual((clamp(5, 0, 3), clamp(-1, 0, 3), clamp(2, 0, 3)), (3, 0, 2))

    def test_mean(self):
        self.assertEqual(mean([1, 2, 3]), 2.0)
        self.assertEqual(mean([]), 0.0)

    def test_percent(self):
        self.assertEqual(percent(1, 3), 33.3)
        self.assertEqual(percent(1, 0), 0.0)


if __name__ == "__main__":
    unittest.main()
