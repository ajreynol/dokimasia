# The plan

The goal is [**complete proofs, always**](docs/goals.md).

**This file holds work *we* do.** Anything we are asking cvc5 to act on lives in
[`docs/issues.md`](docs/issues.md), the other half of the register. Numbered
sections in the `docs/` design notes are named arguments, not tasks.

## What exists

Nine subtools, all dependency-free, all reading a checkout with no build, all
with a `baseline --check` ratchet. What each answers is in its group below.

| tool | answers |
| --- | --- |
| `tcb` | the proof checker's dependency closure, and what each edge costs |
| `ledger` | one row per `ProofRule`: produced, checked, elaborated, printed |
| `trust` | every `TrustId` construction site, and the preprocessing correspondence |
| `inferid` | whether each `InferenceId` names one program point |
| `rewrites` | the 533-rule rewrite vocabulary, RARE vs hand-written vs applied |
| `modes` | what safe and stable mode change about the defaults |
| `gates` | which option legalises each term kind, and so each rewrite rule |
| `fragment` | the supported fragment per theory, and whether it is enforced |
| `signature` | whether the Eunoia signature agrees with cvc5's account of a rule |
| `infer` | whether every inference a theory makes has a proof reconstruction |
| `ci` | whether cvc5's proof testing is still attached |

## What the analysis is for

Every tool here exists to move one number. Not to enumerate — **to measure a
gap between what cvc5 promises and what it enforces, and to watch that gap
close.** A check that produces a list nobody can act on, or a number nobody
would notice moving, does not belong.

Five groups. Each asks one question, carries its own metrics, and has a short
list of things cvc5 could do that would move them.

---

## G1 — How many ways can a proof be incomplete?

*The direct measure. Everything else is instrumental to this one.*

| metric | today | target |
| --- | --- | --- |
| `ProofRule`s the solver emits that the Eunoia seam refuses | **14** — 13 behind `--arith-exp`, plus `SAT_REFUTATION` | 0 reachable in safe mode |
| rewrites applied but unprintable | **40** — 38 macro, 2 hard, all blocked in safe mode | 0 reachable in safe mode |
| rewrites the seam takes **only** outside safe mode | **3** — one (`LAMBDA_ELIM`) not otherwise blocked | 0 |
| `TrustId`s constructible | **70 of 75 live** | ranked by safe-mode reachability |
| theories with no RARE rules, enabled in safe mode | **2** — `datatypes`, `quantifiers` | — |

**Ours:** `ledger`, `rewrites`, `trust` ✅ · rank the trust census by reachability
(needs G-gates below) · cross the static inventory against a corpus run so
*latent* holes — the ones no input has ever reached — can be named.

**What cvc5 can do:** close the holes (`i-7`, `i-18`); declare which seam
refusals are intentional (**R1**, **R6**) so we report gaps instead of inferring
which refusals are gaps.

### Work

**The rule ledger and the Eunoia seam** — `dokimasia.ledger` ✅

One row per `ProofRule`, four columns: **produced by**, **checked by**,
**elaborated by**, **printed by**. A hole in any column is a claim.

- [x] **M2.1** ✅ **`dokimasia.ledger`** — the ledger, built and ratcheted.
      170 `ProofRule`s: 113 always printable, 17 conditionally, 40 never — of
      which 14 by design, 12 unreachable and **14 real gaps**. Also answers
      `RULE0001` (11, all `FF_*`), `RULE0002` (16 trusted checkers: 8 at level
      1, 2 at level 2, 6 at level 4) and `RULE0003` (14 declared and never
      produced). Tests in `tests/test_ledger.py`.
      *Still open:* a safe-mode column — deciding reachability per rule needs
      the option gate, which the tool does not compute (see c-13).
- [ ] `RULE0001` a rule with no registered checker.
- [ ] `RULE0002` a rule registered via `registerTrustedChecker` — surface the
      declared pedantic level (1–4), cvc5's own statement of how much its
      checker really checks.
- [ ] `RULE0003` a rule declared in the public enum that nothing produces.
- [ ] `RULE0004` a rule produced under a build flag whose checker is not
      registered under the same flag.
- [ ] `RULE0010` **documentation drift** — the `\inferrule{premises | args}`
      spec in `cvc5_proof_rule.h` against the arity the checker reads and the
      shape `eo_printer.cpp` prints. *This is cvc5's `cvc5-6` request to anoieu;
      it is a C++ question and belongs here.*
- [ ] `SEAM0001` a rule `EoPrinter::isHandled` can never accept. Three-valued
      output: always handled, never handled, **handled depending on arguments** —
      the conditional arms (`isHandledTheoryRewrite`, `isHandledBitblastStep`)
      make handledness a property of a rule *plus its arguments*.
- [ ] `SEAM0002` for the argument-dependent arms, characterise the unhandled
      argument set and ask whether any producer can construct one.
- [ ] `SEAM0003` `EoNodeConverter::isHandledSkolemId` as the same coverage
      problem over `SkolemId`.
- [ ] `SEAM0004` a `ProofRewriteRule` with no Eunoia landing. Cross-repo: the
      C++ half is ours, the signature half is anoieu's — define the handoff
      before writing this one.

