import io
p = 'internal/strutil/strutil.go'
old = '\tr := []rune(s)'
new = '\t// reverse the runes, not the bytes\n\trunes := []rune(s)\n\tr := runes'
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
