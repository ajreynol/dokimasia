"""Tests for the outbound workflow: the prompts, and the postmortem log.

The two scripts under `scripts/` hold a copy of the prompts in
`docs/workflows.md` so that nobody has to paste one. A copy that has drifted is
worse than no copy, because the drift is invisible from the side that matters:
somebody in cvc5 reading a prompt they were sent. So the document is the
definition and this compares the scripts to it, in every form either can take.

The postmortem log's own shape is checked here too -- the half of it a reader
cannot enforce by reading, since a convention nothing checks is a wish.

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
         ["scripts/check_dokimasia", "--show-prompt", "ID"],
         resolve(one, SWEEP, alt=False),
         lambda s: s.replace("dokimasia-ID", "BRANCH")),
        ("check_dokimasia, the sweep",
         ["scripts/check_dokimasia", "--show-prompt"],
         resolve(one, SWEEP, alt=True),
         lambda s: s.replace("dokimasia-findings", "BRANCH")),
        ("process_dokimasia, one row",
         ["scripts/process_dokimasia", "--show-prompt", "--link", "LINK", "ID"],
         two_form(False, False), lambda s: s),
        ("process_dokimasia, every block",
         ["scripts/process_dokimasia", "--show-prompt", "--link", "LINK"],
         two_form(True, False), lambda s: s),
        ("process_dokimasia --no-postm",
         ["scripts/process_dokimasia", "--show-prompt", "--no-postm",
          "--link", "LINK", "ID"],
         two_form(False, True), lambda s: s),
        # The checkout form: the opening differs by design, the rest may not.
        ("process_dokimasia, from a checkout",
         ["scripts/process_dokimasia", "--show-prompt", ROOT, "ID"],
         from_read(two_form(False, False)),
         lambda s: from_read(s) if "Read it as two things." in s else s),
    ]
    for label, argv, want, fix in cases:
        same(label, want, fix(spoken(argv)))


def test_postmortem():
    """One field block per run, none on the sections beneath, summary short."""
    print("\nthe postmortem log:")
    LIMIT, SENTENCES = 250, 2
    text = re.sub(r"```.*?```", "", read(POSTMORTEM), flags=re.S)  # not the template
    check("it says where the workflow stands",
          "## Where the workflow stands" in text, "no such section")

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
        m = re.search(r"^\*\*Summary:\*\*(.*?)(?=\n\*\*|\Z)", head, re.M | re.S)
        if m:
            s = " ".join(m.group(1).split())
            check(f"{title}: the summary is {LIMIT} characters at most",
                  len(s) <= LIMIT, f"{len(s)}")
            check(f"{title}: the summary is {SENTENCES} sentences at most",
                  len(re.findall(r"[.!?](?:\s|$)", s)) <= SENTENCES, s[:80])


if __name__ == "__main__":
    test_prompts()
    test_postmortem()
    print()
    if FAILURES:
        print(f"FAILED: {len(FAILURES)}: {', '.join(FAILURES)}")
        sys.exit(1)
    print("all checks passed")
