#!/usr/bin/env python3
"""wcl: count lines, words and bytes of files (reference solution)."""
import sys

FLAGS = ("-l", "-w", "-c")


def counts(data):
    return data.count(b"\n"), len(data.split()), len(data)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    flags = {a for a in argv if a in FLAGS}
    files = [a for a in argv if a not in FLAGS]
    if not files:
        print("usage: wcl.py [-l] [-w] [-c] FILE...", file=sys.stderr)
        return 2
    sel = [i for i, f in enumerate(FLAGS) if not flags or f in flags]
    total = [0, 0, 0]
    rc = 0
    for name in files:
        try:
            with open(name, "rb") as f:
                data = f.read()
        except OSError:
            print(f"wcl: {name}: cannot read", file=sys.stderr)
            rc = 1
            continue
        c = counts(data)
        for i in range(3):
            total[i] += c[i]
        print(" ".join(str(c[i]) for i in sel) + " " + name)
    if len(files) > 1:
        print(" ".join(str(total[i]) for i in sel) + " total")
    return rc


if __name__ == "__main__":
    sys.exit(main())
