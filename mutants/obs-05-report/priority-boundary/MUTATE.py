import io
p = 'observer/report.py'
old = 'return p.isdigit() and int(p) <= 3'
new = 'return p.isdigit() and int(p) < 3'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
