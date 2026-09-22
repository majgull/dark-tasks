import io
p = 'observer/report.py'
old = 'lines += [f"- {d}: {per_day.get(d, 0)}" for d in days]'
new = 'lines += [f"- {d}: {n}" for d, n in by_day(inside)]'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
