package strutil

import "testing"

func TestReverse(t *testing.T) {
	if got := Reverse("héllo"); got != "olléh" {
		t.Fatalf("got %q", got)
	}
}

func TestInitials(t *testing.T) {
	if got := Initials("dark factory runner"); got != "DFR" {
		t.Fatalf("got %q", got)
	}
}
