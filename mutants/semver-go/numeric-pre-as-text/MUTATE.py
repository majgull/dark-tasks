import io
p = 'semver.go'
old = '''\t\tcase na && ea:
\t\t\tx, _ := strconv.Atoi(a[i])
\t\t\ty, _ := strconv.Atoi(b[i])
\t\t\tif x != y {
\t\t\t\tif x < y {
\t\t\t\t\treturn -1
\t\t\t\t}
\t\t\t\treturn 1
\t\t\t}'''
new = '''\t\tcase na && ea:
\t\t\tif a[i] != b[i] {
\t\t\t\tif a[i] < b[i] {
\t\t\t\t\treturn -1
\t\t\t\t}
\t\t\t\treturn 1
\t\t\t}'''
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
