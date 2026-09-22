"""obs-01-parse: the parser, from an empty repo."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import chk, check_parse, finish, py_files, root_entries, test_methods, tests_green  # noqa: E402

chk("files", py_files() == ["journal.py", "test_journal.py"] and root_entries() == ["README.md", "journal.py", "test_journal.py"],
    f"{py_files()} {root_entries()}")
chk("test-count", test_methods("test_journal.py") >= 4, test_methods("test_journal.py"))
ok, note = tests_green("test_journal")
chk("visible-tests", ok, note)
check_parse("journal")
finish()
