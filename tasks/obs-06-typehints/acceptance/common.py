"""Shared helpers of the obs chain's hidden acceptance (one copy per step;
the steps are tarred separately). Runs at the repo root in the staging VM
with the acceptance set unpacked at .acceptance/."""

import hashlib
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
    return ok


def fixture(name):
    return os.path.join(FIX, name)


def read(name):
    with open(fixture(name), encoding="utf-8") as f:
        return f.read()


def run(args, env=None, timeout=60):
    e = dict(os.environ)
    e.update(env or {})
    r = subprocess.run([sys.executable, *args], cwd=ROOT, env=e, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def py_files(rel="."):
    d = os.path.join(ROOT, rel)
    return sorted(f for f in os.listdir(d) if f.endswith(".py")) if os.path.isdir(d) else None


def sha(path):
    with open(os.path.join(ROOT, path), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def base_changed(added=False):
    """Existing files modified or deleted (and, with added=True, files added)
    against the starting tree (origin main), or None when no origin is
    reachable."""
    r = subprocess.run(["git", "fetch", "-q", "origin", "main"], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        return None
    r = subprocess.run(["git", "diff", "--name-only", "--diff-filter=" + ("AMD" if added else "MD"), "FETCH_HEAD", "HEAD"],
                       cwd=ROOT, capture_output=True, text=True)
    return [p for p in r.stdout.split("\n") if p.strip()]


def check_base_untouched(name, allowed=(), added=False):
    """Nothing outside `allowed` was modified or deleted since the start
    (added=True: nor added; review S1)."""
    changed = base_changed(added=added)
    if changed is None:
        print(f"  {name}: no origin to compare against (local validation); not checked")
        return chk(name, True)
    extra = sorted(set(changed) - set(allowed))
    return chk(name, not extra, f"touched {extra}")


def root_entries():
    return sorted(e for e in os.listdir(ROOT) if not e.startswith(".") and e != "__pycache__")


def test_methods(path):
    try:
        with open(os.path.join(ROOT, path), encoding="utf-8") as f:
            return sum(1 for line in f if line.lstrip().startswith("def test"))
    except OSError:
        return 0


def base_file(path):
    """The starting tree's version of `path`, or None."""
    r = subprocess.run(["git", "show", f"FETCH_HEAD:{path}"], cwd=ROOT, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def tests_green(*names):
    rc, out, err = run(["-m", "unittest", "-q", *names], timeout=300)
    return rc == 0, (err or out)[-300:]


def finish():
    sys.exit(1 if BAD else 0)


# --- regression checks shared by the steps ---------------------------------
def check_parse(modname):
    """The step-01 contract, through `modname` (journal or observer.journal)."""
    try:
        mod = __import__(modname, fromlist=["parse", "load"])
        parse, load = mod.parse, mod.load
    except Exception as e:  # noqa: BLE001
        chk("parse-import", False, repr(e))
        return
    recs = parse(read("week.txt"))
    chk("parse-week", len(recs) == 24 and all(isinstance(r["__REALTIME_TIMESTAMP"], int) for r in recs), len(recs))
    chk("parse-order-and-fields", recs[0]["_SYSTEMD_UNIT"] == "systemd-journald.service" and recs[1]["PRIORITY"] == "3"
        and recs[10]["MESSAGE"] == "default sink=alsa_output.pci-0000_00_1f.3.analog-stereo volume=0.65"
        and recs[21]["MESSAGE"] == "config reloaded: interval=" and recs[-1]["__REALTIME_TIMESTAMP"] == 1788739199000000)
    e = parse(read("edge.txt"))
    chk("parse-edge", [r["MESSAGE"] for r in e] == ["first", "last wins", " leading space kept"]
        and e[1]["EMPTY"] == "" and e[1]["_SYSTEMD_UNIT"] == "b.service" and "\r" not in str(e[0]), e)
    chk("parse-empty", parse("") == [] and parse("\n\n\n") == [] and parse("__REALTIME_TIMESTAMP=1\nMESSAGE=a") == [{"__REALTIME_TIMESTAMP": 1, "MESSAGE": "a"}])
    bad = 0
    for name in ("bad-noeq.txt", "bad-lower.txt", "bad-ts.txt", "bad-nomsg.txt"):
        try:
            parse(read(name))
            bad += 1
            print(f"  accepted {name}")
        except ValueError:
            pass
        except Exception as e:  # noqa: BLE001
            bad += 1
            print(f"  {name}: raised {type(e).__name__}")
    for text in ("__REALTIME_TIMESTAMP=5\nMESSAGE=a\n_FOO=1\n=x\n", "__REALTIME_TIMESTAMP=-5\nMESSAGE=a\n", "MESSAGE=a\n__REALTIME_TIMESTAMP=\n",
                 "MESSAGE=no timestamp at all\n", "__REALTIME_TIMESTAMP=5\nMESSAGE=a\nFOO-BAR=1\n", "__REALTIME_TIMESTAMP=5\nMESSAGE=a\nfoo=1\n",
                 "__REALTIME_TIMESTAMP=5\nMESSAGE=a\nA B=1\n", "__REALTIME_TIMESTAMP=5\nMESSAGE=a\n\u00e9=1\n"):
        try:
            parse(text)
            bad += 1
            print(f"  accepted {text!r}")
        except ValueError:
            pass
        except Exception as e:  # noqa: BLE001
            bad += 1
            print(f"  {text!r}: raised {type(e).__name__}")
    chk("parse-rejects", bad == 0, f"{bad} miss(es)")
    lf = "__REALTIME_TIMESTAMP=5\nMESSAGE=a=b\n_SYSTEMD_UNIT=x.service\n\n__REALTIME_TIMESTAMP=6\nMESSAGE=c\n"
    chk("parse-crlf", parse(lf.replace("\n", "\r\n")) == parse(lf) == [
        {"__REALTIME_TIMESTAMP": 5, "MESSAGE": "a=b", "_SYSTEMD_UNIT": "x.service"},
        {"__REALTIME_TIMESTAMP": 6, "MESSAGE": "c"}], parse(lf.replace("\n", "\r\n")))
    r1 = parse("__REALTIME_TIMESTAMP=5\nMESSAGE=a\rb\n\n")
    r2 = parse("__REALTIME_TIMESTAMP=5\nMESSAGE=x  \nA_1=\t v\n")
    chk("parse-values-verbatim", r1[0]["MESSAGE"] == "a\rb" and r2[0]["MESSAGE"] == "x  " and r2[0]["A_1"] == "\t v", (r1, r2))
    chk("parse-load", load(fixture("week.txt")) == recs)


def check_count_cli():
    """The step-02 command line, byte for byte."""
    rc, out, err = run(["obs.py", "count", fixture("week.txt")])
    chk("count-week", (rc, out) == (0, read("count-week.txt")), f"rc={rc} out={out[:120]!r}")
    rc, out, err = run(["obs.py", "count", fixture("edge.txt")])
    chk("count-edge", (rc, out) == (0, read("count-edge.txt")), f"rc={rc} out={out!r}")
    ok = True
    for name in ("empty.txt", "empty0.txt"):
        rc, out, err = run(["obs.py", "count", fixture(name)])
        ok = ok and (rc, out) == (0, "")
    chk("count-empty", ok)
    ok = True
    for args in (["obs.py"], ["obs.py", "count"], ["obs.py", "report", fixture("week.txt")], ["obs.py", "count", fixture("week.txt"), "x"]):
        rc, out, err = run(args)
        ok = ok and rc == 2 and out == "" and "usage: obs.py count FILE" in err
    chk("count-usage", ok)
    rc, out, err = run(["obs.py", "count", fixture("does-not-exist.txt")])
    chk("count-missing-file", rc == 2 and out == "" and err.startswith("error: ") and len(err.strip()) > len("error:"), f"rc={rc} err={err[:80]!r}")
    ok = True
    for name in ("bad-noeq.txt", "bad-lower.txt", "bad-ts.txt", "bad-nomsg.txt"):
        rc, out, err = run(["obs.py", "count", fixture(name)])
        ok = ok and rc == 1 and out == "" and err.startswith("error: ") and len(err.strip()) > len("error:")
    chk("count-bad-input", ok)


def check_counts_api(modname):
    try:
        mod = __import__(modname, fromlist=["by_unit", "by_day", "day_of"])
    except Exception as e:  # noqa: BLE001
        chk("counts-import", False, repr(e))
        return
    DAY = 86_400_000_000
    r = lambda ts, u=None: {"__REALTIME_TIMESTAMP": ts, "MESSAGE": "m", **({"_SYSTEMD_UNIT": u} if u else {})}  # noqa: E731
    chk("counts-day-of", mod.day_of(0) == "1970-01-01" and mod.day_of(DAY - 1) == "1970-01-01" and mod.day_of(DAY) == "1970-01-02"
        and mod.day_of(1788739199999999) == "2026-09-06" and mod.day_of(1788739200000000) == "2026-09-07")
    recs = [r(1, "b"), r(2, "a"), r(3, "b"), r(4), r(5, "a"), r(6), r(7, "B")]
    chk("counts-by-unit-order", mod.by_unit(recs) == [("-", 2), ("a", 2), ("b", 2), ("B", 1)] and mod.by_unit([]) == [], mod.by_unit(recs))
    empty = [{"__REALTIME_TIMESTAMP": 1, "MESSAGE": "m", "_SYSTEMD_UNIT": ""}, r(2)]
    chk("counts-empty-unit-is-a-unit", mod.by_unit(empty) == [("", 1), ("-", 1)], mod.by_unit(empty))
    chk("counts-by-day-order", mod.by_day([r(DAY), r(0), r(DAY + 5), r(3 * DAY)]) == [("1970-01-01", 1), ("1970-01-02", 2), ("1970-01-04", 1)]
        and mod.by_day([]) == [])


def check_report_cli():
    ok = True
    for w in ("W35", "W36", "W37"):
        rc, out, err = run(["obsreport.py", fixture("week.txt"), f"2026-{w}"])
        if (rc, out) != (0, read(f"report-{w}.md")):
            ok = False
            print(f"  2026-{w}: rc={rc}\n" + "\n".join("  | " + l for l in out.splitlines()[:40]))
    chk("report-weeks", ok)
    ok = True
    for args in ([fixture("week.txt")], [], [fixture("week.txt"), "2026-W36", "x"]):
        rc, out, err = run(["obsreport.py", *args])
        ok = ok and rc == 2 and out == "" and "usage: obsreport.py FILE YYYY-Www" in err
    chk("report-usage", ok)
    ok = True
    for w in ("2026-W54", "2026-36", "2026-W6", "2026-W00", "26-W36", "2026-w36", "2026-W36 ", "2026-W36\n", "\u0662\u0660\u0662\u0666-W36", "2026-W٣٦"):
        rc, out, err = run(["obsreport.py", fixture("week.txt"), w])
        ok = ok and rc == 2 and out == "" and err.startswith("error:")
    chk("report-bad-week", ok)
    rc, out, err = run(["obsreport.py", fixture("does-not-exist.txt"), "2026-W36"])
    chk("report-missing-file", rc == 2 and out == "" and err.startswith("error:"))
    rc, out, err = run(["obsreport.py", fixture("bad-ts.txt"), "2026-W99"])
    chk("report-week-checked-first", rc == 2 and out == "" and err.startswith("error: "), f"rc={rc} err={err[:80]!r}")
    rc, out, err = run(["obsreport.py", fixture("bad-ts.txt"), "2026-W36"])
    chk("report-bad-input", rc == 1 and out == "" and err.startswith("error: ") and len(err.strip()) > len("error:"))
    rc, out, err = run(["obsreport.py", fixture("does-not-exist.txt"), "2026-W36"])
    chk("report-missing-file-description", rc == 2 and len(err.strip()) > len("error:"))


def check_report_api():
    try:
        from observer.report import week_days, weekly
    except Exception as e:  # noqa: BLE001
        chk("report-import", False, repr(e))
        return
    chk("report-week-days", week_days("2026-W36") == ["2026-08-31", "2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04", "2026-09-05", "2026-09-06"]
        and week_days("2020-W53")[0] == "2020-12-28" and week_days("2021-W01")[0] == "2021-01-04")
    MON = 1788134400000000
    HOUR = 3_600_000_000
    many = [{"__REALTIME_TIMESTAMP": MON + i * HOUR, "MESSAGE": f"e{i}", "PRIORITY": "1", "_SYSTEMD_UNIT": "x.service"} for i in range(23)]
    out = weekly(many, "2026-W36")
    chk("report-error-cap", out.endswith("- 2026-08-31T19:00:00Z x.service: e19\n- and 3 more\n") and out.count("\n- 2026-08-31T") == 20, out[-200:])
    out = weekly([], "2026-W36")
    chk("report-empty", out == "# Week 2026-W36\n\n## Units\n\n| unit | count |\n|---|---|\n\n## Days\n\n- 2026-08-31: 0\n- 2026-09-01: 0\n"
        "- 2026-09-02: 0\n- 2026-09-03: 0\n- 2026-09-04: 0\n- 2026-09-05: 0\n- 2026-09-06: 0\n\n## Errors\n\n- none\n", out)
    edge = [{"__REALTIME_TIMESTAMP": MON, "MESSAGE": "p3", "PRIORITY": "3"}, {"__REALTIME_TIMESTAMP": MON, "MESSAGE": "p4", "PRIORITY": "4"},
            {"__REALTIME_TIMESTAMP": MON, "MESSAGE": "none"}, {"__REALTIME_TIMESTAMP": MON, "MESSAGE": "neg", "PRIORITY": "-1"},
            {"__REALTIME_TIMESTAMP": MON, "MESSAGE": "p03", "PRIORITY": "03"}, {"__REALTIME_TIMESTAMP": MON, "MESSAGE": "p10", "PRIORITY": "10"},
            {"__REALTIME_TIMESTAMP": MON, "MESSAGE": "p07", "PRIORITY": "07"}, {"__REALTIME_TIMESTAMP": MON, "MESSAGE": "p29", "PRIORITY": "29"},
            {"__REALTIME_TIMESTAMP": MON, "MESSAGE": "p000", "PRIORITY": "000"}, {"__REALTIME_TIMESTAMP": MON, "MESSAGE": "p2x", "PRIORITY": "2x"}]
    out = weekly(edge, "2026-W36")
    chk("report-error-rule", out.endswith("## Errors\n\n- 2026-08-31T00:00:00Z -: p000\n- 2026-08-31T00:00:00Z -: p03\n- 2026-08-31T00:00:00Z -: p3\n"), out[-200:])
    twenty = [{"__REALTIME_TIMESTAMP": MON + i * HOUR, "MESSAGE": f"e{i}", "PRIORITY": "0"} for i in range(20)]
    out = weekly(twenty, "2026-W36")
    chk("report-exactly-twenty", out.endswith("- 2026-08-31T19:00:00Z -: e19\n") and "more" not in out, out[-120:])


def check_tz(modname="observer.counts"):
    code = (f"from {modname} import by_day, day_of; "
            "print(day_of(1788219000000000), by_day([{'__REALTIME_TIMESTAMP': 1788219000000000, 'MESSAGE': 'a'},"
            " {'__REALTIME_TIMESTAMP': 1788221400000000, 'MESSAGE': 'b'}]))")
    ok = True
    for tz in ("JST-9", "NZST-12", "PST8PDT", "UTC0", "EST5EDT"):
        rc, out, err = run(["-c", code], env={"TZ": tz})
        if out.strip() != "2026-08-31 [('2026-08-31', 1), ('2026-09-01', 1)]":
            ok = False
            print(f"  TZ={tz}: {out.strip()!r} {err[-100:]!r}")
    chk("days-are-utc", ok)
    rc, out, err = run(["obs.py", "count", fixture("week.txt")], env={"TZ": "JST-9"})
    chk("count-week-in-tokyo", (rc, out) == (0, read("count-week.txt")), out[-120:])
