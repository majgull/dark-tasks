import os
import subprocess
import sys
import tempfile
import unittest

from observer.counts import by_day, by_unit, day_of


def rec(ts, unit=None, msg="m"):
    r = {"__REALTIME_TIMESTAMP": ts, "MESSAGE": msg}
    if unit:
        r["_SYSTEMD_UNIT"] = unit
    return r


DAY = 86_400_000_000


class Counts(unittest.TestCase):
    def test_by_unit_order(self):
        recs = [rec(1, "b.service"), rec(2, "a.service"), rec(3, "b.service"), rec(4), rec(5, "a.service"), rec(6)]
        self.assertEqual(by_unit(recs), [("-", 2), ("a.service", 2), ("b.service", 2)])
        self.assertEqual(by_unit(recs + [rec(7, "b.service")]), [("b.service", 3), ("-", 2), ("a.service", 2)])
        self.assertEqual(by_unit([]), [])

    def test_by_day_is_utc(self):
        self.assertEqual(day_of(0), "1970-01-01")
        self.assertEqual(day_of(DAY - 1), "1970-01-01")
        self.assertEqual(day_of(DAY), "1970-01-02")
        self.assertEqual(by_day([rec(DAY), rec(0), rec(DAY + 5)]), [("1970-01-01", 1), ("1970-01-02", 2)])

    def test_cli(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "j.txt")
        with open(p, "w") as f:
            f.write("__REALTIME_TIMESTAMP=0\n_SYSTEMD_UNIT=x.service\nMESSAGE=a\n\n__REALTIME_TIMESTAMP=86400000000\nMESSAGE=b\n")
        here = os.path.dirname(os.path.abspath(__file__))
        r = subprocess.run([sys.executable, os.path.join(here, "obs.py"), "count", p], capture_output=True, text=True)
        self.assertEqual((r.returncode, r.stdout), (0, "1\t-\n1\tx.service\n\n1\t1970-01-01\n1\t1970-01-02\n"))
        r = subprocess.run([sys.executable, os.path.join(here, "obs.py"), "count"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        r = subprocess.run([sys.executable, os.path.join(here, "obs.py"), "count", p + ".missing"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        with open(p, "w") as f:
            f.write("MESSAGE=no timestamp\n")
        r = subprocess.run([sys.executable, os.path.join(here, "obs.py"), "count", p], capture_output=True, text=True)
        self.assertEqual((r.returncode, r.stdout), (1, ""))
        self.assertTrue(r.stderr.startswith("error:"))


if __name__ == "__main__":
    unittest.main()
