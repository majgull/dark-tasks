#!/bin/bash
# hidden acceptance for split-module-python; runs at the repo root in the staging VM
fail=0
if [ -f numutil.py ]; then echo "CHECK numutil-exists ok"; else echo "CHECK numutil-exists fail"; fail=1; fi
python3 - <<'PY'
import sys
bad = 0
def chk(name, ok, note=""):
    global bad
    bad += not ok
    print(f"CHECK {name} {'ok' if ok else 'fail'}" + ("" if ok else f" ({note})"))
try:
    import numutil, textutil
except Exception as e:
    chk("modules-import", False, repr(e)); sys.exit(1)
pub = lambda m: sorted(n for n in dir(m) if not n.startswith("_") and callable(getattr(m, n)))
chk("numutil-api", pub(numutil) == ["clamp", "mean", "percent"], pub(numutil))
chk("textutil-api", pub(textutil) == ["slug", "title_words", "truncate"], pub(textutil))
chk("numutil-behaviour", (numutil.clamp(5, 0, 3), numutil.mean([2, 4]), numutil.percent(1, 8)) == (3, 3.0, 12.5))
chk("textutil-behaviour", (textutil.slug("A b!"), textutil.title_words("x y"), textutil.truncate("abcdef", 3)) == ("a-b", "X Y", "ab…"))
import ast, subprocess
def funcs(src, names):
    tree = ast.parse(src)
    return {n.name: ast.get_source_segment(src, n) for n in tree.body
            if isinstance(n, ast.FunctionDef) and n.name in names}
root = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"],
                       capture_output=True, text=True).stdout.strip().splitlines()
orig_src = subprocess.run(["git", "show", f"{root[0]}:textutil.py"],
                           capture_output=True, text=True).stdout if root else ""
orig_funcs = funcs(orig_src, {"clamp", "mean", "percent"}) if orig_src else {}
moved_funcs = funcs(open("numutil.py").read(), {"clamp", "mean", "percent"})
chk("numutil-unchanged", bool(orig_funcs) and orig_funcs == moved_funcs)
src = open("app.py").read()
chk("app-imports-numutil", "from numutil import" in src or "import numutil" in src)
chk("app-no-number-from-textutil", not any(f"from textutil import" in l and any(n in l for n in ("clamp", "mean", "percent")) for l in src.splitlines()))
tsrc = open("test_textutil.py").read()
chk("tests-import-numutil", "numutil" in tsrc)
sys.exit(1 if bad else 0)
PY
[ $? = 0 ] || fail=1
want=$(printf 'dark-runner-phase-2\nThe Quick Brown Fox\na rather …\n100 0 42\n79.0\n75.0')
got=$(python3 app.py 2>/dev/null)
if [ "$got" = "$want" ]; then echo "CHECK app-output ok"; else echo "CHECK app-output fail"; fail=1; fi
if python3 -m unittest -q test_textutil >/dev/null 2>&1; then echo "CHECK tests-green ok"; else echo "CHECK tests-green fail"; fail=1; fi
n=$(ls *.py | wc -l)
if [ "$n" = 4 ]; then echo "CHECK no-extra-files ok"; else echo "CHECK no-extra-files fail ($n .py files)"; fail=1; fi
exit $fail
