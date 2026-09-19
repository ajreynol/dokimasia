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

**Who writes it.** [`prompts/close_bug_db`](../prompts/close_bug_db), which
reads a window of cvc5 history against the revision the observations were taken
at and leaves both files changed and uncommitted. A maintainer reads the diff.
No entry is written by hand, and none is written for a closure the database does
not carry.

## What a run learned about itself

Salvaged from the retired `postmortem.md`, which asked a question no other file
here asks and which the [reporting removal](../TODO.md#reporting) dropped
without a successor: *what did working this run teach us about how we work* —
as against `Learned:`, which is about the check that produced the observation.
A window turns up facts about our own tooling that belong to no pull request and
so fit in no entry below. They go here, newest first, one line each, and an empty
section is the honest state when a run turned up nothing.

**2026-09-19, window `40a4bb7e4..dbf176dfb`.**

- **The `ci` check's mode heuristic broke silently on a cvc5 rename.**
  `Job.mode` in `dokimasia/ci/scan.py` keys on the literal substrings
  `safe-mode` / `stable-mode` in a matrix `config:` value; cvc5 #12899 renamed
  those values to `safe` / `stable`. The safe-mode job is still there and still
  runs `--tester proof`, but the check now classifies every job `unrestricted`,
  which silently disarms `CI0001` and makes two links of the `CI0002` chain read
  `NO` for a reason that has nothing to do with cvc5. **A check keyed on a
  spelling cvc5 is free to change will fail open, and this one did.**
- **Two of the window's four candidate closures were entity renames.** cvc5
  #12906 renamed the CI job names carrying all four `CI0004` rows, and #12901
  renamed the `InferenceId` carrying an `INFERID0001` row — in both cases the
  condition moved intact under a new name. A re-run will read both as
  disappearances. *Absence closes nothing* is the rule that caught this; what it
  cost was re-deriving each claim by hand, because nothing in the record links
  an identity to its renamed successor.
- **A retraction went stale in our favour.** [`findings.md`](findings.md#retractions)
  records that our baselines named `SETS_RELS_TCLOSURE_DOWN`, and that **no such
  id has ever existed in cvc5**. That was true when written. As of #12901 the id
  exists, because cvc5 renamed `TCLOSURE_UP` to it. The retraction stays — it is
  the record of an error we made — but it now needs the date qualifier it did
  not need before.

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

**One observation closed, out of 197.** The first window read — cvc5
`40a4bb7e4..dbf176dfb`, 42 commits — closed a single row, and the log below has
the one entry that window earned. A thin log is the honest reading of a thin
window, not a backlog of write-ups nobody got to.

## The log

## 2026-09-19 — cvc5 #12948 — `SUBS`'s documentation gains the argument its checker already read

**Commit:** `6e62c7cf595273b7fdfdc0a607aa53a8555530ee` — Minor simplifications to trust ids and proof docs (#12948)

**Closed:** `dokimasia:398b7ed5b492831606d98491` (`SIG0003`)

**Summary:** cvc5's substitution proof rule takes a third argument that selects
how the substitutions get applied, but its reference documentation described
only two. A reader building or auditing such a proof would not have known the
argument was there.

**What the change did:** the `\inferrule` block above `EVALUE(SUBS)` in
`include/cvc5/cvc5_proof_rule.h` read `\inferrule{F_1 \dots F_n \mid t, ids?}`,
and its prose said the substitutions are "applied in reverse order" as though
that were the only possibility. `BuiltinProofRuleChecker::checkInternal` has all
along asserted `1 <= args.size() && args.size() <= 3` and read `args[2]` as a
second `MethodId`, `ida`, defaulting to `SBA_SEQUENTIAL`. The commit rewrote the
block to `\inferrule{F_1 \dots F_n \mid t, ids?, ida?}`, restated the
conclusion as `\texttt{apply}_{ida}(t, \sigma_{ids}(F_1), \dots)`, and named
the three modes — `SBA_SEQUENTIAL`, `SBA_SIMUL`, `SBA_FIXPOINT` — with the
termination condition the fixpoint mode requires. The checker was not touched;
the documentation was brought up to it. The same pull request also deleted four
dead `TrustId`s and fourteen unproduced `InferenceId`s, which closed nothing
here: none of those ids carried an observation.

**Attribution:** cites us. The pull request body reads, in full, "Based on an
initial pass from https://github.com/ajreynol/dokimasia". The observation had
also been written up as `i-21` in the [issue register](issues.md).

**Learned:** the check was pointing exactly where it claimed to. `SIG0003`
compares two partial parsers — LaTeX on one side, `Assert`s and subscript reads
on the other — and its recorded limitation says so; the worry was that a
disagreement between two approximations is an artifact rather than a finding.
Here it was not: the documented argument count was genuinely short of what the
checker reads, and the fix landed on the documentation side, which is where the
check said the error was. Worth noting what made this row actionable where
others in the same facet are not — it named one rule, one file, and two concrete
numbers to compare (`(2, 1)` documented against an `args[2]` read), so
confirming it took reading a single comment and a single `else if`. The 24
`SIG0002` rows in the same facet name a skolem and a file but no comparable
discriminator, and none of them moved. That `i-20` had to be ground down through
five rounds of parser fixes to leave this one residue is the other half of the
lesson: a check whose output is mostly its own parsing noise buys its findings
expensively, and cvc5 still states rule arity in LaTeX only, so the next such
row costs the same.
