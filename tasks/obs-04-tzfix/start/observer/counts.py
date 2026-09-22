"""counts.py: how many records per unit and per UTC day."""

import datetime as dt

NO_UNIT = "-"


def day_of(ts_us):
    """The UTC calendar day (YYYY-MM-DD) of a journal timestamp in microseconds."""
    return dt.datetime.fromtimestamp(ts_us // 1_000_000).strftime("%Y-%m-%d")


def by_unit(records):
    """[(unit, count)] with a record lacking _SYSTEMD_UNIT counted under "-",
    most frequent first, ties by unit name ascending."""
    counts = {}
    for r in records:
        u = r.get("_SYSTEMD_UNIT", NO_UNIT)
        counts[u] = counts.get(u, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def by_day(records):
    """[(YYYY-MM-DD, count)] per UTC day of __REALTIME_TIMESTAMP, days ascending."""
    counts = {}
    for r in records:
        d = day_of(r["__REALTIME_TIMESTAMP"])
        counts[d] = counts.get(d, 0) + 1
    return sorted(counts.items())
