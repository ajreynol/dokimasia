# dokimasia — the analyzer, and why it is built this way

The Python package: thirteen analyses over cvc5's proof-production source, each
reading a checkout in seconds and building nothing. **This page is the design
philosophy** — what counts as a finding, what we promise about publishing one,
and the bar it clears before anybody carries it to cvc5.

Two other pages complete the picture and neither is repeated here: the argument
for the whole repository, the check catalogue and the register of what we ask
cvc5 to act on are in `docs/README.md`; the concrete
defects this has actually found in cvc5, and what cvc5 did about them, are in
`docs/experience.md`. Commands are in
`docs/maintenance.md`.

## The modules

| module | answers |
| --- | --- |
| [`tcb`](tcb/) | the proof checker's dependency closure, and what each edge costs |
| [`ledger`](ledger/) | one row per `ProofRule`: produced, checked, elaborated, printed |
| [`trust`](trust/) | every `TrustId` construction site, and the preprocessing correspondence |
| [`inferid`](inferid/) | whether each `InferenceId` names one program point |
| [`infer`](infer/) | whether every inference a theory makes has a proof reconstruction |
| [`rewrites`](rewrites/) | the rewrite vocabulary, RARE vs hand-written vs applied |
| [`modes`](modes/) | what safe and stable mode change about the defaults |
| [`ci`](ci/) | whether cvc5's proof testing is still attached |
| [`signature`](signature/) | whether the Eunoia signature agrees with cvc5's account of a rule |
| [`gates`](gates/) | which option legalises each term kind, and so each rewrite rule |
| [`fragment`](fragment/) | the supported fragment per theory, and whether it is enforced |
| [`buildmode`](buildmode/) | is a safe *build* still an unrestricted build with one default flipped? |
| [`latent`](latent/) | the static inventory minus what a corpus reached |

Nine are advertised and emit observations; standalone `gates`, `fragment`,
`tcb` and `latent` reports are developer measurements that emit none.
[`findings.py`](findings.py) owns the check catalogue and the identity scheme;
[`sanity.py`](sanity.py) holds the expectations that make a scanner fail loudly
rather than return a confidently empty answer.

## What a finding is

The reviewed ledger: what a finding is, what clears the bar to be carried to
cvc5, and the log of what has been filed and what has been retracted. Raw run
observations live in `bug_db/`; what cvc5 has since done
about them is `experience.md`.

Four kinds, extending anoieu's three:

| | kind | what it asks of cvc5 |
| --- | --- | --- |
| **A** | a defect | an incomplete proof, named down to the input that produces it |
| **B** | an adoption | run a check of ours in your CI, with the configuration it needs |
| **C** | a change to the pipeline | to the proof infrastructure or to what safe mode promises |
| **D** | **an assertion** | a patch adding an invariant to cvc5, so the check lives in your tree and not ours |

**Kind A is what this repository is for.** An incomplete proof, named down to
the input that produces it, is the only finding that directly serves
the goal. The other three are instruments: B and D are ways of
making a fix stick, C is a way of changing what the pipeline promises. They are
cheap and worth doing, and none of them is the reason this exists.

A note on D, since it is the most easily overrated: an assertion converts a
silent hole into a loud failure and no more. It does not close a hole — it
closes a *check*. That is the shared position *success is the check being
deleted*, and D is how it happens here: where an invariant we check is one cvc5
could check about itself at startup, the deliverable is the patch and our check
goes with it. See
`docs/maintenance.md`.

## The promises

