"""Command line for the signature cross-check.

    python3 -m dokimasia.signature rules   <cvc5>   # printable rules vs the signature
    python3 -m dokimasia.signature skolems <cvc5>   # SkolemIds: documented, built, printable
    python3 -m dokimasia.signature arity   <cvc5>   # doc vs signature arity (noisy; read the caveat)
"""

from __future__ import annotations

import argparse
import json

from .compare import printed_name, scan

ARITY_CAVEAT = """
  READ THIS BEFORE BELIEVING THE ROWS ABOVE.

  The `\\inferrule` documentation is prose-with-LaTeX, not a specification, and
  the Eunoia printer *reshapes* a rule's arguments on the way out — several
  cvc5 arguments become one Eunoia list argument. So a raw arity comparison
  cannot distinguish "the docs are wrong" from "the printer reshaped it".

  Our own history here is the argument: this comparison reported 72
  disagreements, then 19, then 14, then 12, as four separate LaTeX conventions
  were accounted for — a single premise containing `\\dots`, `:args ((= F1 F2))`
  being one s-expression rather than three tokens, `\\,` being a thin space
  whose second character is a comma, and a bare `\\dots` standing between listed
  premises. Every round looked like findings and was our bug.

  What remains is the reshaping class, which is expected. Treat these as
  *questions*, never as defects, until the printer's reshaping is modelled.
"""


def cmd_rules(args) -> int:
    s = scan(args.cvc5)
    miss = s.missing()
    if args.json:
        print(json.dumps({"printable": len(s.printable), "signature_rules": len(s.sig),
                          "missing": miss}, indent=2))
        return 1 if miss else 0
    print("Do the rules cvc5 can print exist in the Eunoia signature?\n")
    print(f"  {len(s.printable)} ProofRules the seam accepts")
    print(f"  {len(s.sig)} rules declared across proofs/eo/\n")
    if miss:
        print("  Printable rules the signature does NOT declare — ethos would")
        print("  reject a proof containing them:")
        for r in miss:
            print(f"    {r:<32} would print as `{printed_name(r)}`")
    else:
        print("  Every printable rule has a declaration. **This one is clean.**")
        print("  `ASSUME` is excluded: an Eunoia `assume` is a command, not a rule.")
    print(f"\n  {len(s.undocumented())} printable rules have no parseable "
          "`\\inferrule` in their doc comment.")
    return 1 if miss else 0


def cmd_skolems(args) -> int:
    k = scan(args.cvc5).skolems
    if args.json:
        print(json.dumps({"unprintable": k.unprintable(), "dead": k.dead(),
                          "undocumented": k.undocumented()}, indent=2))
        return 1 if k.unprintable() else 0
    print("SkolemIds — the other half of what the seam must be able to print\n")
    print(f"  {len(k.declared)} declared, {len(k.doc_indices)} with a documented")
    print(f"  index count, {len(k.constructed)} constructed, "
          f"{len(k.seam_handled)} accepted by the seam\n")
    up = k.unprintable()
    print(f"  {len(up)} are constructed by the solver and refused by the seam.")
    print("  A skolem the seam cannot print sinks a proof exactly as a rule it")
    print("  cannot print does:")
    for i in up:
        print(f"    {i}")
    print(f"\n  {len(k.dead())} declared and never constructed.")
    if k.undocumented():
        print(f"  {len(k.undocumented())} constructed with no documented index count:")
        for i in k.undocumented():
            print(f"    {i}")
    else:
        print("  Every constructed skolem documents its index count — the skolem")
        print("  documentation is in better shape than the proof-rule documentation.")
    print("\n  Severity needs the option gate: most of these are bags, sets,")
    print("  relations or transcendental, which safe mode disables. The ones")
    print("  worth checking first are the ones that are not.")
    return 1 if up else 0


def cmd_arity(args) -> int:
    s = scan(args.cvc5)
    m = s.mismatches()
    if args.json:
        print(json.dumps([{"rule": r, "signature": n, "doc": list(d),
                           "sig": list(sg)} for r, n, d, sg in m], indent=2))
        return 0
    print(f"{len(m)} rules where the documented arity and the signature differ\n")
    for r, n, d, sg in m:
        print(f"  {r:<30} doc(prem={d[0]}, args={d[1]})   sig(prem={sg[0]}, args={sg[1]})")
    print(ARITY_CAVEAT)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -m dokimasia.signature",
        description="Does the Eunoia signature agree with cvc5's account of a rule?")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn, helptext in (("rules", cmd_rules, "printable rules vs the signature"),
                               ("skolems", cmd_skolems, "SkolemId coverage"),
                               ("arity", cmd_arity, "documented vs signature arity")):
        q = sub.add_parser(name, help=helptext)
        q.add_argument("cvc5"); q.add_argument("--json", action="store_true")
        q.set_defaults(func=fn)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
