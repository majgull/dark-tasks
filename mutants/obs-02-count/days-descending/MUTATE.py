import io
p = 'counts.py'
old = 'return sorted(counts.items())'
new = 'return sorted(counts.items(), reverse=True)'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
