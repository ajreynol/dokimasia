# Experience: every interaction we have had with cvc5

One entry per episode, oldest first, numbered `E1` upward. **An episode is
something that passed between this repository and cvc5** — an observation cvc5
closed, an ask cvc5 accepted or rejected, or a question cvc5 put to us. Each is
self-contained and carries what we learned from it.

**A mistake of ours is an episode only when cvc5 was the one to catch it.**
`E14` is here because we filed a claim and cvc5 contradicted it. A claim we
caught ourselves, a check that broke because cvc5 renamed something, a baseline
that was typed rather than generated — those are defects in the analyzer, and
**they are not tracked in prose at all**: the correction lands in the tool and
in a test, which is the only record that cannot go stale. The test this page
applies is whether **a cvc5 maintainer spent attention on it**.

Ids are allocated above the highest ever used and are never reused. Nothing is
edited away: an entry that turns out wrong gains a later entry correcting it,
and both stay. Instructions for adding one are at the foot.

This is not the record of an observation — that is `bug_db/`, which holds
identities, dates, archived evidence and the `closed_*` fields a closure adds.
The open hypotheses that have not yet become an episode are the register in
`docs/README.md`.

**3 episodes so far, and 2 of 3 are negative** — all from the same week, and
none is a proof hole. Of the three, one was cvc5 accepting something and two
were cvc5 telling us we were wrong. That is the honest summary of what this
repository has cost cvc5 and returned to them to date.

The numbering starts at `E9` because `E1`–`E8` and `E11`–`E13` were withdrawn on
2026-09-19: they recorded corrections cvc5 was never party to. **A pull request
of ours that cvc5 has not merged is not an episode either**, however far along
it is — it becomes one when it lands, which is why cvc5's branch removing the
dead includes is described under `f-1` in `docs/README.md` and not here. Their
ids stay spent, as ids here always do.
## E9: cvc5 documented the argument `SUBS`'s checker had always read

