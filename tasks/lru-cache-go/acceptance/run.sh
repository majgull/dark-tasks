#!/bin/bash
# hidden acceptance for lru-cache-go; runs at the repo root in the staging VM
export HOME="${HOME:-/root}" GOCACHE="${GOCACHE:-/root/.cache/go-build}" GOPATH="${GOPATH:-/root/go}"
export PATH="$PATH:/usr/local/go/bin"
fail=0
if [ -f lru.go ] && [ -f lru_test.go ]; then echo "CHECK files ok"; else echo "CHECK files fail"; fail=1; fi
if grep -q 'fmt.Println("app: ok")' main.go; then echo "CHECK main-untouched ok"; else echo "CHECK main-untouched fail"; fail=1; fi
if go vet ./... >/dev/null 2>&1; then echo "CHECK vet ok"; else echo "CHECK vet fail"; fail=1; fi
if go test ./... >/tmp/acc.log 2>&1; then echo "CHECK own-tests ok"; else echo "CHECK own-tests fail"; tail -5 /tmp/acc.log; fail=1; fi
cat > zz_acceptance_test.go <<'GO'
package main

import (
	"reflect"
	"testing"
)

func TestAcceptOrderAndEviction(t *testing.T) {
	c := NewLRU(3)
	for _, k := range []string{"a", "b", "c"} {
		c.Put(k, len(k))
	}
	if got := c.Keys(); !reflect.DeepEqual(got, []string{"c", "b", "a"}) {
		t.Fatalf("keys after puts: %v", got)
	}
	c.Get("a") // a is now most recent
	if got := c.Keys(); !reflect.DeepEqual(got, []string{"a", "c", "b"}) {
		t.Fatalf("keys after get: %v", got)
	}
	c.Put("d", 4) // evicts b
	if got := c.Keys(); !reflect.DeepEqual(got, []string{"d", "a", "c"}) {
		t.Fatalf("keys after evicting put: %v", got)
	}
	if _, ok := c.Get("b"); ok {
		t.Fatal("b should be evicted")
	}
	c.Put("c", 30) // update moves c to front, no eviction
	if got := c.Keys(); !reflect.DeepEqual(got, []string{"c", "d", "a"}) || c.Len() != 3 {
		t.Fatalf("keys after update: %v len %d", got, c.Len())
	}
	if v, ok := c.Get("c"); !ok || v != 30 {
		t.Fatalf("c = %d, %v", v, ok)
	}
}

func TestAcceptMissAndEmpty(t *testing.T) {
	c := NewLRU(2)
	if v, ok := c.Get("x"); ok || v != 0 {
		t.Fatalf("miss = %d, %v", v, ok)
	}
	keys := c.Keys()
	if keys == nil || len(keys) != 0 {
		t.Fatalf("empty Keys() = %#v", keys)
	}
	if c.Len() != 0 {
		t.Fatalf("len %d", c.Len())
	}
	c.Put("x", 1)
	got := c.Keys()
	got[0] = "mutated"
	if k := c.Keys(); k[0] != "x" {
		t.Fatalf("Keys() shares its backing slice: %v", k)
	}
}

func TestAcceptCapacityOne(t *testing.T) {
	c := NewLRU(1)
	c.Put("a", 1)
	c.Put("b", 2)
	if _, ok := c.Get("a"); ok || c.Len() != 1 {
		t.Fatal("capacity 1 kept two entries")
	}
	if v, ok := c.Get("b"); !ok || v != 2 {
		t.Fatalf("b = %d, %v", v, ok)
	}
}

func TestAcceptPanics(t *testing.T) {
	for _, n := range []int{0, -5} {
		func() {
			defer func() {
				if recover() == nil {
					t.Fatalf("NewLRU(%d) did not panic", n)
				}
			}()
			NewLRU(n)
		}()
	}
}

func TestAcceptManyOps(t *testing.T) {
	c := NewLRU(100)
	for i := 0; i < 100000; i++ {
		k := string(rune('a' + i%26))
		c.Put(k+string(rune('a'+(i/26)%26)), i)
		c.Get(k)
	}
	if c.Len() != 100 {
		t.Fatalf("len %d", c.Len())
	}
}
GO
if go test ./... >/tmp/acc.log 2>&1; then echo "CHECK hidden-tests ok"; else echo "CHECK hidden-tests fail"; tail -20 /tmp/acc.log; fail=1; fi
rm -f zz_acceptance_test.go
n=$(ls *.go | wc -l)
if [ "$n" = 3 ]; then echo "CHECK no-extra-files ok"; else echo "CHECK no-extra-files fail ($n .go files)"; fail=1; fi
exit $fail
