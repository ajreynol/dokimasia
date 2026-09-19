"""A baseline may name nothing cvc5 does not have, and record nothing it does not say.

A baseline is only worth what it was generated from. Ours once carried
`SETS_RELS_TCLOSURE_DOWN`, an id cvc5 has never had, and two ratchets failed
against the very commit they claimed to be recorded at. This is the guard:
given a checkout, no baseline may name an id that is not in the enum.

The second half is the same failure in a quieter shape. A baseline records more
than the figure its ratchet compares, and a field nothing checks is a number
carrying the authority of a committed measurement and none of the evidence. So
at the pinned commit every recorded field is recomputed, not only the ratcheted
one.

Run: python3 tests/test_baselines.py <cvc5>
"""
import json, os, subprocess, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokimasia_analyzer.inferid.scan import _declared  # noqa: E402
from dokimasia_analyzer.inferid.__main__ import _src  # noqa: E402
from dokimasia_analyzer.paths import baseline  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
LOCK = os.path.join(ROOT, "scripts", "cvc5.lock")
FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    if not ok:
        print(f"       got {got!r}, want {want!r}")
        FAILURES.append(label)


def _ids_in(obj):
    """Every string that looks like an InferenceId, anywhere in the JSON."""
    if isinstance(obj, str):
        return {obj}
    if isinstance(obj, dict):
        out = set()
        for k, v in obj.items():
            out |= _ids_in(k) | _ids_in(v)
        return out
    if isinstance(obj, list):
        out = set()
        for v in obj:
            out |= _ids_in(v)
        return out
    return set()


def test_cvc5(root):
    print(f"against {root}")
    declared = set(_declared(_src(root)))
    check("the enum was found at all", len(declared) > 100, True)

    # Theory names and bookkeeping keys are not ids; an id is SHOUTY_SNAKE and
    # is not one of the theory buckets the baselines are keyed by.
    for name in ("infer", "inferid"):
        path = baseline(name)
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        buckets = set(data) if isinstance(data, dict) else set()
        candidates = {
            s for s in _ids_in(data)
            if s not in buckets and s.replace("_", "").isalnum()
            and s.isupper() and "_" in s
        }
        unknown = sorted(candidates - declared - {"UNKNOWN"})
        check(f"{name} names only ids cvc5 declares", unknown, [])


def test_tcb_context(root):
    """The TCB baseline's unratcheted fields, recomputed at the pinned commit.

    `tcb baseline --check` compares `tcb_files` and `tcb_lines` and nothing
    else, so the denominator it was recorded against -- the one the published
    8.0% is a fraction of -- is committed and never re-read. Only at the pin:
    every other revision has a different `src/` and a diff against one says
    nothing, so the skip names itself rather than passing quietly.
    """
    from argparse import Namespace
    from dokimasia_analyzer.tcb.__main__ import _closure, _stats

    pin = json.load(open(LOCK, encoding="utf-8"))["cvc5"]["commit"]
    head = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    if not head.startswith(pin):
        print(f"  skip  the TCB baseline's context: {root} is at "
              f"{head[:10] or 'no commit'}, not the pinned {pin}")
        return
    with open(baseline("tcb"), encoding="utf-8") as fh:
        old = json.load(fh)
    graph, clo = _closure(Namespace(cvc5=root, seeds=old["seed_set"], mode=old["mode"]))
    now = _stats(graph, clo)
    now["seed_set"] = old["seed_set"]
    for field in sorted(old):
        check(f"tcb baseline {field} is what the pinned tree gives",
              now.get(field), old[field])
    if any(now.get(f) != old[f] for f in old):
        print("        re-record it: python3 -m dokimasia_analyzer.tcb baseline <cvc5> --write")


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CVC5")
    if not (root and os.path.isdir(root)):
        print("needs a cvc5 checkout: python3 tests/test_baselines.py <cvc5>")
        sys.exit(0)
    test_cvc5(root)
    test_tcb_context(root)
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
