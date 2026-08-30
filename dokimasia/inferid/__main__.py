"""Command line for the InferenceId subtool.

    python3 -m dokimasia.inferid check    <cvc5>   # ids used in more than one place
    python3 -m dokimasia.inferid show     <cvc5> STRINGS_F_UNIFY
    python3 -m dokimasia.inferid dead     <cvc5>   # declared, never produced
    python3 -m dokimasia.inferid stats    <cvc5>
    python3 -m dokimasia.inferid baseline <cvc5> --check
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from .scan import SENTINELS, scan

CONTRACT = (
    "The contract: an InferenceId is used in one place, so that seeing it in a\n"
    "trace, a statistic or a proof identifies a unique point in the control-flow\n"
    "graph. An id with three production sites identifies three, which is to say\n"
    "it identifies none of them."
)


def _src(root: str) -> str:
    cand = os.path.join(root, "src")
    if os.path.isdir(cand):
        return cand
    if os.path.isdir(root):
        return root
    raise SystemExit(f"not a cvc5 checkout: {root!r}")


def cmd_check(args) -> int:
    m = scan(_src(args.cvc5), include_tests=args.include_tests)
    v = m.violations(strict=args.strict)
    total = len([i for i in m.declared if i not in SENTINELS])
    if args.json:
        print(json.dumps([{
            "id": i, "sites": [{"file": u.path, "line": u.line, "kind": u.kind}
                               for u in s]} for i, s in v], indent=2))
        return 1 if v else 0

    what = "uses outside the enum" if args.strict else "production sites"
    print(f"InferenceIds with more than one {what}\n")
    for ident, sites in v:
        files = {u.path for u in sites}
        span = f"{len(sites)} sites" + (f" in {len(files)} files" if len(files) > 1 else "")
        print(f"  {len(sites):>2}x  {ident:<44} {span}")
        for u in sites[: args.max_sites]:
            print(f"        {u.where()}")
        if len(sites) > args.max_sites:
            print(f"        ... {len(sites) - args.max_sites} more (--max-sites)")
    ok = total - len(v)
    print(f"\n  {ok} of {total} ids satisfy the contract "
          f"({100 * ok / total:.0f}%); {len(v)} do not.")
    sent = m.sentinel_uses()
    if sent:
        n = sum(len(s) for s in sent.values())
        names = ", ".join(f"{k} x{len(s)}" for k, s in sorted(sent.items()))
        print(f"\n  Separately: {n} inferences are emitted with a sentinel id "
              f"({names}).")
        print("  Excluded from the contract above -- they are not inferences, they")
        print("  are the absence of one -- but an anonymous inference is its own")
        print("  problem, and these are the sites no later analysis can attribute.")
    print()
    print(CONTRACT)
    return 1 if v else 0


def cmd_show(args) -> int:
    m = scan(_src(args.cvc5), include_tests=args.include_tests)
    ident = args.id.removeprefix("InferenceId::")
    if ident not in m.declared:
        print(f"no such InferenceId: {ident}", file=sys.stderr)
        return 2
    uses = m.uses.get(ident, [])
    print(f"InferenceId::{ident}\n")
    for kind in ("production", "dispatch", "comparison", "definition"):
        rows = [u for u in uses if u.kind == kind]
        if rows:
            print(f"  {kind} ({len(rows)}):")
            for u in rows:
                print(f"    {u.where()}")
    n = len([u for u in uses if u.kind == "production"])
    print()
    print(f"  {n} production site(s) — "
          + ("satisfies the contract." if n == 1 else
             "dead marker." if n == 0 else "ambiguous: the id names no single point."))
    return 0


def cmd_dead(args) -> int:
    m = scan(_src(args.cvc5), include_tests=args.include_tests)
    dead = m.unused()
    if args.json:
        print(json.dumps(dead, indent=2))
        return 0
    print(f"Declared InferenceIds that nothing produces ({len(dead)})\n")
    for ident in dead:
        kinds = {u.kind for u in m.uses.get(ident, [])}
        note = ""
        if "dispatch" in kinds:
            note = "  <- but a switch has a case for it: dead reconstruction"
        print(f"  {ident}{note}")
    print()
    print("  A declared marker nothing emits is a claim about an inference the")
    print("  solver does not make. Removing it shrinks the index that every")
    print("  later coverage analysis quantifies over.")
    return 0


def cmd_stats(args) -> int:
    m = scan(_src(args.cvc5), include_tests=args.include_tests)
    h = m.histogram(strict=args.strict)
    total = len([i for i in m.declared if i not in SENTINELS])
    if args.json:
        print(json.dumps({"declared": len(m.declared), "histogram": h}, indent=2))
        return 0
    print(f"{len(m.declared)} declared InferenceIds "
          f"({len(SENTINELS & set(m.declared))} sentinels excluded below)\n")
    for n, count in h.items():
        label = {0: "never produced", 1: "one site (contract holds)"}.get(n, f"{n} sites")
        bar = "#" * min(60, count)
        print(f"  {label:<28} {count:>4}  {bar}")
    ok = h.get(1, 0)
    print(f"\n  {ok}/{total} = {100 * ok / total:.0f}% satisfy the contract.")
    return 0


def cmd_baseline(args) -> int:
    m = scan(_src(args.cvc5))
    snap = {
        "violations": {i: len(s) for i, s in m.violations()},
        "dead": sorted(m.unused()),
    }
    path = args.file
    if args.write:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(snap, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"wrote baseline to {path}: {len(snap['violations'])} violations, "
              f"{len(snap['dead'])} dead")
        return 0
    if not os.path.exists(path):
        print(f"no baseline at {path}; run with --write first", file=sys.stderr)
        return 2
    with open(path, encoding="utf-8") as fh:
        old = json.load(fh)
    rc = 0
    ov, nv = old.get("violations", {}), snap["violations"]
    worse = {i: (ov.get(i, 0), n) for i, n in nv.items() if n > ov.get(i, 0)}
    fixed = sorted(set(ov) - set(nv))
    for i, (was, now) in sorted(worse.items()):
        print(f"  + {i}: {was} -> {now} production sites")
        rc = 1
    for i in fixed:
        print(f"  - {i}: now satisfies the contract")
    newdead = sorted(set(snap["dead"]) - set(old.get("dead", [])))
    for i in newdead:
        print(f"  + {i}: declared but nothing produces it")
        rc = 1
    if rc:
        print("\nAn InferenceId became more ambiguous, or a new dead marker appeared.")
        print("If that is intended, update the baseline in the same commit.")
    else:
        print(f"OK: {len(nv)} violations, {len(snap['dead'])} dead — none worse.")
    return rc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -m dokimasia.inferid",
        description="Enforce that an InferenceId names exactly one program point.")
    ap.add_argument("--include-tests", action="store_true",
                    help="also scan test/ (off by default: src/ is the product)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="ids used in more than one place")
    c.add_argument("cvc5")
    c.add_argument("--strict", action="store_true",
                   help="count every use outside the enum, not just production sites")
    c.add_argument("--max-sites", type=int, default=8)
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_check)

    s = sub.add_parser("show", help="every site of one id")
    s.add_argument("cvc5")
    s.add_argument("id")
    s.set_defaults(func=cmd_show)

    d = sub.add_parser("dead", help="declared but never produced")
    d.add_argument("cvc5")
    d.add_argument("--json", action="store_true")
    d.set_defaults(func=cmd_dead)

    t = sub.add_parser("stats", help="the distribution")
    t.add_argument("cvc5")
    t.add_argument("--strict", action="store_true")
    t.add_argument("--json", action="store_true")
    t.set_defaults(func=cmd_stats)

    b = sub.add_parser("baseline", help="ratchet violations and dead markers")
    b.add_argument("cvc5")
    b.add_argument("--file", default="inferid-baseline.json")
    b.add_argument("--write", action="store_true")
    b.add_argument("--check", action="store_true")
    b.set_defaults(func=cmd_baseline)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
