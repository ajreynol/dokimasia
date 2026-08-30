# TODO

The plan behind [`README.md`](README.md). Nothing here is built yet; the
ordering is deliberate, and the principle is **cheap and exact before deep and
approximate** — every milestone before M4 needs only a cvc5 checkout, and each
one produces findings on its own.

Status markers, borrowed from anoieu:
✅ **live** — written, tested, run over the corpus · ◐ **partial** — the useful
half exists and the limit is stated · ○ **sketched** — designed here, not written

Everything below is ○.

---

## The front end decision (M0)

The single architectural call, and worth making explicitly because it decides
how far the project gets before it needs a build of cvc5.

**Two tiers.**

**The table tier** reads cvc5's *declarative* structure directly from source
text: the `EVALUE(...)` enumerations in `include/cvc5/cvc5_proof_rule.h`, the
`TrustId` and `InferenceId` enums, the `*.toml` option definitions, the
`registerChecker` call lists, and the `switch`/`case` bodies that act as
registries (`EoPrinter::isHandled`, `InferProofCons::convert`, the post
processor's macro dispatch). These are hand-maintained tables that happen to be
written in C++, and reading them needs a bracket matcher and a `case` scanner,
not a compiler. **No build, no `compile_commands.json`, runs in seconds.** This
tier alone covers `RULE`, `TRUST`, `MODE`, `SEAM`, `ELAB` and most of `PP` — a
large majority of what the README claims.

**The semantic tier** uses clang (libclang, or a plugin over
`compile_commands.json`) for the questions that are genuinely about dataflow:
which call sites pass a null `ProofGenerator`, which `InferenceId`s a theory can
actually emit, call-graph closure for the kernel. Slower, needs a configured
build, and lands later.

- [ ] **M0.1** Repository skeleton: `dokimasia/` package, `tests/`, `tools/`,
      `docs/`, `pyproject.toml`, no dependencies for the table tier.
- [ ] **M0.2** Diagnostic model: code, severity, span, notes, help — the
      rustc-shaped renderer anoieu uses. Formats: text, `json`, `github`.
- [ ] **M0.3** Check registry with docstrings, so `explain <CODE>` and
      `docs/checks.md` are generated from the checks and cannot drift.
- [ ] **M0.4** Table-tier front end: `EVALUE` enum reader, C++ `enum class`
      reader, `switch`/`case` label extractor with `#ifdef` awareness, `.toml`
      option reader. `#ifdef` awareness is not optional — the `FF_*` result
      below is entirely a conditional-compilation story.
- [ ] **M0.5** Pin a cvc5 checkout for the corpus; record the commit. Every
      count in the README is a test.
- [ ] **M0.6** `docs/findings.md` and `docs/upstream.md` skeletons, and the
      finding lifecycle from anoieu (`open` → `filed` → `fixed`/`declined`).

---

## M1 — the rule ledger (`RULE`, `SEAM`)

The ledger is the spine of the project. One row per `ProofRule`, four columns:
**produced by**, **checked by**, **elaborated by**, **printed by**. A hole in
any column is a claim about the pipeline.

- [ ] **M1.1** Build the ledger and render it (`dokimasia rules`).
- [ ] `RULE0001` a rule with no registered checker.
- [ ] `RULE0002` a rule registered via `registerTrustedChecker` — report the
      declared pedantic level (1–4); this is cvc5's own statement of how much
      its checker really checks, and it should be visible rather than buried.
- [ ] `RULE0003` a rule declared in the public enum that nothing in `src/`
      produces.
- [ ] `RULE0004` a rule produced under a build flag whose checker is not
      registered under the same flag (the general form of the `FF_*` case).
- [ ] `RULE0010` **documentation drift** — the `\inferrule{premises | args}`
      spec in `cvc5_proof_rule.h` against the arity the checker actually reads
      and the shape `eo_printer.cpp` prints. *This is cvc5's `cvc5-6` request to
      anoieu; it is a C++ question and belongs here.*
- [ ] `SEAM0001` a rule `EoPrinter::isHandled` can never accept. Requires
      modelling the **conditional arms** — `isHandledTheoryRewrite`,
      `isHandledBitblastStep` and friends make handledness a property of a rule
      *plus its arguments*, so the honest output is three-valued: always
      handled, never handled, handled depending on arguments.
- [ ] `SEAM0002` for the argument-dependent arms, characterise the unhandled
      argument set and ask whether any producer can construct one.
- [ ] `SEAM0003` `EoNodeConverter::isHandledSkolemId` as the same coverage
      problem over `SkolemId` — a skolem the seam cannot print sinks a proof
      just as surely as a rule it cannot print.
- [ ] `SEAM0004` a `ProofRewriteRule` (534 of them) with no Eunoia landing.
      Cross-repo: the C++ half is ours, the signature half is anoieu's — define
      the handoff format before writing this one.

## M2 — the trust census (`TRUST`)

75 `TrustId` values name the ways cvc5 admits a step without proving it. Being
named is good — that is why they exist — but the census nobody has is *which
ones a default-options run can still reach*.

- [ ] **M2.1** Enumerate every construction site: `addTrustedStep`,
      `mkTrustId`, `mkTrustNode`, `mkTrustedNode`, `TrustProofGenerator`.
- [ ] `TRUST0001` a `TrustId` with no construction site — dead, and a cleanup.
- [ ] `TRUST0002` a trust step reachable under default options in a supported
      logic. **The headline check**; severity is reachability.
- [ ] `TRUST0003` a trust step introduced with `TrustId::NONE`, i.e. an
      unnamed hole.
- [ ] `TRUST0004` the theory-lemma census: `TrustId::THEORY_LEMMA` by
      `TheoryId`, matching the `d_trustTheoryLemmaCount` statistic cvc5 already
      keeps — cross-checking against that statistic is how this check gets
      validated cheaply.
- [ ] **M2.2** Diff mode: trust sites added or removed between two cvc5
      revisions. This is the shape CI wants.

## M3 — the proof-mode delta (`MODE`)

Because proofs are off by default, this is not a secondary family. It asks
whether the solver that produces the proof is the solver that solved the
problem.

- [ ] **M3.1** Model `SetDefaults::incompatibleWithProofs` and the
      `produce-proofs` branches of `set_defaults.cpp` as a delta: option, old
      value, new value, whether the change is refused or silent.
- [ ] `MODE0001` a technique **silently disabled** when proofs are enabled.
      Enumerate today: `bvAssertInput`, `bvSolver`, `nlCovVarElim`, and under
      `FULL_STRICT` `ufSymmetryBreaker`, `cegqiMidpoint`, `cegqiUseInfInt`,
      `cegqiUseInfReal`, `dtSharedSelectors`. Each needs a stated
      justification; the check is that the list and the justifications stay in
      sync.
- [ ] `MODE0002` a technique **refused** with proofs — `fresh-binders`,
      `global-negate`, deep restarts, lemma inprocessing, sygus under full
      proofs. Report as the honest scope limit of the contract.
- [ ] `MODE0003` an option added since the pinned revision that reaches
      proof-relevant code and appears in *neither* list — the regression this
      family exists to catch.
- [ ] `MODE0004` the `FULL` vs `FULL_STRICT` gap, per option.
- [ ] `MODE0005` known unresolved: the `TODO (wishue #154)` in
      `incompatibleWithProofs` — Minisat with DRAT/LRAT modes throws no logic
      exception. Track it rather than rediscover it.
- [ ] **M3.2** `dokimasia delta` output as a table a release note could quote:
      *"with proofs on, cvc5 is these N techniques weaker."*

## M4 — inference coverage (`INFER`, `PP`) — needs the semantic tier

Where the real completeness gaps live, and where a compiler becomes necessary.

- [ ] **M4.1** Clang front end over `compile_commands.json`; a resolvable
      call graph restricted to theory and preprocessing code.
- [ ] `INFER0001` a lemma or conflict sent with a null `ProofGenerator`.
- [ ] `INFER0002` an `InferenceId` a theory can emit for which its
      `InferProofCons` has no case — a `switch`-coverage problem against the
      set of ids the theory actually constructs. Only `strings`, `datatypes`
      and `sets` have an `infer_proof_cons.cpp`; **which theories have none at
      all is itself the first finding of this family.**
- [ ] `INFER0003` an `InferProofCons` case whose fallback is a trust step —
      present but not covering.
- [ ] `INFER0004` an `InferenceId` declared and never emitted (cleanup).
- [ ] `PP0001` a `PreprocessingPass` that neither produces a proof nor
      declares a `PREPROCESS_*` trust id. The `TrustId` enum carries a
      `PREPROCESS_*` family that roughly tracks the pass list (32 mentions
      against 37 pass headers), so a first approximation is checkable at the
      table tier — do that version in M2 and the real one here. The passes with
      no entry either prove their work or are the finding.
- [ ] `PP0002` a pass whose `PREPROCESS_*` id exists but is never used.

## M5 — rewriting and elaboration (`RW`, `ELAB`)

- [ ] `ELAB0001` a `ProofRule::MACRO_*` with no expansion case in
      `proof_post_processor.cpp` — 9 macro rules, 16 references, so the
      mapping is not one-to-one and needs reading rather than counting.
- [ ] `ELAB0002` an expansion that can emit another macro without a
      termination argument.
- [ ] `ELAB0003` per granularity mode (`MACRO`, `REWRITE`, `THEORY_REWRITE`,
      `DSL_REWRITE`, `DSL_REWRITE_STRICT`), which rules survive to the final
      proof — a table, and the honest answer to "what does
      `--proof-granularity` actually buy".
- [ ] `RW0001` a `ProofRewriteRule` with no RARE rule and no reconstruction.
- [ ] `RW0002` **budget-dependent completeness.** `proof_post_processor_dsl.cpp`
      reconstructs under `--proof-rewrite-rcons-rec-limit` (default 5) and
      `--proof-rewrite-rcons-step-limit`; on failure the macro step *remains*
      and the proof is incomplete. Report every rewrite whose reconstruction
      depends on the budget. This is the deepest obstacle to the kernel and
      should be characterised early even though it cannot be fixed here.
- [ ] `RW0003` a theory rewriter path returning a rewritten node with no
      `ProofRewriteRule` tag reachable for it.

## M6 — proof API contracts (`API`)

The class of bug that is invisible in release builds.

- [ ] `API0001` a `ProofGenerator::getProofFor(f)` that can return a proof of
      something other than `f`.
- [ ] `API0002` **invariants nothing checks in a default run.**
      `ensureClosedWrtInternal` returns immediately unless
      `--proof-check=eager` is set or a trace is on — so in a default
      proof-producing run, **proof closedness is not checked at all**, and the
      `pfgEnsureClosed` calls scattered through the pipeline are inert. Same
      question for the pedantic-failure machinery and for invariants held only
      by `Assert`, which release builds compile out. Enumerate which proof
      invariants survive into a default run and which do not — that is the
      configuration users get.
- [ ] `API0003` `CDProof::addStep` with arguments the rule's checker would
      reject — a static arity/shape check against the ledger's column two.
- [ ] `API0004` a proof node constructed but never attached to a parent, or a
      generator registered for a fact nothing asks for.

## M7 — the kernel (`KRN`) — the stretch goal

> for every input in this fragment, under this configuration: if the kernel
> answers `unsat`, it emits a proof, every step of which `ethos` can check.

- [ ] **M7.1** A configuration language for *K*: logic fragment + option set +
      pinned revision.
- [ ] **M7.2** `KRN` obligation 1 — **closure**. Reachable code under *K*.
      Every unresolved indirect call is a recorded assumption, never a pass.
- [ ] **M7.3** Obligations 2–5 — coverage, admissibility, elaboration,
      agreement — as queries over M1–M5 restricted to the closure.
- [ ] **M7.4** Obligation 6 — reconstruction termination. Expected outcome: it
      *cannot* be discharged against today's code (see `RW0002`), and the
      deliverable is a proposal to make reconstruction inside the kernel
      syntax-directed rather than searched.
- [ ] **M7.5** The certificate: obligations discharged, assumptions standing,
      and the frontier — what would have to change to close each one. A kernel
      with three honest assumptions beats a green check hiding thirty.
- [ ] **M7.6** First target: `QF_UF`, default options. Then `QF_LIA`, then a
      theory at a time, each an increment that can be measured.

---

## Cross-cutting

- [ ] **Witnesses.** Every check owns a file that must be reported and, where
      the distinction is interesting, one that must not. For a solver analyzer
      a witness is a *cvc5 source excerpt* plus, for reachability claims, an
      SMT-LIB reproducer and an option set.
- [ ] **The oracle.** anoieu runs `ethos` on its witnesses. Ours is
      `cvc5 --check-proofs-complete` on the reproducer: a check claiming a hole
      is reachable is validated by a run that hits it. **The measure worth
      reporting is how many of our findings the runtime check does not already
      catch on cvc5's own regression suite** — that number is the argument for
      the tool.
- [ ] **CI.** Run over the pinned cvc5 on every push, so a change inventing a
      false positive fails our build. Then propose the ladder to cvc5, starting
      with the ledger regression: a commit that adds a rule with no checker, an
      `InferenceId` with no reconstruction, or a technique to
      `incompatibleWithProofs` with no note, fails in seconds.
- [ ] **Docs.** `docs/checks.md` generated from the registry;
      `docs/what-runtime-misses.md` as the counterpart to anoieu's
      `what-ethos-misses.md`, set out by mechanism; `docs/findings.md`;
      `docs/upstream.md`.
- [ ] **Handoff to anoieu.** A defined format for findings that turn out to be
      about the signature rather than the C++, so neither tool files the other's
      bugs.

---

## Candidate findings from this design pass

Noticed while reading cvc5 `16c4001e53`. **Unconfirmed — hypotheses, not
findings.** Each needs a reproducer or a maintainer's answer before it goes near
`docs/findings.md`, per the promise in the README.

| # | what | first check | why it might be nothing |
| --- | --- | --- | --- |
| c-1 | The 11 `FF_*` rules (incl. `MACRO_FF_POLY_COMBINATION`) are in the public enum and documented, have no registered checker, and have zero emission sites in `src/` — `src/theory/ff` is entirely `#ifdef CVC5_USE_COCOA` | `RULE0003`, `RULE0004` | may be deliberate: reserved for a CoCoA build whose proof support is planned. The question is whether the *public* enum should carry rules no build produces |
| c-2 | `EoPrinter::isHandled` is an allowlist of 135 case labels over 172 rules; the unhandled set has never been computed | `SEAM0001` | 172−135 is a naive subtraction, not a finding: labels are not distinct rules, some rules appear in several switches, and conditional arms make handledness argument-dependent. The point is that nobody knows the real number |
| c-3 | Proof completeness depends on `--proof-rewrite-rcons-rec-limit` / `-step-limit`: when reconstruction fails the macro step remains | `RW0002` | known and accepted engineering. Worth stating precisely because it bounds what any kernel contract can claim |
| c-4 | `incompatibleWithProofs` silently changes 8 solver options; the justifications are code comments with no test that they stay true | `MODE0001` | all 8 may be right today. The check is about the *next* one |
| c-5 | Only `strings`, `datatypes` and `sets` have an `infer_proof_cons.cpp`; the other proof-producing theories reconstruct elsewhere or not at all | `INFER0002` | other theories may attach generators at the inference site instead — needs the semantic tier to tell the two apart |
| c-6 | `TODO (wishue #154)`: Minisat with DRAT/LRAT throws no logic exception | `MODE0005` | already known upstream; track, do not re-file |
| c-7 | `ensureClosedWrtInternal` returns early unless `--proof-check=eager` or a trace is on, so a default `--produce-proofs` run never checks that its proofs are closed | `API0002` | deliberate: the check is expensive and CI runs eager mode. Worth stating because it decides what a *release* run guarantees, which is what a kernel contract is about |

## Open design questions

1. **How much clang do we need?** The table tier covers more than expected. Is
   the semantic tier better served by libclang, a clang plugin, or by asking
   cvc5 to *emit* the tables (a build target dumping the ledger as JSON)? The
   third is the least code here and the most useful upstream — and it turns a
   static analysis into an invariant cvc5 maintains itself.
2. **Where does reachability come from?** Call-graph closure is approximate and
   theory code is full of indirection. An alternative: instrument a cvc5 build
   to log which inference sites fire across a benchmark corpus, and use it as a
   *lower bound* on reachability to sharpen severity — dynamic evidence feeding
   a static claim, not replacing it.
3. **Is the ledger better upstream?** Several checks here are arguably things
   cvc5 should assert about itself at build time. If the answer is yes for a
   check, the finding is a patch to cvc5, not a permanent check here — and that
   is a success, not a loss of scope.
4. **What is the unit of a kernel?** Logic fragment, option set, or an explicit
   list of enabled solvers? The first is what users say; the third is what the
   analysis can actually close over.
