"""Tests for what a closure run leaves behind: the write-up and the launcher.

`docs/experience.md` is the one document written by an assistant rather than by
a person, and the half a reader cannot enforce by reading is its shape: a
convention nothing checks is a wish. The entry template is checked as well as
the entries, because there may be no entries for a long time and the template is
what the next run copies.

The closure launcher is checked for the properties that keep it honest --
previewing its prompt reads no tree it should not and writes nothing, and the
prompt still carries the rules that stop a closure being asserted from absence.

The check catalogue is checked against the index that quotes its size, for the
same reason as ever: a count in a second document is a copy, and a copy nobody
re-counts drifts.

Run: python3 tests/test_experience.py
"""

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPERIENCE = os.path.join(ROOT, "docs", "experience.md")
# The catalogue and the index are one document now; the count is still
# compared against the table rather than trusted, which is the point.
CHECKS = os.path.join(ROOT, "docs", "README.md")
INDEX = os.path.join(ROOT, "docs", "README.md")

FAILURES = []


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def check(label, ok, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'} {label}" + ("" if ok else f": {detail}"))
    if not ok:
        FAILURES.append(label)


def test_experience():
    """One entry per defect, in one shape, with a lesson in each.

    The page is a log of concrete defects found in cvc5, so what is checked is
    that every entry looks like every other one: the same field block, a summary
    short enough to read, and a `Learned:` saying what the check got right or
    wrong. The template is checked as well as the entries, because there may be
    no new entry for a long time and the template is what the next run copies.
    """
    print("the experience log:")
    LIMIT, SENTENCES = 250, 2
    ROWS = ("Status", "Identity", "Found by", "In cvc5", "Attribution")
    PROSE = ("Summary:", "What was wrong:", "Learned:")
    raw = read(EXPERIENCE)
    text = re.sub(r"```.*?```", "", raw, flags=re.S)  # not the template
    check("it says where the log stands",
          "## Where this stands" in text, "no such section")
    check("it says how it is maintained, at the foot",
          "## How this page is maintained" in text, "no such section")
    # The template is the pattern. A reader should be able to see it without
    # reverse-engineering it from the entries, and the next run copies it.
    template = re.search(r"```text\n(.*?)\n```", raw, re.S)
    body = template.group(1) if template else ""
    check("the template carries every field block row",
          bool(template) and all(f"**{r}**" in body for r in ROWS),
          "the field block is what makes the pattern visible")
    check("the template carries every prose field",
          bool(template) and all(f"**{f}**" in body for f in PROSE),
          "a section with no Learned: records an event and not a lesson")

    entries = re.split(r"^### (?=\d{4}-\d{2}-\d{2} )", text, flags=re.M)[1:]
    if not entries:
        print("  ok   nothing found yet, so there is no entry to check")
        return
    print(f"  ok   {len(entries)} entries")
    for entry in entries:
        title = entry.splitlines()[0].strip()
        short = title[:60]
        check(f"{short}: says what the defect was, not just a date",
              len(title.split("—", 1)[-1].strip()) > 10, title)
        for row in ROWS:
            n = len(re.findall(rf"^\| \*\*{re.escape(row)}\*\* \|", entry, re.M))
            check(f"{short}: one **{row}** row", n == 1, f"found {n}")
        for field in PROSE:
            n = len(re.findall(rf"^\*\*{re.escape(field)}\*\*", entry, re.M))
            check(f"{short}: one **{field}**", n == 1, f"found {n}")
        # An entry ties itself to something checkable: a database identity, a
        # filed finding id, or an em dash opening an explicit statement that
        # there is neither. "No observation, and here is why" is a better answer
        # than a bare dash, so the dash only has to come first.
        ident = re.search(r"^\| \*\*Identity\*\* \| (.+?) \|", entry, re.M)
        check(f"{short}: the identity is a row, a finding id, or an explicit none",
              bool(ident) and bool(re.search(r"dokimasia:[0-9a-f]{8,}|`[fi]-\d+`|^—",
                                             ident.group(1).strip())),
              ident.group(1) if ident else "no Identity row")
        m = re.search(r"^\*\*Summary:\*\*(.*?)(?=\n\*\*|\n\|)", entry, re.M | re.S)
        if m:
            s = " ".join(m.group(1).split())
            check(f"{short}: the summary is {LIMIT} characters at most",
                  len(s) <= LIMIT, f"{len(s)}")
            check(f"{short}: the summary is {SENTENCES} sentences at most",
                  len(re.findall(r"[.!?](?:\s|$)", s)) <= SENTENCES, s[:80])


def test_launcher():
    """The preview runs anywhere, writes nothing, and keeps the load-bearing rules."""
    print("\nthe closure launcher:")
    script = os.path.join(ROOT, "prompts", "close_bug_db")
    # Read from outside the repository, to prove the launcher resolves its own
    # paths rather than the ones it happens to be standing in.
    watched = {name: read(os.path.join(ROOT, name))
               for name in ("bug_db/bugs.json", "bug_db/bugs.md", "docs/experience.md")}
    p = subprocess.run([sys.executable, script, "--show-prompt"],
                       capture_output=True, text=True, cwd=os.path.dirname(ROOT))
    # cvc5 is not a dependency of this launcher, so the preview owes no excuse
    # on a machine with no checkout: it reads this repository and prints.
    check("the prompt previews with no cvc5 anywhere", p.returncode == 0,
          p.stderr.strip()[:200])
    if p.returncode != 0:
        return
    for phrase, why in (
            ("Absence closes nothing", "absence is the one thing that must not close a row"),
            ("https://github.com/cvc5/cvc5/compare/",
             "the default run reads the history where it is public"),
            ("pages at 250 commits",
             "a window read in pieces must be reported as one, not as complete"),
            ("Confirm the closure in the current source",
             "a commit message is not evidence that a claim is now false"),
            ("closed_commit", "a closure names the commit that made it"),
            ("docs/experience.md", "the write-up is half of what a run produces"),
            ("Commit nothing and push nothing", "the run leaves a diff, not history")):
        check(f"the prompt says: {phrase}", phrase in p.stdout, why)
    # The window is resolved, not described: a prompt that names no revision is
    # asking an assistant to go and decide for itself what "recent" means.
    check("the prompt names the revisions it resolved",
          len(set(re.findall(r"\b[0-9a-f]{40}\b", p.stdout))) >= 1,
          "no full revision in the prompt")
    check("the prompt does not assume a checkout",
          "--use-local" not in p.stdout and "git -C" not in p.stdout,
          "the default prompt reads github, so it names no local tree")
    check("the prompt says how much is on the table",
          bool(re.search(r"holds \d+\s*\n?observations", p.stdout)),
          "the prompt does not say how many observations there are")
    changed = [name for name, before in watched.items()
               if read(os.path.join(ROOT, name)) != before]
    check("previewing changed no record", not changed, f"{changed}")


def test_local_mode():
    """`--use-local` swaps in a checkout, and refuses one that is not cvc5."""
    print("\nthe local optimisation:")
    script = os.path.join(ROOT, "prompts", "close_bug_db")
    p = subprocess.run([sys.executable, script, "--use-local", ROOT, "--dry-run"],
                       capture_output=True, text=True)
    check("a checkout that is not cvc5 is refused", p.returncode == 2, p.stdout[:120])
    check("and the refusal names the tree it was given",
          ROOT in p.stderr and "cvc5 checkout" in p.stderr, p.stderr.strip()[:160])


def test_facets():
    """`docs/README.md` is the register of facets; the index quotes its size.

    Two copies of one fact, and the smaller one is the one nobody re-counts: the
    index said sixteen while the catalogue carried seventeen rows and an
    eighteenth facet was publishing results with no row at all. So the count is
    read from the catalogue rather than trusted, and every prefix that reports a
    measurement must be a prefix the catalogue declares.
    """
    print("\nthe check catalogue:")
    words = {13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
             17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty"}
    text = read(CHECKS)
    catalogue = re.findall(r"^\| [✅◐○] \| `([A-Z]+)` \|", text, re.M)
    produced = re.findall(r"^\| `([A-Z]+)` \| `dokimasia\.[a-z]+` \|", text, re.M)
    check("the catalogue was found at all", len(catalogue) > 5,
          f"{len(catalogue)} rows")
    undeclared = sorted(set(produced) - set(catalogue))
    check("every facet with a result has a catalogue row", not undeclared,
          f"{undeclared} report a measurement and are in no row")
    want = words.get(len(catalogue))
    check(f"the index says the catalogue's size ({len(catalogue)})",
          bool(want) and f"the {want} facets" in read(INDEX),
          f"docs/README.md does not say 'the {want} facets'")


if __name__ == "__main__":
    test_experience()
    test_launcher()
    test_local_mode()
    test_facets()
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
