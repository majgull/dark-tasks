#!/bin/bash
# hidden acceptance for smoke-chain-a; runs at the repo root in the staging VM
fail=0
out=$(python3 hello.py 2>/dev/null); rc=$?
if [ "$rc" = 0 ] && [ "$out" = "hello, dark" ]; then echo "CHECK hello ok"; else echo "CHECK hello fail (rc=$rc out=$out)"; fail=1; fi
exit $fail
