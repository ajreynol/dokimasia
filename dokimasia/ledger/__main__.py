"""Command line for the proof-rule ledger.

    python3 -m dokimasia.ledger holes    <cvc5>   # rows with a hole
    python3 -m dokimasia.ledger table    <cvc5>   # every rule, four columns
    python3 -m dokimasia.ledger rule     <cvc5> TRUST
    python3 -m dokimasia.ledger baseline <cvc5> --check
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from .build import build

CODES = {
    "RULE0001": "no registered checker",
    "RULE0002": "checker registered as trusted (does not fully check)",
    "RULE0003": "declared, and nothing produces it",
    "ELAB0001": "a macro nothing expands",
    "SEAM0001": "emitted by the solver, and the Eunoia seam cannot print it",
}

SEVERITY_NOTE = (
    "Severity needs the option gate, which this tool does not compute. Checked\n"
    "by hand at 16c4001e53: every ARITH_TRANS_* and ARITH_POW2_* rule is behind\n"
    "`--arith-exp`, and its kinds are rejected outright by illegal_checker when\n"
    "that is off -- which safe mode sets. So those gaps are unrestricted-mode\n"
    "gaps, not safe-mode contract violations."
)


def cmd_holes(args) -> int:
    L = build(args.cvc5)
    if args.json:
        print(json.dumps({c: [r.name for r in L.with_hole(c)] for c in CODES}, indent=2))
        return 0
    u = L.unprintable()
    print(f"{len(L.rules)} ProofRules, {len(L.rewrite_rules)} ProofRewriteRules\n")

    print("PRINTED — will the Eunoia seam accept it?")
    from collections import Counter
    c = Counter(r.printed for r in L.rows())
    print(f"  always {c['always']}   conditional {c['conditional']}   never {c['never']}")
    print(f"  of the {c['never']} it never accepts:")
    print(f"    {len(u['by-design']):>3}  by design — a macro or trust step, gone or "
          f"intended before printing")
    print(f"    {len(u['unreachable']):>3}  unreachable — nothing produces them")
    print(f"    {len(u['gap']):>3}  REAL GAPS — the solver emits them, the seam cannot take them")
    for r in sorted(u["gap"], key=lambda r: r.name):
        ped = f"  [trusted checker, level {r.pedantic}]" if r.pedantic else ""
        print(f"         {r.name:<36} {len(r.produced)} site(s){ped}")
    print()
    print(SEVERITY_NOTE)

    print("\nCHECKED")
    for code in ("RULE0001", "RULE0002"):
        rows = L.with_hole(code)
        print(f"  {code} {CODES[code]}: {len(rows)}")
        for r in sorted(rows, key=lambda r: r.name)[: args.limit]:
            extra = f" (level {r.pedantic})" if r.pedantic else ""
            prod = "produced" if r.produced else "not produced"
            print(f"    {r.name:<36} {prod}{extra}")
        if len(rows) > args.limit:
            print(f"    ... {len(rows) - args.limit} more")

    print("\nPRODUCED / ELABORATED")
    for code in ("RULE0003", "ELAB0001"):
        rows = L.with_hole(code)
        print(f"  {code} {CODES[code]}: {len(rows)}")
        for r in sorted(rows, key=lambda r: r.name)[: args.limit]:
            print(f"    {r.name}")
        if len(rows) > args.limit:
            print(f"    ... {len(rows) - args.limit} more")
    return 1 if u["gap"] else 0


def cmd_table(args) -> int:
    L = build(args.cvc5)
    rows = sorted(L.rows(), key=lambda r: r.name)
    if args.produced_only:
        rows = [r for r in rows if r.produced]
    if args.json:
        print(json.dumps([{
            "rule": r.name, "produced": len(r.produced),
            "checker": r.checker, "pedantic": r.pedantic,
            "elaborated": len(r.elaborated), "printed": r.printed,
            "holes": r.holes,
        } for r in rows], indent=2))
        return 0
    print(f"{'rule':<40}{'prod':>5}{'checked':>10}{'elab':>6}  printed")
    for r in rows:
        chk = "-" if r.checker is None else (f"trust:{r.pedantic}" if r.pedantic else "yes")
        print(f"  {r.name:<38}{len(r.produced):>5}{chk:>10}{len(r.elaborated):>6}  {r.printed}")
    return 0


def cmd_rule(args) -> int:
    L = build(args.cvc5)
    name = args.rule.removeprefix("ProofRule::")
    if name not in L.rules:
        print(f"no such ProofRule: {name}", file=sys.stderr)
        return 2
    r = L.rules[name]
    print(f"ProofRule::{r.name}\n")
    print(f"  produced    {len(r.produced)} site(s)")
    for w in r.produced[: args.limit]:
        print(f"                {w}")
    if len(r.produced) > args.limit:
        print(f"                ... {len(r.produced) - args.limit} more")
    if r.checker:
        lvl = f"  (trusted, pedantic level {r.pedantic})" if r.pedantic else "  (fully checked)"
        print(f"  checked     {r.checker}{lvl}")
    else:
        print("  checked     no registered checker")
    print(f"  elaborated  {len(r.elaborated)} site(s)"
          + (f" — e.g. {r.elaborated[0]}" if r.elaborated else ""))
    kind = r.unprintable_kind
    print(f"  printed     {r.printed}" + (f"  ({kind})" if kind else ""))
    if r.holes:
        print(f"\n  holes: {', '.join(r.holes)}")
        for h in r.holes:
            print(f"    {h}  {CODES[h]}")
    return 0


def cmd_baseline(args) -> int:
    L = build(args.cvc5)
    snap = {c: sorted(r.name for r in L.with_hole(c)) for c in CODES}
    path = args.file
    if args.write:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(snap, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"wrote baseline to {path}: "
              + ", ".join(f"{c} {len(v)}" for c, v in snap.items()))
        return 0
    if not os.path.exists(path):
        print(f"no baseline at {path}; run with --write first", file=sys.stderr)
        return 2
    with open(path, encoding="utf-8") as fh:
        old = json.load(fh)
    rc = 0
    for c in CODES:
        was, now = set(old.get(c, [])), set(snap[c])
        for a in sorted(now - was):
            print(f"  + {c} {a}  ({CODES[c]})")
            rc = 1
        for r in sorted(was - now):
            print(f"  - {c} {r}  (fixed)")
    print()
    if rc:
        print("A proof rule gained a hole. If that is intended, update the")
        print("baseline in the same commit and say why.")
    else:
        print("OK: no rule gained a hole.")
    return rc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -m dokimasia.ledger",
        description="One row per ProofRule: produced, checked, elaborated, printed.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    h = sub.add_parser("holes", help="rules with a hole in some column")
    h.add_argument("cvc5")
    h.add_argument("--limit", type=int, default=12)
    h.add_argument("--json", action="store_true")
    h.set_defaults(func=cmd_holes)

    t = sub.add_parser("table", help="every rule, four columns")
    t.add_argument("cvc5")
    t.add_argument("--produced-only", action="store_true")
    t.add_argument("--json", action="store_true")
    t.set_defaults(func=cmd_table)

    r = sub.add_parser("rule", help="one rule, in full")
    r.add_argument("cvc5")
    r.add_argument("rule")
    r.add_argument("--limit", type=int, default=10)
    r.set_defaults(func=cmd_rule)

    b = sub.add_parser("baseline", help="ratchet the holes")
    b.add_argument("cvc5")
    b.add_argument("--file", default="ledger-baseline.json")
    b.add_argument("--write", action="store_true")
    b.add_argument("--check", action="store_true")
    b.set_defaults(func=cmd_baseline)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
