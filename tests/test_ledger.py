"""Tests for the proof-rule ledger.

Run: python3 tests/test_ledger.py [<cvc5>]
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dokimasia.ledger.build import Row, _parse_is_handled, build  # noqa: E402

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}" + ("" if ok else f" != {want!r}"))
    if not ok:
        FAILURES.append(label)


def test_is_handled_parsing():
    print("isHandled parsing (C fallthrough):")
    with tempfile.TemporaryDirectory() as tmp:
        d = os.path.join(tmp, "proof", "eo")
        os.makedirs(d)
        with open(os.path.join(d, "eo_printer.cpp"), "w") as fh:
            fh.write("""
bool EoPrinter::isHandled(const Options& opts, const ProofNode* pfn)
{
  switch (pfn->getRule())
  {
    case ProofRule::A_ONE:
    case ProofRule::A_TWO:
      return true;
    case ProofRule::B_COND:
    {
      return isHandledSomething(pfn->getArguments()[0]);
    }
    break;
    default: break;
  }
  return false;
}
""")
        got = _parse_is_handled(tmp)
    check("a fallthrough label shares the next body's verdict",
          got.get("A_ONE"), "always")
    check("the label carrying the body is also always", got.get("A_TWO"), "always")
    check("an arm that computes its answer is conditional",
          got.get("B_COND"), "conditional")
    check("a rule absent from the switch is not listed", "C_MISSING" in got, False)


def test_classification():
    print("unprintable classification:")
    r = Row(name="MACRO_X", produced=["a:1"], printed="never")
    check("a macro is by design", r.unprintable_kind, "by-design")
    r = Row(name="SUBS", produced=["a:1"], elaborated=["b:2"], printed="never")
    check("an elaborated non-macro is by design too", r.unprintable_kind, "by-design")
    r = Row(name="FF_X", produced=[], printed="never")
    check("nothing produces it, so it cannot bite", r.unprintable_kind, "unreachable")
    r = Row(name="ARITH_X", produced=["a:1"], printed="never")
    check("produced and unprintable is a gap", r.unprintable_kind, "gap")
    check("only a gap raises SEAM0001", "SEAM0001" in r.holes, True)


def test_cvc5(root):
    print(f"cvc5 tree at {root}:")
    L = build(root)
    check("170 ProofRules (172 less UNKNOWN and LAST)", len(L.rules), 170)
    check("533 ProofRewriteRules", len(L.rewrite_rules), 533)

    u = L.unprintable()
    # verified by hand against eo_printer.cpp and the arith solvers
    check("SUBS is elaborated away, so not a gap",
          L.rules["SUBS"].unprintable_kind, "by-design")
    check("MACRO_REWRITE is elaborated", bool(L.rules["MACRO_REWRITE"].elaborated), True)
    check("TRUST is by design, not a printing gap",
          L.rules["TRUST"].unprintable_kind, "by-design")
    check("the FF rules are unreachable, not gaps",
          L.rules["FF_DISEQ"].unprintable_kind, "unreachable")
    check("ARITH_POW2_INIT is a real gap",
          L.rules["ARITH_POW2_INIT"].unprintable_kind, "gap")
    check("ARITH_POW2_INIT's checker is registered as trusted",
          L.rules["ARITH_POW2_INIT"].pedantic, 1)
    check("every gap is produced somewhere",
          all(r.produced for r in u["gap"]), True)
    print(f"       printed: always/conditional/never = "
          f"{sum(1 for r in L.rows() if r.printed=='always')}/"
          f"{sum(1 for r in L.rows() if r.printed=='conditional')}/"
          f"{sum(1 for r in L.rows() if r.printed=='never')}; "
          f"{len(u['gap'])} real gaps")


if __name__ == "__main__":
    test_is_handled_parsing()
    print()
    test_classification()
    root = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CVC5")
    if root and os.path.isdir(root):
        print()
        test_cvc5(root)
    else:
        print("\n(skipping cvc5 tests; pass a checkout or set CVC5)")
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
