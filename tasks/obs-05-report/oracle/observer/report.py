"""report.py: the weekly markdown report."""

import datetime as dt
import re

from observer.counts import NO_UNIT, by_day, by_unit, day_of

_WEEK = re.compile(r"([0-9]{4})-W([0-9]{2})")
MAX_ERRORS = 20


def week_days(week):
    """The seven UTC days (YYYY-MM-DD, Monday first) of an ISO week given
    as YYYY-Www. ValueError for anything else."""
    m = _WEEK.fullmatch(week)
    if not m:
        raise ValueError(f"not an ISO week (YYYY-Www): {week!r}")
    year, num = int(m.group(1)), int(m.group(2))
    try:
        monday = dt.date.fromisocalendar(year, num, 1)
    except ValueError:
        raise ValueError(f"no such week: {week!r}") from None
    return [(monday + dt.timedelta(days=i)).isoformat() for i in range(7)]


def _stamp(ts_us):
    return dt.datetime.fromtimestamp(ts_us // 1_000_000, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _is_error(r):
    p = r.get("PRIORITY", "")
    return p.isdigit() and int(p) <= 3


def weekly(records, week):
    """The markdown report for the records whose UTC day falls in `week`."""
    days = week_days(week)
    inside = [r for r in records if day_of(r["__REALTIME_TIMESTAMP"]) in set(days)]
    lines = [f"# Week {week}", "", "## Units", "", "| unit | count |", "|---|---|"]
    lines += [f"| {u} | {n} |" for u, n in by_unit(inside)]
    lines += ["", "## Days", ""]
    per_day = dict(by_day(inside))
    lines += [f"- {d}: {per_day.get(d, 0)}" for d in days]
    lines += ["", "## Errors", ""]
    errors = sorted((r for r in inside if _is_error(r)),
                    key=lambda r: (r["__REALTIME_TIMESTAMP"], r.get("_SYSTEMD_UNIT", NO_UNIT), r["MESSAGE"]))
    if not errors:
        lines.append("- none")
    for r in errors[:MAX_ERRORS]:
        lines.append(f"- {_stamp(r['__REALTIME_TIMESTAMP'])} {r.get('_SYSTEMD_UNIT', NO_UNIT)}: {r['MESSAGE']}")
    if len(errors) > MAX_ERRORS:
        lines.append(f"- and {len(errors) - MAX_ERRORS} more")
    return "\n".join(lines) + "\n"
