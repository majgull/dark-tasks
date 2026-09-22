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
