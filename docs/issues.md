# Issues

**Everything we are asking cvc5 to act on.** Defects we believe exist, changes we
would like made, and process suggestions — one register, one ID space.

## Where work lives

Two registers, split by who acts. Everything else is rationale.

| | holds | ids |
| --- | --- | --- |
| [`../TODO.md`](../TODO.md) | **work we do** — tools to build, analyses to run | stages `A`–`F`, backlog `M0`–`M7` |
| **this file** | **things cvc5 would act on** — defects, asks, process | `i-*` defects, `R*` asks, `p-*` process |
| everything in `docs/` | **rationale** — why, not what | section names for reference only |

The rule: *if someone is expected to do something about it, it is in one of the
two registers.* A numbered section in a design document — `H1`–`H11` in
[`hygiene.md`](hygiene.md), `E1`–`E4` in
[`rare-correspondence.md`](rare-correspondence.md), `D1`–`D7` in
[`tooling.md`](tooling.md) — is a named argument, not a task. Where such a
section implies an action, it has a row here that links back to it.

**These are hypotheses, not filed findings** — a finding is confirmed and lives
in [`findings.md`](findings.md); this is what is waiting for a verdict.

Ranks, from [`tooling.md`](tooling.md#d5--safe-mode-first-and-the-reproducer-is-the-deliverable):
**1** an incomplete proof under `--safe-mode=safe` — a contract violation, needs
an input · **2** a hole reachable in safe mode, no input yet · **3** a gap in
stable or unrestricted, or a cleanup · **—** a process point, not a defect.

## Open — rank 2

The ones worth someone's attention.

| # | what | found by | what would settle it |
| --- | --- | --- | --- |
| **i-1** | **`LAMBDA_ELIM` may be a genuine safe-mode gap.** *(Strengthened: the fragment analysis finds **no `uf` kind blocked in safe mode at all** — `ufHoExp` gates the declared logic, not `Kind::LAMBDA`, so a lambda reaching the rewriter is not excluded by kind.)* The seam accepts it only when `safeMode == UNRESTRICTED`, `TheoryUfRewriter::rewriteViaRule` applies it, and its arm fires on `Kind::LAMBDA`, which no gate blocks in safe mode | `gates rule` | **still an input, and one attempt has failed.** `(define-fun f ((x Int)) Int (+ x 1))` with an assertion over `f` runs clean under `--safe-mode=safe --produce-proofs --check-proofs --stats-internal`: `unsat`, no unhandled rule, no trust step. That is evidence, not a settlement — the macro is expanded in preprocessing and `LAMBDA_ELIM` may simply not have fired. A benchmark that keeps a lambda alive to the rewriter is the open task. Note `--check-proofs-complete` cannot be passed here (see `i-3`); `--stats-internal` is the route |
| **i-2** | **`stringLazyPreproc` escapes safe mode's promise — and safe mode says so itself.** It declares `no_support = ["proofs"]`, `default = "true"`, `category = "regular"`; `setDefaultsPre` only *reads* it, never disables it. **Verified by running:** `--safe-mode=safe --strings-lazy-pp` is refused with *"cannot set option strings-lazy-pp in safe mode, as this option does not support proofs"* — so safe mode refuses to let you set the option on the grounds that it lacks proof support, while running with it on by default. `--no-strings-lazy-pp` is refused too, so the guard also blocks the one assignment that would make the configuration safer | `modes check`, then run | **verdict: carry.** Clears all five rules. Falsified if a maintainer says the `no_support` annotation is stale — which is itself the answer we want |
| **i-3** | **Proof completeness cannot be named in the mode that promises it.** `--check-proofs-complete` appears nowhere in CI; in a safe build `setDefaultsPre` enables it as a side effect of `--check-proofs`. **It also cannot be passed there:** the option is `category = "expert"`, and safe and stable mode reject expert options — verified by running it. So the side effect is not a convenience, it is the only route, and adding a `--proof-granularity` flag to the `proof` tester would switch it off silently | `ci proofs`, then run | an assertion in `setDefaultsPre` stating the implication (**R2**), which is a [kind D](findings.md) and retires our check |
| **i-4** | **Completeness depends on a search budget, and the budget is load-bearing.** Reconstruction runs under `--proof-rewrite-rcons-rec-limit` (default 5); when it fails the step stays coarse. This is **not a tuning knob on a decidable procedure** — [FMCAD 2022 §IV-A](rare-correspondence.md) states there is *"no guarantee that preconditions are simpler than the current equality to be proved, and so no guarantee of termination in general."* The paper measured 92–95% of rewrite *steps* reconstructed but only **20–22% of proofs fully fine-grained**, since one coarse step spoils a proof | `rewrites gaps` | nothing settles this short of a termination argument for the recursion. It bounds what any kernel contract can claim, and it is the strongest reason [obligation 6](kernel.md) cannot be discharged today |
| **i-5** | **The safe-mode disable list is hand-maintained and untested.** Nothing checks that it still covers every feature without proof support | `modes delta` | not a defect today — the check exists to catch the *next* feature added |
| **i-15** | **The supported fragment is not expressible as a list of kinds.** Two expert options safe mode disables gate no term kind: `ufHoExp` restricts the declared *logic* (`logicInfo().isHigherOrder()`), `fpExp` restricts a *type* (via `checkForExperimentalFloatingPointType`, whose sort has kind `TYPE_CONSTANT` and cannot be excluded by kind). So any statement of the form "safe mode supports exactly these kinds" is incomplete, and `illegal_checker`'s kind deny list cannot be the whole story | `fragment check` | a decision on whether the fragment should be *stated* somewhere — the three mechanisms are each reasonable, but nothing writes down what they add up to |
| **i-17** | **The RARE↔C++ correspondence is established only by runtime search.** A RARE rule that misstates the rewrite never matches and is never reported; a rewrite with no rule, and a rule the search fails to find in budget, produce the same trust step and so cannot be told apart. Nothing checks the 439 declarations against the rewriter that implements them | design note | see [`rare-correspondence.md`](rare-correspondence.md). E1 (instantiate each rule, run the rewriter) is the direct test and belongs upstream |
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
| i-16 | **The RARE↔enum correspondence is exact but under-stated.** The generated marker names the rule, not its file, so a rule's owning theory is not recoverable from the header; hand-written entries are identified only by *absence* of a marker; RARE files carry six basenames and no extension; and the `ite-` prefix is claimed by both `booleans` and `builtin` | `rewrites correspondence` |
| **i-21** | **`SUBS`'s documentation omits an argument the checker reads.** The doc says `\inferrule{F_1 \dots F_n \mid t, ids?}` — one required argument plus an optional `ids`. The checker asserts `1 <= args.size() && args.size() <= 3` and reads `args[2]` as a second `MethodId` (`ida`, defaulting to `SBA_SEQUENTIAL`), which selects how the substitution is *applied*. Nothing in the documentation mentions it | `signature checker` |
| i-19 | **24 `SkolemId`s are constructed by the solver and refused by the Eunoia seam.** A skolem the seam cannot print sinks a proof exactly as an unprintable rule does. Most are bags/sets/relations/transcendental — safe mode disables those — but `GROUND_TERM`, `BV_TO_INT_UF` and `SHARED_SELECTOR` want checking | `signature skolems` |
| i-20 | **The `\inferrule` documentation is prose, not a specification.** Comparing it against the *checker* took five rounds of parser fixes (10 → 3 → 2 → 3 → 1 disagreements) as LaTeX conventions were accounted for: dots inside a conjunction, `\,` thin spaces, bare ellipses between listed premises, and `DSL_REWRITE` alone separating its arguments with spaces rather than commas. The residue is one real finding (`i-21`). **The docs are readable by people and barely by machines**, which is why nothing checks them. cvc5 states a rule's arity in LaTeX only — unlike `SkolemId`, which states "Number of skolem indices: N" in a structured field and is checkable directly | `signature arity`, `signature checker` |
| i-12 | **11 `FF_*` rules** are in the public enum and documented, have no registered checker, and nothing produces them — `src/theory/ff` is entirely `#ifdef CVC5_USE_COCOA` | `ledger holes` |
| i-13 | **Proof closedness is never checked in a default run.** `ensureClosedWrtInternal` returns early unless `--proof-check=eager` or a trace is on, so the `pfgEnsureClosed` calls through the pipeline are inert in the configuration users get | — |
| i-14 | **`--proof-check=lazy` in CI's proof tester** means closedness is not checked there either | `ci proofs` |

## Open — asks

Changes we would like made. The reasoning for each is in the document named;
these rows exist so there is one place to see what is outstanding. Kinds are
from [`findings.md`](findings.md): **B** an adoption, **C** a change to the
pipeline, **D** an assertion.

### Which ask moves which metric

The [analysis groups](../TODO.md#what-the-analysis-is-for) each carry numbers we
watch. If you are a cvc5 developer wondering where effort would show up, this is
the map. **R1 and R2 are the two we would ask for first** — R2 is a one-line
change, R1 is the one that makes everything else exact.

| ask | moves | from → to |
| --- | --- | --- |
| **R1** emit the registries as JSON | *all of G1–G4* | inferred → exact. Retires most of our fragility and several asks below |
| **R2** assert the completeness implication in `setDefaultsPre` | G4 completeness chain | the guarantee obtainable only as a side effect → stated in cvc5's own tree |
| **R3** extract helpers out of solver classes | G2 checker TCB | 41,446 lines → smaller, and 1 of 13 checkers over-scoped → 0 |
| **R4** one `InferenceId`, one site | G3 nameability | 84% single-site → 100% |
| **R5** `no_support` covers defaults | G4 contract | 1 option escaping → 0 |
| **R6** declare intentional seam refusals | G1 hole census | 14 gaps *inferred* → 14 gaps *stated* |
| **R7** derivable pass↔trust-id names | G3 nameability | correspondence checkable only by construction site → by name |
| **R7b** RARE file in the marker | G3 nameability | theory recoverable by scanning two directories → from the header |
| **R8** safe mode prunes at build time | G4 contract | features disabled at runtime → absent from the binary |
| **R9** test each RARE rule against the rewriter | G5 determinacy | a rule that misstates the rewrite fails silently → is caught |
| **R10** rule on the hygiene standard | G3 nameability | eleven proposals open → decided, either way |
| **R11** run our ratchets in CI | all groups | measured when we remember → measured on every push |
| **R12** one corpus run with `--stats-internal` | *decides G1's worth* | holes counted → holes counted **and** the fraction any input has reached |

| # | ask | kind | why | where argued |
| --- | --- | --- | --- | --- |
| **R1** | **emit cvc5's proof registries as JSON** from a build target | C | the highest-leverage ask by a distance: makes our whole table tier exact instead of parsed, and retires most of the fragility below. Three parser bugs in one session are the argument | [coupling](coupling.md#r1--emit-the-tables-cvc5-already-has) |
| **R2** | **make the completeness guarantee statable** — assert in `setDefaultsPre` that a safe build with `--check-proofs` has `checkProofsComplete` on, or exempt the option from the expert refusal | D / C | *(corrected by running it: the flag is `category = "expert"`, so safe **and** stable mode refuse it — it cannot be named in either job whose mode carries the contract. The implication is not just unasserted, it is the only available route.)* (`i-3`) | [coupling](coupling.md#r2--make-the-completeness-guarantee-statable) |
| **R3** | extract the pure `static` helpers out of solver classes | C | six rule checkers compile against the solvers they check. Filed as `f-1` | [coupling](coupling.md#r3--get-the-theory-solvers-out-of-the-proof-checkers-includes) |
| **R4** | one `InferenceId`, one production site | C | until an id names one program point, inference coverage cannot be precise (`i-8`) | [coupling](coupling.md#r4--one-inferenceid-one-place) |
| **R5** | make `no_support` cover defaults, or derive safe mode's list from it | C | the `SolverEngine` guard fires on assignment only, which is how `stringLazyPreproc` gets through (`i-2`) | [coupling](coupling.md#r5--make-nosupport-cover-defaults) |
| **R6** | declare which seam refusals are *by design* | C | we infer "macro or trust step, so intended" from naming and elaboration — a heuristic that already needed one correction | [coupling](coupling.md#r6--declare-what-the-seam-is-supposed-to-reject) |
| **R7** | make the pass↔`TrustId` correspondence derivable, and fix `BV_GUASS` | C | `i-11` | [coupling](coupling.md#r7--make-the-passtrustid-correspondence-derivable) |
| **R7b** | put the RARE source file in the generated marker | C | makes a rule's owning theory recoverable from the header instead of by scanning two directories (`i-16`) | [coupling](coupling.md#r7b--put-the-rare-source-file-in-the-generated-marker) |
| **R8** | make safe mode prune code at build time | C | `CVC5_SAFE_MODE` prunes almost nothing today; each feature moved from runtime-disabled to not-compiled turns a class of hole into a link error | [coupling](coupling.md#r8--safe-mode-as-a-build-time-property) |
| **R9** | **test each RARE rule against the rewriter** — instantiate the match, rewrite, compare to the target | C | the only thing that catches a rule that *misstates* the rewrite, which today fails silently forever (`i-17`). Belongs upstream, beside the rewriter. Partial is fine | [rare-correspondence E1](rare-correspondence.md#e1--instantiate-each-rare-rule-and-run-the-rewriter) |
| **R10** | adopt the proof hygiene standard, or rule on it | B | eleven rules, most ratifying existing practice; the contested ones are `H1`, `H5`, `H6` | [hygiene](hygiene.md) |
| **R11** | run our checks in cvc5 CI, and upload SARIF | B | `p-1`; the ledger and mode ratchets run in seconds and need no baseline | [tooling](tooling.md#d1--three-artifacts-by-what-each-question-needs) |
| **R12** | **run the corpus with `--stats-internal` and publish the `finalProof::*` counters** — *[we did this for `regress0`](reachability.md): safe mode reaches **0** holes over 1,061 proofs, unrestricted reaches one benchmark in ten, and 10 of 70 live `TrustId`s are touched. The ask is now for the levels and corpora we cannot run* | B | the cheapest experiment either side can run, and the one that decides how much the rest of this is worth. cvc5's counters are a numerator — holes some input reached; our census is the denominator — holes that exist to be reached. Nobody currently knows the ratio, and it cuts both ways: if the corpus has touched most of them the static surface has little headroom and we should narrow accordingly | [why](why.md#1-we-supply-the-denominator-your-own-counters-lack) |

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
| s-6 | `SET_FILTER` is ungated in safe mode, and `SETS_FILTER_UP`/`DOWN` are refused by the seam there — so a `set.filter` benchmark should fail `--check-proofs-complete`. A rank-1 candidate | **spurious, and the most instructive miss so far.** Every link held in the source. But `set.filter` takes a predicate, a predicate is a function-typed term, and `TheoryUF::preRegisterTerm` throws `LogicException` on a function-typed term unless the logic is higher-order — which safe *and* stable mode refuse. One command settled what no amount of reading would have. The analysis is fixed rather than the row retracted: `Fragment.requires_higher_order` now recovers this axis from the type rules, and 13 kinds move to blocked. See [`pr-policy.md`](pr-policy.md) |
| s-7 | "No `uf` kind is blocked in safe mode at all", used to strengthen `i-1` | **half wrong.** `HO_APPLY` is blocked, by the same logic axis as `s-6`. `LAMBDA` is *not* — its argument is not function-typed, only its result is — so `i-1` survives at the kind level, but the sweeping form of the claim does not. `tests/test_fragment.py` now asserts the corrected fact |
| s-5 | The proof checker's TCB is 74% of `src/` | **retracted.** An artifact of a saturating closure mode; the real figure is 8.0%. See [retractions](findings.md#retractions) |

## Filed

| # | what | where |
| --- | --- | --- |
| f-1 | Six proof rule checkers compile against the theory solvers they check, to reach `static` helpers parked on solver classes | [`tcb-001`](findings/tcb-001.md) |
