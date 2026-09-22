package main

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func write(t *testing.T, body string) string {
	p := filepath.Join(t.TempDir(), "s.txt")
	if err := os.WriteFile(p, []byte(body), 0o644); err != nil {
		t.Fatal(err)
	}
	return p
}

func TestLoadAndGet(t *testing.T) {
	s, err := Load(write(t, "a=1\n\nb = 2\n"))
	if err != nil {
		t.Fatal(err)
	}
	if v, _ := s.Get("b"); v != 2 {
		t.Fatalf("b = %d", v)
	}
	if sum, _ := s.Sum("a", "b"); sum != 3 {
		t.Fatalf("sum = %d", sum)
	}
}

func TestMessages(t *testing.T) {
	s, _ := Load(write(t, "a=1\n"))
	if _, err := s.Get("zz"); err == nil || err.Error() != `get "zz": key not found` {
		t.Fatalf("got %v", err)
	}
	if _, err := s.Sum("a", "zz"); err == nil || err.Error() != `sum: get "zz": key not found` {
		t.Fatalf("got %v", err)
	}
	_, err := Load(write(t, "a=x\n"))
	if err == nil || !strings.HasPrefix(err.Error(), "load ") || !strings.HasSuffix(err.Error(), `: line 1: strconv.Atoi: parsing "x": invalid syntax`) {
		t.Fatalf("got %v", err)
	}
	_, err = Load(write(t, "novalue\n"))
	if err == nil || !strings.HasSuffix(err.Error(), ": line 1: no '='") {
		t.Fatalf("got %v", err)
	}
	_, err = Load(filepath.Join(t.TempDir(), "missing.txt"))
	if err == nil || !strings.HasPrefix(err.Error(), "load ") || !strings.Contains(err.Error(), "no such file") {
		t.Fatalf("got %v", err)
	}
}
