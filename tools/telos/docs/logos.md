# Logos

*The foothold. Read this before anything else in this directory.*

[`ajreynol/logos`](https://github.com/ajreynol/logos) is **a verified proof
checker for SMT, written in Lean 4**, whose soundness is proved against a
self-contained formalization of SMT-LIB's model semantics, and whose calculus is
compiled from the same `Cpc.eo` signature cvc5 emits proofs against.

It is not prior art telos should study and improve on. It is the thing telos is
built on, and it is a **moving target** — the calculus is regenerated as CPC
changes, and the proof development grows with it.

Measured 2026-08-31 at logos `a5650dad`, against cvc5 `aee8742404`. Every number
below came from a command in the logos tree.

---

## What it is

| | |
| --- | --- |
| **theorem** | `correct___logos_check_proof (input : String) …` — if the parser reads assumptions `assums` out of `input`, and `logos` prints `correct`, then their conjunction is unsatisfiable |
| **grounded in** | `Cpc/SmtModel.lean`, a model semantics for SMT-LIB that is **standalone** — it does not mention the checker and can be read on its own |
| **calculus** | generated from `Cpc.eo` by `ethos-eoc`, the Eunoia compiler in the ethos tree. Not hand-transcribed |
| **verdicts** | `correct` (0) · `incorrect` (1) · `incomplete` (2) |
| **status** | 591 rules, **all proven**; no `sorry`, `admit` or `axiom` anywhere in 872 Lean files |
| **age** | 707 commits since 2026-03-03 |

The verdict trichotomy is the first thing that should catch a dokimasia
reader's eye, and it is discussed [below](#l5--the-incomplete-verdict-is-a-completeness-instrument).

## What it weighs

`scripts/cpc-loc-summary.py`, non-blank non-comment lines:

| | files | lines | |
| --- | ---: | ---: | --- |
| **specification** — `Cpc.Spec` + dependencies | 6 | **2,680** | `SmtModel` 1,602 · `Spec` 387 · `LogosTerm` 253 · `SmtModelDefs` 230 · `SmtEval` 108 · `SmtValueOrder` 100 |
| **checker** — `Cpc.Logos` + dependencies | 3 | **8,573** | `Cpc.Logos` is 8,212 of it, and is generated |
| **parser** | 3 | **2,653** | 654 signature-independent, 1,999 generated. **Unverified** |
| **correctness proof** | 820 | **691,993** | of which rule correctness is 771 files / 634,388 lines |

Inside the proof: rule correctness **634,388**; translation type preservation
23,796; smt-model-eval type preservation 19,832; closedness and evaluation
invariance 8,204; top-level checker correctness 4,599; canonicity 1,091.

**Read those two columns together, because their ratio is the entire product.**

| | ethos + the `cpc` signature | Logos |
| --- | --- | --- |
| what a human must read and believe | **≈26,400 lines** — 13,862 of C++ plus 12,530 of Eunoia | **2,680 lines** of Lean specification |
| what a machine checks | nothing | **691,993 lines** of proof |
| the calculus is | hand-written, and separately hand-implemented in C++ | generated from the signature |
| unverified residue | all of it | the parser — 2,653 lines |
| speed | fast, and the design goal | "not (yet) optimized … significantly slower" |

[`docs/kernel.md`](../../../docs/kernel.md) says the measure that matters is
**"how long the argument is and how much of it a reader can check."** Logos
answers that with a factor of ten, and moves the rest onto Lean's kernel. That
is the axis this whole repository is organised around, moved further in six
months than static analysis of cvc5's C++ will move it ever.

## What its guarantee actually is

Being precise, in the terms of
[the guarantee table](kernel-of-cvc5.md#prior-art-and-what-each-guarantee-actually-is)
— because Logos is **a sixth kind**, and neither of the two nearby ones.

It is **not reflection** (SMTCoq, `bv_decide`): nothing is evaluated by the host
and admitted as an axiom at check time. `correct___logos_check_proof` is an
ordinary Lean theorem, proved once, universally quantified over inputs. Running
the checker produces no proof term.

It is **not cake_lpr's verified binary**: the theorem is about a *Lean function*,
and the executable is produced by Lean's compiler and a C toolchain, neither of
which is verified. cake_lpr's distinguishing move — composing with a verified
compiler's correctness theorem so the statement covers the machine code — is
exactly what is missing.

> **Kind F — a verified program, compiled by an unverified compiler.**
> The theorem is real, unconditional and machine-checked. Getting from it to
> the binary you ran costs you Lean's compiler and the C toolchain.

Trusted base of a `correct` verdict, in full:

| | |
| --- | --- |
| **the specification is the right one** | 2,680 lines. This is the irreducible human obligation and it is what the ten-fold reduction bought |
| **Lean's kernel** | which is not itself verified — see [`language.md`](language.md#lean-4--chosen) |
| **Lean's compiler and the C toolchain** | because you ran a binary, not a proof term |
| **the parser** | 2,653 unverified lines. The theorem is about whatever the parser read |
| **that the assumptions are the problem you asked about** | Logos does not compare them to an original input; `include` and `reference` are ignored |

The last two are the interesting ones and both are named openly in the logos
README, which is the right way to state a guarantee.

---

## What telos learns from it

### L1 — The generated calculus works, and its failure modes are designed

`install/install-cpc.sh` compiles `Cpc.eo` into the `Cpc` package with
`ethos-eoc`. Regeneration rewrites the signature-wide modules and **preserves
per-rule proofs**, so:

- a rule newly added to CPC appears as a `sorry` stub — caught by the
  `proof-hygiene` group, which greps for `sorry`/`admit`/`axiom` textually and
  needs no build;
- a rule whose *statement* changed keeps its old proof and therefore **fails to
  build**;
- `install-cpc.sh --cached --check` is the `regeneration` CI group and fails
  when generated code has drifted from the signature it came from.

That is [inversion I2](design.md#i2--one-definition-of-the-calculus) — one
definition of the calculus — implemented, in production, with each way it can go
wrong turned into a distinct loud signal. telos should not design a second
mechanism for this. It should use this one.

### L2 — The product is the ratio, not the line count

692,000 lines of proof sounds like the achievement. It is not: it is the *cost*.
The achievement is 2,680 lines of specification, because that is what a person
has to read. Every design decision in telos should be evaluated by what it does
to the numerator, and a change that adds 50,000 lines of proof to remove 100
lines of specification is a good trade.

This is worth stating because it inverts the instinct that a smaller development
is a better one. Against ethos it is the *larger* artifact that has the *smaller*
trusted base.

### L3 — The modularity contract is the real foothold

`docs/modularity.md` in the logos tree is written for exactly telos's situation
— "anyone building a Logos-like checker for a different calculus" — and it is
specific:

- **`Proofs/Checker.lean` is byte-identical between `Cpc` and `CpcMini`** modulo
  the package name: the ~25 preservation theorems and
  `correct___eo_is_refutation` contain zero `CRule` references and zero
  calculus-specific invariants. `CheckerState.lean` likewise. That is
  demonstrated, not aspirational — `CpcMini` has 5 rules against `Cpc`'s 591, a
  different signature, and different invariants;
- **the core depends on exactly one signature symbol: `and`.** `not`, `=` and
  `imp` are used only by rule proofs and live outside the checker's transitive
  imports;
- the cost of a new checker is **dominated by the semantics layer**, not the
  checker layer. The checker layer is 0.6% of Cpc's hand-written proof;
- start from `CpcMini`, not `Cpc`.

And one concrete trap, worth repeating because it fails *silently*: Lean names
the arms of a generated definition positionally, so `__smtx_model_eval.eq_9` is
`and` in Cpc and `imp` in CpcMini. A checker-layer proof naming an arm number is
reusable by accident only, and in the bad case rewrites with the wrong arm. The
fix — name the three arms the layer needs in `Common.lean`, each by `rfl` — is
one line of discipline that a new checker should adopt **before its first proof,
not after its second package**.

### L4 — The unverified residue is the parser, and that is not a small thing

[`kernel-of-cvc5.md`](kernel-of-cvc5.md#the-external-checker) makes the point
about ethos and it applies unchanged here: **a checker that mis-parses a proof
accepts the wrong thing.** Logos's parser is 2,653 lines and is outside the
theorem, which the README says plainly.

This is the one place where cake_lpr is strictly ahead — its correctness
statement covers parsing and I/O, because CakeML's compiler theorem composes
with it. Closing the same gap in Lean has no equivalent path today, so the
honest options are to shrink the parser, to verify it against a Lean-level
specification and accept that the compiler is still trusted, or to leave it and
say so. Logos does the third, and says so.

### L5 — The `incomplete` verdict is a completeness instrument

Logos returns **three** verdicts, not two. `incomplete` means: *the checker
accepted the proof, but it mentions something the SMT-LIB specification does not
model, so the correctness theorem does not apply to it.* The run explains on
stderr which assumption or command left the specified fragment.

That is this repository's subject appearing inside a soundness tool. cvc5's
`--check-proofs-complete` asks whether the *solver* left a hole; logos's
`incomplete` asks whether the *specification* covers what the proof mentions.
Two different completeness questions, both answered per-input, both silent about
everything no input has reached — which is exactly the limitation
[`docs/contract.md`](../../../docs/contract.md#the-gap-this-exists-to-close)
exists to name.

The static counterpart — *which proofs could logos ever return `incomplete` on*
— is a dokimasia-shaped question about a Lean development rather than about
C++, and nobody is asking it.

### L6 — `trust` has no soundness proof, and that is the whole story

`Cpc.eo` declares **593** non-expert rules. Logos's `CRule` has **591**
constructors. The two rules in the signature with no constructor are:

> **`beta-reduce`** and **`trust`**.

`trust` is cvc5's declared hole — the rule that proves an arbitrary formula with
no justification, the one
[`dokimasia.trust`](../../../dokimasia/trust/) censuses 75 ids of. It cannot
have a soundness proof, because it is not sound; it appears in the generated
Lean as a *program*, `__eo_prog_trust`, not as a rule with a correctness
theorem.

So the two projects meet exactly here, and the sentence is worth getting right:

> **Every hole dokimasia counts is a proof Logos cannot check.**

dokimasia measures how often cvc5 reaches for `trust`. Logos makes reaching for
it fatal. Neither observation is available from inside the other project, and
together they turn "proof completeness" from a quality metric into a
precondition for the soundness argument existing at all.

### L7 — Performance is the open flank, and it is where telos's questions bite

The README says it: not optimized, significantly slower than performant
checkers. A full proof build takes **over two hours** and is deliberately not in
CI, which compiles only a representative subset.

That is the reality check on
[the language decision](language.md) and on
[I1](design.md#i1--the-answer-carries-its-certificate)'s cost question. It is
also not obviously telos's problem: a checker that is 100× slower than ethos is
still fast relative to solving, and the trade it buys is a ten-fold smaller
trusted base.

### L8 — What Logos deliberately is not

Worth listing, because these are the gaps telos might occupy rather than
duplicate:

- **not a solver.** It checks proofs; it produces none;
- **not a Eunoia checker.** It does not support arbitrary signatures — the rules
  are compiled from CPC specifically. `ethos` remains the general framework
  checker;
- **not linked to the input problem.** `include` and `reference` are ignored, so
  a `correct` verdict is about the assumptions the file states, not about the
  benchmark somebody solved. That is one level down from
  [contract §3](../../../docs/contract.md#why-3-is-not-a-footnote) — *the solver
  that produced the proof is the solver that solved it* — and it is the same
  shape of gap;
- **not fast.**

---

## What this does to telos

Most of what [`TODO.md`](../TODO.md) proposed as telos's first year exists, is
better than the sketch, and is maintained. Specifically: the language question
is settled by demonstration rather than by argument, the SMT-LIB semantics that
[`kernel-of-cvc5.md`](kernel-of-cvc5.md#what-eunoia-actually-is) called the
research risk **exists** as `Cpc/SmtModel.lean`, and the "one definition of the
calculus" inversion is shipping with CI behind it.

What remains unclaimed is the **producer** side. Logos is a checker and says so.
Every inversion in [`design.md`](design.md) that is about the thing *emitting*
proofs — the answer carrying its certificate, rewrites proving themselves as
they fire, safe mode as a type — is untouched by it.

Which gives telos a definition of success that is executable rather than
rhetorical:

> **telos succeeds when Logos says `correct`.**

Not "produces proofs". Not "has a verified kernel" — that is Logos's, and telos
should inherit it rather than rebuild it. A solver whose output Logos accepts
with verdict `correct`, on a fragment, is a complete statement of the goal, and
the `incomplete` count is the completeness metric this repository has been
looking for all along — computed by a tool, per input, with no static analysis
in the loop.

The revised plan is in [`TODO.md`](../TODO.md).
