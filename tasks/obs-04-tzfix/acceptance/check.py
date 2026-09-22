"""obs-04-tzfix: the UTC-day regression fixed in observer/counts.py alone."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (chk, check_base_untouched, check_count_cli, check_counts_api, check_parse, check_tz, finish,  # noqa: E402
                    py_files, root_entries, sha, tests_green)

TZ_TEST_SHA = "0df28f0eb802c0009acfdc71d9267b86fc7e28c0c1f634e7e8637d6dea5fb308"

chk("root-files", py_files() == ["obs.py", "test_counts.py", "test_counts_tz.py", "test_journal.py"]
    and root_entries() == ["README.md", "obs.py", "observer", "test_counts.py", "test_counts_tz.py", "test_journal.py"],
    f"{py_files()} {root_entries()}")
chk("package-files", py_files("observer") == ["__init__.py", "counts.py", "journal.py"], py_files("observer"))
chk("tz-test-untouched", os.path.isfile("test_counts_tz.py") and sha("test_counts_tz.py") == TZ_TEST_SHA)
check_base_untouched("only-counts-touched", allowed=("observer/counts.py",), added=True)
ok, note = tests_green("test_journal", "test_counts", "test_counts_tz")
chk("visible-tests", ok, note)
check_tz()
check_counts_api("observer.counts")
check_count_cli()
check_parse("observer.journal")
finish()
