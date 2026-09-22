package main

import (
	"errors"
	"sort"
)

// ErrEmpty is returned for an empty input.
var ErrEmpty = errors.New("stats: empty input")

// Median returns the median of xs: the middle value of the sorted
// values when len(xs) is odd, the mean of the two middle values when it
// is even. It returns ErrEmpty for an empty slice and never modifies xs.
func Median(xs []float64) (float64, error) {
	if len(xs) == 0 {
		return 0, ErrEmpty
	}
	sort.Float64s(xs)
	return xs[len(xs)/2], nil
}

// Percentile returns the value at percentile p (0 <= p <= 100) of xs
// by the nearest-rank method: sort ascending, take the element at index
// ceil(p/100 * n) - 1, with p = 0 giving the smallest value. It returns
// ErrEmpty for an empty slice, an error for p outside 0..100, and never
// modifies xs.
func Percentile(xs []float64, p float64) (float64, error) {
	if len(xs) == 0 {
		return 0, ErrEmpty
	}
	if p < 0 || p > 100 {
		return 0, errors.New("stats: percentile out of range")
	}
	sort.Float64s(xs)
	idx := int(p / 100 * float64(len(xs)))
	return xs[idx], nil
}
