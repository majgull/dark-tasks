package main

import (
	"testing"
	"time"
)

type clock struct{ t time.Time }

func (c *clock) now() time.Time { return c.t }
func (c *clock) advance(d time.Duration) { c.t = c.t.Add(d) }

func TestBurstThenRefill(t *testing.T) {
	c := &clock{t: time.Unix(1000, 0)}
	b := NewBucket(2, 1, c.now)
	if !b.Allow() || !b.Allow() || b.Allow() {
		t.Fatal("burst of 2 then refusal expected")
	}
	c.advance(500 * time.Millisecond)
	if got := b.Tokens(); got != 0.5 {
		t.Fatalf("tokens = %v", got)
	}
	if b.Allow() {
		t.Fatal("half a token allowed a call")
	}
	c.advance(time.Second)
	if !b.Allow() {
		t.Fatal("refilled token refused")
	}
}

func TestCapAndBackwardsClock(t *testing.T) {
	c := &clock{t: time.Unix(1000, 0)}
	b := NewBucket(3, 10, c.now)
	c.advance(time.Hour)
	if got := b.Tokens(); got != 3 {
		t.Fatalf("tokens over capacity: %v", got)
	}
	b.Allow()
	c.advance(-time.Hour)
	if got := b.Tokens(); got != 2 {
		t.Fatalf("backwards clock changed tokens: %v", got)
	}
}

func TestPanics(t *testing.T) {
	for _, tc := range []struct {
		cap int
		ps  float64
		now func() time.Time
	}{{0, 1, time.Now}, {1, 0, time.Now}, {1, 1, nil}} {
		func() {
			defer func() {
				if recover() == nil {
					t.Fatalf("no panic for %+v", tc)
				}
			}()
			NewBucket(tc.cap, tc.ps, tc.now)
		}()
	}
}
