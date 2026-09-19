"""The pinned cvc5 revision must be real, upstream, and what we measured.

Every number this repository publishes names a commit. If that commit is not on
cvc5/cvc5 main, nobody outside this machine can fetch it, and the promise that
every claim is re-checkable without us is void. That is not hypothetical: the
baselines were originally taken against `16c4001e53`, which is on the
`ajreynol/CVC4` fork and not upstream.

Run: python3 tests/test_pin.py [<cvc5>]
"""
import json, os, re, subprocess, sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)
LOCK = os.path.join(ROOT, "scripts", "cvc5.lock")
FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    if not ok:
        print(f"       got {got!r}, want {want!r}")
        FAILURES.append(label)


def documents():
    """Every written document, front page and plan included, as repo-relative paths.

    `docs/` is walked rather than listed: a filed finding and a case study are
    the documents a cvc5 maintainer actually opens, and a guard that stops at
    the top level passes on the tree while leaving those two unread.
    """
    found = ["README.md", "TODO.md"]
    for base, _dirs, names in os.walk(os.path.join(ROOT, "docs")):
        for name in sorted(names):
            if name.endswith(".md"):
                rel = os.path.relpath(os.path.join(base, name), ROOT)
                found.append(rel.replace(os.sep, "/"))
    return sorted(found)


def test_lock():
    with open(LOCK, encoding="utf-8") as fh:
        d = json.load(fh)["cvc5"]
    check("the lock names the upstream repository",
          d["repo"], "https://github.com/cvc5/cvc5")
    check("the lock names a branch", d["branch"], "main")
    check("the commit is a hex sha",
          bool(re.fullmatch(r"[0-9a-f]{7,40}", d["commit"])), True)
    return d


def test_docs_agree(d, allowed, scoped=None):
    """No document may quote a commit the lock does not account for.

    A runtime measurement needs a build, and we have no upstream build, so a
    few numbers are necessarily taken elsewhere. Those commits must be listed
    in the lock's `unpinned_measurements` **with a reason** -- the point is that
    an unreproducible number is visible, not that it is forbidden.

    **Only abbreviations are checked, and that is the convention rather than an
    oversight.** A 9-12 character sha is how this repository quotes the revision
    one of *its own* numbers was taken at, and such a number has to be
    re-measurable against the pin. A cvc5 commit cited as something cvc5 did --
    a closure in `experience.md`, a `closed_commit` in the database, a revert
    quoted in a retraction -- is written in full, because it is evidence about
    their tree rather than a measurement of ours, and a reader fetches it from
    cvc5 rather than from the pin.
    """
    short = d["commit"][:9]
    stale = []
    for rel in documents():
        with open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        # a bare 9-12 hex run in backticks is a commit reference
        for m in re.finditer(r"`([0-9a-f]{9,12})`", text):
            c = m.group(1)
            if c.startswith(short[:9]) or c in allowed:
                continue
            if (scoped or {}).get(c) == rel:
                continue
            stale.append(f"{rel}:{c}")
    check("no document quotes an unpinned commit", sorted(set(stale)), [])


def test_printed_claims(d):
    """A hand-check the analyzer prints names a commit too, and the same rule binds it.

    The ledger's severity note is the one claim in this repository that is
    published by running the tool rather than by committing a document, so the
    document scan above never sees it. It went a month naming a fork commit no
    reader could fetch.
    """
    from dokimasia.ledger.__main__ import SEVERITY_NOTE

    cited = re.findall(r"\b([0-9a-f]{9,12})\b", SEVERITY_NOTE)
    check("the severity note still cites the commit it was checked at",
          bool(cited), True)
    for c in cited:
        check("the ledger's severity note names the pinned commit",
              c, d["commit"][:len(c)])


def test_checkout(root, d):
    """If a checkout is given, the pinned commit must exist in it."""
    r = subprocess.run(["git", "-C", root, "cat-file", "-t", d["commit"]],
                       capture_output=True, text=True)
    check("the pinned commit exists in the given checkout",
          r.stdout.strip(), "commit")


if __name__ == "__main__":
    d = test_lock()
    with open(LOCK, encoding="utf-8") as fh:
        lk = json.load(fh)
    # A measurement exception is global (the number appears wherever it is
    # discussed); a historical one is scoped to the single document that tells
    # the story, so it cannot spread to a document quoting it as a measurement.
    allowed = {k: v for k, v in lk.get("unpinned_measurements", {}).items()
               if not k.startswith("_")}
    scoped = {k: v["only_in"] for k, v in lk.get("historical", {}).items()
              if not k.startswith("_")}
    for c, why in allowed.items():
        check(f"exception {c} states a reason", bool(why and len(why) > 20), True)
    for c, only in scoped.items():
        check(f"historical {c} is scoped to one document", bool(only), True)
    # The scan below is only worth its green if it reached the documents most
    # likely to quote a commit: the filed findings and the case studies.
    docs = documents()
    check("the scan reaches documents below docs/",
          all(any(p.startswith(sub) for p in docs)
              for sub in ("docs/findings/", "docs/cases/")), True)
    test_docs_agree(d, set(allowed), scoped)
    test_printed_claims(d)
    root = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CVC5")
    if root and os.path.isdir(os.path.join(root, ".git")):
        test_checkout(root, d)
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
