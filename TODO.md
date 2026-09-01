# The plan

The goal is [**complete proofs, always**](docs/goals.md).

**This file holds work *we* do**, and it is meant to stay short. Anything we ask
cvc5 to act on is in [`docs/issues.md`](docs/issues.md); the reasoning behind any
of it is in `docs/`; the catalogue of checks is
[`docs/checks.md`](docs/checks.md). A numbered section in a design note is a
named argument, not a task.

*Numbers below are measured against cvc5 `40a4bb7e4` unless stated.*

## What exists

Twelve subtools, dependency-free, reading a checkout with no build. Eight carry a
`baseline --check` ratchet.

| tool | answers | ratchet |
| --- | --- | --- |
| `tcb` | the proof checker's dependency closure, and what each edge costs | ✅ |
| `ledger` | one row per `ProofRule`: produced, checked, elaborated, printed | ✅ |
| `trust` | every `TrustId` construction site, and the preprocessing correspondence | ✅ |
| `inferid` | whether each `InferenceId` names one program point | ✅ |
| `infer` | whether every inference a theory makes has a proof reconstruction | ✅ |
| `rewrites` | the 533-rule rewrite vocabulary, RARE vs hand-written vs applied | ✅ |
| `modes` | what safe and stable mode change about the defaults | ✅ |
| `ci` | whether cvc5's proof testing is still attached | ✅ |
| `gates` | which option legalises each term kind, and so each rewrite rule | |
| `fragment` | the supported fragment per theory, and whether it is enforced | |
| `signature` | whether the Eunoia signature agrees with cvc5's account of a rule | |
| `latent` | static inventory − what a corpus reached = **the holes nothing has hit** | |

## What the analysis is for

Every tool exists to move one number. Not to enumerate — **to measure a gap
between what cvc5 promises and what it enforces, and to watch it close.** A check
producing a list nobody can act on, or a number nobody would notice moving, does
not belong.

Five groups. Each carries metrics and a short list of what is left.

---

## G1 — How many ways can a proof be incomplete?

*The direct measure. Everything else is instrumental to it.*

| metric | today | target |
| --- | --- | --- |
| `ProofRule`s emitted that the Eunoia seam refuses | **14** — 13 behind `--arith-exp`, plus `SAT_REFUTATION` | 0 reachable in safe mode |
| rewrites applied but unprintable | **40** — 38 macro, 2 hard, all blocked in safe mode | 0 reachable in safe mode |
| rewrites the seam takes **only** outside safe mode | **3** — one (`LAMBDA_ELIM`) not otherwise blocked | 0 |
| `TrustId`s constructible | **70 of 75 live** | ranked by safe-mode reachability |
| inferences falling through to a trust step by construction | **79** | ranked by reachability |
| **of that inventory, what any input has reached** | **[0 in safe mode, 21 of 203 unrestricted](docs/reachability.md)** | the latent set, named |
| **the latent count** — declared, never reached | **182 of 203** (`latent census`) | shrinking, either way it goes |

**Left to do:** work the 182 down (`t-3`). The count is the headline number and
it should move in either direction — an input promotes a hole to a finding, an
unreachability argument removes it from the inventory.

**What cvc5 can do:** close the holes (`i-7`, `i-18`); declare which seam
refusals are intentional (**R1**, **R6**).

---

## G2 — How much of cvc5 must be right?

| metric | today | target |
| --- | --- | --- |
| the internal checker's compile-time surface | **179 files, 41,446 lines, 8.0% of `src/`** | smaller, and not growing |
| rule checkers over-scoped by a solver include | **6** ([`tcb-001`](docs/findings/tcb-001.md)) | 0 |

**Left to do:** nothing queued. The kernel obligations
([`docs/kernel.md`](docs/kernel.md)) stay parked behind `i-4` — reconstruction
runs under a search budget with no termination argument, which bounds what any
kernel contract can claim.

**What cvc5 can do:** **R3** — extract the pure `static` helpers out of solver
classes.

---

## G3 — Can we quantify over the entities at all?

*Nameability. Every other analysis is imprecise by exactly the amount this one
is.*

| metric | today | target |
| --- | --- | --- |
| `InferenceId`s produced at exactly one site | **346 of 411 (84%)** | 100% |
| `InferenceId`s produced nowhere | **14** | 0 |
| trust steps built with `TrustId::NONE` | **8** | 0 |
| dead `PREPROCESS_*` ids | **3** | 0 |
| pass↔`TrustId` names not derivable | **7**, incl. `PREPROCESS_BV_GUASS` | 0 |
| theories emitting inferences with no `InferProofCons` | **10** | *unknown by this mechanism* — needs the call site |

**Left to do:** `INFER0001` (a lemma sent with a null `ProofGenerator`) and the
rest of G3's precision need the call site, which is the AST tier — deferred
until **R1** has been asked for.

**What cvc5 can do:** **R4** (one id, one site), **R7** / **R7b** (derivable
names), **R10** (rule on [the hygiene standard](docs/hygiene.md)).

---

## G4 — Does safe mode do what it says?

*The contract, and the one place cvc5 has already made a promise we can hold it
to.*

