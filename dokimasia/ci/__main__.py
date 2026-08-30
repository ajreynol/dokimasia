"""Command line for the CI-integrity analysis.

    python3 -m dokimasia.ci proofs   <cvc5>   # is proof testing still attached?
    python3 -m dokimasia.ci matrix   <cvc5>   # job x tester
    python3 -m dokimasia.ci testers  <cvc5>   # what each tester actually passes
    python3 -m dokimasia.ci baseline <cvc5> --check
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from .scan import CHECKING_TESTER, PROOF_TESTERS, scan


def cmd_proofs(args) -> int:
    m = scan(args.cvc5)
    chain = m.completeness_chain()
    if args.json:
        print(json.dumps({
            "jobs": len(m.jobs),
            "with_proof_testers": [j.name for j in m.jobs_with_proofs()],
            "chain": [{"link": d, "holds": ok, "evidence": e} for d, ok, e in chain],
        }, indent=2))
        return 0 if all(ok for _, ok, _ in chain) else 1

    wp = m.jobs_with_proofs()
    print(f"{len(m.jobs)} build-matrix jobs; {len(wp)} run a proof tester\n")
    for j in sorted(wp, key=lambda j: j.name):
        print(f"  {j.name:<28} {j.mode:<13} {', '.join(j.proof_testers)}")
    promising = m.modes_promising_proofs()
    naked = [j for j in promising if not j.proof_testers]
    if naked:
        print("\n  CI0001 — a job builds a mode that promises proofs but tests none:")
        for j in naked:
            print(f"    {j.name} ({j.mode})")

    print("\nCI0002 — the completeness chain\n")
    print("  Completeness is not requested anywhere. In a safe build,")
    print("  setDefaultsPre turns on checkProofsComplete when --check-proofs is")
    print("  set and no granularity was asked for. So it is tested only as a")
    print("  side effect, through these links:\n")
    broken = 0
    for i, (desc, ok, ev) in enumerate(chain, 1):
        mark = "ok " if ok else "NO "
        print(f"    {i}. [{mark}] {desc}")
        print(f"           {ev}")
        if not ok:
            broken += 1
    if broken:
        print("\n  Every link holds today except the last: nothing names the")
        print("  guarantee. Adding --check-proofs-complete to the proof tester")
        print("  would make it explicit and cost one line.")

    pt = m.testers.get(CHECKING_TESTER)
    if pt and any("--proof-check=lazy" in f for f in pt.flags):
        print("\n  CI0003 — the proof tester runs --proof-check=lazy, so")
        print("  ensureClosedWrtInternal returns early: proof closedness is")
        print("  never checked by this job.")

    ex = {j.name: j.exclude_regress for j in wp if j.exclude_regress}
    if ex:
        print("\n  CI0004 — regression levels excluded from proof-testing jobs:")
        for n, v in sorted(ex.items()):
            print(f"    {n}: {v}")
    return 1 if broken else 0


def cmd_matrix(args) -> int:
    m = scan(args.cvc5)
    if args.json:
        print(json.dumps([{
            "job": j.name, "workflow": j.workflow, "mode": j.mode,
            "testers": j.testers, "proof_testers": j.proof_testers,
            "exclude_regress": j.exclude_regress,
        } for j in m.jobs], indent=2))
        return 0
    print(f"{'job':<30}{'mode':<14}testers")
    for j in m.jobs:
        mark = "*" if j.proof_testers else " "
        print(f" {mark}{j.name:<29}{j.mode:<14}{', '.join(j.testers) or '(default)'}")
    print(f"\n  * runs at least one proof tester ({', '.join(sorted(PROOF_TESTERS))})")
    print(f"  default testers when a job names none: {', '.join(m.default_testers)}")
    if CHECKING_TESTER in m.default_testers:
        print(f"\n  Note: '{CHECKING_TESTER}' is in the default list, so a developer")
        print("  running regressions locally gets proof checking that most CI")
        print("  jobs, which override the list, do not.")
    return 0


def cmd_testers(args) -> int:
    m = scan(args.cvc5)
    if args.json:
        print(json.dumps({t.name: t.flags for t in m.testers.values()}, indent=2))
        return 0
    print(f"{len(m.testers)} testers in run_regression.py\n")
    for name in sorted(m.testers):
        t = m.testers[name]
        tag = "  <- proof" if name in PROOF_TESTERS else ""
        print(f"  {name:<12} {' '.join(t.flags) or '(no extra flags)'}{tag}")
    return 0


def cmd_baseline(args) -> int:
    m = scan(args.cvc5)
    snap = {
        "jobs_with_proof_testers": sorted(j.name for j in m.jobs_with_proofs()),
        "proof_tester_flags": (m.testers[CHECKING_TESTER].flags
                               if CHECKING_TESTER in m.testers else []),
        "chain_holds": [ok for _, ok, _ in m.completeness_chain()],
    }
    path = args.file
    if args.write:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(snap, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"wrote baseline to {path}: "
              f"{len(snap['jobs_with_proof_testers'])} jobs test proofs")
        return 0
    if not os.path.exists(path):
        print(f"no baseline at {path}; run with --write first", file=sys.stderr)
        return 2
    with open(path, encoding="utf-8") as fh:
        old = json.load(fh)
    rc = 0
    lost = set(old.get("jobs_with_proof_testers", [])) - set(snap["jobs_with_proof_testers"])
    for j in sorted(lost):
        print(f"  - {j} no longer runs a proof tester")
        rc = 1
    if old.get("proof_tester_flags") != snap["proof_tester_flags"]:
        print(f"  ! the proof tester's flags changed:")
        print(f"      was {' '.join(old.get('proof_tester_flags', []))}")
        print(f"      now {' '.join(snap['proof_tester_flags'])}")
        rc = 1
    for i, (was, now) in enumerate(zip(old.get("chain_holds", []), snap["chain_holds"]), 1):
        if was and not now:
            print(f"  - completeness chain link {i} no longer holds")
            rc = 1
    print()
    print("Proof testing got weaker. If intended, update the baseline and say why."
          if rc else "OK: proof testing is no weaker than the baseline.")
    return rc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -m dokimasia.ci",
        description="Independent check that cvc5's proof testing is still attached.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("proofs", help="is proof testing still attached?")
    p.add_argument("cvc5")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_proofs)

    mx = sub.add_parser("matrix", help="job x tester")
    mx.add_argument("cvc5")
    mx.add_argument("--json", action="store_true")
    mx.set_defaults(func=cmd_matrix)

    t = sub.add_parser("testers", help="what each tester passes to cvc5")
    t.add_argument("cvc5")
    t.add_argument("--json", action="store_true")
    t.set_defaults(func=cmd_testers)

    b = sub.add_parser("baseline", help="ratchet proof-test coverage")
    b.add_argument("cvc5")
    b.add_argument("--file", default="ci-baseline.json")
    b.add_argument("--write", action="store_true")
    b.add_argument("--check", action="store_true")
    b.set_defaults(func=cmd_baseline)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
