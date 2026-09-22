package main

import "testing"

func TestCompareSemver(t *testing.T) {
	cases := []struct {
		a, b string
		want int
	}{
		{"1.0.0", "1.0.0", 0},
		{"1.0.0", "2.0.0", -1},
		{"1.0.0-alpha", "1.0.0", -1},
		{"1.0.0-beta.2", "1.0.0-beta.11", -1},
		{"1.0.0+b1", "1.0.0+b2", 0},
	}
	for _, c := range cases {
		got, err := CompareSemver(c.a, c.b)
		if err != nil || got != c.want {
			t.Fatalf("CompareSemver(%q, %q) = %d, %v; want %d", c.a, c.b, got, err, c.want)
		}
	}
	if _, err := CompareSemver("1.0", "1.0.0"); err == nil {
		t.Fatal("expected an error for 1.0")
	}
}
