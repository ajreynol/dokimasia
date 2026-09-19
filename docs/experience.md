# Experience: our claims, and what came of them

Three things, in the order a claim moves through them: what a finding **is** and
the bar it clears to be carried to cvc5; the **log** of what was filed and what
was retracted; and **what cvc5 did** about the observations we recorded.

Raw run observations are data and live in [`bug_db/`](../bug_db/README.md). The
argument, the checks and the register of what we are asking cvc5 for are in
[the documentation index](README.md).

## What a finding is

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
[the goal](README.md#the-stance). The other three are instruments: B and D are ways of
making a fix stick, C is a way of changing what the pipeline promises. They are
cheap and worth doing, and none of them is the reason this exists.

A note on D, since it is the most easily overrated: an assertion converts a
silent hole into a loud failure and no more. It does not close a hole — it
closes a *check*. That is the shared position *success is the check being
deleted*, and D is how it happens here: where an invariant we check is one cvc5
could check about itself at startup, the deliverable is the patch and our check
goes with it. See
[`docs/maintenance.md`](maintenance.md#d3--where-an-invariant-should-live).

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
| **1** | **Silence is never evidence** | structural | where a check reports nothing, the most that may be said is that *those checks reported nothing*. Every code in [`checks.md`](README.md#structured-observations) carries a limitation column, and every archived observation a `limitation` field |
| **4** | **Publish a candidate; carry a finding** | structural | candidates live in [`bug_db/`](../bug_db/README.md) under their own header; findings live in [the log](#the-log) below. Promoting one takes a deliberate act in a different file, not a slip |
| **5** | **Presence is not reachability** | structural | *"this rule has no checker"* and *"and an ordinary run emits it"* are different claims, and only the second is worth somebody's time. [`reachability.md`](maintenance.md#what-the-corpus-reaches) is the measurement that separates them; the 182 latent holes are what it found |
| **6** | **A false positive is ours — and so is anything we asked cvc5 to run** | enforced, for the half that can be | a check that fired wrongly is narrowed until it stops, and the narrowing is recorded in [the retractions](#retractions) in cvc5's terms rather than kinder ones. Eight `baseline --check` ratchets under `tests/baselines/` fail the build on a change that invents one |
| **7** | **Every claim is re-checkable without us** | enforced | a number carries whatever regenerates it and the revision it was measured at. [`scripts/cvc5.lock`](../scripts/cvc5.lock) pins that revision, `tests/test_pin.py` enforces it, and CI fails if the pin names a commit reachable only on a fork — which is the retraction directly below that bought this rule |
| **8** | **Closing is a verdict, not an absence** | enforced, for the launcher | no row leaves without one recorded, and *"won't fix, because —"* is worth as much as a fix. Koine's writer is additive and cannot delete a row; `tests/test_experience.py` fails if [`prompts/close_bug_db`](../prompts/close_bug_db) stops carrying **Absence closes nothing** and **Confirm the closure in the current source** |
| **9** | **A reply is triage; an artifact settles it** | intention | what comes back from cvc5 is somebody's reading, made quickly and on our word. Here the settling artifact is a **cvc5 commit whose effect is re-read in current source** — not the commit message, and not the row going quiet. Failing to find one settles nothing |

Two more are stated in this file rather than in this table, because they are
load-bearing where they sit: *nothing crosses a repository boundary
automatically* is [the bar](#the-bar), and *success is the check being deleted*
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
  [`docs/maintenance.md`](maintenance.md#d5--safe-mode-first-and-the-reproducer-is-the-deliverable).
- **An assertion is not proposed until it has been run.** The promise is the
  shared one; the precondition is ours. It is applied to a cvc5 build configured
  `--assertions` and the regression suite passes with it in place. An assertion
  we have not run is a hypothesis, and hypotheses go in [`issues.md`](README.md#the-register),
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
| **carry** | all five hold; a person can take it upstream today | [`next-report.md`](experience.md#what-to-report-next), with the packet |
| **not yet** | one or more fail — **name which** | [`issues.md`](README.md#the-register), rank and blocking rule on the row |
| **never** | it is ours, or it will never earn the attention | [`issues.md`](README.md#settled) or the retraction log |

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

## What to report next



Applying [the bar](experience.md#the-bar). Two rows clear it; everything else
names the rule that blocks it.

### The verdicts

| verdict | row | |
| --- | --- | --- |
| **carry** | `i-3` / `R2` | completeness in safe mode is obtained by configuration and nothing asserts it *(the category half of this ask was rejected — see below)* |
| **carry** | `i-2` | `stringLazyPreproc` — safe mode refuses to let you set it *because it lacks proof support*, and leaves it on |
| not yet — **run-it** | `i-1`, `i-22`, `i-6` | a static argument with no input. `i-1` has had one attempt fail |
| not yet — **run-it** | the 182 [latent holes](maintenance.md#what-the-corpus-reaches) | declared, and nothing has reached them |
| not yet — **worth-the-attention** | the dead-declaration cleanups | bundled, and only after something substantive lands |
| never | `i-4` | a termination argument for the reconstruction search settles it, and nothing else does |

### The recommendation

**Report the completeness flag first: in safe mode the guarantee is obtained only
as a side effect, and nothing asserts it.** ([`i-3`](README.md#the-register),
[`R2`](README.md#open--asks))

> **Amended 2026-09-19.** This read *"`--check-proofs-complete` cannot be set in
> either mode whose contract it enforces"*, which is true and was the wrong
> emphasis: cvc5 has since established that it *should not* be settable there,
> because the same change would permit switching completeness off. The
> unsettability is the guarantee working, not the defect. The defect is below
> it — the implication is unasserted.

One command is the whole report:

```
$ cvc5 --safe-mode=safe --produce-proofs --check-proofs --check-proofs-complete f.smt2
(error "Fatal error in option parsing: expert option check-proofs-complete
        cannot be set in safe mode.")
```

`checkProofsComplete` is `category = "expert"` in `proof_options.toml`. Safe and
stable mode reject expert options. So the flag can only be passed in the
unrestricted job — the one mode that makes no completeness promise. In safe
mode the guarantee is obtainable **only** as a side effect: `setDefaultsPre`
turns the option on when `--check-proofs` is set and no `--proof-granularity`
was requested. Adding a granularity flag to the proof tester would switch
completeness testing off, and no test would fail.

**Why this one.**

| criterion | |
| --- | --- |
| **it is about the guarantee itself** | not a hole, but the mechanism that detects holes. Everything else this repository reports depends on it working |
| **it takes one command to verify** | no build, no corpus, no argument about reachability. A maintainer can refute or confirm it in thirty seconds — and did, refuting one of the two remedies below |
| **it is not a matter of taste** | the option's own help text says *"enabled by default in safe builds"*, and safe builds are exactly where it cannot be named |
| **the fix is small and has a natural home** | an assertion in `setDefaultsPre` — a [kind D](experience.md#what-a-finding-is), so the invariant lands in cvc5's tree and our `CI0002` check retires |
| **we found it by running, not reading** | the static analysis got this ask *wrong* (see below), which is itself worth telling them |

**The proposed fix.** This listed two forms; **the second was rejected by cvc5
on 2026-09-19 and is withdrawn.**

1. **Assert the implication where it is created.** In `setDefaultsPre`, after a
   safe build enables `checkProofsComplete`, assert it is set — **at the default
   and DSL-rewrite granularities only.** cvc5 supplied that condition: an
   unconditional assertion would fire on the deliberate lower-granularity
   exception. Still the smallest change and still a [kind D](experience.md#what-a-finding-is).
2. ~~**Exempt `checkProofsComplete` from the expert refusal**, so the safe-mode
   regression tester can name what it is testing.~~ **Withdrawn — this asked
   cvc5 to weaken the guarantee we are auditing.** An option's category governs
   both assignments, so making it settable in safe mode equally permits
   `--no-check-proofs-complete` and `(set-option :check-proofs-complete false)`,
   and `setDefaultsPre` honours an explicit user assignment through
   `checkProofsCompleteWasSetByUser`. cvc5 built the promotion at `a960d7d7210e731cf48ad7baa6ad42fc7345b297`,
   reproduced the opt-out, and reverted it at `215eed21a6c8380075c46513e69181a295b6e3b2`. **The expert refusal
   is the mechanism that makes completeness non-negotiable in safe mode**, and we
   read it as an obstacle to naming the guarantee. Recorded in
   [the retractions](experience.md#retractions).

**What sank half of it, and what that leaves.** The report's own criterion was
that a maintainer could refute it in thirty seconds, and one did: the refutation
is `cvc5 --check-proofs --no-check-proofs-complete f.smt2` printing `false`. The
remaining claim is untouched and is the one to carry — **completeness in safe
mode is obtained by configuration, and adding a `--proof-granularity` flag to the
proof tester would switch it off with no test failing.** That wants an assertion,
not a category change.

### The second carry: `i-2`

Two commands, and they contradict each other:

```
$ cvc5 --safe-mode=safe --strings-lazy-pp f.smt2
(error "Fatal error in option parsing: cannot set option strings-lazy-pp in
        safe mode, as this option does not support proofs")
```

...while `strings_options.toml` gives it `default = "true"` and `setDefaultsPre`
never turns it off. **Safe mode refuses to let you set the option on the grounds
that it does not support proofs, and then runs with it on.**

`--no-strings-lazy-pp` is refused too, so the guard also blocks the one
assignment that would make the configuration safer — a user who has read the
annotation and wants to comply cannot.

Either reading is a defect and the fix is a maintainer's one-line call: disable
it in safe mode, or drop the stale annotation. It is cheap to receive, which is
why it goes with `i-3` rather than behind it.

### Runner-up, and why it is second

**[`i-23`](README.md#the-register) — the `safeMode == UNRESTRICTED` guard in
`EoPrinter::isHandled` is inert.** Ten rules are accepted only in unrestricted
builds; none of the ten can be *produced* in safe or stable mode. Verified by
running: transcendental kinds are refused outright, and `set.filter` needs a
function-typed argument and so the higher-order logic both modes reject.

It is second because the fix is not obvious and the payoff is smaller. Deleting
the cases would be **wrong** — they would fall through to `default: return
false` and flip unrestricted mode from handled to unhandled. The right change is
to move them to the always-handled list or to document why the condition cannot
matter, and which of those is right is a question for whoever wrote it. It is a
good *question*, not a good patch.

### Explicitly not recommended yet

- **`i-1` (`LAMBDA_ELIM`).** Our strongest safe-mode candidate, and the one
  nearest to a `set.filter`-shaped mistake. The sweeping claim beside it — *no
  `uf` kind is blocked in safe mode* — turned out to be [half
  wrong](README.md#settled). One reproducer attempt has already failed. **Do not
  carry this without an input.**
- **Anything resting on the 79 fall-through inferences.** Real by construction,
  but [the corpus reaches none of them in safe mode](maintenance.md#what-the-corpus-reaches), so
  severity is unestablished and a maintainer would rightly ask for one input.
- **The dead-declaration cleanups** (4 dead `TrustId`s, 14 dead `InferenceId`s,
  3 dead `PREPROCESS_*` ids, the `PREPROCESS_BV_GUASS` misspelling). These are
  the *most* landable as a patch and the least valuable: near-zero risk,
  near-zero benefit, and they spend the credit that should go to the first
  report above. Worth bundling into one PR **after** something substantive has
  been accepted, never before.

### The general rule this session suggests

**Prefer the claim a maintainer can refute in one command.** Of the four things
this repository got wrong recently, three were static arguments that read
correctly and were false; every one was caught by running something. A report
whose evidence is a command carries its own refutation, which is the property
that makes it cheap to receive.

## The log

Ranks: **1** an incomplete proof in `--safe-mode=safe` (a contract violation,
needs an input); **2** a hole reachable in safe mode, no input yet; **3** a gap
in stable or unrestricted.

| # | what | kind | rank | state |
| --- | --- | --- | --- | --- |
| [tcb-001](experience.md#tcb-001--proof-rule-checkers-compile-against-the-theory-solvers-they-check) | six proof rule checkers compile against the theory solvers they check, to reach `static` helpers parked on solver classes | C | — | open, refactoring proposed |

Everything else this repository currently believes is in
[`TODO.md`](README.md#the-register) as an
unconfirmed candidate, and stays there until it is reproduced.

### `tcb-001` — proof rule checkers compile against the theory solvers they check

**Status:** open · **Kind:** C (a change to the pipeline) · **Reported against:**
cvc5 `40a4bb7e4` · **Severity:** not a bug — an architectural coupling with a
cheap, local fix

### Summary

cvc5's internal proof checker is the natural candidate for a trusted kernel: it
is the component that decides whether a cvc5 proof is valid. Its value depends
on how little of cvc5 it needs to be correct.

The base class is already disciplined — `ProofRuleChecker(NodeManager* nm)` —
and **12 of the 13 registered rule checkers take nothing but a `NodeManager*`**.

But six of them `#include` the headers of the *theory solvers they are checking*.
For the strings checker this is to call `static` helper functions that live on
the solver class: pure functions of `NodeManager*` and `Node` that do not need
the solver, reached by including the whole class. Including the solver drags its
entire header closure into the checker's.

> **Corrected 2026-09-19, and the correction is ours.** This section originally
> gave that mechanism for all six edges. cvc5 replied that the arithmetic
> checker uses nothing from `linear/constraint.h` and the datatypes checker
> nothing from `theory/rewriter.h`: those includes were simply dead, and were
> removed in one line each with no helper extraction. **The measurement never
> established the mechanism** — `cuts` weighed include edges by closure size and
> could not see whether a file used what it included, so a dead include and a
> load-bearing one appeared in the same list and the prose supplied a reason for
> both. The tool now classifies every edge `used`, `unused` or `unknown`
> (`dokimasia.tcb cuts`, and `Closure.dead_includes`), and
> `tests/test_tcb.py` pins these three edges by name. The closure figures below
> are unchanged: they were never what was wrong.

The result: the checker's compile-time dependency surface is **179 files,
41,446 lines — 8.0% of `src/`** — and it contains `theory/strings/core_solver.h`,
`theory/arith/linear/constraint.h`, `theory/theory.h` and `theory/rewriter.h`.

The fix is mechanical, local, and does not change behaviour: move the pure static
helpers out of the solver classes into dependency-light headers that both the
solver and the checker include.

### How to reproduce

No build required; the tool reads a source tree.

```bash
git clone https://github.com/ajreynol/dokimasia && cd dokimasia
python3 -m dokimasia.tcb measure <cvc5>            # the headline figures
python3 -m dokimasia.tcb cuts    <cvc5>            # what each edge costs
python3 -m dokimasia.tcb why     <cvc5> theory/strings/core_solver.h
```

Seeds are `ProofChecker`, `ProofRuleChecker` and all 13 registered theory rule
checkers (`SEED_SETS["proof-checker"]`).

### The measurement

```
closure         179 files      41,446 lines
all of src/    1663 files     521,070 lines
                               = 8.0% of cvc5 by line count
```

Ten theory subsystems are inside it. The heaviest individual checkers:

| checker | closure |
| --- | --- |
| `theory/strings/proof_checker.cpp` | 105 files, 26,985 lines |
| `theory/builtin/proof_checker.cpp` | 72 files, 17,150 lines |
| `theory/arith/nl/transcendental/proof_checker.cpp` | 55 files, 13,811 lines |
| `theory/arith/proof_checker.cpp` | 52 files, 13,153 lines |

### The finding

Every load-bearing edge is a checker including a solver. `cuts` reports what each
is uniquely worth — the lines that leave the closure if that one `#include` goes:

**Every load-bearing edge is a checker including a solver — and not every edge is
load-bearing.** The `use` column is what the original table lacked: `used` means
the file references something the header declares, so the line cannot go until
the declaration moves; `unused` means it references nothing, so deleting the line
is the whole fix.

| from | include | uniquely worth | use | that header's own closure |
| --- | --- | --- | --- | --- |
| `theory/strings/proof_checker.cpp` | `theory/strings/core_solver.h` | **3,193 lines** | used | 86 files, 21,904 lines |
| `theory/arith/proof_checker.cpp` | `theory/arith/linear/constraint.h` | **2,556 lines** | **unused** | 29 files, 9,374 lines |
| `theory/datatypes/proof_checker.cpp` | `theory/datatypes/theory_datatypes_utils.h` | 1,027 lines | used | |
| `theory/arith/nl/transcendental/proof_checker.cpp` | `theory/arith/nl/transcendental/sine_solver.h` | 809 lines | used | |
| `theory/datatypes/proof_checker.cpp` | `expr/dtype_cons.h` | 479 lines | **unused** | |
| `theory/builtin/proof_checker.cpp` | `rewriter/rewrite_db.h` | 332 lines | used | |
| `theory/builtin/proof_checker.cpp` | `theory/quantifiers/extended_rewrite.h` | 270 lines | **unused** | 11 files, 3,568 lines |
| `theory/builtin/proof_checker.cpp` | `smt/term_formula_removal.h` | 237 lines | used | |
| `theory/arrays/proof_checker.cpp` | `theory/rewriter.h` | — | **unused** | 12 files, 3,840 lines |

**19 seed includes in all reference nothing their header declares**, 3 of which
shrink the closure; the other 16 are reachable by another path and are dead
anyway. `python3 -m dokimasia.tcb cuts <cvc5>` lists them.

### Root cause

The helpers the checkers want are `static` methods on solver classes. From
`theory/strings/core_solver.h`:

```cpp
static Node getConclusion(NodeManager* nm, ...);              // :267
static Node getDecomposeConclusion(NodeManager* nm, ...);     // :309
static Node getExtensionalityConclusion(NodeManager* nm, ...);// :325
```

and `theory/strings/proof_checker.cpp` calls exactly these three, at lines 239,
266 and 502. They take a `NodeManager*` and `Node`s, touch no solver state, and
are *already* written as pure functions. They are simply parked on the wrong
class, and C++ makes you include the whole class to reach them.

This is a good sign, not a bad one: the coupling is lexical, not semantic. The
checker and the solver genuinely share a conclusion-computing function — which
is correct and desirable, since the checker should compute the same conclusion
the solver claimed — but sharing it should not mean depending on the solver.

### Proposed refactoring

**Extract the shared pure helpers into dependency-light headers.**

Taking strings as the worked example:

1. Add `theory/strings/core_conclusions.h` — or extend the existing
   `theory/strings/theory_strings_utils.h`, which is light (10 files, 3,454
   lines) and already the home for this sort of thing.
2. Move `getConclusion`, `getDecomposeConclusion` and
   `getExtensionalityConclusion` there as free functions in
   `cvc5::internal::theory::strings`. They are already `static` and already take
   a `NodeManager*`, so the move is a cut-and-paste plus a namespace.
3. `CoreSolver` includes the new header and calls the free functions (or keeps
   thin forwarding wrappers, if call sites elsewhere are numerous).
4. `theory/strings/proof_checker.cpp` includes the new header **instead of**
   `core_solver.h`.

Result: −3,193 lines from the checker's closure, and — the part that matters
more than the number — `StringProofRuleChecker` stops compiling against
`CoreSolver` entirely.

The same shape applies to `transcendental` ↔ `sine_solver.h`, which is `used`.
**It does not apply to `arith/proof_checker.cpp` ↔ `linear/constraint.h`**, where
the include is dead and `git rm` of one line is the entire change — as cvc5
established, and as the tool now reports without being told.

### On `Env` — we checked, and it is not the problem

An earlier hypothesis was that `Env` was the culprit, since
`BuiltinProofRuleChecker` is the one checker that takes one:

```cpp
BuiltinProofRuleChecker(NodeManager* nm, Rewriter* r, Env& env);
```

**Measured, `smt/env.h` closes over 23 files and 7,012 lines** — a third of the
weight of `core_solver.h` alone. `Env` is widely included precisely because it is
thin. So a stripped-down `Env` is *not* where the lines are, and we would not
propose one on size grounds.

There is still an argument for a narrow `ProofCheckerContext` (a `NodeManager*`,
the handful of options the checkers read, and a `Rewriter*` where genuinely
required), but it is an *architectural* argument — it makes "a checker cannot
reach the solver" true by construction rather than by convention — not a
line-count one. We would rather see the solver-header extraction done first; it
is cheaper and it is where the weight actually is.

### Why this is worth doing

`--check-proofs` is most valuable when the checker is small and independent of
the code that produced the proof. Two of these couplings are directly
self-referential: `theory/arrays/proof_checker.cpp` includes `theory/rewriter.h`,
and `BuiltinProofRuleChecker` is *handed* a `Rewriter*` — so `MACRO_REWRITE` is
checked by replaying the rewrite with the same rewriter that produced it. cvc5
already knows this and says so, by registering that rule through
`registerTrustedChecker` at pedantic level 4. The dependency measurement and the
pedantic ladder are two descriptions of one fact.

Shrinking the checker's dependency surface is also the most concrete step
available toward being able to say *which part of cvc5 is its proof kernel* —
an argument that gets shorter every time a coupling like this is removed.

### Keeping it fixed

```bash
python3 -m dokimasia.tcb baseline <cvc5> --write   # record
python3 -m dokimasia.tcb baseline <cvc5> --check   # fail if it grew
```

Runs in seconds, needs no build, and fits cvc5's existing nightly. The ratchet
turns one way; if growth is intended, the baseline moves in the same commit with
a reason.

### What we got wrong first

Recorded because our own errors belong in the same place as our findings.

The first version of this measurement reported that the checker depended on
**74% of `src/`**. That was an artifact. The tool had a mode that followed each
reached header to its `.cpp`, as a proxy for "what could execute". Once any
`.cpp` enters the closure it includes further headers, whose `.cpp` files follow,
and the closure saturates at cvc5's whole link unit: seeding from
`printer/printer.cpp` — unrelated to proof checking — produced the identical
383,760-line figure.

A measure that returns the same answer for every seed measures nothing. The mode
is no longer the default and now prints a warning. The 8.0% figure above is the
compile-time surface, which discriminates.

The real lesson: "what could execute during checking" is a **call-graph**
question, not an `#include` question, and answering it properly needs a build.

**Known under-approximation:** generated headers are invisible to the tool.
`options/options.h` is produced from the `.toml` files at build time and is not
in the source tree, so edges through it are not followed.

## Retractions

Kept visible, because the log of what we got wrong is the more useful half.

| # | what we claimed | what was true |
| --- | --- | --- |
| `i-3` / `R2` | `checkProofsComplete` should stop being an **expert** option, so the safe-mode tester can name the guarantee it is testing | **the ask was for cvc5 to weaken the thing we were auditing, and it was rejected.** An option's category governs *both* assignments: promoting it also permits `--no-check-proofs-complete` and `(set-option :check-proofs-complete false)`, and `setDefaultsPre` honours an explicit user assignment through `checkProofsCompleteWasSetByUser`. So the promotion converts a guarantee that safe mode turns on into one a user can switch off — **the expert refusal is the mechanism keeping it non-negotiable, not an obstacle to stating it.** cvc5 built the promotion at `a960d7d7210e731cf48ad7baa6ad42fc7345b297`, reproduced the opt-out, and reverted it at `215eed21a6c8380075c46513e69181a295b6e3b2`. We reasoned from *the positive flag is refused* to *the option should be settable* without asking what else becomes settable, and one `--no-` run would have shown it. The chain's fifth link, `explicit-completeness`, is withdrawn from `CiModel.completeness_chain` and its `CI0002` entity retired; links three and four carry the exposure that is real. The surviving ask is the assertion form alone, and cvc5 notes it must allow for the deliberate lower-granularity exception |
| tcb-001 | six proof rule checkers include their theory solvers **to reach `static` helpers parked on solver classes** | **true of the strings edge, and asserted of five others without evidence.** cvc5 replied that the arithmetic checker uses nothing from `linear/constraint.h` and the datatypes checker nothing from `theory/rewriter.h`; both were dead includes, deleted in a line each, and the helper extraction the finding proposed for them was work nobody needed to do. The measurement could not have supported the claim: `cuts` weighed an include edge by how much closure it carried and never asked whether the file used what it included, so a dead include and a load-bearing one came out identical and the prose supplied a mechanism for both. `Closure.edge_use` now classifies every edge `used`, `unused` or `unknown` — `unknown` is never collapsed into `unused`, since calling a live include dead is the same error reflected — and `tests/test_tcb.py` pins the three edges cvc5 named. The closure figures were right throughout and are unchanged |
| every published number | measured against cvc5 `16c4001e53`, quoted as though anyone could check it | **that commit is not on `cvc5/cvc5`.** It is on the `ajreynol/CVC4` fork, so no reader could fetch it, and the promise that *every claim is re-checkable without us* was void for the whole document set. The baselines happened to be valid — all eight ratchets are clean at upstream `40a4bb7e4` — so nothing measured was wrong, but nothing was checkable either. Now pinned in [`scripts/cvc5.lock`](../scripts/cvc5.lock), enforced by `tests/test_pin.py`, and fetched in CI by a job that fails if the pin is fork-only |
| `infer`/`inferid` baselines | our baselines named `SETS_RELS_TCLOSURE_DOWN` as an `InferenceId` cvc5 emits | **no such id has ever existed in cvc5.** `git log --all -S` finds it in no commit; the enum at `40a4bb7e4` carries `SETS_RELS_TCLOSURE_FWD` and `_UP`. The baselines had been written rather than generated by running the tools, so two of the eight ratchets failed against the very commit they were recorded at. Both are regenerated and all eight are clean; found while writing [`why.md`](README.md#why-cvc5-should-care) |
| `dokimasia.infer baseline --check` | an id leaving the unhandled set was reported as *now reconstructed* | it leaves for two unrelated reasons — the theory now proves it, or it is no longer emitted. The tool could not distinguish them, so a rename in cvc5 would have been reported as an improvement in cvc5's proof coverage. The delta now marks the second case `?` and says *no longer emitted, NOT reconstructed* |
| tcb-001 (draft) | the checker's TCB is **74% of `src/`** | an artifact of a mode that followed each header to its `.cpp`; the closure saturates at cvc5's whole link unit, and an unrelated seed (`printer/printer.cpp`) gave the identical figure. The compile-time surface is **8.0%**. The mode is no longer the default and warns; `tests/test_tcb.py` guards the result |

## Case studies

A cvc5 design question, answered with a verifier rather than an opinion. The
shape: read the decision, find the invariant that makes it cheap, build a check
that fires when the invariant breaks, and report the check rather than the
opinion. Two so far.

### cvc5 #12899 — is forbidding safe mode with debug symbols actually a restriction?

**The design decision.** cvc5's configure script does not allow a safe build to
be combined with debug symbols. This is **deliberate and for clarity**: the
build already carries a large configuration space, and every combination
permitted is one more thing to explain, test and keep working. Forbidding a
combination nobody has needed is a reasonable simplification, and
[#12899](https://github.com/cvc5/cvc5/pull/12899) flattening the build system is
the natural moment to ask whether it is still the right one.

**The research question is not why it is forbidden.** It is: **does forbidding
it actually deny anyone anything?**

**Our answer:** almost nothing, and we can say exactly what the *almost* is. A
safe build differs from an ordinary build in one semantic respect — the default
value of a runtime option — so an unrestricted debug build run with
`--safe-mode=safe` reproduces a safe build's *behaviour* exactly. What it does
not reproduce is the diagnostic text, and that text is read by the regression
testers.

**So the simplification is currently free, and the reason it is free is an
invariant that nothing in cvc5 maintains.** That is what this case is really
about, and what
[`dokimasia.buildmode`](../dokimasia/buildmode/) exists to protect.

*Measured against cvc5 `40a4bb7e4`.*

### What a safe build actually is

`ENABLE_SAFE_MODE` does three things in `CMakeLists.txt`: defines
`-DCVC5_SAFE_MODE`, turns off `USE_POLY` / `USE_COCOA` / `USE_NORMALIZ`, and
changes the printed build profile. The macro is referenced in **eight places in
all of `src/`**, and every one falls into one of three categories:

| where | what it does | category |
| --- | --- | --- |
| `options/options_template.cpp` | `d_base->safeMode = options::SafeMode::SAFE` in the `Options` constructor | **an option default** |
| `base/configuration_private.h` | `#define IS_SAFE_BUILD true` | build self-report |
| `smt/logic_exception.h` | prepends `"Logic restricted in safe mode. "` | message text |
| `theory/theory_rewriter.cpp` | omits `" Try --ff."`-style hints | message text |
| `smt/illegal_checker.cpp` | omits `" Try --arrays-exp."`-style hints | message text |

Two further facts complete the picture:

- **No source file is excluded.** `src/CMakeLists.txt` never mentions
  `ENABLE_SAFE_MODE`; a safe build compiles the same translation units.
- **Nothing branches on the build.** `Configuration::isSafeBuild()` has exactly
  one caller — `options_handler.cpp`, printing `--show-config`. It is reported,
  never acted on.

The safe build's only semantic act is to change the *starting value* of a
runtime option, which is exactly what `--safe-mode=safe` does.

### What the restriction costs

Three things a safe build gives you, and whether a debug build with
`--safe-mode=safe` gives them too:

| | reproduced by `--safe-mode=safe`? |
| --- | --- |
| the solver's behaviour — what is accepted, rewritten, proved | **yes, exactly.** It is the same option, set the same way |
| the three optional libraries being absent from the binary | **no** — they are linked and simply not reached |
| the diagnostic text, including the `"in safe mode"` prefix | **no** — that is decided at compile time |

Only the third is a cost to a developer, and it is a real one:

**The exception text is load-bearing for CI.** `SafeLogicException` prepends
`"Logic restricted in safe mode. "` at compile time, and
`smt/logic_exception.h` says why that matters:

> *The regression testers will consider any exception having text "in safe mode"
> or "in stable mode" as an admissible failure, and skip the benchmark.*

Verified on an unrestricted binary at `--safe-mode=safe`:

```
$ cvc5 --safe-mode=safe cos.smt2
(error "Cannot handle assertion with term of kind cos in this configuration.")
```

No `"in safe mode"` prefix — a safe build emits one. The same run also *keeps* a
hint a safe build drops:

```
$ cvc5 --safe-mode=safe ff.smt2
(error "Cannot handle assertion with term of kind CONST_FINITE_FIELD in this
        configuration. Try --ff.")
```

**Consequence:** a benchmark that a safe build *skips*, an unrestricted build at
`--safe-mode=safe` *fails*. So the restriction bites in exactly one situation —
**debugging a safe-mode regression skip** — where you would want a debug binary
that produces safe-build diagnostics, and cannot have one. Whether anybody has
wanted that is a question for cvc5, not for us. Our contribution is that the
list is this short, and that we can keep it this short.

### The invariant, and why it is the real subject

> **A safe build differs from an unrestricted build only in (a) the default
> value of the `safeMode` option, (b) the text of diagnostics, and (c) what the
> build reports about itself. No solver behaviour is gated on the build macro.**

**This invariant is what makes the configure restriction cheap.** While it
holds, refusing safe + debug denies a developer only the diagnostic text, and
the simplification pays for itself. If it ever stops holding — if some behaviour
becomes reachable in a safe build and not under `--safe-mode=safe` — then the
same configure line stops being a simplification and becomes a genuine
restriction, because no runtime flag substitutes for the build any more.

Nothing in cvc5 currently maintains it. It holds today by accident, and the
natural way to add a safe-mode restriction is `#ifdef CVC5_SAFE_MODE` around the
restriction, which would break it on the first use. **The invariant is worth
maintaining deliberately, and it is cheap to maintain**: it is a property of
eight lines that a check can read in a tenth of a second.

Keeping it also has a benefit beyond this question: while it holds, "safe mode"
is unambiguous. Every claim anyone makes about safe mode — ours included — is
true of both the build and the flag, and nobody has to say which.

### The check

```bash
python3 -m dokimasia.buildmode check <cvc5>    # BUILD0001
python3 -m dokimasia.buildmode sites <cvc5>    # every conditional, classified
```

It enumerates every `CVC5_SAFE_MODE` / `CVC5_STABLE_MODE` conditional and
classifies each as an option default, a diagnostic, or a build self-report. The
classifier is **closed**: anything it does not positively recognise is reported,
so a new conditional has to argue for itself rather than slip through. It also
fails if a source file becomes excluded from a safe build, or if anything starts
branching on `isSafeBuild()`.

One block — the hint selection in `illegal_checker.cpp` — is message-only but
computes *which* hint to print, which the classifier is too strict to see. It is
allowlisted with a hash of its contents, so editing it re-triggers review rather
than silently staying approved.

`tests/test_buildmode.py` checks that the verifier fires on each way the
invariant can break, because a checker nobody has seen fail is a checker nobody
should trust.

### What we would ask of cvc5

**Not a change to the configure script.** The restriction is a reasonable
simplification and we are not arguing against it; whether the one lost
capability — a debug binary with safe-build diagnostics — is worth a
combination in the build matrix is cvc5's call, and depends on whether anyone
has ever wanted it.

**What we would ask for is the invariant, maintained.** Run `BUILD0001` as a
[kind B](#what-a-finding-is) adoption: seconds, no build, no dependencies. Its value
is not the eight sites it finds today — it is that the ninth gets noticed, and
that the configure simplification keeps being free.

Better still if cvc5 owns it rather than us. The same property could be a
build-time test or an assertion in their tree, at which point our check retires.
That is the [kind D](#what-a-finding-is) outcome and we prefer it.

### Verdict

| | |
| --- | --- |
| **carry** | the answer to the question #12899 raised, with the check as evidence |
| rules it clears | `theirs-not-ours`, `run-it` (the diagnostic divergence is demonstrated, not argued), `cheap-to-refute`, `falsifiable`, `worth-the-attention` |
| falsified by | a `CVC5_SAFE_MODE` conditional that gates behaviour — which is what the check looks for; or a developer naming a use for safe + debug that the flag does not cover, which would make the restriction a real cost after all |

**What we are not claiming.** We have not built a safe build and compared
binaries. The equivalence argument is static and exhaustive over the eight
sites; the divergence we demonstrate empirically is the diagnostic text. A
direct A/B of a safe build against `--safe-mode=safe` over the regression suite
would settle it completely, and needs a build we do not have.

### cvc5 #12905 — a real bug report that is not a proof bug

**The request.** cvc5 [#12905](https://github.com/cvc5/cvc5/issues/12905) — a
fatal failure at `theory_engine.cpp:2030` on a strings-and-quantifiers
benchmark:

```
(declare-const x Int)
(assert (exists ((s String) (t Int))
  (and (= 1 (str.len (str.++ (str.substr s 0 1) (str.at s t))))
       (not (str.suffixof (ite (str.in_re "/" (str.to_re s))
                               (str.substr s 0 x)
                               (str.replace "/" s "")) s)))))
(check-sat)
```

> *wasn't sent to you, so why are you explaining it trivially, for fact
> `(not (= (+ (str.len @quantifiers_skolemize_2) (* (- 1) (str.len @purify_4))) 0))`*

**This is not a proof bug.** It is a theory-explanation defect: a fact reached
the explanation machinery that the engine did not think it had sent. Nothing in
it concerns whether a step can produce a proof, which is the whole of what this
repository is for.

**Two questions follow, and they have different answers.**

### 1. What does this repository do with it?

**Nothing, and it says so.** dokimasia holds one role — *what no proof step
covers* — and an assertion failure in theory combination is not it. Taking it
would be the most ordinary failure mode available to a tool with a working
analysis and spare attention: scope creep dressed as helpfulness.

The register stays clean: #12905 gets no `i-` id, because
[`issues.md`](README.md#the-register) is *things we are asking cvc5 to act on*, and we are
asking nothing. cvc5 already has the report; a second opinion from us is not a
contribution.

**The one thing worth checking is whether the classification is right.** "Not a
proof bug" is a claim, and the cheap version is: does the reproducer produce a
proof hole? If it did, the issue would be partly ours after all. That check is
[the corpus sweep](maintenance.md#what-the-corpus-reaches) pointed at one file, and it costs a
minute.

### 2. Where does the *learning* live?

This is the question worth a case study, because the answer is not "nowhere".

The maintainer will answer #12905 — reproduce it, locate it, fix it or explain
why it is not a bug. **That answer is evidence about how cvc5 issues get
addressed**, and it is evidence this repository is well placed to collect and
badly placed to act on. We ran assistants against cvc5 issues already, through a
`prompts/check_cvc5_issue` launcher since retired with the rest of that
workflow; what we have never done is record what the human answer taught that
the assistant missed.

**The current home is [Paideia](https://github.com/ajreynol/paideia).** The
original decision was to start `empeiria` as a child project under Dokimasia's
`tools/`, using the existing issue workflow and reporting discipline. On
2026-09-18, the maintainer moved it and `anakrisis` to Paideia. That repository
is now the source of truth for their charters, plans, protocols and ledgers.

[Empeiria's charter](https://github.com/ajreynol/paideia/blob/main/tools/empeiria/README.md)
owns the question of **working a cvc5 bug and learning from how the maintainers
answered**. General cvc5 development belongs there. Dokimasia keeps the proof
question: if an issue exposes a proof-completeness gap, that gap enters this
repository's register. Performance, including proof-production overhead,
belongs to
[Tachyon's Elaphros](https://github.com/ajreynol/tachyon/tree/main/tools/elaphros)
and is outside this repository's scope.

### What the original decision sought to change

The maintainer's side of the loop was already defined — that launcher wrote a
`TRIAGE:` block and left `HUMAN RESPONSE:` empty for a person. What was missing
is what happened **after** the response arrived: the answer was read and the
file was forgotten.

The change is small and is the whole point: **the response is an artifact, and
the delta between it and the triage is the thing worth keeping.** Not the
issue, not the fix — the difference between what an assistant concluded and what
a maintainer did. The work to record and learn from it belongs to Paideia,
which carries its status.

### Verdict

| | |
| --- | --- |
| **never** — for the issue itself | #12905 is not ours. No id, no register row, no report. The only work it earns is confirming it produces no proof hole |
| **carry — to ourselves** | the routing decision; [Empeiria in Paideia](https://github.com/ajreynol/paideia/tree/main/tools/empeiria) holds the general bug-work question |
| what would change it | the reproducer turning out to produce a trust step or an unhandled rule, which would make it partly a proof bug and partly ours |

**What we are not claiming.** We have not run the reproducer. The
classification rests on reading the assertion message, which names theory
explanation and not proof production — good enough to decline the issue, not
good enough to assert there is no proof hole behind it. That check is queued,
not done.

### A note on scope, since more of these will arrive

The generalisable part is the second question, not the first. Declining
out-of-scope work is easy and this repository should keep doing it. The harder
discipline is **noticing that the out-of-scope thing still produced evidence**,
and putting the evidence somewhere with a boundary around it rather than either
absorbing it or throwing it away.

The routing test, for the next one:

1. **Is it ours?** If it is about whether a step can produce a proof, it is a
   normal candidate and goes in the register.
2. **Is it about performance?** Time and memory overhead, including that of
   producing proofs, belong to
   [Tachyon's Elaphros](https://github.com/ajreynol/tachyon/tree/main/tools/elaphros).
3. **Is it general cvc5 development or learning from that work?** Route it to
   [Paideia](https://github.com/ajreynol/paideia); its project charters determine
   what work it takes on.
4. **If none applies, decline it and say why in one line.** Silence reads as
   agreement, and a tool that quietly collects other people's problems has
   stopped having a role.

## What cvc5 did

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


### What a run learned about itself

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
- **A retraction went stale in our favour.** [`findings.md`](experience.md#retractions)
  records that our baselines named `SETS_RELS_TCLOSURE_DOWN`, and that **no such
  id has ever existed in cvc5**. That was true when written. As of #12901 the id
  exists, because cvc5 renamed `TCLOSURE_UP` to it. The retraction stays — it is
  the record of an error we made — but it now needs the date qualifier it did
  not need before.

### The shape of an entry

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

## The log of changes

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
also been written up as `i-21` in the [issue register](README.md#the-register).

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
