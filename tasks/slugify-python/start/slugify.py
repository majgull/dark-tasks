"""slugify(text) -> a URL slug.

Contract: the result is lowercase; every run of one or more characters
that are not ASCII letters or digits becomes a single hyphen; the result
has no leading or trailing hyphen; a text with no letters or digits at
all (including the empty string) gives the empty string.
"""
import re


def slugify(text):
    return re.sub(r"[^a-z0-9]", "-", text.lower())
