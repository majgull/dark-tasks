import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


def run(*args):
    return subprocess.run([sys.executable, os.path.join(HERE, "jsonflat.py"), *args], capture_output=True, text=True)


class JsonFlat(unittest.TestCase):
    def doc(self, value):
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w") as f:
            json.dump(value, f)
        self.addCleanup(os.remove, path)
        return path

    def test_example(self):
        p = self.doc({"name": "dark", "tags": ["a", "b"], "meta": {"ok": True, "n": None, "empty": {}}})
        r = run(p)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout, "meta.empty={}\nmeta.n=null\nmeta.ok=true\nname=dark\ntags[0]=a\ntags[1]=b\n")

    def test_nested_lists(self):
        r = run(self.doc([[1, 2], {"b": []}]))
        self.assertEqual(r.stdout, "[0][0]=1\n[0][1]=2\n[1].b=[]\n")

    def test_errors(self):
        self.assertEqual(run().returncode, 2)
        self.assertEqual(run(self.doc(5)).returncode, 1)
        self.assertEqual(run("/nonexistent/x.json").returncode, 1)


if __name__ == "__main__":
    unittest.main()
