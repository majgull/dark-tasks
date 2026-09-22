import io
p = 'roman.py'
old = '    if total < 1 or total > 3999 or to_roman(total) != s:'
new = '    if total < 1 or total > 3999:'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
