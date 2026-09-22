#!/bin/bash
# hidden acceptance for semver-go; runs at the repo root in the staging VM
export HOME="${HOME:-/root}" GOCACHE="${GOCACHE:-/root/.cache/go-build}" GOPATH="${GOPATH:-/root/go}"
export PATH="$PATH:/usr/local/go/bin"
fail=0
if [ -f semver.go ]; then echo "CHECK semver-file ok"; else echo "CHECK semver-file fail"; fail=1; fi
if [ -f semver_test.go ]; then echo "CHECK test-file ok"; else echo "CHECK test-file fail"; fail=1; fi
cat > zz_acceptance_test.go <<'EOF'
package main

import "testing"

func acceptSign(n int) int {
	if n < 0 {
		return -1
	}
	if n > 0 {
		return 1
	}
	return 0
}

func TestAcceptOrder(t *testing.T) {
	order := []string{"1.0.0-alpha", "1.0.0-alpha.1", "1.0.0-alpha.beta", "1.0.0-beta", "1.0.0-beta.2",
		"1.0.0-beta.11", "1.0.0-rc.1", "1.0.0", "1.0.1", "1.1.0", "2.0.0", "10.0.0"}
	for i := range order {
		for j := range order {
			got, err := CompareSemver(order[i], order[j])
			if err != nil {
				t.Fatalf("CompareSemver(%q, %q): %v", order[i], order[j], err)
			}
			if got != acceptSign(i-j) {
				t.Fatalf("CompareSemver(%q, %q) = %d, want %d", order[i], order[j], got, acceptSign(i-j))
			}
		}
	}
}

func TestAcceptBuildAndEquality(t *testing.T) {
	for _, p := range [][2]string{{"1.0.0+build1", "1.0.0+build2"}, {"1.0.0-alpha+1", "1.0.0-alpha+2"}, {"0.0.0", "0.0.0"}, {"1.0.0-a.b.c", "1.0.0-a.b.c+x"}} {
		got, err := CompareSemver(p[0], p[1])
		if err != nil || got != 0 {
			t.Fatalf("CompareSemver(%q, %q) = %d, %v; want 0", p[0], p[1], got, err)
		}
	}
}

func TestAcceptPrereleaseRules(t *testing.T) {
	cases := []struct {
		a, b string
		want int
	}{
		{"1.0.0-1", "1.0.0-a", -1},        // numeric < alphanumeric
		{"1.0.0-2", "1.0.0-10", -1},       // numeric compares numerically
		{"1.0.0-a", "1.0.0-a.1", -1},      // fewer identifiers is lower
		{"1.0.0-B", "1.0.0-a", -1},        // ASCII order
		{"1.0.0-x-y", "1.0.0-x-z", -1},    // hyphens allowed
		{"2.0.0-alpha", "1.9.9", 1},       // core wins first
	}
	for _, c := range cases {
		got, err := CompareSemver(c.a, c.b)
		if err != nil || got != c.want {
			t.Fatalf("CompareSemver(%q, %q) = %d, %v; want %d", c.a, c.b, got, err, c.want)
		}
	}
}

func TestAcceptInvalid(t *testing.T) {
	for _, bad := range []string{"1.0", "a.b.c", "", "1.0.0-", "01.0.0", "1.0.0-01", "1..0", "1.0.0+", "1.0.0-a..b", " 1.0.0", "1.0.0.0", "-1.0.0"} {
		if _, err := CompareSemver(bad, "1.0.0"); err == nil {
			t.Fatalf("CompareSemver(%q, ...) accepted an invalid version", bad)
		}
		if _, err := CompareSemver("1.0.0", bad); err == nil {
			t.Fatalf("CompareSemver(..., %q) accepted an invalid version", bad)
		}
	}
}
EOF
if go test ./... >/tmp/acc.log 2>&1; then echo "CHECK semver ok"; else echo "CHECK semver fail"; tail -30 /tmp/acc.log; fail=1; fi
rm -f zz_acceptance_test.go
exit $fail
