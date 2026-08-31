"""Tests for the signature cross-check.

Run: python3 tests/test_signature.py [<cvc5>]
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokimasia.signature.compare import _arg_count, _premise_shape, printed_name, scan  # noqa: E402

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}" + ("" if ok else f" != {want!r}"))
    if not ok:
        FAILURES.append(label)


def test_latex():
    print("LaTeX arity parsing — each case is a bug this tool once had:")
    check("a conjunction containing dots is ONE premise",
          _premise_shape(r"(F_1 \land \dots \land F_n)"), 1)
    check("a bare ellipsis between items means variadic",
          _premise_shape(r"t_1=t_2,\dots,t_{n-1}=t_n"), "variadic")
    check(r"`\,` is a thin space, not a premise separator",
          _premise_shape(r"n \geq 0,\, \mathit{len}(t) \geq n"), 2)
    check("no premises", _premise_shape("-"), 0)
    check("a negated quantifier with bound-variable dots is one premise",
          _premise_shape(r"\neg (\forall x_1\dots x_n.\> F)"), 1)
    check("an s-expression argument counts once", _arg_count("F_1 = F_2"), 1)
    check("variadic args", _arg_count(r"F_1, \dots, F_n"), -1)


def test_cvc5(root):
    print(f"cvc5 tree at {root}:")
    s = scan(root)
    check("ASSUME is the only printable rule without a declaration",
          s.missing(), [])
    check("the signature declares 620 rules", len(s.sig), 620)
    check("AND_ELIM prints as and_elim", printed_name("AND_ELIM"), "and_elim")
    check("three rules collapse to refl",
          {printed_name(r) for r in ("ENCODE_EQ_INTRO", "HO_APP_ENCODE", "BV_EAGER_ATOM")},
          {"refl"})
    k = s.skolems
    check("65 SkolemIds declared", len(k.declared), 65)
    check("every constructed skolem documents its index count", k.undocumented(), [])
    check("some constructed skolems are unprintable", len(k.unprintable()) > 0, True)
    print(f"       {len(k.unprintable())} skolems constructed but unprintable, "
          f"{len(k.dead())} dead")


if __name__ == "__main__":
    test_latex()
    root = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CVC5")
    if root and os.path.isdir(root):
        print()
        test_cvc5(root)
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
