# the new package is created but the old one is left in place
import io, os
os.makedirs('internal/util', exist_ok=True)
for new, old in (('strutil.go', 'util.go'), ('strutil_test.go', 'util_test.go')):
    s = io.open('internal/strutil/' + new, encoding='utf-8').read()
    s = s.replace('package strutil', 'package util').replace('Package strutil', 'Package util')
    io.open('internal/util/' + old, 'w', encoding='utf-8').write(s)
