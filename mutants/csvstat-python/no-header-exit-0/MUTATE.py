import io
p = 'csvstat.py'
old = '''        print(f"csvstat: {name}: no header", file=sys.stderr)
        return 1'''
new = '''        print(f"csvstat: {name}: no header", file=sys.stderr)
        return 0'''
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
