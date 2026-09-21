# Removing regression tester disables

Source review on 2026-09-21, against cvc5 `40a4bb7e43` (the reference in
`scripts/cvc5.lock`). Scope: the **49 proof and 19 CPC directives** reported by
the audit. Suite-wide exclusions are out of scope. CPC-Logos is not registered
at this revision, so there are no CPC-Logos directives to assess.

Four proof directives are redundant under the current harness. Other candidates
below require execution before removal. No solver/checker runs were performed,
and no cvc5 regression file was changed. Regression paths below are relative
to cvc5's `test/regress/cli/`; other source paths are relative to cvc5's root.

## Remove four inactive proof directives

- [x] Inspect all 68 directives against the runner's expected-output metadata
  and proof/CPC applicability conditions.
- [ ] Remove the following four `DISABLE-TESTER: proof` lines in a cvc5 patch,
  after confirming the same expected outputs at the patch's target revision.

| Regression and directive line | Expected output | Assessment |
| --- | --- | --- |
| `regress0/nl/issue12499-learned-rewrite-mod-range.smt2:4` | `sat` | proof tester does not apply |
| `regress0/prop/issue11867.smt2:2` | `sat`, `sat` | proof tester does not apply |
| `regress0/prop/red-psyco-134.smt2:2` | `sat` | proof tester does not apply |
| `regress1/sygus/issue4025-no-rlv-cond.smt2:2` | `sat` from `set-info :status` | proof tester does not apply |

Evidence: `run_regression.py:188` requires an `unsat` token for the proof
tester. The inherited LFSC, Alethe and CPC testers each require exactly
`unsat` (`:208`, `:276`, `:352`). Expected-output extraction and its fallback
to `set-info :status` are at `:914` and `:945`. None of these four files has
an expected `unsat`, so removing the proof directive changes no tester's
applicability. Existing unsat-core or other tester directives can stay.

This is metadata cleanup, with **no added proof coverage**. It would reduce
the proof `yes` count from 49 to 45 at this revision. The remaining 45 proof
directives and all 19 CPC directives pass their respective applicability
checks; there is no equivalent inactive-CPC cleanup in this snapshot.

## Retry performance exclusions first

- [ ] Retry these two proof directives independently, keeping unrelated tester
  directives in place. Remove only after successful runs within the affected
  CI configurations' time budgets.

| Regression | Recorded explanation | What to establish |
| --- | --- | --- |
| `regress1/bv/divtest.smt2:2` | `slow conversion` | Whether internal proof checking still needs a disable; then test CPC, which inherits this proof disable. Slowness alone does not establish a timeout. |
| `regress2/fp/issue7056.smt2:2` | `timeout with unsat cores` | Whether proof and CPC testing time out when the separate unsat-core tester remains disabled. The comment alone does not answer this. |

These are the explicit performance explanations among the direct proof/CPC
disables: one timeout and one slow-conversion comment. Missing explanations
must not be relabelled as timeouts without a run or historical evidence.

## Establish why unexplained directives remain

- [ ] Retry the following cases, recording a specific failure or a successful
  result for each. These are investigation candidates, not established fixes.

| Regression | Tester | Why retry it |
| --- | --- | --- |
| `regress1/quantifiers/bug802.smt2:1` | proof | No command-line override or adjacent reason accompanies the disable. |
| `regress2/instance_1444.smtv1.smt2:1` | proof | Expected `unsat`, QF_UF, and explicitly non-incremental; no adjacent disable reason. |
| `regress1/quantifiers/cdt-0208-to.smt2:3` | cpc | Expected `unsat`; `--full-saturate-quant` and no recorded reason. |
| `regress1/quantifiers/stream-x2014-09-18-unsat.smt2:2` | cpc | Expected `unsat`, no command-line override and no recorded reason. |

- [ ] For the other unexplained directives, recover the introducing change
  before proposing removal. Preserve the intended option coverage: making a
  proof run pass by deleting the option that the benchmark tests is not a
  successful restoration of that test.

## Keep exclusions with an identified obstacle

- [ ] Revisit these after addressing their obstacle, rather than removing the
  directive as a standalone cleanup.

| Regressions | Evidence and required work |
| --- | --- |
| `regress0/deep-restart/dd.fuzz21.smtv1.smt2`, `regress0/deep-restart/dd.wrong-sat-020322.smt2` | Deep restarts are explicitly incompatible with proofs in `src/smt/set_defaults.cpp:1148`. |
| `regress0/quantifiers/issue11066-fresh-binders.smt2` | Fresh binders are explicitly incompatible with proofs at `src/smt/set_defaults.cpp:1101`. |
| `regress0/quantifiers/lra-triv-gn.smt2` | Global negation is explicitly incompatible with proofs at `src/smt/set_defaults.cpp:1107`; its `unsat` answer is not a refutation of the original assertions. |
| `regress0/quantifiers/dd.german169-lemma-inp.smt2` | Lemma inprocessing is explicitly incompatible with proofs at `src/smt/set_defaults.cpp:1159`; all three command-line variants must retain their intended coverage. |
| `regress1/quantifiers/dump-inst.smt2`, `regress1/quantifiers/dump-inst-i.smt2` | Their comments explain that proof production changes the instantiation output. Isolate proof coverage in a companion test or revise the output contract first. |
| `regress0/uf/distinct-elim-threshold-unsat.smt2` | Its comment explains that benchmark output interferes with the external proof stream. Isolate the outputs before enabling CPC. |
| `regress0/quantifiers/dd_SA10-027-dt-ipc.smt2`, `regress0/quantifiers/nl-sqrt2-q.smt2` | Recorded CPC obstacles are overloaded constructors and real algebraic numbers respectively. No fix was established by this review; require successful CPC replay before removal. |

## Evidence required for the remaining removals

- [ ] Use a disposable cvc5 checkout and remove only the candidate directive.
  Invoking a tester while leaving its disable in place can produce a misleading
  successful run that never exercises the tester.
- [ ] Run the regression harness for base, proof and CPC as applicable, retaining
  every `COMMAND-LINE` variant, expectations, scrubbers and feature requirements.
  When removing a proof directive, also check the external testers it re-enables
  wherever they are selected by CI.
- [ ] Record cvc5 and checker revisions, build configuration, arguments, elapsed
  time and the actual executed tester results. A skip or an applicability failure
  does not demonstrate newly working proof coverage. For timeout cases, preserve
  the relevant CI budget and do not accept a timeout converted to a skip.
- [ ] Regenerate the audit and verify that only the intended `yes` entries were
  removed. Keep metadata-only cleanup separate from demonstrated coverage gains.
