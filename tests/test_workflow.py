"""Tests for the outbound workflow: the prompts, and the postmortem log.

The two scripts under `scripts/` hold a copy of the prompts in
`docs/workflows.md` so that nobody has to paste one. A copy that has drifted is
worse than no copy, because the drift is invisible from the side that matters:
somebody in cvc5 reading a prompt they were sent. So the document is the
definition and this compares the scripts to it, in every form either can take.

The postmortem log's own shape is checked here too -- the half of it a reader
cannot enforce by reading, since a convention nothing checks is a wish. So is the
check catalogue against the index that quotes its size, for the same reason: a
count in a second document is a copy, and a copy nobody re-counts drifts.

Run: python3 tests/test_workflow.py
"""

import difflib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOWS = os.path.join(ROOT, "docs", "workflows.md")
POSTMORTEM = os.path.join(ROOT, "docs", "postmortem.md")
CHECKS = os.path.join(ROOT, "docs", "checks.md")
INDEX = os.path.join(ROOT, "docs", "README.md")

SWEEP = "-- or, for the sweep form --"
BLOCKS = "-- or, for every block --"
POSTM = "-- or, with --no-postm --"

FAILURES = []


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def check(label, ok, detail=""):
    print(f"  {'ok  ' if ok else 'FAIL'} {label}" + ("" if ok else f": {detail}"))
    if not ok:
        FAILURES.append(label)


def same(label, want, got):
    """Two texts, with the difference printed rather than both of them."""
    if want.strip() == got.strip():
        print(f"  ok   {label}")
        return
    FAILURES.append(label)
    print(f"  FAIL {label} has drifted from docs/workflows.md")
    for line in difflib.unified_diff(want.strip().splitlines(),
                                     got.strip().splitlines(),
                                     "document", "script", lineterm=""):
        print(f"       {line}")


def body(doc, start, end):
    """The fenced prompt between two headings."""
    chunk = doc[doc.index(start):doc.index(end)]
    return re.search(r"```text\n(.*?)\n```", chunk, re.S).group(1)


def resolve(text, marker, alt):
    """Keep one side of an alternatives block and drop the marker.

    The block is the run of lines before the marker back to the last blank line,
    the marker, and the run after it up to the next blank line. Written this way
    so the comparison can cover every line of a prompt rather than anchoring
    part way down and leaving the rest of it unchecked.
    """
    lines = text.split("\n")
    i = next(k for k, l in enumerate(lines) if l.strip() == marker)
    a = max((k for k in range(i) if not lines[k].strip()), default=-1) + 1
    b = next((k for k in range(i + 1, len(lines)) if not lines[k].strip()), len(lines))
    keep = lines[i + 1:b] if alt else lines[a:i]
    return "\n".join(lines[:a] + keep + lines[b:])


def spoken(argv):
    got = subprocess.run(["bash"] + argv, cwd=ROOT, capture_output=True, text=True)
    if got.returncode != 0:
        return f"!! {argv[0]}: {(got.stderr or got.stdout).strip()[:200]}"
    return got.stdout


def from_read(text):
    """Prompt two below its opening, which the script and the document word
    differently on purpose -- the document says paste a link, the script has
    usually resolved a checkout already."""
    return text[text.index("Read it as two things."):]


def test_prompts():
    print("the outbound prompts:")
    doc = read(WORKFLOWS)
    one = body(doc, "## Prompt one", "## Prompt two")
    two = body(doc, "## Prompt two", "### Keeping them in step")

    def two_form(scope_alt, postm_alt):
        return resolve(resolve(two, BLOCKS, scope_alt), POSTM, postm_alt)

    cases = [
        ("check_dokimasia, one row",
         ["prompts/check_dokimasia", "--show-prompt", "ID"],
         resolve(one, SWEEP, alt=False),
         lambda s: s.replace("dokimasia-ID", "BRANCH")),
        ("check_dokimasia, the sweep",
         ["prompts/check_dokimasia", "--show-prompt"],
         resolve(one, SWEEP, alt=True),
         lambda s: s.replace("dokimasia-findings", "BRANCH")),
        ("process_dokimasia, one row",
         ["prompts/process_dokimasia", "--show-prompt", "--link", "LINK", "ID"],
         two_form(False, False), lambda s: s),
        ("process_dokimasia, every block",
         ["prompts/process_dokimasia", "--show-prompt", "--link", "LINK"],
         two_form(True, False), lambda s: s),
        ("process_dokimasia --no-postm",
         ["prompts/process_dokimasia", "--show-prompt", "--no-postm",
          "--link", "LINK", "ID"],
         two_form(False, True), lambda s: s),
        # The checkout form: the opening differs by design, the rest may not.
        ("process_dokimasia, from a checkout",
         ["prompts/process_dokimasia", "--show-prompt", ROOT, "ID"],
         from_read(two_form(False, False)),
         lambda s: from_read(s) if "Read it as two things." in s else s),
    ]
    for label, argv, want, fix in cases:
        same(label, want, fix(spoken(argv)))


