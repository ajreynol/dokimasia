"""Tests for inference coverage, and for the extraction guard.

Run: python3 tests/test_infer.py [<cvc5>]
"""
import os, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokimasia import sanity  # noqa: E402
from dokimasia.infer.coverage import CORE, _theory_of, scan  # noqa: E402

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}" + ("" if ok else f" != {want!r}"))
    if not ok:
        FAILURES.append(label)


def test_guard():
    print("the extraction guard:")
    fired = False
    try:
        sanity.expect(0, 300, "InferenceId enum members", "the enum")
    except sanity.ExtractionError as e:
        fired = True
        msg = str(e)
    check("a silent-zero extraction raises", fired, True)
    check("the message names the anchor", "the enum" in msg, True)
    check("and says the bug is ours", "our" in msg, True)
    sanity.set_enabled(False)
    try:
        sanity.expect(0, 300, "x", "y")
        check("disabled, it does not fire", True, True)
    except sanity.ExtractionError:
        check("disabled, it does not fire", False, True)
    sanity.set_enabled(True)


def test_attribution():
    print("theory attribution:")
    check("a file in a theory directory", _theory_of("theory/strings/core_solver.cpp"), "strings")
    # `theory/theory_engine.cpp` has no owning theory; taking parts[1] blindly
    # once produced a theory called `theory_engine.cpp`
    check("a file directly in theory/ is core", _theory_of("theory/theory_engine.cpp"), CORE)
    check("a file outside theory/ has no theory", _theory_of("smt/proof_manager.cpp"), None)


def test_cvc5(root):
    print(f"cvc5 tree at {root}:")
    c = scan(root)
    st = c.theories["strings"]
    check("strings has a reconstructor", st.has_ipc, True)
    check("its default case builds a TRUST step", st.trust_fallback, True)
    check("strings emits more inferences than it reconstructs",
          len(st.produced) > len(st.reconstructed), True)
    check("STRINGS_CODE_PROXY is a case for an inference nothing emits",
          "STRINGS_CODE_PROXY" in st.reconstructed_not_produced, True)
    check("quantifiers has no InferProofCons",
          c.theories["quantifiers"].has_ipc, False)
    check("a theory without one gets no rate rather than 0%",
          c.theories["quantifiers"].rate, None)
    check("unhandled counts only theories that have a reconstructor",
          c.total_unhandled() == sum(len(t.unhandled) for t in c.with_reconstructor()),
          True)
    print(f"       {c.total_unhandled()} inferences fall through to a trust step; "
          f"{len(c.without_reconstructor())} theories have no reconstructor")


if __name__ == "__main__":
    test_guard()
    print()
    test_attribution()
    root = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CVC5")
    if root and os.path.isdir(root):
        print()
        test_cvc5(root)
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
