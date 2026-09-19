# Findings

The reviewed ledger: what a finding is, what clears the bar to be carried to
cvc5, and the log of what has been filed and what has been retracted. Raw run
observations live in [`bug_db/`](../bug_db/README.md); what cvc5 has since done
about them is [`experience.md`](experience.md).

Four kinds, extending anoieu's three:

| | kind | what it asks of cvc5 |
| --- | --- | --- |
| **A** | a defect | an incomplete proof, named down to the input that produces it |
| **B** | an adoption | run a check of ours in your CI, with the configuration it needs |
| **C** | a change to the pipeline | to the proof infrastructure or to what safe mode promises |
| **D** | **an assertion** | a patch adding an invariant to cvc5, so the check lives in your tree and not ours |

**Kind A is what this repository is for.** An incomplete proof, named down to
the input that produces it, is the only finding that directly serves
[the goal](goals.md). The other three are instruments: B and D are ways of
making a fix stick, C is a way of changing what the pipeline promises. They are
cheap and worth doing, and none of them is the reason this exists.

A note on D, since it is the most easily overrated: an assertion converts a
silent hole into a loud failure and no more. It does not close a hole — it
closes a *check*. That is the shared position *success is the check being
deleted*, and D is how it happens here: where an invariant we check is one cvc5
could check about itself at startup, the deliverable is the patch and our check
goes with it. See
[`docs/tooling.md`](tooling.md#d3--where-an-invariant-should-live).

## The promises

These originated as the position shared with anoieu, in a
[`reporting-policy.md`](https://github.com/ajreynol/anoieu/blob/main/docs/reports/reporting-policy.md)
that anoieu deprecated on 2026-09-18 with its replacement still pending. They
were cited here by name and not restated, which left the statement of our own
policy in a deprecated file in another repository. They are restated below
because a policy you cannot read without leaving the tree is not one you can be
held to. Cite a position **by name**, never by number.

The tier says what backs it — **enforced**, something fails when it is broken;
**structural**, the arrangement makes the failure hard rather than impossible;
**intention**, nothing but our record. Several sit a tier above anoieu's because
the mechanism here is a test rather than a habit; where that is so, the test is
named, and a tier with no mechanism beside it is an intention wearing a better
word.

| | position | tier here | what backs it |
| --- | --- | --- | --- |
| **1** | **Silence is never evidence** | structural | where a check reports nothing, the most that may be said is that *those checks reported nothing*. Every code in [`checks.md`](checks.md#structured-observations) carries a limitation column, and every archived observation a `limitation` field |
| **4** | **Publish a candidate; carry a finding** | structural | candidates live in [`bug_db/`](../bug_db/README.md) under their own header; findings live in [the log](#the-log) below. Promoting one takes a deliberate act in a different file, not a slip |
| **5** | **Presence is not reachability** | structural | *"this rule has no checker"* and *"and an ordinary run emits it"* are different claims, and only the second is worth somebody's time. [`reachability.md`](reachability.md) is the measurement that separates them; the 182 latent holes are what it found |
| **6** | **A false positive is ours — and so is anything we asked cvc5 to run** | enforced, for the half that can be | a check that fired wrongly is narrowed until it stops, and the narrowing is recorded in [the retractions](#retractions) in cvc5's terms rather than kinder ones. Eight `baseline --check` ratchets under `tests/baselines/` fail the build on a change that invents one |
| **7** | **Every claim is re-checkable without us** | enforced | a number carries whatever regenerates it and the revision it was measured at. [`scripts/cvc5.lock`](../scripts/cvc5.lock) pins that revision, `tests/test_pin.py` enforces it, and CI fails if the pin names a commit reachable only on a fork — which is the retraction directly below that bought this rule |
| **8** | **Closing is a verdict, not an absence** | enforced, for the launcher | no row leaves without one recorded, and *"won't fix, because —"* is worth as much as a fix. Koine's writer is additive and cannot delete a row; `tests/test_experience.py` fails if [`prompts/close_bug_db`](../prompts/close_bug_db) stops carrying **Absence closes nothing** and **Confirm the closure in the current source** |
| **9** | **A reply is triage; an artifact settles it** | intention | what comes back from cvc5 is somebody's reading, made quickly and on our word. Here the settling artifact is a **cvc5 commit whose effect is re-read in current source** — not the commit message, and not the row going quiet. Failing to find one settles nothing |

Two more are stated in this file rather than in this table, because they are
load-bearing where they sit: *nothing crosses a repository boundary
automatically* is [the bar](#the-bar), and *success is the check being deleted*
is the note on kind D above.

Two things this repository adds, because the subject is a solver rather than a
signature:

- **Carrying a kind A means an input.** Not a code location and an argument — a
  `.smt2` file, an option set, and the quoted `--check-proofs-complete` failure.
  A claim that a path is reachable is worth nothing until something reaches it,
  and the static analysis's job is to tell us *where to look*, not to substitute
  for looking. What evidence each rank needs is set out in
  [`docs/tooling.md`](tooling.md#d5--safe-mode-first-and-the-reproducer-is-the-deliverable).
- **An assertion is not proposed until it has been run.** The promise is the
  shared one; the precondition is ours. It is applied to a cvc5 build configured
  `--assertions` and the regression suite passes with it in place. An assertion
  we have not run is a hypothesis, and hypotheses go in [`issues.md`](issues.md),
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
| **carry** | all five hold; a person can take it upstream today | [`next-report.md`](next-report.md), with the packet |
| **not yet** | one or more fail — **name which** | [`issues.md`](issues.md), rank and blocking rule on the row |
| **never** | it is ours, or it will never earn the attention | [`issues.md`](issues.md#settled) or the retraction log |

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
we have, and it is why [`TODO.md`](../TODO.md) declines a SARIF framework, a
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
that produced it, and logged in [the retractions](#retractions) below.

## The log

Ranks: **1** an incomplete proof in `--safe-mode=safe` (a contract violation,
needs an input); **2** a hole reachable in safe mode, no input yet; **3** a gap
in stable or unrestricted.

| # | what | kind | rank | state |
| --- | --- | --- | --- | --- |
| [tcb-001](findings/tcb-001.md) | six proof rule checkers compile against the theory solvers they check, to reach `static` helpers parked on solver classes | C | — | open, refactoring proposed |

Everything else this repository currently believes is in
[`TODO.md`](issues.md) as an
unconfirmed candidate, and stays there until it is reproduced.

## Retractions

Kept visible, because the log of what we got wrong is the more useful half.

| # | what we claimed | what was true |
| --- | --- | --- |
| `i-3` / `R2` | `checkProofsComplete` should stop being an **expert** option, so the safe-mode tester can name the guarantee it is testing | **the ask was for cvc5 to weaken the thing we were auditing, and it was rejected.** An option's category governs *both* assignments: promoting it also permits `--no-check-proofs-complete` and `(set-option :check-proofs-complete false)`, and `setDefaultsPre` honours an explicit user assignment through `checkProofsCompleteWasSetByUser`. So the promotion converts a guarantee that safe mode turns on into one a user can switch off — **the expert refusal is the mechanism keeping it non-negotiable, not an obstacle to stating it.** cvc5 built the promotion at `a960d7d7210e731cf48ad7baa6ad42fc7345b297`, reproduced the opt-out, and reverted it at `215eed21a6c8380075c46513e69181a295b6e3b2`. We reasoned from *the positive flag is refused* to *the option should be settable* without asking what else becomes settable, and one `--no-` run would have shown it. The chain's fifth link, `explicit-completeness`, is withdrawn from `CiModel.completeness_chain` and its `CI0002` entity retired; links three and four carry the exposure that is real. The surviving ask is the assertion form alone, and cvc5 notes it must allow for the deliberate lower-granularity exception |
| tcb-001 | six proof rule checkers include their theory solvers **to reach `static` helpers parked on solver classes** | **true of the strings edge, and asserted of five others without evidence.** cvc5 replied that the arithmetic checker uses nothing from `linear/constraint.h` and the datatypes checker nothing from `theory/rewriter.h`; both were dead includes, deleted in a line each, and the helper extraction the finding proposed for them was work nobody needed to do. The measurement could not have supported the claim: `cuts` weighed an include edge by how much closure it carried and never asked whether the file used what it included, so a dead include and a load-bearing one came out identical and the prose supplied a mechanism for both. `Closure.edge_use` now classifies every edge `used`, `unused` or `unknown` — `unknown` is never collapsed into `unused`, since calling a live include dead is the same error reflected — and `tests/test_tcb.py` pins the three edges cvc5 named. The closure figures were right throughout and are unchanged |
| every published number | measured against cvc5 `16c4001e53`, quoted as though anyone could check it | **that commit is not on `cvc5/cvc5`.** It is on the `ajreynol/CVC4` fork, so no reader could fetch it, and the promise that *every claim is re-checkable without us* was void for the whole document set. The baselines happened to be valid — all eight ratchets are clean at upstream `40a4bb7e4` — so nothing measured was wrong, but nothing was checkable either. Now pinned in [`scripts/cvc5.lock`](../scripts/cvc5.lock), enforced by `tests/test_pin.py`, and fetched in CI by a job that fails if the pin is fork-only |
| `infer`/`inferid` baselines | our baselines named `SETS_RELS_TCLOSURE_DOWN` as an `InferenceId` cvc5 emits | **no such id has ever existed in cvc5.** `git log --all -S` finds it in no commit; the enum at `40a4bb7e4` carries `SETS_RELS_TCLOSURE_FWD` and `_UP`. The baselines had been written rather than generated by running the tools, so two of the eight ratchets failed against the very commit they were recorded at. Both are regenerated and all eight are clean; found while writing [`why.md`](why.md#the-mechanism-and-the-first-thing-it-caught) |
| `dokimasia.infer baseline --check` | an id leaving the unhandled set was reported as *now reconstructed* | it leaves for two unrelated reasons — the theory now proves it, or it is no longer emitted. The tool could not distinguish them, so a rename in cvc5 would have been reported as an improvement in cvc5's proof coverage. The delta now marks the second case `?` and says *no longer emitted, NOT reconstructed* |
| tcb-001 (draft) | the checker's TCB is **74% of `src/`** | an artifact of a mode that followed each header to its `.cpp`; the closure saturates at cvc5's whole link unit, and an unrelated seed (`printer/printer.cpp`) gave the identical figure. The compile-time surface is **8.0%**. The mode is no longer the default and warns; `tests/test_tcb.py` guards the result |
