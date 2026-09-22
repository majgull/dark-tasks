import io
p = 'intervals.go'
old = '''\ts := make([][2]int, len(iv))
\tcopy(s, iv)
\tsort.Slice(s'''
new = '''\ts := iv
\tsort.Slice(s'''
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
