#!/bin/bash
# hidden acceptance for vmreap-plan; runs at the repo root in the staging VM
exec python3 "$(dirname "$0")/check.py"