**The trust census and preprocessing** — `dokimasia.trust` ✅

75 `TrustId` values name the ways cvc5 admits a step without proving it. Being
named is the point; the census nobody has is **which are reachable in safe
mode**.

- [x] **M3.1** ✅ **`dokimasia.trust`** — the census. 75 declared `TrustId`s:
      **70 live, 4 dead, 8 sites built with `TrustId::NONE`**. Ranked by
      subsystem (`preprocessing/passes` leads with 30 ids over 41 sites).
      Answers `TRUST0002`, `TRUST0003`, `PP0001` and `PP0002`. Tests in
      `tests/test_trust.py`.
      *Still open:* `TRUST0001` — which are reachable in safe mode — needs the
      same option-gate machinery the ledger wants (c-13).
- [ ] `TRUST0001` a `TrustId` reachable under `--safe-mode=safe`. Rank 2 on its
      own; rank 1 the moment an input reaches it.
- [ ] `TRUST0002` a `TrustId` with no construction site — dead, and a cleanup.
- [ ] `TRUST0003` a trust step introduced with `TrustId::NONE` — an unnamed hole.
- [ ] `TRUST0004` theory-lemma census by `TheoryId`; cross-check against cvc5's
      own `d_trustTheoryLemmaCount` statistic, which is how this check gets
      validated cheaply.
- [ ] `PP0001` a `PreprocessingPass` that neither produces a proof nor declares
      a `PREPROCESS_*` trust id. The enum carries a `PREPROCESS_*` family that
      roughly tracks the pass list (32 mentions against 37 pass headers), so a
      first approximation is table-tier; the passes with no entry either prove
      their work or are the finding.
- [ ] `PP0002` a pass whose `PREPROCESS_*` id exists but is never used.
- [ ] **M3.2** Diff mode: sites added or removed between two cvc5 revisions.
      This is the shape CI wants.

**Rewriting and macro elaboration** — `dokimasia.rewrites` ✅

- [ ] `ELAB0001` a `ProofRule::MACRO_*` with no expansion case in
      `proof_post_processor.cpp` — 9 macro rules, 16 references, so the mapping
      is not one-to-one and needs reading rather than counting.
- [ ] `ELAB0002` an expansion that can emit another macro with no termination
      argument.
- [ ] `ELAB0003` per granularity mode, which rules survive to the final proof —
      the honest answer to what `--proof-granularity` buys.
- [x] **M5.1** ✅ **`dokimasia.rewrites`** — 533 rules: 321 RARE, 212
      hand-written, 93 applicable via `rewriteViaRule`, 53 accepted by the seam.
      **40 gaps** (38 macro, 2 hard) plus **3 safe-mode gaps**. Tests in
      `tests/test_rewrites.py`.
- [x] `RW0001` ✅ a `ProofRewriteRule` with no RARE rule and no reconstruction:
      119 declared, not RARE, and implemented by no rewriter.
- [ ] `RW0002` **budget-dependent completeness.** `proof_post_processor_dsl.cpp`
      reconstructs under `--proof-rewrite-rcons-rec-limit` (default 5) and
      `-step-limit`; on failure the macro step *remains*. Report every rewrite
      whose reconstruction depends on the budget. The deepest obstacle to M7 and
      worth characterising early even though it cannot be fixed here.
- [ ] `RW0003` a theory rewriter path returning a rewritten node with no
      `ProofRewriteRule` tag reachable for it.

**The latent inventory** — the holes no input has reached. *The one thing here
nobody else can do.*

**The corpus cannot prove *always*.** It shows what benchmarks reach; the risk is
what they do not, and on safe mode that is now essentially all of the remaining
risk. This is the one thing here nobody else can do:

> **static hole inventory − what any input has hit = the latent holes.**

