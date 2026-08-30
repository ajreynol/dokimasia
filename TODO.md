# TODO

The goal is [**complete proofs, always**](README.md#the-goal). This file is the
route to it. The delivery decisions are in [`docs/tooling.md`](docs/tooling.md).

Everything here is judged by one question: *does this get cvc5 closer to
producing a complete proof for everything it solves?* Work that does not is
either an instrument for work that does, or it should be dropped.

## The route, ordered by latency

Safe mode already has **almost no proof holes on SMT-LIB**. So the corpus is a
good oracle and a nearly exhausted signal, and the remaining holes are the ones
it does not reach. The ordering below is by **how fast a stage returns an
answer**, not by how much it costs — because feedback latency is the bottleneck,
not compute.

| stage | what | latency | status |
| --- | --- | --- | --- |
| **A** | **Safe mode does what it says** | seconds, no build | ◐ tooling built, first candidate found |
| **B** | **The latent inventory** — holes no input reaches | seconds, no build | needs M1–M5 |
| **C** | **A safe build that cannot be unsafe** | one build | stretch, tooling exists |
| **D** | **Fast dynamic signals** — fuzzing, known-hole corpus | minutes | murxla already in cvc5's build |
| **E** | **The SMT-LIB baseline** | hours, once | needs a build + corpus |
| **F** | Close holes, certify fragments, keep them closed | ongoing | downstream of all of it |

---

## Stage A — safe mode does what it says

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

## Stage B — the latent inventory

**The corpus cannot prove *always*.** It shows what benchmarks reach; the risk is
what they do not, and on safe mode that is now essentially all of the remaining
risk. This is the one thing here nobody else can do:

> **static hole inventory − what any input has hit = the latent holes.**

- [ ] **B.1** The static inventory, from [M1–M5](#the-analysis-backlog).
- [ ] **B.2** Subtract stage D and E results. Publish the difference — the
      **latent count** is one of the project's two headline numbers.
- [ ] **B.3** Per latent hole: construct an input that reaches it (promoting it
      to a real finding), or argue it is unreachable (shrinking the problem).
- [ ] **B.4** A latent hole that resists both is the most interesting object in
      the project — it is exactly what neither testing nor analysis settles.

## Stage C — a safe build that cannot be unsafe

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

## Stage D — fast dynamic signals

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

## Stage E — the SMT-LIB baseline

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

## Stage F — close, certify, keep closed

- [ ] **F.1** Rank found holes by frequency × difficulty; separate "needs a new
      proof rule" from "needs one line" — most of the value to a cvc5 developer.
- [ ] **F.2** Minimize every reproducer with
      [`ddsmt`](https://github.com/ddsmt/ddsmt).
- [ ] **F.3** Certify a fragment: start wherever E.3 reports 100%, argue no hole
      is reachable, grow. Detail in [M7](#m7--the-kernel-krn--the-stretch-goal).
- [ ] **F.4** Regression: the known-hole corpus, the TCB ratchet, hygiene, CI.
      Cheap, continuous, explicitly not the point.

---

# The analysis backlog

What stages A, B and C are built out of. Ordered *within itself* by cost. M1 is
the machinery behind stage A; M2–M5 build the latent inventory of stage B.

---

## M0 — skeleton and the table-tier front end

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

## M0.5 — proof hygiene (the warm-up)

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

## M1 — the safe-mode contract (`MODE`) — machinery for stage A

cvc5 promises that safe mode has "full proof and model support" and implements
the promise as a hand-maintained list of things safe mode turns off. The whole
question is whether that list is complete. This milestone is the machinery
behind [stage A](#stage-a--safe-mode-does-what-it-says), and its
output is the work list for [stage C](#stage-c--a-safe-build-that-cannot-be-unsafe).

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

## M2 — the rule ledger (`RULE`, `SEAM`)

One row per `ProofRule`, four columns: **produced by**, **checked by**,
**elaborated by**, **printed by**. A hole in any column is a claim.

- [ ] **M2.1** Build the ledger and render it (`dokimasia rules`), with a
      safe-mode column: can this rule be produced under `--safe-mode=safe`?
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

## M3 — the trust census (`TRUST`, `PP`)

75 `TrustId` values name the ways cvc5 admits a step without proving it. Being
named is the point; the census nobody has is **which are reachable in safe
mode**.

- [ ] **M3.1** Enumerate every construction site: `addTrustedStep`, `mkTrustId`,
      `mkTrustNode`, `mkTrustedNode`, `TrustProofGenerator`.
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

## M4 — inference coverage (`INFER`) — first tier-1/2 checks

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

## M5 — rewriting and elaboration (`RW`, `ELAB`)

- [ ] `ELAB0001` a `ProofRule::MACRO_*` with no expansion case in
      `proof_post_processor.cpp` — 9 macro rules, 16 references, so the mapping
      is not one-to-one and needs reading rather than counting.
- [ ] `ELAB0002` an expansion that can emit another macro with no termination
      argument.
- [ ] `ELAB0003` per granularity mode, which rules survive to the final proof —
      the honest answer to what `--proof-granularity` buys.
- [ ] `RW0001` a `ProofRewriteRule` with no RARE rule and no reconstruction.
- [ ] `RW0002` **budget-dependent completeness.** `proof_post_processor_dsl.cpp`
      reconstructs under `--proof-rewrite-rcons-rec-limit` (default 5) and
      `-step-limit`; on failure the macro step *remains*. Report every rewrite
      whose reconstruction depends on the budget. The deepest obstacle to M7 and
      worth characterising early even though it cannot be fixed here.
- [ ] `RW0003` a theory rewriter path returning a rewritten node with no
      `ProofRewriteRule` tag reachable for it.

## M6 — proof API contracts (`API`)

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

## M7 — the kernel (`KRN`) — the stretch goal

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
- [ ] **M7.4** Obligation 6 — reconstruction termination. Expected outcome: it
      *cannot* be discharged against today's code (`RW0002`), and the deliverable
      is a proposal to make reconstruction inside the kernel syntax-directed
      rather than searched.
- [ ] **M7.5** The certificate: obligations discharged, assumptions standing,
      and the frontier. A kernel with three honest assumptions beats a green
      check hiding thirty.
- [ ] **M7.6** Grow: `QF_UF` → `QF_LIA` → a theory at a time, each increment
      measured.

---

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

## Candidate findings from the design pass

Noticed while reading cvc5 `16c4001e53`. **Unconfirmed — hypotheses, not
findings.** Each needs a reproducer or a maintainer's answer before it goes near
`docs/findings.md`.

| # | what | first check | rank | why it might be nothing |
| --- | --- | --- | --- | --- |
| c-1 | The safe-mode disable list in `setDefaultsPre` is hand-maintained; nothing tests that it still covers everything without proof support | `MODE0001` | 2 | it may be complete today. The check is about the next feature added |
| c-2 | `EoPrinter::isHandled` is an allowlist of 135 case labels over 172 rules; the unhandled set has never been computed | `SEAM0001` | 2 | 172−135 is a naive subtraction, not a finding: labels are not distinct rules, some rules appear in several switches, and conditional arms make handledness argument-dependent. The point is that nobody knows the real number |
| c-3 | Proof completeness depends on `--proof-rewrite-rcons-rec-limit` / `-step-limit`: when reconstruction fails the macro step remains | `RW0002` | 2 | known and accepted engineering. Worth stating precisely because it bounds what any kernel contract can claim |
| c-4 | The 11 `FF_*` rules are in the public enum and documented, have no registered checker, and have zero emission sites — `src/theory/ff` is entirely `#ifdef CVC5_USE_COCOA` | `RULE0003`, `RULE0004` | 3 | likely deliberate: reserved for a CoCoA build. The question is whether the *public* enum should carry rules no build produces. Note safe mode disables `ff` anyway |
| c-5 | Only `strings`, `datatypes` and `sets` have an `infer_proof_cons.cpp` | `INFER0002` | 2 | other theories may attach generators at the inference site instead — needs tier 1 to tell the two apart |
| c-6 | `ensureClosedWrtInternal` returns early unless `--proof-check=eager` or a trace is on, so a default `--produce-proofs` run never checks its proofs are closed | `API0002` | 3 | deliberate: the check is expensive and CI runs eager mode. Worth stating because it decides what a *release* run guarantees, which is what a kernel contract is about |
| c-7 | `TODO (wishue #154)`: Minisat with DRAT/LRAT throws no logic exception | `MODE0006` | 3 | already known upstream; track, do not re-file |
| c-8 | The nightly enforces only via `-warnings-as-errors`; no SARIF upload, no baseline, no PR annotation | `A.1` | — | a process recommendation, not a defect |
| **c-9** | **`stringLazyPreproc` declares `no_support = ["proofs"]`, defaults to `true`, and is disabled by neither `setDefaultsPre` nor the `SolverEngine` guard — so a default safe-mode run enables a feature cvc5 annotates as having no proof support** | `modes check` ✅ | 2 | two readings, both defects: either safe mode should disable it, or the annotation is stale and strings lazy preprocessing does now have proof support. **Needs a maintainer's answer, not a reproducer** — that is the cheapest way to settle it |
| c-10 | `macrosQuantMode` also surfaces from `modes check` | `modes check` ✅ | 3 | almost certainly spurious: its effect is gated by `macrosQuant`, default `false`. A defaults-only check cannot see that gate. Listed so the limitation is visible rather than silently filtered |

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
