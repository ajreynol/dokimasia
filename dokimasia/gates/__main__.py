"""Command line for the option-gate analysis.

    python3 -m dokimasia.gates kinds    <cvc5>   # Kind -> option that legalises it
    python3 -m dokimasia.gates rule     <cvc5> LAMBDA_ELIM
    python3 -m dokimasia.gates verdicts <cvc5>   # every rewrite rule, in safe mode
"""

from __future__ import annotations

import argparse
import json
import sys

from .gates import SAFE_MODE_DISABLES, scan

CAVEAT = (
    "note: a kind gate is evidence, not proof. A kind can be introduced\n"
    "      internally rather than parsed from input, and an arm naming no kind\n"
    "      gets no verdict. 'partial' means the arm's kinds are a mix -- if the\n"
    "      arm conjoins them it is blocked, if it offers them as alternatives it\n"
    "      is not. Read the arm before filing either way."
)


def cmd_kinds(args) -> int:
    kg = scan(args.cvc5)
    rows = sorted((k, sorted(v), kg.origin.get(k, "-")) for k, v in kg.kind_gate.items())
    if args.json:
        print(json.dumps([{"kind": k, "options": o, "origin": src} for k, o, src in rows],
                         indent=2))
        return 0
    print(f"{len(rows)} term kinds carry an option gate\n")
    for k, opts, src in rows:
        safe = [o for o in opts if o in SAFE_MODE_DISABLES]
        mark = "safe-mode blocks" if safe else "                "
        print(f"  {k:<26} needs {', '.join('--' + o for o in opts):<24} {mark}  {src}")
    print()
    print("  Sources: smt/illegal_checker.cpp, and the LogicException guards")
    print("  theories throw from ppRewrite. Both are hand-maintained tables.")
    return 0


def cmd_rule(args) -> int:
    kg = scan(args.cvc5)
    name = args.rule.removeprefix("ProofRewriteRule::")
    kinds = kg.rule_kinds.get(name)
    if kinds is None:
        print(f"no rewriteViaRule arm found for {name}", file=sys.stderr)
        return 2
    v, why = kg.verdict(name)
    print(f"ProofRewriteRule::{name}\n")
    print(f"  kinds named by its arm: {', '.join(sorted(kinds))}")
    for k in sorted(kinds):
        opts = sorted(kg.kind_gate.get(k, []))
        print(f"    Kind::{k:<22} {'needs ' + ', '.join('--' + o for o in opts) if opts else 'no gate found'}")
    print(f"\n  safe mode: {v.upper()} — {why}")
    return 0


def cmd_verdicts(args) -> int:
    kg = scan(args.cvc5)
    rows = [(r, *kg.verdict(r)) for r in sorted(kg.rule_kinds)]
    if args.only:
        rows = [r for r in rows if r[1] == args.only]
    if args.json:
        print(json.dumps([{"rule": r, "verdict": v, "why": w} for r, v, w in rows],
                         indent=2))
        return 0
    from collections import Counter
    counts = Counter(v for _, v, _ in rows)
    print(f"{len(rows)} rewrite rules whose arm names a term kind\n")
    for v in ("blocked", "partial", "open"):
        if counts.get(v):
            print(f"  {counts[v]:>3}  {v}")
    print()
    for r, v, w in rows:
        if v != "open" or args.only:
            print(f"  {v:<8} {r:<34} {w}")
    print()
    print(CAVEAT)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -m dokimasia.gates",
        description="Which option must be on for a term kind, and so a rule, to occur.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    k = sub.add_parser("kinds", help="Kind -> option that legalises it")
    k.add_argument("cvc5"); k.add_argument("--json", action="store_true")
    k.set_defaults(func=cmd_kinds)
    r = sub.add_parser("rule", help="one rewrite rule's gate")
    r.add_argument("cvc5"); r.add_argument("rule")
    r.set_defaults(func=cmd_rule)
    v = sub.add_parser("verdicts", help="safe-mode verdict per rule")
    v.add_argument("cvc5")
    v.add_argument("--only", choices=("blocked", "partial", "open"))
    v.add_argument("--json", action="store_true")
    v.set_defaults(func=cmd_verdicts)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
