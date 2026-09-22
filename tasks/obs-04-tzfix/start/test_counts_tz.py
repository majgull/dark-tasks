"""Regression: the weekly numbers on a host in Tokyo disagreed with the same
export counted on a host in London. Days are UTC days, whatever the
process's timezone. Only these two records; nothing else is measured."""

import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
# 2026-08-31T23:30:00Z and 2026-09-01T00:10:00Z: the same UTC day boundary
# seen from Tokyo (UTC+9) is 08:30 and 09:10 on the 1st
CODE = ("from observer.counts import by_day, day_of; "
        "print(day_of(1788219000000000), by_day([{'__REALTIME_TIMESTAMP': 1788219000000000, 'MESSAGE': 'a'},"
        " {'__REALTIME_TIMESTAMP': 1788221400000000, 'MESSAGE': 'b'}]))")


class UTCDays(unittest.TestCase):
    def test_day_is_utc_whatever_the_process_timezone(self):
        for tz in ("JST-9", "NZST-12", "PST8PDT", "UTC0"):
            r = subprocess.run([sys.executable, "-c", CODE], cwd=HERE, env={**os.environ, "TZ": tz},
                               capture_output=True, text=True)
            self.assertEqual(r.stdout.strip(), "2026-08-31 [('2026-08-31', 1), ('2026-09-01', 1)]", f"TZ={tz}: {r.stderr}")


if __name__ == "__main__":
    unittest.main()
