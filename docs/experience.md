# Experience: what cvc5 did with what we found

A living log of **the cvc5 changes that closed a recorded observation** — one
section per cvc5 pull request, newest first, written in the same run that marks
the closure in [`bug_db/bugs.json`](../bug_db/bugs.json).

**What it is for.** A static analyzer can produce findings forever without any
of them being worth producing. The one external signal that a check points at
something real is that somebody who did not run it changed the code anyway. This
file is where that signal is legible: each entry is a change cvc5 made, said at
a level somebody who works on neither project can read, with what it says about
the check underneath it. A check whose observations nothing ever closes is a
check measuring something nobody agrees is wrong, and that shows up here as
silence.

**Attribution is secondary, and recorded anyway.** Whether cvc5 made the change
because we reported it or found it themselves, the observation is closed either
way and the check was pointing at something real either way. Only the first is
also evidence that the *reporting* works. So the field says which, in one line,
and nothing here argues for credit.

**This is not the record of the claim.** That is
[`bug_db/`](../bug_db/README.md): the identity, the original claim, the dates,
the archived evidence, and the `closed_on` / `closed_commit` / `closed_pr` /
`closed_why` fields a closure adds to an entry. The database says *that* a
change closed an observation and which change it was; this file says what it
meant. An entry here without a closed identity behind it is a story, and the
database is what keeps it honest.

**Who writes it.** [`prompts/update_bug_db`](../prompts/update_bug_db), which
reads a window of cvc5 history against the revision the observations were taken
at and leaves both files changed and uncommitted. A maintainer reads the diff.
No entry is written by hand, and none is written for a closure the database does
not carry.

## The shape of an entry

One section per pull request, whatever number of observations it closed, because
the unit of the thing that happened is the change and not the row.

```text
## <date> — cvc5 #<pr> — <what the change was>

**Commit:** <full sha> — <the commit subject>

**Closed:** <identity (code)>, <identity (code)>, …

**Summary:** what was actually wrong with the software, for somebody who works
on neither project: no identities, no check codes, no procedure. **Two
sentences, 250 characters at most.**

**What the change did:** the mechanism, at the level of the code somebody would
have had to read to write it. Long enough to be checkable against the diff.

**Attribution:** cites us | independent | cannot tell — and what that rests on.

**Learned:** what this says about the check that produced the observation —
whether it was pointing where we thought, what it over- or under-claimed, and
what would have made the row easier for cvc5 to act on.
```

`Learned:` is the field that makes this a post-mortem rather than a changelog,
and it is the one a run drops first when a window is thin. A section without it
records that something happened and nothing about what to do differently.

## Where this stands

**Nothing has been closed yet.** No run of `prompts/update_bug_db` has recorded
a closure, so the log below is empty because there is nothing in it — not
because nobody wrote it up. The first closure writes the first entry.

## The log
