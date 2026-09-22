"""obs-02-count: counts and the command line, on top of the parser."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (chk, check_base_untouched, check_count_cli, check_counts_api, check_parse, check_tz, finish,  # noqa: E402
                    py_files, root_entries, test_methods, tests_green)

chk("files", py_files() == ["counts.py", "journal.py", "obs.py", "test_counts.py", "test_journal.py"]
    and root_entries() == ["README.md", "counts.py", "journal.py", "obs.py", "test_counts.py", "test_journal.py"],
    f"{py_files()} {root_entries()}")
check_base_untouched("earlier-files-untouched")
chk("test-count", test_methods("test_counts.py") >= 3, test_methods("test_counts.py"))
ok, note = tests_green("test_journal", "test_counts")
chk("visible-tests", ok, note)
check_parse("journal")
check_counts_api("counts")
check_count_cli()
check_tz("counts")
finish()
