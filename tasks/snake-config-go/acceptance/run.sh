#!/bin/bash
# hidden acceptance for snake-config-go; runs at the repo root in the staging VM
export HOME="${HOME:-/root}" GOCACHE="${GOCACHE:-/root/.cache/go-build}" GOPATH="${GOPATH:-/root/go}"
export PATH="$PATH:/usr/local/go/bin"
fail=0
if ! grep -qE 'listenAddr|maxItems|logLevel' config.go config.json; then echo "CHECK no-camel ok"; else echo "CHECK no-camel fail"; fail=1; fi
if grep -q '"listen_addr"' config.json && grep -q '"max_items"' config.json && grep -q '"log_level"' config.json; then echo "CHECK sample-snake ok"; else echo "CHECK sample-snake fail"; fail=1; fi
if grep -q '127.0.0.1:8080' config.json && grep -q '50' config.json && grep -q '"info"' config.json; then echo "CHECK sample-values ok"; else echo "CHECK sample-values fail"; fail=1; fi
if grep -q 'ListenAddr string' config.go && grep -q 'MaxItems   int' config.go && grep -q 'LogLevel   string' config.go; then echo "CHECK fields-kept ok"; else echo "CHECK fields-kept fail"; fail=1; fi
n=$(ls *.go | wc -l)
if [ "$n" = 3 ]; then echo "CHECK no-extra-files ok"; else echo "CHECK no-extra-files fail ($n .go files)"; fail=1; fi
cat > zz_acceptance_test.go <<'EOF'
package main

import (
	"os"
	"path/filepath"
	"testing"
)

func acceptWrite(t *testing.T, body string) string {
	p := filepath.Join(t.TempDir(), "c.json")
	if err := os.WriteFile(p, []byte(body), 0o644); err != nil {
		t.Fatal(err)
	}
	return p
}

func TestAcceptSnakeKeys(t *testing.T) {
	c, err := Load(acceptWrite(t, `{"listen_addr": "0.0.0.0:9", "max_items": 7, "log_level": "debug"}`))
	if err != nil {
		t.Fatalf("Load: %v", err)
	}
	if c.ListenAddr != "0.0.0.0:9" || c.MaxItems != 7 || c.LogLevel != "debug" {
		t.Fatalf("snake_case keys not read: %+v", c)
	}
}

func TestAcceptCamelKeysIgnored(t *testing.T) {
	c, err := Load(acceptWrite(t, `{"listenAddr": "0.0.0.0:9", "maxItems": 7, "logLevel": "debug"}`))
	if err != nil {
		t.Fatalf("Load: %v", err)
	}
	if c.ListenAddr != "" || c.MaxItems != 0 || c.LogLevel != "" {
		t.Fatalf("camelCase keys still read: %+v", c)
	}
}
EOF
if go test ./... >/tmp/acc.log 2>&1; then echo "CHECK tests ok"; else echo "CHECK tests fail"; tail -20 /tmp/acc.log; fail=1; fi
rm -f zz_acceptance_test.go
exit $fail
