# dokimasia

A static analyzer for the **proof-production code of cvc5** — the C++ that is
supposed to emit a proof for everything the solver does, and the seam where that
proof becomes a [Eunoia](https://github.com/cvc5/ethos) proof for `ethos` to
check.

Its question is **completeness, not soundness**: not *is this proof step valid*,
but *is there a path through the solver that reaches an inference no proof step
covers*.

*Status: nothing is written yet. This document and [`TODO.md`](TODO.md) are the
design. Every number quoted below was measured against cvc5 `16c4001e53` on
2026-08-30, and each one is a check waiting to be written.*

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
filed (see [what we promise](#what-we-promise-about-a-finding)).

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

Ten families. Each is a namespace of check codes, each check owns a witness, and
each says something about the pipeline that is true or false rather than
stylish.

| prefix | family | asks |
| --- | --- | --- |
| `MODE` | **the proof-mode delta** | what does enabling proofs change about the solver? which changes are silent? is `incompatibleWithProofs` still complete after this commit? |
| `RULE` | **the rule ledger** | for every `ProofRule`: who produces it, who checks it, who elaborates it, who prints it. Four columns; the interesting rows are the ones with a hole |
| `TRUST` | **the trust census** | every site that can introduce a trust step, keyed by `TrustId`; which are reachable by default, which are dead, which are unnamed |
| `INFER` | **inference coverage** | for each `InferenceId` a theory can emit, does its `InferProofCons` have a case, and is a `ProofGenerator` attached at the call site? |
| `RW` | **rewrite coverage** | can every rewrite the rewriter can perform be reconstructed as DSL or theory-rewrite steps, and which reconstructions are budget-dependent? |
| `PP` | **preprocessing coverage** | does every `PreprocessingPass` either prove its work or declare a `PREPROCESS_*` trust id? |
| `ELAB` | **macro elaboration** | for each `MACRO_*` and each granularity mode, is there an expansion, and does it terminate in non-macro rules? |
| `SEAM` | **the Eunoia seam** | `isHandled` and `isHandledSkolemId` as coverage problems, including their argument-dependent arms |
| `API` | **proof API contracts** | does a `ProofGenerator` return a proof of what was asked? which proof invariants are enforced only by `Assert`, and so are absent from release builds? |
| `KRN` | **kernel obligations** | see below |

Two of these — the rule ledger's argument/arity column, and severity derived
from whether a path is reachable rather than merely present — are things
**cvc5 asked anoieu for** (`cvc5-6`, `cvc5-7` in
[anoieu's tracker](https://github.com/ajreynol/anoieu/blob/main/docs/README.md)).
They are C++ questions. They live here.

## The stretch goal: a verified kernel

The arc of this project is to stop reporting holes and start certifying their
absence — to identify a **kernel** of cvc5 carrying the contract

> for every input in this fragment, under this configuration: if the kernel
> answers `unsat`, it emits a proof, every step of which `ethos` can check.

Static analysis gets there by turning that sentence into obligations and
discharging them one at a time. For a configuration *K* (a logic fragment plus
an option set):

1. **Closure** — determine what code *K* can reach: which theories, solvers,
   preprocessing passes, rewriters. Everything after this is relative to that
   set, and an unresolved indirect call is an assumption, not a pass.
2. **Coverage** — every inference site in the closure attaches a proof.
3. **Admissibility** — every `ProofRule` those sites emit is accepted by the
   seam, for the arguments they can pass.
4. **Elaboration** — every `MACRO_*` emitted is expanded at *K*'s granularity.
5. **Agreement** — *K* names the same solver with proofs on and off, or names
   the difference.
6. **Termination of reconstruction** — the budget problem above. Honestly, this
   one probably cannot be discharged against today's code; it is discharged by
   *changing* cvc5 so that reconstruction in the kernel is syntax-directed
   rather than searched.

The output is not a boolean. It is a **certificate**: the obligations
discharged, the assumptions left standing, and the exact frontier of what would
have to change to close each one. A kernel with three honest assumptions is
worth more than a green check that hides thirty.

Start small and grow: `QF_UF` at default options is a kernel someone could
plausibly certify this year, and every theory added is a measurable increment
rather than an aspiration. `KRN` checks are the obligations; `TODO.md` M6 is the
plan.

## Two things this repository is

**A tool**, first: an analyzer you run over a cvc5 checkout, in CI or before a
release, that reports where solving and proof production have come apart.

**And a reporting system.** Nothing dokimasia finds is about dokimasia. Every
finding is about *cvc5's* code, so findings have to be published where their
owners will read them, argued where they can be disagreed with, and tracked
until they are resolved or declined. `docs/findings.md` will carry how each was
confirmed; `docs/upstream.md` will carry what came back — accepted, declined,
deferred — because the log of what we got *wrong* is the more useful half.

## What we promise about a finding

Inherited from anoieu, unchanged, because they are the reason anyone reads the
second report:

- **It was confirmed before it was filed.** For an analyzer of a solver that
  means a reproducer: an input, an option set, and the trust step or incomplete
  proof it produces — quoted. A claim that a path is reachable is worth nothing
  until something reaches it.
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

*Designed, not built.* Python 3.10 or later; the table tier needs only a cvc5
checkout, the semantic tier additionally needs a `compile_commands.json`.

```bash
python3 -m dokimasia scan <cvc5>                  # every check over a checkout
python3 -m dokimasia rules <cvc5>                 # the ledger: produced / checked / elaborated / printed
python3 -m dokimasia rule TRUST_THEORY_REWRITE    # one rule, all four columns, every site
python3 -m dokimasia trust <cvc5> --reachable     # trust census, default options only
python3 -m dokimasia delta <cvc5>                 # what --produce-proofs changes about the solver
python3 -m dokimasia infer strings <cvc5>         # InferenceId coverage for one theory
python3 -m dokimasia kernel <cvc5> --logic QF_UF  # obligations: discharged, and still assumed
python3 -m dokimasia explain SEAM0001             # the manual page of a check
python3 -m dokimasia list-checks
```

A finding is meant to look like this:

```text
src/theory/strings/infer_proof_cons.cpp:1279: warning[INFER0002]: an inference with no proof reconstruction
     |
1279 |     ps.d_args.push_back(mkTrustId(nm, TrustId::THEORY_INFERENCE_STRINGS));
     |                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ falls through to a trust step
     = note: reached by InferenceId::STRINGS_I_CYCLE_E, which theory_strings.cpp:812 can emit
     = note: `--check-proofs-complete` fails on any input reaching this step
     = help: reproducer in docs/findings/infer0002.smt2 (default options, QF_S)
```

## In CI

The ladder anoieu proposes, aimed at cvc5's build: one versioned tool, a policy
file and a baseline owned by cvc5, and a corpus job *here* that fails our build
when a change would invent a false positive in theirs.

The rung that matters first is cheap and needs no baseline: **the ledger is a
regression test**. A commit that adds a `ProofRule` without a checker, an
`InferenceId` without a reconstruction case, or a technique to
`incompatibleWithProofs` without a note, is a commit that widens a hole nobody
sees until a benchmark finds it. That check runs in seconds and is the whole
argument for adoption.

## How this repository is maintained

**Written by an AI agent, under light human supervision.** The code, the checks,
the witnesses and the documents here are drafted by an agent working in this
repository; a human maintainer directs the work, reviews it, and decides what is
reported upstream. Findings are filed by the human, not the agent.