def test_debts(text):
    """Every booked debt names what would settle it.

    A debt with no settling condition is a complaint that has been written down,
    and the whole reason for booking these before the first round is that the
    first round is then measured against a record that already knows what it is
    missing. The section may be empty; a row in it may not be half-written.
    """
    chunk = text.partition("## Open debts")[2].partition("\n## ")[0]
    if not chunk.strip():
        print("  ok   no debts booked")
        return
    rows = [r for r in re.findall(r"^\| (.+?) \| (.+?) \|\s*$", chunk, re.M)
            if not set(r[0].strip()) <= {"-"} and r[0].strip() != "debt"]
    check("at least one debt is booked", bool(rows), "the table has no rows")
    for what, settles in rows:
        name = " ".join(what.split())[:56]
        check(f"the debt '{name}' names what settles it",
              len(settles.strip()) > 10, f"{settles.strip()!r}")


def test_postmortem():
    """One field block per run, none on the sections beneath, summary short."""
    print("\nthe postmortem log:")
    LIMIT, SENTENCES = 250, 2
    raw = read(POSTMORTEM)
    text = re.sub(r"```.*?```", "", raw, flags=re.S)  # not the template
    check("it says where the workflow stands",
          "## Where the workflow stands" in text, "no such section")
    # The field that makes an entry a postmortem rather than a log. It is the
    # one a copy of somebody else's template loses silently, so the template is
    # checked as well as the entries -- there may be no entries for a long time.
    template = re.search(r"```text\n(.*?)\n```", raw, re.S)
    check("the entry template carries **Learned:**",
          bool(template) and "**Learned:**" in template.group(1),
          "a section with no Learned: records an event and not a lesson")
    test_debts(text)

    runs = re.split(r"^## (?=\d{4}-\d{2}-\d{2} )", text, flags=re.M)[1:]
    if not runs:
        print("  ok   no runs logged yet, so there is no entry to check")
        return
    for run in runs:
        title = run.splitlines()[0].strip()
        head, _, rest = run.partition("\n### ")
        for field in ("Tool:", "Summary:", "Resolution:"):
            n = len(re.findall(rf"^\*\*{field}\*\*", head, re.M))
            check(f"{title}: one **{field}** above the sections", n == 1, f"found {n}")
        stray = sorted(set(re.findall(r"^\*\*(Tool|Summary|Resolution):\*\*", rest, re.M)))
        check(f"{title}: no fields on the sections beneath", not stray, f"{stray}")
        for section in ("### " + s for s in rest.split("\n### ") if s.strip()):
            name = section.splitlines()[0][4:].strip()
            n = len(re.findall(r"^\*\*Learned:\*\*", section, re.M))
            check(f"{title}: '{name}' says what was learned", n == 1, f"found {n}")
        m = re.search(r"^\*\*Summary:\*\*(.*?)(?=\n\*\*|\Z)", head, re.M | re.S)
        if m:
            s = " ".join(m.group(1).split())
            check(f"{title}: the summary is {LIMIT} characters at most",
                  len(s) <= LIMIT, f"{len(s)}")
            check(f"{title}: the summary is {SENTENCES} sentences at most",
                  len(re.findall(r"[.!?](?:\s|$)", s)) <= SENTENCES, s[:80])


def test_facets():
    """`docs/checks.md` is the register of facets; the index quotes its size.

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
    test_prompts()
    test_postmortem()
    test_facets()
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
