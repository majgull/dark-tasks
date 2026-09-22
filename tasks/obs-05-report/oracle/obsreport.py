"""obsreport.py: the weekly report on the command line.

    python3 obsreport.py FILE YYYY-Www
"""

import sys

from observer import journal, report

USAGE = "usage: obsreport.py FILE YYYY-Www"


def main(argv):
    if len(argv) != 3:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        report.week_days(argv[2])
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    try:
        records = journal.load(argv[1])
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    sys.stdout.write(report.weekly(records, argv[2]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
