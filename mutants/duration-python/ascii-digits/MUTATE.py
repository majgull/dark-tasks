import io
p = 'duration.py'
old = 'r"(?:(\\d+)h)?(?:(\\d+)m)?(?:(\\d+)s)?", re.ASCII'
new = 'r"(?:(\\d+)h)?(?:(\\d+)m)?(?:(\\d+)s)?"'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
