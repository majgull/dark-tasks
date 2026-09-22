import io
p = 'observer/report.py'
old = 'MAX_ERRORS = 20'
new = 'MAX_ERRORS = 1000'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
