# The pipeline, and where it leaks

The stages a cvc5 proof passes through, what can go missing at each, and
what the code measures today.


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

## What the measurements already say

Counted against cvc5 `40a4bb7e4`. These are the inputs to the first checks,
not findings — a finding is a claim, and claims get reproduced before they are
filed (see [what we promise](findings.md)).

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
[`TODO.md`](../TODO.md):

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

