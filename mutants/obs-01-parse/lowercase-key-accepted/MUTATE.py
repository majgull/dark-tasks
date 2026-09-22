import io
p = 'journal.py'
old = 'r"^[A-Z0-9_]+$"'
new = 'r"^[A-Za-z0-9_]+$"'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
