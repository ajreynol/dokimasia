"""The rewriter faithfulness report: its records, probes and generated page.

Needs no solver: the probe parsers are tested on canned output, and the
records and REPORT.md are checked as files.

Run: python3 tests/test_rewriter_report.py
"""
import glob, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                    "rewriter_report")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build_report as B  # noqa: E402
import probe as P  # noqa: E402

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    if not ok:
        print(f"       got {got!r}, want {want!r}")
        FAILURES.append(label)


def test_parsers():
    print("probe parsers:")
    check("an answer after an error is no evidence",
          P._answer('(error "unknown constant str.rev")\nsat\n'), "error")
    check("a plain answer", P._answer("unsat\n"), "unsat")
    pf = ("; trust TRUST_THEORY_REWRITE\n"
          "; trust TRUST MACRO_THEORY_REWRITE_RCONS_SIMPLE\n")
    check("trust lines with one or two tokens",
          [i or k for k, i in P._TRUST.findall(pf)],
          ["TRUST_THEORY_REWRITE", "MACRO_THEORY_REWRITE_RCONS_SIMPLE"])
    defs = "(define @t1 () (bvadd x y))\n(define @t2 () (bvneg @t1))\n"
    check("printer abbreviations are inlined",
          P._expand("(= @t2 @t1)", defs),
          "(= (bvneg (bvadd x y)) (bvadd x y))")


def test_records():
    print("records:")
    units, rules, errors = B.load()
    check("every record is well formed and its probes exist", errors, [])
    check("there is at least one unit", bool(units), True)
    merged = B.merge(rules)
    sus = sorted(r["id"] for r in merged if r["confidence"] == "suspect")
    # The calibration case: #13039 must stay suspect at the pinned revision.
    check("MultSltMult is suspect", "MultSltMult" in sus, True)
    with open(os.path.join(ROOT, "REPORT.md")) as f:
        check("REPORT.md is regenerated", f.read() == B.render(units, merged),
              True)


def test_probes():
    print("probes:")
    files = glob.glob(os.path.join(ROOT, "probes", "*", "*.smt2"))
    missing = [os.path.relpath(f, ROOT) for f in files
               if not P._EXPECT.search(open(f).read())]
    check("every probe declares EXPECT", missing, [])


if __name__ == "__main__":
    test_parsers()
    test_records()
    test_probes()
    print(f"\n{len(FAILURES)} failure(s)")
    sys.exit(1 if FAILURES else 0)
