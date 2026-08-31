# Next steps

**Rewritten after reading [Logos](docs/logos.md).** The previous version planned
a year of work — describe Eunoia's semantics, mechanize the type system, build a
checker in Lean — most of which exists, is finished, and is maintained. What
follows is what is left.

Ordered by **how fast each one could kill the project**, the same selection rule
[`docs/goals.md`](../../docs/goals.md) applies to finding holes: optimise for
the latency of the answer, not for how much work it represents.

| | task | tests | cost | produces |
| --- | --- | --- | --- | --- |
| **T1** | read Logos properly | nothing — it is the prerequisite for every other row | days | knowing what is already done |
| **T2** | a proof-carrying rewriter for one theory | **[I3](docs/design.md#i3--rewrites-prove-themselves-as-they-fire)**, the riskiest inversion, and the only one Logos does not settle | a week | the answer to whether telos's central claim holds |
| **T3** | a CPC corpus, run through **both** ethos and logos | nothing — it is the oracle, and a measurement nobody has | days | agreement data, and the first `incomplete` census |
| **T4** | the static `incomplete` question | nothing | weeks | a dokimasia-shaped analysis of a Lean development |
| **T5** | differential-test ethos's evaluator against logos's compiled semantics | nothing here — but it may find a real defect | days | possibly a soundness finding, for somebody else's register |
| **T6** | measure ethos's real TCB | nothing — it corrects a number | hours | an exact figure to replace a file-level estimate |

**T2 first.** It is the only item on the list that could invalidate the design,
it is a week, and nothing else depends on its outcome being favourable.

---

## T1 — Read Logos properly

Not a formality. [`docs/logos.md`](docs/logos.md) is an outside reading of the
repository, made in an afternoon from its README, its scripts and its line
counts. It is not a substitute for the four things that actually matter:

- **`Cpc/SmtModel.lean`** — 1,602 lines, and the only part of the whole
  development a human is obliged to read. If the specification is wrong, nothing
  downstream of it means anything, and it is the one place where "the proof
  checks" is not an answer;
- **`docs/modularity.md`** — written for exactly telos's situation and specific
  about it: `Proofs/Checker.lean` is byte-identical between `Cpc` and `CpcMini`,
  the core depends on a single signature symbol (`and`), the cost of a new
  checker is dominated by the semantics layer, and *start from `CpcMini`*.
  Including the trap where Lean's positional arm names (`__smtx_model_eval.eq_9`
  is `and` in Cpc and `imp` in CpcMini) make a proof reusable by accident only,
  with a one-line discipline to adopt **before the first proof**;
- **`Cpc/Api.lean`, `ApiChecks.lean`, `ApiCorrect.lean`** — how the theorem
  connects to the string the executable was handed. This is the part most
  verified-checker projects leave informal and this one does not;
- **`docs/smt-model-definitions.pdf`** — the intended write-up of the semantics,
  the specification and the checker.

Also worth knowing before planning anything: a full proof build is **over two
hours** and is deliberately not in CI, and `scripts/check-proof-hygiene.sh`
rejects `sorry`/`admit`/`axiom` textually with no build at all.

## T2 — A proof-carrying rewriter for one theory

**The experiment that matters, and the only inversion Logos leaves open.**

