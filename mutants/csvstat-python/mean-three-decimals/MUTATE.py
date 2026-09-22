import io
p = 'csvstat.py'
old = 'mean={mean:.2f}'
new = 'mean={mean:.3f}'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
