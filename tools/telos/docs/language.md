# What telos is written in

**Decision: Lean 4**, for the calculus, the kernel, the metatheory and the first
solver. **Rust** named in advance as the escape hatch for a search core that
needs to be fast, entering through the certificate interface so that nothing
verified is lost when it is used.

This is a decision record, not an advocacy document. The alternatives are good
and the reasons they lost are specific.

## What the language has to do

Ranked. The order is the argument — a language that is excellent at 3 and 4 and
cannot do 1 is not a candidate.

| | requirement | why |
| --- | --- | --- |
| **1** | express *"this function cannot return an answer without a certificate"* as a **type** | [I1](design.md#i1--the-answer-carries-its-certificate) is the whole point. If this needs a linter, telos is rebuilding dokimasia |
| **2** | state and machine-check a soundness theorem about the kernel | [K2, K3](kernel-of-cvc5.md) — ≈500 lines, inductive definitions, structural induction |
| **3** | one artifact for spec, proof and program | the moment the specification and the implementation are separate files, [I2](design.md#i2--one-definition-of-the-calculus) is violated in the tool that exists to demonstrate I2 |
| **4** | produce a runnable binary of respectable speed | a research kernel need not be fast. A solver nobody can run teaches nothing |
| **5** | be legible to the cvc5 orbit | this is a research project inside a repository about cvc5. A language nobody here reads produces artifacts nobody here reads |

## The candidates

### Lean 4 — chosen

Requirement 1 is *free*. `Answer φ` with no proofless constructor is an ordinary
inductive type, and "the solver cannot answer without evidence" is checked by
Lean's kernel. No analysis, no convention, no CI job — the property holds
because the program elaborated.

Be precise about what that buys, since this document is about not overstating
guarantees. **Lean's kernel is not verified.** It is small, and it has
independent reimplementations — `lean4lean` in Lean and `Trepplein` in Scala —
which is a meaningful hedge but is not a proof. (`lean4checker` is *not* one of
them: it re-runs the reference kernel over a compiled environment to catch
`sorry`, unsafe declarations and tampering. Same kernel, different question.)
Lean4Lean's work on mechanizing Lean's metatheory is in progress, not done. So
requirement 1's guarantee is "checked by a small, widely exercised, independently
reimplemented kernel", which is the strongest thing available and is not the
same as "proved".

Requirement 2 is what the language is for. Requirement 3 likewise: an inductive
definition of the calculus, a checker that is a function over it, and a
soundness theorem relating them are three declarations in one file.

Requirement 5 is better than it looks, and for a specific reason: **the two
existing Lean tools in this space bracket telos's design space exactly.**

`lean-smt` runs cvc5, takes back a Cooperating Proof Calculus proof — the very
calculus [`kernel-of-cvc5.md`](kernel-of-cvc5.md) is about — and reconstructs it
as native Lean terms. Nothing in it is proved correct; the terms are checked by
Lean's kernel, so the trusted base is the kernel and nothing else. It
reconstructs **15,271 of 21,595 cvc5 proofs, 71%**.

`bv_decide` bitblasts with correctness theorems against Lean's `BitVec` theory,
calls CaDiCaL untrusted, and checks the returned LRAT certificate with a checker
whose **soundness is proved in Lean**. But it runs that checker by
proof-by-reflection and admits the compiled result as an axiom, which puts **the
Lean compiler in its trusted base** — strictly more than lean-smt trusts, in the
same language, for the same untrusted-solver architecture.

So the untrusted-search / verified-checker split of
[I5](design.md#i5--soundness-is-the-kernels-job-completeness-is-the-type-systems)
is not speculative here — it ships, twice, with two different trusted bases and
a measured completeness cost. That is a better starting position than any other
candidate offers.

Requirement 4 is the weakness and it is real. Lean is reference-counted with
persistent data structures; CDCL wants mutable arrays, cache-friendly watch
lists, and no allocation in the inner loop. Lean has `Array` with in-place
update when the reference is unique, and `ST`/`IO`, so this is a fight you can
win — but it is a fight, and Lean has no mature equivalent of Isabelle's Sepref
refinement framework for *proving* imperative code correct. Since
[I5](design.md#i5--soundness-is-the-kernels-job-completeness-is-the-type-systems)
says the search is untrusted, that gap costs telos nothing today. It would cost
a lot if the project ever changed its mind about verifying the search.

### Rust + Verus — the runner-up, and the escape hatch

The best language for requirement 4 by a distance, and the one the surrounding
field increasingly uses (Carcara is Rust). Verus is a serious verifier for
ownership-typed Rust with real performance code behind it.

It loses on 1, 2 and 3 together:

- Rust's type system cannot index a return type by a *value* without heavy
  encoding. `Answer φ` is not expressible; the nearest thing is a runtime
  invariant and a discipline, which is where cvc5 already is.
- Verus is SMT-backed. Discharging the metatheory of a dependently typed
  framework — inductive predicates, structural induction over derivations — is
  the case SMT-backed verification handles worst.
- Verifying an SMT solver's kernel *with an SMT solver* is defensible (the
  argument is relative soundness, and Lean's kernel would not be in the loop
  either way) but it is rhetorically bad for a project whose stated goal is
  **an argument a reader can check**. [`docs/kernel.md`](../../../docs/kernel.md)
  measures success as "how long the argument is and how much of it a reader can
  check", and "Z3 said so" is a short argument that a reader cannot check.

**Where it comes back.** When the search is the bottleneck, write it in Rust,
leave it untrusted, and have it emit a certificate the Lean kernel checks. That
is I5 working as designed: swapping the search implementation changes nothing
about what is verified. Plan for this rather than resisting it — and note that
Aeneas can lift a pure Rust subset into Lean if some part of it later wants
proving.

### F\* → C (Low\*, KaRaMeL) — the serious third option

The strongest existence proof for *verified code at C speed*: HACL\*, EverCrypt,
EverParse, shipping in Firefox and the Linux kernel. Dependent types, extraction
to idiomatic C, and C is the language that links into cvc5's build without
ceremony.

Loses on 5 and, more importantly, on the same SMT-automation point as Verus:
F\*'s proofs go to Z3, and the parts that do not (`Meta-F*` tactics) are the
parts you would be living in for the metatheory. Smaller community, and the
language has been through a significant redesign. If telos's centre of gravity
were "verified C that cvc5 can link", this would win; it is not.

### Isabelle/HOL + Sepref → LLVM — the closest precedent, and still no

**IsaSAT is the reason to take this seriously.** A CDCL SAT solver refined from
an abstract calculus down to LLVM, whose *search* is verified in both
directions: given 32-bit literals and no duplicate literals in an input clause,
it returns a model when the input is satisfiable and none when it is not.
Sepref is the mature technology for the abstract→imperative refinement that made
that possible, and nothing else on this list has produced a verified solver
anyone would run.

Calibrate that carefully, because it is easy to over-read. IsaSAT solves roughly
4.5× more problems than any *other verified* solver — a comparison within a
small field, not with CaDiCaL or Kissat, which it is not close to. And it
**emits no certificate**: you trust the solver, so a third party has nothing to
re-check. That is kind C in
[the guarantee table](kernel-of-cvc5.md#the-five-kinds-of-guarantee-on-that-list),
and it is the opposite of the trade telos is making.

It loses on 1 and 3. HOL is simply typed: `Answer φ` — a type indexed by a term
— is not directly expressible, and the encodings are exactly the ceremony that
would make [I1](design.md#i1--the-answer-carries-its-certificate) an argument
rather than a fact. Add requirement 5, where Isabelle is the furthest of any
candidate from cvc5's orbit, and it is out — but it is the option to reconsider
first if verifying the *search* ever becomes the goal, because then Sepref is
the only game in town.

### Rocq (Coq) + extraction — no

SMTCoq is the direct prior art and worth reading. But extraction targets OCaml,
which puts requirement 4 out of reach for a solver, and Rocq's imperative story
is weaker than Lean's for no compensating advantage. Lean does what Rocq does
here, with a better compilation target and a community currently pointed at
exactly this problem.

### Everything else

C++ (requirement 1 impossible), Agda/Idris (requirement 4, and no ecosystem),
Dafny (requirement 2 — SMT-backed, and no dependent types), ATS, Why3. None of
them beats a candidate above on any requirement.

## The decision, restated

| | | Lean 4 | Rust+Verus | F\* → C | Isabelle+Sepref |
| --- | --- | :-: | :-: | :-: | :-: |
| **1** | certificate as a type | **yes** | no | yes | encoded |
| **2** | metatheory | **yes** | poorly | yes | **yes** |
| **3** | one artifact | **yes** | no | mostly | no |
| **4** | speed | weak | **best** | strong | **proven** |
| **5** | legible here | good | good | fair | poor |

Lean 4 wins 1, 2, 3 and 5, and loses 4 — which is the requirement
[I5](design.md#i5--soundness-is-the-kernels-job-completeness-is-the-type-systems)
was designed to make cheap to fix later.

## Reflection or reconstruction

Choosing Lean does not settle how the kernel is *run*, and the two options have
materially different trusted bases. Both exist in Lean today, which is the
reason this decision can be made on evidence rather than taste.

| | **reflection** | **reconstruction** |
| --- | --- | --- |
| the kernel is | a Lean function, with a soundness theorem | a translator producing Lean proof terms |
| checking a proof means | evaluating that function on the certificate | elaborating a term and letting Lean's kernel check it |
| trusted base | the soundness theorem, plus whatever evaluates the function | **Lean's kernel, and nothing else** |
| in Lean, today | `bv_decide` — and it admits the compiled result as an axiom, so **the Lean compiler is trusted** | `lean-smt` — kernel only |
| the cost | a larger trusted base, in exchange for speed | **incompleteness**: lean-smt lands 71% of cvc5's proofs |
| what it produces | a verdict | a proof term a third party can re-check with any Lean checker |

The honest reading is that reflection is what you do when the certificate is
large and uniform — LRAT is millions of near-identical steps, and building a
proof term per step is absurd — while reconstruction is what you do when the
certificate is small, structured, and you want the artifact. A Cooperating
Proof Calculus proof is the second kind.

**Provisional decision: reconstruction**, because the whole point of
[`kernel.md`](../../../docs/kernel.md)'s measure — *how long the argument is and
how much of it a reader can check* — is served by a trusted base of exactly one
component, and because it produces an object somebody else can check without
running our code. Revisit it the first time evaluation of a `program`
([K5](kernel-of-cvc5.md#what-eunoia-actually-is)) makes term-building
untenable, which it plausibly will: `Bitblasting.eo` is 684 lines of Eunoia
generating exactly the large-and-uniform certificates reflection is for.

A third option, worth naming so it is not reinvented: **cake_lpr's shape** — a
checker verified in a theorem prover and then compiled by a *verified compiler*
to a standalone binary, so the theorem covers the executable and neither
reflection nor a proof assistant is in the loop at run time. It is the
strongest guarantee on offer and it requires CakeML, which means HOL4, which
means abandoning requirements 1 and 3. Not available to telos, and worth
knowing precisely what is being given up.


## What would change this

Stated in advance, so the decision can be reopened honestly rather than
defended.

- **A Lean-native separation logic / refinement framework matures** and
  verifying imperative Lean becomes routine. Strengthens Lean; changes nothing
  about the decision, but removes its one weakness.
- **The prototype kernel is unusably slow in Lean** — not the solver, the
  *checker*. If checking cvc5's proof corpus in Lean is 100× ethos, requirement
  4 has moved into the kernel and F\*→C becomes the serious candidate.
- **[I3](design.md#i3--rewrites-prove-themselves-as-they-fire) turns out to be
  wrong** and telos reverts to reconstruction. Then most of the dependent typing
  is not earning its keep and Rust looks much better.
- **The project's goal changes to verifying the search.** Then Isabelle+Sepref,
  and this document is void.

## The first thing to write

Not a solver. **A Eunoia type checker in Lean**, covering
[K1, K2, K3, K6](kernel-of-cvc5.md) only — no evaluation, no `program`s — and
differential-tested against `ethos` on the proofs cvc5 already emits. It is
about 500 lines of original to model, it decides whether the language choice
survives contact, and it produces something that runs.

Ordered next steps are in [`TODO.md`](../TODO.md).