Logos settles the kernel. It says nothing about the *producer*, and
[I3](docs/design.md#i3--rewrites-prove-themselves-as-they-fire) is the load-
bearing claim on that side: that a rewriter can return `(t', proof that t = t')`
at no meaningful cost to the author of a rewrite rule, dissolving
[i-4](../../docs/issues.md) — the search budget that cvc5's proof completeness
currently depends on. FMCAD 2022 explicitly declined to do this, for stated
reasons. The claim is that a dependently typed host changes the arithmetic, and
**it has never been tested.**

Test it small. Pick one theory where cvc5's RARE coverage is already good — the
Boolean rules, `theory/booleans/rewrites` — and:

1. write its rules once, declaratively;
2. elaborate each into a rewrite *and* its justification;
3. measure **how much per-rule manual work the justification needed** (the FMCAD
   objection) and **what building a proof term on every step costs at runtime**
   (the objection FMCAD did not have to make).

Three outcomes, all worth having: the claim survives; the authoring cost is real
and the FMCAD objection stands in a dependently typed setting too, which is an
interesting negative result; or proof terms on every rewrite step do not scale
and telos needs a different answer to i-4 than "make it not exist."

The natural target format is CPC, so that step 2's output is something
`logos` can be pointed at — which makes T3 a dependency in practice even though
it is not one in principle.

## T3 — A CPC corpus, through both checkers

Run cvc5 with `--dump-proofs --proof-format=cpc` over a benchmark set, then run
**both** `ethos` and `logos` over the result. Split the corpus by
`--safe-mode=safe` against unrestricted, so it divides along the line
[the contract](../../docs/contract.md) cares about.

Three things fall out, and the second and third are measurements nobody has:

- **the oracle** for T2 and T5;
- **the `incomplete` census.** Logos returns three verdicts, and `incomplete`
  means it accepted the proof but the proof mentions something the SMT-LIB
  specification does not model. How often, and on what? That is a coverage
  number for the specification, and the specification is the only part of the
  trusted base a human reads;
- **ethos/logos disagreement.** Any proof one accepts and the other rejects is
  interesting by construction, and the direction matters: a proof `ethos`
  accepts and `logos` calls `incorrect` is the more alarming one.

## T4 — The static `incomplete` question

T3 answers *how often* per input. The dokimasia question is the other one:

> **Which CPC proofs could Logos ever return `incomplete` on?**

That is the same shape as everything in
[`docs/pipeline.md`](../../docs/pipeline.md) — take the code, ask what it could
ever produce, with no benchmark in hand — pointed at a Lean development instead
of at C++. The side conditions are `TranslatableAssumptionList` and
`CmdListTranslationOk` in `Cpc/Proofs/Assumptions.lean`, and they are
`Decidable`, which means the question is about the *reach* of `__eo_to_smt`
rather than about a heuristic.

Worth doing because it is the one place telos's parent repository has a genuine
methodological advantage, and because a specification's coverage gap is exactly
as invisible as a solver's until somebody enumerates it.

## T5 — ethos's evaluator against logos's compiled semantics

The previous version of this list proposed differential-testing the signature's
4,186 lines of Eunoia `program`s against the C++ they mirror, on the grounds
that they were trusted completely and checked by nothing.

**That is no longer the right framing.** The programs are compiled into Logos —
592 `__eo_prog_*` definitions — and **520 of the 591 rule proofs depend on one**.
A program that was wrong in a way that made its rule unsound would make that
rule's soundness proof fail. The signature's computational content is inside the
soundness argument now.

What is *not* established is that the two implementations of Eunoia evaluation
agree: `ethos`'s C++ evaluator (`TypeChecker::evaluate`, the 56 `eo::` builtins,
`evaluateProgramApp`) against what `ethos-eoc` compiles the same signature into.
If they diverge, one of them accepts a proof the other does not, and the Lean
theorem is about the Lean one. T3's corpus makes this cheap to look for.

**Where it belongs.** This is a *soundness* question about `ethos`, and
dokimasia is [completeness, not soundness](../../docs/goals.md#the-stance).
Recording it because the gap is real and nobody appears to be looking at it —
not because this repository should claim it.

## T6 — Measure ethos's real TCB

[`kernel-of-cvc5.md`](docs/kernel-of-cvc5.md) still says *"roughly 4,000 lines of
typing and evaluation, 2,300 of state, 3,600 of parsing"* and admits the split is
by file rather than by dependency closure. Two closures, seeded from
`TypeChecker` and from the parser entry point.

**A dokimasia task, not a telos one**, and one already implied by
[`TODO.md` G2](../../TODO.md)'s *"extend the closure to the Eunoia seam."*
Deprioritised: it sharpens a comparison rather than deciding anything.

---

## Then: the producer side

Everything above is reading, measuring, or one experiment. What telos would
actually *build*, if T2 comes back favourable, is the part Logos does not cover:
a solver whose output is a CPC proof, structured so that
[I1](docs/design.md#i1--the-answer-carries-its-certificate) and
[I4](docs/design.md#i4--safe-mode-is-a-type-not-a-list) hold by construction —
the answer carries its certificate, and a proofless configuration does not
typecheck.

The target is precise and someone else maintains the goalposts:

> **telos succeeds when Logos says `correct`.**

Not `incomplete`, which means the proof left the specified fragment. Not
"produces proofs", which is unfalsifiable. A fragment on which a telos solver's
output is accepted by an independently maintained verified checker, with the
`incomplete` count as the completeness metric — measured per input, by a tool,
with no static analysis in the loop.

## Not doing

- **Writing a kernel.** Logos is the kernel. Rebuilding it would be the single
  most expensive way for this project to produce nothing.
- **Writing a solver**, until T2 returns. A CDCL(T) implementation is the least
  interesting and most expensive part of this, and starting there is how
  research projects become abandoned codebases.
- **Verifying the search.** Ever, under the current design. See
  [I5](docs/design.md#i5--soundness-is-the-kernels-job-completeness-is-the-type-systems),
  and the price tag IsaSAT and versat put on the alternative.
- **Claiming anything about cvc5, ethos or logos.** telos is a design exercise.
  If it produces a fact about any of them — as T3 and T5 might — that fact goes
  into the appropriate register under the appropriate project's name, with the
  same evidence standard everything else here is held to.
- **Announcing it.** See the [notice](README.md).

## The honest cost

T1 and T6 are days. T3 is days. T2 is a week or two and could fail. T4 is weeks.
Nothing here produces a solver.

But the scale has changed, and in the right direction. The previous version of
this file estimated a year before anything could be called a solver, on the
assumption that telos had to build a verified kernel first. It does not. Logos
took roughly six months and 707 commits to do that — the repository carries its
own estimate of what the proofs would have cost by hand, and the number in it is
25 expert person-years, which is worth reading as a statement about how the
work was done as much as about how large it is.

The progressive stance from [`docs/kernel.md`](../../docs/kernel.md) applies
unchanged: **every degree is worth having, and there is no finish line.** T3
alone — a corpus through both checkers, with an `incomplete` census — would
justify the directory.
