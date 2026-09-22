#!/bin/bash
# hidden acceptance for obs-06-typehints; runs at the repo root in the staging VM
exec python3 "$(dirname "$0")/check.py"
