#!/bin/bash
# hidden acceptance for duration-python; runs at the repo root in the staging VM
fail=0
if python3 -m unittest -q test_duration >/dev/null 2>&1; then echo "CHECK visible-tests ok"; else echo "CHECK visible-tests fail"; fail=1; fi
if grep -q 'def test_order_and_repeats' test_duration.py && grep -q '"1h0m5s"' test_duration.py && grep -q '"1h 30m"' test_duration.py; then echo "CHECK tests-untouched ok"; else echo "CHECK tests-untouched fail"; fail=1; fi
n=$(ls *.py | wc -l)
if [ "$n" = 2 ]; then echo "CHECK no-extra-files ok"; else echo "CHECK no-extra-files fail ($n .py files)"; fail=1; fi
python3 - <<'PY'
import sys
from duration import parse_duration
bad = 0
def chk(name, ok, note=""):
    global bad
    bad += not ok
    print(f"CHECK {name} {'ok' if ok else 'fail'}" + ("" if ok else f" ({note})"))
good = {"100h": 360000, "59m59s": 3599, "0h0m0s": 0, "1h59s": 3659, "000m": 0, "7m": 420, "1h1m1s": 3661}
got = {k: (lambda k: (parse_duration(k)))(k) for k in good}
chk("hidden-values", got == good, got)
rej = 0
for s in ("", "1s1s", "1m1m", "1h1m1m", "1s1h", "m", "1ms", "1hm", "1h\n", "\t1s", "1h+1m", "١s", "1d", "1w"):
    try:
        parse_duration(s); rej += 1; print(f"  accepted {s!r}")
    except ValueError:
        pass
    except Exception as e:  # the contract says ValueError; anything else is a miss, not a crash
        rej += 1; print(f"  raised {type(e).__name__} for {s!r}")
chk("hidden-rejects", rej == 0, f"{rej} accepted")
chk("hidden-type", isinstance(parse_duration("1h"), int) and not isinstance(parse_duration("1h"), bool))
sys.exit(1 if bad else 0)
PY
[ $? = 0 ] || fail=1
exit $fail
