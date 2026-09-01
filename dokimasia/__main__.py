"""One entry point across every subtool.

`python3 -m dokimasia check <cvc5>` runs all eight ratchets in a single
process, so the ~17 MB of `src/` is read once instead of once per tool. That is
the whole trick; each subtool computes exactly what it computed before.
"""
from __future__ import annotations

import argparse
import importlib
import io
import sys
import time
from contextlib import redirect_stdout

from . import source

#: The subtools carrying a `baseline --check` ratchet, in the order a reader
#: wants them: contract first, then inventory, then hygiene.
RATCHETS = ("modes", "ci", "ledger", "rewrites", "trust", "infer", "inferid", "tcb")

#: Checks that assert an invariant outright rather than against a baseline.
#: They pass or fail on the tree alone, so there is nothing to re-record.
INVARIANTS = ("buildmode",)

#: Everything, including the tools with no baseline to ratchet against.
ALL = RATCHETS + INVARIANTS + ("gates", "fragment", "signature", "latent")


def _run(mod: str, argv: list[str]) -> tuple[int, str]:
    """Run a subtool's main() in-process, capturing what it printed."""
    m = importlib.import_module(f".{mod}.__main__", package="dokimasia")
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            rc = m.main(argv)
    except SystemExit as e:                      # argparse, or a bad checkout
        rc = e.code if isinstance(e.code, int) else 1
    except Exception as e:                       # a scanner blew up: say which
        return 2, f"{type(e).__name__}: {e}"
    return rc, buf.getvalue()


def cmd_check(args) -> int:
    """Every ratchet, one process. The CI job and the pre-commit check."""
    t0 = time.time()
    failed, broke = [], []
    for mod in RATCHETS + INVARIANTS:
        t = time.time()
        argv = ([args.cvc5] if mod in INVARIANTS
                else ["baseline", args.cvc5, "--check"])
        rc, out = _run(mod, ["check"] + argv if mod in INVARIANTS else argv)
        last = [ln for ln in out.strip().splitlines() if ln.strip()]
        # A ratchet's verdict is its last line; an invariant states its verdict
        # in the middle and then explains itself, so look for the verdict.
        tail = next((ln.strip() for ln in last if "INVARIANT" in ln),
                    last[-1] if last else "(no output)")
        mark = "ok  " if rc == 0 else ("FAIL" if rc == 1 else "ERR ")
        print(f"  {mark} {mod:<9} {time.time()-t:5.2f}s  {tail}")
        if rc == 1:
            failed.append(mod)
            if args.verbose:
                print("\n".join("        " + ln for ln in last[:-1]))
        elif rc != 0:
            broke.append(mod)
    n, b = source.stats()
    print(f"\n  {len(RATCHETS)} ratchets + {len(INVARIANTS)} invariant(s) "
          f"in {time.time()-t0:.2f}s; "
          f"read {n} files / {b/1e6:.1f} MB once")
    if broke:
        print(f"\n  {len(broke)} tool(s) errored: {', '.join(broke)} — "
              "that is our bug, not cvc5's.")
    if failed:
        print(f"\n  {len(failed)} ratchet(s) moved: {', '.join(failed)}.\n"
              "  Re-run the one that moved for detail, or pass --verbose.\n"
              "  If the change is intended, update its baseline in the same commit.")
    return 1 if (failed or broke) else 0


def cmd_write(args) -> int:
    """Re-record every baseline. Only ever run deliberately."""
    for mod in RATCHETS:
        rc, out = _run(mod, ["baseline", args.cvc5, "--write"])
        print(f"  {mod:<9} {out.strip().splitlines()[-1] if out.strip() else rc}")
    return 0


def cmd_report(args) -> int:
    """Every analysis, printed. The 'what does cvc5 look like today' pass."""
    views = {
        "modes": ["check"], "ci": ["proofs"], "ledger": ["holes"],
        "rewrites": ["gaps"], "trust": ["census"], "infer": ["coverage"],
        "inferid": ["check"], "tcb": ["measure"], "gates": ["verdicts"],
        "fragment": ["check"], "signature": ["skolems"],
        "latent": ["census"], "buildmode": ["check"],
    }
    for mod in ALL:
        print(f"\n{'=' * 72}\n== {mod}\n{'=' * 72}")
        _, out = _run(mod, views[mod] + [args.cvc5])
        print(out.rstrip())
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -m dokimasia",
        description="Every dokimasia analysis, in one process.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn, helptext in (
            ("check", cmd_check, "run every ratchet (the CI check)"),
            ("write", cmd_write, "re-record every baseline"),
            ("report", cmd_report, "print every analysis")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("cvc5")
        p.add_argument("-v", "--verbose", action="store_true")
        p.set_defaults(fn=fn)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
