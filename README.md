# dokimasia

A static analyzer for the **proof-production code of cvc5** — the C++ that is
supposed to emit a proof for everything the solver does, and the seam where that
proof becomes a [Eunoia](https://github.com/cvc5/ethos) proof for `ethos` to
check.

Its question is **completeness, not soundness**: not *is this proof step valid*,
but *is there a path through the solver that reaches an inference no proof step
covers*.

*Status: the first subtool is written — [`dokimasia.tcb`](dokimasia/tcb/)
measures the trusted computing base of cvc5's internal proof checker, and has
produced the first report, [`tcb-001`](docs/findings/tcb-001.md). The rest is
design: [`TODO.md`](TODO.md) is the plan, [`docs/hygiene.md`](docs/hygiene.md)
is the warm-up. Every number quoted below was measured against cvc5
`16c4001e53` on 2026-08-30.*

## The goal

**cvc5 should have complete proofs, always.**

That is the point of this repository. Everything else in it — the checks, the
hygiene standard, the TCB measurement, the CI proposals — is an *instrument* for
that, and should be judged by how much it moves it.

### The operating constraint: agility

Safe mode already has **almost no proof holes on SMT-LIB**. That single fact
sets the strategy, because it means the obvious approach is the wrong one:

- running a benchmark corpus is a **good oracle** and a **slow, largely
  exhausted signal**. It is worth doing once for a baseline. It is not where the
  next hole comes from;
- the holes that remain are, by definition, the ones **SMT-LIB does not reach**;
- so the thing to optimize is not compute — it is **feedback latency**. How
  quickly can we find the *next* hole, and how cheaply can we tell whether a
  change introduced one?

Ranked by how fast they return an answer, not by how much they cost:

| | signal | latency | finds |
| --- | --- | --- | --- |
| **1** | **static analysis** of the pipeline | seconds, no build | holes no input has ever reached — *the ones that are left* |
| **2** | **safe-mode consistency** — does safe mode do what it says? | seconds, no build | features that escape their own guard |
| **3** | **build-time pruning** — is the unsafe code even linked? | one build | a whole class of hole, converted into a link error |
| **4** | **fuzzing** (murxla is already in cvc5's build) | minutes | inputs a fixed corpus does not contain |
| **5** | **a curated corpus of known holes** | seconds | regressions on holes already reported |
| **6** | **SMT-LIB census** | hours | the baseline, once |

The priority order, so it is not ambiguous:

| | | |
| --- | --- | --- |
| **1** | **Complete proofs, always** | the goal |
| **2** | **Find the next hole fast** | latency is the metric. Rows 1–5 above, in that order |
| **3** | **Close the holes** | each is a concrete work item for a cvc5 developer, with a reproducer |
| **4** | **Make safe mode true by construction** | not a hand-maintained list that happens to be right — see [below](#the-second-stretch-goal-a-safe-build-that-cannot-be-unsafe) |
| **5** | Keep closed holes closed | regression. Useful, not the point |
| **6** | Argue a growing fragment is hole-free | the [kernel](#the-stretch-goal-a-kernel-you-can-argue-about). The long game |

Assertions, SARIF uploads and nightly jobs live below all of this. They are
worth doing and they are not why this exists.

### How we will know it is working

Two numbers, and neither is "benchmarks passed":

> **latency** — how long from "a hole exists" to "we can point at it"?
>
> **the latent count** — how many holes are reachable that no input has hit?

cvc5 already instruments the second half of the measurement:
`src/smt/proof_final_callback.cpp` registers
`finalProof::ruleUnhandledEoCount`, `finalProof::theoryRewriteRuleUnhandledEoCount`,
`finalProof::trustCount`, `finalProof::trustTheoryLemmaCount` and
`finalProof::minPedanticLevel`, all switched on by `--stats-internal`. Run once,
that gives the baseline; the interesting number is the *difference* between what
static analysis says is reachable and what the corpus actually hit.

## The second stretch goal: a safe build that cannot be unsafe

Safe mode promises "no feature that does not have full proof and model support."
Today that promise is kept **at runtime**, by `SetDefaults::setDefaultsPre`
turning things off by name, and by `NoOpTheoryRewriter` throwing
`SafeLogicException` when a disabled theory is reached anyway. The unsafe code is
still compiled, still linked, still one missed guard away.

There is already a build-time safe mode — `cvc5_option(ENABLE_SAFE_MODE)` sets
`-DCVC5_SAFE_MODE` — but it prunes almost nothing of cvc5's own code. **Five
files in `src/` mention it**, and two of those only reword an error message
("suggested options only in non-safe builds"). What it genuinely excludes is
third-party: LibPoly and CoCoA.

So the goal, in the same spirit as the kernel and sharing its tooling:

> **Make the safe build not contain the unsafe code.**

Progressive, exactly like the kernel argument, and with the same measure — the
dependency closure of the safe binary, which
[`dokimasia.tcb`](dokimasia/tcb/) already computes. Each feature moved from
"disabled at runtime" to "not compiled" is a class of proof hole converted into
a **link error**, which is the cheapest possible latency: the compiler finds it,
instantly, without an input.

And there is a consistency check available *right now*, statically, with no
build: **the runtime disable list and the build-time exclusion list must agree.**
Today they plainly do not — `setDefaultsPre` disables `sep`, `bags`, `ff` and
`fp`; `CVC5_SAFE_MODE` excludes LibPoly and CoCoA. Every feature that is disabled
at runtime but present in the safe build is a feature that a missed guard makes
reachable.

## The gap this exists to close

cvc5 already asks our question — at runtime, one benchmark at a time.
`--check-proofs-complete` walks the finished proof and fails the run if any node
is one `proof::EoPrinter::isHandled` rejects
([`src/smt/proof_final_callback.cpp:177`](https://github.com/cvc5/cvc5/blob/main/src/smt/proof_final_callback.cpp)):

```
The proof was incomplete due to a trust step with id THEORY_LEMMA, from theory THEORY_STRINGS
```

That is the right check. It has one property that no amount of CI fixes: **it
fires only on an input that reaches the step.** A theory can carry an inference
with no proof for years and no benchmark in the suite will name it. The check is
a sampler over a space nobody has measured.

dokimasia reads the same pipeline the other way. `--check-proofs-complete` takes
the proof a run produced and asks whether it is complete. dokimasia takes the
*code* and asks **which proofs it could ever produce**, and whether any of them
is not — with no benchmark in hand.

The relationship is the one `anoieu` has to `ethos`, and dokimasia is modelled
on [`anoieu`](https://github.com/ajreynol/anoieu) deliberately: same staging,
same check-with-a-witness discipline, same promise that a false positive is our
bug. Where anoieu is the eager counterpart to a lazy *checker*, dokimasia is the
static counterpart to a *dynamic* completeness test.

## The contract

The target, stated as one line:

> **If cvc5 solves it, cvc5 will produce a proof of it.**

### cvc5 already promises this, in one configuration

That sentence is not our invention. `--safe-mode=safe` is defined in
[`base_options.toml`](https://github.com/cvc5/cvc5/blob/main/src/options/base_options.toml)
as:

> *"Do not allow using expert options or theories, more than one regular option,
> or any feature that does not have **full proof and model support**."*

and its sibling `--safe-mode=stable` is defined as the one that *"**may allow
incomplete proofs** or models."*

So cvc5 draws the line itself, and **safe mode is the side of it that carries
the contract**. `SetDefaults::setDefaultsPre` implements the promise by
disabling, by name, the features that would break it — `nlCov`,
`ufSymmetryBreaker` ("never use symmetry breaker, which does not have proofs"),
`cegqiBv` ("proofs not yet supported"), `varEntEqElimQuant` ("a class of
rewrites in quantifiers we don't have proof support for"), the experimental
theories, and `bvSolver → BITBLAST_INTERNAL`. It upgrades `proofMode` to
`FULL_STRICT`, and turns on `checkProofsComplete` when proofs are checked.

**That list is hand-maintained.** Which gives dokimasia its sharpest question,
and its first priority:

> Is there anything reachable in safe mode with no proof support that nobody
> remembered to put on the list?

An input for which

```bash
cvc5 --safe-mode=safe --produce-proofs --check-proofs benchmark.smt2
```

reports `The proof was incomplete` is not a gap or a wish. It is **cvc5 failing
a promise it makes in its own documentation** — and it is the bug report this
project exists to produce.

Stable and unrestricted are worth analyzing too, and most of the checks below
apply unchanged. But findings there are *roadmap items*: those modes never
promised complete proofs, so a hole in them is a gap to prioritize, not a
contract to enforce. The ranking is in
[`docs/tooling.md`](docs/tooling.md#d5--safe-mode-first-and-the-reproducer-is-the-deliverable).

### The three ways it breaks

Three things have to hold for that to be true, and each is a different kind of
analysis. Keeping them apart is most of the design.

| | the claim | what breaks it |
| --- | --- | --- |
| **1. Coverage** | every inference the solver can make has a proof step | a theory lemma sent with no `ProofGenerator`; an `InferenceId` its theory's `InferProofCons` has no case for |
| **2. Admissibility** | every step it emits survives to a checkable proof | a `ProofRule` `EoPrinter::isHandled` rejects; a `MACRO_*` nothing elaborates; a rewrite reconstruction that runs out of budget |
| **3. Agreement** | the solver that produces the proof is the solver that solved it | `incompatibleWithProofs` silently turning a technique off, so the proof-producing run is a different run |

### Why (3) is not a footnote

**Proofs are off by default.** Solving without proofs is what users do, because
proofs are slow. So `produce-proofs` does not merely *observe* the solver — it
*changes* it, and cvc5 says so out loud in
[`SetDefaults::incompatibleWithProofs`](https://github.com/cvc5/cvc5/blob/main/src/smt/set_defaults.cpp):

- **refused outright** — `fresh-binders`, `global-negate`, deep restarts, lemma
  inprocessing, and sygus under full proofs; the run throws
  `FatalOptionException`;
- **changed underneath the user** — `bvAssertInput → false`,
  `bvSolver → BITBLAST_INTERNAL`, `nlCovVarElim → false`, and under
  `FULL_STRICT` also `ufSymmetryBreaker → false`, `cegqiMidpoint → true`,
  `cegqiUseInfInt/Real → false`, `dtSharedSelectors → false`.

Every line in the second group is a place where **the run that produced the
proof is not the run that solved the problem**. That is fine when it is
deliberate and written down. It is not fine that the list is hand-maintained: a
technique added without a line here produces proofs nobody has reasoned about,
and a technique added *with* a line here quietly makes the prover weaker than
the solver, with no record of how much.

So dokimasia analyzes **both configurations and the difference between them**.
A contract about a solver users do not run is not the contract.

## What we look at, and what we do not

**We analyze the C++ of cvc5.** The proof infrastructure in `src/proof`, the
proof reconstruction in `src/theory/*/infer_proof_cons.cpp` and
`src/rewriter`, the post-processing in `src/smt`, the option logic in
`src/smt/set_defaults.cpp`, and the rule/id enumerations that tie them together.

**We do not analyze Eunoia signatures.** `Cpc.eo` and its semantics are
`anoieu`'s subject and it is better at them. Where a question genuinely spans
the boundary — *does this `ProofRule` have a Eunoia rule to land on* — the C++
half is ours and the signature half is a reference we consult, never a file we
diagnose. Findings that belong to the signature get handed to anoieu.

The seam itself is C++ and is very much ours:
[`src/proof/eo/`](https://github.com/cvc5/cvc5/tree/main/src/proof/eo) is where
a cvc5 proof becomes a Eunoia proof, and "is the Eunoia pipeline healthy" is,
on this side of the line, a question about `eo_printer.cpp` and
`eo_node_converter.cpp`.

## The pipeline, and where it leaks

Each row is a place a proof can go missing, and each is an analysis family.

| stage | code | the completeness question |
| --- | --- | --- |
| **configure** | `smt/set_defaults.cpp` | does enabling proofs change which solver runs? |
| **preprocess** | `preprocessing/passes/*` | does every pass produce a proof, or a named `PREPROCESS_*` trust step? |
| **infer** | `theory/*/inference_manager*` | is every `InferenceId` emitted with a `ProofGenerator`? |
| **reconstruct** | `theory/*/infer_proof_cons.cpp` | does the theory's reconstructor have a case for it? |
| **rewrite** | `rewriter/`, `theory/*/rewrites` | is every rewrite reachable as a RARE or `ProofRewriteRule` step? |
| **check** | `proof/proof_checker.cpp` | does the rule have a checker, and does the checker actually check? |
| **elaborate** | `smt/proof_post_processor*.cpp` | is every `MACRO_*` expanded at the requested granularity? |
| **print** | `proof/eo/eo_printer.cpp` | does `isHandled` accept it, for the arguments it can carry? |

### What the measurements already say

Counted against cvc5 `16c4001e53`. These are the inputs to the first checks,
not findings — a finding is a claim, and claims get reproduced before they are
filed (see [what we promise](#what-a-finding-is-and-what-we-promise-about-it)).

| | count | why it matters |
| --- | --- | --- |
| `ProofRule` values | **172** | the vocabulary a proof can be written in |
| `ProofRewriteRule` values | **534** | the rewrite vocabulary underneath it |
| `TrustId` values | **75** | the *named* ways to admit a step without proving it |
| `InferenceId` values | **412** | the inferences the theories can make |
| `case ProofRule::` labels in `EoPrinter::isHandled` | **135** | the hand-maintained allowlist the Eunoia seam is gated on |
| distinct rules passed to `registerChecker`/`registerTrustedChecker` | **159 of 172** | the 13 that are not: 2 sentinels, and 11 `FF_*` |
| rules registered via `registerTrustedChecker` | pedantic levels **1–4** | cvc5's own declared ladder of how much a checker really checks |
| `ProofRule::MACRO_*` | **9** (plus 38 in `ProofRewriteRule`) | each needs an elaboration or it is permanently coarse |

Three things stand out already, and each is written up as a task in
[`TODO.md`](TODO.md):

- **`isHandled` is an allowlist of 135 case labels over 172 rules**, and several
  of its arms are *conditional* — they inspect the step's arguments
  (`isHandledTheoryRewrite`, `isHandledBitblastStep`). So "handled" is not a
  property of a rule; it is a property of a rule *applied to particular
  arguments*. Computing the unhandled set is the first real check, and the
  conditional arms are why it is not a `grep`.
- **The 11 `FF_*` rules have no registered checker and no emission site** —
  zero occurrences of `ProofRule::FF_` outside the enum, because
  `src/theory/ff` is entirely behind `#ifdef CVC5_USE_COCOA`. Declared in the
  public API and documented, produced by nothing. Harmless for soundness;
  exactly the kind of drift between a public enum and its implementation that a
  ledger catches and a reviewer does not.
- **Proof completeness currently depends on a search budget.**
  `smt/proof_post_processor_dsl.cpp` reconstructs rewrite proofs under
  `--proof-rewrite-rcons-rec-limit` (default 5) and
  `--proof-rewrite-rcons-step-limit`; when the search fails, the macro step
  *stays*. A proof is therefore complete or not depending on how long a search
  was allowed to run. No static analysis can discharge that as stated — which
  makes it the first thing a kernel contract has to confront rather than
  inherit.

## The analyses

Eleven families. Each is a namespace of check codes, each check owns a witness, and
each says something about the pipeline that is true or false rather than
stylish.

| prefix | family | asks |
| --- | --- | --- |
| `MODE` | **the safe-mode contract** | is anything reachable in `--safe-mode=safe` without proof support and not on the disable list? and what does enabling proofs change about the solver at all? |
| `RULE` | **the rule ledger** | for every `ProofRule`: who produces it, who checks it, who elaborates it, who prints it. Four columns; the interesting rows are the ones with a hole |
| `TRUST` | **the trust census** | every site that can introduce a trust step, keyed by `TrustId`; **which are reachable in safe mode**, which are dead, which are unnamed |
| `INFER` | **inference coverage** | for each `InferenceId` a theory can emit, does its `InferProofCons` have a case, and is a `ProofGenerator` attached at the call site? |
| `RW` | **rewrite coverage** | can every rewrite the rewriter can perform be reconstructed as DSL or theory-rewrite steps, and which reconstructions are budget-dependent? |
| `PP` | **preprocessing coverage** | does every `PreprocessingPass` either prove its work or declare a `PREPROCESS_*` trust id? |
| `ELAB` | **macro elaboration** | for each `MACRO_*` and each granularity mode, is there an expansion, and does it terminate in non-macro rules? |
| `SEAM` | **the Eunoia seam** | `isHandled` and `isHandledSkolemId` as coverage problems, including their argument-dependent arms |
| `API` | **proof API contracts** | does a `ProofGenerator` return a proof of what was asked? which proof invariants are enforced only by `Assert`, and so are absent from release builds? |
| `TCB` | **the checker's dependency surface** ✅ | how much of cvc5 must be right for `--check-proofs` to mean something? what does each dependency edge cost, and is it growing? |
| `KRN` | **kernel obligations** | see below |

Two of these — the rule ledger's argument/arity column, and severity derived
from whether a path is reachable rather than merely present — are things
**cvc5 asked anoieu for** (`cvc5-6`, `cvc5-7` in
[anoieu's tracker](https://github.com/ajreynol/anoieu/blob/main/docs/README.md)).
They are C++ questions. They live here.

## The stretch goal: a kernel you can argue about

The arc of this project is to stop reporting holes and start being able to say
which part of cvc5 is its proof kernel.

**This is not a claim about verification tools.** "Verified kernel" here does not
mean a machine-checked theorem, and treating it that way sets the bar somewhere
useless — nothing available today verifies a contract like this over cvc5's C++,
and waiting for something that does means delivering nothing. The goal is softer
and much more achievable:

> **Make it easier to argue what cvc5's proof-producing kernel is.**

An argument, made to a person, that this set of code is what has to be right.
That goal is *progressive*: it improves by degrees, every degree is worth
having on its own, and no step is the last one. The axes it improves along:

| axis | the question | today |
| --- | --- | --- |
| **nameable** | can you enumerate the kernel at all? | partly — `--safe-mode=safe` names a configuration, not a set of code |
| **closed** | does the boundary hold — does nothing inside reach out? | unknown, and [`tcb-001`](docs/findings/tcb-001.md) is one place it does not |
| **small** | how much is inside? | the internal checker compiles against 41,446 lines, 8.0% of `src/` |
| **local** | can a reader check one obligation by reading one function? | rarely |
| **mechanized** | is any part machine-checked? | no, and that is the *last* axis, not the first |

Progress on any row is real progress. A kernel that is nameable and closed but
unverified is worth far more than one nobody can point at, and the measure that
matters is **how long the argument is and how much of it a reader can check** —
not whether a tool printed `QED`.

### Hygiene comes first, because you cannot bound what you cannot name

Every such argument is made out of entities — inferences, rules, trust steps —
and is only as sharp as those entities are. If an `InferenceId` is emitted at
eight places, "the inferences theory X can make" is not an enumerable set, and
nothing quantified over it means anything.

So the warm-up project is a **proof hygiene standard** for cvc5:
[`docs/hygiene.md`](docs/hygiene.md). Naming conventions, calling conventions,
checker registration, and the discipline around inference ids — which are cvc5's
existing *informal* proof markers, and the natural spine for all of this. Ten
rules, each with a measurement behind it, most of them ratifying what cvc5
already does. The chain the whole project runs on:

**hygiene → nameable entities → a drawable boundary → an argument someone can
check → (eventually, in places) mechanization.**

### Measuring the kernel: the checker's TCB

The internal proof checker is the natural kernel candidate — it is the component
that decides whether a cvc5 proof is valid — and its value is inversely
proportional to how much of cvc5 it needs. That is measurable today, so it is
the first thing this repository actually built:

```bash
python3 -m dokimasia.tcb measure <cvc5>   # 179 files, 41,446 lines, 8.0% of src/
python3 -m dokimasia.tcb cuts    <cvc5>   # what each dependency edge costs
python3 -m dokimasia.tcb why     <cvc5> theory/strings/core_solver.h
python3 -m dokimasia.tcb baseline <cvc5> --check   # the ratchet, for CI
```

The first finding came out of it:
[**`tcb-001`**](docs/findings/tcb-001.md) — 12 of 13 rule checkers are clean,
but six include the headers of the theory solvers they check, to reach `static`
helpers parked on the solver classes. The refactoring is mechanical and the
report names it per site.

That number going down *is* the kernel argument getting shorter. It needs no
verification tool, no build, and nobody's agreement to start.

## Two things this repository is

**A tool**, first: an analyzer you run over a cvc5 checkout, in CI or before a
release, that reports where solving and proof production have come apart.

**And a reporting system.** Nothing dokimasia finds is about dokimasia. Every
finding is about *cvc5's* code, so findings have to be published where their
owners will read them, argued where they can be disagreed with, and tracked
until they are resolved or declined. `docs/findings.md` will carry how each was
confirmed; `docs/upstream.md` will carry what came back — accepted, declined,
deferred — because the log of what we got *wrong* is the more useful half.

## What a finding is, and what we promise about it

Four kinds, extending anoieu's three:

| | kind | what it asks of cvc5 |
| --- | --- | --- |
| **A** | a defect | an incomplete proof, named down to the input that produces it |
| **B** | an adoption | run a check of ours in your CI, with the configuration it needs |
| **C** | a change to the pipeline | to the proof infrastructure or to what safe mode promises |
| **D** | **an assertion** | a patch adding an invariant to cvc5, so the check lives in your tree and not ours |

**Kind A is what this repository is for.** An incomplete proof, named down to
the input that produces it, is the only finding that directly serves
[the goal](#the-goal). The other three are instruments: B and D are ways of
making a fix stick, C is a way of changing what the pipeline promises. They are
cheap and worth doing, and none of them is the reason this exists.

A note on D, since it is the most easily overrated: an assertion converts a
silent hole into a loud failure and no more. It does not close a hole. It is
worth proposing when an invariant we check is one cvc5 could check about itself
at startup — then the deliverable is the patch and our check gets deleted. See
[`docs/tooling.md`](docs/tooling.md#d3--where-an-invariant-should-live).

The promises:

- **It was confirmed before it was filed, and for kind A that means an input.**
  Not a code location and an argument — a `.smt2` file, an option set, and the
  quoted `--check-proofs-complete` failure. A claim that a path is reachable is
  worth nothing until something reaches it, and the static analysis's job is to
  tell us *where to look*, not to substitute for looking.
- **A suggested assertion that fires falsely is our bug.** Exactly as a false
  positive is. So no assertion is proposed until it has been applied to a cvc5
  build configured `--assertions` and the regression suite has passed with it in
  place. An assertion we have not run is a hypothesis, and hypotheses go in
  `docs/findings.md`, not in a patch.
- **A false positive is our bug, not yours.** Every check that fires wrongly on
  cvc5 gets narrowed until it stops, and each narrowing is recorded as what it
  is — a fact about cvc5 we had got wrong. Our own CI runs the checks over a
  pinned cvc5 so that a change inventing a false positive fails *this* build
  before it reaches theirs.
- **Severity is reachability.** "This rule has no checker" is a different claim
  from "this rule has no checker and a default-options run in `QF_LIA` emits
  it." We will say which one we mean, every time.
- **Declining is an outcome.** A finding can end in "won't fix" with a reason,
  and the check gets a suppression or a `disable` in the policy file. Both beat
  the same argument every month.

## The name

**δοκιμασία** — *dokimasia* — was the scrutiny every official-elect in
classical Athens underwent before taking office. It did not ask whether the man
had done wrong. It asked whether he was **fit to serve**, and it asked *before*
he served: fail the scrutiny and the office was never held.

That is the distinction this tool is built on. Soundness asks, after the fact,
whether a proof is valid. Completeness asks, in advance, whether a code path can
produce a proof at all — a fitness question, asked before the office is taken,
about a candidate who has not yet done anything wrong. cvc5's own scrutiny
happens at runtime, when a benchmark finally exercises the path. Ours happens
first.

The related adjective, **δόκιμος**, means *tested, and approved*. That is what a
kernel certificate would say.

## Using it

*Designed, not built.* Tier 0 is Python 3.10 or later and needs only a cvc5
checkout; tiers 1 and 2 ship as checks inside cvc5's own nightly (see
[how it ships](#how-it-ships)).

```bash
python3 -m dokimasia safe <cvc5>                  # THE check: holes reachable in --safe-mode=safe
python3 -m dokimasia scan <cvc5>                  # every check over a checkout
python3 -m dokimasia rules <cvc5> --mode safe     # the ledger: produced / checked / elaborated / printed
python3 -m dokimasia rule TRUST_THEORY_REWRITE    # one rule, all four columns, every site
python3 -m dokimasia trust <cvc5> --mode safe     # trust census, restricted to safe mode
python3 -m dokimasia delta <cvc5>                 # safe vs stable vs unrestricted, per option
python3 -m dokimasia infer strings <cvc5>         # InferenceId coverage for one theory
python3 -m dokimasia kernel <cvc5> --logic QF_UF  # obligations: discharged, and still assumed
python3 -m dokimasia explain SEAM0001             # the manual page of a check
python3 -m dokimasia list-checks
```

A finding is meant to look like this:

```text
src/theory/strings/infer_proof_cons.cpp:1279: error[INFER0002]: an inference with no proof reconstruction
     |
1279 |     ps.d_args.push_back(mkTrustId(nm, TrustId::THEORY_INFERENCE_STRINGS));
     |                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ falls through to a trust step
     = note: reached by InferenceId::STRINGS_I_CYCLE_E, which theory_strings.cpp:812 can emit
     = note: rank 1 — reachable under --safe-mode=safe, which promises full proof support
     = note: cvc5 --safe-mode=safe --produce-proofs --check-proofs docs/findings/infer0002.smt2
             reports: The proof was incomplete due to a trust step with id
             THEORY_INFERENCE_STRINGS, from theory THEORY_STRINGS
     = help: minimized with ddsmt from QF_S benchmark <origin>
```

## How it ships

**The infrastructure already exists, and this changed the design.** cvc5 runs a
nightly [`static_analysis.yml`](https://github.com/cvc5/cvc5/blob/main/.github/workflows/static_analysis.yml)
that builds a **custom clang-tidy plugin** from `contrib/tidy-checks/`, builds
cvc5 inside a **CodeQL database**, runs a **custom CodeQL query** that computes
a transitive call-graph closure, decodes it to CSV, and passes that CSV *into*
the clang-tidy check as a configuration option.

That pairing — CodeQL answers the whole-program question, a clang-tidy check
consumes the answer and judges each site — is precisely what dokimasia's harder
checks need. cvc5's existing `cvc5-node-id-determinism` check is a domain
invariant enforced exactly that way. Ours are the same shape with different
roots.

So we ship as three artifacts, chosen by what each question needs:

| tier | question | artifact | cost |
| --- | --- | --- | --- |
| **0 — ledger** | is this table consistent with that table? | standalone, reads a checkout | **seconds, no build** |
| **1 — local** | does this call site attach a proof? | `cvc5-proof-*` checks in `contrib/tidy-checks/` | one clang-tidy pass |
| **2 — closure** | what can safe mode reach? | queries in `contrib/codeql/` | one CodeQL DB build |

Tiers 1 and 2 belong **upstream, in cvc5's tree**, because that is where the
pipeline is. A tool cvc5 must install and schedule will not be run; a check in
`contrib/tidy-checks/` is already built, loaded and enforced by a job that
exists. Tier 0 stays here and runs per-push, because table-against-table checks
need a bracket matcher rather than a compiler — and because it produces findings
before anyone configures a build.

Two adoptions we can propose immediately, independent of any check we write:

- **Upload SARIF.** The nightly enforces via `-warnings-as-errors` and nothing
  else, so findings never reach GitHub's code-scanning UI, are not annotated on
  pull requests, and have no baseline or dismissal mechanism.
- **The ledger as a per-push lint.** A commit that adds a `ProofRule` with no
  checker, an `InferenceId` with no reconstruction case, or a technique to
  `incompatibleWithProofs` with no note, widens a hole nobody sees until a
  benchmark finds it. That check runs in seconds.

The full survey of C++ static analysis tooling, why none of it can ask our
question, and the design decisions that follow, are in
[`docs/tooling.md`](docs/tooling.md).

## How this repository is maintained

**Written by an AI agent, under light human supervision.** The code, the checks,
the witnesses and the documents here are drafted by an agent working in this
repository; a human maintainer directs the work, reviews it, and decides what is
reported upstream. Findings are filed by the human, not the agent.
