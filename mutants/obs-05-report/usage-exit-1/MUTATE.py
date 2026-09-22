import io
p = 'obsreport.py'
old = 'print(USAGE, file=sys.stderr)\n        return 2'
new = 'print(USAGE, file=sys.stderr)\n        return 1'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
