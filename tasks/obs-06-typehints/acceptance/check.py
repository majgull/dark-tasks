"""obs-06-typehints: every function annotated, nothing else different."""

import ast
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (ROOT, base_file, chk, check_base_untouched, check_count_cli, check_counts_api, check_parse,  # noqa: E402
                    check_report_api, check_report_cli, check_tz, finish, py_files, root_entries, tests_green)

MODULES = ("observer/journal.py", "observer/counts.py", "observer/report.py")


def source(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def strip_annotations(tree):
    """The same module with every annotation removed: what must be equal
    before and after."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            node.returns = None
            for a in node.args.posonlyargs + node.args.args + node.args.kwonlyargs + [node.args.vararg, node.args.kwarg]:
                if a is not None:
                    a.annotation = None
    return tree


def annotated(fn):
    args = fn.args.posonlyargs + fn.args.args + fn.args.kwonlyargs + [a for a in (fn.args.vararg, fn.args.kwarg) if a]
    return fn.returns is not None and all(a.annotation is not None for a in args)


REC = "dict[str, str | int]"
EXPECTED = {  # the spec's table: every public function's parameters and return
    "observer/journal.py": {"parse": (["str"], f"list[{REC}]"), "load": (["str"], f"list[{REC}]")},
    "observer/counts.py": {"day_of": (["int"], "str"), "by_unit": ([f"list[{REC}]"], "list[tuple[str, int]]"),
                           "by_day": ([f"list[{REC}]"], "list[tuple[str, int]]")},
    "observer/report.py": {"week_days": (["str"], "list[str]"), "weekly": ([f"list[{REC}]", "str"], "str")},
}


def norm(node):
    return re.sub(r"\s+", "", ast.unparse(node))


def signature(fn):
    args = fn.args.posonlyargs + fn.args.args + fn.args.kwonlyargs
    return [norm(a.annotation) if a.annotation is not None else None for a in args], (norm(fn.returns) if fn.returns is not None else None)


chk("root-files", py_files() == ["obs.py", "obsreport.py", "test_counts.py", "test_counts_tz.py", "test_journal.py", "test_report.py"]
    and root_entries() == ["README.md", "obs.py", "observer", "obsreport.py", "test_counts.py", "test_counts_tz.py", "test_journal.py", "test_report.py"],
    f"{py_files()} {root_entries()}")
chk("package-files", py_files("observer") == ["__init__.py", "counts.py", "journal.py", "report.py"], py_files("observer"))
check_base_untouched("only-modules-touched", allowed=MODULES, added=True)
for path in MODULES:
    try:
        tree = ast.parse(source(path))
    except (OSError, SyntaxError) as e:
        chk(f"annotated-{os.path.basename(path)}", False, repr(e))
        continue
    fns = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    missing = [f.name for f in fns if not annotated(f)]
    chk(f"annotated-{os.path.basename(path)}", fns and not missing, f"unannotated {missing}")
    wrong = []
    for name, (params, ret) in EXPECTED[path].items():
        fn = next((f for f in fns if f.name == name), None)
        if fn is None:
            wrong.append(f"{name}: missing")
            continue
        got = signature(fn)
        if got != ([re.sub(r"\s+", "", p) for p in params], re.sub(r"\s+", "", ret)):
            wrong.append(f"{name}: {got}")
    chk(f"types-as-specified-{os.path.basename(path)}", not wrong, "; ".join(wrong)[:200])
    nested = [n.name for f in fns for n in ast.walk(f) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n is not f and annotated(n)]
    lambdas = [1 for f in fns for n in ast.walk(f) if isinstance(n, ast.Lambda) and any(a.annotation for a in n.args.args)]
    chk(f"nested-unannotated-{os.path.basename(path)}", not nested and not lambdas, nested)
    imports = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    typing_or_future = [n for n in imports if (isinstance(n, ast.ImportFrom) and n.module in ("typing", "__future__"))
                        or (isinstance(n, ast.Import) and any(a.name == "typing" for a in n.names))]
    chk(f"builtin-generics-{os.path.basename(path)}", not typing_or_future)
    before = base_file(path)
    if before is None:
        print(f"  unchanged-{os.path.basename(path)}: no origin to compare against (local validation); not checked")
        chk(f"unchanged-{os.path.basename(path)}", True)
        continue
    try:
        same = ast.dump(strip_annotations(ast.parse(before))) == ast.dump(strip_annotations(tree))
    except SyntaxError as e:
        same = False
        print(f"  {path}: {e!r}")
    chk(f"unchanged-{os.path.basename(path)}", same)
ok, note = tests_green("test_journal", "test_counts", "test_counts_tz", "test_report")
chk("visible-tests", ok, note)
check_parse("observer.journal")
check_counts_api("observer.counts")
check_count_cli()
check_tz()
check_report_cli()
check_report_api()
finish()
