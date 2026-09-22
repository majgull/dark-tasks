#!/bin/bash
# hidden acceptance for obs-02-count; runs at the repo root in the staging VM
exec python3 "$(dirname "$0")/check.py"
