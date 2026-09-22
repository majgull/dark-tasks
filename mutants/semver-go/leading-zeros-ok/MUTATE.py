import io
p = 'semver.go'
old = '\t\tif !allDigits(p) || (len(p) > 1 && p[0] == \'0\') {'
new = '\t\tif !allDigits(p) {'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
