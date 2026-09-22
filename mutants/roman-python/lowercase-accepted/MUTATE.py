import io
p = 'roman.py'
old = '''    for ch in s:
        if ch not in _DIGIT:'''
new = '''    s = s.upper()
    for ch in s:
        if ch not in _DIGIT:'''
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
