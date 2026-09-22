package main

// Merge returns the union of the closed integer intervals in iv as a list of
// disjoint intervals sorted by start. Intervals that overlap or touch (for
// example [1,3] and [3,5]) are merged into one. The input may be in any
// order and is not modified. An empty input gives an empty result.
func Merge(iv [][2]int) [][2]int {
	if len(iv) == 0 {
		return nil
	}
	out := [][2]int{iv[0]}
	for _, cur := range iv[1:] {
		last := &out[len(out)-1]
		if cur[0] >= last[1] {
			out = append(out, cur)
		} else if cur[1] > last[1] {
			last[1] = cur[1]
		}
	}
	return out
}
