"""static inventory − what the corpus reached = the latent set."""
from __future__ import annotations

import argparse
import json
import sys

from .latent import CENSUS, State, scan

_ORDER = (State.SAFE, State.LATENT, State.OPEN)
_LABEL = {
    State.SAFE: ("rank 1", "reached under --safe-mode=safe — a contract violation"),
    State.LATENT: ("rank 2", "declared, and no input we have run has reached it"),
    State.OPEN: ("rank 3", "reached, but only outside safe mode"),
}


def _warn(l) -> None:
    if not l.have_census:
        print(f"  !! no {CENSUS} found — every hole is reported latent by default,\n"
              f"     which is a fact about the missing census, not about cvc5.\n"
              f"     Produce one with scripts/sweep_corpus.\n")


def cmd_census(args) -> int:
    l = scan(args.cvc5)
    if args.json:
        print(json.dumps({s: [h.name for h in l.by_state(s)] for s in _ORDER}, indent=2))
        return 0
    print("static hole inventory  −  what the corpus reached  =  the latent set\n")
    _warn(l)
    kinds = l.by_kind()
    width = max(len(k) for k in kinds)
    print(f"  {'':<{width}}  {'safe':>6} {'latent':>7} {'unres':>6}   total")
    for k in sorted(kinds):
        d = kinds[k]
        tot = sum(d.values())
        print(f"  {k:<{width}}  {d.get(State.SAFE,0):>6} {d.get(State.LATENT,0):>7} "
              f"{d.get(State.OPEN,0):>6}   {tot:>5}")
    tot = {s: len(l.by_state(s)) for s in _ORDER}
    print(f"  {'':<{width}}  {'-'*6} {'-'*7} {'-'*6}   {'-'*5}")
    print(f"  {'all':<{width}}  {tot[State.SAFE]:>6} {tot[State.LATENT]:>7} "
          f"{tot[State.OPEN]:>6}   {sum(tot.values()):>5}\n")
    for s in _ORDER:
        rank, why = _LABEL[s]
        print(f"  {rank}  {len(l.by_state(s)):>4}  {why}")
    print(f"\n  Corpus: {l.corpus}. **Latent is not unreachable.** It is the absence")
    print("  of evidence either way, and it is the only population cvc5's runtime")
    print("  oracle cannot see: that oracle fires when an input reaches a step.")
    if tot[State.SAFE] == 0:
        print("\n  No hole was reached in safe mode. That is a fact about this corpus.")
    return 0


def cmd_list(args) -> int:
    l = scan(args.cvc5)
    _warn(l)
    holes = [h for h in l.by_state(args.state)
             if not args.kind or h.kind == args.kind]
    if args.json:
        print(json.dumps([{"kind": h.kind, "name": h.name, "hits": h.hits,
                           "detail": h.detail} for h in holes], indent=2))
        return 0
    rank, why = _LABEL[args.state]
    print(f"{len(holes)} {args.state} — {why}\n")
    for h in holes:
        hits = f"  ({h.hits} hit{'s' if h.hits != 1 else ''})" if h.hits else ""
        print(f"  {h.kind:<10} {h.name}{hits}")
        if h.detail:
            print(f"             {h.detail}")
    if args.state == State.LATENT and holes:
        print("\n  Each of these needs one of two things, and either shrinks the problem:")
        print("    · an input that reaches it   → it becomes a finding")
        print("    · an argument that nothing can → it leaves the inventory")
        print("  A hole that resists both is the most interesting object here.")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -m dokimasia.latent",
        description="The holes no input we have run has ever reached.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("census", help="the three-way split")
    p.add_argument("cvc5")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_census)
    p = sub.add_parser("list", help="the worklist")
    p.add_argument("cvc5")
    p.add_argument("--state", default=State.LATENT, choices=list(_ORDER))
    p.add_argument("--kind", default="",
                   choices=["", "trust-id", "seam-rule", "rewrite", "inference"])
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_list)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
