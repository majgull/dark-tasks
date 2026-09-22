import io
p = 'observer/counts.py'
old = 'return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))'
new = 'return sorted(counts.items(), key=lambda kv: (kv[1], kv[0]))'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
