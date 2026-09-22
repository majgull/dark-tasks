import io
p='observer/journal.py'
s=io.open(p,encoding='utf-8').read()
assert 'REQUIRED = ' in s
io.open(p,'w',encoding='utf-8').write(s.replace('REQUIRED = (', 'REQUIRED = (  # reordered\n    '))
