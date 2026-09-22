import unittest

from csvline import split_line


class SplitLine(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(split_line("a,b,c"), ["a", "b", "c"])
        self.assertEqual(split_line("a, b ,c"), ["a", " b ", "c"])

    def test_empty_fields(self):
        self.assertEqual(split_line(""), [""])
        self.assertEqual(split_line("a,b,"), ["a", "b", ""])
        self.assertEqual(split_line(",,"), ["", "", ""])

    def test_quoted(self):
        self.assertEqual(split_line('"x,y",z'), ["x,y", "z"])
        self.assertEqual(split_line('"say ""hi""",'), ['say "hi"', ""])
        self.assertEqual(split_line('""'), [""])

    def test_errors(self):
        for bad in ('"abc', 'a"b', '"a"b', '"a",b"'):
            with self.assertRaises(ValueError):
                split_line(bad)


if __name__ == "__main__":
    unittest.main()
