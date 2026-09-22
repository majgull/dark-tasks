import io
p = 'csvstat.py'
old = '''            lo = min(range(len(values)), key=lambda i: values[i])
            hi = max(range(len(values)), key=lambda i: values[i])'''
new = '''            lo = max(i for i in range(len(values)) if values[i] == min(values))
            hi = max(i for i in range(len(values)) if values[i] == max(values))'''
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
