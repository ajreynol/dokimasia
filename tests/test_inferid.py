"""Tests for the InferenceId subtool.

Run: python3 tests/test_inferid.py [<cvc5>]
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dokimasia.inferid.scan import SENTINELS, scan  # noqa: E402

from dokimasia import sanity  # noqa: E402

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}" + ("" if ok else f" != {want!r}"))
    if not ok:
        FAILURES.append(label)


def test_synthetic():
    # a synthetic fixture is smaller than any real tree; the size
    # thresholds describe cvc5, not a five-line stand-in for it
    sanity.set_enabled(False)
    print("synthetic tree:")
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "src")
        os.makedirs(os.path.join(src, "theory", "foo"))
        with open(os.path.join(src, "theory", "inference_id.h"), "w") as fh:
            fh.write("enum class InferenceId\n{\n  NONE,\n  A_ONE,\n  A_TWO,\n"
                     "  A_DEAD,\n  // a comment\n  UNKNOWN\n};\n")
        with open(os.path.join(src, "theory", "inference_id.cpp"), "w") as fh:
            fh.write("case InferenceId::A_ONE: return \"A_ONE\";\n"
                     "case InferenceId::A_DEAD: return \"A_DEAD\";\n")
        with open(os.path.join(src, "theory", "foo", "solver.cpp"), "w") as fh:
            fh.write("d_im.lemma(x, InferenceId::A_ONE);\n"
                     "d_im.lemma(y, InferenceId::A_TWO);\n"
                     "d_im.lemma(z, InferenceId::A_TWO);\n"
                     "if (id == InferenceId::A_ONE) {}\n"
                     "switch (id) { case InferenceId::A_ONE: break; }\n")
        m = scan(src)

        check("the final enum member (no trailing comma) is found",
              "UNKNOWN" in m.declared, True)
        check("all members are declared", m.declared,
              ["NONE", "A_ONE", "A_TWO", "A_DEAD", "UNKNOWN"])
        check("one production site satisfies the contract",
              len(m.production("A_ONE")), 1)
        check("a comparison is not a production site",
              [u.kind for u in m.uses["A_ONE"] if u.line == 4], ["comparison"])
        check("a case label is not a production site",
              [u.kind for u in m.uses["A_ONE"] if u.line == 5], ["dispatch"])
        check("two production sites is a violation",
              [i for i, _ in m.violations()], ["A_TWO"])
        check("an id nothing produces is dead", m.unused(), ["A_DEAD"])
        check("sentinels are excluded from violations",
              all(i not in SENTINELS for i, _ in m.violations()), True)

    sanity.set_enabled(True)


def test_cvc5(root):
    src = os.path.join(root, "src") if os.path.isdir(os.path.join(root, "src")) else root
    m = scan(src)
    print(f"cvc5 tree at {root}:")
    check("413 ids declared (412 plus the comma-less UNKNOWN)", len(m.declared), 413)

    # verified by hand against theory_arrays.cpp
    check("ARRAYS_EQ_TAUTOLOGY has 8 production sites",
          len(m.production("ARRAYS_EQ_TAUTOLOGY")), 8)
    # verified by hand: only in the toString switch
    check("BV_LAYERED_CONFLICT is produced nowhere",
          len(m.production("BV_LAYERED_CONFLICT")), 0)
    # verified by hand: dispatched on in infer_proof_cons, produced nowhere
    kinds = {u.kind for u in m.uses["STRINGS_CODE_PROXY"]}
    check("STRINGS_CODE_PROXY is dispatched but never produced",
          ("dispatch" in kinds, "production" in kinds), (True, False))

    total = len([i for i in m.declared if i not in SENTINELS])
    ok = total - len(m.violations())
    print(f"       {ok}/{total} satisfy the contract; "
          f"{len(m.violations())} violations, {len(m.unused())} dead")
    check("the contract already holds for most ids", ok / total > 0.8, True)


if __name__ == "__main__":
    test_synthetic()
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
