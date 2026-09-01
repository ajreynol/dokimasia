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
LOCK = os.path.join(ROOT, "tools", "cvc5.lock")
FAILURES = []


def check(label, got, want):
    ok = got == want
    print(f"  {'ok  ' if ok else 'FAIL'} {label}")
    if not ok:
        print(f"       got {got!r}, want {want!r}")
        FAILURES.append(label)


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
    """
    short = d["commit"][:9]
    stale = []
    for sub, names in (("", ["README.md", "TODO.md"]), ("docs", None)):
        base = os.path.join(ROOT, sub) if sub else ROOT
        for name in (names or sorted(os.listdir(base))):
            if not name.endswith(".md"):
                continue
            path = os.path.join(base, name)
            if not os.path.isfile(path):
                continue
            with open(path, encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
            # a bare 9-12 hex run in backticks is a commit reference
            for m in re.finditer(r"`([0-9a-f]{9,12})`", text):
                c = m.group(1)
                rel = f"{sub}/{name}" if sub else name
                if c.startswith(short[:9]) or c in allowed:
                    continue
                if (scoped or {}).get(c) == rel:
                    continue
                stale.append(f"{rel}:{c}")
    check("no document quotes an unpinned commit", sorted(set(stale)), [])


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
    test_docs_agree(d, set(allowed), scoped)
    root = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CVC5")
    if root and os.path.isdir(os.path.join(root, ".git")):
        test_checkout(root, d)
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
