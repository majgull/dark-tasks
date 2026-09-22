import io
p = 'observer/counts.py'
old = 'import datetime as dt'
new = 'import datetime as dt\nimport typing  # noqa: F401'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
