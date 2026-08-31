# Five inversions

Each section takes one thing dokimasia measured about cvc5, states why it is
the way it is, and states what a solver built the other way round would do
instead. Each also carries **what would make it wrong**, because a design note
whose author cannot say how it fails is an advertisement.

Nothing here has been built. Every claim is a hypothesis.

---

## I1 — The answer carries its certificate

**What cvc5 does, and why.** `TheoryInferenceManager` declares
`ProofGenerator* pg = nullptr` as a default argument, and `conflict(TNode,
InferenceId)` and `lemma(TNode, InferenceId, LemmaProperty)` take no generator
at all ([H6](../../../docs/hygiene.md#h6--no-proof-must-be-said-out-loud)). So

```cpp
d_im.lemma(lem, InferenceId::ARITH_MY_NEW_INFERENCE);
```

compiles, runs, and silently produces a trust step. **The ergonomic path is the
proofless one.** That is not carelessness — it is what happens when proofs are
added to a solver that already worked, and every one of them would have had to
be retrofitted at once otherwise.

Downstream: 79 inferences fall through to a trust step by construction
([i-22](../../../docs/issues.md)), 8 trust steps are built with `TrustId::NONE`
and so cannot be attributed at all ([i-9](../../../docs/issues.md)), and
`--check-proofs-complete` exists to discover at runtime, one benchmark at a
time, which of these a given input reached.

**The inversion.** The result type is indexed by the input:

```lean
inductive Answer (phi : Formula) where
  | unsat   (pi : Proof (.not phi))
  | sat     (M : Model) (h : M |= phi)
  | unknown (r : Limitation)
```

`unsat` is uninhabited without a proof term. Not "discouraged", not "checked in
CI" — uninhabited. There is no `pg = nullptr` because there is no `pg`; the
proof is the constructor's argument, and the compiler will not let you omit it.

Three consequences, in increasing order of how much they matter:

1. **dokimasia's founding question is answered by `grep`.** *Is there a path
   through the solver that produces no proof at all?* The paths are exactly the
   `unknown` constructors. Enumerable, at compile time, with no analysis tool.
2. **A hole must name itself to typecheck.** `Limitation` is a closed inductive
   type. `TrustId::NONE` — a declared hole with no stated reason — is not
   expressible. Whether the *reason* is honest is still a human question, but
   whether one was given stops being one.
3. **Proofs cannot be off.** Contract §3 —
   [*the solver that produces the proof is the solver that solved it*](../../../docs/contract.md#why-3-is-not-a-footnote)
   — is the subtlest of cvc5's three failure modes, and it exists because
   `--produce-proofs` is a mode. Here it is not a mode. There is one solver.

**What would make it wrong.** Cost. cvc5 turns proofs off by default because
users want speed, and "there is one solver and it is the slow one" may simply
be unacceptable. The honest mitigation is that a proof term you never inspect
can be cheap — a lazily-constructed DAG, or an opaque token in a build that
compiles the checker out — but "cheap" is a measurement nobody here has taken,
and if it turns out to be 3x then this inversion has a real price and the
project should say so rather than argue.

---

## I2 — One definition of the calculus

**What cvc5 does, and why.** The calculus is stated three times: as LaTeX
`\inferrule` blocks in `cvc5_proof_rule.h`
([H9](../../../docs/hygiene.md#h9--the-rule-documentation-is-a-contract)), as
C++ checkers registered with `ProofChecker`, and as 620 `declare-rule`s in the
Eunoia signature. They are written by different people at different times, and
[`dokimasia.signature`](../../../dokimasia/signature/) exists precisely because
they can disagree — it found one
([i-21](../../../docs/issues.md): `SUBS`'s documentation omits an argument its
checker reads).

[R1](../../../docs/coupling.md#r1--emit-the-tables-cvc5-already-has) is this
repository's highest-leverage ask: *emit the tables cvc5 already has*. It is an
ask because the tables are currently recovered by parsing C++, which produced
three parser bugs in one afternoon.

**The inversion.** There is one inductive definition of the calculus. The
checker is a function over it, the printer is a function over it, the
documentation is generated from it, and the signature *is* it.
`dokimasia.signature` has nothing to check because there is nothing for the two
halves to disagree about — the class of defect it looks for is not expressible.

This is the least novel idea in the document and the most reliably valuable.
[H11](../../../docs/hygiene.md#h11--the-rare-correspondence-is-stated-not-inferred)
already observes the pattern working inside cvc5: the RARE→`ProofRewriteRule`
correspondence is *exact in both directions, and holds because it is generated*.
"Nobody maintains it, so it cannot drift" is the whole design principle,
applied once. telos applies it everywhere.

**What would make it wrong.** Nothing, in principle — but note what it costs.
A single definition means the checker's representation is the printer's
representation is the solver's representation, and those three have genuinely
different performance requirements. cvc5 states the calculus three times partly
by accident and partly because a `switch` over an enum is fast and an LF-style
term is not. Expect to need a compilation step, and expect that compilation step
to become a thing that can drift.

---

## I3 — Rewrites prove themselves as they fire

**What cvc5 does, and why.** cvc5's rewriter is a black box, and proofs of
rewrites are recovered afterwards by searching a database of RARE rules for
something that explains what the rewriter did. This is deliberate and argued in
print — Nötzli et al., FMCAD 2022, §I:

> *"we propose an alternative approach that does not rely on instrumenting the
> original rewriter … instrumenting this code to additionally produce proofs
> makes it even more complex and makes it harder to add new rewrite rules."*

The consequence is [i-4](../../../docs/issues.md), the sharpest finding in this
repository and the one it explicitly cannot fix: reconstruction is a recursive
search with **no termination guarantee** — applying a rule spawns sub-problems
(its preconditions, and the gap between its instantiated RHS and the target)
that are not provably simpler than the goal. The paper says so outright, which
is why `--proof-rewrite-rcons-rec-limit` exists at all. Measured: 92–95% of
rewrite *steps* reconstruct, but only **20–22% of proofs are fully
fine-grained**, because one coarse step spoils a proof.

So: **whether a cvc5 proof is complete depends on how long a search was allowed
to run.** That is a strange property for a contract to have, and
[`docs/kernel.md`](../../../docs/kernel.md) is right that a kernel has to
confront it rather than inherit it.

**The inversion.** The rewriter's type is

```lean
def rewrite (t : Term) : (t' : Term) × Proof (t = t')
```

There is no reconstruction, so there is no search, so there is no budget, so
`i-4` does not exist. The 38 rewrites whose reconstruction depends on a search
budget do not get a bigger budget — they have none.

**Why this is not just re-proposing what FMCAD 2022 rejected.** It is exactly
re-proposing that, and the paper's objection is real: instrumenting a rewriter
by hand makes it complex and makes rules harder to add. The claim is that the
objection is *about the language*, not about the architecture. A declarative
rule in a dependently typed host elaborates to **both** the rewrite and its
justification from one source, so there is no second thing to maintain and no
second place to get it wrong. Writing a rule stays as cheap as writing a RARE
rule; the proof is a derived artifact, not a parallel obligation.

That also kills [F1 and F3](../../../docs/rare-correspondence.md) outright — a
rule that *misstates* the rewrite, and a rule that is dead — which today are
**invisible failure modes**: F1 never matches and so silently contributes
nothing, forever.

**What would make it wrong.** This is the inversion most likely to be wrong,
and it should be tested before anything else is built on it. Three ways it
fails:

- the elaboration is not as free as claimed, and generating the justification
  turns out to need per-rule manual work — in which case the FMCAD objection
  stands and telos has learned something worth writing down;
- the rewriter needs optimisations that are not expressible as rule
  applications — caching, in-place mutation, normalisation strategies that are
  not confluent — and those are exactly the parts that resist carrying a proof;
- performance. Building a proof term for every rewrite step, when a solver
  performs millions of them, may dominate. cvc5's design avoids this cost by
  construction and telos would be paying it on every step.

**The cheapest test:** implement one theory's rewriter this way, for a fragment
where cvc5's RARE coverage is already good, and measure both the rule-authoring
cost and the runtime. Small, decisive, and does not require a solver.

---

## I4 — Safe mode is a type, not a list

**What cvc5 does, and why.** `--safe-mode=safe` promises no feature "that does
not have full proof and model support", and delivers it at *runtime*:
`SetDefaults::setDefaultsPre` turns features off by name, and
`NoOpTheoryRewriter` throws `SafeLogicException` if a disabled theory is reached
anyway. The list is hand-maintained ([i-5](../../../docs/issues.md)), and
`stringLazyPreproc` already escapes it — it declares `no_support = ["proofs"]`,
defaults to `true`, and neither mechanism disables it
([i-2](../../../docs/issues.md)). The unsafe code is compiled, linked, and one
missed guard away.

[R8](../../../docs/coupling.md#r8--safe-mode-as-a-build-time-property) asks for
the build-time version: make the safe build not *contain* the unsafe code, so a
missed guard is a link error. `ENABLE_SAFE_MODE` exists and prunes almost
nothing — five files in `src/` mention `CVC5_SAFE_MODE`, two of them only to
reword an error message.

**The inversion.** The solver core is parameterised by the set of enabled
features, and a feature with no proof support does not typecheck in the safe
instantiation. Not pruned at link time — *rejected at type-check time*, with the
error naming the feature.

Concretely: an inference that can only produce `Answer.unknown` has that in its
type, and the safe configuration instantiates `Limitation` at the empty type. A
proofless inference in a safe build is then not a runtime exception, not a link
error, but a type error at the definition site, before anything is built.

This is the second stretch goal in [`docs/kernel.md`](../../../docs/kernel.md)
— *a safe build that cannot be unsafe* — reached by construction rather than by
progressive pruning. And it makes the consistency check that document proposes
(the runtime disable list and the build-time exclusion list must agree)
vacuous: there is one list and it is the type.

**What would make it wrong.** Feature configuration in a real solver is not a
clean lattice. Options interact, some features are partially proof-producing,
and "does this have proof support" is often *fragment*-dependent rather than
feature-dependent — which is exactly [i-15](../../../docs/issues.md): the
supported fragment is not expressible as a list of kinds, because two of the
options safe mode disables gate a *logic* and a *type* rather than a kind. A
type-level encoding that cannot express that is a worse model than cvc5's list,
not a better one.

---

## I5 — Soundness is the kernel's job; completeness is the type system's

This is the one that makes the other four affordable, and it is a restatement of
dokimasia's own stance rather than a new idea.

[`docs/goals.md`](../../../docs/goals.md) is explicit: **completeness, not
soundness.** Not *is this proof step valid* but *is there a path that produces
no proof at all*. It can take that stance because something else handles
soundness — `ethos` checks the proof, so dokimasia does not have to.

telos splits the same way, and the split is what keeps it from being a decade of
work:

| | who guarantees it | how | what it costs |
| --- | --- | --- | --- |
| **soundness** | a verified kernel | a machine-checked theorem about ≈500 lines of typing and matching ([K2, K3](kernel-of-cvc5.md#what-eunoia-actually-is)) | the hard part, but small and bounded |
| **completeness** | the type system | `Answer φ` has no proofless constructor ([I1](#i1--the-answer-carries-its-certificate)) | free |
| **the search** | **nobody** | untrusted, deliberately | nothing |

**The search is not verified and should not be.** This is the LCF / de Bruijn
architecture: the search may be wrong in any way that does not produce a proof
the kernel accepts, the kernel is small enough to verify, and the type system
rules out the one remaining failure — answering without a certificate at all.

The alternative has been tried and the price is on the record. IsaSAT and versat
verify the *search* itself, and both show what that costs: IsaSAT is the fastest
verified SAT solver by a wide margin and still nowhere near CaDiCaL, and
versat's guarantee turns out to be soundness of UNSAT only — not completeness,
not termination, with some checks deferred to run time. Neither emits a
certificate, so neither gives a third party anything to check. Meanwhile
`cake_lpr`, SMTCoq, `bv_decide` and `lean-smt` all verify or kernel-check the
*checker* and leave the solver alone, and all four exist and work. The
per-tool guarantees are tabulated in
[`kernel-of-cvc5.md`](kernel-of-cvc5.md#prior-art-and-what-each-guarantee-actually-is);
they differ more than the shared word "verified" suggests.

So "a statically verified SMT solver" means, precisely:

> a solver whose **kernel** is verified, whose **completeness** is a type, and
> whose **search** is untrusted and free to be as clever and as ugly as it needs
> to be.

Any other reading of the phrase is a much larger project and probably not a
finishable one.

**What would make it wrong.** Two things. First, the kernel is only small if K4
and K5 stay out of it — and 1,009 lines of builtin operations plus 248 signature
`program`s say they will not. Second, "the search is untrusted" is only
comfortable if a rejected proof is *diagnosable*; a solver that emits a proof
the kernel rejects, with no way to attribute the rejection, is worse than one
that emits nothing. Carcara's elaborator work is the place to look for what that
costs.
