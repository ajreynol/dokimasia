# Rewriter faithfulness

Does a proof rule capture each hand-written cvc5 rewrite exactly? If one does,
an unsound rewrite cannot survive a complete proof check. If none does, the
rewrite rests on the C++ alone, and a bug in it appears in a proof only as a
`trust` step. That is how [cvc5#13039](https://github.com/cvc5/cvc5/issues/13039)
(`MultSltMult`) went unnoticed.

This directory reviews the **bit-vector** and **strings/sequences** rewriters
at the pinned source revision (`40a4bb7e43`, see `scripts/cvc5.lock`). Each
rewrite gets a confidence level that it corresponds to proof rules, and is
therefore sound.

- [METHOD.md](METHOD.md): evidence, confidence levels and record schema.
- [REPORT.md](REPORT.md): per-rule tables, the suspect rules and probe-sweep
  totals. Generated; do not edit.
- `data/<unit>.json`: one record per rule, one file per review unit.
- `probes/{bv,strings}/*.smt2`: 909 small inputs, each with `; EXPECT:`.
- `runs/<rev>.json`: every probe re-run on one cvc5 binary, with ethos.
- `tools/probe.py`, `tools/build_report.py`: the harness and the aggregator.

```bash
python3 rewriter_report/tools/probe.py rewriter_report/probes/bv/MultSltMult_issue13039.smt2
python3 rewriter_report/tools/probe.py --ethos -j 12 --out rewriter_report/runs/<rev>.json rewriter_report/probes/*/*.smt2
python3 rewriter_report/tools/build_report.py      # regenerate REPORT.md
python3 tests/test_rewriter_report.py              # no solver needed
```

The probe needs `cvc5` and `z3` on PATH, or `$CVC5_BIN` and `$Z3_BIN`.
`--ethos` also needs `ethos`, and uses `$CPC_SIG`, which defaults to
`deps/cvc5/proofs/eo/cpc`.

## Results at 40a4bb7e43

447 rules: 2 suspect, 38 low, 66 medium, 268 high, 73 n/a.

| Theory | suspect | low | medium | high | n/a |
| --- | ---: | ---: | ---: | ---: | ---: |
| bv | 2 | 7 | 31 | 111 | 44 |
| strings | 0 | 31 | 35 | 157 | 29 |

All 909 probes were run on two binaries. On both, the only disagreements with
z3 are the 8 `MultSltMult` probes. 681 of the 787 unsat probes on b08092b502
have proofs that are trust-free and accepted by ethos.

### Unsound: `MultSltMult` / `MACRO_BV_MULT_SLT_MULT` (bv)

The pinned revision still has the #13039 code. The C++ accepts three input
classes that the RARE rules `bv-mult-slt-mult-1/2` do not cover, and it
rewrites all three wrongly. All are confirmed by z3 and yices, including with
the model fixed:

1. The #13039 shape: the add is under `sign_extend` and `a` is under
   `zero_extend`.
2. **New:** the left product has the right roles, but in the right product the
   shared `a` is zero-extended and `x` is sign-extended. Example:
   `x=#b11 t=#b11 a=#b01` makes
   `(bvslt (bvmul (zext (x+t)) (sext a)) (bvmul (zext a) (sext x)))` false,
   but the rewrite makes it true. A fix that pins only the left side's roles
   leaves this open.
3. `concat` of a zero with more than two children is read as `zero_extend` of
   its first child. This fails even on ground terms, because it fires in
   pre-rewrite before constant folding, and proof printing then errors with
   `expecting comparable bit-vector terms`.

By inspection, upstream fix #13042 closes all three; it has not been run. The
proof channel is the same in every case. The elaborator normalizes, then adds
an unconditional `MACRO_THEORY_REWRITE_RCONS_SIMPLE` step for the remainder.
When RARE cannot close it, it stays `trust` and nothing fails.
`--check-proofs-complete`, ethos and `--no-proof-allow-trust` all reject these
proofs; plain `--check-proofs` does not.

### Proof-side defects (the rewrite is right, the proof is not)

- **`STR_EQ_CONJ_LEN_ENTAIL` / `MACRO_STR_EQ_LEN_UNIFY_PREFIX`:** the
  elaborated proof contains a false `ARITH_POLY_NORM` step when the length
  bound holds only by entailment. Example:
  `(= (str.substr w 0 1) (str.++ z "a" u))`.
  - At `macro_rewrite_elaborator.cpp:645`, the code expects
    `CDProof::addStep` to fail on a bad step. It does not check the step
    unless eager checking is on, so the fallback never fires.
  - Plain `--check-proofs` passes. `--proof-check=eager` and ethos reject it.
- **`SEQ_EVAL_OP` on `seq.update`:** the C++ evaluates it, but the CPC
  `$seq_eval` has no case for it, so ethos rejects every such step. This fails
  closed.
- **`$str_is_code_point`** (`proofs/eo/cpc/programs/Strings.eo`) accepts
  196608, one past its documented range [0, 196607].
- **`bv-zero-extend-eq-const-1/2`** are ill-typed: they extract m+1 bits and
  compare them with an m-bit zero. No proof uses them today.
- **`--bv-rw-extend-eq`** crashes on ordinary BV equalities.
  `TheoryBV::ppStaticRewrite` returns `mkTrustRewrite(atom, null)` when
  neither extend rule matches.

### Low: uncovered C++ guards with the #13039 shape, but sound

Each of these C++ guards is broader than its RARE rule. Brute force,
differential fuzzing and z3 found no wrong result, but a bug in the uncovered
part would show up only as `trust`:
- `ExtractMultLeadingBit`: an n-ary `concat` multiplicand.
- `CTN_REPL_LEN_ONE_TO_CTN` and `REPL_CHAR_NCONTRIB_FIND`: `len <= 1`
  against a RARE rule's `= 1`.
- `RPL_CCTN`, `RPL_CCTN_RPL` and `IDOF_DEF_CTN`: a needle inside a constant
  with characters left over.
- `MACRO_STR_STRIP_ENDPOINTS`: `str.from_int` endpoints.
- `XorSimplify`: complement pairs.

[REPORT.md](REPORT.md) lists the rest. Most are trivially sound rewrites with
no RARE rule, such as `BvIteConstCond`, `STR_LEQ_ID`, `STR_CONV_IDEM` and
`UPD_*`.

### Pipeline observation

RARE conditions are enforced at reconstruction, so a C++ step that violates
one cannot use that rule. It degrades silently to `trust`, as
`MACRO_THEORY_REWRITE_RCONS_SIMPLE`, `TRUST_THEORY_REWRITE` or the macro's
name. A trust step therefore cannot tell a bug from a coverage gap: sound
rewrites leave the same trust as #13039 did. Rejecting trust
(`--check-proofs-complete`, on by default in safe builds per `cvc5 --help`)
catches every unsound probe here. The cost is also failing on the 65 sound
probes that still leave trust on b08092b502.

## Caveats

- **No binary at the pin.** Probes ran on b08092b502 (193 commits before the
  pin; its strings rewriter and elaborator match the pin) and on the PATH
  binary, dc8ad24031 (478 commits before). Each record notes where the rule's
  C++ or RARE rules changed in between.
- **Some ethos rejects are version skew.** Old proofs checked against the
  pin's signature can fail because rule arguments changed (aafcc486e2), or
  because indices became opaque (a13878bc19). Skew-only rejects are not
  findings.
  - `CTN_SPLIT_constlhs_seq` fails in a `concat_csplit` solver step, not a
    rewrite. It is unresolved.
- **The reviewers were model agents**, each reading one unit of C++ against
  its proof rules. `suspect` and proof-defect items were reproduced by hand.
  `high` means the probes and the guard comparison found nothing. It is not a
  proof of soundness.
- **z3 is no evidence for unsupported operators.** It lacks `str.rev`,
  `str.update`, `str.to_lower/upper`, `str.indexof_re` and
  `seq.update/rev/replace_all`, so those probes rely on cvc5 proofs, brute
  force and fuzzing.
- **Not covered:** arithmetic, booleans, sets, arrays, datatypes and quantifier
  rewriters. The same method and harness apply; add a unit under `data/`.
