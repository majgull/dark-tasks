"""obs-03-package: the library moved into observer/, nothing else changed."""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (ROOT, base_file, chk, check_base_untouched, check_count_cli, check_counts_api, check_parse,  # noqa: E402
                    finish, py_files, root_entries, tests_green)


def text(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


chk("root-files", py_files() == ["obs.py", "test_counts.py", "test_journal.py"]
    and root_entries() == ["README.md", "obs.py", "observer", "test_counts.py", "test_journal.py"], f"{py_files()} {root_entries()}")
chk("package-files", py_files("observer") == ["__init__.py", "counts.py", "journal.py"], py_files("observer"))
chk("init-empty", os.path.isfile(os.path.join(ROOT, "observer", "__init__.py")) and text("observer/__init__.py").strip() == "")
check_base_untouched("only-named-files-touched", allowed=("journal.py", "counts.py", "obs.py", "test_journal.py", "test_counts.py"))
for old, new in (("journal.py", "observer/journal.py"), ("counts.py", "observer/counts.py")):
    before = base_file(old)
    if before is None:
        print(f"  moved-unchanged-{old}: no origin to compare against (local validation); not checked")
        chk(f"moved-unchanged-{old}", True)
    else:
        chk(f"moved-unchanged-{old}", os.path.isfile(os.path.join(ROOT, new)) and text(new) == before)
BARE = re.compile(r"^\s*(import (journal|counts)\b|from (journal|counts) import\b)", re.M)
PKG = re.compile(r"^\s*(import observer\b|from observer(\.\w+)? import\b)", re.M)
ok = True
for f in ("obs.py", "test_journal.py", "test_counts.py"):
    src = text(f)
    if BARE.search(src):
        ok = False
        print(f"  {f}: still imports a moved module by its old name")
    before = base_file(f)
    # a file that imported a moved module before must import it through the
    # package now; a file that never imported one owes nothing (review obs-03)
    if before is not None and BARE.search(before) and not PKG.search(src):
        ok = False
        print(f"  {f}: had an import of a moved module and has no package import now")
chk("imports-through-package", ok)
ok, note = tests_green("test_journal", "test_counts")
chk("visible-tests", ok, note)
check_parse("observer.journal")
check_counts_api("observer.counts")
check_count_cli()
finish()
