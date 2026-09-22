import io
p = 'numutil.py'
old = '    return lo if x < lo else hi if x > hi else x'
new = '''    if x < lo:
        return lo
    if x > hi:
        return hi
    return x'''
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
