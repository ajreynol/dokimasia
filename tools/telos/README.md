# telos

*What would you build if you started from the answer?*

**Internal.** This is a research note, not a project announcement. It is not
linked from the root [`README`](../../README.md), from
[`docs/kernel.md`](../../docs/kernel.md), or from either register
([`TODO.md`](../../TODO.md), [`docs/issues.md`](../../docs/issues.md)), and it
should stay that way until there is something to show. Note that
`ajreynol/dokimasia` is a **public** remote: unadvertised here means
*not pointed at*, not *not visible*. Nothing in this directory makes a claim
about cvc5, asks anything of cvc5, or should be quoted as though it did.

**Read-only member of this repository.** telos consumes dokimasia's analyses.
Nothing in `dokimasia/` imports it, no test covers it, no baseline ratchets it,
no CI job runs it. It ships no code. If this directory were deleted the
repository would be exactly as functional as it is now, which is the property
that makes it safe to keep here.

---

## The charter

Stated here because a research project's charter is the thing a person agreed
to, and until now it was spread across this file and [`TODO.md`](TODO.md)
instead of being in one place somebody could hold it to.

**The question.** *If the proof came first, what would the solver look like?*
The premise below says why that is the complementary question to the parent's
and not a competing one.

**The goals, in order** — they are [`TODO.md`](TODO.md)'s `T1` to `T6`, ordered
by how fast each could kill the project rather than by how much work each
represents. `T2`, a proof-carrying rewriter for one theory, is first because it
is the only one whose outcome could invalidate the design.

**The wishue** — the outcome if this went unusually well, and not a commitment.
It is already stated, and stated as a target somebody else maintains the
goalposts for: **telos succeeds when Logos says `correct`** — a fragment on
which a telos solver's output is accepted by an independently maintained
verified checker, with the `incomplete` count as the completeness metric.

**Out of scope**, in full in [`TODO.md`](TODO.md)'s *Not doing*, and in
summary: writing a kernel (Logos is the kernel); writing a solver until `T2`
returns; verifying the search, ever, under the current design; claiming anything
about cvc5, ethos or logos, since a fact about any of them goes into that
project's register under its own name; and announcing this directory.

**Is there a paper in it?** Not in the design, and probably never — a set of
inversions nobody has implemented is a position, not a result. There are two
candidates and both are measurements rather than arguments: `T3`'s `incomplete`
census over a CPC corpus run through both checkers, which is a coverage number
for the specification that nobody has taken, and `T2`'s outcome either way,
including the negative one. Neither is close, and whether either is worth
writing up is a decision for a person and not for this file.

## The premise

dokimasia measures cvc5's proof kernel from the outside, and the arc of that
measurement is stated in [`docs/kernel.md`](../../docs/kernel.md): make it
easier to *argue* which part of cvc5 has to be right, along five axes —
nameable, closed, small, local, mechanized — with mechanized named explicitly as
**the last axis, not the first**.

