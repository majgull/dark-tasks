import io
p = 'counts.py'
old = 'return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))'
new = 'return sorted(sorted(counts.items(), key=lambda kv: kv[0], reverse=True), key=lambda kv: -kv[1])'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
