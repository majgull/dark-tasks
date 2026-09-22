#!/bin/bash
# hidden acceptance for rename-helpers-python; runs at the repo root in the staging VM
fail=0
if [ ! -e utils.py ]; then echo "CHECK utils-gone ok"; else echo "CHECK utils-gone fail"; fail=1; fi
if [ -f helpers.py ]; then echo "CHECK helpers-exists ok"; else echo "CHECK helpers-exists fail"; fail=1; fi
if ! grep -qw utils app.py test_app.py helpers.py 2>/dev/null; then echo "CHECK no-utils-refs ok"; else echo "CHECK no-utils-refs fail"; fail=1; fi
if python3 -c 'import helpers; assert helpers.parse_kv("k = v") == ("k", "v"); assert helpers.slugify("A B") == "a-b"' 2>/dev/null; then echo "CHECK helpers-api ok"; else echo "CHECK helpers-api fail"; fail=1; fi
if python3 -m unittest -q test_app >/dev/null 2>&1; then echo "CHECK tests-green ok"; else echo "CHECK tests-green fail"; fail=1; fi
out=$(printf 'Max Items = 3\n# c\n\nLog Level=debug\n' | python3 app.py 2>/dev/null)
if [ "$out" = "$(printf 'max-items=3\nlog-level=debug')" ]; then echo "CHECK app-runs ok"; else echo "CHECK app-runs fail: [$out]"; fail=1; fi
# the helper bodies moved unchanged
if grep -q 'def slugify(text):' helpers.py && grep -q 'def parse_kv(line):' helpers.py && grep -q 'text.strip("-")' helpers.py && grep -q "raise ValueError" helpers.py; then echo "CHECK helpers-content ok"; else echo "CHECK helpers-content fail"; fail=1; fi
n=$(ls *.py 2>/dev/null | wc -l)
if [ "$n" = 3 ]; then echo "CHECK no-extra-files ok"; else echo "CHECK no-extra-files fail ($n .py files)"; fail=1; fi
exit $fail
