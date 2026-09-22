import unittest

from roman import from_roman, to_roman


class ToRoman(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(to_roman(1), "I")
        self.assertEqual(to_roman(3), "III")
        self.assertEqual(to_roman(58), "LVIII")

    def test_subtractive(self):
        self.assertEqual(to_roman(4), "IV")
        self.assertEqual(to_roman(9), "IX")
        self.assertEqual(to_roman(40), "XL")
        self.assertEqual(to_roman(90), "XC")
        self.assertEqual(to_roman(400), "CD")
        self.assertEqual(to_roman(1994), "MCMXCIV")

    def test_range(self):
        for bad in (0, -1, 4000):
            with self.assertRaises(ValueError):
                to_roman(bad)


class FromRoman(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(from_roman("III"), 3)
        self.assertEqual(from_roman("LVIII"), 58)

    def test_subtractive(self):
        self.assertEqual(from_roman("IV"), 4)
        self.assertEqual(from_roman("MCMXCIV"), 1994)

    def test_rejects(self):
        for bad in ("", "IIII", "VX", "iv", "ABC"):
            with self.assertRaises(ValueError):
                from_roman(bad)


if __name__ == "__main__":
    unittest.main()
