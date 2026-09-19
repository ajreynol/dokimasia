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
    """One numbered episode per interaction with cvc5, all in one shape.

    The page is a list of self-contained case studies, so what is checked is
    that it stays a list: nothing but `E<n>:` headings and the maintenance
    footnote, ids allocated upward and never reused, and every entry carrying
    the same five-row block and the same two prose fields. The template is
    checked as well as the entries, because it is what the next run copies.
    """
    print("the experience log:")
    LIMIT = 4
    ROWS = ("When", "Kind", "Ours", "cvc5", "Outcome")
    PROSE = ("What happened.", "What we learned.")
    FOOT = "## How this page is maintained"
    raw = read(EXPERIENCE)
    text = re.sub(r"```.*?```", "", raw, flags=re.S)  # not the template

    # The shape is the point: a reader should see one pattern repeated and
    # nothing else competing with it.
    heads = re.findall(r"^## (.+)$", text, re.M)
    stray = [h for h in heads
             if not re.match(r"E\d+: ", h) and h != FOOT[3:]]
    check("the only headings are the episodes and the footnote", not stray, stray)
    check("the footnote is last",
          heads and heads[-1] == FOOT[3:], heads[-1] if heads else "none")
    deep = re.findall(r"^#{3,6} .*$", text, re.M)
    check("no heading below the episodes", not deep, deep[:3])

    ids = [int(m) for m in re.findall(r"^## E(\d+): ", text, re.M)]
    check("ids are unique", len(set(ids)) == len(ids), ids)
    check("ids ascend, so the next one is one above the highest",
          ids == sorted(ids), ids)

    template = re.search(r"```text\n(.*?)\n```", raw, re.S)
    body = template.group(1) if template else ""
    check("the template carries every block row",
          bool(template) and all(f"**{r}**" in body for r in ROWS),
          "the block is what makes the pattern visible")
    check("the template carries both prose fields",
          bool(template) and all(f"**{f}**" in body for f in PROSE),
          "an entry with no lesson records an event and not an episode")

    entries = re.split(r"^## (?=E\d+: )", text, flags=re.M)[1:]
    entries = [e for e in entries if not e.startswith("How this page")]
    if not entries:
        print("  ok   nothing has happened yet, so there is no entry to check")
        return
    print(f"  ok   {len(entries)} episodes")
    for entry in entries:
        eid = entry.split(":", 1)[0]
        title = entry.splitlines()[0]
        check(f"{eid}: the heading says what happened",
              len(title.split(":", 1)[1].split()) >= 5, title)
        for row in ROWS:
            n = len(re.findall(rf"^\| \*\*{re.escape(row)}\*\* \|", entry, re.M))
            check(f"{eid}: one **{row}** row", n == 1, f"found {n}")
        for field in PROSE:
            n = len(re.findall(rf"^\*\*{re.escape(field)}\*\*", entry, re.M))
            check(f"{eid}: one **{field}**", n == 1, f"found {n}")
        # Positive or negative, never unlabelled: the ratio of the two is the
        # most useful thing the page reports about itself.
        kind = re.search(r"^\| \*\*Kind\*\* \| (.+?) \|", entry, re.M)
        check(f"{eid}: the kind is positive, negative or neutral",
              bool(kind) and kind.group(1).split()[0].strip("*") in
              ("positive", "negative", "neutral"),
              kind.group(1) if kind else "no Kind row")
        # An episode is self-contained: it says what it was about without
        # sending the reader to another document to find out.
        learned = re.search(r"^\*\*What we learned\.\*\*(.*?)(?=\n\n\#\#|\Z)",
                            entry, re.M | re.S)
        check(f"{eid}: the lesson is at least a few sentences",
              bool(learned) and len(learned.group(1).split()) >= 25,
              len(learned.group(1).split()) if learned else 0)
        words = len(entry.split())
        check(f"{eid}: the entry stays readable in one sitting",
              words <= 600, f"{words} words")
    # The page opens with the ratio. A count in prose is a copy, and a copy
    # nobody re-counts drifts -- this one was wrong within a minute of writing.
    neg = sum(1 for e in entries if re.search(r"\| \*\*Kind\*\* \| negative", e))
    stated = re.search(r"\*\*(\d+) of (\d+) are negative", text)
    check("the page states its own ratio",
          bool(stated), "no 'N of M are negative' claim in the opening")
    if stated:
        check(f"the stated ratio is the counted one ({neg} of {len(entries)})",
              (int(stated.group(1)), int(stated.group(2))) == (neg, len(entries)),
              f"page says {stated.group(1)} of {stated.group(2)}")


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
