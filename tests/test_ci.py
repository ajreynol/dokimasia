"""Tests for the CI-integrity analysis.

Run: python3 tests/test_ci.py [<cvc5>]
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dokimasia.ci.scan import scan  # noqa: E402

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
        wf = os.path.join(tmp, ".github", "workflows")
        rr = os.path.join(tmp, "test", "regress", "cli")
        os.makedirs(wf)
        os.makedirs(rr)
        with open(os.path.join(wf, "ci.yml"), "w") as fh:
            fh.write("""jobs:
  builds:
    strategy:
      matrix:
        build:
          - name: linux:safe-mode
            config: safe-mode --auto-download
            exclude_regress: 3-4
            run_regression_args: --tester base --tester proof --tester cpc
          - name: linux:plain
            config: production --auto-download
            run_regression_args: --tester base --tester model
    steps:
      - name: Checkout code
""")
        with open(os.path.join(rr, "run_regression.py"), "w") as fh:
            fh.write('''
class BaseTester(Tester):
    def __init__(self):
        super().__init__("base")

class ProofTester(Tester):
    def __init__(self):
        super().__init__("proof")
    def run_internal(self, b):
        return super().run_internal(b._replace(
            command_line_args=b.command_line_args + ["--check-proofs", "--proof-check=lazy"]))

g_default_testers = ["base", "proof"]
PARSER.add_argument("--not-a-tester-flag")
''')
        m = scan(tmp)

    check("matrix entries are found, workflow steps are not",
          sorted(j.name for j in m.jobs), ["linux:plain", "linux:safe-mode"])
    check("a safe-mode config is recognised",
          [j.mode for j in m.jobs if j.name == "linux:safe-mode"], ["safe"])
    check("testers are parsed from run_regression_args",
          [j.testers for j in m.jobs if j.name == "linux:safe-mode"],
          [["base", "proof", "cpc"]])
    check("only jobs with a proof tester are listed",
          [j.name for j in m.jobs_with_proofs()], ["linux:safe-mode"])
    check("tester flags are extracted",
          m.testers["proof"].flags, ["--check-proofs", "--proof-check=lazy"])
    check("a flag-free tester reports none", m.testers["base"].flags, [])
    check("module-level argparse flags do not leak into the last tester",
          "--not-a-tester-flag" not in m.testers["proof"].flags, True)

    chain = m.completeness_chain()
    check("four links hold", sum(1 for _, ok, _ in chain if ok), 4)
    check("the last link -- naming completeness -- does not", chain[-1][1], False)

    sanity.set_enabled(True)


def test_cvc5(root):
    print(f"cvc5 tree at {root}:")
    m = scan(root)
    # A count is the wrong assertion here: a branch may add a tester (cvc5-ajr
    # carries `cpc-logos`), and pinning the number makes an unrelated checkout
    # fail for no defect. What must hold is that the ten we reason about are
    # all present -- a missing one silently narrows every CI claim we make.
    known = {"abduct", "alethe", "base", "cpc", "dump", "lfsc",
             "model", "proof", "synth", "unsat-core"}
    check("the ten testers we reason about are all present",
          sorted(known - set(m.testers)), [])
    # verified by hand against run_regression.py
    check("the proof tester's flags", m.testers["proof"].flags,
          ["--check-proofs", "--proof-check=lazy"])
    check("BaseTester adds no flags (it does not inherit UnsatCoreTester's)",
          m.testers["base"].flags, [])
    check("cpc's flags come from a differently-shaped list",
          "--dump-proofs" in m.testers["cpc"].flags, True)
    names = {j.name for j in m.jobs_with_proofs()}
    check("the safe-mode job tests proofs", "ubuntu:safe-mode" in names, True)
    chain = m.completeness_chain()
    check("completeness is not named anywhere", chain[-1][1], False)
    check("every other link holds", all(ok for _, ok, _ in chain[:-1]), True)
    print(f"       {len(m.jobs)} jobs, {len(names)} run a proof tester")


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
