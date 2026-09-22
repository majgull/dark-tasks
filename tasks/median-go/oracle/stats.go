package main

import (
	"errors"
	"math"
	"sort"
)

// ErrEmpty is returned for an empty input.
var ErrEmpty = errors.New("stats: empty input")

func sortedCopy(xs []float64) []float64 {
	ys := make([]float64, len(xs))
	copy(ys, xs)
	sort.Float64s(ys)
	return ys
}

// Median returns the median of xs: the middle value of the sorted
// values when len(xs) is odd, the mean of the two middle values when it
// is even. It returns ErrEmpty for an empty slice and never modifies xs.
func Median(xs []float64) (float64, error) {
	if len(xs) == 0 {
		return 0, ErrEmpty
	}
	ys := sortedCopy(xs)
	n := len(ys)
	if n%2 == 1 {
		return ys[n/2], nil
	}
	return (ys[n/2-1] + ys[n/2]) / 2, nil
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
	ys := sortedCopy(xs)
	idx := int(math.Ceil(p/100*float64(len(ys)))) - 1
	if idx < 0 {
		idx = 0
	}
	return ys[idx], nil
}
