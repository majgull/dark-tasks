import io
p = 'observer/counts.py'
old = 'counts[u] = counts.get(u, 0) + 1'
new = 'counts[u] = 1 + counts.get(u, 0)'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
