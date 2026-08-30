# How this ships

A survey of domain-independent C++ static analysis, what cvc5 already runs, and
the design decisions that follow. The conclusion up front, because it is not the
one this document set out to reach:

> **cvc5 has already built the analyzer architecture dokimasia needs, and runs
> it nightly.** The right move is to add checks to it, not to build a second
> tool beside it.

## What cvc5 already runs

Measured at `16c4001e53`.

[`.github/workflows/static_analysis.yml`](https://github.com/cvc5/cvc5/blob/main/.github/workflows/static_analysis.yml)
is a **nightly** job (`cron: '0 4 * * *'`, plus `workflow_dispatch`) that does
something more interesting than run a linter:

1. builds a **custom clang-tidy plugin** from
   [`contrib/tidy-checks/`](https://github.com/cvc5/cvc5/tree/main/contrib/tidy-checks)
   → `Cvc5TidyChecks.so`, registering checks under a `cvc5-*` namespace;
2. builds cvc5 with `./configure.sh production --auto-download --assertions`
   inside a **CodeQL database**;
3. runs a **custom CodeQL query**
   ([`contrib/codeql/IdentifyNodeIdDependentCalls.ql`](https://github.com/cvc5/cvc5/blob/main/contrib/codeql/IdentifyNodeIdDependentCalls.ql))
   that computes a transitive call-graph closure from two "minting point"
   functions, and decodes it to **CSV**;
4. runs `run-clang-tidy` with the plugin loaded and **the CSV passed in as a
   check option**, `-warnings-as-errors "*"`.

Read step 3 and 4 together. That is the answer to the hardest question in this
project, already implemented: **CodeQL answers the whole-program reachability
question; a clang-tidy check consumes the answer and makes local, per-site
judgements with it.** Neither tool can do the job alone. The existing check,
`cvc5-node-id-determinism`, is a *domain* invariant — not a language defect —
enforced by exactly that pairing, and it emits suggested fixes.

dokimasia's checks have the same shape. "Which functions can reach an inference
site with no proof generator, under safe mode" is the same query as "which
functions transitively mint a NodeId," with a different set of roots.

Also present: `.clang-tidy` (enabling `cvc5-*` plus a small set of `modernize-*`
checks, `HeaderFilterRegex: '.*'`), and `cmake/IWYU.cmake` for
include-what-you-use. cvc5's functional CI builds with `--assertions --tracing`.

**The gap in the existing setup**: results are enforced via
`-warnings-as-errors` and nothing else. There is no `upload-sarif` step, so
findings do not appear in GitHub's code-scanning UI, are not annotated inline on
pull requests, and have no baseline or suppression mechanism. That is a
recommendation we can make cheaply and independently of any check we write.

## The survey

The question each tool answers, and whether it is ours.

### Compiler-based, AST-level

| tool | what it does | for us |
| --- | --- | --- |
| **clang-tidy** | AST matchers per translation unit, custom checks as a loadable module, fix-it emission | **Yes — the delivery vehicle.** cvc5 already loads a custom module; adding `cvc5-proof-*` checks costs the project no new infrastructure |
| **Clang Static Analyzer** | path-sensitive symbolic execution within a TU, custom checkers via plugin | Useful for one narrow family (`API` — can a generator return a proof of the wrong fact on some path). Cross-TU mode is fragile at cvc5's size |
| **CodeChecker** | driver over CSA + clang-tidy, adds a results server, baselines, suppression, SARIF | Worth recommending if cvc5 wants baselines without building them; competes with plain SARIF upload |
| **include-what-you-use** | header hygiene | Not ours. Already wired up |

### Query and database

| tool | what it does | for us |
| --- | --- | --- |
| **CodeQL** | relational DB from a build; declarative QL with global dataflow and call-graph libraries; native SARIF; free for open source | **Yes — the closure engine.** Already in the tree, already in the nightly, already producing a call-graph closure for another check |
| **Joern** | code property graph, queryable without a full build | No reason to add it; CodeQL is already here and has the stronger C++ front end |
| **Semgrep** | fast syntactic and shallow-semantic patterns, no build required | Plausible alternative for the *ledger* tier. Rejected: our table reading is bracket-matching over enums and `switch` bodies, which is less code as a direct parser than as Semgrep rules, and it keeps the tier dependency-free |

### Abstract interpretation and whole-program

| tool | what it does | for us |
| --- | --- | --- |
| **Infer** | separation logic, incremental, strong on nullability and leaks | Not ours — its bug classes are language-level, and its C++ front end is the weakest part of it |
| **SVF** | LLVM-based pointer analysis and value-flow, as a library | A fallback if CodeQL's call graph proves too imprecise for the kernel closure. Not a starting point |
| **IKOS** | abstract interpretation over LLVM | Same |
| **Cppcheck** | pattern-based, no build needed | Ceiling too low |
| **Frama-C** | C only | Rules itself out |
| **Coverity / PVS-Studio / SonarQube / Klocwork** | commercial, broad defect classes | Not extensible to a project-specific contract, which is the only thing we care about |

### Verification-grade, for the kernel stretch goal

| tool | what it does | for us |
| --- | --- | --- |
| **CBMC / ESBMC** | bounded model checking of C/C++ | The only realistic candidate for discharging a kernel obligation *mechanically*, and only over a small extracted component |
| **VeriFast / VCC** | separation-logic verifiers, annotation-heavy | Would require annotating cvc5. Out of proportion to the goal |
| **Why3, Frama-C WP** | deductive verification, C only | Not applicable |

**The honest read for M7:** verifying the contract over cvc5's actual C++ is not
on the table with today's tools. The kernel is reached by *restricting* the code
until the contract is checkable — closure, coverage, admissibility — and by
converting the residue into assertions and exhaustive tests. A certificate with
stated assumptions, not a machine-checked theorem.

## The positioning

**None of these tools can ask our question, and that is not a deficiency in
them.** Domain-independent analyzers look for *language-level* defects:
undefined behaviour, null dereference, leaks, unsequenced writes. Every finding
dokimasia is after is **perfectly well-formed C++** that violates a contract
only cvc5 states — an `InferenceId` with no reconstruction case, a `ProofRule`
the Eunoia seam cannot print, a technique reachable in safe mode with no proof
support.

So the tools are **infrastructure, not analyzers**. We supply the invariant;
clang gives us an AST and a fix-it mechanism; CodeQL gives us a call graph. The
value is entirely in knowing which invariant to state — which is why the
research goal stays narrow.

## Design decisions

### D1 — Three artifacts, by what each question needs

| tier | question | artifact | cost to run |
| --- | --- | --- | --- |
| **0 — ledger** | is this table consistent with that table? | standalone Python, reads a checkout | **seconds, no build** |
| **1 — local** | does this call site attach a proof? | `cvc5-proof-*` checks in `contrib/tidy-checks/` | one clang-tidy pass |
| **2 — closure** | what can safe mode reach? | `.ql` queries in `contrib/codeql/` | one CodeQL DB build |

Tier 0 is deliberately not a clang tool. The rule ledger, the trust census, the
safe-mode delta and the seam coverage are all *table against table* — enums,
registries, `switch` bodies, `.toml` option definitions. Reading them needs a
bracket matcher, not a compiler, and the resulting check runs on every push
rather than nightly. It also means the project produces findings before anyone
has to configure a build.

Tiers 1 and 2 go **upstream, into cvc5's tree**, because that is where the
pipeline already is. A tool cvc5 has to install and schedule will not be run; a
check in `contrib/tidy-checks/` is already built, loaded and enforced by a job
that exists.

### D2 — Recommend SARIF regardless of anything we write

`run-clang-tidy` → SARIF → `github/codeql-action/upload-sarif`. Findings then
annotate pull requests inline, get a baseline, and get dismissal-with-reason.
This is worth filing on its own; it is the difference between a nightly that
fails loudly and a nightly whose output someone reads.

### D3 — Where an invariant should live

Not every finding should become a check here. The cheapest enforcement that
actually holds is the right one, and the order is:

| if the invariant is… | it belongs as… | who maintains it |
| --- | --- | --- |
| decidable from types or constants at compile time | `static_assert` | cvc5, free, forever |
| decidable from cvc5's own tables at startup | an **assertion** in the registry that builds the table | cvc5, free, forever |
| a property of one function's AST | a `cvc5-proof-*` tidy check | cvc5, one nightly pass |
| a property of the whole call graph | a CodeQL query feeding a tidy check | cvc5, one nightly pass |
| only observable on an input | a corpus run with `--check-proofs-complete` | us |

**A check here that could have been an assertion in cvc5 is a design failure**,
not a feature. If `ProofChecker` can assert at registration time that every
`ProofRule` it is asked about has a checker, that invariant is enforced on every
developer's machine forever, and dokimasia should delete the corresponding
check and keep only the patch that introduced it.

Two facts make assertions more attractive here than they look. cvc5's `Assert`
compiles out unless `CVC5_ASSERTIONS` — but **the nightly static-analysis build
and the functional CI builds both configure `--assertions`**, so a recommended
`Assert` is genuinely enforced across cvc5's test suite. And `AlwaysAssert`
exists for the handful of invariants cheap enough to hold in production.

### D4 — We own the assertions we suggest

Same promise as a false positive, because it is the same failure: **if an
assertion we recommend fires spuriously in cvc5, that is our bug.** The practical
consequence is a hard precondition on the finding category:

> No assertion is proposed until it has been applied to a cvc5 build configured
> `--assertions` and the regression suite has passed with it in place.

An assertion we have not run is a hypothesis about cvc5's invariants, and
hypotheses go in `docs/findings.md`, not in a patch.

### D5 — Safe mode first, and the reproducer is the deliverable

See [the contract](../README.md#the-contract). `--safe-mode=safe` is the only
configuration cvc5 promises complete proofs in, so it is the only configuration
where an incomplete proof is a **contract violation** rather than a known gap.

Findings are ranked accordingly, and the rank is part of the finding:

| rank | what it is | evidence required |
| --- | --- | --- |
| **1** | safe mode produces an incomplete proof | **an input.** `.smt2` file, option set, quoted `--check-proofs-complete` failure |
| **2** | a hole reachable in safe mode, no input yet | the static argument, plus what fragment an input would need |
| **3** | a gap in stable or unrestricted | the static argument; filed as a roadmap item, not a bug |

Rank 1 is what we are for. The static analysis exists to make the search for
rank-1 inputs *targeted* — without it, finding these is running benchmarks and
hoping.

### D6 — The reproducer pipeline

Static hypothesis → corpus run under
`--safe-mode=safe --produce-proofs --check-proofs` → minimize with
[`ddsmt`](https://github.com/ddsmt/ddsmt) → attribute the failure back to the
site the analysis predicted → file with the input attached.

The last step is the one that closes the loop and the one worth measuring: **a
prediction that was confirmed by an input is the only evidence that a check is
worth running.** The headline number for this project is how many rank-1 inputs
it produced that cvc5's regression suite does not already contain.

### D7 — Performance budget

Tier 0 must stay under a few seconds so it can run per-push as a lint. Tiers 1
and 2 inherit the nightly's budget, which already absorbs a full CodeQL database
build. Nothing here needs a new machine.

## Posture toward murxla

[murxla](https://github.com/murxla/murxla) is an end-to-end, black-box fuzzer
for SMT solvers. It is already an `ExternalProject` in cvc5's build
(`cmake/fuzzing-murxla.cmake`), pinned and maintained by people who are good at
it. **It is a separate project and we should keep it that way.**

The division is not about quality, it is about method:

| | murxla | dokimasia |
| --- | --- | --- |
| **method** | black box — generate inputs, run the solver, check an oracle | white box — read the C++ |
| **finds a hole by** | *hitting* it | *reading* it |
| **needs** | a build, and time | a checkout, and seconds |
| **can say** | "this input breaks it" | "this code path has no proof, and nothing has ever run it" |
| **cannot say** | anything about a path its inputs never reach | with certainty that a path is reachable |

Those last two rows are the whole relationship, and they are complementary
rather than competitive. Safe mode already has almost no proof holes on SMT-LIB,
so the holes that remain are the ones **no input has reached** — which is
exactly what a black-box tool cannot find and a white-box tool can. Symmetrically,
we can point at a suspicious path and be wrong about whether anything reaches it;
an input settles that and we cannot manufacture one by reading.

**So we do not build, wrap, drive or vendor a fuzzer.** Concretely:

- no fuzzing harness in this repository, and no dependency on murxla;
- we do not measure ourselves in bugs-found-by-fuzzing;
- when a static finding needs a witness input, the honest options are to
  construct one by hand or to hand the *fragment description* to whoever runs
  the fuzzing — "this hole needs a formula with these features" is a useful
  thing to give someone, and it is the right size of contribution;
- if murxla finds a proof hole, it lands in our `holes/` corpus as a regression
  and as evidence about a code site, which is data we consume, not work we did.

The one thing we should actively want from that direction is the *negative*
information: a hole murxla has never produced, in code we believe is reachable,
is the most interesting object either tool produces.

## What we are not doing

- **Not building a general C++ analyzer.** Every check is a statement about
  cvc5's proof pipeline; if a check would be useful to a project that is not
  cvc5, it is probably in the wrong repository.
- **Not replacing `--check-proofs-complete`.** It is the oracle. We are the
  thing that decides where to point it.
- **Not building a fuzzer.** See the posture above.
- **Not analyzing Eunoia signatures.** `anoieu` does that, better.
