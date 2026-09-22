package main

import "sort"

// Merge returns the union of the closed integer intervals in iv as a list of
// disjoint intervals sorted by start. Intervals that overlap or touch (for
// example [1,3] and [3,5]) are merged into one. The input may be in any
// order and is not modified. An empty input gives an empty result.
func Merge(iv [][2]int) [][2]int {
	if len(iv) == 0 {
		return nil
	}
	s := make([][2]int, len(iv))
	copy(s, iv)
	sort.Slice(s, func(i, j int) bool { return s[i][0] < s[j][0] })
	out := [][2]int{s[0]}
	for _, cur := range s[1:] {
		last := &out[len(out)-1]
		if cur[0] > last[1] {
			out = append(out, cur)
		} else if cur[1] > last[1] {
			last[1] = cur[1]
		}
	}
	return out
}
