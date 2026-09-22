#!/bin/bash
# hidden acceptance for intervals-go; runs at the repo root in the staging VM
export HOME="${HOME:-/root}" GOCACHE="${GOCACHE:-/root/.cache/go-build}" GOPATH="${GOPATH:-/root/go}"
export PATH="$PATH:/usr/local/go/bin"
fail=0
if grep -q 'func TestMergeTouching' intervals_test.go && grep -q '{5, 7}, {1, 2}, {6, 9}' intervals_test.go; then echo "CHECK tests-untouched ok"; else echo "CHECK tests-untouched fail"; fail=1; fi
n=$(ls *.go | wc -l)
if [ "$n" = 3 ]; then echo "CHECK no-extra-files ok"; else echo "CHECK no-extra-files fail ($n .go files)"; fail=1; fi
if go test ./... >/tmp/vis.log 2>&1; then echo "CHECK visible-tests ok"; else echo "CHECK visible-tests fail"; tail -10 /tmp/vis.log; fail=1; fi
cat > zz_acceptance_test.go <<'EOF'
package main

import (
	"reflect"
	"testing"
)

func TestAcceptMerge(t *testing.T) {
	cases := []struct {
		in, want [][2]int
	}{
		{[][2]int{{1, 10}, {2, 3}}, [][2]int{{1, 10}}},
		{[][2]int{{4, 4}}, [][2]int{{4, 4}}},
		{[][2]int{{1, 2}, {2, 3}, {3, 4}}, [][2]int{{1, 4}}},
		{[][2]int{{9, 12}, {1, 2}, {3, 8}, {2, 3}}, [][2]int{{1, 8}, {9, 12}}},
		{[][2]int{{-5, -1}, {-2, 0}, {1, 1}}, [][2]int{{-5, 0}, {1, 1}}}, // adjacent integers do not touch
		{[][2]int{{-5, -1}, {-2, 0}, {0, 1}}, [][2]int{{-5, 1}}},
		{[][2]int{{1, 2}, {4, 5}, {7, 8}}, [][2]int{{1, 2}, {4, 5}, {7, 8}}},
	}
	for _, c := range cases {
		got := Merge(c.in)
		if !reflect.DeepEqual(got, c.want) {
			t.Fatalf("Merge(%v) = %v, want %v", c.in, got, c.want)
		}
	}
	if got := Merge([][2]int{}); len(got) != 0 {
		t.Fatalf("Merge(empty) = %v", got)
	}
}

func TestAcceptInputNotModified(t *testing.T) {
	in := [][2]int{{5, 7}, {1, 2}, {6, 9}}
	before := make([][2]int, len(in))
	copy(before, in)
	Merge(in)
	if !reflect.DeepEqual(in, before) {
		t.Fatalf("input modified: %v (was %v)", in, before)
	}
}
EOF
if go test ./... >/tmp/acc.log 2>&1; then echo "CHECK hidden-tests ok"; else echo "CHECK hidden-tests fail"; tail -20 /tmp/acc.log; fail=1; fi
rm -f zz_acceptance_test.go
exit $fail
