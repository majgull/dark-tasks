import io
p = 'csvstat.py'
old = 'min={cells[lo]} max={cells[hi]}'
new = 'min={values[lo]:g} max={values[hi]:g}'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
