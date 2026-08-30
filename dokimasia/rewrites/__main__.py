"""Command line for rewrite-rule coverage.

    python3 -m dokimasia.rewrites coverage <cvc5>   # the four-way split
    python3 -m dokimasia.rewrites gaps     <cvc5>   # applied, and unprintable
    python3 -m dokimasia.rewrites baseline <cvc5> --check
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from .scan import scan


def cmd_coverage(args) -> int:
    r = scan(args.cvc5)
    if args.json:
        print(json.dumps({
            "declared": len(r.declared), "rare": len(r.rare),
            "handwritten": len(r.handwritten), "implemented": len(r.implemented),
            "seam_handles": len(r.handled), "gaps": r.gaps(),
            "hard_gaps": r.hard_gaps(), "safe_mode_gaps": r.safe_mode_gaps(),
        }, indent=2))
        return 0
    print(f"{len(r.declared)} ProofRewriteRules\n")
    print(f"  {len(r.rare):>4}  defined in RARE files — declarative, so the same")
    print(f"        definition drives cvc5 and the signature; handled generically")
    print(f"  {len(r.handwritten):>4}  hand-written C++ the seam must be taught one at a time")
    print(f"  {len(r.implemented):>4}  implemented in some rewriteViaRule — i.e. applicable")
    print(f"  {len(r.handled):>4}  accepted by isHandledTheoryRewrite")
    dr = r.rare_without_enum()
    if dr:
        print(f"\n  {len(dr)} RARE names match no enum entry: {', '.join(dr[:6])}")
    print(f"\n  {len(r.declared_only()):>4}  declared, not RARE, and no rewriter implements them")
    print(f"        — dead vocabulary, or applied by a route this does not model")
    return 0


def cmd_gaps(args) -> int:
    r = scan(args.cvc5)
    hard, macro, smg = r.hard_gaps(), r.macro_gaps(), r.safe_mode_gaps()
    if args.json:
        print(json.dumps({"hard": hard, "macro": macro, "safe_mode": smg}, indent=2))
        return 1 if (hard or smg) else 0

    print("Rules a rewriter applies and the Eunoia seam will not print\n")
    print(f"  {len(hard)} hard gaps — no macro to expand, nothing else to try:")
    for n in hard:
        print(f"    {n:<32} {r.implemented[n]}")
    print(f"\n  {len(macro)} macro gaps — expected to be elaborated first, but that")
    print("  elaboration runs under a search budget (--proof-rewrite-rcons-rec-limit),")
    print("  and when it fails the macro step stays. Conditional, not benign:")
    for k, v in r.by_theory(macro).items():
        print(f"    {k:<20} {v}")
    if smg:
        print(f"\n  {len(smg)} SAFE-MODE gaps — the seam accepts these *only* when")
        print("  safeMode == UNRESTRICTED, so safe mode is stricter at the seam than")
        print("  the default. If a rewriter applies one under --safe-mode=safe, the")
        print("  step cannot be printed:")
        for n in smg:
            print(f"    {n:<32} {r.implemented[n]}")
        print("\n  Whether a rewriter can apply them in safe mode needs the option")
        print("  gate, which this tool does not compute. Confirm before filing.")
    return 1 if (hard or smg) else 0


def cmd_baseline(args) -> int:
    r = scan(args.cvc5)
    snap = {"hard_gaps": sorted(r.hard_gaps()),
            "safe_mode_gaps": sorted(r.safe_mode_gaps()),
            "macro_gap_count": len(r.macro_gaps()),
            "seam_handles": len(r.handled)}
    path = args.file
    if args.write:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(snap, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"wrote baseline to {path}: {len(snap['hard_gaps'])} hard, "
              f"{len(snap['safe_mode_gaps'])} safe-mode, "
              f"{snap['macro_gap_count']} macro gaps")
        return 0
    if not os.path.exists(path):
        print(f"no baseline at {path}; run with --write first", file=sys.stderr)
        return 2
    with open(path, encoding="utf-8") as fh:
        old = json.load(fh)
    rc = 0
    for key in ("hard_gaps", "safe_mode_gaps"):
        for a in sorted(set(snap[key]) - set(old.get(key, []))):
            print(f"  + {key}: {a}")
            rc = 1
        for x in sorted(set(old.get(key, [])) - set(snap[key])):
            print(f"  - {key}: {x} (fixed)")
    if snap["macro_gap_count"] > old.get("macro_gap_count", 0):
        print(f"  + macro gaps: {old.get('macro_gap_count', 0)} -> "
              f"{snap['macro_gap_count']}")
        rc = 1
    print()
    print("A rewrite became unprintable. If intended, update the baseline."
          if rc else "OK: no new unprintable rewrite.")
    return rc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -m dokimasia.rewrites",
        description="Coverage of cvc5's rewrite vocabulary at the Eunoia seam.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("coverage", help="the four-way split")
    c.add_argument("cvc5"); c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_coverage)
    g = sub.add_parser("gaps", help="applied, and unprintable")
    g.add_argument("cvc5"); g.add_argument("--json", action="store_true")
    g.set_defaults(func=cmd_gaps)
    b = sub.add_parser("baseline", help="ratchet the gaps")
    b.add_argument("cvc5"); b.add_argument("--file", default="rewrites-baseline.json")
    b.add_argument("--write", action="store_true"); b.add_argument("--check", action="store_true")
    b.set_defaults(func=cmd_baseline)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
