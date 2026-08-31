# Next steps

Ordered by **how fast each one could kill the project**, which is the same
selection rule [`docs/goals.md`](../../docs/goals.md) applies to finding holes:
optimise for the latency of the answer, not for how much work it represents.

Three of the five inversions in [`design.md`](docs/design.md) are safe bets.
Two are load-bearing hypotheses that have never been tested, and if either is
false the design is different. Test those first, cheaply, before writing
anything that assumes them.

| | task | tests | cost | produces |
| --- | --- | --- | --- | --- |
| **T1** | measure ethos's real TCB | nothing — it corrects a number | hours | an exact figure to replace a file-level estimate |
| **T2** | describe the kernel, K1–K6 | nothing — it is the prerequisite | weeks | `docs/eunoia-semantics.md` |
| **T3** | build a proof corpus | nothing — it is the oracle | a day | differential-testing input for T4 and T6 |
| **T4** | a Eunoia type checker in Lean | **the language choice** | weeks | the first thing telos runs |
| **T5** | a proof-carrying rewriter for one theory | **[I3](docs/design.md#i3--rewrites-prove-themselves-as-they-fire)**, the riskiest inversion | a week | the answer to whether telos's central claim holds |
| **T6** | differential-test the signature's `program`s | nothing here — but it may find a real defect | days | possibly a finding, for somebody else's register |

T5 is independent of everything and should probably go first despite being
fifth in the list above by dependency order. It is a week, and it decides
whether the interesting part of the design survives.

---

## T1 — Measure ethos's real TCB

[`kernel-of-cvc5.md`](docs/kernel-of-cvc5.md) currently says *"roughly 4,000
lines of typing and evaluation, 2,300 of state, 3,600 of parsing"* and admits
the split is by file rather than by dependency closure. That is exactly the
estimate [`dokimasia.tcb`](../../dokimasia/tcb/) exists to replace.

Two closures, seeded separately:

- from `TypeChecker` — what does checking a proof actually compile against;
- from the parser entry point — how much of the binary is soundness-critical
  *because a mis-parse accepts the wrong thing*.

**This is a dokimasia task, not a telos one.** `tcb` is seeded from cvc5's
`ProofChecker` and the 13 rule checkers; pointing it at another tree is a
generalisation of an existing tool, and it belongs in
[`TODO.md` G2](../../TODO.md), which already carries *"extend the closure to the
Eunoia seam, the other component whose independence matters"*. telos ships no
code; it gets to consume the number.

## T2 — Describe the kernel

The K1–K6 obligations in [`kernel-of-cvc5.md`](docs/kernel-of-cvc5.md), written
out: the term language, the typing rules, matching, evaluation, the 56 `eo::`
builtins, `program` application, and what makes a proof valid. Prose and
inference rules, of the density a paper would carry, checkable by a reader
against `~/ethos/src/type_checker.cpp`.

No tools, no proof assistant, no Lean. This is the deliverable that has to exist
before anything can be mechanized, and it is worth having even if nothing ever
is — **an account of Eunoia's semantics does not currently exist in any form**,
and the checker is the specification.

Start with K2 and K3 — 466 lines together, and the part that decides whether a
rule application is legitimate. Do K4's 1,009 lines of builtin operations last;
they are arithmetic and string manipulation, they are tedious, and they are
where the effort will otherwise all go.

## T3 — Build a proof corpus

Run cvc5 with `--dump-proofs --proof-format=cpc` over a benchmark set and keep
the output. This is the differential-testing oracle for T4 (does the Lean
checker agree with ethos) and for T6 (do the `program`s compute what cvc5
computes).

Cheap, mechanical, and needed by two later items. Worth doing under
`--safe-mode=safe` as well as unrestricted, so the corpus splits along the line
[the contract](../../docs/contract.md) cares about.

## T4 — A Eunoia type checker in Lean

**Scope: K1, K2, K3, K6 only.** The term language, the type system, matching,
and what a proof is. **No evaluation, no `eo::` builtins, no `program`s** —
which means it will reject most real proofs, and that is fine. It answers a
different question.

The deliverable is a Lean development with:

- the term language as an inductive type;
- typing as an inductive relation, and a decision procedure for it;
- the `declare-rule` form as data, with rule application as a function;
- a differential test against `ethos` over T3's corpus, on the subset that
  needs no evaluation.

**What it decides.** Whether [`language.md`](docs/language.md) is right. Three
specific things to watch, each of which would reopen the decision:

| watch for | means |
| --- | --- |
| the inductive definitions are awkward — heavy encoding, dependent-type fighting | Eunoia's design does not map onto Lean's as cleanly as assumed |
| checking the corpus is orders of magnitude slower than ethos | requirement 4 has moved into the kernel; F\*→C becomes serious |
| the differential test finds disagreements that are *ethos* bugs | good news, and a finding for the ethos maintainers |

## T5 — A proof-carrying rewriter for one theory

**The experiment that matters, and it should go first.**

[I3](docs/design.md#i3--rewrites-prove-themselves-as-they-fire) claims that a
rewriter can return `(t' , proof that t = t')` at no meaningful cost to the
author of a rewrite rule, and that this dissolves
[i-4](../../docs/issues.md) — the search budget that completeness currently
depends on. FMCAD 2022 explicitly chose not to do this, for reasons that are
stated and are not stupid. The claim is that a dependently typed host changes
the arithmetic, and **that claim has never been tested.**

Test it small. Pick one theory where cvc5's RARE coverage is already good — the
Boolean rules are the obvious start, `theory/booleans/rewrites` — and:

1. write its rules once, declaratively;
2. elaborate each into a rewrite *and* its justification;
3. measure two things: **how much per-rule manual work the justification
   needed** (the FMCAD objection), and **what building a proof term on every
   step costs at runtime** (the objection FMCAD did not have to make).

A week, maybe two. Three outcomes and all of them are worth having:

- **it works** — telos's central claim survives, and the design in
  [`design.md`](docs/design.md) is worth building on;
- **the authoring cost is real** — the FMCAD objection stands in a
  dependently typed setting too, which is a genuinely interesting negative
  result and is worth writing down carefully;
- **the runtime cost is prohibitive** — proof terms on every rewrite step do
  not scale, and telos needs a different answer to i-4 than "make it not exist".

## T6 — Differential-test the signature's `program`s

4,186 lines of Eunoia `program` definitions are trusted completely and checked
by nothing. `PolyNorm.eo`'s `$poly_neg`, `$poly_mod_coeffs` and neighbours
re-implement arithmetic normalisation that cvc5 also does in C++;
`Bitblasting.eo` re-implements the bit-blaster; `Strings.eo` is 2,277 lines on
its own. **If a `program` is more permissive than the C++ it mirrors, ethos
accepts proofs of things that are not true.**

The test is mechanical: generate inputs, run the `program` via `ethos`, run the
C++ equivalent via cvc5, compare. `PolyNorm` first — smallest, most
self-contained, and clearest correspondence.

**Two caveats about where this belongs, and they matter.** This is a
*soundness* question, and dokimasia is
[completeness, not soundness](../../docs/goals.md#the-stance). It is also a
question about a *Eunoia signature*, and
[the contract](../../docs/contract.md#what-we-look-at-and-what-we-do-not) says
plainly: *"We do not analyze Eunoia signatures. `Cpc.eo` and its semantics are
`anoieu`'s subject and it is better at them."*

So telos should not run this as a dokimasia analysis. Either it goes to
`anoieu`, or it is done here as background reading for T2 with any finding
handed over. Recording it because the gap is real and nobody appears to be
looking at it — not because this repository should claim it.

---

## Not doing

- **Writing a solver.** Not until T4 and T5 have both returned. A CDCL(T)
  implementation is the least interesting and most expensive part of this, and
  starting there is how research projects become abandoned codebases.
- **Verifying the search.** Ever, under the current design. See
  [I5](docs/design.md#i5--soundness-is-the-kernels-job-completeness-is-the-type-systems)
  — the search is untrusted on purpose, and that is what makes the kernel small
  enough to verify.
- **Claiming anything about cvc5.** telos is a design exercise. If it produces a
  fact about cvc5 — as T6 might — that fact goes into the appropriate register
  under the appropriate project's name, with the same evidence standard
  everything else here is held to.
- **Announcing it.** See the [notice](README.md).

## The honest cost

T1 and T3 are days. T2 is weeks and is unavoidable. T4 and T5 are each a few
weeks and either could fail. Nothing here produces a solver, and the first
version of anything that could be called one is a year away at a generous
estimate, assuming both experiments succeed.

That is the correct scale for a stretch goal and it should not be presented as
anything else. The progressive stance from
[`docs/kernel.md`](../../docs/kernel.md) applies unchanged: **every degree is
worth having, and there is no finish line.** T2 alone — a written semantics for
Eunoia, which does not exist today — would justify the directory.
