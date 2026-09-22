import os
import subprocess
import sys
import tempfile
import unittest

from observer.report import week_days, weekly

HERE = os.path.dirname(os.path.abspath(__file__))
MON = 1788134400000000  # 2026-08-31T00:00:00Z, Monday of 2026-W36
HOUR = 3_600_000_000
DAY = 24 * HOUR


def rec(ts, unit=None, msg="m", prio=None):
    r = {"__REALTIME_TIMESTAMP": ts, "MESSAGE": msg}
    if unit:
        r["_SYSTEMD_UNIT"] = unit
    if prio is not None:
        r["PRIORITY"] = str(prio)
    return r


class Weeks(unittest.TestCase):
    def test_week_days(self):
        self.assertEqual(week_days("2026-W36")[0], "2026-08-31")
        self.assertEqual(week_days("2026-W36")[6], "2026-09-06")
        self.assertEqual(len(week_days("2020-W53")), 7)
        for bad in ("2026-W54", "2026-36", "2026-W6", "2026-W00", "26-W36", "2026-w36"):
            with self.assertRaises(ValueError):
                week_days(bad)

    def test_weekly(self):
        recs = [rec(MON - 1, "a.service", "before"), rec(MON, "a.service", "first", 3), rec(MON + 2 * DAY, None, "kernel", 2),
                rec(MON + 2 * DAY + HOUR, "b.service", "warn", 4), rec(MON + 7 * DAY, "a.service", "after", 0)]
        out = weekly(recs, "2026-W36")
        self.assertEqual(out, "# Week 2026-W36\n\n## Units\n\n| unit | count |\n|---|---|\n| - | 1 |\n| a.service | 1 |\n| b.service | 1 |\n"
                              "\n## Days\n\n- 2026-08-31: 1\n- 2026-09-01: 0\n- 2026-09-02: 2\n- 2026-09-03: 0\n- 2026-09-04: 0\n- 2026-09-05: 0\n- 2026-09-06: 0\n"
                              "\n## Errors\n\n- 2026-08-31T00:00:00Z a.service: first\n- 2026-09-02T00:00:00Z -: kernel\n")
        self.assertTrue(weekly([], "2026-W36").endswith("## Errors\n\n- none\n"))
        many = [rec(MON + i * HOUR, "x.service", f"e{i}", 1) for i in range(23)]
        self.assertTrue(weekly(many, "2026-W36").endswith("- 2026-08-31T19:00:00Z x.service: e19\n- and 3 more\n"))

    def test_cli(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "j.txt")
        with open(p, "w") as f:
            f.write(f"__REALTIME_TIMESTAMP={MON}\nPRIORITY=3\nMESSAGE=boom\n")
        cli = os.path.join(HERE, "obsreport.py")
        r = subprocess.run([sys.executable, cli, p, "2026-W36"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertTrue(r.stdout.startswith("# Week 2026-W36\n"))
        self.assertIn("- 2026-08-31T00:00:00Z -: boom\n", r.stdout)
        for args, code in (([p], 2), ([p, "2026-W99"], 2), ([p + ".nope", "2026-W36"], 2)):
            r = subprocess.run([sys.executable, cli, *args], capture_output=True, text=True)
            self.assertEqual((r.returncode, r.stdout), (code, ""), args)
        with open(p, "w") as f:
            f.write("MESSAGE=no timestamp\n")
        r = subprocess.run([sys.executable, cli, p, "2026-W36"], capture_output=True, text=True)
        self.assertEqual((r.returncode, r.stdout), (1, ""))


if __name__ == "__main__":
    unittest.main()
