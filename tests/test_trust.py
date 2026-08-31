"""Tests for the trust census.

Run: python3 tests/test_trust.py [<cvc5>]
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dokimasia.trust.census import census  # noqa: E402

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
        os.makedirs(os.path.join(src, "proof"))
        os.makedirs(os.path.join(src, "preprocessing", "passes"))
        with open(os.path.join(src, "proof", "trust_id.h"), "w") as fh:
            fh.write("enum class TrustId : uint32_t\n{\n  NONE,\n  T_LIVE,\n"
                     "  PREPROCESS_MY_PASS,\n  T_DEAD\n};\n")
        with open(os.path.join(src, "proof", "trust_id.cpp"), "w") as fh:
            fh.write("case TrustId::T_DEAD: return \"T_DEAD\";\n")
        with open(os.path.join(src, "preprocessing", "passes", "my_pass.h"), "w") as fh:
            fh.write("class MyPass;\n")
        with open(os.path.join(src, "preprocessing", "passes", "my_pass.cpp"), "w") as fh:
            fh.write("cdp.addTrustedStep(f, TrustId::PREPROCESS_MY_PASS, {}, {});\n")
        with open(os.path.join(src, "preprocessing", "passes", "quiet.h"), "w") as fh:
            fh.write("class Quiet;\n")
        with open(os.path.join(src, "preprocessing", "passes", "quiet.cpp"), "w") as fh:
            fh.write("// proves its own work\n")
        with open(os.path.join(src, "proof", "other.cpp"), "w") as fh:
            fh.write("mkTrustId(nm, TrustId::T_LIVE);\n"
                     "if (id == TrustId::T_LIVE) {}\n"
                     "cdp.addTrustedStep(f, TrustId::NONE, {}, {});\n")
        c = census(tmp)

        check("the final enum member without a comma is found",
              "T_DEAD" in c.declared, True)
        check("a constructed id is live", c.live(), ["T_LIVE", "PREPROCESS_MY_PASS"])
        check("an id only in the toString switch is dead", c.dead(), ["T_DEAD"])
        check("a comparison is not a construction",
              len(c.construction("T_LIVE")), 1)
        check("TrustId::NONE sites are reported as anonymous",
              len(c.anonymous()), 1)

        pc = c.pass_correspondence()
        check("a pass that constructs an id declares its hole",
              pc["declares"], [("my_pass", ["PREPROCESS_MY_PASS"])])
        check("a pass that constructs none is silent", pc["silent"], ["quiet"])

    sanity.set_enabled(True)


def test_cvc5(root):
    print(f"cvc5 tree at {root}:")
    c = census(root)
    check("75 declared TrustIds", len(c.declared), 75)
    check("all but a few are constructed", len(c.live()), 70)

    # verified by hand: mentioned nowhere outside trust_id.{h,cpp}
    for i in ("PREPROCESS_BV_TO_INT", "PREPROCESS_BV_TO_INT_LEMMA",
              "PREPROCESS_BITVECTOR_EAGER_ATOMS"):
        check(f"{i} is dead", i in c.dead(), True)

    pc = c.pass_correspondence()
    # verified by hand: bv_to_int's trust step is INT_BLASTER, from int_blaster.cpp
    check("bv_to_int constructs no TrustId of its own",
          "bv_to_int" in pc["silent"], True)
    check("INT_BLASTER is live and lives outside the passes directory",
          bool(c.construction("INT_BLASTER")), True)

    # bv_gauss owns two ids, so collect rather than index
    mis = {(p, got) for p, got, _ in c.misnamed_pass_ids()}
    check("the bv_gauss id is misspelled (GUASS)",
          ("bv_gauss", "PREPROCESS_BV_GUASS") in mis, True)
    check("its _LEMMA sibling carries the same typo",
          ("bv_gauss", "PREPROCESS_BV_GUASS_LEMMA") in mis, True)
    print(f"       {len(pc['declares'])} passes declare a hole, "
          f"{len(pc['silent'])} construct no TrustId, "
          f"{len(c.anonymous())} anonymous sites")


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
