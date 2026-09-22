# the result is reversed at the end: still disjoint, no longer sorted by start
import io
p = 'intervals.go'
old = '''\treturn out
}'''
new = '''\tfor i, j := 0, len(out)-1; i < j; i, j = i+1, j-1 {
\t\tout[i], out[j] = out[j], out[i]
\t}
\treturn out
}'''
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
