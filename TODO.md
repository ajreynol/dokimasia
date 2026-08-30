# TODO

The plan behind [`README.md`](README.md); the delivery decisions are in
[`docs/tooling.md`](docs/tooling.md).

Two principles set the ordering:

**Safe mode first.** `--safe-mode=safe` is the only configuration cvc5 promises
complete proofs in, so it is the only one where a hole is a *contract violation*
rather than a known gap. Everything that narrows the search inside safe mode
outranks everything that broadens it elsewhere.

**Cheap and exact before deep and approximate.** Everything through M3 is
table-against-table: it needs a checkout and no build, runs in seconds, and
produces findings before anyone configures clang.

Status markers, borrowed from anoieu:
✅ **live** — written, tested, run over the corpus · ◐ **partial** — the useful
half exists and the limit is stated · ○ **sketched** — designed here, not written

Everything below is ○.

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

## M1 — the safe-mode contract (`MODE`) — **top priority**

cvc5 promises that safe mode has "full proof and model support" and implements
the promise as a hand-maintained list of things safe mode turns off. The whole
question is whether that list is complete.

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

> for every input in this fragment, under this configuration: if the kernel
> answers `unsat`, it emits a proof, every step of which `ethos` can check.

Safe mode is the natural first kernel: cvc5 already asserts the contract for it,
so M7 is the work of *discharging* a claim someone already made rather than
inventing one.

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
