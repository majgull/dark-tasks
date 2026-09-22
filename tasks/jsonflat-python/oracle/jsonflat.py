"""jsonflat.py FILE: print every leaf of a JSON document as PATH=VALUE."""

import json
import sys


def leaves(value, path=""):
    if isinstance(value, dict):
        if not value:
            yield path, "{}"
        for k, v in value.items():
            yield from leaves(v, f"{path}.{k}" if path else k)
    elif isinstance(value, list):
        if not value:
            yield path, "[]"
        for i, v in enumerate(value):
            yield from leaves(v, f"{path}[{i}]")
    elif isinstance(value, str):
        yield path, value
    else:
        yield path, json.dumps(value)


def main(argv):
    if len(argv) != 2:
        print("usage: jsonflat.py FILE", file=sys.stderr)
        return 2
    name = argv[1]
    try:
        with open(name, encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, ValueError, UnicodeDecodeError):
        print(f"jsonflat: {name}: cannot read", file=sys.stderr)
        return 1
    if not isinstance(doc, (dict, list)):
        print(f"jsonflat: {name}: not an object or array", file=sys.stderr)
        return 1
    if not doc:
        return 0
    for path, text in sorted(leaves(doc), key=lambda pv: pv[0]):
        print(f"{path}={text}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
