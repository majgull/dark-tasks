#!/bin/bash
# hidden acceptance for csvstat-python; runs at the repo root in the staging VM
A=.acceptance
fail=0
chk() { local name=$1 want=$2 got=$3; if [ "$got" = "$want" ]; then echo "CHECK $name ok"; else echo "CHECK $name fail: want [$want] got [$got]"; fail=1; fi; }
printf 'name,age,city\nann,34,Bonn\nbob,,K\xc3\xb6ln\ncid,27.5,Bonn\n' > $A/ex.csv
chk example "$(printf 'name: count=3 distinct=3\nage: count=2 min=27.5 max=34 mean=30.75\ncity: count=3 distinct=2')" "$(python3 csvstat.py $A/ex.csv 2>/dev/null)"
printf 'a,b,c\n-1,x,\n2e1,y,\n003,x,\n' > $A/num.csv
chk numeric-forms "$(printf 'a: count=3 min=-1 max=2e1 mean=7.33\nb: count=3 distinct=2\nc: count=0 distinct=0')" "$(python3 csvstat.py $A/num.csv 2>/dev/null)"
printf 'v\n1.0\n1\n1.00\n' > $A/ties.csv
chk ties-first-text "v: count=3 min=1.0 max=1.0 mean=1.00" "$(python3 csvstat.py $A/ties.csv 2>/dev/null)"
printf 'p,q\n1\n2,z,extra\n' > $A/short.csv
chk short-and-long-rows "$(printf 'p: count=2 min=1 max=2 mean=1.50\nq: count=1 distinct=1')" "$(python3 csvstat.py $A/short.csv 2>/dev/null)"
printf 'n\n5\nfive\n' > $A/mixed.csv
chk mixed-is-text "n: count=2 distinct=2" "$(python3 csvstat.py $A/mixed.csv 2>/dev/null)"
printf 'q\n"a, b"\n"a, b"\n" "\n' > $A/quoted.csv
chk quoted-cells "q: count=3 distinct=2" "$(python3 csvstat.py $A/quoted.csv 2>/dev/null)"
printf 'h1,h2\n' > $A/header-only.csv
chk header-only "$(printf 'h1: count=0 distinct=0\nh2: count=0 distinct=0')" "$(python3 csvstat.py $A/header-only.csv 2>/dev/null)"
printf 'x\n0.005\n0.004\n' > $A/round.csv
chk mean-two-decimals "x: count=2 min=0.004 max=0.005 mean=0.00" "$(python3 csvstat.py $A/round.csv 2>/dev/null)"
: > $A/empty.csv
out=$(python3 csvstat.py $A/empty.csv 2>$A/err); rc=$?
chk empty-exit "1" "$rc"; chk empty-stdout "" "$out"; chk empty-stderr "csvstat: $A/empty.csv: no header" "$(cat $A/err)"
out=$(python3 csvstat.py $A/nope.csv 2>$A/err); rc=$?
chk missing-exit "1" "$rc"; chk missing-stderr "csvstat: $A/nope.csv: cannot read" "$(cat $A/err)"
python3 csvstat.py >/dev/null 2>$A/err; chk usage-exit "2" "$?"; chk usage-stderr "usage: csvstat.py FILE" "$(cat $A/err)"
python3 csvstat.py $A/ex.csv >/dev/null 2>&1; chk ok-exit "0" "$?"
if [ -f test_csvstat.py ] && python3 -m unittest -q test_csvstat >/dev/null 2>&1; then echo "CHECK own-test ok"; else echo "CHECK own-test fail"; fail=1; fi
exit $fail
