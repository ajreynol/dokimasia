"""Tests for the supported-fragment analysis.

Run: python3 tests/test_fragment.py [<cvc5>]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokimasia.fragment.fragment import EXPERT_OPTIONS, scan  # noqa: E402

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}" + ("" if ok else f" != {want!r}"))
    if not ok:
        FAILURES.append(label)


def test_cvc5(root):
    print(f"cvc5 tree at {root}:")
    f = scan(root)
    check("14 theories have a kinds.toml", len(f.theory_id), 14)
    check("theory ids are read", f.theory_id.get("arrays"), "THEORY_ARRAYS")

    # theories safe mode disables outright are swept whole
    for th in ("fp", "ff", "bags", "sep"):
        avail, blocked = f.safe_fragment(th)
        check(f"{th} contributes no available kind", avail, [])
        check(f"{th} is blocked by the sweep",
              f.blocked_in_safe_mode(blocked[0])[1].startswith("whole-theory sweep"), True)

    # verified by hand against illegal_checker.cpp and theory_arrays.cpp
    check("STORE_ALL is on the deny list",
          f.blocked_in_safe_mode("STORE_ALL")[0], True)
    check("EQ_RANGE is blocked by a theory-local guard",
          f.blocked_in_safe_mode("EQ_RANGE")[0], True)
    check("a core boolean kind is available",
          f.blocked_in_safe_mode("AND")[0], False)

    # the nested-guard shape: kinds in the enclosing block, option in the inner
    cov = f.expert_coverage()
    check("setsExp's four kinds are recovered from the enclosing guard",
          cov["setsExp"],
          ["RELATION_JOIN_IMAGE", "SET_COMPLEMENT", "SET_COMPREHENSION", "SET_UNIVERSE"])

    # the substantive result
    unc = {o for o, _a, _w in f.uncovered_expert_options()}
    check("two expert options gate no term kind", unc, {"fpExp", "ufHoExp"})
    axes = {o: a for o, a, _w in f.uncovered_expert_options()}
    check("ufHoExp restricts the logic", axes["ufHoExp"], "logic")
    check("fpExp restricts a type", axes["fpExp"], "type")

    # no UF kind is blocked -- bears on i-1 (LAMBDA_ELIM)
    check("no uf kind is blocked in safe mode", f.safe_fragment("uf")[1], [])
    print(f"       {len(f.kinds)} kinds over {len(f.theory_id)} theories; "
          f"{len(EXPERT_OPTIONS)} expert options")


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CVC5")
    if not (root and os.path.isdir(root)):
        print("needs a cvc5 checkout: python3 tests/test_fragment.py <cvc5>")
        sys.exit(0)
    test_cvc5(root)
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
