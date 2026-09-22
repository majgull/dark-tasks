import io
p = 'journal.py'
old = 'REQUIRED = ("__REALTIME_TIMESTAMP", "MESSAGE")'
new = 'REQUIRED = ("__REALTIME_TIMESTAMP",)'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
