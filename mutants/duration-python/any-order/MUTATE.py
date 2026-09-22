import io
p = 'duration.py'
old = '''    m = _WHOLE.fullmatch(text)
    if not m:
        raise ValueError(f"not a duration: {text!r}")
    h, mi, s = (int(x) if x is not None else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s'''
new = '''    parts = re.findall(r"(\\d+)([hms])", text, re.ASCII)
    if not parts or "".join(n + u for n, u in parts) != text:
        raise ValueError(f"not a duration: {text!r}")
    mult = {"h": 3600, "m": 60, "s": 1}
    return sum(int(n) * mult[u] for n, u in parts)'''
s = io.open(p, encoding='utf-8').read()
assert s.count(old) == 1, (p, old)
io.open(p, 'w', encoding='utf-8').write(s.replace(old, new))