- [ ] **B.1** The static inventory, from [M1–M5](#g1--how-many-ways-can-a-proof-be-incomplete).
- [ ] **B.2** Subtract stage D and E results. Publish the difference — the
      **latent count** is one of the project's two headline numbers.
- [ ] **B.3** Per latent hole: construct an input that reaches it (promoting it
      to a real finding), or argue it is unreachable (shrinking the problem).
- [ ] **B.4** A latent hole that resists both is the most interesting object in
      the project — it is exactly what neither testing nor analysis settles.

**The corpus baseline** — once, not per change.

Worth doing **once**, for the baseline and to confirm the "almost no holes"
claim quantitatively. Not a recurring cost.

cvc5 already computes it: `finalProof::ruleUnhandledEoCount`,
`theoryRewriteRuleUnhandledEoCount`, `trustCount`, `trustTheoryLemmaCount`,
`minPedanticLevel` — all under `--stats-internal`.

- [ ] **E.1** Corpus run under `--safe-mode=safe --produce-proofs
      --stats-internal`. **Use `--stats-internal`, not
      `--check-proofs-complete`**: the latter aborts on the first hole, which is
      right for CI and wrong for a census.
- [ ] **E.2** The completeness rate, and the ranked table of holes still hit.
      Expected to be short — that is the point, and it makes stage B the
      interesting half.
- [ ] **E.3 — per-logic breakdown.** Which logics are *already* complete? This
      is where stage F's fragment certification starts.
- [ ] **E.4** Re-run per cvc5 release, not per change.

**Closing, certifying, keeping closed**

- [ ] **F.1** Rank found holes by frequency × difficulty; separate "needs a new
      proof rule" from "needs one line" — most of the value to a cvc5 developer.
- [ ] **F.2** Minimize every reproducer with
      [`ddsmt`](https://github.com/ddsmt/ddsmt).
- [ ] **F.3** Certify a fragment: start wherever E.3 reports 100%, argue no hole
      is reachable, grow. Detail in [M7](#g2--how-much-of-cvc5-must-be-right).
- [ ] **F.4** Regression: the known-hole corpus, the TCB ratchet, hygiene, CI.
      Cheap, continuous, explicitly not the point.

---

## G2 — How much of cvc5 must be right?

*The kernel arc, and the one number designed to be watched rather than resolved.*

| metric | today | target |
| --- | --- | --- |
| internal proof checker's dependency closure | **179 files, 41,446 lines — 8.0% of `src/`** | monotonically down |
| rule checkers taking more than a `NodeManager*` | **1 of 13** | 0 |
| rules whose checker is registered as *trusted* | **16** — 8 at level 1, 2 at level 2, 6 at level 4 | fewer, or justified |

**Ours:** `tcb` ✅ with a CI ratchet · extend the closure to the Eunoia seam,
the other component whose independence matters.

**What cvc5 can do:** **R3** — extract the pure `static` helpers out of solver
classes; six checkers currently compile against the solvers they check
([`f-1`](docs/findings/tcb-001.md)). Mechanical, and named per site.

### Work

**Proof API contracts** — needs the semantic tier.

- [ ] `API0001` a `ProofGenerator::getProofFor(f)` that can return a proof of
      something other than `f`.
- [ ] `API0002` **invariants nothing checks in a default run.**
      `ensureClosedWrtInternal` returns immediately unless `--proof-check=eager`
      is set or a trace is on — so in a default proof-producing run, **proof
      closedness is not checked at all**, and the `pfgEnsureClosed` calls through
      the pipeline are inert. Same question for the pedantic-failure machinery
      and for invariants held only by `Assert`. Enumerate which proof invariants
      survive into a default run; that is the configuration users get.
- [ ] `API0003` `CDProof::addStep` with arguments the rule's checker would
      reject — a static arity check against the ledger's second column.
- [ ] `API0004` a proof node constructed but never attached, or a generator
      registered for a fact nothing asks for.

**The kernel** — progressive by construction.

The goal is **not** a machine-checked theorem — nothing available today verifies
this contract over cvc5's C++, and setting that bar means delivering nothing.
The goal is to make it *easier to argue* what cvc5's proof kernel is, along five
axes that improve independently: **nameable, closed, small, locally checkable,
and — last, and only in places — mechanized.** Progress on any axis is real. The
measure is how long the argument is and how much of it a reader can check.

The contract being argued toward:

> for every input in this fragment, under this configuration: if the kernel
> answers `unsat`, it emits a proof, every step of which `ethos` can check.

Safe mode is the natural first kernel: cvc5 already asserts the contract for it,
so this is *discharging* a claim someone already made rather than inventing one.
And M0.7 already moved the "small" axis — that is what a progressive goal looks
like in practice.

- [ ] **M7.1** A configuration language for *K*: logic fragment + option set +
      pinned revision. Start from `--safe-mode=safe`, `QF_UF`.
- [ ] **M7.2** Obligation 1 — **closure**. Reachable code under *K*, via M4.1.
      Every unresolved indirect call is a recorded assumption, never a pass.
- [ ] **M7.3** Obligations 2–5 — coverage, admissibility, elaboration,
      agreement — as queries over M1–M5 restricted to the closure.
- [ ] **M7.4** Obligation 6 — reconstruction termination. **Cannot be discharged
      against today's code**, and now for a cited reason rather than a hunch:
      rewrite reconstruction is a recursive search whose sub-problems — a rule's
      preconditions, and the gap between its instantiated RHS and the target —
      are not provably smaller than the goal, so
      [FMCAD 2022](docs/rare-correspondence.md) bounds it by depth instead.
      Supplying a termination argument is an open research problem.
      *(An earlier draft proposed "make reconstruction syntax-directed rather
      than searched". That was a misreading: matching is already compiled into a
      discrimination tree; the search is over proof obligations, not rules.)*
      The tractable sub-question, and a static analysis we could actually do:
      **classify the 439 RARE rules by whether their preconditions and RHS gaps
      are structurally decreasing**, which bounds how much of the database a
      termination-guaranteeing restriction could cover.
- [ ] **M7.5** The certificate: obligations discharged, assumptions standing,
      and the frontier. A kernel with three honest assumptions beats a green
      check hiding thirty.
- [ ] **M7.6** Grow: `QF_UF` → `QF_LIA` → a theory at a time, each increment
      measured.

---

## G3 — Can we quantify over the entities at all?

*The precondition for G1 being precise. A hole census over fuzzy entities is a
fuzzy census.*

| metric | today | target |
| --- | --- | --- |
| `InferenceId`s produced at exactly one site | **346 of 411 — 84%** | 100% |
| inferences emitted with a sentinel id | **21** (`UNKNOWN` ×15, `NONE` ×6) | 0 |
| declared ids nothing produces | **14** inference, **4** trust, **14** rule | 0 |
| trust steps built with no stated reason | **8** | 0 |
| RARE↔enum correspondence | **439/439, exact both ways** ✅ | hold it |
| rules whose origin is stated rather than inferred | **439 of 533** — the other 94 are identified by *absence* of a marker | 533 |

**Ours:** `inferid`, `trust`, `rewrites` ✅ · `INFER` coverage — cross production
sites against each theory's `InferProofCons` switch. **The completeness core,
still unbuilt, and feasible today.**

**What cvc5 can do:** **R4** (one id, one site), **R7** (derivable pass↔trust-id
names, and `BV_GUASS`), **R7b** (RARE source file in the marker), **R10** (rule
on the hygiene standard). None is hard; together they are what makes G1
trustworthy.

### Work

**Inference coverage** — the completeness core, and the biggest unbuilt
analysis still available without clang.

Where the real completeness gaps live, and where the clang-tidy plugin and
CodeQL earn their place.

- [ ] **M4.1** A CodeQL query computing reachability from safe-mode entry
      points, on the model of `IdentifyNodeIdDependentCalls.ql` — same shape,
      different roots. Output CSV, consumed by the tidy checks below.
- [ ] **M4.2** `cvc5-proof-*` checks in `contrib/tidy-checks/`, registered in
      `Cvc5TidyModule.cpp` alongside `cvc5-node-id-determinism`.
- [ ] `INFER0001` a lemma or conflict sent with a null `ProofGenerator`.
- [ ] `INFER0002` an `InferenceId` a theory can emit for which its
      `InferProofCons` has no case — `switch` coverage against the ids the
      theory actually constructs. Only `strings`, `datatypes` and `sets` have an
      `infer_proof_cons.cpp`; **which theories have none is itself the first
      finding of this family.**
- [ ] `INFER0003` an `InferProofCons` case whose fallback is a trust step —
      present but not covering.
- [ ] `INFER0004` an `InferenceId` declared and never emitted (cleanup).

**Proof hygiene** — the standard is drafted; these are the moves on it.

[`docs/hygiene.md`](docs/hygiene.md) — ten rules on naming, calling conventions,
checker registration and inference-id discipline. It comes before the analysis
milestones because **you cannot bound what you cannot name**: if an
`InferenceId` is emitted at eight sites, "the inferences of theory X" is not a
set, and M4 has nothing to quantify over.

- [x] **H.0** ✅ Draft the standard, with a measurement behind each rule.
- [ ] **H.1** Propose the near-universal rules upstream (H2, H3, H7, H8) — these
      ratify existing practice: 81% of ids are already single-site, prefixes
      already name the owner, the trusted ladder already exists.
- [ ] **H.2** Argue the ones that cost something: H1's 76 exceptions, H5's
      missing rule, H6's API change (`ProofGenerator* pg = nullptr` makes the
      proofless path the default and silent).
- [ ] **H.3** File H10 as [`tcb-001`](docs/findings/tcb-001.md) ✅ and follow it.
- [ ] **H.4** Write checks only for rules that are accepted. A check enforcing a
      convention its owners have not agreed to is noise and will be turned off.
- [ ] **H.5** Offer the settled standard upstream as the contributor guide cvc5
      does not have — its proof docs are 161 lines across five files, with no
      guidance on adding a proof rule or an inference id.

## G4 — Does safe mode do what it says?

*Cheapest signal we have, and it guards the only configuration that carries a
contract.*

| metric | today | target |
| --- | --- | --- |
| options declaring `no_support=["proofs"]` that safe mode leaves on | **1** — `stringLazyPreproc` | 0 |
| links in the completeness chain that anything asserts | **0 of 4** | 4 |
| build jobs running a proof tester | **4 of 22** | — |
| expert options gating no term kind | **2** — `ufHoExp` (logic), `fpExp` (type) | documented, not necessarily 0 |
| features safe mode disables at runtime but the safe build still contains | **essentially all of them** | 0 |

**Ours:** `modes`, `ci`, `fragment`, `gates` ✅ · extend `gates` beyond rewrites
so `ProofRule` and trust severities stop being set by hand.

**What cvc5 can do:** **R2** (name `--check-proofs-complete` in the tester — one
line), **R5** (`no_support` should cover defaults), **R8** (make the safe build
not *contain* the unsafe code, so a class of hole becomes a link error).

### Work

**Safe mode does what it says** — `modes`, `gates`, `fragment` ✅

**Start here.** The fastest signal available: it needs no build and no input,
and it targets the one configuration that carries the contract.

Safe mode's promise — "no feature that does not have full proof and model
support" — is kept by a **hand-maintained list** in
`SetDefaults::setDefaultsPre`, backed by `NoOpTheoryRewriter` throwing
`SafeLogicException` when a disabled theory is reached anyway. Nothing checks
that the list is complete or that the guards are exhaustive.

- [x] **A.1** ✅ Extract the runtime disable list —
      [`dokimasia.modes`](dokimasia/modes/). Parses all 172 macro call sites in
      `set_defaults.cpp` with their guards; renders the per-mode delta (24
      options for safe, 19 for stable); ratchets it against a baseline.
      Tests in `tests/test_modes.py`.
- [x] **A.1c** ✅ **`dokimasia.inferid`** — the InferenceId contract: an id is
      produced at exactly one place, so the control-flow graph is unambiguous.
      **346 of 411 (84%) already comply**; 51 violations, 14 dead markers, and
      21 inferences emitted with a sentinel id. Ratchets. Tests in
      `tests/test_inferid.py`. Feeds [`INFER`](#g3--can-we-quantify-over-the-entities-at-all),
      which cannot enumerate "the inferences of theory X" until this holds.
- [x] **A.1b** ✅ **The `no_support` cross-check** (`modes check`). cvc5's option
      definitions carry a machine-readable `no_support` field; 15 options declare
      `no_support = ["proofs"]`. Every one must be off in a safe run. Two
      mechanisms try to ensure it and neither is complete: `setDefaultsPre`
      disables some by name, and `SolverEngine` throws if a user *sets* one —
      which never fires for an option already on by default. **Found
      `stringLazyPreproc`** (see candidates below).
- [ ] **A.2 — the list against the build.** The runtime disable list and the
      `CVC5_SAFE_MODE` build exclusions must agree. **Today they plainly do
      not:** runtime disables `sep`, `bags`, `ff`, `fp`; the build excludes
      LibPoly and CoCoA. Every feature disabled at runtime but present in the
      safe build is one missed guard from being reachable. This is stage C's
      work list, produced statically.
- [ ] **A.3 — guard exhaustiveness.** For each theory safe mode disables, is
      *every* entry point guarded, or only the rewriter path that
      `NoOpTheoryRewriter` covers?
- [ ] **A.4 — the list against reality.** A feature reachable in safe mode with
      no proof support that is on neither list. The headline check.
- [ ] **A.5 — drift.** An option or theory added since the pinned revision that
      reaches proof-relevant code and appears on no list. What catches the
      *next* one.

**The safe-mode contract machinery**

cvc5 promises that safe mode has "full proof and model support" and implements
the promise as a hand-maintained list of things safe mode turns off. The whole
question is whether that list is complete. This milestone is the machinery
behind [stage A](#g4--does-safe-mode-do-what-it-says), and its
output is the work list for [stage C](#g4--does-safe-mode-do-what-it-says).

- [ ] **M1.1** Model safe mode as a configuration: what
      `SetDefaults::setDefaultsPre` disables under `SAFE` and `STABLE`, the
      `FULL_STRICT` upgrade, and the `checkProofsComplete` implication.
- [ ] `MODE0001` **a feature reachable in safe mode with no proof support that
      is not on the disable list.** The headline check of the project. Needs the
      inventory from M4/M5 to say "no proof support" precisely, but the
      *reachability* half is table-tier and can land first.
- [ ] `MODE0002` an option or theory added since the pinned revision that
      reaches proof-relevant code and appears in neither the safe-mode list nor
      `incompatibleWithProofs` — the regression this family exists to catch.
- [ ] `MODE0003` the silent-change set: `bvAssertInput`, `bvSolver`,
      `nlCovVarElim`, and under `FULL_STRICT` `ufSymmetryBreaker`,
      `cegqiMidpoint`, `cegqiUseInfInt/Real`, `dtSharedSelectors`. Each carries
      a justification as a code comment and no test that it stays true.
- [ ] `MODE0004` the refused set — `fresh-binders`, `global-negate`, deep
      restarts, lemma inprocessing, sygus under full proofs — reported as the
      honest scope limit of the contract.
- [ ] `MODE0005` the `SAFE` vs `STABLE` vs `UNRESTRICTED` delta, per option, as
      a table a release note could quote.
- [ ] `MODE0006` known unresolved: `TODO (wishue #154)` — Minisat with
      DRAT/LRAT throws no logic exception. Track, do not re-file.

**Is cvc5's proof CI intact?** — `dokimasia.ci` ✅

An **independent** check that the thing currently keeping proofs complete is
still doing it. CI is the safety net today, and a safety net that quietly stops
being attached looks exactly like one that is working: every job still passes.

This is static — CI config and the regression runner are just files — so it is
stage-A latency, and it is the only analysis here whose subject is cvc5's
*test infrastructure* rather than its solver.

What the configuration says today, at `16c4001e53`:

- **Proof testers run in 4 of 22 matrix jobs.** `ubuntu:safe-mode` and
  `ubuntu:stable-mode` carry `--tester proof --tester cpc`;
  `ubuntu:production-dbg` carries `proof`; `ubuntu:production-dbg-clang` carries
  `cpc`, `alethe` and `unsat-core`. *(An earlier hand count here said 2 of ~25;
  it missed the jobs whose proof testers are not named `proof`. The tool
  corrected it — which is the argument for the tool.)*
- **`proof` is in `g_default_testers` but almost every job overrides the list**,
  so a developer running regressions locally gets proof checking that most CI
  jobs do not.
- **`--check-proofs-complete` appears nowhere** in `.github/` or `test/`. The
  `proof` tester passes `--check-proofs --proof-check=lazy`; completeness is
  enabled *implicitly*, because in a safe build `setDefaultsPre` turns
  `checkProofsComplete` on when `checkProofs` is set and no granularity was
  requested.
- So the completeness guarantee is a **chain of four links**, none asserted
  anywhere: the safe-mode job exists → it runs `--tester proof` → the tester
  passes no `--proof-granularity` → the implication in `setDefaultsPre`
  survives. Adding a granularity flag to that tester would silently switch
  completeness testing off, and every job would still pass.
- **`--proof-check=lazy`** means `ensureClosedWrtInternal` returns early, so
  **proof closedness is never checked in CI** either (see `API0002`).
- `exclude_regress: 3-4` — the two heaviest regression levels are excluded from
  these jobs.

- [x] **A2.1** ✅ **`dokimasia.ci`** — the matrix, the tester flags, and the
      completeness chain, ratcheted. Tests in `tests/test_ci.py`.
- [x] `CI0001` ✅ a build job that promises a proof-bearing mode but runs no
      proof tester. None today: both safe- and stable-mode jobs test proofs.
- [ ] `CI0002` **the completeness chain.** Assert each link, and fail if any
      breaks. The cheapest fix upstream is to pass `--check-proofs-complete`
      *explicitly* in the proof tester, so the guarantee is named rather than
      implied — a finding of kind C, and a one-line patch.
- [x] `CI0003` ✅ a proof tester whose flags disable a check it appears to
      perform. Reported: the `proof` tester runs `--proof-check=lazy`, so
      closedness is never checked by it.
- [x] `CI0004` ◐ the exclusions are reported (`exclude_regress: 3-4` on all four
      proof-testing jobs). *Still open:* whether each still has a reason.
- [ ] `CI0005` drift: a new job, tester or exclusion that changes proof coverage
      without changing the stated coverage.

**A safe build that cannot be unsafe**

The second stretch goal, in the same spirit as the kernel and sharing its
tooling. **Make the safe build not contain the unsafe code**, so that a class of
proof hole becomes a *link error* — the lowest-latency signal there is.

Starting point: `ENABLE_SAFE_MODE` → `-DCVC5_SAFE_MODE` exists, but **five files
in `src/` mention it** and two only reword an error message. Real exclusions are
third-party only (LibPoly, CoCoA).

- [ ] **C.1** Measure the safe build's dependency closure with
      `dokimasia.tcb --seeds ...`, against the default build. Today the
      difference should be near zero; that gap *is* the goal, quantified.
- [ ] **C.2** Take stage A.2's list and, feature by feature, move each from
      "disabled at runtime" to "not compiled." Experimental theories first —
      they are already cleanly separated by directory.
- [ ] **C.3** Each move is checkable: the symbol should not be in the safe
      binary. That is a test, not an argument.
- [ ] **C.4** Report progress as a ratio: *of the features safe mode disables,
      how many are absent from the safe build?* Starts near 0.
- [ ] **C.5** The end state: safe mode's promise is kept by the linker, and
      `setDefaultsPre`'s list becomes a redundant belt to the build's braces
      rather than the only thing standing between a user and an unproven
      inference.

## G5 — Is completeness a property of the code, or of a budget?

*The research frontier. We can measure it; we cannot fix it.*

| metric | today | target |
| --- | --- | --- |
| rewrites whose reconstruction depends on a search budget | **38** | — |
| proofs fully fine-grained, per FMCAD 2022 | **20–22%** (92–95% of *steps*) | — |
| RARE rules whose preconditions and RHS gap are structurally decreasing | **unmeasured** | measure it |

Reconstruction is a recursive search with **no termination guarantee** — the
depth limit is what makes it halt, not a tuning knob
([`rare-correspondence.md`](docs/rare-correspondence.md)).

**Ours:** classify the 439 RARE rules by whether their sub-problems are
provably smaller. That bounds how much of the database a
termination-guaranteeing restriction could cover, and it is the honest static
contribution to an open problem.

**What cvc5 can do:** **R9** — test each RARE rule against the rewriter. It is
the only thing that catches a rule which *misstates* the rewrite, a failure that
today is silent forever.

---

### Work

- [ ] **G5.1** Classify the 439 RARE rules by whether their preconditions
      and RHS gap are structurally decreasing. Bounds how much of the
      database a termination-guaranteeing restriction could cover, and is
      the honest static contribution to an open problem.
- [ ] **G5.2** Measure the budget's bite: how often does reconstruction fail
      at the default `--proof-rewrite-rcons-rec-limit`, and does raising it
      help? Needs a corpus run, and settles whether `i-4` is theoretical or
      routine.

---

## Fast signals, and where inputs come from

Where new inputs come from, once SMT-LIB is exhausted.

- [ ] **D.1 — fuzzing is murxla's job, not ours.** murxla is an end-to-end
      black-box fuzzer, already an `ExternalProject` in cvc5's build
      (`cmake/fuzzing-murxla.cmake`, pinned at `9ba2583`), maintained by people
      who are good at it. **We do not build, wrap or drive a fuzzer**; we are
      white box and our value is the holes an input-driven tool cannot reach.
      Posture written up in
      [`docs/tooling.md`](docs/tooling.md#posture-toward-murxla).

      What we *can* usefully contribute in that direction is a fragment
      description — "a hole here needs a formula with these features" — from
      stage B.3, and consumption of anything it finds as a `holes/` regression.
- [ ] **D.2 — targeted synthesis.** Stage B.3 says which fragment a latent hole
      needs; generate small inputs against that, rather than fuzzing blind.
- [ ] **D.3 — the known-hole corpus.** A local `holes/` directory: per hole, the
      `.smt2`, the option set, the expected rule or `TrustId`, and a provenance
      line. Fast to run, and it is the regression suite for stage F.

### Design decision — no network access on any analysis path

Proof holes get reported as GitHub issues, and that data is worth having. The
tool will still not fetch it. Three reasons:

1. **Reproducibility.** An analysis whose result depends on *when* it ran is not
   a measurement. The same cvc5 revision must give the same answer.
2. **Hermetic CI.** A check that can fail because a network call was slow is a
   check people switch off.
3. **The volume does not justify it.** Proof-hole reports arrive at a rate a
   human handles comfortably. Automating the fetch optimizes the part that is
   not the bottleneck.

So: `holes/` is populated **by a human**, or by an import script that is invoked
explicitly, never runs as part of an analysis, and writes files a human reviews
before they land. Provenance is recorded as text (an issue number), not as a
live link the tool follows.

*Revisit if* the volume outgrows manual curation, or if we want closed issues to
auto-retire regression entries. Neither is true now.

## Infrastructure

The front-end question is now half-settled: cvc5 already runs a custom
clang-tidy plugin fed by a custom CodeQL query
([`docs/tooling.md`](docs/tooling.md#what-cvc5-already-runs)), so tiers 1 and 2
have a delivery vehicle and we do not design one. What is left to build here is
tier 0.

- [ ] **M0.1** Repository skeleton: `dokimasia/` package, `tests/`, `tools/`,
      `docs/`, `pyproject.toml`. No dependencies for tier 0.
- [ ] **M0.2** Diagnostic model: code, severity, span, notes, help — the
      rustc-shaped renderer anoieu uses. Formats: text, `json`, **`sarif`**,
      `github`.
- [ ] **M0.3** Check registry with docstrings, so `explain <CODE>` and
      `docs/checks.md` are generated from the checks and cannot drift.
- [ ] **M0.4** Table-tier front end: `EVALUE` enum reader, C++ `enum class`
      reader, `switch`/`case` label extractor with `#ifdef` awareness, `.toml`
      option reader. `#ifdef` awareness is not optional — the `FF_*` result
      below is entirely a conditional-compilation story.
- [ ] **M0.5** Pin a cvc5 checkout for the corpus; record the commit. Every
      count in the README is a test.
- [ ] **M0.6** `docs/findings.md` and `docs/upstream.md`, with the finding
      lifecycle and the **rank** (1/2/3) from
      [`docs/tooling.md`](docs/tooling.md#d5--safe-mode-first-and-the-reproducer-is-the-deliverable).
- [x] **M0.7** ✅ **`dokimasia.tcb`** — the first subtool. Measures the internal
      proof checker's dependency closure, weighs each edge and subsystem as a
      cut, explains why any file is in the closure, and ratchets the number in
      CI. Tests in `tests/test_tcb.py`; baseline in `tcb-baseline.json`.
      Produced [`docs/findings/tcb-001.md`](docs/findings/tcb-001.md).

## Cross-cutting

### The reproducer pipeline — what turns a hypothesis into a bug report

A rank-1 finding needs an input, and this is the machinery that produces one.

- [ ] **R.1** Corpus runner: cvc5 over a benchmark set under
      `--safe-mode=safe --produce-proofs --check-proofs`, collecting every
      `The proof was incomplete` with its rule, `TrustId` and theory.
- [ ] **R.2** Attribution: map each failure back to the code site the static
      analysis predicted. **This is the measurement that justifies the project** —
      a prediction confirmed by an input is the only evidence a check is worth
      running.
- [ ] **R.3** Minimize with [`ddsmt`](https://github.com/ddsmt/ddsmt) before
      filing.
- [ ] **R.4** The inverse direction, and the harder one: given a predicted
      unreachable-by-the-corpus site, *construct* an input that reaches it.
      Start with the fragment the analysis says is needed and build up by hand;
      fuzzing guided by the same predicate is the stretch version.
- [ ] **R.5** Headline metric: rank-1 inputs produced that cvc5's regression
      suite does not already contain.

### Assertion recommendations (finding kind D)

- [ ] **D.1** A rule for which checks *should* become assertions: decidable from
      cvc5's own tables at startup, cheap, and stable across configurations.
      First candidates: every `ProofRule` asked about has a registered checker;
      every `InferenceId` a theory emits has an `InferProofCons` case.
- [ ] **D.2** **The validation gate.** No assertion is proposed until it has been
      applied to a cvc5 build configured `--assertions` and the regression suite
      has passed with it in place. If an assertion we suggest fires falsely, that
      is our bug, exactly as a false positive is.
- [ ] **D.3** Retire the corresponding check once the assertion lands upstream.
      A check here that could have been an assertion in cvc5 is a design failure.

### Adoption and CI

- [ ] **A.1** Propose **SARIF upload** for cvc5's existing nightly. Independent
      of anything we write, and the difference between a job that fails loudly
      and one whose output someone reads.
- [ ] **A.2** Propose the ledger as a **per-push lint** — seconds, no baseline
      needed.
- [ ] **A.3** Our own CI runs every check over the pinned cvc5, so a change
      inventing a false positive fails *this* build before it reaches theirs.
- [ ] **A.4** Upstream tiers 1 and 2 into `contrib/tidy-checks/` and
      `contrib/codeql/`.

### Witnesses, docs, handoff

- [ ] **W.1** Every check owns a witness: a source excerpt that must be reported
      and, where the distinction matters, one that must not. For reachability
      claims, additionally an SMT-LIB reproducer and an option set.
- [ ] **W.2** The oracle is `cvc5 --check-proofs-complete`, as `ethos` is
      anoieu's. The number worth reporting is how many of our findings it does
      not already catch on cvc5's own regressions.
- [ ] **W.3** `docs/checks.md` generated from the registry;
      `docs/what-runtime-misses.md` as the counterpart to anoieu's
      `what-ethos-misses.md`; `docs/findings.md`; `docs/upstream.md`.
- [ ] **W.4** Handoff format to anoieu for findings that turn out to be about
      the signature rather than the C++.

---

## Open design questions

1. **Should cvc5 emit the ledger itself?** Several tier-0 checks are table
   consistency questions cvc5 could answer at build time by dumping its own
   registries as JSON. That is less code here and more value there — and it
   turns a static analysis into an invariant cvc5 maintains itself. The same
   argument as finding kind D, one level up.
2. **How precise is CodeQL's call graph on cvc5?** The kernel closure stands or
   falls on it, and theory code is full of virtual dispatch. Measure on the
   existing `IdentifyNodeIdDependentCalls.ql` before committing to M7.2; SVF is
   the fallback if it is too imprecise.
3. **Where does reachability evidence come from?** Static closure over-
   approximates. An instrumented build logging which inference sites fire across
   a corpus gives a *lower* bound, and the gap between the two bounds is the
   honest uncertainty in every severity claim we make.
4. **What is the unit of a kernel?** Logic fragment, option set, or an explicit
   list of enabled solvers? The first is what users say; the third is what the
   analysis can close over. Safe mode is a useful forcing function because cvc5
   has already picked an answer.

## Next four

In order. Everything above that is not on this list is context, not a queue.

1. **Get an input for `i-1`.** `LAMBDA_ELIM` is the only candidate that could
   become a rank-1 finding, and no amount of static work will settle it. A
   `define-fun` benchmark under `--safe-mode=safe --produce-proofs
   --check-proofs`.
2. **Build `INFER` coverage** (G3). The completeness core, table-tier, and it
   settles `i-6`.
3. **Extend `gates` to rules and trust steps** (G4). Ranks ~85 currently
   unranked entries across two tools.
4. **Ask for R1 and R2.** R2 is one line. R1 retires most of our fragility and
   is useful to cvc5 independently of us.

## Standing

- **Ratchets in CI** — `tcb`, `modes`, `ledger`, `trust`, `inferid`, `rewrites`,
  `ci` all have `baseline --check`. They run in seconds and need no build.
- **A finding is confirmed before it is filed**, and for a defect that means an
  input. See [`docs/findings.md`](docs/findings.md).
- **A false positive is our bug**, including a retracted headline number — the
  log is in [`issues.md`](docs/issues.md#settled).

## Deliberately not doing

- **Alethe.** Not on the critical production path and **not available in safe
  mode**, so it cannot bear on the contract. A shallow look found the shape one
  would expect — the post-processor carries a `d_reasonForConversionFailure`,
  and deliberately emits holes for `BV_BITBLAST_STEP` on `udiv`/`urem`/shifts
  ("no checking for those yet in Carcara or Isabelle"). Recorded, not pursued.

- **Fuzzing.** [murxla's job](docs/tooling.md#posture-toward-murxla); we are
  white box and our value is the holes an input-driven tool cannot reach.
- **An AST tier**, until the table tier is exhausted and **R1** has been asked
  for. R1 would retire most of what an AST tier would be for.
- **A robustness abstraction layer** over cvc5's source. Tests pinning
  hand-verified facts are the whole budget; see
  [`coupling.md`](docs/coupling.md).
