# The kernel of cvc5

What has to be right for a cvc5 proof to mean something, measured rather than
asserted, and what "defining" it would take. This is the learning agenda; the
design that follows from it is [`design.md`](design.md).

Measured 2026-08-31 against cvc5 `aee8742404` and ethos `b9188b86`. Every number
here is reproducible with a command; where a number is an estimate it says so.

## There are two kernels

cvc5 checks its own proofs twice, by two mechanisms that share nothing.

### The internal checker

`ProofChecker` plus the 13 registered theory rule checkers, run by
`--check-proofs`. [`dokimasia.tcb`](../../../dokimasia/tcb/) measures what it
compiles against:

```
$ python3 -m dokimasia.tcb measure ~/cvc5
  closure         179 files      41,446 lines
  all of src/    1663 files     521,073 lines
  the checker depends on 8.0% of cvc5 by line count
```

Inside that closure are 97 files of `theory/` (22,217 lines), across 10 theory
subsystems, plus the rewriter. Six rule checkers `#include` the headers of the
solvers they check
([`tcb-001`](../../../docs/findings/tcb-001.md)), and `MACRO_REWRITE`'s checker
replays the rewrite with the same code that produced it — which cvc5 says out
loud by registering it through `registerTrustedChecker` at pedantic level 4.

**So the internal checker is not an independent check.** It is a very good
consistency check, and `--check-proofs-complete` riding on it is the oracle this
whole repository points at. It is not a kernel, because its correctness is not
independent of the correctness of the thing it checks.

### The external checker

`ethos`, run on the output of `--proof-format=cpc`. This one *is* independent —
it contains no cvc5 code at all:

```
$ find ~/ethos/src -name '*.cpp' -o -name '*.h' | xargs wc -l | tail -1
  13862 total
```

Its weight, by file:

| | lines | what it is |
| --- | --- | --- |
| `type_checker.cpp` | 1,971 | typing, matching, evaluation — the core |
| `state.cpp` | 1,874 | symbol table, rule registry, scopes |
| `expr_parser.cpp` | 1,395 | term syntax |
| `cmd_parser.cpp` | 1,100 | command syntax |
| `expr.cpp` / `literal.cpp` / `kind.cpp` | 1,514 | terms, literals, the kind enum |
| `lexer.cpp` | 477 | |
| everything else | ~5,500 | `util/`, `base/`, `main`, stats, plugin |

Roughly **4,000 lines of typing and evaluation, 2,300 of state, 3,600 of
parsing.** That split is by file, not by a dependency closure — a proper
measurement is a `tcb`-shaped job and is [item 1 in `TODO.md`](../TODO.md).

Note that the parser is soundness-critical here in a way it usually is not: a
checker that mis-parses a proof accepts the wrong thing. 3,600 lines is a third
of the binary.

### But the trusted base is not the binary

`ethos` is a *framework* checker. It knows nothing about SMT. Everything cvc5
specific lives in the signature it is handed:

```
$ find ~/cvc5/proofs/eo/cpc -name '*.eo' | xargs wc -l | tail -1
  12530 total
```

| | count | |
| --- | --- | --- |
| `declare-rule` | **620** | the inference rules of the calculus |
| `declare-const` / `declare-parameterized-const` / `declare-consts` | **340** | the term vocabulary |
| `define` | **151** | abbreviations |
| `program` | **248** | **side conditions — computational content** |

The `program`s are the thing to look at. 4,186 lines of them:

| file | lines |
| --- | --- |
| `programs/Strings.eo` | 2,277 |
| `programs/Bitblasting.eo` | 684 |
| `programs/Quantifiers.eo` | 207 |
| `programs/PolyNorm.eo` | 193 |
| `programs/DistinctValues.eo` | 186 |
| `programs/Datatypes.eo` | 162 |
| `programs/Utils.eo` | 156 |
| six more | 321 |

