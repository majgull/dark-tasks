#!/bin/bash
# hidden acceptance for errwrap-go; runs at the repo root in the staging VM
export HOME="${HOME:-/root}" GOCACHE="${GOCACHE:-/root/.cache/go-build}" GOPATH="${GOPATH:-/root/go}"
export PATH="$PATH:/usr/local/go/bin"
fail=0
if grep -qE '%v",[[:space:]]*(err|ErrNotFound)\)|%v",[[:space:]]*[a-z]+,[[:space:]]*err\)|%v",[[:space:]]*path,[[:space:]]*i\+1,[[:space:]]*err\)' store.go; then echo "CHECK no-v-wrap fail"; fail=1; else echo "CHECK no-v-wrap ok"; fi
if [ "$(grep -c '%w' store.go)" = 4 ]; then echo "CHECK four-w-wraps ok"; else echo "CHECK four-w-wraps fail ($(grep -c '%w' store.go))"; fail=1; fi
if grep -q 'var ErrNotFound = errors.New("key not found")' store.go && grep -q 'func (s \*Store) Sum(keys ...string)' store.go; then echo "CHECK rest-untouched ok"; else echo "CHECK rest-untouched fail"; fail=1; fi
if grep -q 'func TestMessages' store_test.go && grep -q '`sum: get "zz": key not found`' store_test.go; then echo "CHECK tests-untouched ok"; else echo "CHECK tests-untouched fail"; fail=1; fi
n=$(ls *.go | wc -l)
if [ "$n" = 3 ]; then echo "CHECK no-extra-files ok"; else echo "CHECK no-extra-files fail ($n .go files)"; fail=1; fi
if go test ./... >/tmp/acc.log 2>&1; then echo "CHECK visible-tests ok"; else echo "CHECK visible-tests fail"; tail -5 /tmp/acc.log; fail=1; fi
cat > zz_acceptance_test.go <<'GO'
package main

import (
	"errors"
	"io/fs"
	"path/filepath"
	"strconv"
	"testing"
)

func TestAcceptUnwrap(t *testing.T) {
	s, err := Load(write(t, "a=1\n"))
	if err != nil {
		t.Fatal(err)
	}
	_, err = s.Get("nope")
	if !errors.Is(err, ErrNotFound) {
		t.Fatalf("Get: errors.Is(ErrNotFound) false: %v", err)
	}
	_, err = s.Sum("a", "nope")
	if !errors.Is(err, ErrNotFound) {
		t.Fatalf("Sum: errors.Is(ErrNotFound) false: %v", err)
	}
	_, err = Load(filepath.Join(t.TempDir(), "missing.txt"))
	if !errors.Is(err, fs.ErrNotExist) {
		t.Fatalf("Load: errors.Is(fs.ErrNotExist) false: %v", err)
	}
	_, err = Load(write(t, "a=zz\n"))
	var ne *strconv.NumError
	if !errors.As(err, &ne) {
		t.Fatalf("Load: errors.As(*strconv.NumError) false: %v", err)
	}
}
GO
if go test ./... >/tmp/acc.log 2>&1; then echo "CHECK hidden-tests ok"; else echo "CHECK hidden-tests fail"; tail -20 /tmp/acc.log; fail=1; fi
rm -f zz_acceptance_test.go
if go vet ./... >/dev/null 2>&1; then echo "CHECK vet ok"; else echo "CHECK vet fail"; fail=1; fi
exit $fail
