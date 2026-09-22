"""journal.py: parse the text form of the systemd journal export format.

A record is a run of KEY=VALUE lines ended by an empty line (or by the
end of the text). Keys match [A-Z0-9_]+; the first "=" splits key and
value; a "\r" right before the newline is dropped. Every record carries
__REALTIME_TIMESTAMP (microseconds since the epoch, decimal digits) and
MESSAGE. Every other field is kept as the string it was; a repeated key
keeps its last value.
"""

import re

_KEY = re.compile(r"^[A-Z0-9_]+$")
REQUIRED = ("__REALTIME_TIMESTAMP", "MESSAGE")


def parse(text: str) -> list[dict[str, str | int]]:
    """Records of `text`, in order, as dicts of field -> str, with
    __REALTIME_TIMESTAMP as an int. ValueError on a line that is not
    KEY=VALUE, a record missing a required field, or a timestamp that is
    not decimal digits."""
    records = []
    current = {}
    n = 0
    for n, raw in enumerate(text.split("\n"), 1):
        line = raw[:-1] if raw.endswith("\r") else raw
        if line == "":
            if current:
                records.append(_finish(current, n))
                current = {}
            continue
        key, sep, value = line.partition("=")
        if not sep or not _KEY.match(key):
            raise ValueError(f"line {n}: not a KEY=VALUE line: {line!r}")
        current[key] = value
    if current:
        records.append(_finish(current, n))
    return records


def _finish(rec: dict[str, str | int], n: int) -> dict[str, str | int]:
    for k in REQUIRED:
        if k not in rec:
            raise ValueError(f"record ending at line {n}: missing {k}")
    ts = rec["__REALTIME_TIMESTAMP"]
    if not ts.isdigit():
        raise ValueError(f"record ending at line {n}: __REALTIME_TIMESTAMP is not decimal digits: {ts!r}")
    rec["__REALTIME_TIMESTAMP"] = int(ts)
    return rec


def load(path: str) -> list[dict[str, str | int]]:
    """parse() of the file at `path` (UTF-8)."""
    with open(path, encoding="utf-8") as f:
        return parse(f.read())
