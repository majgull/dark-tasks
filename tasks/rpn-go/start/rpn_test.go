package main

import "testing"

func TestEvalValues(t *testing.T) {
	cases := map[string]int{
		"1 2 +": 3, "3 4 -": -1, "7 2 /": 3, "-7 2 /": -3, "2 3 4 * +": 14,
		"5 1 2 + 4 * + 3 -": 14, "42": 42, "1   2 +": 3, "6 3 / 2 /": 1,
	}
	for expr, want := range cases {
		got, err := Eval(expr)
		if err != nil || got != want {
			t.Errorf("Eval(%q) = %d, %v; want %d", expr, got, err, want)
		}
	}
}

func TestEvalErrors(t *testing.T) {
	cases := map[string]string{
		"1 0 /": "division by zero", "1 +": "stack underflow", "+": "stack underflow",
		"1 2": "malformed expression", "": "malformed expression", "1 x +": "bad token: x",
		"1.5 2 +": "bad token: 1.5",
	}
	for expr, want := range cases {
		got, err := Eval(expr)
		if err == nil || err.Error() != want || got != 0 {
			t.Errorf("Eval(%q) = %d, %v; want 0, %q", expr, got, err, want)
		}
	}
}
