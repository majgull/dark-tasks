import io
p = 'observer/counts.py'
old = 'dt.datetime.fromtimestamp(ts_us // 1_000_000, dt.timezone.utc)'
new = 'dt.datetime.fromtimestamp(ts_us // 1_000_000)'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
