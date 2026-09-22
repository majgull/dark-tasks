import io
p = 'semver.go'
old = '''\tcase len(a) == 0:
\t\treturn 1
\tcase len(b) == 0:
\t\treturn -1'''
new = '''\tcase len(a) == 0:
\t\treturn -1
\tcase len(b) == 0:
\t\treturn 1'''
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
