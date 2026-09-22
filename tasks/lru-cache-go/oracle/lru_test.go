package main

import (
	"reflect"
	"testing"
)

func TestPutGetEvict(t *testing.T) {
	c := NewLRU(2)
	c.Put("a", 1)
	c.Put("b", 2)
	if v, ok := c.Get("a"); !ok || v != 1 {
		t.Fatalf("a = %d, %v", v, ok)
	}
	c.Put("c", 3) // evicts b, the least recently used
	if _, ok := c.Get("b"); ok {
		t.Fatal("b survived")
	}
	if got := c.Keys(); !reflect.DeepEqual(got, []string{"c", "a"}) {
		t.Fatalf("keys %v", got)
	}
	if c.Len() != 2 {
		t.Fatalf("len %d", c.Len())
	}
}

func TestUpdateKeepsSize(t *testing.T) {
	c := NewLRU(1)
	c.Put("a", 1)
	c.Put("a", 2)
	if v, _ := c.Get("a"); v != 2 || c.Len() != 1 {
		t.Fatalf("a = %d, len %d", v, c.Len())
	}
}

func TestBadCapacityPanics(t *testing.T) {
	defer func() {
		if recover() == nil {
			t.Fatal("no panic")
		}
	}()
	NewLRU(0)
}
