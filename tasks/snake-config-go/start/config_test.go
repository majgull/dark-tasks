package main

import "testing"

func TestLoadSample(t *testing.T) {
	c, err := Load("config.json")
	if err != nil {
		t.Fatalf("Load: %v", err)
	}
	if c.ListenAddr != "127.0.0.1:8080" || c.MaxItems != 50 || c.LogLevel != "info" {
		t.Fatalf("unexpected config: %+v", c)
	}
}

func TestLoadMissing(t *testing.T) {
	if _, err := Load("does-not-exist.json"); err == nil {
		t.Fatal("expected an error for a missing file")
	}
}
