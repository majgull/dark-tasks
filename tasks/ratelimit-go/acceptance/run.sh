#!/bin/bash
# hidden acceptance for ratelimit-go; runs at the repo root in the staging VM
export HOME="${HOME:-/root}" GOCACHE="${GOCACHE:-/root/.cache/go-build}" GOPATH="${GOPATH:-/root/go}"
export PATH="$PATH:/usr/local/go/bin"
fail=0
if [ -f bucket.go ] && [ -f bucket_test.go ]; then echo "CHECK files ok"; else echo "CHECK files fail"; fail=1; fi
if grep -q 'fmt.Println("app: ok")' main.go; then echo "CHECK main-untouched ok"; else echo "CHECK main-untouched fail"; fail=1; fi
if grep -q 'time.Sleep' bucket_test.go 2>/dev/null; then echo "CHECK no-sleep-in-tests fail"; fail=1; else echo "CHECK no-sleep-in-tests ok"; fi
if go vet ./... >/dev/null 2>&1; then echo "CHECK vet ok"; else echo "CHECK vet fail"; fail=1; fi
if timeout 120 go test ./... >/tmp/acc.log 2>&1; then echo "CHECK own-tests ok"; else echo "CHECK own-tests fail"; tail -5 /tmp/acc.log; fail=1; fi
cat > zz_acceptance_test.go <<'GO'
package main

import (
	"math"
	"testing"
	"time"
)

type acceptClock struct{ t time.Time }

func (c *acceptClock) now() time.Time { return c.t }

func near(a, b float64) bool { return math.Abs(a-b) < 1e-9 }

func TestAcceptSpecExample(t *testing.T) {
	c := &acceptClock{t: time.Unix(5000, 0)}
	b := NewBucket(2, 1, c.now)
	if !b.Allow() || !b.Allow() {
		t.Fatal("a full bucket refused")
	}
	if b.Allow() {
		t.Fatal("an empty bucket allowed")
	}
	c.t = c.t.Add(500 * time.Millisecond)
	if got := b.Tokens(); !near(got, 0.5) {
		t.Fatalf("Tokens after 0.5s = %v", got)
	}
	if b.Allow() {
		t.Fatal("0.5 tokens allowed")
	}
	c.t = c.t.Add(time.Second)
	if !b.Allow() {
		t.Fatal("1.5 tokens refused")
	}
	if got := b.Tokens(); !near(got, 0.5) {
		t.Fatalf("Tokens after take = %v", got)
	}
}

func TestAcceptFractionalRateAndCap(t *testing.T) {
	c := &acceptClock{t: time.Unix(5000, 0)}
	b := NewBucket(5, 0.25, c.now) // one token every 4 s
	for i := 0; i < 5; i++ {
		if !b.Allow() {
			t.Fatalf("call %d refused on a full bucket", i)
		}
	}
	c.t = c.t.Add(3 * time.Second)
	if b.Allow() {
		t.Fatal("0.75 tokens allowed")
	}
	c.t = c.t.Add(time.Second)
	if !b.Allow() {
		t.Fatal("1.0 tokens refused")
	}
	c.t = c.t.Add(24 * time.Hour)
	if got := b.Tokens(); !near(got, 5) {
		t.Fatalf("cap not applied: %v", got)
	}
}

func TestAcceptTokensDoesNotTake(t *testing.T) {
	c := &acceptClock{t: time.Unix(5000, 0)}
	b := NewBucket(1, 1, c.now)
	for i := 0; i < 3; i++ {
		if got := b.Tokens(); !near(got, 1) {
			t.Fatalf("Tokens() took a token: %v", got)
		}
	}
	if !b.Allow() {
		t.Fatal("token gone")
	}
}

func TestAcceptBackwardsClock(t *testing.T) {
	c := &acceptClock{t: time.Unix(5000, 0)}
	b := NewBucket(2, 1, c.now)
	b.Allow()
	c.t = c.t.Add(-10 * time.Second)
	if got := b.Tokens(); !near(got, 1) {
		t.Fatalf("backwards clock changed tokens: %v", got)
	}
	// what the reference time becomes after a backwards reading is not
	// specified; only "adds nothing" is
}

func TestAcceptPanics(t *testing.T) {
	cases := []func(){
		func() { NewBucket(0, 1, time.Now) },
		func() { NewBucket(-1, 1, time.Now) },
		func() { NewBucket(1, 0, time.Now) },
		func() { NewBucket(1, -0.5, time.Now) },
		func() { NewBucket(1, 1, nil) },
	}
	for i, f := range cases {
		func() {
			defer func() {
				if recover() == nil {
					t.Fatalf("case %d did not panic", i)
				}
			}()
			f()
		}()
	}
}
GO
if timeout 120 go test ./... >/tmp/acc.log 2>&1; then echo "CHECK hidden-tests ok"; else echo "CHECK hidden-tests fail"; tail -20 /tmp/acc.log; fail=1; fi
rm -f zz_acceptance_test.go
n=$(ls *.go | wc -l)
if [ "$n" = 3 ]; then echo "CHECK no-extra-files ok"; else echo "CHECK no-extra-files fail ($n .go files)"; fail=1; fi
exit $fail
