import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


def run(*args):
    return subprocess.run([sys.executable, os.path.join(HERE, "csvstat.py"), *args], capture_output=True, text=True)


class CsvStat(unittest.TestCase):
    def csv(self, text):
        fd, path = tempfile.mkstemp(suffix=".csv")
        with os.fdopen(fd, "w") as f:
            f.write(text)
        self.addCleanup(os.remove, path)
        return path

    def test_example(self):
        r = run(self.csv("name,age,city\nann,34,Bonn\nbob,,Köln\ncid,27.5,Bonn\n"))
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "name: count=3 distinct=3\nage: count=2 min=27.5 max=34 mean=30.75\ncity: count=3 distinct=2\n")

    def test_short_rows_and_ties(self):
        r = run(self.csv("a,b\n1.0\n1,x\n"))
        self.assertEqual(r.stdout, "a: count=2 min=1.0 max=1.0 mean=1.00\nb: count=1 distinct=1\n")

    def test_errors(self):
        self.assertEqual(run().returncode, 2)
        self.assertEqual(run("/nonexistent/x.csv").returncode, 1)
        self.assertEqual(run(self.csv("")).returncode, 1)


if __name__ == "__main__":
    unittest.main()
