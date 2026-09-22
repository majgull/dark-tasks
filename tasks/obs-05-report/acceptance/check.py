"""obs-05-report: the weekly report and its command, on top of everything before."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (chk, check_base_untouched, check_count_cli, check_counts_api, check_parse, check_report_api,  # noqa: E402
                    check_report_cli, check_tz, finish, py_files, root_entries, test_methods, tests_green)

chk("root-files", py_files() == ["obs.py", "obsreport.py", "test_counts.py", "test_counts_tz.py", "test_journal.py", "test_report.py"]
    and root_entries() == ["README.md", "obs.py", "observer", "obsreport.py", "test_counts.py", "test_counts_tz.py", "test_journal.py", "test_report.py"],
    f"{py_files()} {root_entries()}")
chk("package-files", py_files("observer") == ["__init__.py", "counts.py", "journal.py", "report.py"], py_files("observer"))
check_base_untouched("earlier-files-untouched")
chk("test-count", test_methods("test_report.py") >= 3, test_methods("test_report.py"))
ok, note = tests_green("test_journal", "test_counts", "test_counts_tz", "test_report")
chk("visible-tests", ok, note)
check_report_cli()
check_report_api()
check_parse("observer.journal")
check_counts_api("observer.counts")
check_count_cli()
check_tz()
finish()
