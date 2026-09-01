"""BUILD0001 — a safe build must differ only in defaults, text and reporting."""
from __future__ import annotations

import argparse
import json
import sys

from .buildmode import BENIGN, MACROS, REVIEWED_BLOCKS, UNCLASSIFIED, scan

_WHY = {
    "option-default": "sets the safeMode option's initial value — the same thing "
                      "--safe-mode=safe does at runtime",
    "diagnostic": "builds an error message and nothing else",
    "diagnostic-reviewed": "message-only; read by a person, hash-pinned",
    "config-report": "defines what the build reports about itself",
}


def cmd_check(args) -> int:
    r = scan(args.cvc5)
    if args.json:
        print(json.dumps({
            "holds": r.holds(),
            "by_kind": r.by_kind(),
            "unclassified": [c.where for c in r.unclassified()],
            "excluded_sources": r.excluded_sources,
            "behavioural_readers": r.behavioural_readers,
            "disabled_libraries": r.disabled_libraries,
        }, indent=2, sort_keys=True))
        return 0 if r.holds() else 1

    print("BUILD0001 — is a safe build still an unrestricted build with a "
          "different default?\n")
    print(f"  {len(r.conditionals)} conditionals on {' / '.join(MACROS)}:")
    for kind, n in sorted(r.by_kind().items()):
        print(f"    {n:>3}  {kind:<20} {_WHY.get(kind, '')}")
    print(f"\n  source files a safe build excludes: {len(r.excluded_sources)}")
    print(f"  behavioural readers of isSafeBuild(): {len(r.behavioural_readers)}")
    print(f"  optional libraries not linked:        "
          f"{', '.join(r.disabled_libraries) or 'none'}")

    if r.holds():
        print("\n  INVARIANT HOLDS.\n")
        print("  Every conditional changes a default, a message, or what the")
        print("  build says about itself. No solver behaviour is gated on the")
        print("  build macro, no source file is excluded, and nothing branches")
        print("  on isSafeBuild(). So `--safe-mode=safe` on an unrestricted")
        print("  binary reproduces a safe build's behaviour exactly; what it")
        print("  does not reproduce is the diagnostic text, which the")
        print("  regression testers read, and the libraries above, which a")
        print("  safe build declines to link at all.")
        print("\n  While this holds, a build configuration that forbids safe")
        print("  mode alongside something else costs only those diagnostics,")
        print("  and 'safe mode' means one thing whether it names the build")
        print("  or the flag.")
        return 0

    print("\n  INVARIANT BROKEN.\n")
    for c in r.unclassified():
        print(f"    {c.where}")
        print(f"      {c.directive}")
        print("      does something other than set a default or build a message.")
    for f in r.excluded_sources:
        print(f"    a safe build excludes a source file: {f}")
    for b in r.behavioural_readers:
        print(f"    isSafeBuild() is branched on: {b}")
    print("\n  A safe build now differs from `--safe-mode=safe` in behaviour,")
    print("  not only in text. Two consequences: a runtime flag no longer")
    print("  stands in for the build, so any build configuration that excludes")
    print("  safe mode has become a real restriction rather than a")
    print("  simplification; and every claim about 'safe mode' has to say")
    print("  which one it means.")
    print("\n  If the new conditional really is message-only, add it to")
    print("  REVIEWED_BLOCKS with its hash and the reason.")
    return 1


def cmd_sites(args) -> int:
    r = scan(args.cvc5)
    for c in sorted(r.conditionals, key=lambda c: (c.path, c.line)):
        mark = "!!" if c.kind == UNCLASSIFIED else "ok"
        print(f"  {mark} {c.where:<40} {c.kind}")
        print(f"       {c.directive}")
        if args.body:
            for ln in c.body.splitlines()[:12]:
                print(f"         | {ln}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -m dokimasia.buildmode",
        description="Verify that a safe build is an unrestricted build with a "
                    "different option default.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("check", help="verify the invariant")
    p.add_argument("cvc5")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_check)
    p = sub.add_parser("sites", help="every conditional, classified")
    p.add_argument("cvc5")
    p.add_argument("--body", action="store_true")
    p.set_defaults(fn=cmd_sites)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
