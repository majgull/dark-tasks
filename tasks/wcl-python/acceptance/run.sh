#!/bin/bash
# hidden acceptance for wcl-python; runs at the repo root in the staging VM
A=.acceptance
fail=0
chk() { local name=$1 want=$2 got=$3; if [ "$got" = "$want" ]; then echo "CHECK $name ok"; else echo "CHECK $name fail: want [$want] got [$got]"; fail=1; fi; }
printf 'hello world\nsecond line\n' > $A/a.txt
printf 'one' > $A/b.txt
: > $A/empty.txt
printf 'h\xc3\xa9llo w\xc3\xb6rld\n' > $A/u.txt
chk default "2 4 24 $A/a.txt" "$(python3 wcl.py $A/a.txt 2>/dev/null)"
chk lines "2 $A/a.txt" "$(python3 wcl.py -l $A/a.txt 2>/dev/null)"
chk words-bytes-order "4 24 $A/a.txt" "$(python3 wcl.py -c -w $A/a.txt 2>/dev/null)"
chk flag-after-file "4 $A/a.txt" "$(python3 wcl.py $A/a.txt -w 2>/dev/null)"
chk no-final-newline "0 1 3 $A/b.txt" "$(python3 wcl.py $A/b.txt 2>/dev/null)"
chk empty "0 0 0 $A/empty.txt" "$(python3 wcl.py $A/empty.txt 2>/dev/null)"
chk utf8-bytes "1 2 14 $A/u.txt" "$(python3 wcl.py $A/u.txt 2>/dev/null)"
chk total "$(printf '2 4 24 %s\n0 1 3 %s\n2 5 27 total' $A/a.txt $A/b.txt)" "$(python3 wcl.py $A/a.txt $A/b.txt 2>/dev/null)"
chk total-lines-only "$(printf '2 %s\n0 %s\n2 total' $A/a.txt $A/b.txt)" "$(python3 wcl.py -l $A/a.txt $A/b.txt 2>/dev/null)"
out=$(python3 wcl.py $A/a.txt $A/nope.txt 2>$A/err); rc=$?
chk missing-exit "1" "$rc"
chk missing-stdout "$(printf '2 4 24 %s\n2 4 24 total' $A/a.txt)" "$out"
chk missing-stderr "wcl: $A/nope.txt: cannot read" "$(cat $A/err)"
python3 wcl.py >/dev/null 2>&1; chk usage-exit "2" "$?"
python3 wcl.py $A/a.txt >/dev/null 2>&1; chk ok-exit "0" "$?"
if [ -f test_wcl.py ] && python3 -m unittest -q test_wcl >/dev/null 2>&1; then echo "CHECK own-test ok"; else echo "CHECK own-test fail"; fail=1; fi
exit $fail
