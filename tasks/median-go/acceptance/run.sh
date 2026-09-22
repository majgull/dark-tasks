#!/bin/bash
# hidden acceptance for median-go; runs at the repo root in the staging VM
export HOME="${HOME:-/root}" GOCACHE="${GOCACHE:-/root/.cache/go-build}" GOPATH="${GOPATH:-/root/go}"
export PATH="$PATH:/usr/local/go/bin"
fail=0
if go test ./... >/tmp/acc.log 2>&1; then echo "CHECK visible-tests ok"; else echo "CHECK visible-tests fail"; tail -5 /tmp/acc.log; fail=1; fi
if grep -q 'func TestMedianDoesNotModifyInput' stats_test.go && grep -q '30: 20, 40: 20, 50: 35' stats_test.go; then echo "CHECK tests-untouched ok"; else echo "CHECK tests-untouched fail"; fail=1; fi
n=$(ls *.go | wc -l)
if [ "$n" = 3 ]; then echo "CHECK no-extra-files ok"; else echo "CHECK no-extra-files fail ($n .go files)"; fail=1; fi
cat > zz_acceptance_test.go <<'GO'
package main

import (
	"errors"
	"testing"
)

func TestAcceptMedianMore(t *testing.T) {
	cases := []struct {
		in   []float64
		want float64
	}{
		{[]float64{1}, 1}, {[]float64{2, 1}, 1.5}, {[]float64{-3, -1, -2}, -2},
		{[]float64{1, 1, 1, 1}, 1}, {[]float64{9, 2, 7, 4, 5, 6}, 5.5}, {[]float64{0.5, 0.25}, 0.375},
	}
	for _, c := range cases {
		got, err := Median(c.in)
		if err != nil || got != c.want {
			t.Errorf("Median(%v) = %v, %v; want %v", c.in, got, err, c.want)
		}
	}
}

func TestAcceptPercentileNearestRank(t *testing.T) {
	xs := []float64{7, 3, 9, 1}
	cases := map[float64]float64{0: 1, 1: 1, 25: 1, 26: 3, 50: 3, 51: 7, 75: 7, 76: 9, 99: 9, 100: 9}
	for p, want := range cases {
		got, err := Percentile(xs, p)
		if err != nil || got != want {
			t.Errorf("Percentile(%v, %v) = %v, %v; want %v", xs, p, got, err, want)
		}
	}
	if xs[0] != 7 || xs[1] != 3 || xs[2] != 9 || xs[3] != 1 {
		t.Fatalf("input modified: %v", xs)
	}
}

func TestAcceptEmptyIsErrEmpty(t *testing.T) {
	if _, err := Median([]float64{}); !errors.Is(err, ErrEmpty) {
		t.Fatal(err)
	}
	if _, err := Percentile([]float64{}, 0); !errors.Is(err, ErrEmpty) {
		t.Fatal(err)
	}
}
GO
if go test ./... >/tmp/acc.log 2>&1; then echo "CHECK hidden-tests ok"; else echo "CHECK hidden-tests fail"; tail -20 /tmp/acc.log; fail=1; fi
rm -f zz_acceptance_test.go
if go vet ./... >/dev/null 2>&1; then echo "CHECK vet ok"; else echo "CHECK vet fail"; fail=1; fi
exit $fail
