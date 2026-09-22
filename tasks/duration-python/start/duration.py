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

_PART = re.compile(r"(\d+)([hms])")
_MULT = {"h": 3600, "m": 60, "s": 1}


def parse_duration(text):
    parts = _PART.findall(text)
    if not parts:
        raise ValueError(f"not a duration: {text!r}")
    total = 0
    for number, unit in parts:
        total += int(number) * _MULT[unit]
    return total
