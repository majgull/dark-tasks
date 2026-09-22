import io
p = 'observer/report.py'
old = 'm = _WEEK.fullmatch(week)'
new = 'm = _WEEK.match(week)'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
