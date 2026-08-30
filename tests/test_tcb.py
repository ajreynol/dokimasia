"""Tests for the TCB subtool.

Run: python3 tests/test_tcb.py [<cvc5>]

The synthetic tests need nothing. If a cvc5 checkout is given (or CVC5 is set),
the tree tests also run and guard the numbers in docs/findings/tcb-001.md.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dokimasia.tcb.closure import Closure, IncludeGraph  # noqa: E402

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}" + ("" if ok else f" != {want!r}"))
    if not ok:
        FAILURES.append(label)


def write_tree(root, files):
    for rel, text in files.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)


def test_synthetic():
    print("synthetic tree:")
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "src")
        write_tree(src, {
            "a/checker.cpp": '#include "a/checker.h"\n#include "b/solver.h"\n',
            "a/checker.h": "x\n",
            "b/solver.h": '#include "c/deep.h"\n',
            "b/solver.cpp": '#include "d/unrelated.h"\n',
            "c/deep.h": "y\n",
            "d/unrelated.h": "z\n",
        })
        g = IncludeGraph.build(src)
        c = Closure.compute(g, ["a/checker.cpp"], "headers")
        check("headers closure follows headers only",
              sorted(c.files), ["a/checker.cpp", "a/checker.h", "b/solver.h", "c/deep.h"])
        check("headers mode excludes solver.cpp", "b/solver.cpp" in c.files, False)

        e = Closure.compute(g, ["a/checker.cpp"], "exec")
        check("exec mode pulls the .cpp and its deps (why it saturates)",
              "d/unrelated.h" in e.files, True)

        cut = Closure.compute(g, ["a/checker.cpp"], "headers",
                              skip_edge=("a/checker.cpp", "b/solver.h"))
        check("cutting the solver edge drops its closure",
              sorted(cut.files), ["a/checker.cpp", "a/checker.h"])

        path = c.path_to("c/deep.h")
        check("path_to explains why a file is in the closure",
              path, ["a/checker.cpp", "b/solver.h", "c/deep.h"])

        sub = Closure.compute(g, ["a/checker.cpp"], "headers", skip_prefix="b/")
        check("subsystem cut removes everything behind it",
              sorted(sub.files), ["a/checker.cpp", "a/checker.h"])


def test_cvc5(root):
    print(f"cvc5 tree at {root}:")
    from dokimasia.tcb.closure import SEED_SETS, resolve_src
    import glob
    src = resolve_src(root)
    g = IncludeGraph.build(src)
    seeds = []
    for pat in SEED_SETS["proof-checker"]:
        seeds += [os.path.relpath(h, src) for h in sorted(glob.glob(os.path.join(src, pat)))]
    check("13 theory rule checkers plus the dispatcher are seeded", len(seeds) >= 15, True)

    clo = Closure.compute(g, seeds, "headers")
    print(f"       closure: {len(clo.files)} files, {clo.loc:,} lines")
    check("solver headers are in the checker closure (tcb-001)",
          [h for h in ("theory/strings/core_solver.h", "theory/rewriter.h",
                       "theory/theory.h") if h in clo.files],
          ["theory/strings/core_solver.h", "theory/rewriter.h", "theory/theory.h"])
    check("the solver engine is NOT reachable at compile time",
          "smt/solver_engine.h" in clo.files, False)

    env = Closure.compute(g, ["smt/env.h"], "headers")
    core = Closure.compute(g, ["theory/strings/core_solver.h"], "headers")
    check("Env is lighter than one theory solver header", env.loc < core.loc, True)

    # The negative result that made us change the default mode.
    a = Closure.compute(g, ["printer/printer.cpp"], "exec")
    b = Closure.compute(g, ["proof/proof_rule_checker.cpp"], "exec")
    check("exec mode saturates: unrelated seeds give the same closure",
          a.loc == b.loc, True)


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
        print(f"FAILED: {len(FAILURES)} check(s): {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
