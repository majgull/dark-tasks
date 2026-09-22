#!/bin/bash
# hidden acceptance for smoke-chain-b; runs at the repo root in the staging VM
fail=0
out=$(python3 bye.py 2>/dev/null); rc=$?
if [ "$rc" = 0 ] && [ "$out" = "bye, dark" ]; then echo "CHECK bye ok"; else echo "CHECK bye fail (rc=$rc out=$out)"; fail=1; fi
out=$(python3 hello.py 2>/dev/null); rc=$?
if [ "$rc" = 0 ] && [ "$out" = "hello, dark" ]; then echo "CHECK hello still ok"; else echo "CHECK hello still fail (rc=$rc out=$out)"; fail=1; fi
exit $fail
