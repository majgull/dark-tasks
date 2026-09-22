"""Number helpers used by app.py."""


def clamp(x, lo, hi):
    """x limited to the closed range [lo, hi]."""
    return lo if x < lo else hi if x > hi else x


def mean(xs):
    """Arithmetic mean; 0.0 for an empty sequence."""
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def percent(part, whole):
    """part as a percentage of whole, rounded to one decimal; 0.0 when whole is 0."""
    return round(100.0 * part / whole, 1) if whole else 0.0
