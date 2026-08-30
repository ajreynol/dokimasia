# Issues

Everything dokimasia currently believes about cvc5, in one place. **These are
hypotheses, not filed findings** — a finding is confirmed and lives in
[`findings.md`](findings.md); this is what is waiting for a verdict.

Ranks, from [`tooling.md`](tooling.md#d5--safe-mode-first-and-the-reproducer-is-the-deliverable):
**1** an incomplete proof under `--safe-mode=safe` — a contract violation, needs
an input · **2** a hole reachable in safe mode, no input yet · **3** a gap in
stable or unrestricted, or a cleanup · **—** a process point, not a defect.

## Open — rank 2

The ones worth someone's attention.

| # | what | found by | what would settle it |
| --- | --- | --- | --- |
| **i-1** | **`LAMBDA_ELIM` may be a genuine safe-mode gap.** *(Strengthened: the fragment analysis finds **no `uf` kind blocked in safe mode at all** — `ufHoExp` gates the declared logic, not `Kind::LAMBDA`, so a lambda reaching the rewriter is not excluded by kind.)* The seam accepts it only when `safeMode == UNRESTRICTED`, `TheoryUfRewriter::rewriteViaRule` applies it, and its arm fires on `Kind::LAMBDA`, which no gate blocks in safe mode | `gates rule` | **an input.** A `define-fun` benchmark under `--safe-mode=safe --produce-proofs --check-proofs`. `canEliminateLambda` may only succeed in HOL cases, which `ufHoExp` gates — static work cannot tell |
| **i-2** | **`stringLazyPreproc` escapes safe mode's promise.** It declares `no_support = ["proofs"]`, defaults to `true`, and neither `setDefaultsPre` nor the `SolverEngine` guard turns it off — that guard fires when a user *sets* an option, never on a default | `modes check` | a maintainer's answer. Either safe mode should disable it, or the annotation is stale. Cheapest possible settlement |
| **i-3** | **Proof completeness is never named in cvc5's CI.** `--check-proofs-complete` appears nowhere; in a safe build `setDefaultsPre` enables it as a side effect of `--check-proofs`. Four links, none asserted; adding a `--proof-granularity` flag to the `proof` tester would switch it off silently | `ci proofs` | confirmation that the chain is what keeps it on, then a one-line patch naming the flag |
| **i-4** | **Completeness depends on a search budget, and the budget is load-bearing.** Reconstruction runs under `--proof-rewrite-rcons-rec-limit` (default 5); when it fails the step stays coarse. This is **not a tuning knob on a decidable procedure** — [FMCAD 2022 §IV-A](rare-correspondence.md) states there is *"no guarantee that preconditions are simpler than the current equality to be proved, and so no guarantee of termination in general."* The paper measured 92–95% of rewrite *steps* reconstructed but only **20–22% of proofs fully fine-grained**, since one coarse step spoils a proof | `rewrites gaps` | nothing settles this short of a termination argument for the recursion. It bounds what any kernel contract can claim, and it is the strongest reason [obligation 6](kernel.md) cannot be discharged today |
| **i-5** | **The safe-mode disable list is hand-maintained and untested.** Nothing checks that it still covers every feature without proof support | `modes delta` | not a defect today — the check exists to catch the *next* feature added |
| **i-15** | **The supported fragment is not expressible as a list of kinds.** Two expert options safe mode disables gate no term kind: `ufHoExp` restricts the declared *logic* (`logicInfo().isHigherOrder()`), `fpExp` restricts a *type* (via `checkForExperimentalFloatingPointType`, whose sort has kind `TYPE_CONSTANT` and cannot be excluded by kind). So any statement of the form "safe mode supports exactly these kinds" is incomplete, and `illegal_checker`'s kind deny list cannot be the whole story | `fragment check` | a decision on whether the fragment should be *stated* somewhere — the three mechanisms are each reasonable, but nothing writes down what they add up to |
| **i-17** | **The RARE↔C++ correspondence is established only by runtime search.** A RARE rule that misstates the rewrite never matches and is never reported; a rewrite with no rule, and a rule the search fails to find in budget, produce the same trust step and so cannot be told apart. Nothing checks the 439 declarations against the rewriter that implements them | design note | see [`rare-correspondence.md`](rare-correspondence.md). E1 (instantiate each rule, run the rewriter) is the direct test and belongs upstream |
| **i-18** | **`datatypes` and `quantifiers` have no RARE rules at all**, and both are enabled in safe mode. Every rewrite they perform must reconstruct through a hand-written `ProofRewriteRule` or become a trust step | `rewrites correspondence` | where reconstruction failure is structurally concentrated. Worth a corpus read before assuming it bites |
| **i-6** | **Only `strings`, `datatypes` and `sets` have an `infer_proof_cons.cpp`.** The other proof-producing theories reconstruct elsewhere or not at all | — | the `INFER` analysis, which does not exist yet |

## Open — rank 3

Cleanups and unrestricted-mode gaps. Real, but nobody is relying on them.

| # | what | found by |
| --- | --- | --- |
| i-7 | **14 `ProofRule`s the solver emits, the seam cannot print**: 4 `ARITH_POW2_*`, 9 `ARITH_TRANS_*`, `SAT_REFUTATION`. The arith ones are behind `--arith-exp`; the `ARITH_POW2_*` four are *also* registered trusted at pedantic level 1. `SAT_REFUTATION` is the one that is not arith and wants its own answer | `ledger holes` |
| i-8 | **51 `InferenceId`s are produced at more than one site**, 14 are produced nowhere, and 21 inferences are emitted with a sentinel id. Not defects; they are what makes an inference-coverage analysis imprecise | `inferid check` |
| i-9 | **8 trust steps are built with `TrustId::NONE`** — a declared hole with no stated reason, so nothing downstream can attribute them | `trust census` |
| i-10 | **3 `PREPROCESS_*` trust ids are dead**: both `bv_to_int` ids and `PREPROCESS_BITVECTOR_EAGER_ATOMS`. That pass's actual trust step is `INT_BLASTER`, built in a different file | `trust passes` |
| i-11 | **The pass↔trust-id correspondence is not derivable by name.** 7 ids do not follow their pass filename, including `PREPROCESS_BV_GUASS` — a misspelling of Gauss | `trust passes` |
| i-16 | **The RARE↔enum correspondence is exact but under-stated.** The generated marker names the rule, not its file, so a rule's owning theory is not recoverable from the header; hand-written entries are identified only by *absence* of a marker; RARE files carry six basenames and no extension; and the `ite-` prefix is claimed by both `booleans` and `builtin` | `rewrites correspondence` |
| i-12 | **11 `FF_*` rules** are in the public enum and documented, have no registered checker, and nothing produces them — `src/theory/ff` is entirely `#ifdef CVC5_USE_COCOA` | `ledger holes` |
| i-13 | **Proof closedness is never checked in a default run.** `ensureClosedWrtInternal` returns early unless `--proof-check=eager` or a trace is on, so the `pfgEnsureClosed` calls through the pipeline are inert in the configuration users get | — |
| i-14 | **`--proof-check=lazy` in CI's proof tester** means closedness is not checked there either | `ci proofs` |

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
| s-5 | The proof checker's TCB is 74% of `src/` | **retracted.** An artifact of a saturating closure mode; the real figure is 8.0%. See [retractions](findings.md#retractions) |

## Filed

| # | what | where |
| --- | --- | --- |
| f-1 | Six proof rule checkers compile against the theory solvers they check, to reach `static` helpers parked on solver classes | [`tcb-001`](findings/tcb-001.md) |
