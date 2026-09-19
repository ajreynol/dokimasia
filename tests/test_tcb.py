"""Tests for the TCB subtool.

Run: python3 tests/test_tcb.py [<cvc5>]

The synthetic tests need nothing. If a cvc5 checkout is given (or CVC5 is set),
the tree tests also run and guard the numbers in docs/experience.md.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dokimasia_analyzer.tcb.closure import Closure, IncludeGraph  # noqa: E402

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


def test_edge_use():
    """Used, unused and unknown -- and every false verdict this once gave.

    Each case below is a bug that shipped or nearly shipped while building
    this. `tcb-001` told cvc5 that six checkers included their solvers to reach
    static helpers; for two of the edges the include was simply dead, and the
    refactoring we proposed was unnecessary. The classifier that fixes that is
    only worth having if it does not make the mirror mistake, so the mirror
    mistakes are the tests.
    """
    print("\nedge use:")
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "src")
        write_tree(src, {
            # A solver header whose helper the checker really calls.
            "b/solver.h": "#ifndef CVC5__B__SOLVER_H\n#define CVC5__B__SOLVER_H\n"
                          "class CoreSolver {\n static Node getConclusion();\n};\n#endif\n",
            "a/uses.cpp": '#include "b/solver.h"\nNode f() { return CoreSolver::getConclusion(); }\n',
            # The tcb-001 case: included, and nothing from it referenced.
            "a/dead.cpp": '#include "b/solver.h"\nint f() { return 1; }\n',
            # A comment naming the header is not a use.
            "a/comment.cpp": '#include "b/solver.h"\n// CoreSolver used to be called here\nint f() { return 1; }\n',
            # Only an include guard: nothing is declared, so nothing is known.
            "b/guard_only.h": "#ifndef CVC5__B__GUARD_ONLY_H\n#define CVC5__B__GUARD_ONLY_H\n#endif\n",
            "a/guard.cpp": '#include "b/guard_only.h"\nint f() { return 1; }\n',
            # Free functions in a namespace, reached as utils::mkConcat.
            "b/utils.h": "#ifndef CVC5__B__UTILS_H\n#define CVC5__B__UTILS_H\n"
                         "namespace utils {\nNode mkConcat(Node a);\n}\n#endif\n",
            "a/ns.cpp": '#include "b/utils.h"\nNode f() { return utils::mkConcat(x); }\n',
            # A forward declaration is a name the header does not supply.
            "b/fwd.h": "#ifndef CVC5__B__FWD_H\n#define CVC5__B__FWD_H\n"
                       "class Rewriter;\nclass ExtendedRewriter {\n int x;\n};\n#endif\n",
            "a/fwd_user.cpp": '#include "b/fwd.h"\nvoid f(Rewriter* r) {}\n',
        })
        g = IncludeGraph.build(src)
        check("a called helper is used", g.edge_use("a/uses.cpp", "b/solver.h"), "used")
        check("an include referencing nothing is unused",
              g.edge_use("a/dead.cpp", "b/solver.h"), "unused")
        check("a mention in a comment is not a use",
              g.edge_use("a/comment.cpp", "b/solver.h"), "unused")
        # The include guard is a #define, and counting it as a declaration
        # turned "we cannot tell" into a confident "dead" for every guarded
        # header -- which is three false positives on cvc5 alone.
        check("a header declaring only its guard is unknown, never unused",
              g.edge_use("a/guard.cpp", "b/guard_only.h"), "unknown")
        # A utility header is often nothing but free functions in a namespace.
        # Matching classes alone called every one of them dead.
        check("free functions behind a namespace count as declarations",
              g.edge_use("a/ns.cpp", "b/utils.h"), "used")
        # `class Rewriter;` announces a name this header does not define, so a
        # file that says `Rewriter` is not thereby using this header.
        check("a forward declaration does not make the edge used",
              g.edge_use("a/fwd_user.cpp", "b/fwd.h"), "unused")


def test_cvc5(root):
    print(f"cvc5 tree at {root}:")
    from dokimasia_analyzer.tcb.closure import SEED_SETS, resolve_src
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

    # The edges cvc5 replied about, pinned by name. `tcb-001` claimed all six
    # checker->solver edges existed to reach static helpers; cvc5 answered that
    # two were dead includes and removed them in one line each. Whichever way
    # the classifier drifts, one of these fails.
    check("the strings edge is a real dependency, as cvc5 agreed",
          g.edge_use("theory/strings/proof_checker.cpp",
                     "theory/strings/core_solver.h"), "used")
    check("the arith edge was a dead include, as cvc5 reported",
          g.edge_use("theory/arith/proof_checker.cpp",
                     "theory/arith/linear/constraint.h"), "unused")
    check("the datatypes rewriter edge was a dead include too",
          g.edge_use("theory/datatypes/proof_checker.cpp",
                     "theory/rewriter.h"), "unused")
    # A checker plainly uses the node it is checking; a classifier that calls
    # this dead has inverted the error rather than fixed it.
    check("a header the file obviously uses is never called dead",
          g.edge_use("proof/proof_checker.h", "expr/node.h"), "used")

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
    test_edge_use()
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
