"""Small helpers used by app.py."""
import re


def slugify(text):
    text = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return text.strip("-")


def parse_kv(line):
    key, sep, value = line.partition("=")
    if not sep:
        raise ValueError(f"no '=' in {line!r}")
    return key.strip(), value.strip()
