"""The safe-build invariant, and that its verifier actually fires.

A checker nobody has seen fail is a checker nobody should trust, so the
violations are tested against synthetic trees alongside the real one.

Run: python3 tests/test_buildmode.py [<cvc5>]
"""
import os, sys, tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokimasia.buildmode import buildmode as B  # noqa: E402

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    if not ok:
        print(f"       got {got!r}, want {want!r}")
        FAILURES.append(label)


def _tree(files):
    d = tempfile.mkdtemp()
    for rel, text in files.items():
        p = os.path.join(d, "src", rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
    return d


def test_classify():
    check("a message-only block is diagnostic",
          B._classify("#ifdef CVC5_SAFE_MODE",
                      '#ifdef CVC5_SAFE_MODE\n  ss << " Try --ff.";\n'),
          B.DIAGNOSTIC)
    check("an option default is recognised",
          B._classify("#ifdef CVC5_SAFE_MODE",
                      "#ifdef CVC5_SAFE_MODE\n"
                      "  d_base->safeMode = options::SafeMode::SAFE;\n"),
          B.OPTION_DEFAULT)
    check("a build-report define is recognised",
          B._classify("#ifdef CVC5_SAFE_MODE",
                      "#ifdef CVC5_SAFE_MODE\n#define IS_SAFE_BUILD true\n"),
          B.CONFIG_REPORT)
    check("a call that is not a message is unclassified",
          B._classify("#ifdef CVC5_SAFE_MODE",
                      "#ifdef CVC5_SAFE_MODE\n  d_engine->disableTheory(X);\n"),
          B.UNCLASSIFIED)
    check("an option default doing more is unclassified",
          B._classify("#ifdef CVC5_SAFE_MODE",
                      "#ifdef CVC5_SAFE_MODE\n"
                      "  d_base->safeMode = options::SafeMode::SAFE;\n"
                      "  rebuildEverything();\n"),
          B.UNCLASSIFIED)


def test_fires():
    """Each way the invariant can break must actually be reported."""
    d = _tree({"theory/x.cpp":
               "void f() {\n#ifdef CVC5_SAFE_MODE\n"
               "  d_engine->disableTheory(THEORY_STRINGS);\n#endif\n}\n"})
    r = B.scan(d)
    check("behaviour gated on the build macro breaks it", r.holds(), False)
    check("...and the site is named", len(r.unclassified()), 1)

    d = _tree({"theory/y.cpp":
               "void g() {\n  if (Configuration::isSafeBuild()) { other(); }\n}\n"})
    r = B.scan(d)
    check("branching on isSafeBuild breaks it", r.holds(), False)
    check("...and the branch is named", len(r.behavioural_readers), 1)

    d = _tree({"theory/z.cpp":
               'void h() {\n#ifdef CVC5_SAFE_MODE\n  ss << " Try --ff.";\n#endif\n}\n'})
    check("a message-only conditional does not break it", B.scan(d).holds(), True)


def test_cvc5(root):
    r = B.scan(root)
    check("the invariant holds on cvc5", r.holds(), True)
    check("no source file is excluded from a safe build", r.excluded_sources, [])
    check("nothing branches on isSafeBuild()", r.behavioural_readers, [])
    kinds = r.by_kind()
    check("every conditional is classified benign",
          [k for k in kinds if k not in B.BENIGN], [])
    check("a safe build declines exactly the three optional libraries",
          sorted(r.disabled_libraries), ["USE_COCOA", "USE_NORMALIZ", "USE_POLY"])
    # The reviewed allowlist is a debt; keep it visibly small.
    check("at most one block rests on human review",
          len(B.REVIEWED_BLOCKS) <= 1, True)
    print(f"       {len(r.conditionals)} conditionals: {kinds}")


if __name__ == "__main__":
    test_classify()
    print()
    test_fires()
    root = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CVC5")
    if root and os.path.isdir(root):
        print()
        test_cvc5(root)
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
