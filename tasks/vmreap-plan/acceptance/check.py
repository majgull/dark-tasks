"""vmreap-plan: hidden acceptance on real qm output shapes."""

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
PLAN = "qm stop 110\nqm destroy 110 --purge\nqm stop 111\nqm destroy 111 --purge\nqm destroy 113 --purge\n"

pyfiles = sorted(f for f in os.listdir(ROOT) if f.endswith(".py"))
chk("files", pyfiles == ["test_vmreap.py", "vmreap.py"], pyfiles)
chk("test-count", sum(1 for l in open(os.path.join(ROOT, "test_vmreap.py")) if l.lstrip().startswith("def test")) >= 3 if os.path.exists(os.path.join(ROOT, "test_vmreap.py")) else False)
r = subprocess.run([sys.executable, "-m", "unittest", "-q", "test_vmreap"], cwd=ROOT, capture_output=True, text=True, timeout=300)
chk("visible-tests", r.returncode == 0, (r.stderr or r.stdout)[-300:])

rc, out, err = run("plan", "--list", fx("list.txt"), "--status-dir", STATUS_DIR)
chk("plan-default", (rc, out, err) == (1, PLAN, "vmreap: 4 factory VM(s), 3 to reap\n"), f"rc={rc} out={out!r} err={err!r}")
rc, out, err = run("plan", "--list", fx("list.txt"), "--status-dir", STATUS_DIR, "--max-age", "5001")
chk("plan-max-age-high", (rc, out, err) == (1, "qm destroy 113 --purge\n", "vmreap: 4 factory VM(s), 1 to reap\n"), f"rc={rc} out={out!r} err={err!r}")
rc, out, err = run("plan", "--max-age", "100", "--status-dir", STATUS_DIR, "--list", fx("list.txt"))
chk("plan-max-age-low-any-order", (rc, out, err) == (1, "qm stop 110\nqm destroy 110 --purge\nqm stop 111\nqm destroy 111 --purge\nqm stop 112\nqm destroy 112 --purge\nqm destroy 113 --purge\n",
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
    chk("api-parse-list", [v["vmid"] for v in vms] == [100, 101, 102, 120, 121, 122, 103, 104, 111, 110, 112, 113]
        and vms[1] == {"vmid": 101, "name": "model-server", "status": "running", "mem_mb": 16000, "bootdisk_gb": 180.0, "pid": 4242}
        and vms[6]["name"] == "agent-1", vms[:2])
    chk("api-parse-list-blank-lines", parse_list("\n" + real + "\n\n") == vms)
    bad = 0
    for text in ("", "NAME VMID\n", real + "      115 dark-s3 running 4096 16.00\n", real.replace("4242", "42x2"), real.replace("16000", "16k")):
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
    chk("api-parse-status-real", st.get("uptime") == "3585" and st.get("status") == "running" and st.get("name") == "model-server" and st.get("vmid") == "101", st.get("uptime"))
    chk("api-parse-status-loose", parse_status("no colon here\nk: v: w\n  rd_bytes: 5\nk: z\n") == {"k": "z", "rd_bytes": "5"})
    sts = {110: {"uptime": "5000"}, 111: {"uptime": "3600"}, 112: {"uptime": "120"}}
    chk("api-plan", plan(vms, sts, 3600) == PLAN.splitlines() and plan(vms, sts, 3601) == ["qm stop 110", "qm destroy 110 --purge", "qm destroy 113 --purge"])
    chk("api-plan-ignores-others", plan([{"vmid": 1, "name": "darkroom", "status": "stopped", "mem_mb": 1, "bootdisk_gb": 1.0, "pid": 0},
                                         {"vmid": 2, "name": "dark-x", "status": "stopped", "mem_mb": 1, "bootdisk_gb": 1.0, "pid": 0},
                                         {"vmid": 3, "name": "dark-y1", "status": "running", "mem_mb": 1, "bootdisk_gb": 1.0, "pid": 0},
                                         {"vmid": 4, "name": "dark-s7", "status": "paused", "mem_mb": 1, "bootdisk_gb": 1.0, "pid": 0}], {}, 0) == ["qm destroy 4 --purge"])
    bad = 0
    for sts2 in ({}, {110: {}, 111: sts[111], 112: sts[112]}, {110: {"uptime": "-1"}, 111: sts[111], 112: sts[112]}):
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
