#!/bin/bash
# hidden acceptance for rpn-go; runs at the repo root in the staging VM
export HOME="${HOME:-/root}" GOCACHE="${GOCACHE:-/root/.cache/go-build}" GOPATH="${GOPATH:-/root/go}"
export PATH="$PATH:/usr/local/go/bin"
fail=0
if go test ./... >/tmp/acc.log 2>&1; then echo "CHECK visible-tests ok"; else echo "CHECK visible-tests fail"; tail -5 /tmp/acc.log; fail=1; fi
if grep -q '"5 1 2 + 4 \* + 3 -": 14' rpn_test.go && grep -q '"1.5 2 +": "bad token: 1.5"' rpn_test.go; then echo "CHECK tests-untouched ok"; else echo "CHECK tests-untouched fail"; fail=1; fi
n=$(ls *.go | wc -l)
if [ "$n" = 3 ]; then echo "CHECK no-extra-files ok"; else echo "CHECK no-extra-files fail ($n .go files)"; fail=1; fi
cat > zz_acceptance_test.go <<'GO'
package main

import "testing"

func TestAcceptValues(t *testing.T) {
	cases := map[string]int{
		"10 3 /": 3, "-10 3 /": -3, "10 -3 /": -3, "-10 -3 /": 3, "0 5 /": 0,
		"1 2 3 + +": 6, "1 2 3 + -": -4, "2 3 - 4 *": -4, "  7  ": 7, "-0": 0,
		"1 2 * 3 * 4 *": 24, "100 7 / 7 *": 98,
	}
	for expr, want := range cases {
		got, err := Eval(expr)
		if err != nil || got != want {
			t.Errorf("Eval(%q) = %d, %v; want %d", expr, got, err, want)
		}
	}
}

func TestAcceptErrors(t *testing.T) {
	cases := map[string]string{
		"0 0 /": "division by zero", "1 2 + +": "stack underflow", "1 2 3 +": "malformed expression",
		"   ": "malformed expression", "1 2 ^": "bad token: ^", "+1 1 +": "bad token: +1",
		"1 2 3 4 + +": "malformed expression", "1 -": "stack underflow",
	}
	for expr, want := range cases {
		got, err := Eval(expr)
		if err == nil || err.Error() != want || got != 0 {
			t.Errorf("Eval(%q) = %d, %v; want 0, %q", expr, got, err, want)
		}
	}
}

func TestAcceptNoPanicOnDivZero(t *testing.T) {
	defer func() {
		if r := recover(); r != nil {
			t.Fatalf("panic: %v", r)
		}
	}()
	_, _ = Eval("5 0 /")
}
GO
if go test ./... >/tmp/acc.log 2>&1; then echo "CHECK hidden-tests ok"; else echo "CHECK hidden-tests fail"; tail -20 /tmp/acc.log; fail=1; fi
rm -f zz_acceptance_test.go
if go vet ./... >/dev/null 2>&1; then echo "CHECK vet ok"; else echo "CHECK vet fail"; fail=1; fi
exit $fail
