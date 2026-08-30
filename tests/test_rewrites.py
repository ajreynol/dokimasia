"""Tests for rewrite-rule coverage.

Run: python3 tests/test_rewrites.py [<cvc5>]
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dokimasia.rewrites.scan import _strip_comments, rare_to_enum, scan  # noqa: E402

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}" + ("" if ok else f" != {want!r}"))
    if not ok:
        FAILURES.append(label)


def test_units():
    print("units:")
    check("RARE names map to enum names",
          rare_to_enum("bool-double-not-elim"), "BOOL_DOUBLE_NOT_ELIM")
    # the bug that silently lost switch arms: `//.*` under DOTALL ate the rest
    src = "// a comment\nreturn true;"
    check("a line comment does not swallow what follows it",
          _strip_comments(src).strip(), "return true;")
    check("block comments still span lines",
          _strip_comments("/* a\nb */x").strip(), "x")


def test_cvc5(root):
    print(f"cvc5 tree at {root}:")
    r = scan(root)
    check("533 ProofRewriteRules", len(r.declared), 533)
    # RARE files carry six different basenames; discovery is by content, so a
    # glob on `rewrites` alone undercounts by 118 rules.
    check("439 come from RARE files", len(r.rare), 439)
    check("94 are hand-written", len(r.handwritten), 94)
    check("every RARE name has an enum entry", r.rare_without_enum(), [])
    check("the enum marks every generated entry", len(r.marker), 439)
    corr = r.correspondence()
    check("the marker correspondence is exact both ways",
          (corr["marked_without_file"], corr["file_without_marker"]), ([], []))
    check("six RARE file basenames", len(r.file_shapes()), 6)
    check("the ite- prefix is claimed by two theories",
          r.ambiguous_prefixes(), {"ite": ["booleans", "builtin"]})
    # 53 `case ProofRewriteRule::` labels in isHandledTheoryRewrite
    check("all 53 seam arms are parsed", len(r.handled), 53)

    # the fallthrough group at the end of the switch, verified by hand
    for n in ("ARITH_POW_ELIM", "ARRAYS_SELECT_CONST", "LAMBDA_ELIM"):
        check(f"{n} is parsed (last fallthrough group)", n in r.handled, True)
        check(f"{n} needs an unrestricted build", n in r.unrestricted_only, True)
    check("safe-mode gaps are the implemented subset of those",
          r.safe_mode_gaps(),
          ["ARITH_POW_ELIM", "ARRAYS_SELECT_CONST", "LAMBDA_ELIM"])

    check("hard gaps: applied, unprintable, no macro to expand",
          sorted(r.hard_gaps()), ["ARRAYS_EQ_RANGE_EXPAND", "DT_MATCH_ELIM"])
    check("every gap is implemented by some rewriter",
          all(n in r.implemented for n in r.gaps()), True)
    check("no RARE rule is counted as hand-written",
          all(n not in r.rare for n in r.handwritten), True)
    print(f"       {len(r.handwritten)} hand-written, {len(r.implemented)} applicable, "
          f"{len(r.gaps())} gaps ({len(r.macro_gaps())} macro)")


if __name__ == "__main__":
    test_units()
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
