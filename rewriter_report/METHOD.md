# Rewriter faithfulness review: method

cvc5 issue [#13039](https://github.com/cvc5/cvc5/issues/13039) was an unsound
hand-written BV rewrite (`MultSltMult`). Its RARE counterparts
(`bv-mult-slt-mult-1/2`) were sound, but the C++ accepted one operand order the
RARE rules do not cover. With proofs on, the step was not reconstructed. It
appeared as a `trust` step (`MACRO_THEORY_REWRITE_RCONS_SIMPLE`), so the proof
checker never saw an unsound inference. Proof production masked the bug instead
of catching it.

This review asks the same question of every hand-written rewrite in a
theory rewriter: **does a proof rule capture exactly what the C++ does?** When
a sound proof rule covers a rewrite on every input the C++ accepts, an unsound
rewrite cannot pass a complete proof check. When coverage is partial, the
uncovered part rests on the C++ alone.

## Evidence for each rule

1. **Dispatch.** Where the rule runs: which kind, pre- or post-rewrite, the
   position in the `LinearRewriteStrategy` or `if` chain, and the
   `ProofRewriteRule` it is registered as (if any).
2. **Proof coverage.** The mechanism that justifies the step in a
   proof:
   - `rare`: one RARE rule (`src/theory/*/rewrites*`) matches the step directly.
   - `rare-multi`: a chain of RARE rules found by generic reconstruction
     (`rewrite_db_proof_cons`).
   - `theory-rewrite`: a `ProofRewriteRule` checked as `THEORY_REWRITE`.
     The **internal** checker recomputes it by calling the same C++
     (`rewriteViaRule`), so it is *circular* and gives no independent evidence.
     Only the Eunoia/CPC definition in `proofs/eo/cpc` is an independent check,
     and only if it is written independently of the C++.
   - `macro-elaborated`: a `MACRO_*` rule elaborated in
     `macro_rewrite_elaborator.cpp` or `basic_rewrite_rcons.cpp` into RARE
     steps. Any `addTrustedStep(... MACRO_THEORY_REWRITE_RCONS*)` in the
     elaboration is a residual hole, and it gets judged on its own.
   - `evaluate`: constant folding justified by `EVALUATE` (sound if the
     evaluator is; out of scope here).
   - `none`: no proof rule. Reconstruction must find a RARE chain by search, or
     the step stays `trust`.
3. **Guard comparison.** The C++ `applies` or match conditions and its output,
   set against the RARE rule's pattern, `define-cond-rule` conditions, and
   right-hand side. A **guard gap** is any input the C++ rewrites that no
   matching proof rule instance accepts with the same result. Look for
   operand-order loops (`std::swap`, `for i in 0..1`), mixed cases like
   zext/sext, n-ary vs binary, width or bit-index arithmetic, signed vs
   unsigned, empty or singleton cases, and overflow in index computations.
4. **Probes** (`probes/<theory>/<Rule>_*.smt2`, run with `tools/probe.py`).
   - *Differential*: a formula that the rewrite decides, at edge widths and
     values, with the expectation in `; EXPECT:`. cvc5 is compared with z3. A
     disagreement is direct evidence of unsoundness. Confirm it by fixing z3's
     model in the input and rerunning both solvers before calling it a bug.
   - *Proof*: an unsat instance, usually `(assert (not (= LHS RHS)))`, whose
     proof should contain the step. List the remaining `trust` steps and their
     ids. No trust means the step was reconstructed from RARE rules.
   The cvc5 binary (`cvc5 --version`) may be older than the analyzed source
   checkout. A rule whose C++ changed between the two needs a note, from
   `git -C deps/cvc5 log <bin>..HEAD -- <file>`.
5. **Independent check.** Optionally state the rewrite schematically and ask z3
   to prove it valid at several widths or lengths. This checks the
   *specification*, not the C++, so it never raises confidence alone.

## Confidence levels

| Level | Meaning |
| --- | --- |
| `high` | Every rewrite the C++ performs is an instance of a RARE rule, or a short RARE chain, whose conditions follow from the C++ guards. A proof probe reconstructs with no trust, and differential probes agree. |
| `medium` | Covered by proof rules, but the evidence has a gap: generic reconstruction search (budgeted), an n-ary or flattening mismatch handled by normalization, an Eunoia definition that is only partly independent, or no probe could isolate the step. |
| `low` | Soundness rests on the C++ alone. This covers no proof rule, reconstruction that leaves `trust` (`MACRO_THEORY_REWRITE_RCONS*`, `REWRITE_NO_ELABORATE`, ...), and only the circular internal checker. Not a known bug, but a proof check would not catch one. |
| `suspect` | A concrete guard gap was found: an input the C++ accepts that the proof rule does not, with a different result. It may also be a confirmed differential disagreement. The record carries a witness. |
| `n/a` | Dead code, not dispatched, or pure constant evaluation. |

## Record schema (`data/<unit>.json`)

```json
{
  "unit": "bv-simplification-a",
  "source_rev": "40a4bb7e43",
  "binary": "cvc5 version ... [git dc8ad24031 ...]",
  "rules": [
    {
      "id": "MultSltMult",
      "theory": "bv",
      "location": "src/theory/bv/theory_bv_rewrite_rules_simplification.h:1893",
      "dispatch": "post-rewrite BITVECTOR_SLT via RewriteSlt; MACRO_BV_MULT_SLT_MULT",
      "summary": "one line: what it rewrites to what",
      "coverage": "macro-elaborated",
      "proof_rules": ["MACRO_BV_MULT_SLT_MULT", "bv-mult-slt-mult-1", "bv-mult-slt-mult-2"],
      "guard_comparison": "what was compared and how it lines up",
      "guard_gap": "null, or the input class the proof rules miss",
      "probes": ["probes/bv/MultSltMult_issue13039.smt2"],
      "probe_result": "cvc5=unsat z3=sat; trust MACRO_THEORY_REWRITE_RCONS_SIMPLE",
      "confidence": "suspect",
      "rationale": "why this level, in 1-3 sentences",
      "witness": "for suspect: the smallest input and the wrong result"
    }
  ]
}
```

Paths in records are relative to the cvc5 checkout (`location`) or to
`rewriter_report/` (`probes`).
