#!/bin/bash
# hidden acceptance for jsonflat-python; runs at the repo root in the staging VM
A=.acceptance
fail=0
chk() { local name=$1 want=$2 got=$3; if [ "$got" = "$want" ]; then echo "CHECK $name ok"; else echo "CHECK $name fail: want [$want] got [$got]"; fail=1; fi; }
printf '{"name": "dark", "tags": ["a", "b"], "meta": {"ok": true, "n": null, "empty": {}}}' > $A/ex.json
chk example "$(printf 'meta.empty={}\nmeta.n=null\nmeta.ok=true\nname=dark\ntags[0]=a\ntags[1]=b')" "$(python3 jsonflat.py $A/ex.json 2>/dev/null)"
printf '[[1, 2.5], {"b": [], "c": -3}, "s p a c e", false]' > $A/list.json
chk top-list "$(printf '[0][0]=1\n[0][1]=2.5\n[1].b=[]\n[1].c=-3\n[2]=s p a c e\n[3]=false')" "$(python3 jsonflat.py $A/list.json 2>/dev/null)"
printf '{"a.b": 1, "": 2, "z": {"": {"k": "v"}}}' > $A/keys.json
chk dotted-and-empty-keys "$(printf '=2\na.b=1\nz..k=v')" "$(python3 jsonflat.py $A/keys.json 2>/dev/null)"
printf '{"x": "quote\\"d", "y": "line"}' > $A/str.json
chk raw-strings "$(printf 'x=quote"d\ny=line')" "$(python3 jsonflat.py $A/str.json 2>/dev/null)"
printf '{"b": 1, "a": 2, "a0": 3, "B": 4}' > $A/sort.json
chk plain-sort "$(printf 'B=4\na=2\na0=3\nb=1')" "$(python3 jsonflat.py $A/sort.json 2>/dev/null)"
printf '{}' > $A/empty.json
chk empty-top "" "$(python3 jsonflat.py $A/empty.json 2>/dev/null)"
python3 jsonflat.py $A/empty.json >/dev/null 2>&1; chk empty-exit "0" "$?"
printf '42' > $A/scalar.json
out=$(python3 jsonflat.py $A/scalar.json 2>$A/err); rc=$?
chk scalar-exit "1" "$rc"; chk scalar-stdout "" "$out"; chk scalar-stderr "jsonflat: $A/scalar.json: not an object or array" "$(cat $A/err)"
printf '{"a": ' > $A/bad.json
out=$(python3 jsonflat.py $A/bad.json 2>$A/err); rc=$?
chk bad-exit "1" "$rc"; chk bad-stderr "jsonflat: $A/bad.json: cannot read" "$(cat $A/err)"
out=$(python3 jsonflat.py $A/nope.json 2>$A/err); chk missing-stderr "jsonflat: $A/nope.json: cannot read" "$(cat $A/err)"
python3 jsonflat.py >/dev/null 2>$A/err; chk usage-exit "2" "$?"; chk usage-stderr "usage: jsonflat.py FILE" "$(cat $A/err)"
python3 jsonflat.py $A/ex.json $A/ex.json >/dev/null 2>&1; chk two-args-exit "2" "$?"
if [ -f test_jsonflat.py ] && python3 -m unittest -q test_jsonflat >/dev/null 2>&1; then echo "CHECK own-test ok"; else echo "CHECK own-test fail"; fail=1; fi
exit $fail