| | |
| --- | --- |
| **When** | 2026-09-19 |
| **Kind** | positive — an observation closed, citing us |
| **Ours** | `dokimasia:398b7ed5b492831606d98491` (`SIG0003`), register row `i-21` |
| **cvc5** | [#12948](https://github.com/cvc5/cvc5/pull/12948), `6e62c7cf595273b7fdfdc0a607aa53a8555530ee` |
| **Outcome** | closed; the pull request reads *"Based on an initial pass from ajreynol/dokimasia"* |

**What happened.** cvc5's substitution proof rule takes a third argument that
selects how the substitutions are applied, and its reference documentation
described only two. The `\inferrule` block read
`\inferrule{F_1 \dots F_n \mid t, ids?}` while
`BuiltinProofRuleChecker::checkInternal` had all along asserted
`1 <= args.size() && args.size() <= 3` and read `args[2]` as a second
`MethodId`. cvc5 rewrote the block to name `ida`, restated the conclusion, and
named the three modes with the termination condition `SBA_FIXPOINT` requires.
**The checker was not touched; the documentation was brought up to it.**

**What we learned.** `SIG0003` compares two partial parsers — LaTeX on one side,
`Assert`s and subscript reads on the other — and the worry was that a
disagreement between two approximations is an artifact. Here it was not, and the
fix landed on the side the check named. What made the row actionable is worth
copying: it named one rule, one file and two numbers to compare, so confirming
it took reading a single comment and a single `else if`. The 24 `SIG0002` rows
name a skolem and a file but no comparable discriminator, and none of them
moved.

## E10: cvc5 decided to keep proof-completeness checking an expert option

| | |
| --- | --- |
| **When** | 2026-09-19 |
| **Kind** | negative — our ask was rejected, and rightly |
| **Ours** | `i-3` / `R2`, second form |
| **cvc5** | built at `a960d7d7210e731cf48ad7baa6ad42fc7345b297` and reverted at `215eed21a6c8380075c46513e69181a295b6e3b2`, both on the answering branch; `main` still has `category = "expert"` |
| **Outcome** | withdrawn; only the assertion form of the ask survives |

**What happened.** We asked cvc5 to drop `checkProofsComplete` from the
`expert` category so the safe-mode tester could name the guarantee it tests.
cvc5 built the promotion, reproduced its effect, and reverted it: an option's
category governs **both** assignments, so making it settable in safe mode
equally permits `--no-check-proofs-complete` and
`(set-option :check-proofs-complete false)`, and `setDefaultsPre` honours an
explicit user assignment through `checkProofsCompleteWasSetByUser`. The
promotion would have turned a guarantee safe mode switches on into one a user
can switch off.

**What we learned.** **The expert refusal is the mechanism that keeps
completeness non-negotiable, and we read it as an obstacle to stating it.** We
reasoned from *the positive flag is refused* to *the option should be settable*
without asking what else becomes settable, and one `--no-` run would have shown
it — our own report set the bar it failed, at *"a maintainer can refute this in
thirty seconds."* The chain's fifth link, `explicit-completeness`, is withdrawn
from `CiModel.completeness_chain` and its `CI0002` entity retired, since it
asked cvc5 to weaken what we were auditing. The real exposure is untouched and
still worth carrying: completeness in safe mode is obtained by configuration,
and a `--proof-granularity` flag added to the tester would switch it off with no
test failing.

## E14: cvc5 rejected the mechanism we gave for half of `tcb-001`

| | |
| --- | --- |
| **When** | 2026-09-19 |
| **Kind** | negative — a filed claim of ours, contradicted on inspection |
| **Ours** | `f-1` / `tcb-001`, and `Closure.cuts` behind it |
| **cvc5** | the response to `tcb-001`; `theory/arith/proof_checker.cpp`, `theory/datatypes/proof_checker.cpp`, `theory/builtin/proof_checker.cpp` |
| **Outcome** | conceded; `Closure.edge_use` added and the disputed edges pinned by test |

**What happened.** `f-1` said six proof rule checkers include their theory
solvers *to reach `static` helpers parked on solver classes*. cvc5 read it and
answered that the arithmetic checker uses **nothing** from
`linear/constraint.h`, the datatypes checker nothing from `theory/rewriter.h` or
`expr/dtype_cons.h`, and the builtin checker nothing from
`extended_rewrite.h`: those includes were simply dead, and *"removing the
include needs no extraction of solver helpers"*. The refactoring we proposed for
them was work nobody needed to do. The mechanism was right for the strings edge
and asserted of the rest without evidence.

**What we learned.** The measurement could never have supported the claim.
`cuts` weighed an include by how much closure it carried and never asked whether
the file *used* what it included, so a dead include and a load-bearing one
produced identical rows and the prose supplied a mechanism for both — **a
measurement can be exactly right and still carry a wrong story, if the tool
never checked the story.** `Closure.edge_use` now classifies every edge `used`,
`unused` or `unknown`, and `unknown` is never collapsed into `unused`, since
calling a live include dead is the same error reflected. Getting that bias right
took three corrections of its own, each now a named test. The closure figures
were right throughout and are unchanged.

## How this page is maintained

**Who writes it.** `prompts/close_bug_db`, which reads a window of cvc5 history
against the revision the observations were taken at and leaves this file and
`bug_db/bugs.json` changed and uncommitted. A maintainer reads the diff. No
entry is written by hand, and none is written for a closure the database does
not carry.

**When an episode earns an entry.** One test, and it is about cvc5 rather than
about us: **a cvc5 maintainer spent attention on it.** They merged, rejected or
acted on something of ours, or they put a question to us.

What is *not* an episode, with where each belongs instead:

| not an episode | why | where it goes |
| --- | --- | --- |
| a claim of ours we caught ourselves | nobody at cvc5 saw it | nowhere in prose — the corrected tool and its test are the record |
| a check of ours broken by a cvc5 rename | cvc5 renamed its own build types; we broke unaided | what a run learned about itself, in `dokimasia_analyzer/README.md` |
| a pull request of ours cvc5 has not merged | however far along, the decision has not been taken | nowhere yet — it earns an entry when it lands |
| a check that found nothing | that is a result, not an interaction | the measurement tables in `docs/README.md` |
| a hypothesis waiting for a verdict | nothing has happened to it | the register in `docs/README.md` |

**The bar is deliberately high, and the page is short because of it.** A log
padded with our own corrections reads as activity and measures nothing; the
count of entries here is meant to be the count of times this repository was
worth somebody else's time. The one exception is a mistake **cvc5** caught —
that cost them attention, so it counts, and `E14` is the first of them.

**The template.** Copy it exactly. The next id is one above the highest ever
used, including entries that were later corrected; ids are never reused, and an
entry is never deleted or rewritten to say something else — a later entry
corrects it and names the earlier one by id.

```text
## E<n>: <what cvc5 did, as a sentence with cvc5 as the subject where it was>

| | |
| --- | --- |
| **When** | the date, or what it was before if no date is recoverable |
| **Kind** | positive or negative, and in four words why |
| **Ours** | the identity, register row, or tool that carried it — or — |
| **cvc5** | the pull request, commit or files |
| **Outcome** | what state it is in now |

**What happened.** The episode, for somebody who works on neither project: no
check codes in the first sentence, and enough of the mechanism that a reader
could go and check it. Name the commit or the file.

**What we learned.** What this says about the check, the report or the
judgement behind it — what it over- or under-claimed, and what would have
caught it sooner. **This field is why the page exists.** An entry without it
records that something happened and nothing about what to do differently.
```

**Two rules that keep it honest.** Attribution is recorded and never argued:
whether cvc5 made a change because we reported it or found it independently, the
check was pointing at something real either way, and only the first is also
evidence that the *reporting* works. And a closure is a decision about a **cvc5
change**, never about a row going quiet — absence closes nothing, and the claim
has to be re-read in cvc5's current source rather than taken from a commit
message. `tests/test_experience.py` enforces the shape above; the closure rules
live in the launcher and are checked there.
