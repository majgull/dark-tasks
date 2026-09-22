import io
p = 'duration.py'
old = '    return h * 3600 + mi * 60 + s'
new = '    return float(h * 3600 + mi * 60 + s)'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
