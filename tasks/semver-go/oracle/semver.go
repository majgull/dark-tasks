package main

import (
	"errors"
	"strconv"
	"strings"
)

type semver struct {
	nums [3]int
	pre  []string
}

// CompareSemver returns -1, 0 or 1 by Semantic Versioning 2.0.0 precedence
// (reference solution).
func CompareSemver(a, b string) (int, error) {
	va, err := parseSemver(a)
	if err != nil {
		return 0, err
	}
	vb, err := parseSemver(b)
	if err != nil {
		return 0, err
	}
	for i := 0; i < 3; i++ {
		if va.nums[i] != vb.nums[i] {
			if va.nums[i] < vb.nums[i] {
				return -1, nil
			}
			return 1, nil
		}
	}
	return comparePre(va.pre, vb.pre), nil
}

func identOK(s string) bool {
	if s == "" {
		return false
	}
	for i := 0; i < len(s); i++ {
		c := s[i]
		if !(c == '-' || (c >= '0' && c <= '9') || (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
			return false
		}
	}
	return true
}

func allDigits(s string) bool {
	if s == "" {
		return false
	}
	for i := 0; i < len(s); i++ {
		if s[i] < '0' || s[i] > '9' {
			return false
		}
	}
	return true
}

func parseSemver(s string) (semver, error) {
	var v semver
	bad := errors.New("invalid semantic version: " + strconv.Quote(s))
	if i := strings.IndexByte(s, '+'); i >= 0 {
		for _, id := range strings.Split(s[i+1:], ".") {
			if !identOK(id) {
				return v, bad
			}
		}
		s = s[:i]
	}
	core := s
	if i := strings.IndexByte(s, '-'); i >= 0 {
		core = s[:i]
		for _, id := range strings.Split(s[i+1:], ".") {
			if !identOK(id) || (allDigits(id) && len(id) > 1 && id[0] == '0') {
				return v, bad
			}
			v.pre = append(v.pre, id)
		}
	}
	parts := strings.Split(core, ".")
	if len(parts) != 3 {
		return v, bad
	}
	for i, p := range parts {
		if !allDigits(p) || (len(p) > 1 && p[0] == '0') {
			return v, bad
		}
		n, err := strconv.Atoi(p)
		if err != nil {
			return v, bad
		}
		v.nums[i] = n
	}
	return v, nil
}

func comparePre(a, b []string) int {
	switch {
	case len(a) == 0 && len(b) == 0:
		return 0
	case len(a) == 0:
		return 1
	case len(b) == 0:
		return -1
	}
	for i := 0; i < len(a) && i < len(b); i++ {
		na, ea := allDigits(a[i]), allDigits(b[i])
		switch {
		case na && ea:
			x, _ := strconv.Atoi(a[i])
			y, _ := strconv.Atoi(b[i])
			if x != y {
				if x < y {
					return -1
				}
				return 1
			}
		case na:
			return -1
		case ea:
			return 1
		default:
			if a[i] != b[i] {
				if a[i] < b[i] {
					return -1
				}
				return 1
			}
		}
	}
	if len(a) != len(b) {
		if len(a) < len(b) {
			return -1
		}
		return 1
	}
	return 0
}
