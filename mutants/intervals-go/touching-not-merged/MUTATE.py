import io
p = 'intervals.go'
old = '\t\tif cur[0] > last[1] {'
new = '\t\tif cur[0] >= last[1] {'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
