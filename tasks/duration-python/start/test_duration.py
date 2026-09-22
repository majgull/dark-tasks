import unittest

from duration import parse_duration


class ParseDuration(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(parse_duration("1h30m"), 5400)
        self.assertEqual(parse_duration("45s"), 45)
        self.assertEqual(parse_duration("2h"), 7200)
        self.assertEqual(parse_duration("1h0m5s"), 3605)
        self.assertEqual(parse_duration("0s"), 0)
        self.assertEqual(parse_duration("05s"), 5)

    def test_order_and_repeats(self):
        for bad in ("30m1h", "1h1h", "5s1m", "1m1h1s"):
            with self.assertRaises(ValueError):
                parse_duration(bad)

    def test_shape(self):
        for bad in ("", "1.5h", "1H", " 1h", "1h ", "h", "1", "1h30", "1h 30m", "-1h"):
            with self.assertRaises(ValueError):
                parse_duration(bad)


if __name__ == "__main__":
    unittest.main()
