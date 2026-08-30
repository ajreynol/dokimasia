"""Command line for the trust census.

    python3 -m dokimasia.trust census   <cvc5>   # every TrustId, by subsystem
    python3 -m dokimasia.trust show     <cvc5> THEORY_LEMMA
    python3 -m dokimasia.trust dead     <cvc5>   # declared, never constructed
    python3 -m dokimasia.trust passes   <cvc5>   # preprocessing correspondence
    python3 -m dokimasia.trust baseline <cvc5> --check
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from .census import SENTINELS, census


def cmd_census(args) -> int:
    c = census(args.cvc5)
    live, dead = c.live(), c.dead()
    if args.json:
        print(json.dumps({
            "live": {i: [s.where() for s in c.construction(i)] for i in live},
            "dead": dead,
        }, indent=2))
        return 0
    print(f"{len(c.declared)} declared TrustIds — the holes cvc5 knows about\n")
    print(f"  live  {len(live)}   constructed somewhere")
    print(f"  dead  {len(dead)}   declared and never constructed")
    anon = c.anonymous()
    if anon:
        print(f"\n  {len(anon)} trust steps are built with TrustId::NONE — a hole "
              "with no stated reason:")
        for s in anon[: args.limit]:
            print(f"    {s.where()}")
    print("\n  by subsystem:")
    for sub, ids, n in c.by_subsystem():
        print(f"    {sub:<30} {ids:>3} ids   {n:>3} sites")
    print("\n  most-constructed ids:")
    ranked = sorted(((len(c.construction(i)), i) for i in live), reverse=True)
    for n, i in ranked[: args.limit]:
        subs = {s.subsystem for s in c.construction(i)}
        print(f"    {n:>3}x  {i:<38} {', '.join(sorted(subs))}")
    return 0


def cmd_show(args) -> int:
    c = census(args.cvc5)
    ident = args.id.removeprefix("TrustId::")
    if ident not in c.declared:
        print(f"no such TrustId: {ident}", file=sys.stderr)
        return 2
    print(f"TrustId::{ident}\n")
    for kind in ("construction", "dispatch", "comparison", "definition"):
        rows = [s for s in c.sites.get(ident, []) if s.kind == kind]
        if rows:
            print(f"  {kind} ({len(rows)}):")
            for s in rows:
                print(f"    {s.where()}")
    n = len(c.construction(ident))
    print(f"\n  {n} construction site(s)" + ("  — dead" if n == 0 else ""))
    return 0


def cmd_dead(args) -> int:
    c = census(args.cvc5)
    dead = c.dead()
    if args.json:
        print(json.dumps(dead, indent=2))
        return 0
    print(f"TrustIds declared and never constructed ({len(dead)})\n")
    for i in dead:
        other = [s for s in c.sites.get(i, []) if s.kind != "definition"]
        note = "  <- but something dispatches on it" if other else ""
        print(f"  {i}{note}")
    print("\n  A declared hole nothing builds is a claim about a step cvc5 does")
    print("  not take. Removing it shrinks the inventory every later analysis")
    print("  quantifies over.")
    return 0


def cmd_passes(args) -> int:
    c = census(args.cvc5)
    pc = c.pass_correspondence()
    if args.json:
        print(json.dumps(pc, indent=2))
        return 0
    print(f"{len(c.passes)} preprocessing passes\n")
    print(f"  {len(pc['declares'])} construct a TrustId — a declared hole")
    print(f"  {len(pc['silent'])} construct none — either they prove their work, "
          "or the hole is undeclared:")
    for p in pc["silent"]:
        print(f"    {p}")
    if pc["orphan_id"]:
        print(f"\n  {len(pc['orphan_id'])} PREPROCESS_* ids nothing constructs:")
        for i in pc["orphan_id"]:
            print(f"    {i}")
    mis = c.misnamed_pass_ids()
    if mis:
        print(f"\n  {len(mis)} ids are not derivable from their pass filename, "
              "so this\n  correspondence cannot be checked by name — only by "
              "construction site:")
        for p, got, want in mis:
            print(f"    {p:<26} constructs {got}")
            print(f"    {'':<26} filename implies {want}")
    return 0


def cmd_baseline(args) -> int:
    c = census(args.cvc5)
    snap = {
        "live": sorted(c.live()),
        "dead": sorted(c.dead()),
        "anonymous_sites": len(c.anonymous()),
        "silent_passes": sorted(c.pass_correspondence()["silent"]),
    }
    path = args.file
    if args.write:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(snap, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"wrote baseline to {path}: {len(snap['live'])} live, "
              f"{len(snap['dead'])} dead, {snap['anonymous_sites']} anonymous")
        return 0
    if not os.path.exists(path):
        print(f"no baseline at {path}; run with --write first", file=sys.stderr)
        return 2
    with open(path, encoding="utf-8") as fh:
        old = json.load(fh)
    rc = 0
    for a in sorted(set(snap["live"]) - set(old.get("live", []))):
        print(f"  + a new trust id is now constructed: {a}")
        rc = 1
    for r in sorted(set(old.get("live", [])) - set(snap["live"])):
        print(f"  - no longer constructed: {r}")
    if snap["anonymous_sites"] > old.get("anonymous_sites", 0):
        print(f"  + anonymous trust steps: {old.get('anonymous_sites', 0)} -> "
              f"{snap['anonymous_sites']}")
        rc = 1
    for a in sorted(set(snap["silent_passes"]) - set(old.get("silent_passes", []))):
        print(f"  + a pass stopped declaring a trust id: {a}")
    print()
    print("A new hole appeared. If intended, update the baseline in the same commit."
          if rc else "OK: no new trust step.")
    return rc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -m dokimasia.trust",
        description="The census of cvc5's declared holes.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("census", help="every TrustId, by subsystem")
    c.add_argument("cvc5")
    c.add_argument("--limit", type=int, default=12)
    c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_census)

    s = sub.add_parser("show", help="every site of one id")
    s.add_argument("cvc5")
    s.add_argument("id")
    s.set_defaults(func=cmd_show)

    d = sub.add_parser("dead", help="declared, never constructed")
    d.add_argument("cvc5")
    d.add_argument("--json", action="store_true")
    d.set_defaults(func=cmd_dead)

    p = sub.add_parser("passes", help="preprocessing pass correspondence")
    p.add_argument("cvc5")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_passes)

    b = sub.add_parser("baseline", help="ratchet the census")
    b.add_argument("cvc5")
    b.add_argument("--file", default="trust-baseline.json")
    b.add_argument("--write", action="store_true")
    b.add_argument("--check", action="store_true")
    b.set_defaults(func=cmd_baseline)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
