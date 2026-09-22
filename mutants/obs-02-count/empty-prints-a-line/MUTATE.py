import io
p = 'obs.py'
old = 'if not records:\n        return 0'
new = 'if not records:\n        print()\n        return 0'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
