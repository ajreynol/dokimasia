"""Command line for inference coverage.

    python3 -m dokimasia.infer coverage <cvc5>          # per theory
    python3 -m dokimasia.infer unhandled <cvc5> strings # the ids that fall through
    python3 -m dokimasia.infer baseline <cvc5> --check
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from .coverage import scan


def cmd_coverage(args) -> int:
    c = scan(args.cvc5)
    rows = sorted(c.theories.values(), key=lambda t: -len(t.produced))
    if args.json:
        print(json.dumps([{"theory": t.theory, "produced": len(t.produced),
                           "reconstructed": len(t.reconstructed),
                           "unhandled": t.unhandled, "has_ipc": t.has_ipc}
                          for t in rows], indent=2))
        return 0
    print("Does every inference a theory makes have a proof reconstruction?\n")
    print(f"  {'theory':<16}{'emits':>7}{'reconstructed':>15}{'falls through':>15}   rate")
    for t in rows:
        rate = f"{t.rate * 100:.0f}%" if t.rate is not None else "—"
        note = "" if t.has_ipc else "   no InferProofCons"
        print(f"  {t.theory:<16}{len(t.produced):>7}{len(t.reconstructed):>15}"
              f"{len(t.unhandled):>15}   {rate}{note}")
    print(f"\n  {c.total_unhandled()} inferences are emitted by a theory that has a")
    print("  reconstructor and are not named in it. Its default case builds a")
    print("  TRUST step, so each of these is a hole by construction.\n")
    nr = c.without_reconstructor()
    if nr:
        print(f"  {len(nr)} theories emit inferences with no InferProofCons at all:")
        for t in sorted(nr, key=lambda t: -len(t.produced)):
            print(f"    {t.theory:<16} {len(t.produced)} inferences")
        print("\n  That is NOT the same as having no proofs. Several theories attach")
        print("  a ProofGenerator at the inference site instead, which this does")
        print("  not see. For these the honest verdict is *unknown by this")
        print("  mechanism*, and settling it needs the call site, not the switch.")
    dead = {t.theory: t.reconstructed_not_produced
            for t in c.with_reconstructor() if t.reconstructed_not_produced}
    if dead:
        print(f"\n  Reconstruction cases for inferences nothing emits:")
        for th, ids in dead.items():
            print(f"    {th}: {', '.join(ids)}")
    return 1 if c.total_unhandled() else 0


def cmd_unhandled(args) -> int:
    c = scan(args.cvc5)
    t = c.theories.get(args.theory)
    if t is None:
        print(f"no theory {args.theory!r}; known: "
              f"{', '.join(sorted(c.theories))}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(t.unhandled, indent=2))
        return 0
    if not t.has_ipc:
        print(f"{t.theory} has no InferProofCons; all {len(t.produced)} of its")
        print("inferences are reconstructed elsewhere, or not at all.")
        return 0
    print(f"{t.theory}: {len(t.unhandled)} of {len(t.produced)} inferences fall")
    print(f"through {t.ipc_file} to a TRUST step\n")
    for i in t.unhandled:
        print(f"  {i}")
    return 1 if t.unhandled else 0


def cmd_baseline(args) -> int:
    c = scan(args.cvc5)
    snap = {t.theory: sorted(t.unhandled)
            for t in c.with_reconstructor()}
    path = args.file
    if args.write:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(snap, fh, indent=2, sort_keys=True); fh.write("\n")
        print(f"wrote baseline to {path}: "
              f"{sum(len(v) for v in snap.values())} unhandled inferences")
        return 0
    if not os.path.exists(path):
        print(f"no baseline at {path}; run with --write first", file=sys.stderr)
        return 2
    with open(path, encoding="utf-8") as fh:
        old = json.load(fh)
    rc = 0
    for th, ids in sorted(snap.items()):
        added = sorted(set(ids) - set(old.get(th, [])))
        fixed = sorted(set(old.get(th, [])) - set(ids))
        for a in added:
            print(f"  + {th}: {a} now falls through to a trust step"); rc = 1
        for f in fixed:
            print(f"  - {th}: {f} is now reconstructed")
    print()
    print("An inference lost its reconstruction. If intended, update the baseline."
          if rc else "OK: no inference newly falls through.")
    return rc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -m dokimasia.infer",
        description="Per-theory coverage of inferences by proof reconstruction.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("coverage", help="per theory")
    c.add_argument("cvc5"); c.add_argument("--json", action="store_true")
    c.set_defaults(func=cmd_coverage)
    u = sub.add_parser("unhandled", help="the ids that fall through, for one theory")
    u.add_argument("cvc5"); u.add_argument("theory")
    u.add_argument("--json", action="store_true")
    u.set_defaults(func=cmd_unhandled)
    b = sub.add_parser("baseline", help="ratchet the fall-through set")
    b.add_argument("cvc5"); b.add_argument("--file", default="infer-baseline.json")
    b.add_argument("--write", action="store_true"); b.add_argument("--check", action="store_true")
    b.set_defaults(func=cmd_baseline)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
