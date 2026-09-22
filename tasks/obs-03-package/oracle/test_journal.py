import os
import tempfile
import unittest

from observer.journal import load, parse

TWO = ("__REALTIME_TIMESTAMP=1788478200000000\n_SYSTEMD_UNIT=sshd.service\nPRIORITY=6\nMESSAGE=Accepted publickey\n"
       "\n__REALTIME_TIMESTAMP=1788478260000000\nMESSAGE=x=y=z\n\n")


class Parse(unittest.TestCase):
    def test_two_records(self):
        recs = parse(TWO)
        self.assertEqual(len(recs), 2)
        self.assertEqual(recs[0]["__REALTIME_TIMESTAMP"], 1788478200000000)
        self.assertEqual(recs[0]["_SYSTEMD_UNIT"], "sshd.service")
        self.assertEqual(recs[1]["MESSAGE"], "x=y=z")
        self.assertNotIn("_SYSTEMD_UNIT", recs[1])

    def test_blank_lines_and_crlf(self):
        recs = parse("\n\n__REALTIME_TIMESTAMP=5\r\nMESSAGE=a\r\n\n\n\n__REALTIME_TIMESTAMP=6\nMESSAGE=\nMESSAGE=b")
        self.assertEqual([r["MESSAGE"] for r in recs], ["a", "b"])
        self.assertEqual(parse(""), [])
        self.assertEqual(parse("\n\n"), [])

    def test_errors(self):
        for bad in ("__REALTIME_TIMESTAMP=5\nMESSAGE=a\nno equals\n",
                    "__REALTIME_TIMESTAMP=5\nmessage=a\n",
                    "MESSAGE=a\n",
                    "__REALTIME_TIMESTAMP=5\n",
                    "__REALTIME_TIMESTAMP=5x\nMESSAGE=a\n"):
            with self.assertRaises(ValueError):
                parse(bad)

    def test_load(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "j.txt")
        with open(p, "w", encoding="utf-8") as f:
            f.write(TWO)
        self.assertEqual(load(p), parse(TWO))


if __name__ == "__main__":
    unittest.main()
