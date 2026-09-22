"""parse_duration(text) -> int: total seconds of a duration string.

A duration is one or more parts written back to back with no spaces,
each part a non-negative integer in ASCII digits 0-9 followed by one unit
letter:
h (hours, 3600 s), m (minutes, 60 s) or s (seconds). Parts must appear
in the order h, m, s and each unit at most once, so "1h30m", "45s",
"2h", "1h0m5s" and "0s" are valid; "30m1h", "1h1h", "", "1.5h", "1H",
" 1h", "1h ", "h", "1" and "1h30" are not. An invalid string raises
ValueError. Leading zeros in a number are fine ("05s" is 5).
"""

import re

_WHOLE = re.compile(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", re.ASCII)


def parse_duration(text):
    if not isinstance(text, str) or not text:
        raise ValueError(f"not a duration: {text!r}")
    m = _WHOLE.fullmatch(text)
    if not m:
        raise ValueError(f"not a duration: {text!r}")
    h, mi, s = (int(x) if x is not None else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s
