import io
p = 'journal.py'
old = 'rec["__REALTIME_TIMESTAMP"] = int(ts)'
new = 'pass'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