| metric | today | target |
| --- | --- | --- |
| options declaring no proof support that safe mode leaves on | **1** (`stringLazyPreproc`; `macrosQuantMode` is [spurious](docs/issues.md#settled)) | 0 |
| completeness chain links that hold | **4 of 5** — and the fifth [cannot be stated](docs/issues.md) in safe mode at all | 5, asserted |
| build-matrix jobs running a proof tester | **4 of 22** | — |
| term kinds carrying an option gate | **59** | — |
| the supported fragment | **341 kinds over 14 theories**; 216 available, 125 blocked | stated somewhere |
| expert options gating no term kind | **2** (`ufHoExp`, `fpExp`) — the axis a kind list cannot express | — |
| **holes reached in safe mode over `regress0`** | **[0, over 1,061 proofs](docs/reachability.md)** | stays 0 |

**Left to do:** `t-1` (an input for `i-1`) and `t-5` (per-logic breakdown).

**What cvc5 can do:** **R2** (assert the completeness implication — [the next
thing we would report](docs/next-report.md)), **R5** (`no_support` covers
defaults), **R8** (safe mode prunes at build time).

---

## G5 — Is completeness a property of the code, or of a budget?

| metric | today | target |
| --- | --- | --- |
| RARE rules vs hand-written | **439 / 94** of 533 | — |
| theories enabled in safe mode with no RARE rules | **2** — `datatypes`, `quantifiers` | — |
| the RARE↔C++ correspondence | established **only by runtime search** (`i-17`) | tested |

**Left to do:** nothing we can build. `i-4` is the standing limit: reconstruction
runs under `--proof-rewrite-rcons-rec-limit` with no termination guarantee, and
nothing short of a termination argument settles it.

**What cvc5 can do:** **R9** — test each RARE rule against the rewriter.

---

## The queue

Everything above that is not on this list is context, not a queue.

| | | why |
| --- | --- | --- |
| **t-1** | **Get an input for `i-1` (`LAMBDA_ELIM`).** | The only candidate that could become a rank-1 finding, and static work cannot settle it. **One attempt has failed** — a plain `define-fun` runs clean in safe mode; the macro is expanded before the rewriter. Needs a benchmark that keeps a lambda alive. Treat [`s-6`](docs/issues.md#settled) as the cautionary case |
| **t-2** | **Re-run the corpus census on a clean upstream build.** | [The census](docs/reachability.md) was produced by a binary built from `ajreynol/CVC4` with local modifications, so it is the one set of numbers a reader cannot re-check by fetching the pin. Listed as a debt in `tools/cvc5.lock`, and it needs a build we do not have |
| **t-3** | **Work the latent set down.** | `dokimasia.latent` now names **182 holes no input has reached**. Each needs an input (it becomes a finding) or an unreachability argument (it leaves the inventory). Start with the 5 latent seam rules — `SAT_REFUTATION` is the one that is not arith |
| **t-4** | **Carry `i-3`/`R2` and `i-2` to cvc5.** | The two rows that [clear the bar](docs/pr-policy.md#the-bar). `i-3`: the completeness flag cannot be set in the mode that promises it. `i-2`: safe mode refuses `--strings-lazy-pp` *because it lacks proof support*, then runs with it on. Both are one command to check and a one-line call to fix — see [the verdicts](docs/next-report.md) |

Deferred until **R1** has been asked for, because R1 would retire most of what
they are for: the AST tier (`API0001`–`0004`, `INFER0001`), `SEAM0002` (the
unhandled *argument* set of the conditional arms), `ELAB0002`/`0003`
(granularity is a runtime property).

## Standing

- **One command.** `python3 -m dokimasia check <cvc5>` runs every ratchet in a
  single process, reading `src/` once instead of once per tool: **2.4s, down
  from 7.4s**. `report` prints every analysis; `write` re-records baselines.
- **Ratchets, in CI.** Eight tools carry `baseline --check`. `.github/workflows/checks.yml`
  runs the whole suite and every ratchet on each push, against the commit
  [`tools/cvc5.lock`](tools/cvc5.lock) pins. Re-run the corpus census per cvc5
  release, not per change.
- **The pin must be upstream.** Every published number names a commit on
  `cvc5/cvc5 main`, so anyone can fetch it and re-check us. `tests/test_pin.py`
  fails if a document quotes a commit the lock does not account for. Numbers
  that genuinely cannot be taken at the pin — a runtime measurement needs a
  build — are listed as debts in the lock, with a reason.
- **A finding is confirmed before it is filed**, and for a defect that means an
  input ([`docs/findings.md`](docs/findings.md)).
- **A false positive is our bug**, including a retracted number and a fabricated
  baseline entry — the logs are
  [`issues.md#settled`](docs/issues.md#settled) and
  [`findings.md#retractions`](docs/findings.md#retractions).
- **We never open a pull request or an issue.**
  [`docs/pr-policy.md`](docs/pr-policy.md).
- **Prefer the claim a maintainer can refute in one command.** Of the recent
  things we got wrong, every one was a static argument that read correctly and
  was false, and every one was caught by running something.

## Deliberately not doing

- **Fuzzing.** [murxla's job](docs/tooling.md#posture-toward-murxla). What we can
  contribute is a fragment description — *a hole here needs a formula with these
  features* — not a fuzzer.
- **Alethe.** Not on the critical path and not available in safe mode, so it
  cannot bear on the contract.
- **A diagnostic/SARIF framework and a generated check registry.** Modelled on
  anoieu and never needed: `docs/checks.md` is written by hand and is accurate,
  and the check-code namespace is not currently carrying weight — most tools
  answer their question without printing a code. Revisit if we ever ask cvc5 to
  run our checks in their CI (**R11**), which is when a machine format matters.
- **A `holes/` regression corpus**, until there is a hole to put in it. Safe mode
  reaches none.
- **An AST tier**, until the table tier is exhausted and **R1** has been asked
  for.
- **Network access on any analysis path.** An analysis whose result depends on
  when it ran is not a measurement, and a check that can fail on a slow network
  is a check people switch off.
