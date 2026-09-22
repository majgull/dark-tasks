import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

import wcl


class WclTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.a = os.path.join(self.tmp, "a.txt")
        with open(self.a, "wb") as f:
            f.write(b"hello world\nsecond line\n")

    def run_wcl(self, *args):
        out = io.StringIO()
        with redirect_stdout(out):
            rc = wcl.main(list(args))
        return rc, out.getvalue()

    def test_default(self):
        rc, out = self.run_wcl(self.a)
        self.assertEqual((rc, out), (0, f"2 4 24 {self.a}\n"))

    def test_flags_order(self):
        _, out = self.run_wcl("-c", "-w", self.a)
        self.assertEqual(out, f"4 24 {self.a}\n")

    def test_total_and_missing(self):
        rc, out = self.run_wcl(self.a, os.path.join(self.tmp, "nope"))
        self.assertEqual(rc, 1)
        self.assertEqual(out, f"2 4 24 {self.a}\n2 4 24 total\n")


if __name__ == "__main__":
    unittest.main()
