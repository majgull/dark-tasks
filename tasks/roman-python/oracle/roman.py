"""Roman numerals, standard form only.

to_roman(n): the standard (subtractive) numeral for an int 1..3999, using
the pairs IV, IX, XL, XC, CD and CM; e.g. 4 -> "IV", 1994 -> "MCMXCIV".
Any other value (0, negative, > 3999, non-int) raises ValueError.

from_roman(s): the int for a numeral written in that same standard form,
uppercase only. A string that is empty, has a character outside MDCLXVI,
or is not the standard form of its value (so "IIII", "VX", "iv") raises
ValueError. from_roman(to_roman(n)) == n for every n in 1..3999.
"""

_VALUES = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
           (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
_DIGIT = {"M": 1000, "D": 500, "C": 100, "L": 50, "X": 10, "V": 5, "I": 1}


def to_roman(n):
    if not isinstance(n, int) or isinstance(n, bool) or n < 1 or n > 3999:
        raise ValueError(f"out of range: {n!r}")
    out = []
    for value, glyph in _VALUES:
        while n >= value:
            out.append(glyph)
            n -= value
    return "".join(out)


def from_roman(s):
    if not s or not isinstance(s, str):
        raise ValueError("empty")
    for ch in s:
        if ch not in _DIGIT:
            raise ValueError(f"bad character: {ch!r}")
    total = 0
    for i, ch in enumerate(s):
        v = _DIGIT[ch]
        if i + 1 < len(s) and _DIGIT[s[i + 1]] > v:
            total -= v
        else:
            total += v
    if total < 1 or total > 3999 or to_roman(total) != s:
        raise ValueError(f"not standard form: {s!r}")
    return total
