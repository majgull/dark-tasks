# the build metadata is kept as one more pre-release identifier, so it orders
import io
p = 'semver.go'
old = '''\t\ts = s[:i]
\t}
\tcore := s'''
new = '''\t\tv.pre = append(v.pre, s[i+1:])
\t\ts = s[:i]
\t}
\tcore := s'''
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