That ordering is correct for cvc5, and it is correct because cvc5 exists. The
axes are hard there because proofs were added to a solver that already worked,
and every finding in this repository is a consequence of that order:
`ProofGenerator* pg = nullptr` is a default argument
([H6](../../docs/hygiene.md#h6--no-proof-must-be-said-out-loud)), the safe-mode
disable list is maintained by hand ([i-5](../../docs/issues.md)), and
completeness depends on a search budget ([i-4](../../docs/issues.md)) because the
rewriter was deliberately left uninstrumented.

telos asks the complementary question, and only the complementary question:

> **If the proof came first, what would the solver look like?**

Not a competitor to cvc5, not a replacement, not a proposal to anyone. A
research vehicle for the one experiment dokimasia cannot run, because dokimasia
is downstream of a design that is already fixed.

## The foothold: Logos

**telos is built on [`ajreynol/logos`](https://github.com/ajreynol/logos), and
Logos is a moving target.** Everything below is downstream of that fact, so it
belongs before the design rather than after it.

Logos is a **verified proof checker for SMT in Lean 4**. Its soundness theorem
`correct___logos_check_proof` says: if the checker prints `correct` for a proof
file, the assumptions the parser read out of it are unsatisfiable — proved
against `Cpc/SmtModel.lean`, a standalone Lean formalization of SMT-LIB's model
semantics. Its calculus is **compiled from the same `Cpc.eo` signature cvc5
emits proofs against**, by `ethos-eoc`, and regenerated as CPC changes.

Measured at logos `a5650dad`:

| | ethos + the `cpc` signature | **Logos** |
| --- | --- | --- |
| what a human must read and believe | ≈**26,400 lines** — 13,862 C++, 12,530 Eunoia | **2,680 lines** of Lean specification |
| what a machine checks | nothing | **691,993 lines** of proof |
| rules proved sound | — | **591 of 593**, no `sorry`/`admit`/`axiom` in 872 files |
| the calculus is | hand-written twice, in Eunoia and in C++ | generated from the signature, with drift caught in CI |
| unverified residue | all of it | the parser — 2,653 lines |

The two CPC rules with no soundness proof are `beta-reduce` and **`trust`** —
cvc5's declared hole, the one
[`dokimasia.trust`](../../dokimasia/trust/) censuses 75 ids of. It cannot have
one. Which states the relationship between these two projects in a sentence:

> **Every hole dokimasia counts is a proof Logos cannot check.**

Full description, measurements and eight things telos should learn from it are
in [`docs/logos.md`](docs/logos.md). **Read that first.**

The consequence for telos is large and worth stating plainly: the kernel half of
this project already exists and is better than the sketch that preceded it. What
is unclaimed is the **producer** side — and that gives telos a definition of
success that is executable rather than rhetorical:

> **telos succeeds when Logos says `correct`.**

## Why here, and not somewhere else

Because the analysis is the input. Every design decision below is derived from a
measured finding in this repository, and the derivation is the interesting part —
a list of things a hypothetical solver could do better is worthless; a list where
each entry closes a hole somebody measured is a specification.

| dokimasia found | telos's answer | where |
| --- | --- | --- |
| the proofless call is the *ergonomic* one ([H6](../../docs/hygiene.md#h6--no-proof-must-be-said-out-loud)) | the answer type carries the certificate; there is no proofless return | [`design.md`](docs/design.md#i1--the-answer-carries-its-certificate) |
| the calculus is stated three times and can disagree (`SIG`, [R1](../../docs/coupling.md#r1--emit-the-tables-cvc5-already-has)) | stated once; checker, printer and docs are functions of it | [`design.md`](docs/design.md#i2--one-definition-of-the-calculus) |
| completeness depends on a search budget ([i-4](../../docs/issues.md)) | the rewriter returns its justification; there is no reconstruction to bound | [`design.md`](docs/design.md#i3--rewrites-prove-themselves-as-they-fire) |
| safe mode is a hand-maintained list ([i-5](../../docs/issues.md), [R8](../../docs/coupling.md#r8--safe-mode-as-a-build-time-property)) | the feature set is a type parameter; the unsafe configuration does not compile | [`design.md`](docs/design.md#i4--safe-mode-is-a-type-not-a-list) |
| 8 trust steps have no stated reason ([i-9](../../docs/issues.md)) | a hole must name itself to typecheck | [`design.md`](docs/design.md#i1--the-answer-carries-its-certificate) |

Five inversions, five findings. That is the whole design so far, and it is
enough to start.

## What cvc5's kernel actually is

Before defining a kernel you have to be able to point at the one that exists.
cvc5 has **two**, they are not the same size, and they do not trust the same
things. Measured 2026-08-31 against cvc5 `aee8742404` and ethos `b9188b86`:

| | internal — `--check-proofs` | external — `ethos` |
| --- | --- | --- |
| trusted C++ | **41,446 lines**, 179 files — 8.0% of `src/` | **13,862 lines**, standalone |
| trusted declarative | — | **12,530 lines** of Eunoia (the `cpc` signature) |
| the calculus is written as | `switch` bodies and LaTeX doc comments | 620 `declare-rule`, 340 `declare-const`, 151 `define`, 248 `program` |
| shares code with the solver it checks | **yes** — 10 theory subsystems, the rewriter, `Env` | **no** |
| how it checks a rewrite | replays it — `MACRO_REWRITE`, registered trusted at pedantic level 4 | re-derives it from rules in the signature |

Read the last two rows together and the external checker is the real kernel: it
is the only one whose correctness is independent of the solver's. It is also
the smaller one, and its 13,862 lines are a *general-purpose* framework checker
rather than cvc5-specific code.

But the trusted total is not 13,862. It is 13,862 **plus 12,530 lines of
Eunoia**, of which **4,186 lines are `program` definitions** — side conditions,
which is to say a second implementation of polynomial normalisation, ACI
normalisation, bit-blasting and string reasoning, written in an unverified DSL
and evaluated by an unverified evaluator. `programs/Strings.eo` alone is 2,277
lines.

**That is the kernel to learn, and it is the right size to verify.** Not 41,446
lines of C++ entangled with the solver — the type system and the matcher, the
two pieces that decide whether a rule application is legitimate, are **466 lines
together** (`type_checker.cpp:91–556`).

Note what is *not* true of any of it: **neither checker is verified.** ethos is
an efficient, independent, unverified C++ program, and independence is not
verification even though the two are constantly conflated. Getting that
distinction right matters enough that
[`docs/kernel-of-cvc5.md`](docs/kernel-of-cvc5.md#prior-art-and-what-each-guarantee-actually-is)
tabulates what every comparable tool actually proves — cake_lpr, SMTCoq,
lean-smt, bv_decide, IsaSAT, versat, Carcara — because "verified" names at least
five different guarantees across that list, with trusted bases ranging from *a
theorem about the machine code* down to *nothing at all*.

## The language

**Lean 4** — which Logos settles by demonstration rather than by argument, so
the decision record below is now a rationalisation of a choice that has already
been made and validated at scale. Rust stays named as the escape hatch for a
search core that needs to go fast.

The independent argument, had Logos not existed, is that in a dependently typed
host language **[inversion 1](docs/design.md#i1--the-answer-carries-its-certificate)
is free**. `solve` cannot return `unsat` without a proof term, because the
return type says so, and that is checked by a kernel nobody has to trust our
account of. dokimasia's founding question — *is there a path through the solver
that produces no proof at all?* — is answered by the type signature, statically,
permanently, for no ongoing cost. A language that cannot do that would put
telos in the business of building dokimasia again.

Alternatives considered and why they lost — Rust + Verus, F\* → C, Isabelle/HOL
+ Sepref, Rocq — are in [`docs/language.md`](docs/language.md), along with what
would change the decision.

## On the name

`telos` — τέλος — *end, completion, purpose*; Aristotle's final cause, the
"that for the sake of which". It fits, it is spelled correctly, and it sits in
the family already in use: `dokimasia` (δοκιμασία, the scrutiny before office),
`eunoia`, `ethos`, `anoieu`, `alethe`.

The one alternative with a real argument behind it:

| | word | means | the case for it |
| --- | --- | --- | --- |
| **telos** | τέλος (noun) | the end, the goal, the purpose | recommended. Correct, recognisable, in the family |
| teleos | τέλεος (adj.) | **complete**, perfect, having reached its end | the Attic variant of τέλειος. It names the project's actual subject — this repository is about *completeness, not soundness* — and it is the more distinctive string |
| entelecheia | ἐντελέχεια | having its end *within itself* | Aristotle's coinage, ἐν + τέλος + ἔχειν. Semantically exact for a solver that carries its own certificate. Unusable as a directory name |

Worth knowing that "teleos" is not a misspelling of "telos" — they are two real
words, and the adjective is arguably the better fit. Worth also knowing that
both are common in software naming and neither is distinctive; `entelecheia` is
unique and unpronounceable. Recommendation is to keep `telos`; renaming is one
`git mv` and nothing depends on the string.

*(Also noted, for a different tool one day: εὔθυνα, `euthyna`, the Athenian
audit **after** leaving office — the exact counterpart of δοκιμασία, which is
the scrutiny before. That pair is sitting there unused.)*

## Status

Design notes only. Nothing is written here. The measurements are of other
people's trees — cvc5, ethos and logos — and no design claim in this directory
has been tested against an implementation.

There are three endings and a person picks: it graduates into its own
repository, it is folded into the parent, or it is retired in place with a note
saying what was learned and why it stopped. Going quiet is not one of them, and
a directory that has not moved is a claim nobody is standing behind.

- **[`docs/logos.md`](docs/logos.md) — the foothold: what Logos is, what it weighs, what its guarantee is, and eight lessons. Start here**
- [`docs/kernel-of-cvc5.md`](docs/kernel-of-cvc5.md) — what the kernel is today, what "defining" it means, and what each comparable tool's guarantee actually is
- [`docs/design.md`](docs/design.md) — the five inversions, and the risks in each
- [`docs/language.md`](docs/language.md) — the decision record
- [`TODO.md`](TODO.md) — next steps, ordered, with what each produces

The same standard as the rest of the repository applies: **a number here comes
from something that ran**, and everything else is labelled as a design note.
