"""vmreap.py: a reap plan for leftover factory VMs (dark-x<N>, dark-s<N>) from
`qm list` and `qm status --verbose` output. Prints commands, never runs them.

    python3 vmreap.py plan --list FILE --status-dir DIR [--max-age SECONDS]
"""

import os
import re
import sys

USAGE = "usage: vmreap.py plan --list FILE --status-dir DIR [--max-age SECONDS]"
FACTORY = re.compile(r"^dark-[xs][0-9]+$")


def parse_list(text):
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines or lines[0].split()[0] != "VMID":
        raise ValueError("qm list output must start with a VMID header")
    out = []
    for line in lines[1:]:
        f = line.split()
        if len(f) != 6:
            raise ValueError(f"row does not have six fields: {line!r}")
        try:
            out.append({"vmid": int(f[0]), "name": f[1], "status": f[2], "mem_mb": int(f[3]),
                        "bootdisk_gb": float(f[4]), "pid": int(f[5])})
        except ValueError:
            raise ValueError(f"row has a non-numeric field: {line!r}") from None
    return out


def parse_status(text):
    out = {}
    for line in text.splitlines():
        key, sep, value = line.lstrip().partition(": ")
        if sep:
            out[key] = value
    return out


def plan(vms, statuses, max_age):
    out = []
    for vm in sorted((v for v in vms if FACTORY.match(v["name"])), key=lambda v: v["vmid"]):
        vmid = vm["vmid"]
        if vm["status"] == "running":
            st = statuses.get(vmid)
            if st is None:
                raise ValueError(f"no status for running factory VM {vmid}")
            up = st.get("uptime", "")
            if not up.isdigit():
                raise ValueError(f"no uptime for running factory VM {vmid}")
            if int(up) >= max_age:
                out += [f"qm stop {vmid}", f"qm destroy {vmid} --purge"]
        else:
            out.append(f"qm destroy {vmid} --purge")
    return out


def main(argv):
    args = argv[1:]
    if not args or args[0] != "plan":
        print(USAGE, file=sys.stderr)
        return 2
    opts = {"--max-age": "3600"}
    rest = args[1:]
    while rest:
        if rest[0] in ("--list", "--status-dir", "--max-age") and len(rest) >= 2:
            opts[rest[0]] = rest[1]
            rest = rest[2:]
        else:
            print(USAGE, file=sys.stderr)
            return 2
    if "--list" not in opts or "--status-dir" not in opts:
        print(USAGE, file=sys.stderr)
        return 2
    try:
        max_age = int(opts["--max-age"])
    except ValueError:
        print(f"error: --max-age is not an integer: {opts['--max-age']!r}", file=sys.stderr)
        return 2
    try:
        with open(opts["--list"], encoding="utf-8") as f:
            vms = parse_list(f.read())
        statuses = {}
        for vm in vms:
            if FACTORY.match(vm["name"]) and vm["status"] == "running":
                with open(os.path.join(opts["--status-dir"], f"{vm['vmid']}.txt"), encoding="utf-8") as f:
                    statuses[vm["vmid"]] = parse_status(f.read())
        lines = plan(vms, statuses, max_age)
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    for line in lines:
        print(line)
    factory = sum(1 for v in vms if FACTORY.match(v["name"]))
    reaped = len({l.split()[2] for l in lines})
    print(f"vmreap: {factory} factory VM(s), {reaped} to reap", file=sys.stderr)
    return 1 if reaped else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
