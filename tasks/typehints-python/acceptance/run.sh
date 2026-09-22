#!/bin/bash
# hidden acceptance for typehints-python; runs at the repo root in the staging VM
fail=0
python3 - <<'PY'
import ast, inspect, sys
import shapes
bad = 0
def chk(name, ok, note=""):
    global bad
    bad += not ok
    print(f"CHECK {name} {'ok' if ok else 'fail'}" + ("" if ok else f" ({note})"))
want = {
    "area_circle": ({"r": float}, float),
    "area_rect": ({"w": float, "h": float}, float),
    "perimeter_rect": ({"w": float, "h": float}, float),
    "scale": ({"points": list[tuple[float, float]], "factor": float}, list[tuple[float, float]]),
    "describe": ({"name": str, "area": float}, str),
}
for fn, (params, ret) in want.items():
    f = getattr(shapes, fn, None)
    if f is None:
        chk(f"sig-{fn}", False, "missing"); continue
    sig = inspect.signature(f)
    got = {k: p.annotation for k, p in sig.parameters.items()}
    chk(f"sig-{fn}", list(got) == list(params) and got == params and sig.return_annotation == ret,
        f"{sig}")
src = open("shapes.py").read()
tree = ast.parse(src)
names = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
chk("only-five-functions", names == list(want), names)
imports = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
chk("no-new-imports", [ast.unparse(i) for i in imports] == ["import math"], [ast.unparse(i) for i in imports])
chk("no-typing-aliases", "List[" not in src and "Tuple[" not in src and "typing" not in src)
bodies = [ast.unparse(n.body) for n in tree.body if isinstance(n, ast.FunctionDef)]
want_bodies = ["return math.pi * r * r", "return w * h", "return 2 * (w + h)",
               "return [(x * factor, y * factor) for x, y in points]", "return f'{name}: {area:.2f}'"]
chk("bodies-unchanged", bodies == want_bodies, bodies)
sys.exit(1 if bad else 0)
PY
[ $? = 0 ] || fail=1
if grep -q 'def test_describe' test_shapes.py && grep -q '"disc: 3.14"' test_shapes.py; then echo "CHECK tests-untouched ok"; else echo "CHECK tests-untouched fail"; fail=1; fi
if python3 -m unittest -q test_shapes >/dev/null 2>&1; then echo "CHECK tests-green ok"; else echo "CHECK tests-green fail"; fail=1; fi
n=$(ls *.py | wc -l)
if [ "$n" = 2 ]; then echo "CHECK no-extra-files ok"; else echo "CHECK no-extra-files fail ($n .py files)"; fail=1; fi
exit $fail
