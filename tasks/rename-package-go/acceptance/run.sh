#!/bin/bash
# hidden acceptance for rename-package-go; runs at the repo root in the staging VM
export HOME="${HOME:-/root}" GOCACHE="${GOCACHE:-/root/.cache/go-build}" GOPATH="${GOPATH:-/root/go}"
export PATH="$PATH:/usr/local/go/bin"
fail=0
if [ ! -e internal/util ] || [ -z "$(ls -A internal/util 2>/dev/null)" ]; then echo "CHECK old-package-gone ok"; else echo "CHECK old-package-gone fail"; fail=1; fi
if [ -f internal/strutil/strutil.go ] && [ -f internal/strutil/strutil_test.go ]; then echo "CHECK new-files ok"; else echo "CHECK new-files fail"; fail=1; fi
if grep -q '^package strutil$' internal/strutil/strutil.go 2>/dev/null && grep -q '^package strutil$' internal/strutil/strutil_test.go 2>/dev/null; then echo "CHECK package-line ok"; else echo "CHECK package-line fail"; fail=1; fi
if grep -q '"app/internal/strutil"' main.go && grep -q 'strutil.Reverse' main.go && grep -q 'strutil.Initials' main.go && ! grep -q '"app/internal/util"' main.go; then echo "CHECK main-imports ok"; else echo "CHECK main-imports fail"; fail=1; fi
if grep -q 'func Reverse(s string) string' internal/strutil/strutil.go 2>/dev/null && grep -q 'func Initials(s string) string' internal/strutil/strutil.go 2>/dev/null && grep -q 'func TestInitials' internal/strutil/strutil_test.go 2>/dev/null; then echo "CHECK content-kept ok"; else echo "CHECK content-kept fail"; fail=1; fi
python3 - <<'PY'
import subprocess, sys
bad = 0
def chk(name, ok, note=""):
    global bad
    bad += not ok
    print(f"CHECK {name} {'ok' if ok else 'fail'}" + ("" if ok else f" ({note})"))
def after_package_line(text):
    lines = text.splitlines(keepends=True)
    for i, l in enumerate(lines):
        if l.startswith("package "):
            return "".join(lines[i + 1:])
    return None
root = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"],
                       capture_output=True, text=True).stdout.strip().splitlines()
pairs = [("internal/util/util.go", "internal/strutil/strutil.go", "strutil-unchanged"),
         ("internal/util/util_test.go", "internal/strutil/strutil_test.go", "strutil-test-unchanged")]
for old_path, new_path, name in pairs:
    orig = subprocess.run(["git", "show", f"{root[0]}:{old_path}"],
                           capture_output=True, text=True).stdout if root else ""
    try:
        new = open(new_path, encoding="utf-8").read()
    except OSError as e:
        chk(name, False, repr(e)); continue
    a, b = after_package_line(orig), after_package_line(new)
    chk(name, a is not None and a == b)
sys.exit(1 if bad else 0)
PY
[ $? = 0 ] || fail=1
n=$(find . -name '*.go' -not -path './.git/*' | wc -l)
if [ "$n" = 3 ]; then echo "CHECK no-extra-files ok"; else echo "CHECK no-extra-files fail ($n .go files)"; fail=1; fi
if go vet ./... >/dev/null 2>&1; then echo "CHECK vet ok"; else echo "CHECK vet fail"; fail=1; fi
if go test ./... >/tmp/acc.log 2>&1; then echo "CHECK tests ok"; else echo "CHECK tests fail"; tail -5 /tmp/acc.log; fail=1; fi
want=$(printf 'krad\nDR')
got=$(go run . 2>/dev/null)
if [ "$got" = "$want" ]; then echo "CHECK run-output ok"; else echo "CHECK run-output fail (got: $got)"; fail=1; fi
exit $fail
