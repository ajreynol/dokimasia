"""Every InferenceId named in a baseline must be one cvc5 actually declares.

A baseline is only worth what it was generated from. Ours once carried
`SETS_RELS_TCLOSURE_DOWN`, an id cvc5 has never had, and two ratchets failed
against the very commit they claimed to be recorded at. This is the guard:
given a checkout, no baseline may name an id that is not in the enum.

Run: python3 tests/test_baselines.py <cvc5>
"""
import json, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokimasia.inferid.scan import _declared  # noqa: E402
from dokimasia.inferid.__main__ import _src  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
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
    for name in ("infer-baseline.json", "inferid-baseline.json"):
        path = os.path.join(ROOT, name)
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


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CVC5")
    if not (root and os.path.isdir(root)):
        print("needs a cvc5 checkout: python3 tests/test_baselines.py <cvc5>")
        sys.exit(0)
    test_cvc5(root)
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