**That is a second implementation of solver logic**, written in a dynamically
evaluated DSL, trusted completely, and checked by nothing. `$poly_neg`,
`$poly_mod_coeffs` and their neighbours in `PolyNorm.eo` re-do what cvc5's
arithmetic normalisation does in C++. `Bitblasting.eo` re-does the bit-blaster.
If a `program` is wrong in a way that is *more* permissive than the C++, ethos
accepts proofs of things that are not true, and no test in either project is
positioned to notice.

**The honest trusted base of a cvc5 proof is therefore ≈13,900 lines of C++ plus
≈12,500 lines of Eunoia**, and the second half is the part nobody measures.

## What Eunoia actually is

Worth stating plainly, because the design in [`design.md`](design.md) depends
on it: **Eunoia is a logical framework in the LF tradition, with computational
side conditions.** It is the successor to LFSC, from the same lineage. The
family resemblance is to Dedukti / λΠ-modulo — a dependently typed core plus a
user-supplied rewrite system — rather than to a proof format like DRAT.

Concretely, from `rules/Booleans.eo`:

```lisp
(declare-rule resolution ((C1 Bool) (C2 Bool) (pol Bool) (L Bool))
    :premises (C1 C2)
    :args (pol L)
    :conclusion ($resolve C1 C2 pol L)
)
```

A rule is a typed constant. Its premises are proof terms, its arguments are
terms, and its conclusion may be *computed* by a `program` (`$resolve`).
`:requires` adds a side condition that must evaluate to `true`:

```lisp
(declare-rule reordering ((C1 Bool) (C2 Bool))
    :premises (C1)
    :args (C2)
    :requires (((eo::list_minclude or C2 C1) true))
    :conclusion C2
)
```

Checking a proof is therefore **type checking plus evaluation**, and the
evaluator is where the semantics live. `ethos`'s `Kind` enum carries **56
`EVAL_*` builtin operators** — arithmetic, list operations, string operations,
bit-vector extraction, comparison, hashing — implemented in
`TypeChecker::evaluateLiteralOpInternal`. `TypeChecker::evaluateProgramApp`
runs user `program`s by matching against their defining equations.

So the kernel's specification, stated as a list of obligations, is:

| | what needs defining | where it lives today |
| --- | --- | --- |
| **K1** | the term language | the `Kind` enum, `expr.cpp`, `literal.cpp`, `kind.cpp` — 1,514 lines |
| **K2** | the type system | `getType` … `getTypeAppInternal`, `type_checker.cpp:91–440` — **350 lines** |
| **K3** | matching — when a pattern matches a term | `TypeChecker::match`, `:441–556` — **116 lines** |
| **K4** | evaluation, and the 56 `eo::` builtins | `evaluate` **295 lines**, literal and list operations **1,009 lines** |
| **K5** | evaluation of user `program`s, and its termination | `evaluateProgramApp` / `evaluateProgramInternal` — **111 lines**, plus 248 programs |
| **K6** | what a proof *is*, and what makes one valid | `Kind::PROOF`, `(pf F)`, and the rule registry in `state.cpp` |
| **K7** | what the signature's rules **mean**, w.r.t. an SMT-LIB semantics | `Cpc/SmtModel.lean` in [Logos](logos.md) — **1,602 lines, and it did not exist a year ago** |

The striking thing is how small K2 and K3 are. The type system and the matcher —
the two pieces that decide whether a rule application is legitimate — are **466
lines together**. The weight is in evaluation, and specifically in the 1,009
lines of builtin operations, which is arithmetic and string manipulation rather
than logic.

K1–K6 are engineering: a specification of an existing 14,000-line program.
Large, finite, and carrying no research risk — with the one exception of K5's
termination question, which is genuinely open and is discussed below.

**K7 was the research risk, and it is the one that has been retired.** Verifying
K1–K6 alone buys *relative soundness* — "if the signature's rules are sound, the
checker only accepts valid proofs" — which is what most checkers in this space
deliver and is not the whole claim. Discharging K7 needs a mechanized SMT-LIB
semantics, and the honest position a year ago was that no such thing existed.

