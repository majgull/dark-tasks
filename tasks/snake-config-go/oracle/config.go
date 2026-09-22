package main

import (
	"encoding/json"
	"os"
)

// Config is the service configuration, loaded from a JSON file.
type Config struct {
	ListenAddr string `json:"listen_addr"`
	MaxItems   int    `json:"max_items"`
	LogLevel   string `json:"log_level"`
}

// Load reads a Config from the JSON file at path.
func Load(path string) (Config, error) {
	var c Config
	data, err := os.ReadFile(path)
	if err != nil {
		return c, err
	}
	err = json.Unmarshal(data, &c)
	return c, err
}
