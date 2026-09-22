"""app: turn 'key = value' lines from stdin into slug=value lines."""
import sys

import utils


def render(lines):
    out = []
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, value = utils.parse_kv(line)
        out.append(f"{utils.slugify(key)}={value}")
    return out


def main():
    for row in render(sys.stdin.read().splitlines()):
        print(row)


if __name__ == "__main__":
    main()
