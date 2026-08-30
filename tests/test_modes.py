"""Tests for the modes subtool.

Run: python3 tests/test_modes.py [<cvc5>]
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dokimasia.modes.delta import (  # noqa: E402
    ModeDelta, parse_option_defaults, parse_set_defaults, unsupported_but_enabled,
)

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}" + ("" if ok else f" != {want!r}"))
    if not ok:
        FAILURES.append(label)


def test_cvc5(root):
    src = os.path.join(root, "src") if os.path.isdir(os.path.join(root, "src")) else root
    changes = parse_set_defaults(src)
    # 81 + 34 + 30 + 24 + 3 macro call sites at 16c4001e53
    check("every macro call site is parsed", len(changes) == 172, True)

    md = ModeDelta(changes)
    safe = {c.option for c in md.for_mode("safe")}
    # ground truth read directly out of setDefaultsPre
    for opt in ("sep", "bags", "ff", "fp", "nlCov", "ufSymmetryBreaker",
                "cegqiBv", "varEntEqElimQuant", "bvSolver"):
        check(f"safe mode disables {opt}", opt in safe, True)

    defaults = parse_option_defaults(src)
    # a [[option.mode.X]] subsection must not clobber its parent's fields
    check("bvSolver default survives its mode subsections",
          defaults["bvSolver"]["default"], "BITBLAST")
    check("no_support is captured",
          "proofs" in defaults["stringLazyPreproc"].get("no_support", ""), True)

    # a guard offering plain FULL is not a test for FULL_STRICT
    strict = [c for c in changes if "full_strict" in c.tags]
    check("FULL_STRICT tag excludes disjunctions offering plain FULL",
          all("ProofMode::FULL " not in " ".join(c.guards).replace("FULL_STRICT", "")
              for c in strict), True)

    rows = unsupported_but_enabled(src, md)
    check("the no_support cross-check finds stringLazyPreproc",
          "stringLazyPreproc" in {r["option"] for r in rows}, True)
    check("options safe mode does disable are not reported",
          {"nlCov", "cegqiBv", "ufSymmetryBreaker"} & {r["option"] for r in rows},
          set())


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CVC5")
    if not (root and os.path.isdir(root)):
        print("needs a cvc5 checkout: python3 tests/test_modes.py <cvc5>")
        sys.exit(0)
    print(f"cvc5 tree at {root}:")
    test_cvc5(root)
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
