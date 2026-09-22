import io
p = 'journal.py'
old = 'line.partition("=")'
new = 'line.rpartition("=")'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
