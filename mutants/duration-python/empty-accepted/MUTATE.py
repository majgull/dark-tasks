import io
p = 'duration.py'
old = '    if not isinstance(text, str) or not text:'
new = '    if not isinstance(text, str):'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