These originated as the position shared with anoieu, in a
[`reporting-policy.md`](https://github.com/ajreynol/anoieu/blob/06bd7872ea5ce24bf4d264bf5e6958ed8edee3c2/docs/reports/reporting-policy.md)
that anoieu deprecated on 2026-09-18 and **removed on 2026-09-19**. They were
cited here by name and not restated, which left the statement of our own policy
in another repository's deprecated file — and that file no longer exists, so the
citation above is pinned to the last commit it did. They are restated below
because a policy you cannot read without leaving the tree is not one you can be
held to, and a month later the tree you were leaving for may not have it. Cite a
position **by name**, never by number.

The tier says what backs it — **enforced**, something fails when it is broken;
**structural**, the arrangement makes the failure hard rather than impossible;
**intention**, nothing but our record. Several sit a tier above anoieu's because
the mechanism here is a test rather than a habit; where that is so, the test is
named, and a tier with no mechanism beside it is an intention wearing a better
word.

| | position | tier here | what backs it |
| --- | --- | --- | --- |
| **1** | **Silence is never evidence** | structural | where a check reports nothing, the most that may be said is that *those checks reported nothing*. Every code in the check catalogue carries a limitation column, and every archived observation a `limitation` field |
| **4** | **Publish a candidate; carry a finding** | structural | candidates live in `bug_db/` under their own header; findings live in the log below. Promoting one takes a deliberate act in a different file, not a slip |
| **5** | **Presence is not reachability** | structural | *"this rule has no checker"* and *"and an ordinary run emits it"* are different claims, and only the second is worth somebody's time. what the corpus reaches (`docs/maintenance.md`) is the measurement that separates them; the 182 latent holes are what it found |
| **6** | **A false positive is ours — and so is anything we asked cvc5 to run** | enforced, for the half that can be | a check that fired wrongly is narrowed until it stops, and the narrowing is recorded in the retractions in cvc5's terms rather than kinder ones. Eight `baseline --check` ratchets under `tests/baselines/` fail the build on a change that invents one |
| **7** | **Every claim is re-checkable without us** | enforced | a number carries whatever regenerates it and the revision it was measured at. [`scripts/cvc5.lock`](../scripts/cvc5.lock) pins that revision, `tests/test_pin.py` enforces it, and CI fails if the pin names a commit reachable only on a fork — which is the retraction directly below that bought this rule |
| **8** | **Closing is a verdict, not an absence** | enforced, for the launcher | no row leaves without one recorded, and *"won't fix, because —"* is worth as much as a fix. Koine's writer is additive and cannot delete a row; `tests/test_experience.py` fails if [`prompts/close_bug_db`](../prompts/close_bug_db) stops carrying **Absence closes nothing** and **Confirm the closure in the current source** |
| **9** | **A reply is triage; an artifact settles it** | intention | what comes back from cvc5 is somebody's reading, made quickly and on our word. Here the settling artifact is a **cvc5 commit whose effect is re-read in current source** — not the commit message, and not the row going quiet. Failing to find one settles nothing |

Two more are stated in this file rather than in this table, because they are
load-bearing where they sit: *nothing crosses a repository boundary
automatically* is the bar, and *success is the check being deleted*
is the note on kind D above.

**And two about what we take, rather than what we say.** These came last, as a
section anoieu added on 2026-09-17 and we signed on 2026-09-18; they are here
because the page carrying them was deleted the next day and they would otherwise
survive only inside a piece of correspondence that gets removed when it settles.

| | position | tier here | what backs it |
| --- | --- | --- | --- |
| **13** | **Published is not available** | intention | reading a published tree needs nobody's permission, and making somebody's work the material of an exercise they have no stake in is a different act. The test is *who carries the cost if the output is misread* — for us that is always cvc5, which is the whole reason for the discipline |
| **14** | **Unpublished work is not material** | intention, **with one qualification of ours** | clean when the material is a signature, which is released or not. A source tree has a third state: a personal branch on a public host is published in the only sense a machine can check and unreleased in every sense that matters. We sign this as *unreleased work is nobody's material* — forbidding the exercise nobody asked for, not forbidding an answer to a question somebody asks us about our own registers. Read strictly, with *no balancing test*, we could not sign it as written |

The qualification is not a private reservation: it was put to anoieu when we
signed, and our own `scripts/cvc5.lock` books a reachability census run against
a personal fork as a debt for exactly this reason.

Two things this repository adds, because the subject is a solver rather than a
signature:

- **Carrying a kind A means an input.** Not a code location and an argument — a
  `.smt2` file, an option set, and the quoted `--check-proofs-complete` failure.
  A claim that a path is reachable is worth nothing until something reaches it,
  and the static analysis's job is to tell us *where to look*, not to substitute
  for looking. What evidence each rank needs is set out in
  `docs/maintenance.md`.
- **An assertion is not proposed until it has been run.** The promise is the
  shared one; the precondition is ours. It is applied to a cvc5 build configured
  `--assertions` and the regression suite passes with it in place. An assertion
  we have not run is a hypothesis, and hypotheses go in the register,
  not in a patch.

## The bar

**This repository never opens a pull request against cvc5. No program here
pushes a branch, opens an issue, posts a comment, or touches a tracker. A human
does that, or it does not happen.** A hard rule about the *act*, not about the
judgement: deciding what deserves to go upstream is this repository's job, and
handing back an unranked list for somebody to sort is the work left undone.

Five rules, by name so they can be cited. A candidate is **worth carrying** only
when all five hold.

| rule | it means |
| --- | --- |
| **theirs-not-ours** | it is a defect in cvc5. A parser bug, a stale baseline or a bad assumption of ours is fixed here and logged, never reported |
| **run-it** | every claim about behaviour is backed by a command and its actual output. Static reasoning alone is a hypothesis |
| **cheap-to-refute** | the evidence is a command, a reproducer, or a named line — checkable in minutes, without us |
| **falsifiable** | we have said what would show it is wrong. A claim with no stated falsifier is not finished being thought about |
| **worth-the-attention** | it earns the time it costs. Cleanups are bundled and go *after* something substantive lands, never before |

Every candidate carries exactly one verdict, and every one is recorded.

| verdict | means | lives in |
| --- | --- | --- |
| **carry** | all five hold; a person can take it upstream today | what to carry next (`docs/README.md`), with the packet |
| **not yet** | one or more fail — **name which** | the register, rank and blocking rule on the row |
| **never** | it is ours, or it will never earn the attention | the register or the retraction log |

*Not yet* is the verdict we issue most, and naming the failing rule is what makes
it actionable: it says exactly what work would change the answer.

**The carry packet** is what a person needs in order to act, and no more: the
claim in one sentence and its rank; the command that reproduces it against a
stated commit; the reproducer where the claim is about behaviour — a `.smt2`
file, the option set, the quoted output; what would falsify it; and the patch as
a diff in a file, never as a branch.

### The bar is also a design constraint

**Before building a check, ask what its output would be worth.** If everything a
check can produce would come back *not yet — worth-the-attention*, the check is
not worth building. That single question retires more work than any other test
we have, and it is why `TODO.md` declines a SARIF framework, a
generated check registry, and a `holes/` corpus with no holes in it.

**Design every check with its verification path.** A check that can only ever
produce hypotheses fails **run-it** by construction, and will sit in the register
forever. This is why `dokimasia.latent` ships with
[`scripts/sweep_corpus`](../scripts/sweep_corpus): the static half alone could
never clear the bar, so the runtime half is not an extra, it is what makes the
analysis reportable at all.

**Fix at the source, not in the report.** When a candidate dies because we were
wrong, the deliverable is a corrected *analysis*, not a retraction. `SET_FILTER`
did not just get struck from the register; `Fragment.requires_higher_order` now
recovers the logic-level gate, so the whole class of mistake is gone. A
retraction with no code change behind it means the analysis will make the same
error again. Our own errors go through the same pipeline, inverted: a false
positive is ours by promise, so it is filed against us, tested against the case
that produced it, and logged in the retractions below.

## Why a check and not an answer

**A cvc5 developer asks a design question. We answer it with a check.** That is
the highest-value thing this repository does per hour spent, and the
case studies (`docs/experience.md`) are where the answers land.

A design question from a maintainer — *why can't safe mode have debug symbols?*,
*is this restriction still needed?*, *does this flag still do anything?* — has
three possible answers, and only one of them is worth the exchange.

| answer | worth |
| --- | --- |
| an opinion | nothing. They know the code better than we do |
| a reading of the source | something, once. It is stale the next time somebody edits |
| **an invariant, verified, with the verifier attached** | the answer, *and* the guarantee it stays the answer |

The third is the only one that survives contact with a codebase under
development. It also inverts the usual burden: instead of us asserting something
about their code, they get a thing that will tell them when it stops being true.

### The shape a case follows

Every case follows it, and a new one should:

1. **State the question as the requester asked it**, not as we would rather
   answer it — and state the existing decision as what it is. A deliberate
   simplification is not an oversight, and reading it as one gets the whole case
   wrong. Ask what the decision *costs*, not why it was made.
2. **Find the invariant the answer rests on.** *"Forbidding safe + debug costs
   almost nothing"* rests on *"a safe build differs only in defaults, text and
   reporting"*. The second is checkable; the first is not.
3. **Enumerate exhaustively.** Eight sites, all eight classified. A case that
   says "we looked at the main ones" has not answered anything.
4. **Say where the invariant is imperfect**, in its own section. Every one of
   these has an *almost*, and the almost is usually the interesting part — for
   #12899 it is that the divergence is real but lives in message text the
   regression testers read, so the restriction bites only when debugging a
   safe-mode skip.
5. **Ship the verifier**, with tests that show it firing on each way the
   invariant can break.
6. **Give a verdict** against the bar, including what
   would falsify it and what we are *not* claiming.

### Standing rules

- **The requester's question is the title.** If the case study cannot be named
  by the question it answers, it has drifted.
- **A case study is not a finding.** It is an answer to something asked. It may
  *produce* a finding — an adoption, or a defect discovered on the way — and
  those go in the register (`docs/README.md`) with an id, as usual.
- **The verifier is the deliverable, and it must have failed in a test.** A
  checker nobody has seen fail is a checker nobody should trust.
- **We never open the PR.** Same as everything else:
  the bar.
- **Say what we did not check.** For #12899 we did not build a safe build and
  diff the binaries; the case says so.
- **We are usually not asking for the decision to change.** The useful output is
  what a decision costs and what keeps that cost stable. Arguing for a different
  choice is the requester's prerogative to invite, not our default.

## What a run learned about itself

A window of cvc5 history turns up facts about *our own* tooling that belong to
no pull request and so fit in no entry of the experience log. They go here,
newest first, one line each. An empty section is the honest state when a run
turned up nothing.

Salvaged from the retired `postmortem.md`, which asked a question no other file
here asks and which the reporting removal (`TODO.md`) dropped
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
- **A retraction went stale in our favour.** the promises (`docs/experience.md`)
  records that our baselines named `SETS_RELS_TCLOSURE_DOWN`, and that **no such
  id has ever existed in cvc5**. That was true when written. As of #12901 the id
  exists, because cvc5 renamed `TCLOSURE_UP` to it. The retraction stays — it is
  the record of an error we made — but it now needs the date qualifier it did
  not need before.
