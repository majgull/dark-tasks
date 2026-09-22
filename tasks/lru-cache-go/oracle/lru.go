package main

import "container/list"

type entry struct {
	key   string
	value int
}

// LRU is a least-recently-used cache of string keys and int values.
type LRU struct {
	capacity int
	order    *list.List // front = most recently used
	items    map[string]*list.Element
}

// NewLRU returns an empty cache holding at most capacity entries.
func NewLRU(capacity int) *LRU {
	if capacity < 1 {
		panic("lru: capacity must be at least 1")
	}
	return &LRU{capacity: capacity, order: list.New(), items: map[string]*list.Element{}}
}

// Get returns the value for key and marks it most recently used.
func (c *LRU) Get(key string) (int, bool) {
	el, ok := c.items[key]
	if !ok {
		return 0, false
	}
	c.order.MoveToFront(el)
	return el.Value.(*entry).value, true
}

// Put stores value under key, evicting the least recently used entry
// when a new key would exceed the capacity.
func (c *LRU) Put(key string, value int) {
	if el, ok := c.items[key]; ok {
		el.Value.(*entry).value = value
		c.order.MoveToFront(el)
		return
	}
	if c.order.Len() >= c.capacity {
		last := c.order.Back()
		c.order.Remove(last)
		delete(c.items, last.Value.(*entry).key)
	}
	c.items[key] = c.order.PushFront(&entry{key: key, value: value})
}

// Len is the number of entries held.
func (c *LRU) Len() int { return c.order.Len() }

// Keys lists the keys from most to least recently used.
func (c *LRU) Keys() []string {
	keys := make([]string, 0, c.order.Len())
	for el := c.order.Front(); el != nil; el = el.Next() {
		keys = append(keys, el.Value.(*entry).key)
	}
	return keys
}
