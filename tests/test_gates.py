"""Tests for the option-gate analysis.

Run: python3 tests/test_gates.py [<cvc5>]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokimasia.gates.gates import scan  # noqa: E402

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}" + ("" if ok else f" != {want!r}"))
    if not ok:
        FAILURES.append(label)


def test_cvc5(root):
    print(f"cvc5 tree at {root}:")
    kg = scan(root)
    # verified by hand against smt/illegal_checker.cpp
    check("MATCH is gated by datatypesExp",
          sorted(kg.kind_gate.get("MATCH", [])), ["datatypesExp"])
    check("STORE_ALL is gated by arraysExp",
          sorted(kg.kind_gate.get("STORE_ALL", [])), ["arraysExp"])
    # verified by hand against theory/arrays/theory_arrays.cpp:321 -- a
    # LogicException guard, not illegal_checker
    check("EQ_RANGE's gate comes from a theory LogicException",
          (sorted(kg.kind_gate.get("EQ_RANGE", [])),
           kg.origin.get("EQ_RANGE")),
          (["arraysExp"], "theory/arrays/theory_arrays.cpp"))

    for rule, want in (("DT_MATCH_ELIM", "blocked"),
                       ("ARRAYS_EQ_RANGE_EXPAND", "blocked"),
                       ("ARITH_POW_ELIM", "blocked"),
                       # conjunctive arm: SELECT && STORE_ALL
                       ("ARRAYS_SELECT_CONST", "partial"),
                       # only names Kind::LAMBDA, which nothing gates
                       ("LAMBDA_ELIM", "open")):
        check(f"{rule} is {want} in safe mode", kg.verdict(rule)[0], want)

    check("a rule with no arm gets no verdict",
          kg.verdict("NO_SUCH_RULE")[0], "unknown")
    print(f"       {len(kg.kind_gate)} gated kinds, {len(kg.rule_kinds)} rules with kinds")


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CVC5")
    if not (root and os.path.isdir(root)):
        print("needs a cvc5 checkout: python3 tests/test_gates.py <cvc5>")
        sys.exit(0)
    test_cvc5(root)
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
