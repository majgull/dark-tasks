# the three number helpers are copied into numutil.py but left in textutil.py too
import io
src = io.open('numutil.py', encoding='utf-8').read()
body = src.split('"""Number helpers used by app.py."""', 1)[1]
t = io.open('textutil.py', encoding='utf-8').read()
io.open('textutil.py', 'w', encoding='utf-8').write(t.rstrip('\n') + '\n' + body)
