import io
p = 'csvstat.py'
old = '''        print("usage: csvstat.py FILE", file=sys.stderr)
        return 2'''
new = '''        print("usage: csvstat.py FILE", file=sys.stderr)
        return 1'''
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
