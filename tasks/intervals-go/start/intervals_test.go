package main

import (
	"reflect"
	"testing"
)

func TestMergeOverlapping(t *testing.T) {
	got := Merge([][2]int{{1, 3}, {2, 6}, {8, 10}})
	want := [][2]int{{1, 6}, {8, 10}}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("got %v, want %v", got, want)
	}
}

func TestMergeTouching(t *testing.T) {
	got := Merge([][2]int{{1, 3}, {3, 5}})
	want := [][2]int{{1, 5}}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("got %v, want %v", got, want)
	}
}

func TestMergeUnsorted(t *testing.T) {
	got := Merge([][2]int{{5, 7}, {1, 2}, {6, 9}})
	want := [][2]int{{1, 2}, {5, 9}}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("got %v, want %v", got, want)
	}
}

func TestMergeEmpty(t *testing.T) {
	if got := Merge(nil); len(got) != 0 {
		t.Fatalf("got %v, want empty", got)
	}
}