[Logos](logos.md) has one. `Cpc/SmtModel.lean` is 1,602 lines of standalone
model semantics for SMT-LIB — standalone in the strong sense that it never
mentions the checker — and `Cpc/Spec.lean` supplies the correspondence between
Eunoia terms and SMT-LIB terms. **591 of CPC's 593 non-expert rules are proved
sound against it**, with no `sorry`, `admit` or `axiom` anywhere in the
development. The two that are not are `beta-reduce` and `trust`, and `trust`
cannot be, which is
[the point](logos.md#l6--trust-has-no-soundness-proof-and-that-is-the-whole-story).

So the list above is no longer a research agenda. It is a description of
something that exists, and telos's job is to read it rather than to redo it.

## What "defining the kernel" means, in order

Four things, in the order they become possible. Each is worth having alone,
which is the same progressive stance as
[`docs/kernel.md`](../../../docs/kernel.md).

1. **Describe it.** A precise account of K1–K6, of the kind a paper would carry,
   checkable by a reader against `type_checker.cpp`.
2. **Mechanize the syntax, typing and matching.** K1, K2, K3, K6 as inductive
   definitions. A type checker falls out.
3. **Mechanize evaluation.** K4, K5 — where the interesting obligations are: is
   `program` evaluation confluent, does it terminate, and what happens when it
   does not. Dedukti's literature is directly applicable.
4. **Discharge the signature.** K7, against a mechanized semantics.

Steps 1–3 verify *the checker*; step 4 verifies *the calculus*, and it is the
one everybody skips. Skipping it is respectable, but it should be said out loud
that the rules then *are* the axioms, and 593 hand-written axioms is a large
thing to trust.

**[Logos](logos.md) has done all four**, for CPC specifically rather than for
Eunoia in general, and did not stop at three. That is the single most important
fact in this directory, and it means the list above is context for reading
somebody else's development rather than a plan. What telos does about that is
[the last section of `logos.md`](logos.md#what-this-does-to-telos).

## Prior art, and what each guarantee actually is

**"Verified" means a different thing for every tool on this list**, and the
differences are the useful part. Read the theorem, not the adjective: some of
these prove a property of a *checker*, some prove a property of a *solver*, one
proves a property of a *binary*, one proves nothing at all and is on the list
anyway because independence is worth something without proof.

| tool | what it is | what is actually proved | what is still trusted |
| --- | --- | --- | --- |
| **Logos** | verified SMT proof checker in Lean 4, for **CPC** — the calculus cvc5 emits ([`logos.md`](logos.md)) | `correct___logos_check_proof`: if `logos` prints `correct` for a proof file, the assumptions the parser read out of it are unsatisfiable — against a standalone Lean formalization of SMT-LIB model semantics. **591 rules, all proven, no `sorry`/`admit`/`axiom` in 872 files** | the 2,680-line specification being the right one; Lean's kernel; **Lean's compiler and the C toolchain**, since you run a binary; the **unverified 2,653-line parser**; and that the assumptions are the problem you asked about — `include` and `reference` are ignored |
| **cake_lpr** | LPR/LRAT checker; HOL4, compiled by CakeML | if the **binary** prints `s VERIFIED UNSAT`, the CNF in the parsed DIMACS file is unsatisfiable. Composed with CakeML's compiler-correctness theorem, so the statement is about the machine code — **parsing and I/O included** | HOL4, CakeML's compiler theorem, the machine model. Notably **not** an extraction step or an unverified C compiler |
| **SMTCoq** | Rocq/Coq plugin; certified checker for zChaff, veriT and CVC4 certificates | the checker is proved correct in Coq; by computational reflection a successful check yields a Coq proof of the goal | Coq itself. Solvers untrusted. Scope is the quantifier-free fragment of bit-vectors, arrays, LIA and UF — not "SMT" |
| **lean-smt** | Lean 4 tactic; runs cvc5, reconstructs CPC proofs | **nothing is proved.** It builds a native Lean proof *term* for each CPC step, so the result is checked by Lean's kernel like any other proof | Lean's kernel, and nothing else. Reconstruction is not proved correct — it either yields a term the kernel accepts or it fails. Measured: **15,271 of 21,595 cvc5 proofs (71%)**, so the cost of the small trusted base is incompleteness |
| **bv_decide** | Lean 4 tactic; verified bitblasting → CaDiCaL → LRAT check | bitblasting correctness against Lean's `BitVec` theory, **and a soundness proof of the LRAT checker** | **the Lean compiler.** It runs by proof-by-reflection and adds the compiled check's result as an axiom, which puts the compiler in the trusted base — strictly more than lean-smt trusts, in the same language. CaDiCaL is *not* trusted |
| **IsaSAT** | verified CDCL SAT solver; Isabelle/HOL refined to LLVM | if literals fit in 32 bits and no input clause has duplicate literals, it returns a model when SAT and none when UNSAT. **The search itself is verified, both directions** | Isabelle, the refinement chain and code generator, LLVM. **It emits no certificate** — you trust the solver rather than checking its output |
| **versat** | verified CDCL SAT solver in Guru | **soundness of UNSAT only**: if it answers UNSAT then a resolution derivation of the empty clause exists — proved *statically*; the derivation is never built at run time. Explicitly **not** proved complete and **not** proved terminating | Guru, and checks deferred to run time — which are a source of incompleteness, not unsoundness |
| **Carcara** | Alethe checker and elaborator, Rust | **nothing. Carcara is not a verified tool.** | all of it. Its value is *independence* from the solver plus speed, and elaboration of coarse steps into fine ones |
| **ethos** | the Eunoia framework checker, C++ | **nothing. ethos is not a verified tool.** | all 13,862 lines, plus the 12,530-line signature it is handed |

### The five kinds of guarantee on that list

Worth separating, because telos has to choose one and the choice is the design.

| | shape | who | what you get | what it costs |
| --- | --- | --- | --- | --- |
| **A** | **verified checker, by reflection** | SMTCoq, bv_decide | a proved-correct checking function, *evaluated* by the host | the host's reduction machinery — and its compiler too, if native reduction is used, which is why bv_decide trusts more than SMTCoq does |
| **B** | **verified checker, as a binary** | cake_lpr | a theorem about the executable, parser and all | a verified compiler toolchain, which exists for exactly one language |
| **C** | **verified solver** | IsaSAT, versat | the search is proved; no certificate is produced or needed | years of work, a large trusted base by comparison, and no artifact a third party can re-check |
| **D** | **proof reconstruction** | lean-smt | the smallest possible trusted base — the host kernel and nothing else | **incompleteness.** 29% of cvc5's proofs do not reconstruct |
| **E** | **unverified but independent** | Carcara, ethos | a second opinion from code that shares nothing with the solver | no proof. Independence is not verification, and the two get conflated constantly |
| **F** | **verified program, unverified compiler** | **Logos** | an ordinary, unconditional theorem about the checking function — proved once, no axiom admitted at check time, no proof term produced per input | the compiler that turned it into the binary you ran. Strictly weaker than B, strictly stronger than A, and it is where you land when your language has no verified compiler |

Two observations that bear directly on telos.

**cvc5's production kernel is kind E; its verified one is kind F.** `ethos` is
independent and fast and proves nothing — a respectable engineering position,
and the right one for a checker that has to keep up with a solver. But it means
the answer to *"what has to be right for a cvc5 proof to mean something"* is, on
the production path, "13,862 lines of C++ and 12,530 lines of Eunoia, on their
authors' word."

[Logos](logos.md) answers the same question with **2,680 lines of Lean
specification** and a machine-checked proof of everything else. Same calculus,
same signature — generated from it, in fact — and roughly a tenth of the reading.
That is the kernel argument getting shorter in the sense
[`docs/kernel.md`](../../../docs/kernel.md) means, and it happened while this
repository was measuring the C++ side of it.

**Kind C is the road telos explicitly does not take.** IsaSAT and versat prove
the search, and they are the two clearest demonstrations of what that costs:
IsaSAT is the fastest verified SAT solver by a wide margin and is still not in
the same conversation as CaDiCaL or Kissat, and versat's guarantee — sound on
UNSAT, not complete, not terminating — is much narrower than the word
"verified" suggests on first reading. Both emit no certificate, so a third party
has nothing to check.
[I5](design.md#i5--soundness-is-the-kernels-job-completeness-is-the-type-systems)
is the decision to go the other way.

**And note what lean-smt's 71% is.** It is a *completeness* number, produced by
the same trade dokimasia measures in cvc5: the smaller the trusted base, the
more proofs fail to land. That is this repository's subject appearing in a
different tool, and it is the closest existing measurement of what telos's
architecture would cost.

## Reading

The lineage, closest first. Not endorsements — the ones worth reading before
writing anything, with what to read each one *for*.

**Read first, and completely**
- **[Logos](https://github.com/ajreynol/logos)** — `~/logos`. Not background:
  the thing telos is built on. Read `README.md`'s *Correctness* section for the
  theorem, `docs/modularity.md` for the contract a second checker has to meet,
  `Cpc/SmtModel.lean` for the 1,602 lines that are the actual specification, and
  `scripts/cpc-loc-summary.py` for where the weight sits. Analysis in
  [`logos.md`](logos.md).

**The framework itself**
- Eunoia / ethos — `~/ethos`, and the `cpc` signature in `~/cvc5/proofs/eo/cpc`.
  The primary source; read `type_checker.cpp` before reading anything written
  about it. The Cooperating Proof Calculus has its own paper, which is the
  intended account of what the rules mean.
- LFSC — ethos's predecessor, from Stump's group, which is also versat's. The
  design decisions telos would be re-examining were mostly made here.
- Dedukti / λΠ-modulo, and Lambdapi. The same shape — a dependently typed core
  plus a user-supplied rewrite system — with a mature literature on exactly the
  [K5](#what-eunoia-actually-is) obligations: confluence, termination, subject
  reduction. This is where to look when `program` evaluation has to be
  justified rather than described.

**Read for the theorem statement**
- cake_lpr — read the correctness theorem and what CakeML's compiler theorem
  adds to it. It is the strongest end-to-end claim anyone in this space makes,
  and it is worth knowing exactly how much it covers before using the phrase
  "verified checker" anywhere in telos.
- lean-smt — read it for the 71%, and for the architecture: cvc5 CPC proofs
  reconstructed as Lean terms, kernel-checked, nothing else trusted. It is the
  closest existing thing to what telos would build, in the language telos
  chose, against the calculus telos cares about.
- bv_decide — read it for the *contrast* with lean-smt. Same language, same
  untrusted-solver architecture, and a strictly larger trusted base because it
  reflects rather than reconstructs. The choice between those two is a real
  design decision telos has to make, discussed in
  [`language.md`](language.md#reflection-or-reconstruction).
- SMTCoq — the closest prior art for "SMT proofs, mechanized", and worth reading
  for what its authors found hard and for how narrow the supported fragment is.

**Read for what verifying the search costs**
- IsaSAT (Fleury) — the refinement chain from an abstract CDCL calculus down to
  LLVM is the mature technology for turning a verified algorithm into fast code,
  and the effort involved is the honest price tag on kind C.
- versat (Oe, Stump et al.) — read the *limitations* section. "Verified SAT
  solver" turns out to mean soundness of UNSAT, statically, with runtime checks
  that can fail. A good calibration exercise.

**The problem telos claims to dissolve**
- Nötzli et al., *Reconstructing Fine-Grained Proofs of Rewrites Using a
  Domain-Specific Language*, FMCAD 2022. Read §IV-A before believing
  [inversion 3](design.md#i3--rewrites-prove-themselves-as-they-fire). The paper
  chose not to instrument the rewriter, for stated reasons, and telos's answer
  is that a different host language changes the cost — a hypothesis, not a
  refutation.
- Carcara — read the elaborator, not the checker. Turning coarse steps into fine
  ones is [i-4](../../../docs/issues.md) in another format, solved by a tool
  that does not claim verification and does not need to.
