#!/bin/bash
# hidden acceptance for obs-05-report; runs at the repo root in the staging VM
exec python3 "$(dirname "$0")/check.py"
