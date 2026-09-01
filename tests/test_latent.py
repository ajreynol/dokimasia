"""The subtraction: static inventory − what the corpus reached = the latent set.

Run: python3 tests/test_latent.py [<cvc5>]
"""
import json, os, sys, tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dokimasia.latent import latent as L  # noqa: E402

FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    if not ok:
        print(f"       got {got!r}, want {want!r}")
        FAILURES.append(label)


def test_state():
    safe = {"trustCount": {"A": 3}}
    unres = {"trustCount": {"A": 9, "B": 4}}
    check("reached in safe mode wins over unrestricted",
          L._state("A", safe, unres, ("trustCount",)), (L.State.SAFE, 3))
    check("reached only unrestricted",
          L._state("B", safe, unres, ("trustCount",)), (L.State.OPEN, 4))
    check("never reached is latent",
          L._state("C", safe, unres, ("trustCount",)), (L.State.LATENT, 0))
    check("a safe-mode hit outranks everything",
          L.Hole("trust-id", "A", L.State.SAFE).rank, 1)
    check("latent outranks unrestricted-only",
          L.Hole("trust-id", "C", L.State.LATENT).rank
          < L.Hole("trust-id", "B", L.State.OPEN).rank, True)


def test_no_census_is_not_evidence():
    """With no census, everything must read latent -- and say why."""
    real = L.CENSUS
    try:
        L.CENSUS = "definitely-not-a-file.json"
        safe, unres, have = L._census("")
        check("a missing census is reported, not assumed empty", have, False)
        check("no counters are invented", (safe, unres), ({}, {}))
    finally:
        L.CENSUS = real


def test_cvc5(root):
    l = L.scan(root)
    check("a census was found", l.have_census, True)
    kinds = l.by_kind()
    check("all four hole kinds are inventoried",
          sorted(kinds), ["inference", "rewrite", "seam-rule", "trust-id"])
    tot = sum(sum(v.values()) for v in kinds.values())
    check("every hole lands in exactly one state",
          sum(len(l.by_state(s)) for s in
              (L.State.SAFE, L.State.LATENT, L.State.OPEN)), tot)
    # The headline claim, and the one worth a regression test.
    check("no hole is reached in safe mode on this corpus",
          len(l.by_state(L.State.SAFE)), 0)
    check("some holes are reached unrestricted",
          len(l.by_state(L.State.OPEN)) > 0, True)
    check("the latent set is the majority",
          len(l.by_state(L.State.LATENT)) > len(l.by_state(L.State.OPEN)), True)
    print(f"       {tot} holes: {len(l.by_state(L.State.LATENT))} latent, "
          f"{len(l.by_state(L.State.OPEN))} unrestricted-only")


if __name__ == "__main__":
    test_state()
    print()
    test_no_census_is_not_evidence()
    root = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CVC5")
    if root and os.path.isdir(root):
        print()
        test_cvc5(root)
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
