"""csvstat.py FILE: one line of statistics per CSV column."""

import csv
import sys


def column_line(name, cells):
    cells = [c for c in cells if c != ""]
    if cells:
        try:
            values = [float(c) for c in cells]
        except ValueError:
            values = None
        if values is not None:
            lo = min(range(len(values)), key=lambda i: values[i])
            hi = max(range(len(values)), key=lambda i: values[i])
            mean = sum(values) / len(values)
            return f"{name}: count={len(cells)} min={cells[lo]} max={cells[hi]} mean={mean:.2f}"
    return f"{name}: count={len(cells)} distinct={len(set(cells))}"


def main(argv):
    if len(argv) != 2:
        print("usage: csvstat.py FILE", file=sys.stderr)
        return 2
    name = argv[1]
    try:
        with open(name, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
    except (OSError, UnicodeDecodeError, csv.Error):
        print(f"csvstat: {name}: cannot read", file=sys.stderr)
        return 1
    if not rows:
        print(f"csvstat: {name}: no header", file=sys.stderr)
        return 1
    header, body = rows[0], rows[1:]
    for i, col in enumerate(header):
        print(column_line(col, [r[i] if i < len(r) else "" for r in body]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
