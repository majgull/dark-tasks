package main

import (
	"errors"
	"testing"
)

func TestMedianOdd(t *testing.T) {
	m, err := Median([]float64{3, 1, 2})
	if err != nil || m != 2 {
		t.Fatalf("got %v, %v", m, err)
	}
}

func TestMedianEven(t *testing.T) {
	m, err := Median([]float64{4, 1, 3, 2})
	if err != nil || m != 2.5 {
		t.Fatalf("got %v, %v; want 2.5", m, err)
	}
}

func TestMedianEmpty(t *testing.T) {
	if _, err := Median(nil); !errors.Is(err, ErrEmpty) {
		t.Fatalf("got %v; want ErrEmpty", err)
	}
}

func TestMedianDoesNotModifyInput(t *testing.T) {
	xs := []float64{3, 1, 2}
	if _, err := Median(xs); err != nil {
		t.Fatal(err)
	}
	if xs[0] != 3 || xs[1] != 1 || xs[2] != 2 {
		t.Fatalf("input modified: %v", xs)
	}
}

func TestPercentile(t *testing.T) {
	xs := []float64{15, 20, 35, 40, 50}
	cases := map[float64]float64{0: 15, 5: 15, 30: 20, 40: 20, 50: 35, 100: 50}
	for p, want := range cases {
		got, err := Percentile(xs, p)
		if err != nil || got != want {
			t.Errorf("Percentile(p=%v) = %v, %v; want %v", p, got, err, want)
		}
	}
	if xs[0] != 15 || xs[4] != 50 || xs[2] != 35 {
		t.Fatalf("input modified: %v", xs)
	}
}

func TestPercentileErrors(t *testing.T) {
	if _, err := Percentile(nil, 50); !errors.Is(err, ErrEmpty) {
		t.Fatalf("empty: got %v", err)
	}
	for _, p := range []float64{-1, 101} {
		if _, err := Percentile([]float64{1}, p); err == nil {
			t.Fatalf("p=%v accepted", p)
		}
	}
}
