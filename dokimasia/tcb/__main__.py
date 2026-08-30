"""Command line for the TCB subtool.

    python3 -m dokimasia.tcb measure  <cvc5>   # the headline numbers
    python3 -m dokimasia.tcb cuts     <cvc5>   # which edges carry the weight
    python3 -m dokimasia.tcb baseline <cvc5>   # write or check a ratchet
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from .closure import SEED_SETS, Closure, IncludeGraph, resolve_src

CAVEAT = (
    "note: this is the transitive #include closure -- the surface the checker\n"
    "      compiles against. It is not proof that the code runs during checking;\n"
    "      that is a call-graph question and needs a build. Generated headers\n"
    "      (options/options.h) are not in the source tree, so this is a lower\n"
    "      bound in that respect."
)

EXEC_WARNING = (
    "WARNING: --mode exec saturates and does not discriminate. Seeding from an\n"
    "         unrelated file (printer/printer.cpp) gives the same closure as\n"
    "         seeding from the proof checker. Use the default 'headers' mode.\n"
    "         See dokimasia/tcb/closure.py for the measurement.\n"
)


def _closure(args) -> tuple[IncludeGraph, Closure]:
    if getattr(args, "mode", "headers") == "exec":
        print(EXEC_WARNING, file=sys.stderr)
    src = resolve_src(args.cvc5)
    graph = IncludeGraph.build(src)
    seeds: list[str] = []
    patterns = SEED_SETS.get(args.seeds)
    if patterns is None:
        raise SystemExit(
            f"unknown seed set {args.seeds!r}; known: {', '.join(SEED_SETS)}"
        )
    import glob as _glob

    for pat in patterns:
        for hit in sorted(_glob.glob(os.path.join(src, pat))):
            seeds.append(os.path.relpath(hit, src))
    if not seeds:
        raise SystemExit(f"seed set {args.seeds!r} matched no files under {src}")
    return graph, Closure.compute(graph, seeds, mode=args.mode)


def _stats(graph: IncludeGraph, clo: Closure) -> dict:
    total_files = len(graph.all_files)
    total_loc = graph.loc(graph.all_files)
    return {
        "seed_set": None,
        "mode": clo.mode,
        "seed_files": len(clo.seeds),
        "tcb_files": len(clo.files),
        "tcb_lines": clo.loc,
        "src_files": total_files,
        "src_lines": total_loc,
        "pct_files": round(100 * len(clo.files) / total_files, 1),
        "pct_lines": round(100 * clo.loc / total_loc, 1),
    }


def cmd_measure(args) -> int:
    graph, clo = _closure(args)
    st = _stats(graph, clo)
    st["seed_set"] = args.seeds
    if args.json:
        print(json.dumps(st, indent=2))
        return 0

    print(f"TCB of '{args.seeds}' ({clo.mode} mode)")
    print(f"  seeds        {st['seed_files']:>6} files")
    print(f"  closure      {st['tcb_files']:>6} files   {st['tcb_lines']:>9,} lines")
    print(f"  all of src/  {st['src_files']:>6} files   {st['src_lines']:>9,} lines")
    print(f"  the checker depends on {st['pct_lines']}% of cvc5 by line count")
    print()
    print("  by subsystem (heaviest first):")
    for name, nf, nl in clo.by_subsystem(1)[:10]:
        print(f"    {name:<18} {nf:>5} files  {nl:>9,} lines")
    theory = [r for r in clo.by_subsystem(2) if r[0].startswith("theory/")]
    if theory:
        print()
        print(f"  theory subsystems inside the TCB: {len(theory)}")
        for name, nf, nl in theory[:10]:
            print(f"    {name:<24} {nf:>5} files  {nl:>9,} lines")
    print()
    print(CAVEAT)
    return 0


def cmd_cuts(args) -> int:
    graph, clo = _closure(args)
    subs = clo.subsystem_cuts(depth=args.depth)
    edges = clo.cuts(limit=args.limit)
    if args.json:
        print(json.dumps({
            "subsystem_cuts": [
                {"subsystem": a, "files": b, "lines": c} for a, b, c in subs
            ],
            "edge_cuts": [
                {"from": a, "include": b, "files": c, "lines": d}
                for a, b, c, d in edges
            ],
        }, indent=2))
        return 0

    print(f"Cut analysis for '{args.seeds}' ({clo.mode} mode)")
    print()
    print("SUBSYSTEM CUTS -- if the checker did not reach into this at all:")
    print()
    for name, nf, nl in subs[: args.limit]:
        pct = 100 * nl / clo.loc if clo.loc else 0
        print(f"  -{nl:>8,} lines  ({pct:>4.1f}% of TCB)  {nf:>5} files   {name}")
    print()

    heaviest = edges[0][3] if edges else 0
    print("SINGLE-EDGE CUTS -- what one #include is uniquely worth:")
    print()
    for frm, inc, nf, nl in edges[:5]:
        print(f"  -{nl:>8,} lines  {nf:>5} files   {frm}")
        print(f"  {'':>10}        {'':>5}    -> #include \"{inc}\"")
    print()
    if heaviest < 0.02 * clo.loc:
        print(f"  The heaviest single edge is worth {heaviest:,} lines, under 2% of")
        print("  the TCB. That is the real finding: the include graph is dense,")
        print("  so no one bad #include explains the size and no one-line fix")
        print("  shrinks it. Reducing this TCB means severing a subsystem")
        print("  relationship above, not deleting an include.")
    return 0


def cmd_why(args) -> int:
    graph, clo = _closure(args)
    if args.target not in clo.files:
        print(f"{args.target} is not in the '{args.seeds}' closure", file=sys.stderr)
        return 2
    path = clo.path_to(args.target)
    if path is None:
        print(f"no path found to {args.target}", file=sys.stderr)
        return 2
    print(f"Why '{args.target}' is in the '{args.seeds}' TCB:")
    print()
    for i, node in enumerate(path):
        lead = "  " if i == 0 else "    " * 1 + "-> "
        print(f"  {lead}{node}")
    print()
    print(f"  {len(path) - 1} include hop(s) from a proof checker.")
    return 0


def cmd_baseline(args) -> int:
    graph, clo = _closure(args)
    st = _stats(graph, clo)
    st["seed_set"] = args.seeds
    path = args.file
    if args.write and args.check:
        raise SystemExit("--write and --check are mutually exclusive")
    if args.write:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(st, fh, indent=2)
            fh.write("\n")
        print(f"wrote baseline to {path}: {st['tcb_files']} files, "
              f"{st['tcb_lines']:,} lines")
        return 0

    if not os.path.exists(path):
        print(f"no baseline at {path}; run with --write first", file=sys.stderr)
        return 2
    with open(path, encoding="utf-8") as fh:
        old = json.load(fh)
    d_files = st["tcb_files"] - old["tcb_files"]
    d_lines = st["tcb_lines"] - old["tcb_lines"]
    print(f"baseline {old['tcb_files']} files / {old['tcb_lines']:,} lines")
    print(f"current  {st['tcb_files']} files / {st['tcb_lines']:,} lines")
    print(f"delta    {d_files:+d} files / {d_lines:+,} lines")
    if d_lines > args.tolerance:
        print()
        print(f"FAIL: the proof checker's TCB grew by {d_lines:,} lines "
              f"(tolerance {args.tolerance:,}).")
        print("The ratchet only turns one way. If this growth is intended,")
        print("update the baseline in the same commit and say why.")
        return 1
    print()
    print("OK: the TCB did not grow.")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -m dokimasia.tcb",
        description="Measure the trusted computing base of cvc5's internal "
                    "proof checker.",
    )
    ap.add_argument("--seeds", default="proof-checker",
                    help=f"seed set: {', '.join(SEED_SETS)} (default: %(default)s)")
    ap.add_argument("--mode", default="headers", choices=("headers", "exec"),
                    help="headers is the compile-time surface and the only "
                         "mode that discriminates; exec saturates and is kept "
                         "only for reproducibility (default: %(default)s)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("measure", help="the headline numbers")
    m.add_argument("cvc5")
    m.add_argument("--json", action="store_true")
    m.set_defaults(func=cmd_measure)

    c = sub.add_parser("cuts", help="what would shrink the TCB")
    c.add_argument("cvc5")
    c.add_argument("--limit", type=int, default=12)
    c.add_argument("--depth", type=int, default=2,
                   help="path depth for subsystem grouping (default: %(default)s)")
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_cuts)

    w = sub.add_parser("why", help="shortest include path from a checker to a file")
    w.add_argument("cvc5")
    w.add_argument("target", help="src-relative path, e.g. theory/rewriter.h")
    w.set_defaults(func=cmd_why)

    b = sub.add_parser("baseline", help="write or check a TCB ratchet")
    b.add_argument("cvc5")
    b.add_argument("--file", default="tcb-baseline.json")
    b.add_argument("--write", action="store_true",
                   help="write the baseline instead of checking it")
    b.add_argument("--check", action="store_true",
                   help="check against the baseline (the default; explicit for CI)")
    b.add_argument("--tolerance", type=int, default=0,
                   help="lines of growth to allow (default: %(default)s)")
    b.set_defaults(func=cmd_baseline)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
