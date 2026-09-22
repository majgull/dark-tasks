package main

import "time"

// Bucket is a token bucket: capacity tokens at most, perSecond added
// continuously, one taken per allowed call.
type Bucket struct {
	capacity  float64
	perSecond float64
	now       func() time.Time
	tokens    float64
	last      time.Time
}

// NewBucket returns a full bucket whose clock is now.
func NewBucket(capacity int, perSecond float64, now func() time.Time) *Bucket {
	if capacity < 1 || perSecond <= 0 || now == nil {
		panic("bucket: bad arguments")
	}
	t := now()
	return &Bucket{capacity: float64(capacity), perSecond: perSecond, now: now, tokens: float64(capacity), last: t}
}

func (b *Bucket) refill() {
	t := b.now()
	if elapsed := t.Sub(b.last).Seconds(); elapsed > 0 {
		b.tokens += elapsed * b.perSecond
		if b.tokens > b.capacity {
			b.tokens = b.capacity
		}
	}
	b.last = t
}

// Allow takes one token if one is available.
func (b *Bucket) Allow() bool {
	b.refill()
	if b.tokens >= 1 {
		b.tokens--
		return true
	}
	return false
}

// Tokens is the current token count after refilling.
func (b *Bucket) Tokens() float64 {
	b.refill()
	return b.tokens
}
