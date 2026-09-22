import io
p = 'journal.py'
old = 'line = raw[:-1] if raw.endswith("\\r") else raw'
new = 'line = raw'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
