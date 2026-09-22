# a missing cell is treated as the text "0" rather than as empty, so it counts
import io
p = 'csvstat.py'
old = 'print(column_line(col, [r[i] if i < len(r) else "" for r in body]))'
new = 'print(column_line(col, [r[i] if i < len(r) else "0" for r in body]))'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
