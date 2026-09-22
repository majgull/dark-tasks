#!/bin/bash
# hidden acceptance for obs-01-parse; runs at the repo root in the staging VM
exec python3 "$(dirname "$0")/check.py"
