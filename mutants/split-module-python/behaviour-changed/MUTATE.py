import io
p = 'numutil.py'
old = '    return round(100.0 * part / whole, 1) if whole else 0.0'
new = '    return round(100.0 * part / whole, 2) if whole else 0.0'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
