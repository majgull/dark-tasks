"""obs.py: the observer's command line.

    python3 obs.py count FILE
"""

import sys

import counts
import journal

USAGE = "usage: obs.py count FILE"


def main(argv):
    if len(argv) != 3 or argv[1] != "count":
        print(USAGE, file=sys.stderr)
        return 2
    try:
        records = journal.load(argv[2])
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    if not records:
        return 0
    for unit, n in counts.by_unit(records):
        print(f"{n}\t{unit}")
    print()
    for day, n in counts.by_day(records):
        print(f"{n}\t{day}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
