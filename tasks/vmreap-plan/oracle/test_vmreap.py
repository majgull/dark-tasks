import os
import subprocess
import sys
import tempfile
import unittest

from vmreap import parse_list, parse_status, plan

LIST = """      VMID NAME                 STATUS     MEM(MB)    BOOTDISK(GB) PID
       101 model-server         running    16000            180.00 4242
       110 dark-x0              running    4096              16.00 6161
       113 dark-s2              stopped    4096              16.00 0
"""
STATUS = "cpus: 4\nname: dark-x0\nstatus: running\nuptime: 5000\nvmid: 110\n"


class Parse(unittest.TestCase):
    def test_list(self):
        vms = parse_list(LIST)
        self.assertEqual([v["vmid"] for v in vms], [101, 110, 113])
        self.assertEqual(vms[0], {"vmid": 101, "name": "model-server", "status": "running", "mem_mb": 16000, "bootdisk_gb": 180.0, "pid": 4242})
        for bad in ("", "NAME VMID\n", LIST + "      115 dark-s3 running 4096 16.00\n", LIST.replace("110", "11x0")):
            with self.assertRaises(ValueError):
                parse_list(bad)

    def test_status(self):
        self.assertEqual(parse_status(STATUS)["uptime"], "5000")
        self.assertEqual(parse_status("nothing here\nblockstat:\n  rd: 1\n")["rd"], "1")

    def test_plan(self):
        vms = parse_list(LIST)
        self.assertEqual(plan(vms, {110: parse_status(STATUS)}, 3600),
                         ["qm stop 110", "qm destroy 110 --purge", "qm destroy 113 --purge"])
        self.assertEqual(plan(vms, {110: parse_status(STATUS)}, 6000), ["qm destroy 113 --purge"])
        with self.assertRaises(ValueError):
            plan(vms, {}, 3600)
        with self.assertRaises(ValueError):
            plan(vms, {110: {"uptime": "soon"}}, 3600)

    def test_cli(self):
        d = tempfile.mkdtemp()
        with open(os.path.join(d, "list.txt"), "w") as f:
            f.write(LIST)
        with open(os.path.join(d, "110.txt"), "w") as f:
            f.write(STATUS)
        cli = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vmreap.py")
        r = subprocess.run([sys.executable, cli, "plan", "--list", os.path.join(d, "list.txt"), "--status-dir", d],
                           capture_output=True, text=True)
        self.assertEqual((r.returncode, r.stdout), (1, "qm stop 110\nqm destroy 110 --purge\nqm destroy 113 --purge\n"))
        self.assertEqual(r.stderr, "vmreap: 2 factory VM(s), 2 to reap\n")
        r = subprocess.run([sys.executable, cli, "plan", "--list", os.path.join(d, "list.txt")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
