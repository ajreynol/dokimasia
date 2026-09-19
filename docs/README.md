# dokimasia's documentation

**cvc5 should have complete proofs, always.** That is the point of this
repository; everything in it is an instrument for that and should be judged by
how much it moves it. This page is the argument and the registers. Three other
documents complete the set, and `docs/` holds nothing else:

| | |
| --- | --- |
| **this page** | the goal, the contract, the checks, and everything we are asking cvc5 to act on |
| [`maintenance.md`](maintenance.md) | how to run it, what each command answers, the pins, the tests and the script catalogue |
| [`experience.md`](experience.md) | what a finding is, the bar it clears, the log and retractions, and what cvc5 did about them |
| [`discussion.md`](discussion.md) | the standing channel to the rest of the ecosystem, and the gate on responding to it |

Generated views are data artifacts and live with the data, in
[`bug_db/`](../bug_db/README.md): [`bugs.md`](../bug_db/bugs.md) is every
recorded observation, [`fragment.md`](../bug_db/fragment.md) is the supported
fragment per theory.

**The boundary is cvc5's proofs.** General cvc5 development belongs to
[Paideia](https://github.com/ajreynol/paideia). Performance, including
proof-production overhead, belongs to
[Tachyon's Elaphros](https://github.com/ajreynol/tachyon/tree/main/tools/elaphros).

## The stance

**Completeness, not soundness.** Not *is this proof step valid*, but *is there a
path through the solver that produces no proof at all*.

**White box, and eager.** We read the code. Finding holes by generating inputs
is murxla's job and it is good at it; the ones that matter now are the holes
**no input has reached**, which is what reading finds and running cannot. cvc5
asks our question at runtime — `--check-proofs-complete`, one benchmark at a
time, firing only on an input that reaches the step. We ask it of the code, with
no benchmark in hand.

**Only claims we can back.** Every number we publish comes from a tool here that
runs in seconds against a checkout. A claim we cannot measure is a design note
and lives in [`TODO.md`](../TODO.md) as one. What we will and will not say about
somebody else's code is [the promises](experience.md#the-promises), each with
the tier and the mechanism behind it, enforced at the edge by
[the bar](experience.md#the-bar).

### The operating constraint: agility

Safe mode already has **almost no proof holes on SMT-LIB**, which makes the
obvious approach the wrong one. A benchmark corpus is a good oracle and a slow,
largely exhausted signal; the holes that remain are by definition the ones
SMT-LIB does not reach. So the thing to optimise is not compute — it is
**feedback latency**.

| | signal | latency | finds |
| --- | --- | --- | --- |
| **1** | **static analysis** of the pipeline | seconds, no build | holes no input has ever reached — *the ones that are left* |
| **2** | **safe-mode consistency** — does safe mode do what it says? | seconds, no build | features that escape their own guard |
| **3** | **build-time pruning** — is the unsafe code even linked? | one build | a whole class of hole, converted into a link error |
| **4** | **fuzzing** — murxla's job, not ours | minutes | inputs a fixed corpus does not contain |
| **5** | **a curated corpus of known holes** | seconds | regressions on holes already reported |
| **6** | **SMT-LIB census** | hours | the baseline, once |

Priority order, so it is not ambiguous: **1** complete proofs, always — the goal.
**2** find the next hole fast; latency is the metric. **3** close the holes, each
with a reproducer. **4** make safe mode true by construction rather than by a
hand-maintained list. **5** keep closed holes closed. **6** argue a growing
fragment is hole-free. Assertions, SARIF uploads and nightly jobs live below all
of it.

## The contract

> **If cvc5 solves it, cvc5 will produce a proof of it.**

That sentence is not our invention. `--safe-mode=safe` is defined in
`base_options.toml` as allowing no feature *"that does not have full proof and
model support"*, and its sibling `--safe-mode=stable` as the one that *"may
allow incomplete proofs"*. **Safe mode is the side of the line that carries the
contract.** `SetDefaults::setDefaultsPre` implements it by disabling, by name,
the features that would break it — `nlCov`, `ufSymmetryBreaker`, `cegqiBv`,
`varEntEqElimQuant`, the experimental theories, `bvSolver → BITBLAST_INTERNAL` —
upgrades `proofMode` to `FULL_STRICT`, and turns on `checkProofsComplete` when
proofs are checked.

**That list is hand-maintained**, which gives the sharpest question here: *is
there anything reachable in safe mode with no proof support that nobody
remembered to put on the list?* An input for which
`cvc5 --safe-mode=safe --produce-proofs --check-proofs b.smt2` reports
`The proof was incomplete` is not a gap or a wish — it is cvc5 failing a promise
it makes in its own documentation.

Stable and unrestricted are worth analysing too, and most checks apply
unchanged, but findings there are roadmap items rather than contract violations.

### The three ways it breaks

| | the claim | what breaks it |
| --- | --- | --- |
| **1. Coverage** | every inference the solver can make has a proof step | a theory lemma sent with no `ProofGenerator`; an `InferenceId` its theory's `InferProofCons` has no case for |
| **2. Admissibility** | every step it emits survives to a checkable proof | a `ProofRule` `EoPrinter::isHandled` rejects; a `MACRO_*` nothing elaborates; a rewrite reconstruction that runs out of budget |
| **3. Agreement** | the solver that produces the proof is the solver that solved it | `incompatibleWithProofs` silently turning a technique off, so the proof-producing run is a different run |

**Why (3) is not a footnote.** Proofs are off by default, so `produce-proofs`
does not merely observe the solver — it changes it, and cvc5 says so in
`SetDefaults::incompatibleWithProofs`: some options are refused outright
(`fresh-binders`, `global-negate`, deep restarts, lemma inprocessing, sygus
under full proofs), and others are **changed underneath the user**
(`bvAssertInput`, `bvSolver`, `nlCovVarElim`, and under `FULL_STRICT` also
`ufSymmetryBreaker`, `cegqiMidpoint`, `cegqiUseInfInt/Real`,
`dtSharedSelectors`). Every line in the second group is a place where the run
that produced the proof is not the run that solved the problem. So we analyse
both configurations **and the difference between them**.

### Where a proof leaks

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

### What we do not analyse

**We do not analyse Eunoia signatures.** `Cpc.eo` and its semantics are
[anoieu](https://github.com/ajreynol/anoieu)'s subject. Where a question spans
the boundary — *does this `ProofRule` have a Eunoia rule to land on* — the C++
half is ours and the signature half is a reference we consult, never a file we
diagnose. **The seam itself is C++ and is very much ours:** `src/proof/eo/` is
where a cvc5 proof becomes a Eunoia proof.

## Why cvc5 should care

Three claims, ranked by how well we can back them, and one admission. Everything
was measured against cvc5 `40a4bb7e4`.

### 1. We supply the denominator your own counters lack

cvc5 already measures proof incompleteness: `proof_final_callback.cpp` registers
`finalProof::trustCount`, `ruleUnhandledEoCount`,
`theoryRewriteRuleUnhandledEoCount`, `trustTheoryLemmaCount` and
`minPedanticLevel`, all switched on by `--stats-internal`. Over a corpus those
are a **numerator**: the holes something actually reached. They cannot be a
denominator — *how many holes exist to be reached* is a property of the code,
and no execution reports the paths it did not take.

| the population | today | from |
| --- | --- | --- |
| declared `TrustId`s, constructed somewhere | **70 of 75** | `trust census` |
| inferences whose theory's `InferProofCons` does not name them, so its default case builds a `TRUST` step | **79** | `infer coverage` |
| `ProofRule`s the solver emits that `EoPrinter::isHandled` refuses | **14** | `ledger holes` |
| rewrites applied and unprintable | **40** | `rewrites gaps` |

Measured for one corpus, all 2,608 `regress0` benchmarks:

| | proofs produced | reached **any** hole |
| --- | --- | --- |
| `--safe-mode=safe` | 1,061 | **0** |
| unrestricted | 1,236 | **129** (10.4%) |

The subtraction across the whole inventory is the number this repository should
be judged on: **182 of 203 declared holes have never been reached by any input
we have run.** 21 were reached outside safe mode, none inside it.

The same run validated the static tier against the runtime oracle — cvc5's
completeness check is literally `!EoPrinter::isHandled(...)`, the predicate
`dokimasia.ledger` computes without building: **nine of the fourteen gaps we
predicted were hit, and nothing hit was outside our prediction.** And it bounds
us honestly: on `regress0`, safe mode is clean.

### 2. Three properties your pipeline depends on are true today and asserted nowhere

Each holds at `40a4bb7e4`, none is checked by anything in cvc5's tree, and the
failure mode of all three is **silence**.

**The completeness chain is an implication, not a flag.**
`--check-proofs-complete` appears nowhere in cvc5's CI, and cannot: it is
`category = "expert"` and safe and stable mode refuse expert options.
Completeness is obtained as a side effect — in a safe build `setDefaultsPre`
turns it on when `--check-proofs` is set and no granularity was requested. Four
links, and `dokimasia.ci proofs` prints each:

```
1. [ok ] a build job runs in safe mode              ubuntu:safe-mode
2. [ok ] that job runs --tester proof               ubuntu:safe-mode
3. [ok ] the tester passes --check-proofs           --check-proofs --proof-check=lazy
4. [ok ] the tester requests no --proof-granularity none requested
```

Adding a `--proof-granularity` flag to the proof tester — an ordinary thing to
want — breaks link 4 and completeness testing stops. **No test fails.** A fifth
link once asked for the flag to be named here; it was withdrawn, because making
the option settable would equally permit `--no-check-proofs-complete`
([the retraction](experience.md#retractions) has the detail).

**Safe mode's disable list is hand-maintained and unchecked.** The guard fires
when a user *sets* an option, never on its default value, which is how
`stringLazyPreproc` gets through (`i-2`).

**The checker's trusted surface is not measured** — 179 files, 41,446 lines,
8.0% of `src/`. Nothing in cvc5 measures it, so nothing would notice it growing,
and it is the number any kernel argument starts from.

**The mechanism, and the first thing it caught.** Every property has a
`baseline --check` ratchet: no build, no dependencies, seconds against a
checkout. Run against the commit they were recorded at, two of eight failed —
not because cvc5 had changed, but because our baselines named an `InferenceId`
cvc5 had never had, and one tool stood ready to report a rename in cvc5 as an
improvement in cvc5's proof coverage. Both fixed, all eight clean. **The first
thing our ratchets caught was us**, which is a smaller claim than we might have
liked and a better-evidenced one.

### 3. A candidate list with the option gate already applied

When we say a hole is reachable, we have asked whether safe mode blocks it
rather than reporting presence and leaving severity to the reader. That
distinction has killed several of our own rows — `s-1` through `s-7` below.

### What we have not delivered

**Kind A — an incomplete proof named down to the input that produces it — is
what this repository is for, and we have produced none.** One finding is filed
([`tcb-001`](experience.md#tcb-001--proof-rule-checkers-compile-against-the-theory-solvers-they-check)),
a kind C refactoring ask. The accurate summary is **instrumentation that works,
a small number of live hypotheses, and no confirmed hole.** A cvc5 maintainer is
entitled to weigh it on that basis.

**What would show we are wrong:** the corpus difference comes back small, so the
runtime oracle is sufficient and this is a ratchet repository rather than a
hole-finding one; or our parsing turns out load-bearing and brittle, which is
the whole argument for `R1`.

## The checks

The facets we audit. Each is a namespace of check codes; each check owns a
witness; each says something about the pipeline that is true or false. There are
**the eighteen facets** below, and the individual claims are in
[the register](#the-register).

✅ live · ◐ partial · ○ designed


| | prefix | facet | asks |
| --- | --- | --- | --- |
| ✅ | `TCB` | **the checker's dependency surface** | how much of cvc5 must be right for `--check-proofs` to mean anything — and is it growing? |
| ◐ | `MODE` | **the safe-mode contract** | is anything reachable in safe mode without proof support? what does enabling proofs change about the solver at all? |
| ✅ | `RULE` | **the rule ledger** | for every `ProofRule`: who produces it, checks it, elaborates it, prints it. The interesting rows are the ones with a hole |
| ✅ | `TRUST` | **the trust census** | every site that can introduce a trust step, keyed by `TrustId`: which are reachable, which are dead, which are unnamed |
| ✅ | `INFER` | **inference coverage** | for each `InferenceId` a theory emits, does its reconstruction have a case, and is a `ProofGenerator` attached? |
| ✅ | `RW` | **rewrite coverage** | can every rewrite the rewriter performs be reconstructed — and which reconstructions depend on a search budget? |
| ◐ | `PP` | **preprocessing coverage** | does every pass either prove its work or declare a `PREPROCESS_*` trust id? |
| ◐ | `ELAB` | **macro elaboration** | is every `MACRO_*` expanded at each granularity, terminating in non-macro rules? |
| ◐ | `SEAM` | **the Eunoia seam** | `isHandled` and `isHandledSkolemId` as coverage problems, including their argument-dependent arms |
| ◐ | `INFERID` | **inference-id hygiene** | is each `InferenceId` produced at one place, so the control-flow graph is unambiguous? |
| ✅ | `BUILD` | **the safe-build invariant** | is a safe build still an unrestricted build with one option default flipped? While it is, excluding safe mode from a build configuration costs only diagnostics |
| ✅ | `CI` | **is cvc5's proof CI intact?** | do the jobs that guard proof completeness still run, with the flags they need — independently of anyone remembering to keep them? |
| ○ | `API` | **proof API contracts** | does a `ProofGenerator` return a proof of what was asked? which invariants vanish in a release build? |
| ✅ | `GATE` | **option gates** | which option must be on for a term kind — and so a rule — to occur, so severity can be computed instead of guessed |
| ✅ | `FRAG` | **the supported fragment** | which term kinds may appear per theory under safe mode — and do the three enforcement mechanisms actually cover it? |
| ✅ | `SIG` | **signature agreement** | do the rules and skolems cvc5 can print exist in the Eunoia signature, and does its own documentation match? |
| ✅ | `LATENT` | **the latent set** | of the holes the facets above declare, which has no input behind it — the static inventory minus what a corpus reached |
| ○ | `KRN` | **kernel obligations** | see [the wishues](README.md#the-two-wishues) |

Two of these — the ledger's arity column, and severity derived from reachability
rather than presence — are things [cvc5 asked anoieu
for](https://github.com/ajreynol/anoieu/blob/main/docs/README.md). They are C++
questions, so they live here.
## What each facet has produced

Only the live ones, and only what a check actually returned against a checkout.
The register row for each is in [`issues.md`](README.md#the-register).

| prefix | tool | measured at `40a4bb7e4` | rows |
| --- | --- | --- | --- |
| `TCB` | `dokimasia.tcb` | 179 files, 41,446 lines, 8.0% of `src/`; 6 rule checkers compile against the solvers they check | [`f-1`](experience.md#tcb-001--proof-rule-checkers-compile-against-the-theory-solvers-they-check) |
| `MODE` | `dokimasia.modes` | 24 distinct option settings changed in safe mode; 2 options declare no proof support and stay on, of which 1 survives review | `i-2`, `i-5` |
| `RULE` | `dokimasia.ledger` | 170 rules: 113 always printable, 17 conditionally, 40 never — 14 by design, 12 unreachable, **14 real gaps** | `i-7`, `i-12` |
| `TRUST` | `dokimasia.trust` | 75 declared ids: 70 live, 4 dead, 8 sites built with `TrustId::NONE` | `i-9`, `i-10`, `i-11` |
| `INFER` | `dokimasia.infer` | 79 inferences fall through to a trust step by construction; 10 theories have no `InferProofCons` at all | `i-22`, `i-6` |
| `RW` | `dokimasia.rewrites` | 533-rule vocabulary; 40 applied and unprintable; 3 taken only outside safe mode | `i-17`, `i-18` |
| `INFERID` | `dokimasia.inferid` | 51 ids produced at more than one site, 14 produced nowhere, 21 emitted with a sentinel | `i-8` |
| `CI` | `dokimasia.ci` | 4 of 22 jobs run a proof tester; all 4 completeness links hold, and the guarantee still rests on configuration | `i-3`, `i-13`, `i-14` |
| `GATE` | `dokimasia.gates` | 59 term kinds carry an option gate; verdicts blocked / partial / open per rule | `i-1`, `s-1`–`s-5` |
| `FRAG` | `dokimasia.fragment` | 341 kinds over 14 theories (216 available, 125 blocked); two safe-mode options gate no kind at all | `i-15` |
| `BUILD` | `dokimasia.buildmode` | **8 conditionals on the safe-build macro, all benign**; 0 excluded sources; 0 behavioural readers of `isSafeBuild()` | [`cases/safe-build-vs-safe-mode.md`](experience.md#cvc5-12899--is-forbidding-safe-mode-with-debug-symbols-actually-a-restriction) |
| `LATENT` | `dokimasia.latent` | **182 of 203 declared holes reached by no input**; 21 reached only outside safe mode; 0 in safe mode | [`reachability.md`](maintenance.md#what-the-corpus-reaches) |
| `SIG` | `dokimasia.signature` | 0 printable rules undeclared; 24 skolems constructed and unprintable; 1 documented arity disagreement | `i-19`, `i-20`, `i-21` |

The `MODE` row is the shape to notice: the check returned two options and one of
them ([`s-4`](README.md#settled), `macrosQuantMode`) was spurious — its effect is
gated by a flag defaulting to `false`, which a defaults-only comparison cannot
see. The tool prints that limit beside the result.

## What a partial or designed facet is waiting on

| prefix | blocked on |
| --- | --- |
| `PP` | the pass↔trust-id correspondence is not derivable by name (`i-11`, [`R7`](README.md#open--asks)) |
| `ELAB` | granularity is a runtime property; deciding it statically needs the elaboration graph, not the rule list |
| `SEAM` | `SEAM0002` — characterising the unhandled *argument* set of the conditional arms, not just the rule |
| `INFERID` | nothing; it is live but its precision is bounded by `i-8`, which is cvc5's to fix ([`R4`](README.md#open--asks)) |
| `API` | needs the call site, which is the AST tier — see [`tooling.md`](maintenance.md#the-static-analysis-landscape) |
| `KRN` | [`i-4`](README.md#the-register): reconstruction runs under a search budget with no termination argument, which bounds what any kernel contract can claim |

## The check-code convention

A check code is `PREFIX` plus four digits — `RULE0001`, `TRUST0003`,
`CI0002` — allocated once and never reused, the same convention anoieu uses for
signatures. A code names a *question asked of the code*, not an occurrence: one
code can return many rows or none, and returning none is a fact about the check
rather than about cvc5. The structured analyzer's emitted codes are below.
Designed checks remain in [`TODO.md`](../TODO.md) and are not emitted.

## Structured observations

These codes describe static observations, not reviewed verdicts. Both the
program and the independent agent use this catalogue. The
[analyzer guide](maintenance.md#identity-and-evidence) defines the entity keys.

| code | emitted when | limitation |
| --- | --- | --- |
| `RULE0001` | a syntactically produced rule has no registered checker | production and checker registration are recovered from text |
| `RULE0002` | a produced rule has a trusted checker registration with a nonzero pedantic level | intentional trust may be acceptable; the level is evidence, not severity |
| `ELAB0001` | a produced `MACRO_*` rule has no detected postprocessor expansion | only the scanned postprocessor files are considered |
| `SEAM0001` | a produced rule is never handled by the Eunoia printer, excluding macros, expanded rules and intentional format/trust refusals | production alone does not establish safe-mode reachability |
| `CI0001` | a safe/stable matrix job has no proof tester | CI YAML parsing is limited to the existing matrix shape |
| `CI0002` | a link in the four-part completeness chain is absent | the chain was five links until 2026-09-19; the fifth asked for `--check-proofs-complete` to be passed in safe mode, which cvc5 rejected because the same change permits `--no-check-proofs-complete`. The `explicit-completeness` entity is retired, not renamed |
| `CI0003` | the proof tester passes `--proof-check=lazy` | a configuration fact, not a demonstrated incomplete proof |
| `CI0004` | a proof-testing matrix job excludes regression levels | the exclusion may be deliberate |
| `BUILD0001` | an unclassified safe/stable macro conditional, a behavioral `isSafeBuild()` reader, or an inferred safe-build source exclusion is found | unfamiliar benign blocks and nearby CMake text require review |
| `MODE0001` | an option declaring no proof support defaults on and has no direct safe-mode override | defaults-only reasoning misses coupled guards; `macrosQuantMode` is the known example |
| `RW0001` | an implemented handwritten rewrite is never handled by the seam | macros may reconstruct; report mode-gate evidence separately |
| `RW0002` | an implemented rewrite is handled only in unrestricted mode | a safe-mode gate may prevent that rewrite entirely |
| `TRUST0001` | a source file constructs a trust step with `TrustId::NONE` | an attribution gap; one observation per file, with every site as evidence |
| `INFER0002` | an emitted inference lacks a switch case in its theory's reconstructor, whose fallback constructs trust | call-site generators and reachability are not resolved; `INFER0001` remains reserved for the planned call-site check |
| `INFERID0001` | an inference id has multiple detected production sites | hygiene, not necessarily a defect |
| `INFERID0002` | a file produces a sentinel inference id | one observation per file and sentinel, with every site as evidence |
| `SIG0001` | a printable rule has no signature declaration after known printer renamings and exclusions | generated or specially reshaped signatures need review |
| `SIG0002` | a constructed skolem is refused by the seam | construction does not establish reachability in a particular mode |
| `SIG0003` | parseable documentation disagrees with detectable checker arity | both parsers are partial; this does not compare the printer's reshaped signature arity |

`RULE0003` remains an inventory of declared but unproduced rules in the existing
ledger. It is not emitted into the database. Standalone gates, fragment, TCB
and historical latent-census reports are opt-in developer measurements with
no bug identities; the default analyzer does not run those reports.
Dead trust/inference ids and theories without a reconstructor are recorded as
measurements: lack of that mechanism does not establish lack of a proof.

## The register

**Everything we are asking cvc5 to act on**: defects we believe exist, changes
we would like made, and process suggestions — one register, one id space.

Two registers, split by who acts. [`TODO.md`](../TODO.md) holds **work we do**;
this section holds **things cvc5 would act on** — `i-*` defects, `R*` asks,
`p-*` process. Everything else on this page is rationale. The rule: *if somebody
is expected to do something about it, it is in one of the two registers.* A
numbered section in a design argument — `H1`–`H11` in
[proof hygiene](#proof-hygiene) below — is a named argument, not a task; where
it implies an action it has a row here.

**These are hypotheses, not filed findings.** A finding is confirmed and lives
in [`experience.md`](experience.md#the-log); this is what is waiting for a
verdict.

Ranks: **1** an incomplete proof under `--safe-mode=safe` — a contract
violation, needs an input · **2** a hole reachable in safe mode, no input yet ·
**3** a gap in stable or unrestricted, or a cleanup · **—** a process point.

## Open — rank 2

The ones worth someone's attention.

| # | what | found by | what would settle it |
| --- | --- | --- | --- |
| **i-1** | **`LAMBDA_ELIM` may be a genuine safe-mode gap.** *(Strengthened: the fragment analysis finds **no `uf` kind blocked in safe mode at all** — `ufHoExp` gates the declared logic, not `Kind::LAMBDA`, so a lambda reaching the rewriter is not excluded by kind.)* The seam accepts it only when `safeMode == UNRESTRICTED`, `TheoryUfRewriter::rewriteViaRule` applies it, and its arm fires on `Kind::LAMBDA`, which no gate blocks in safe mode | `gates rule` | **still an input, and one attempt has failed.** `(define-fun f ((x Int)) Int (+ x 1))` with an assertion over `f` runs clean under `--safe-mode=safe --produce-proofs --check-proofs --stats-internal`: `unsat`, no unhandled rule, no trust step. That is evidence, not a settlement — the macro is expanded in preprocessing and `LAMBDA_ELIM` may simply not have fired. A benchmark that keeps a lambda alive to the rewriter is the open task. Note `--check-proofs-complete` cannot be passed here (see `i-3`); `--stats-internal` is the route |
| **i-2** | **`stringLazyPreproc` escapes safe mode's promise — and safe mode says so itself.** It declares `no_support = ["proofs"]`, `default = "true"`, `category = "regular"`; `setDefaultsPre` only *reads* it, never disables it. **Verified by running:** `--safe-mode=safe --strings-lazy-pp` is refused with *"cannot set option strings-lazy-pp in safe mode, as this option does not support proofs"* — so safe mode refuses to let you set the option on the grounds that it lacks proof support, while running with it on by default. `--no-strings-lazy-pp` is refused too, so the guard also blocks the one assignment that would make the configuration safer | `modes check`, then run | **verdict: carry.** Clears all five rules. Falsified if a maintainer says the `no_support` annotation is stale — which is itself the answer we want |
| **i-3** | **Proof completeness is obtained only as a side effect.** `--check-proofs-complete` appears nowhere in CI; in a safe build `setDefaultsPre` enables it from `--check-proofs`. **It also cannot be passed there** — the option is `category = "expert"` and safe and stable mode reject expert options — and *that is correct*: cvc5 established that making it settable would equally permit `--no-check-proofs-complete`, so the refusal is what keeps the guarantee non-negotiable. **The defect is not that the flag cannot be named**, which is where this row started; it is that adding a `--proof-granularity` flag to the `proof` tester would switch completeness off with no test failing | `ci proofs`, then run | an assertion in `setDefaultsPre` stating the implication (**R2**), which is a [kind D](experience.md#what-a-finding-is) and retires our check |
| **i-4** | **Completeness depends on a search budget, and the budget is load-bearing.** Reconstruction runs under `--proof-rewrite-rcons-rec-limit` (default 5); when it fails the step stays coarse. This is **not a tuning knob on a decidable procedure** — [FMCAD 2022 §IV-A](README.md#the-rare-correspondence) states there is *"no guarantee that preconditions are simpler than the current equality to be proved, and so no guarantee of termination in general."* The paper measured 92–95% of rewrite *steps* reconstructed but only **20–22% of proofs fully fine-grained**, since one coarse step spoils a proof | `rewrites gaps` | nothing settles this short of a termination argument for the recursion. It bounds what any kernel contract can claim, and it is the strongest reason [obligation 6](README.md#the-two-wishues) cannot be discharged today |
| **i-5** | **The safe-mode disable list is hand-maintained and untested.** Nothing checks that it still covers every feature without proof support | `modes delta` | not a defect today — the check exists to catch the *next* feature added |
| **i-15** | **The supported fragment is not expressible as a list of kinds.** Two expert options safe mode disables gate no term kind: `ufHoExp` restricts the declared *logic* (`logicInfo().isHigherOrder()`), `fpExp` restricts a *type* (via `checkForExperimentalFloatingPointType`, whose sort has kind `TYPE_CONSTANT` and cannot be excluded by kind). So any statement of the form "safe mode supports exactly these kinds" is incomplete, and `illegal_checker`'s kind deny list cannot be the whole story | `fragment check` | a decision on whether the fragment should be *stated* somewhere — the three mechanisms are each reasonable, but nothing writes down what they add up to |
| **i-17** | **The RARE↔C++ correspondence is established only by runtime search.** A RARE rule that misstates the rewrite never matches and is never reported; a rewrite with no rule, and a rule the search fails to find in budget, produce the same trust step and so cannot be told apart. Nothing checks the 439 declarations against the rewriter that implements them | design note | see [`rare-correspondence.md`](README.md#the-rare-correspondence). E1 (instantiate each rule, run the rewriter) is the direct test and belongs upstream |
| **i-18** | **`datatypes` and `quantifiers` have no RARE rules at all**, and both are enabled in safe mode. Every rewrite they perform must reconstruct through a hand-written `ProofRewriteRule` or become a trust step | `rewrites correspondence` | where reconstruction failure is structurally concentrated. Worth a corpus read before assuming it bites |
| **i-22** | **79 inferences fall through to a trust step by construction.** Their theory has an `InferProofCons` whose default case builds `ProofRule::TRUST`, and its switch does not name them: strings reconstructs 68 of the 86 ids it emits (78%), datatypes 11 of 26 (42%), sets 13 of 58 (22%) | `infer coverage` | each is a hole *by construction*, not by accident — the fall-through is what the code does when the switch misses. Severity still needs the gate: many are behind expert options |
| **i-6** | **Ten theories emit inferences with no `InferProofCons` at all** — quantifiers (74), arith (68), uf (20), bags (32), sep (13), arrays, bv, fp, ff, and the theory core (10) | `infer coverage` | **not** the same as having no proofs: several attach a `ProofGenerator` at the inference site instead, which the switch-based analysis cannot see. Settling it needs the call site, and that is the AST tier |

## Open — rank 3

Cleanups and unrestricted-mode gaps. Real, but nobody is relying on them.

| # | what | found by |
| --- | --- | --- |
| **i-23** | **The `safeMode == UNRESTRICTED` guard in `EoPrinter::isHandled` is inert.** Ten rules are accepted only in unrestricted builds — 8 `ARITH_TRANS_*` plus `SETS_FILTER_UP`/`SETS_FILTER_DOWN`. **None can be produced in safe or stable mode at all**, verified by running: the transcendental kinds are refused (*"Cannot handle assertion with term of kind cos"*), and `set.filter` needs a function-typed argument, so it needs the higher-order logic both modes refuse (*"Function terms are only supported with higher-order logic"*). So in every mode where the guard can return `false`, the rule is unreachable. Note the fix is **not** deleting the cases — that would flip unrestricted from handled to unhandled. It is either moving them to the always-handled list or documenting why the condition is moot | `ledger holes`, then run |
| i-7 | **14 `ProofRule`s the solver emits, the seam cannot print**: 4 `ARITH_POW2_*`, 9 `ARITH_TRANS_*`, `SAT_REFUTATION`. The arith ones are behind `--arith-exp`; the `ARITH_POW2_*` four are *also* registered trusted at pedantic level 1. `SAT_REFUTATION` is the one that is not arith and wants its own answer | `ledger holes` |
| i-8 | **51 `InferenceId`s are produced at more than one site**, 14 are produced nowhere, and 21 inferences are emitted with a sentinel id. Not defects; they are what makes an inference-coverage analysis imprecise | `inferid check` |
| i-9 | **8 trust steps are built with `TrustId::NONE`** — a declared hole with no stated reason, so nothing downstream can attribute them | `trust census` |
| i-10 | **3 `PREPROCESS_*` trust ids are dead**: both `bv_to_int` ids and `PREPROCESS_BITVECTOR_EAGER_ATOMS`. That pass's actual trust step is `INT_BLASTER`, built in a different file | `trust passes` |
| i-11 | **The pass↔trust-id correspondence is not derivable by name.** 7 ids do not follow their pass filename, including `PREPROCESS_BV_GUASS` — a misspelling of Gauss | `trust passes` |
| i-16 | **The RARE↔enum correspondence is exact but under-stated.** The generated marker names the rule, not its file, so a rule's owning theory is not recoverable from the header; hand-written entries are identified only by *absence* of a marker; RARE files carry six basenames and no extension; and the `ite-` prefix is claimed by both `booleans` and `builtin`. *The missing source file is now an accepted cost — the marker sits in a public header and the RARE layout is not ours to publish there (**R7b**, [withdrawn](#withdrawn)); we scan the two directories instead. The other three remain under-stated, and only identification-by-absence is worth an ask ([H11 C2](README.md#proof-hygiene)).* | `rewrites correspondence` |
| **i-21** | **`SUBS`'s documentation omits an argument the checker reads.** The doc says `\inferrule{F_1 \dots F_n \mid t, ids?}` — one required argument plus an optional `ids`. The checker asserts `1 <= args.size() && args.size() <= 3` and reads `args[2]` as a second `MethodId` (`ida`, defaulting to `SBA_SEQUENTIAL`), which selects how the substitution is *applied*. Nothing in the documentation mentions it | `signature checker` |
| i-19 | **24 `SkolemId`s are constructed by the solver and refused by the Eunoia seam.** A skolem the seam cannot print sinks a proof exactly as an unprintable rule does. Most are bags/sets/relations/transcendental — safe mode disables those — but `GROUND_TERM`, `BV_TO_INT_UF` and `SHARED_SELECTOR` want checking | `signature skolems` |
| i-20 | **The `\inferrule` documentation is prose, not a specification.** Comparing it against the *checker* took five rounds of parser fixes (10 → 3 → 2 → 3 → 1 disagreements) as LaTeX conventions were accounted for: dots inside a conjunction, `\,` thin spaces, bare ellipses between listed premises, and `DSL_REWRITE` alone separating its arguments with spaces rather than commas. The residue is one real finding (`i-21`). **The docs are readable by people and barely by machines**, which is why nothing checks them. cvc5 states a rule's arity in LaTeX only — unlike `SkolemId`, which states "Number of skolem indices: N" in a structured field and is checkable directly | `signature arity`, `signature checker` |
| i-12 | **11 `FF_*` rules** are in the public enum and documented, have no registered checker, and nothing produces them — `src/theory/ff` is entirely `#ifdef CVC5_USE_COCOA` | `ledger holes` |
| i-13 | **Proof closedness is never checked in a default run.** `ensureClosedWrtInternal` returns early unless `--proof-check=eager` or a trace is on, so the `pfgEnsureClosed` calls through the pipeline are inert in the configuration users get | — |
| i-14 | **`--proof-check=lazy` in CI's proof tester** means closedness is not checked there either | `ci proofs` |

## Open — asks

Changes we would like made. The reasoning for each is in the document named;
these rows exist so there is one place to see what is outstanding. Kinds are
from [`findings.md`](experience.md#what-a-finding-is): **B** an adoption, **C** a change to the
pipeline, **D** an assertion.

### Which ask moves which metric

The [analysis groups](../TODO.md#what-the-analysis-is-for) each carry numbers we
watch. If you are a cvc5 developer wondering where effort would show up, this is
the map. **R1 and R2 are the two we would ask for first** — R2 is a small
assertion, though no longer the one-line change we first called it, and R1 is
the one that makes everything else exact.

| ask | moves | from → to |
| --- | --- | --- |
| **R1** emit the registries as JSON | *all of G1–G4* | inferred → exact. Retires most of our fragility and several asks below |
| **R2** assert the completeness implication in `setDefaultsPre`, at the granularities where it holds | G4 completeness chain | the guarantee obtainable only as a side effect → stated in cvc5's own tree |
| **R3** extract helpers out of solver classes | G2 checker TCB | 41,446 lines → smaller, and 1 of 13 checkers over-scoped → 0 |
| **R4** one `InferenceId`, one site | G3 nameability | 84% single-site → 100% |
| **R5** `no_support` covers defaults | G4 contract | 1 option escaping → 0 |
| **R6** declare intentional seam refusals | G1 hole census | 14 gaps *inferred* → 14 gaps *stated* |
| **R7** derivable pass↔trust-id names | G3 nameability | correspondence checkable only by construction site → by name |
| **R8** safe mode prunes at build time | G4 contract | features disabled at runtime → absent from the binary |
| **R9** test each RARE rule against the rewriter | G5 determinacy | a rule that misstates the rewrite fails silently → is caught |
| **R10** rule on the hygiene standard | G3 nameability | eleven proposals open → decided, either way |
| **R11** run our ratchets in CI | all groups | measured when we remember → measured on every push |
| **R12** one corpus run with `--stats-internal` | *decides G1's worth* | holes counted → holes counted **and** the fraction any input has reached |

| # | ask | kind | why | where argued |
| --- | --- | --- | --- | --- |
| **R1** | **emit cvc5's proof registries as JSON** from a build target | C | the highest-leverage ask by a distance: makes our whole table tier exact instead of parsed, and retires most of the fragility below. Three parser bugs in one session are the argument | [coupling](README.md#r1--emit-the-tables-cvc5-already-has) |
| **R2** | **make the completeness guarantee statable** — assert in `setDefaultsPre` that a safe build with `--check-proofs` at default or DSL-rewrite granularity has `checkProofsComplete` on | D | *(corrected twice. By running it: the flag is `category = "expert"`, so safe **and** stable mode refuse it — it cannot be named in either job whose mode carries the contract. Then by cvc5, who **rejected the second form of this ask**: dropping the expert category also permits `--no-check-proofs-complete`, and `setDefaultsPre` honours an explicit user assignment, so the promotion would make the guarantee opt-out-able. Built at `a960d7d7210e731cf48ad7baa6ad42fc7345b297`, reverted at `215eed21a6c8380075c46513e69181a295b6e3b2`. The expert refusal is the mechanism, not the obstacle; only the assertion form survives, and it must allow for the deliberate lower-granularity exception.)* (`i-3`, [retracted](experience.md#retractions)) | [coupling](README.md#r2--make-the-completeness-guarantee-statable) |
| **R3** | extract the pure `static` helpers out of solver classes | C | six rule checkers compile against the solvers they check. Filed as `f-1` | [coupling](README.md#r3--get-the-theory-solvers-out-of-the-proof-checkers-includes) |
| **R4** | one `InferenceId`, one production site | C | until an id names one program point, inference coverage cannot be precise (`i-8`) | [coupling](README.md#r4--one-inferenceid-one-place) |
| **R5** | make `no_support` cover defaults, or derive safe mode's list from it | C | the `SolverEngine` guard fires on assignment only, which is how `stringLazyPreproc` gets through (`i-2`) | [coupling](README.md#the-asks-argued) |
| **R6** | declare which seam refusals are *by design* | C | we infer "macro or trust step, so intended" from naming and elaboration — a heuristic that already needed one correction | [coupling](README.md#r6--declare-what-the-seam-is-supposed-to-reject) |
| **R7** | make the pass↔`TrustId` correspondence derivable, and fix `BV_GUASS` | C | `i-11` | [coupling](README.md#r7--make-the-passtrustid-correspondence-derivable) |
| **R8** | make safe mode prune code at build time | C | `CVC5_SAFE_MODE` prunes almost nothing today; each feature moved from runtime-disabled to not-compiled turns a class of hole into a link error | [coupling](README.md#r8--safe-mode-as-a-build-time-property) |
| **R9** | **test each RARE rule against the rewriter** — instantiate the match, rewrite, compare to the target | C | the only thing that catches a rule that *misstates* the rewrite, which today fails silently forever (`i-17`). Belongs upstream, beside the rewriter. Partial is fine | [rare-correspondence E1](README.md#the-rare-correspondence) |
| **R10** | adopt the proof hygiene standard, or rule on it | B | eleven rules, most ratifying existing practice; the contested ones are `H1`, `H5`, `H6` | [hygiene](README.md#proof-hygiene) |
| **R11** | run our checks in cvc5 CI, and upload SARIF | B | `p-1`; the ledger and mode ratchets run in seconds and need no baseline | [tooling](maintenance.md#d1--three-artifacts-by-what-each-question-needs) |
| **R12** | **run the corpus with `--stats-internal` and publish the `finalProof::*` counters** — *[we did this for `regress0`](maintenance.md#what-the-corpus-reaches): safe mode reaches **0** holes over 1,061 proofs, unrestricted reaches one benchmark in ten, and 10 of 70 live `TrustId`s are touched. The ask is now for the levels and corpora we cannot run* | B | the cheapest experiment either side can run, and the one that decides how much the rest of this is worth. cvc5's counters are a numerator — holes some input reached; our census is the denominator — holes that exist to be reached. Nobody currently knows the ratio, and it cuts both ways: if the corpus has touched most of them the static surface has little headroom and we should narrow accordingly | [why](README.md#1-we-supply-the-denominator-your-own-counters-lack) |

### Withdrawn

An ask we decided not to make. Kept with its id so the id is not reused and the
reasoning stays visible.

| # | what we were going to ask for | why we withdrew it |
| --- | --- | --- |
| **R7b** | put the RARE source file in the generated marker — `/** Auto-generated from RARE rule bool-double-not-elim (theory/booleans/rewrites) */` | **wrong surface.** The 439 markers live in `include/cvc5/cvc5_proof_rule.h`, a *public* header whose comments are published as the `ProofRewriteRule` API documentation. The RARE file layout is an internal build detail — six extensionless basenames under two directories — and this ask would have published it there. The rule *name* in the marker is already user-visible vocabulary (`--proof-granularity=dsl-rewrite` prints it); its source path is not, and nothing user-facing should have to know it. The missing source file stays a cost we absorb (`i-16`), not a request we make |

## Process

| # | what |
| --- | --- |
| p-1 | cvc5's nightly enforces only via `-warnings-as-errors`: no SARIF upload, so findings never reach code scanning, PR annotations, or a baseline |
| p-2 | `TODO (wishue #154)`: Minisat with DRAT/LRAT throws no logic exception. Known upstream — track, do not re-file |

## Settled

Kept visible. A hypothesis that dies is a good outcome, and the reasoning is
worth as much as a finding.

| # | what we suspected | what settled it |
| --- | --- | --- |
| s-1 | `ARITH_POW_ELIM` and `ARRAYS_SELECT_CONST` might be safe-mode seam gaps | **blocked.** `POW` needs `--arith-exp`; `ARRAYS_SELECT_CONST`'s arm conjoins `SELECT` with `STORE_ALL`, which needs `--arrays-exp` |
| s-2 | `ARRAYS_EQ_RANGE_EXPAND` and `DT_MATCH_ELIM` — two hard rewrite gaps | **blocked.** `EQ_RANGE` needs `--arrays-exp`, `MATCH` needs `--datatypes-exp` |
| s-3 | "`EoPrinter::isHandled` refuses 37 rules" (172 − 135) | **superseded.** The subtraction was naive. The ledger computes it: 40 refused, of which 14 by design, 12 unreachable, 14 real gaps |
| s-4 | `macrosQuantMode` escapes safe mode like `stringLazyPreproc` | **spurious.** Its effect is gated by `macrosQuant`, default `false`. A defaults-only check cannot see that gate |
| s-6 | `SET_FILTER` is ungated in safe mode, and `SETS_FILTER_UP`/`DOWN` are refused by the seam there — so a `set.filter` benchmark should fail `--check-proofs-complete`. A rank-1 candidate | **spurious, and the most instructive miss so far.** Every link held in the source. But `set.filter` takes a predicate, a predicate is a function-typed term, and `TheoryUF::preRegisterTerm` throws `LogicException` on a function-typed term unless the logic is higher-order — which safe *and* stable mode refuse. One command settled what no amount of reading would have. The analysis is fixed rather than the row retracted: `Fragment.requires_higher_order` now recovers this axis from the type rules, and 13 kinds move to blocked. See [the bar](experience.md#the-bar) |
| s-7 | "No `uf` kind is blocked in safe mode at all", used to strengthen `i-1` | **half wrong.** `HO_APPLY` is blocked, by the same logic axis as `s-6`. `LAMBDA` is *not* — its argument is not function-typed, only its result is — so `i-1` survives at the kind level, but the sweeping form of the claim does not. `tests/test_fragment.py` now asserts the corrected fact |
| s-5 | The proof checker's TCB is 74% of `src/` | **retracted.** An artifact of a saturating closure mode; the real figure is 8.0%. See [retractions](experience.md#retractions) |

## Filed

| # | what | where |
| --- | --- | --- |
| f-1 | Six proof rule checkers compile against the theory solvers they check, to reach `static` helpers parked on solver classes | [`tcb-001`](experience.md#tcb-001--proof-rule-checkers-compile-against-the-theory-solvers-they-check) |

## Proof hygiene

A proposed standard for cvc5's proof system — naming, calling conventions,
checker registration, and the discipline around inference ids. **It is the
precondition for every later goal here**, for a reason worth stating plainly:
*you cannot draw a boundary around a thing you cannot name.* If an
`InferenceId` is emitted at eight places then "the inferences theory X can make"
is not an enumerable set, and nothing quantified over it means anything.

`InferenceId` is cvc5's existing *informal* proof annotation: not a proof and it
does not claim to be, but the closest thing cvc5 has to a complete index of what
inferences exist, and the natural spine for this analysis. That only works if an
id means one thing.

Eleven rules, each measured against `40a4bb7e4`. Four ratify existing practice
and should be uncontroversial; three cost something and are the ones to argue.

| | rule | status | what it costs |
| --- | --- | --- | --- |
| **H1** | **One id, one place** — an `InferenceId` names one program point | **contested** | 76 exceptions today (`i-8`, `R4`) |
| **H2** | **No anonymous inferences** — no sentinel id on an emitted inference | ratifies practice | 21 sites |
| **H3** | **The prefix names the owner** — `STRINGS_*` is emitted by strings | ratifies practice | near-universal already |
| **H4** | **One vocabulary per theory** — a theory's ids are declared together | ratifies practice | — |
| **H5** | **Every id has one reconstruction home** | **contested** | needs a rule cvc5 has not written |
| **H6** | **"No proof" must be said out loud** — a trust step names a `TrustId` | **contested** | an API change; 8 sites use `TrustId::NONE` (`i-9`) |
| **H7** | **Trusted is declared, never discovered** — `registerTrustedChecker` with a pedantic level | ratifies practice | — |
| **H8** | **Registration is total, and cvc5 says so itself** | ratifies practice | 13 unregistered, 11 of them `FF_*` (`i-12`) |
| **H9** | **The rule documentation is a contract**, not prose | worth asking | `i-20`, `i-21` |
| **H10** | **The checker's dependencies are the thing to minimise** | **measure now** | needs nobody's agreement; the number is the argument (`R3`) |
| **H11** | **The RARE correspondence is stated, not inferred** | worth asking | `i-16`, `i-17` |

**The natural home for a settled version is upstream.** cvc5's proof
documentation is 161 lines across five files and there is **no contributor guide
for adding a proof rule or an inference id**; this would be that missing guide,
which makes it a kind B/C ask rather than a check of ours. A convention written
down is enforced by reviewers on every pull request, for free, forever; a
convention enforced only by our checker is enforced nightly, by us, at a cost.
So: measure H10 now, propose the four uncontroversial rules, argue the three
that cost something with the measurements attached, and **write checks only for
what is accepted** — a check enforcing a convention its owners have not agreed
to is noise, and it will be turned off.

### The RARE correspondence

`i-17` and `R9` rest on one argument worth keeping. A RARE rule and the C++ that
performs the same rewrite are **two statements of one fact, and nothing relates
them**. The correspondence is established only by runtime search: a RARE rule
that misstates the rewrite never matches and is never reported, and a rewrite
with no rule, a rule the search fails to find in budget, and a rule that is
simply wrong all produce the same trust step. Nothing checks the 439
declarations against the rewriter that implements them.

The direct test is `R9` — instantiate each rule's match, run the rewriter,
compare to the target — and it belongs upstream beside the rewriter, where a
failure is one rule rather than a corpus statistic. Partial coverage is fine;
the point is that a misstatement stops being silent.

## The two wishues

A **wishue** is a goal you would take if the work went unusually well and are
not committing to — a wish written down as an issue. The word is cvc5's own: it
keeps a `cvc5-wishues` tracker and its source carries seventeen
`TODO (wishue #N)` comments. Both wishues below are *progressive*: they improve
by degrees, every degree is worth having, and neither has a finish line.
**Neither is a claim about verification tools.**

### A kernel you can argue about

The arc is to stop reporting holes and start being able to say which part of
cvc5 is its proof kernel — not a machine-checked theorem, but

> **an argument, made to a person, that this set of code is what has to be right.**

| axis | the question | today |
| --- | --- | --- |
| **nameable** | can you enumerate the kernel at all? | partly — `--safe-mode=safe` names a configuration, not a set of code |
| **closed** | does the boundary hold — does nothing inside reach out? | unknown, and `tcb-001` is one place it does not |
| **small** | how much is inside? | the internal checker compiles against 41,446 lines, 8.0% of `src/` |
| **local** | can a reader check one obligation by reading one function? | rarely |
| **mechanized** | is any part machine-checked? | no, and that is the *last* axis, not the first |

Progress on any row is real progress, and the measure that matters is **how long
the argument is and how much of it a reader can check** — not whether a tool
printed `QED`. The TCB number going down *is* the argument getting shorter, and
it needs no verification tool, no build and nobody's agreement to start.
`i-4` is the strongest reason this cannot be discharged today: reconstruction
runs under a search budget with no termination argument.

### A safe build that cannot be unsafe

Safe mode's promise is kept **at runtime**, by `setDefaultsPre` turning things
off by name and by `NoOpTheoryRewriter` throwing when a disabled theory is
reached anyway. The unsafe code is still compiled, still linked, one missed
guard away. There is a build-time safe mode — `cvc5_option(ENABLE_SAFE_MODE)`
sets `-DCVC5_SAFE_MODE` — but it prunes almost nothing of cvc5's own code: five
files in `src/` mention it, two only to reword an error message. What it
genuinely excludes is third-party, LibPoly and CoCoA.

> **Make the safe build not contain the unsafe code.**

Each feature moved from *disabled at runtime* to *not compiled* converts a class
of proof hole into a **link error** — the cheapest possible latency. And there
is a consistency check available right now, with no build: the runtime disable
list and the build-time exclusion list must agree, and today they plainly do not
(`R8`).

## The asks, argued

Ordered by leverage, not by effort. The register above carries the one-line
version of each; this is the reasoning.

> **This repository imposes no constraints on refactoring cvc5.** dokimasia is
> downstream. If cvc5 changes and a tool here breaks, that is our bug to fix —
> exactly like a false positive. Nothing below is a request that cvc5 keep a
> name, a file or a switch. The point of writing it down is that when a tool
> does break, we already know why.

Ordered by leverage, not by effort.

### R1 — emit the tables cvc5 already has

**The single highest-leverage change.** A build target that dumps the proof
registries as JSON: `ProofRule` with its checker and pedantic level, `TrustId`,
`InferenceId`, `ProofRewriteRule` with its RARE origin, and what the Eunoia
seam accepts.

Today we recover all of that by parsing C++ — enum blocks, `switch` bodies,
`registerChecker` calls. That works, and it is exactly as brittle as it sounds:
**three parser bugs in one afternoon of building these tools**, two of which
produced confidently wrong numbers before a cross-check caught them. A dumped
table would make the whole tier-0 analysis exact instead of inferred.

It is also useful to cvc5 independently of us: the same JSON documents the
calculus, feeds the signature, and lets cvc5 assert its own invariants at build
time. R1 makes several of the asks below unnecessary rather than merely easier.

### R2 — make the completeness guarantee statable

`--check-proofs-complete` appears nowhere in `.github/` or `test/`. In a safe
build, `setDefaultsPre` enables it as a side effect of `--check-proofs`, so
completeness is tested through a chain nothing asserts. See [`CI0002`](README.md#the-register).

**Corrected, by running it.** This ask first read *"pass the flag explicitly in
the proof tester; it costs one line."* That is impossible, and one command shows
why:

```
$ cvc5 --safe-mode=safe --produce-proofs --check-proofs --check-proofs-complete f.smt2
(error "Fatal error in option parsing: expert option check-proofs-complete
        cannot be set in safe mode.")
```

`checkProofsComplete` is `category = "expert"` in `proof_options.toml`, and safe
and stable mode reject expert options. So the flag **cannot be named in either
of the two jobs whose mode carries the contract** — it can only be passed in the
unrestricted job, where the guarantee is not the one being promised. The
implication is not merely unasserted; it is currently *the only way the
guarantee can be obtained where it matters.*

That made the ask sharper, and we then asked for the wrong thing.

**Withdrawn 2026-09-19: do not ask for the expert category to be dropped.** This
section proposed two forms, the first being *exempt `checkProofsComplete` from
the expert refusal, so the safe-mode tester can name what it is testing.* cvc5
rejected it, having built it and reverted it:

> Making this Boolean option available also permits `--no-check-proofs-complete`
> and `(set-option :check-proofs-complete false)`. Those assignments let a user
> disable completeness checking in safe mode.

An option's category governs **both** assignments, and `setDefaultsPre` respects
an explicit user assignment through `checkProofsCompleteWasSetByUser`. So the
promotion turns a guarantee safe mode switches on into one a user can switch
off. **The expert refusal is what makes completeness non-negotiable in the mode
that promises it** — the very property this ask exists to protect. Reproduced at
cvc5 `a960d7d7210e731cf48ad7baa6ad42fc7345b297`, reverted at `215eed21a6c8380075c46513e69181a295b6e3b2`. The error was ours: we reasoned
from *the positive flag is refused* to *the option should be settable*, without
asking what else becomes settable, and it is recorded in
[the retractions](experience.md#retractions).

**The one surviving form: assert the implication where it is created** — in
`setDefaultsPre`, where a safe build turns the option on, state that a safe build
with `--check-proofs` has `checkProofsComplete` set. That is the
[kind D](experience.md#what-a-finding-is) form: the invariant moves into cvc5's tree and our
`CI0002` check retires. cvc5 adds the condition we had missed — **an
unconditional assertion would also have to account for the intentional
lower-granularity exception**, since the implication holds only at the default
and DSL-rewrite granularities.

### R3 — get the theory solvers out of the proof checker's includes

Six rule checkers `#include` the headers of the solvers they check, to reach
`static` helpers parked on solver classes. Extracting those helpers into
dependency-light headers shrinks the checker's compile-time surface and breaks
the coupling. Written up as [`tcb-001`](experience.md#tcb-001--proof-rule-checkers-compile-against-the-theory-solvers-they-check).

### R4 — one InferenceId, one place

51 ids are produced at more than one site, 14 are produced nowhere, and 21
inferences are emitted with a sentinel id. Until an id names one program point,
"the inferences theory X can make" is not an enumerable set, and the `INFER`
coverage analysis cannot be precise. [`docs/README.md`](README.md#proof-hygiene).

### R5 — make `no_support` cover defaults

Option definitions carry a machine-readable `no_support = ["proofs"]`, and
`SolverEngine` throws if a user *sets* such an option in safe mode. It never
fires for an option already on by default, which is how `stringLazyPreproc`
reaches a safe-mode run. Either the guard should consider defaults, or safe
mode's disable list should be derived from the annotation rather than
maintained beside it.

### R6 — declare what the seam is *supposed* to reject

`EoPrinter::isHandled` refuses 40 rules; 14 are refused **by design** (macros
that get elaborated away, trust steps, other formats' rules). We infer that
distinction from the rule's name and whether the post-processor expands it,
which is a heuristic that already needed one correction (`SUBS` is not named
`MACRO_*` but is elaborated). If cvc5 stated the intent, the analysis would
report gaps instead of guessing which refusals are gaps.

### R7 — make the pass↔TrustId correspondence derivable

Seven `PREPROCESS_*` ids are not derivable from their pass filename, including
`PREPROCESS_BV_GUASS` — a misspelling of Gauss. We work around it by matching
construction sites, which is more robust anyway, but a naming rule would make
the correspondence checkable directly and would catch a pass added without a
declared hole.

### R7b — put the RARE source file in the generated marker — **withdrawn**

*Kept for the reasoning. The ask is [withdrawn](README.md#withdrawn) and should
not be carried.*

The argument was: `mkrewrites.py` already emits
`/** Auto-generated from RARE rule <name> */` and the correspondence it creates
is exact, so adding the file — `(theory/booleans/rewrites)` — would make a rule's
owning theory recoverable from the header instead of by scanning two
directories.

**What it missed.** Those 439 markers are emitted into
`include/cvc5/cvc5_proof_rule.h` — a *public* header, and `ProofRewriteRule` is
published in [the C++ API documentation](https://cvc5.github.io/docs/latest/api/cpp/cpp.html).
So the one-line change to `mkrewrites.py:380` would not have added an internal
annotation; it would have put cvc5's internal RARE file layout into cvc5's API
doc, where no consumer of the API has any business needing it. The rule *name*
is already user-visible — `--proof-granularity=dsl-rewrite` prints RARE rule
names into proofs — but the path it was parsed from is not, and should not
become so to save us a directory scan.

This is the general shape worth remembering: **an ask that is cheap in the
generator can still be expensive in the published surface**, and the cost lands
on cvc5's users rather than on the maintainer who would apply it. Our
convenience is not a reason to widen an API. See
[H11](README.md#proof-hygiene), whose C1
is withdrawn with this row.

### R7c — state a rule's arity in a structured field

`SkolemId` documents "Number of skolem indices: ``N``" and is checkable
mechanically; `ProofRule` states arity only inside LaTeX prose, and comparing it
to the checker took five rounds of parser work to get from 10 apparent
disagreements down to the one real one. The same structured field on proof rules
would make `RULE0010` a two-line check instead of a research project.

### R8 — safe mode as a build-time property

`ENABLE_SAFE_MODE` exists and prunes almost nothing of cvc5's own code: five
files in `src/` mention `CVC5_SAFE_MODE`, two only to reword an error message.
Moving features from "disabled at runtime" to "not compiled" turns a class of
proof hole into a link error. [`docs/README.md`](README.md#a-safe-build-that-cannot-be-unsafe).

## What we parse, and what would break us

Kept short on purpose. The mitigation is not an abstraction layer — it is that
**every tool has tests asserting facts we verified by hand against a pinned
checkout**, so a break shows up as a named test failure rather than a quietly
wrong number. That is the whole robustness budget, and it is enough.

| we read | tool | what breaks us |
| --- | --- | --- |
| `EVALUE(...)` enum blocks in `cvc5_proof_rule.h`, `cvc5_skolem_id.h` | ledger, rewrites | changing the macro, or splitting the enums across files |
| `enum class` bodies in `inference_id.h`, `trust_id.h` | inferid, trust | moving the enum, or generating it |
| `EoPrinter::isHandled`, `isHandledTheoryRewrite` switches | ledger, rewrites | renaming them, or replacing the switch with a table (**which would be an improvement** — see R1) |
| `registerChecker` / `registerTrustedChecker` call sites | ledger | registering in a loop over a list instead of call-by-call |
| `rewriteViaRule` switch bodies | rewrites | same |
| `SET_AND_NOTIFY*` macros in `set_defaults.cpp` | modes | renaming the macros, or moving the logic out of one file |
| `*.toml` option definitions | modes | switching option format |
| `.github/workflows/*.yml` matrix entries | ci | restructuring the matrix, or moving tester selection into a script |
| `run_regression.py` tester classes | ci | building tester args somewhere other than the class body |
| `preprocessing/passes/*` filenames | trust | reorganising the directory |
| RARE files, found by content | rewrites | nothing much — content discovery is why. **Renaming them freely is already safe**, which was not true of our first version |
| `Auto-generated from RARE rule` markers in `cvc5_proof_rule.h` | rewrites | changing the marker text in `mkrewrites.py` |
| `d_illegalKinds.insert` blocks in `illegal_checker.cpp`, and theory `LogicException` guards | gates | moving the gate out of a table into scattered checks (**the reverse would help us** — one table would be better) |
| `#include` graph under `src/` | tcb | nothing much; it is the most robust thing here |

### Known limits, not breakages

Worth separating from the above, because these are things the tools *cannot*
do rather than things that might stop working:

- **Option gates are computed for rewrite rules only.** `dokimasia.gates` links
  a rule to the term kinds its `rewriteViaRule` arm names, and those kinds to
  the options that legalise them. It says nothing about `ProofRule`s or trust
  steps, whose sites name no kind — those severities are still set by hand.
- **Conjunction and disjunction are not distinguished.** An arm naming several
  kinds may require all of them or accept any; the tool reports `partial` and
  asks a human to read it.
- **Generated headers are invisible.** `options/options.h` is built from the
  `.toml` files, so the TCB closure does not follow edges through it.
- **`rewriteViaRule` is one route.** A rewrite applied another way will look
  unimplemented to the `rewrites` tool.

## Parser bugs found while building these tools

Recorded because they are the argument for R1, and because two of them produced
wrong output that a cross-check caught rather than a test.

| bug | effect | caught by |
| --- | --- | --- |
| `//.*` under `re.DOTALL` | any switch arm whose body opened with a line comment was read as a fallthrough and its labels silently lost | a rule appearing in the seam that the tool called unhandled |
| next-label bound used `m.end()` instead of `m.start()` | fallthrough groups mis-grouped | the same investigation |
| anchoring on `bool EoPrinter::isHandled` | matched the call site, then `isHandledTheoryRewrite` is a prefix-match hazard for the other tool | zero results where 53 were expected |
| fixed-size window past a class declaration | `BaseTester` inherited `UnsatCoreTester`'s flags; the last tester swallowed the module's argparse | reading the output against the source |
| `exec`-mode include closure | saturated at cvc5's whole link unit, giving 74% for any seed | seeding from an unrelated file |
