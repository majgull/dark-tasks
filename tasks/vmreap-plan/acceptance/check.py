"""vmreap-plan: hidden acceptance on real qm output shapes (cpu-host, 2026-09-03)."""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
ROOT = os.getcwd()
sys.path.insert(0, ROOT)
BAD = 0


def chk(name, ok, note=""):
    global BAD
    BAD += not ok
    print(f"CHECK {name} {'ok' if ok else 'fail'}" + ("" if ok or not note else f" ({str(note)[:200]})"))


def run(*args):
    r = subprocess.run([sys.executable, "vmreap.py", *args], cwd=ROOT, capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout, r.stderr


def fx(name):
    return os.path.join(FIX, name)


STATUS_DIR = fx("status")
PLAN = "qm stop 9500\nqm destroy 9500 --purge\nqm stop 9503\nqm destroy 9503 --purge\nqm destroy 9552 --purge\n"

pyfiles = sorted(f for f in os.listdir(ROOT) if f.endswith(".py"))
chk("files", pyfiles == ["test_vmreap.py", "vmreap.py"], pyfiles)
chk("test-count", sum(1 for l in open(os.path.join(ROOT, "test_vmreap.py")) if l.lstrip().startswith("def test")) >= 3 if os.path.exists(os.path.join(ROOT, "test_vmreap.py")) else False)
r = subprocess.run([sys.executable, "-m", "unittest", "-q", "test_vmreap"], cwd=ROOT, capture_output=True, text=True, timeout=300)
chk("visible-tests", r.returncode == 0, (r.stderr or r.stdout)[-300:])

rc, out, err = run("plan", "--list", fx("list.txt"), "--status-dir", STATUS_DIR)
chk("plan-default", (rc, out, err) == (1, PLAN, "vmreap: 4 factory VM(s), 3 to reap\n"), f"rc={rc} out={out!r} err={err!r}")
rc, out, err = run("plan", "--list", fx("list.txt"), "--status-dir", STATUS_DIR, "--max-age", "5001")
chk("plan-max-age-high", (rc, out, err) == (1, "qm destroy 9552 --purge\n", "vmreap: 4 factory VM(s), 1 to reap\n"), f"rc={rc} out={out!r} err={err!r}")
rc, out, err = run("plan", "--max-age", "100", "--status-dir", STATUS_DIR, "--list", fx("list.txt"))
chk("plan-max-age-low-any-order", (rc, out, err) == (1, "qm stop 9500\nqm destroy 9500 --purge\nqm stop 9503\nqm destroy 9503 --purge\nqm stop 9551\nqm destroy 9551 --purge\nqm destroy 9552 --purge\n",
                                                    "vmreap: 4 factory VM(s), 4 to reap\n"), f"rc={rc} out={out!r} err={err!r}")
rc, out, err = run("plan", "--list", fx("list-empty.txt"), "--status-dir", STATUS_DIR)
chk("plan-empty", (rc, out, err) == (0, "", "vmreap: 0 factory VM(s), 0 to reap\n"), f"rc={rc} out={out!r} err={err!r}")
ok = True
for name in ("list-bad-header.txt", "list-bad-row.txt", "list-bad-num.txt", "list-missing-status.txt", "list-does-not-exist.txt"):
    rc, out, err = run("plan", "--list", fx(name), "--status-dir", STATUS_DIR)
    if not (rc == 2 and out == "" and err.startswith("error:")):
        ok = False
        print(f"  {name}: rc={rc} out={out!r} err={err[:80]!r}")
chk("plan-errors", ok)
rc, out, err = run("plan", "--list", fx("list.txt"), "--status-dir", STATUS_DIR, "--max-age", "abc")
chk("plan-bad-max-age", rc == 2 and out == "" and err.startswith("error:"), f"rc={rc} err={err[:80]!r}")
ok = True
for args in ((), ("plan",), ("plan", "--list", fx("list.txt")), ("reap", "--list", fx("list.txt"), "--status-dir", STATUS_DIR),
             ("plan", "--list", fx("list.txt"), "--status-dir", STATUS_DIR, "--bogus", "1")):
    rc, out, err = run(*args)
    if not (rc == 2 and out == "" and "usage: vmreap.py plan --list FILE --status-dir DIR [--max-age SECONDS]" in err):
        ok = False
        print(f"  {args}: rc={rc} out={out!r} err={err[:80]!r}")
chk("usage", ok)

try:
    from vmreap import parse_list, parse_status, plan
    real = open(fx("list.txt")).read()
    vms = parse_list(real)
    chk("api-parse-list", [v["vmid"] for v in vms] == [100, 101, 102, 120, 121, 122, 9000, 9001, 9503, 9500, 9551, 9552]
        and vms[1] == {"vmid": 101, "name": "llm-server", "status": "running", "mem_mb": 16000, "bootdisk_gb": 180.0, "pid": 1578}
        and vms[6]["name"] == "factory-agent-template", vms[:2])
    chk("api-parse-list-blank-lines", parse_list("\n" + real + "\n\n") == vms)
    bad = 0
    for text in ("", "NAME VMID\n", real + "      9553 dark-s3 running 4096 16.00\n", real.replace("1578", "15x8"), real.replace("16000", "16k")):
        try:
            parse_list(text)
            bad += 1
        except ValueError:
            pass
        except Exception as e:  # noqa: BLE001
            bad += 1
            print(f"  raised {type(e).__name__}")
    chk("api-parse-list-rejects", bad == 0, bad)
    st = parse_status(open(os.path.join(STATUS_DIR, "101.txt")).read())
    chk("api-parse-status-real", st.get("uptime") == "3585" and st.get("status") == "running" and st.get("name") == "llm-server" and st.get("vmid") == "101", st.get("uptime"))
    chk("api-parse-status-loose", parse_status("no colon here\nk: v: w\n  rd_bytes: 5\nk: z\n") == {"k": "z", "rd_bytes": "5"})
    sts = {9500: {"uptime": "5000"}, 9503: {"uptime": "3600"}, 9551: {"uptime": "120"}}
    chk("api-plan", plan(vms, sts, 3600) == PLAN.splitlines() and plan(vms, sts, 3601) == ["qm stop 9500", "qm destroy 9500 --purge", "qm destroy 9552 --purge"])
    chk("api-plan-ignores-others", plan([{"vmid": 1, "name": "darkroom", "status": "stopped", "mem_mb": 1, "bootdisk_gb": 1.0, "pid": 0},
                                         {"vmid": 2, "name": "dark-x", "status": "stopped", "mem_mb": 1, "bootdisk_gb": 1.0, "pid": 0},
                                         {"vmid": 3, "name": "dark-y1", "status": "running", "mem_mb": 1, "bootdisk_gb": 1.0, "pid": 0},
                                         {"vmid": 4, "name": "dark-s7", "status": "paused", "mem_mb": 1, "bootdisk_gb": 1.0, "pid": 0}], {}, 0) == ["qm destroy 4 --purge"])
    bad = 0
    for sts2 in ({}, {9500: {}, 9503: sts[9503], 9551: sts[9551]}, {9500: {"uptime": "-1"}, 9503: sts[9503], 9551: sts[9551]}):
        try:
            plan(vms, sts2, 3600)
            bad += 1
        except ValueError:
            pass
        except Exception as e:  # noqa: BLE001
            bad += 1
            print(f"  raised {type(e).__name__}")
    chk("api-plan-never-guesses", bad == 0, bad)
except Exception as e:  # noqa: BLE001
    chk("api-import", False, repr(e))

sys.exit(1 if BAD else 0)
