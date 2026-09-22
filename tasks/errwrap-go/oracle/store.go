package main

import (
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// ErrNotFound is returned by Get for a key the store does not hold.
var ErrNotFound = errors.New("key not found")

// Store is a flat key=value file loaded into memory.
type Store struct {
	values map[string]int
}

// Load reads path, one "key=int" per line, blank lines ignored.
func Load(path string) (*Store, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("load %s: %w", path, err)
	}
	s := &Store{values: map[string]int{}}
	for i, line := range strings.Split(string(data), "\n") {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		key, val, ok := strings.Cut(line, "=")
		if !ok {
			return nil, fmt.Errorf("load %s: line %d: no '='", path, i+1)
		}
		n, err := strconv.Atoi(strings.TrimSpace(val))
		if err != nil {
			return nil, fmt.Errorf("load %s: line %d: %w", path, i+1, err)
		}
		s.values[strings.TrimSpace(key)] = n
	}
	return s, nil
}

// Get returns the value for key.
func (s *Store) Get(key string) (int, error) {
	v, ok := s.values[key]
	if !ok {
		return 0, fmt.Errorf("get %q: %w", key, ErrNotFound)
	}
	return v, nil
}

// Sum adds the values of keys; a missing key is an error.
func (s *Store) Sum(keys ...string) (int, error) {
	total := 0
	for _, k := range keys {
		v, err := s.Get(k)
		if err != nil {
			return 0, fmt.Errorf("sum: %w", err)
		}
		total += v
	}
	return total, nil
}
