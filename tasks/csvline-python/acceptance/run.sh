#!/bin/bash
# hidden acceptance for csvline-python; runs at the repo root in the staging VM
fail=0
if python3 -m unittest -q test_csvline >/dev/null 2>&1; then echo "CHECK visible-tests ok"; else echo "CHECK visible-tests fail"; fail=1; fi
if grep -q 'def test_quoted' test_csvline.py && grep -q 'say ""hi""' test_csvline.py; then echo "CHECK tests-untouched ok"; else echo "CHECK tests-untouched fail"; fail=1; fi
n=$(ls *.py | wc -l)
if [ "$n" = 2 ]; then echo "CHECK no-extra-files ok"; else echo "CHECK no-extra-files fail ($n .py files)"; fail=1; fi
if grep -q 'import csv' csvline.py; then echo "CHECK no-csv-module fail"; fail=1; else echo "CHECK no-csv-module ok"; fi
python3 - <<'PY'
import sys
from csvline import split_line
bad = 0
def chk(name, ok, note=""):
    global bad
    bad += not ok
    print(f"CHECK {name} {'ok' if ok else 'fail'}" + ("" if ok else f" ({note})"))
Q = '"'
cases = [
    ("a", ["a"]),
    (",", ["", ""]),
    (Q + Q + "," + Q + Q, ["", ""]),
    (Q + "a,b" + Q + "," + Q + "c,d" + Q, ["a,b", "c,d"]),
    (Q + Q + Q + Q + ",x", [Q, "x"]),
    (Q + "a" + Q + Q + "b" + Q + Q + "c" + Q, ["a" + Q + "b" + Q + "c"]),
    ("x," + Q + Q + ",y", ["x", "", "y"]),
    (Q + "tab\tin" + Q + ",z", ["tab\tin", "z"]),
    (Q + " spaced " + Q + ",q", [" spaced ", "q"]),
    ("a,,b", ["a", "", "b"]),
]
wrong = {}
for text, want in cases:
    got = split_line(text)
    if got != want:
        wrong[text] = got
chk("hidden-values", not wrong, wrong)
rej = 0
for s in (Q, Q + "a", "a" + Q, "ab" + Q + "c,d", Q + "a" + Q + "x,b", "x," + Q + "a" + Q + "b", Q + "a" + Q + Q, Q + "a" + Q + Q + ",b", " " + Q + "a" + Q):
    try:
        split_line(s); rej += 1; print(f"  accepted {s!r}")
    except ValueError:
        pass
    except Exception as e:  # the contract says ValueError; anything else is a miss, not a crash
        rej += 1; print(f"  raised {type(e).__name__} for {s!r}")
chk("hidden-rejects", rej == 0, f"{rej} accepted")
sys.exit(1 if bad else 0)
PY
[ $? = 0 ] || fail=1
exit $fail
