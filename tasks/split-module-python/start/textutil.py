"""Small helpers used by app.py."""

import re


def slug(text):
    """Lowercase, words joined by single hyphens, nothing else."""
    return "-".join(w for w in re.split(r"[^a-z0-9]+", text.lower()) if w)


def title_words(text):
    """Every word capitalised, single spaces."""
    return " ".join(w.capitalize() for w in text.split())


def truncate(text, width):
    """At most width characters; a cut string ends with an ellipsis."""
    if len(text) <= width:
        return text
    return text[: max(width - 1, 0)] + "…"


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
