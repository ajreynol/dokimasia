"""Command line for the modes subtool.

    python3 -m dokimasia.modes delta    <cvc5>   # what safe mode changes
    python3 -m dokimasia.modes list     <cvc5>   # every guarded option change
    python3 -m dokimasia.modes baseline <cvc5>   # track the list over time
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from .delta import ModeDelta, parse_option_defaults, unsupported_but_enabled

LIMIT_NOTE = (
    "note: a syntactic extraction of the guards written around each change. It\n"
    "      does not solve path conditions. Rows marked (implied) are reachable\n"
    "      in safe mode only via safe mode's own proofMode -> FULL_STRICT\n"
    "      upgrade; that inference is encoded, and shown rather than merged."
)


def _load(args):
    src = args.cvc5
    src = os.path.join(src, "src") if os.path.isdir(os.path.join(src, "src")) else src
    if not os.path.isdir(src):
        raise SystemExit(f"not a cvc5 checkout: {args.cvc5!r}")
    return src, ModeDelta.load(src), parse_option_defaults(src)


def _row(c, defaults, md, mode):
    d = defaults.get(c.option, {})
    return {
        "option": c.key(),
        "long": d.get("long", ""),
        "default": d.get("default", ""),
        "value": c.value,
        "reason": c.reason,
        "line": c.line,
        "refuses": c.refuses,
        "respects_user": c.respects_user,
        "implied": md.implied(c, mode),
        "tags": sorted(c.tags),
    }


def cmd_delta(args) -> int:
    _src, md, defaults = _load(args)
    mode = args.mode
    rows = [_row(c, defaults, md, mode)
            for c in md.for_mode(mode, with_proofs=not args.no_proofs)]
    if args.json:
        print(json.dumps({"mode": mode, "with_proofs": not args.no_proofs,
                          "changes": rows}, indent=2))
        return 0

    pf = "without proofs" if args.no_proofs else "with proofs"
    print(f"What --safe-mode={mode} changes about the defaults ({pf})")
    print(f"  {len(rows)} option changes\n")

    direct = [r for r in rows if not r["implied"]]
    implied = [r for r in rows if r["implied"]]

    def show(rs):
        for r in rs:
            mark = "[refuse]" if r["refuses"] else ("[if-uns]" if r["respects_user"] else "[silent]")
            dflt = r["default"] or "?"
            print(f"  {mark} {r['option']:<34} {dflt:>16} -> {r['value']}")
            print(f"           {'':<34} {r['reason']}  (set_defaults.cpp:{r['line']})")

    show(direct)
    if implied:
        print(f"\n  reachable only via safe mode's proofMode -> FULL_STRICT upgrade:")
        show(implied)
    print()
    print(f"  {sum(1 for r in rows if r['refuses'])} refused outright, "
          f"{sum(1 for r in rows if r['respects_user'])} yield to an explicit user setting, "
          f"{sum(1 for r in rows if not r['refuses'] and not r['respects_user'])} changed silently.")
    print()
    print(LIMIT_NOTE)
    return 0


def cmd_list(args) -> int:
    _src, md, defaults = _load(args)
    rows = [c for c in md.changes if not args.tagged or c.tags]
    if args.json:
        print(json.dumps([{
            "option": c.key(), "value": c.value, "reason": c.reason,
            "line": c.line, "tags": sorted(c.tags), "guards": c.guards,
        } for c in rows], indent=2))
        return 0
    print(f"{len(rows)} option changes in set_defaults.cpp"
          + (" with a mode/proof guard" if args.tagged else "") + "\n")
    for c in sorted(rows, key=lambda c: c.line):
        tags = ",".join(sorted(c.tags)) or "-"
        print(f"  L{c.line:<5} {c.key():<36} -> {c.value:<28} [{tags}]")
    return 0


def cmd_check(args) -> int:
    src, md, _defaults = _load(args)
    rows = unsupported_but_enabled(src, md)
    if args.json:
        print(json.dumps(rows, indent=2))
        return 1 if rows else 0

    print("Options declaring no proof support that safe mode leaves on\n")
    if not rows:
        print("  none -- every option with no_support=[\"proofs\"] is either off by")
        print("  default or disabled by safe mode.")
        return 0
    for r in rows:
        print(f"  {r['option']:<22} --{r['long']:<26} default {r['default']}")
        print(f"  {'':<22} declares no_support = {r['no_support']}  ({r['file']})")
    print()
    print("  Safe mode promises no feature 'that does not have full proof and")
    print("  model support'. Each row is an option cvc5 itself annotates as")
    print("  having none, which is on by default, and which neither")
    print("  setDefaultsPre nor the SolverEngine guard turns off -- that guard")
    print("  fires when a user *sets* an option, not on its default value.")
    print()
    print("  Either reading is a defect: the option should be disabled in safe")
    print("  mode, or the no_support annotation is stale and should go.")
    print()
    print("  LIMIT: this compares defaults only. A mode option whose effect is")
    print("  gated by another flag (macrosQuantMode is gated by macrosQuant,")
    print("  default false) can appear here without being active. Confirm")
    print("  before filing.")
    return 1


def cmd_baseline(args) -> int:
    _src, md, defaults = _load(args)
    snap = {}
    for mode in ("safe", "stable"):
        # dedupe: the same option can be set under several guards
        snap[mode] = sorted({
            f"{c.key()}={c.value}" for c in md.for_mode(mode)
        })
    path = args.file
    if args.write:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(snap, fh, indent=2)
            fh.write("\n")
        print(f"wrote baseline to {path}: "
              + ", ".join(f"{m} {len(v)}" for m, v in snap.items()))
        return 0
    if not os.path.exists(path):
        print(f"no baseline at {path}; run with --write first", file=sys.stderr)
        return 2
    with open(path, encoding="utf-8") as fh:
        old = json.load(fh)
    rc = 0
    for mode in ("safe", "stable"):
        was, now = set(old.get(mode, [])), set(snap[mode])
        added, removed = sorted(now - was), sorted(was - now)
        print(f"{mode}: {len(now)} changes ({len(added)} added, {len(removed)} removed)")
        for a in added:
            print(f"  + {a}")
        for r in removed:
            print(f"  - {r}")
        if added or removed:
            rc = 1
    if rc:
        print("\nThe mode delta moved. That is not automatically wrong -- but it is")
        print("a change to what safe mode promises, so it should be deliberate.")
        print("Update the baseline in the same commit and say why.")
    else:
        print("\nOK: the mode delta is unchanged.")
    return rc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -m dokimasia.modes",
        description="Track what cvc5's safe and stable modes change about the "
                    "default configuration.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("delta", help="what a mode changes about the defaults")
    d.add_argument("cvc5")
    d.add_argument("--mode", default="safe", choices=("safe", "stable"))
    d.add_argument("--no-proofs", action="store_true",
                   help="exclude changes reachable only via the FULL_STRICT upgrade")
    d.add_argument("--json", action="store_true")
    d.set_defaults(func=cmd_delta)

    l = sub.add_parser("list", help="every option change, with its guards")
    l.add_argument("cvc5")
    l.add_argument("--tagged", action="store_true",
                   help="only changes under a mode or proof guard")
    l.add_argument("--json", action="store_true")
    l.set_defaults(func=cmd_list)

    k = sub.add_parser("check", help="options with no proof support that safe mode leaves on")
    k.add_argument("cvc5")
    k.add_argument("--json", action="store_true")
    k.set_defaults(func=cmd_check)

    b = sub.add_parser("baseline", help="track the mode delta over time")
    b.add_argument("cvc5")
    b.add_argument("--file", default="modes-baseline.json")
    b.add_argument("--write", action="store_true")
    b.add_argument("--check", action="store_true")
    b.set_defaults(func=cmd_baseline)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
